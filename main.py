import os
import json
import sqlite3
from datetime import datetime, timedelta
from tkinter import PhotoImage, messagebox

import customtkinter as ctk
from tkcalendar import Calendar

from incomes import incomes_page
from expenses import expenses_page
from reports import reports_page
from settings import settings_page

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x800")
        self.title("Expense Tracker")

        ctk.set_appearance_mode("dark-blue")

        self.currencies = ["$", "€", "¥", "£", "A$", "C$", "CHF", "¥", "kr", "₺"]
        
        settings = self.load_settings()
        self.theme = settings.get("theme")
        self.color = settings.get("color")
        self.currency = settings.get("currency")

        ctk.set_appearance_mode(self.theme)
        ctk.set_default_color_theme(self.color)

        # self.currency = "$"
        self.period = "This Week"
        self.current_day = datetime.now().day
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.selected_year = datetime.now().year

        self.formatted_date = f"{self.current_year}-{str(self.current_month).zfill(2)}-{str(self.current_day).zfill(2)}"
        self.formatted_year = f"{self.selected_year}-00-00"
        self.formatted_next_year = f"{self.selected_year+1}-00-00"

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.homepage_icon_path = os.path.join(BASE_DIR, "icons/homepage_icon.png")
        self.dollar_icon_path = os.path.join(BASE_DIR, "icons/dollar_icon.png")
        self.reports_icon_path = os.path.join(BASE_DIR, "icons/stats_icon.png")
        self.settings_icon_path = os.path.join(BASE_DIR, "icons/settings_icon.png")
        self.exit_icon_path = os.path.join(BASE_DIR, "icons/exit_icon.png")

        self.connect_database()

        self.get_categories()

        self.balance = self.get_balance()

        self.dashboard_page()

    def load_settings(self):
        try:
            with open("data/settings.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"theme": "dark", "color": "dark-blue", "currency": "$"}

    def connect_database(self):
        self.conn = sqlite3.connect("data/database/categories.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                date DATE,
                category TEXT,
                type TEXT,
                note TEXT
            )
        """)
        self.conn.commit()
    
    def get_balance(self):
        balance = self.cursor.execute("""
            SELECT
                (SELECT COALESCE(SUM (amount), 0) FROM transactions WHERE type = 'income' ) - 
                (SELECT COALESCE(SUM (amount), 0) FROM transactions WHERE type = 'expense') AS balance;
            """
        ).fetchone()

        return balance[0]
    
    def get_balance_by_month(self, period):
        year, month = map(int, self.formatted_date[:7].split("-"))
        if month == 12:
            next_ym = f"{year + 1}-01"
        else:
            next_ym = f"{year}-{month+1:02d}"

        balance = self.cursor.execute("""
            SELECT 
                strftime('%Y-%m-%d', date) AS day,
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) -
                COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS balance
            FROM transactions
            WHERE date >= ? AND date < ?
            GROUP BY day
            ORDER BY day;
            """
        , (self.formatted_date[:7], next_ym)).fetchall()

        days = [datetime.strptime(data[0], '%Y-%m-%d').day for data in balance]

        balances_per_day = [data[1] for data in balance]
        total_balance = []

        for i, amount in enumerate(balances_per_day):
            total_balance.append(amount)
            total_balance[i] = sum(total_balance)

        return days, total_balance
    
    def get_balance_by_date(self, period):
        balance = self.cursor.execute("""
            SELECT 
                strftime('%Y-%m', date) AS month,
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) -
                COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS balance
            FROM transactions
            WHERE date >= ? AND date < ?
            GROUP BY month
            ORDER BY month;
            """
        , (self.formatted_year, self.formatted_next_year)).fetchall()

        months = [datetime.strptime(data[0], '%Y-%m').month for data in balance]

        balances_per_month = [data[1] for data in balance]
        total_balance = []

        for i, amount in enumerate(balances_per_month):
            total_balance.append(amount)
            total_balance[i] = sum(total_balance)

        return months, total_balance
    
    def get_latest_transactions(self, type, limit=3):
        transactions = self.cursor.execute("SELECT amount, category, transaction_id FROM transactions WHERE type = ? ORDER BY transaction_id DESC LIMIT ?", (type, limit)).fetchall()
        
        return transactions
    
    def get_all_latest_transactions(self, limit=3):
        transactions = self.cursor.execute("SELECT amount, category, type, transaction_id FROM transactions ORDER BY date DESC LIMIT ?", (str(limit))).fetchall()

        return transactions

    def get_categories(self):
        self.cursor.execute("SELECT name FROM categories WHERE TYPE = 'income'")
        self.income_categories = self.cursor.fetchall()

        self.cursor.execute("SELECT name FROM categories WHERE TYPE = 'expense'")
        self.expense_categories = self.cursor.fetchall()

    def get_fav_category(self, type):
        try:
            fav_category = self.cursor.execute("""
                SELECT COUNT(*) AS total_transaction, category
                FROM transactions 
                WHERE type = ?
                GROUP BY category
                ORDER BY total_transaction DESC
                LIMIT 1;
                """, 
            (type,)).fetchone()[1]
            
            return fav_category
        except:
            print("no fav category data")

    def get_total_amount_by_type(self, type, period):
        time = self.period_to_date(period)
        total_amount = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = ? AND date >= ?", (type, time)).fetchone()[0]

        if not total_amount:
            total_amount = 0

        return total_amount

    def get_latest_transactions_by_category(self, type, category, period, limit=3):
        time = self.period_to_date(period)
        transactions = self.cursor.execute("SELECT transaction_id, amount, category FROM transactions WHERE type = ? AND category = ? AND date >= ? ORDER BY transaction_id DESC LIMIT ?", (type, category, time, limit)).fetchall()

        return transactions

    def get_total_amount_by_categories(self, type, category, period):
        time = self.period_to_date(period)
        total_amount = self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = ? AND category = ? AND date >= ?", (type, category, time)).fetchone()[0]

        return total_amount
    
    def delete_transaction(self, id, page):
        control = messagebox.askyesno("Delete Transaction", "Are you sure you want to delete this transaction?")
        if control:
            self.cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (id,))
            self.conn.commit()
            
            if page == "income":
                incomes_page(self)
            else:
                expenses_page(self)

    def get_used_categories(self, type):
        categories = self.cursor.execute("SELECT category FROM transactions WHERE type = ?", (type,)).fetchall()

        return categories
    
    def get_max_by_date(self, period, type):
        time = self.period_to_date(period)
        max_amount = self.cursor.execute("SELECT MAX(amount) FROM transactions WHERE type = ? AND date >= ?", (type, time)).fetchone()[0]
        
        max_amount = 0 if not max_amount else max_amount

        return max_amount 
    
    def get_transaction_details(self, id):
        details = self.cursor.execute("SELECT amount, date, category, type, note FROM transactions WHERE transaction_id = ?", (id,)).fetchall()[0]

        return details
    
    def period_to_date(self, period):
        today = datetime.today()

        if period == "This Week":
            start_of_week = today - timedelta(days=7)
            return start_of_week.date().strftime("%Y-%m-%d")

        if period == "This Month":
            start_of_month = today - timedelta(days=30)
            return start_of_month.date().strftime("%Y-%m-%d")

        if period == "This Year":
            start_of_year = today - timedelta(days=365)
            return start_of_year.date().strftime("%Y-%m-%d")

        if period == "All Time":
            start_of_time = datetime(2000, 1, 1)
            return start_of_time.date().strftime("%Y-%m-%d")
        
        return today.date().strftime("%Y-%m-%d")

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()

    def dashboard_page(self):
        if hasattr(self, "details_window") and self.details_window.winfo_exists():
            self.details_window.destroy()

        for widget in self.winfo_children():
            widget.grid_forget()

        self.balance = self.get_balance()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=9)

        # Header Frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        self.header_frame.grid_rowconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(0, weight=1)

        # Menu Frame
        self.menu_frame = ctk.CTkFrame(self, fg_color="#008f11")
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2, rowspan=2)
        for i in range(7):
            if i != 0:
                self.menu_frame.grid_rowconfigure(i, weight=1)
            else:
                self.menu_frame.grid_rowconfigure(i, weight=3)
        self.menu_frame.grid_columnconfigure(0, weight=1)

        # Content Frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=5)
        self.content_frame.grid_rowconfigure(2, weight=1)
        self.content_frame.grid_rowconfigure(3, weight=3)
        self.content_frame.grid_columnconfigure((0, 1), weight=1)

        self.header = ctk.CTkLabel(self.header_frame, text="Dashboard", font=("Helvetica", 25))
        self.header.grid(row=0, column=0, padx=20, pady=20)

        header = ctk.CTkLabel(self.menu_frame, text="", font=("Helvetica", 25))
        header.grid(row=0, column=0, padx=20, pady=20)

        # Menu Frame Buttons
        self.homepage_icon = PhotoImage(file=self.homepage_icon_path)
        self.homepage_icon = self.homepage_icon.subsample(15, 15)

        self.dollar_icon = PhotoImage(file=self.dollar_icon_path)
        self.dollar_icon = self.dollar_icon.subsample(15, 15)

        self.reports_icon = PhotoImage(file=self.reports_icon_path)
        self.reports_icon = self.reports_icon.subsample(15, 15)

        self.settings_icon = PhotoImage(file=self.settings_icon_path)
        self.settings_icon = self.settings_icon.subsample(15, 15)

        self.exit_icon = PhotoImage(file=self.exit_icon_path)
        self.exit_icon = self.exit_icon.subsample(15, 15)

        dashboard_button = ctk.CTkButton(
            self.menu_frame, 
            text="Dashboard", 
            font=("Helvetica", 20), 
            fg_color="transparent", 
            hover_color="#00690c", 
            command=self.dashboard_page,
            image=self.homepage_icon,
            compound="left"
        )
        dashboard_button.grid(row=1, column=0, padx=0, pady=30, sticky="w")

        incomes_button = ctk.CTkButton(
            self.menu_frame, 
            text="Incomes", 
            font=("Helvetica", 20), 
            fg_color="transparent",  
            hover_color="#005f00",  
            command=lambda: incomes_page(self),
            image=self.dollar_icon,
            compound="left"
        )
        incomes_button.grid(row=2, column=0, padx=0, pady=30, sticky="w")

        expenses_button = ctk.CTkButton(
            self.menu_frame, 
            text="Expenses", 
            font=("Helvetica", 20), 
            fg_color="transparent",  
            hover_color="#8b0000",  
            command=lambda: expenses_page(self),
            image=self.dollar_icon,
            compound="left"
        )
        expenses_button.grid(row=3, column=0, padx=0, pady=30, sticky="w")

        reports_button = ctk.CTkButton(
            self.menu_frame, 
            text="Reports", 
            font=("Helvetica", 20), 
            fg_color="transparent", 
            hover_color="#00690c", 
            command=lambda: reports_page(self),
            image=self.reports_icon,
            compound="left"
        )
        reports_button.grid(row=4, column=0, padx=0, pady=30, sticky="w")

        settings_button = ctk.CTkButton(
            self.menu_frame, 
            text="Settings", 
            font=("Helvetica", 20), 
            fg_color="transparent", 
            hover_color="#00690c", 
            command=lambda: settings_page(self),
            image=self.settings_icon,
            compound="left"
        )
        settings_button.grid(row=5, column=0, padx=0, pady=30, sticky="w")

        exit_button = ctk.CTkButton(
            self.menu_frame, 
            text="Exit", 
            font=("Helvetica", 20), 
            fg_color="transparent", 
            hover_color="#8b0000",  
            command=self.exit,
            image=self.exit_icon,
            compound="left"
        )
        exit_button.grid(row=6, column=0, padx=0, pady=30, sticky="w")
        
        self.clear_content_frame()
        
        balance_label = ctk.CTkLabel(self.content_frame, text=f"Balance\n\n{str(self.balance)} {self.currency}", font=("Helvetica", 25)).grid(row=0, column=0, columnspan=2)

        # Incomes Frame
        incomes_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        incomes_frame.grid(row=1, column=0, sticky="we")
        incomes_frame.grid_rowconfigure(0, weight=1)
        incomes_frame.grid_rowconfigure(1, weight=9)
        incomes_frame.grid_columnconfigure((0, 1), weight=1)

        # Expenses Frame
        expenses_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        expenses_frame.grid(row=1, column=1, sticky="we")
        expenses_frame.grid_rowconfigure(0, weight=1)
        expenses_frame.grid_rowconfigure(1, weight=9)
        expenses_frame.grid_columnconfigure((0, 1), weight=1)

        label = ctk.CTkLabel(incomes_frame, text="Latest Incomes\n", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2)
        amount_label = ctk.CTkLabel(incomes_frame, text="Amount", font=("Helvetica", 18)).grid(row=1, column=0)
        category_label = ctk.CTkLabel(incomes_frame, text="Category", font=("Helvetica", 18)).grid(row=1, column=1)
        
        incomes = self.get_latest_transactions("income")
        # Income Records
        if len(incomes) < 3:
            for i in range(3):
                if len(incomes) == 0 and i == 0:
                    label = ctk.CTkLabel(incomes_frame, text="No data found!")
                    label.grid(row=i+2, column=0, sticky="")
                else:
                    text = ""
                label = ctk.CTkLabel(incomes_frame, text="")
                label.grid(row=i+2, column=0, sticky="w")
        for i, amount in enumerate(incomes):
            label = ctk.CTkLabel(incomes_frame, text=f"{incomes[i][0]} {self.currency}").grid(row=i+2, column=0)
            category = ctk.CTkLabel(incomes_frame, text=incomes[i][1]).grid(row=i+2, column=1)

        label = ctk.CTkLabel(expenses_frame, text="Latest Expenses\n", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2)
        amount_label = ctk.CTkLabel(expenses_frame, text="Amount", font=("Helvetica", 18)).grid(row=1, column=0)
        category_label = ctk.CTkLabel(expenses_frame, text="Category", font=("Helvetica", 18)).grid(row=1, column=1)

        expenses = self.get_latest_transactions("expense")
        # Expense Records
        if len(expenses) < 3:
            for i in range(3):
                if len(expenses) == 0 and i == 0:
                    label = ctk.CTkLabel(expenses_frame, text="No data found!")
                    label.grid(row=i+2, column=0, sticky="w")
                else:
                    text = ""
                label = ctk.CTkLabel(expenses_frame, text="")
                label.grid(row=i+2, column=0, sticky="w")
        for i, amount in enumerate(expenses):
            label = ctk.CTkLabel(expenses_frame, text=f"{expenses[i][0]} {self.currency}").grid(row=i+2, column=0)
            category = ctk.CTkLabel(expenses_frame, text=expenses[i][1]).grid(row=i+2, column=1)

        fav_income_category = self.get_fav_category("income")
        fav_expense_category = self.get_fav_category("expense")

        favourite_income_label = ctk.CTkLabel(self.content_frame, text=f"Favourite Income Category\n\n{fav_income_category}").grid(row=2, column=0)
        favourite_expense_label = ctk.CTkLabel(self.content_frame, text=f"Favourite Expense Category\n\n{fav_expense_category}").grid(row=2, column=1)

        add_income_button = ctk.CTkButton(self.content_frame, text="Add Income", font=("Helvetica", 20), height=50, fg_color="#008f11", hover_color="#00690c", corner_radius=20, command=lambda: self.add_transaction_screen("income")).grid(row=3, column=0)
        add_expense_button = ctk.CTkButton(self.content_frame, text="Add Expense", font=("Helvetica", 20), height=50, fg_color="#a71e00", hover_color="#7d1600", corner_radius=20, command=lambda: self.add_transaction_screen("expense")).grid(row=3, column=1)

    def add_transaction_screen(self, operation):
        self.clear_content_frame()

        categories = []
        
        if operation == "income":
            text = "Add Income"
        else:
            text = "Add Expense"
        self.header.configure(text=text)

        # Center frame
        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=50)

        center_frame.grid_columnconfigure((0, 1), weight=1)

        # Amount field
        label = ctk.CTkLabel(center_frame, text=f"Amount ({self.currency})", font=("Helvetica", 20)).grid(row=0, column=0, sticky="w")
        
        validate_command = (self.content_frame.register(self.validate_number), "%P")

        amount_entry = ctk.CTkEntry(center_frame, placeholder_text=self.currency, corner_radius=5, height=25, width=250, validate="key", validatecommand=validate_command)
        amount_entry.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        # Category field
        if operation == "income":
            for i, category in enumerate(self.income_categories):
                categories.append(category[0])
        else:
            for i, category in enumerate(self.expense_categories):
                categories.append(category[0])
        
        selected_category = ctk.StringVar(value=categories[0])

        label = ctk.CTkLabel(center_frame, text="Category", font=("Helvetica", 20)).grid(row=2, column=0, sticky="w", pady=(25, 0))
        category_selectBox = ctk.CTkOptionMenu(center_frame, values=categories, variable=selected_category)
        category_selectBox.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

        # Note field
        label = ctk.CTkLabel(center_frame, text="Note (Optional)", font=("Helvetica", 20)).grid(row=4, column=0, sticky="w", padx=10, pady=(25, 0))
        note_textBox = ctk.CTkTextbox(center_frame, corner_radius=5, height=50, width=250)
        note_textBox.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

        # Date field
        calendar = Calendar(center_frame, background="darkgreen", selectmode="day", date_pattern="yyyy-mm-dd")
        calendar.grid(row=6, column=0, columnspan=2, sticky="w", pady=(25, 0))

        # Submit button
        submit_button = ctk.CTkButton(
            center_frame, text="Submit", 
            font=("Helvetica", 20), 
            corner_radius=5, 
            height=35, 
            width=150, 
            command=lambda: self.add_transaction_to_db(amount_entry.get(), category_selectBox.get(), note_textBox.get("1.0", "end-1c") if note_textBox.get("1.0", "end-1c") != "" else "", calendar.get_date(), operation)
        )
        submit_button.grid(row=7, column=0, columnspan=2, sticky="w", pady=(25, 0))

        # Go Back button
        button = ctk.CTkButton(center_frame, text="Go Back", font=("Helvetica", 20), corner_radius=5, height=35, width=150, command=self.dashboard_page)
        button.grid(row=8, column=0, columnspan=2, sticky="w", pady=(5, 20))

        def focus_selectbox(event):
            category_selectBox.focus_set()

        def focus_textBox(event):
            note_textBox.focus_set()

        def on_submit(event):
            submit_button.focus_set()

        amount_entry.bind("<Return>", focus_selectbox)
        category_selectBox.bind("<Return>", focus_textBox)
        note_textBox.bind("<Return>", on_submit)

    def validate_number(self, input_value):
        if input_value == "" or input_value.isdigit():
            return True
        return False

    def add_transaction_to_db(self, amount, category, note, date, operation):
        if amount == 0 or not amount:
            messagebox.showerror("Error", "Amount cannot be 0!")
            return
        
        self.cursor.execute("""
            INSERT INTO transactions (amount, date, category, type, note) 
            VALUES (:amount, :date, :category, :type, :note)
        """, {
            "amount": amount,
            "date": date,
            "category": category,
            "type": operation,
            "note": note
        })
        self.conn.commit()

        messagebox.showinfo("Success", "Transaction successful!")
        self.dashboard_page()

    # This functions runs on Incomes, Expenses and Reports screens
    def show_details_window(self, id):
        details = self.get_transaction_details(id)

        if hasattr(self, "details_window") and self.details_window.winfo_exists():
            self.details_window.destroy()

        self.details_window = ctk.CTkToplevel(self)
        self.details_window.title("Details")
        self.details_window.geometry("300x400")

        for i in range(6):
            self.details_window.grid_rowconfigure(i, weight=1)
        self.details_window.grid_columnconfigure(0, weight=1)
        self.details_window.grid_columnconfigure(1, weight=9)

        labels = ["Amount", "Date", "Category", "Type", "Note"]
        for i, text in enumerate(labels):
            ctk.CTkLabel(self.details_window, text=text).grid(row=i, column=0, padx=20, sticky="w")
        
        for i, text in enumerate(details):
            text="No data..." if not details[4] and i==4 else text
            ctk.CTkLabel(self.details_window, text=text).grid(row=i, column=1, padx=20, sticky="w")

        button = ctk.CTkButton(
            self.details_window, 
            text="Delete Transaction", 
            fg_color="red", 
            hover_color="darkred", 
            corner_radius=20
            )
        button.grid(row=i+1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    def exit(self):
        self.destroy()

if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()