import customtkinter as ctk
from incomes import incomes_page
from expenses import expenses_page
from reports import reports_page
from settings import settings_page
import sqlite3

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x800")
        self.title("Expense Tracker")

        ctk.set_appearance_mode("dark-blue")

        self.currency = "USD"

        self.connect_database()

        self.get_categories()

        # self.income_categories = ["Other", "Salary", "Freelance", "Investment", "Rental Income", "Gift"]
        # self.expense_categories = ["Other", "Housing", "Food", "Transportation", "Healthcare", "Entertainment"]

        self.dashboard_page()

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

        self.conn.commit()

    def get_categories(self):
        self.cursor.execute("SELECT name FROM categories WHERE TYPE = 'income'")
        self.income_categories = self.cursor.fetchall()

        self.cursor.execute("SELECT name FROM categories WHERE TYPE = 'expense'")
        self.expense_categories = self.cursor.fetchall()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()

    def dashboard_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

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
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        self.header = ctk.CTkLabel(self.header_frame, text="Dashboard", font=("Helvetica", 25))
        self.header.grid(row=0, column=0, padx=20, pady=20)

        header = ctk.CTkLabel(self.menu_frame, text="", font=("Helvetica", 25))
        header.grid(row=0, column=0, padx=20, pady=20)

        # Menu Frame Buttons
        dashboard_button = ctk.CTkButton(self.menu_frame, text="Dashboard", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=self.dashboard_page)
        dashboard_button.grid(row=1, column=0, padx=0, pady=30)

        incomes_button = ctk.CTkButton(self.menu_frame, text="Incomes", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=lambda: incomes_page(self))
        incomes_button.grid(row=2, column=0, padx=0, pady=30)

        expenses_button = ctk.CTkButton(self.menu_frame, text="Expenses", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=lambda: expenses_page(self))
        expenses_button.grid(row=3, column=0, padx=0, pady=30)

        reports_button = ctk.CTkButton(self.menu_frame, text="Reports", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=lambda: reports_page(self))
        reports_button.grid(row=4, column=0, padx=0, pady=30)

        settings_button = ctk.CTkButton(self.menu_frame, text="Settings", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=lambda: settings_page(self))
        settings_button.grid(row=5, column=0, padx=0, pady=30)

        exit_button = ctk.CTkButton(self.menu_frame, text="Exit", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=self.exit)
        exit_button.grid(row=6, column=0, padx=0, pady=30)
        
        self.clear_content_frame()

        # Incomes Frame
        incomes_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        incomes_frame.grid(row=1, column=0)

        # Expenses Frame
        expenses_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        expenses_frame.grid(row=1, column=1)

        balance_label = ctk.CTkLabel(self.content_frame, text="Balance\n\n"+"2000$", font=("Helvetica", 25)).grid(row=0, column=0, columnspan=2)

        label = ctk.CTkLabel(incomes_frame, text="Latest Incomes\n", font=("Helvetica", 20)).grid(row=0, column=0)
        
        # Income Records
        money = 0 # Delete later
        for i in range(3):
            money += 100
            label = ctk.CTkLabel(incomes_frame, text="*"+str(money).join(" $")+" (Category)").grid(row=i+1, column=0, sticky="w")

        label = ctk.CTkLabel(expenses_frame, text="Latest Expenses\n", font=("Helvetica", 20)).grid(row=0, column=0)

        # Expense Records
        money = 0 # Delete later
        for i in range(3):
            money += 100
            label = ctk.CTkLabel(expenses_frame, text="*"+str(money).join(" $")+" (Category)").grid(row=i+1, column=0, sticky="w")

        favourite_income_label = ctk.CTkLabel(self.content_frame, text="Favourite Income Category").grid(row=2, column=0)
        favourite_expense_label = ctk.CTkLabel(self.content_frame, text="Favourite Expense Category").grid(row=2, column=1)

        add_income_button = ctk.CTkButton(self.content_frame, text="Add Income", font=("Helvetica", 20), height=50, fg_color="#008f11", hover_color="#00690c", corner_radius=20, command=lambda: self.add_income_expense_screen("income")).grid(row=3, column=0)
        add_expense_button = ctk.CTkButton(self.content_frame, text="Add Expense", font=("Helvetica", 20), height=50, fg_color="#a71e00", hover_color="#7d1600", corner_radius=20, command=lambda: self.add_income_expense_screen("expense")).grid(row=3, column=1)
    
    def add_income_expense_screen(self, operation):
        self.clear_content_frame()
        
        if operation == "income":
            text = "Add Income"
        else:
            text = "Add Expense"
        self.header.configure(text=text)

        # Center frame
        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=100)

        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)

        # Amount field
        label = ctk.CTkLabel(center_frame, text="Amount", font=("Helvetica", 20)).grid(row=0, column=0, sticky="w")
        
        validate_command = (self.content_frame.register(self.validate_number), "%P")

        amount_entry = ctk.CTkEntry(center_frame, placeholder_text="$", corner_radius=5, height=25, width=250, validate="key", validatecommand=validate_command)
        amount_entry.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        # Category field
        if operation == "income":
            # categories = ["Other", "Salary", "Freelance", "Investment", "Rental Income", "Gift"]
            categories = self.income_categories
        else:
            # categories = ["Other", "Housing", "Food", "Transportation", "Healthcare", "Entertainment"]
            categories = self.expense_categories
        
        selected_category = ctk.StringVar(value=categories[0])

        label = ctk.CTkLabel(center_frame, text="Category", font=("Helvetica", 20)).grid(row=2, column=0, sticky="w", pady=(25, 0))
        category_selectBox = ctk.CTkOptionMenu(center_frame, values=categories, variable=selected_category)
        category_selectBox.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

        # Note field
        label = ctk.CTkLabel(center_frame, text="Note", font=("Helvetica", 20)).grid(row=4, column=0, sticky="w", padx=10, pady=(25, 0))
        note_textBox = ctk.CTkTextbox(center_frame, corner_radius=5, height=50, width=250)
        note_textBox.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

        # Submit button
        submit_button = ctk.CTkButton(center_frame, text="Submit", font=("Helvetica", 20), corner_radius=5, height=35, width=150, command=self.dashboard_page)
        submit_button.grid(row=6, column=0, columnspan=2, sticky="w", pady=(25, 0))

        # Go Back button
        button = ctk.CTkButton(center_frame, text="Go Back", font=("Helvetica", 20), corner_radius=5, height=35, width=150, command=self.dashboard_page)
        button.grid(row=7, column=0, columnspan=2, sticky="w", pady=(5, 20))

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

    def exit(self):
        self.destroy()

if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()