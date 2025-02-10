import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import calendar

def reports_page(self):
    self.clear_content_frame()
    self.header.configure(text="Reports")
    
    today = datetime.today()
    year, month = today.year, today.month
    days_in_month = calendar.monthrange(year, month)[1]

    self.content_frame.grid_rowconfigure(0, weight=1)
    self.content_frame.grid_columnconfigure(0, weight=1)
    self.content_frame.grid_columnconfigure(1, weight=1)

    # Top Frame
    top_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    top_frame.grid(row=1, column=0, columnspan=2, padx=20, sticky="nsew")
    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_columnconfigure(1, weight=1)

    # Chart Frame
    chart_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
    chart_frame.grid(row=0, column=0, sticky="w")

    net_balance = ctk.CTkLabel(self.content_frame, text=str(self.balance)+"$", text_color="yellow", font=("Helvetica", 30)).grid(row=0, column=0, columnspan=2, pady=20)
    if self.period == "This Year":
        dates, balances = self.get_balance_by_date(self.period)
        x = list(range(1, 13))

        min_length = min(len(x), len(balances))
        x = x[:min_length]
        y = balances[:min_length]
    else:
        dates, balances = self.get_balance_by_month(self.period)
        x = dates
        y = balances

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(x, y, marker='o', linestyle='-', color='g')
    ax.set_xlabel("Months" if self.period == "This Year" else "Days")
    ax.set_ylabel("Dollars")
    ax.grid(True)

    if self.period == "This Month":
        ax.set_title(f"Balance for {self.current_year}-{str(self.current_month).zfill(2)}", fontsize=11, fontweight="bold")
    elif self.period == "This Year":
        ax.set_title(f"Balance for {self.selected_year}", fontsize=11, fontweight="bold")

    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    
    canvas.get_tk_widget().grid(row=1, column=0, pady=(10, 5), columnspan=4, sticky="nsew")

    if self.period == "This Month":
        left_arrow = ctk.CTkButton(chart_frame, text="<-", width=40, command=lambda: update_month(self, "back"))
        left_arrow.grid(row=2, column=3, sticky="w")
        right_arrow = ctk.CTkButton(chart_frame, text="->", width=40, command=lambda: update_month(self, "forward"))
        right_arrow.grid(row=2, column=3, sticky="e")

    if self.period == "This Year":
        left_arrow = ctk.CTkButton(chart_frame, text="<-", width=40, command=lambda: update_year(self, "back"))
        left_arrow.grid(row=2, column=3, sticky="w")
        right_arrow = ctk.CTkButton(chart_frame, text="->", width=40, command=lambda: update_year(self, "forward"))
        right_arrow.grid(row=2, column=3, sticky="e")

    # Period Buttons
    this_week_button = ctk.CTkButton(chart_frame, text="This Week", width=40)
    this_week_button.grid(row=0, column=0, sticky="w")

    this_month_button = ctk.CTkButton(chart_frame, text="This Month", width=40, command=lambda: update_period(self, "This Month"))
    this_month_button.grid(row=0, column=1, sticky="")

    this_year_button = ctk.CTkButton(chart_frame, text="This Year", width=40, command=lambda: update_period(self, "This Year"))
    this_year_button.grid(row=0, column=2, sticky="")

    all_time_button = ctk.CTkButton(chart_frame, text="All Time", width=40)
    all_time_button.grid(row=0, column=3, sticky="e")

    # Summary Frame
    summary_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
    summary_frame.grid(row=0, column=1, sticky="nsew")
    summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    summary_header = ctk.CTkLabel(summary_frame, text="Summary", font=("Helvetica", 20)).grid(row=0, column=0, pady=(5, 20), sticky="w")

    # Last Records in Summary Frame
    label = ctk.CTkLabel(summary_frame, text="Amount").grid(row=1, column=0, pady=5, sticky="w")
    label = ctk.CTkLabel(summary_frame, text="Category").grid(row=1, column=1, pady=5, sticky="w")
    label = ctk.CTkLabel(summary_frame, text="Type").grid(row=1, column=2, pady=5, sticky="w")
    transactions = self.get_all_latest_transactions(9)
    for i, amount in enumerate(transactions):
        label = ctk.CTkLabel(summary_frame, text=f"{transactions[i][0]} $").grid(row=i+2, column=0, pady=5, sticky="w")
        category = ctk.CTkLabel(summary_frame, text=transactions[i][1]).grid(row=i+2, column=1, sticky="w")
        type = ctk.CTkLabel(summary_frame, text=transactions[i][2]).grid(row=i+2, column=2, sticky="w")
        details = ctk.CTkButton(summary_frame, text="Details", width=20)
        details.grid(row=i+2, column=3, sticky="")

    # Footer Frame
    footer_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    footer_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
    # footer_frame.grid_columnconfigure((0, 1), weight=1)

    label = ctk.CTkLabel(footer_frame, text="Max Income & Expense "+self.period, font=("Helvetica", 15)).grid(row=0, column=0, sticky="w")

    # label = ctk.CTkLabel(footer_frame, text="Max Income & Expense by Categories "+self.period, font=("Helvetica", 15)).grid(row=0, column=1, sticky="w")

    # categories = ["All Categories", "Housing", "Food", "Transportation", "Healthcare", "Entertainment"]
    
    # selected_category = ctk.StringVar(value=categories[0])

    
    
    # categories_selectBox = ctk.CTkOptionMenu(footer_frame, values=categories, variable=selected_category)
    # categories_selectBox.grid(row=1, column=1, pady=15, sticky="w")

    max_income = self.get_max_by_date(self.period, "income")
    max_expense = self.get_max_by_date(self.period, "expense")

    # Left Footer Frame
    records_by_categories_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
    records_by_categories_frame.grid(row=2, column=0, sticky="nsew")

    max_income_label = ctk.CTkLabel(records_by_categories_frame, text="Max Income: "+str(max_income)+"$")
    max_income_label.grid(row=0, column=0, sticky="w")

    max_expense_label = ctk.CTkLabel(records_by_categories_frame, text="Max Expense: "+str(max_expense)+"$")
    max_expense_label.grid(row=1, column=0, sticky="w")

    # # Right Footer Frame
    # expense_by_categories_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
    # expense_by_categories_frame.grid(row=2, column=1, sticky="nsew")

    # max_income_label = ctk.CTkLabel(expense_by_categories_frame, text="Max Income: "+"$")
    # max_income_label.grid(row=0, column=0, sticky="w")

    # max_expense_label = ctk.CTkLabel(expense_by_categories_frame, text="Max Expense: "+"$")
    # max_expense_label.grid(row=1, column=0, sticky="w")

def update_period(self, period):
    self.period = period

    reports_page(self)

def update_month(self, operation):
    if operation == "back":
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
    else:
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

    self.formatted_date = f"{self.current_year}-{str(self.current_month).zfill(2)}-{str(self.current_day).zfill(2)}"

    reports_page(self)

def update_year(self, operation):
    if operation == "back":
        self.selected_year -= 1
    else:
        self.selected_year += 1

    self.formatted_year = f"{self.selected_year}-00-00"
    self.formatted_next_year = f"{self.selected_year+1}-00-00"

    reports_page(self)