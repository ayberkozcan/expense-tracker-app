import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def expenses_page(self):
    self.clear_content_frame()
    self.header.configure(text="Expenses")

    self.content_frame.grid_rowconfigure(0, weight=2)
    self.content_frame.grid_rowconfigure(1, weight=4)
    self.content_frame.grid_rowconfigure(2, weight=4)

    self.content_frame.grid_columnconfigure(0, weight=1)
    self.content_frame.grid_columnconfigure(1, weight=1)

    net_expense = 0
    
    net_expense = self.get_total_amount_by_type("expense", self.period)
    net_expense_label = ctk.CTkLabel(self.content_frame, text=f"{str(net_expense)} {self.currency}", text_color="darkred", font=("Helvetica", 30)).grid(row=0, column=0, columnspan=2, pady=20)

    # Top Frame
    top_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    top_frame.grid(row=1, column=0, columnspan=2, padx=20, sticky="nsew")
    top_frame.grid_columnconfigure((0, 1), weight=1)

    # Chart Frame
    chart_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
    chart_frame.grid(row=0, column=0, sticky="w")
    
    # Period Buttons
    this_week_button = ctk.CTkButton(chart_frame, text="This Week", width=40, command=lambda: update_period(self, "This Week"))
    this_week_button.grid(row=0, column=0, sticky="w")

    this_month_button = ctk.CTkButton(chart_frame, text="This Month", width=40, command=lambda: update_period(self, "This Month"))
    this_month_button.grid(row=0, column=1, sticky="")

    this_year_button = ctk.CTkButton(chart_frame, text="This Year", width=40, command=lambda: update_period(self, "This Year"))
    this_year_button.grid(row=0, column=2, sticky="")

    all_time_button = ctk.CTkButton(chart_frame, text="All Time", width=40, command=lambda: update_period(self, "All Time"))
    all_time_button.grid(row=0, column=3, sticky="e")

    labels = [label[0] for label in self.expense_categories]
    
    category_amounts = []
    for category in self.expense_categories:
        amount = self.get_total_amount_by_categories("expense", category[0], self.period)
        if amount:
            category_amounts.append(amount)
        else:
            category_amounts.append(0)

    sizes = []
    for i in range(len(category_amounts)):
        if sum(category_amounts) == 0:
            percent = 100 / len(self.income_categories)
        else:
            percent = (category_amounts[i] * 100) / sum(category_amounts)
        sizes.append(percent)
        
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()

    canvas.get_tk_widget().grid(row=1, column=0, pady=(10, 5), columnspan=4, sticky="nsew")
    
    # Summary Frame
    summary_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
    summary_frame.grid(row=0, column=1, sticky="nsew")
    summary_frame.grid_columnconfigure((0, 1, 2), weight=1)

    summary_header = ctk.CTkLabel(summary_frame, text="Latest Expenses", font=("Helvetica", 20)).grid(row=0, column=0, pady=(5, 20), sticky="w")
    
    # Last Records in Summary Frame
    label = ctk.CTkLabel(summary_frame, text="Amount").grid(row=1, column=0, pady=5, sticky="w")
    label = ctk.CTkLabel(summary_frame, text="Category").grid(row=1, column=1, pady=5, sticky="w")
    expenses = self.get_latest_transactions("expense", 6)
    for i, amount in enumerate(expenses):
        label = ctk.CTkLabel(summary_frame, text=f"{expenses[i][0]} {self.currency}").grid(row=i+2, column=0, pady=5, sticky="w")
        category = ctk.CTkLabel(summary_frame, text=expenses[i][1]).grid(row=i+2, column=1, sticky="w")
        details = ctk.CTkButton(summary_frame, text="Details", width=20)
        details.grid(row=i+2, column=2, sticky="")

    # Footer Frame
    footer_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    footer_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
    footer_frame.grid_columnconfigure((0, 1), weight=1)
    
    categories = [category[0] for category in self.expense_categories]
    
    selected_category = ctk.StringVar(value=categories[0])

    def update_records_by_category(selected):
        for widget in records_by_categories_frame.winfo_children():
            widget.destroy()

        expenses = self.get_latest_transactions_by_category("expense", selected, self.period, 10)
        for i, amount in enumerate(expenses):
            label = ctk.CTkLabel(records_by_categories_frame, text=f"{expenses[i][1]} {self.currency}").grid(row=i+2, column=0, pady=5, sticky="w")
            details = ctk.CTkButton(records_by_categories_frame, text="Details", width=20)
            details.grid(row=i+2, column=1, sticky="")
            id = expenses[i][0]
            delete = ctk.CTkButton(records_by_categories_frame, text="Delete", width=20, fg_color="red", hover_color="darkred", command=lambda id=id: self.delete_transaction(id, "expense"))
            delete.grid(row=i+2, column=1, sticky="e")

    categories_selectBox = ctk.CTkOptionMenu(footer_frame, values=categories, variable=selected_category, command=update_records_by_category)
    categories_selectBox.grid(row=0, column=0, pady=5, sticky="w")

    # Left Footer Frame
    records_by_categories_frame = ctk.CTkScrollableFrame(footer_frame, fg_color="transparent")
    records_by_categories_frame.grid(row=1, column=0, sticky="nsew")
    records_by_categories_frame.grid_columnconfigure((0, 1), weight=1)

    update_records_by_category(selected_category.get())

    label = ctk.CTkLabel(footer_frame, text="Total Expense by Categories "+self.period, font=("Helvetica", 15)).grid(row=0, column=1, sticky="w")

    # Right Footer Frame
    expense_by_categories_frame = ctk.CTkScrollableFrame(footer_frame, fg_color="transparent")
    expense_by_categories_frame.grid(row=1, column=1, sticky="nsew")
    expense_by_categories_frame.grid_columnconfigure((0, 1), weight=1)

    label = ctk.CTkLabel(expense_by_categories_frame, text="Category").grid(row=0, column=0, pady=5, sticky="w")
    label = ctk.CTkLabel(expense_by_categories_frame, text="Total Amount").grid(row=0, column=1, pady=5, sticky="w")

    for i, category in enumerate(categories, start=1):  
        total_amount = self.get_total_amount_by_categories("expense", category, self.period)
        text = "No data..." if not total_amount else f"{str(total_amount)} {self.currency}"
        label = ctk.CTkLabel(expense_by_categories_frame, text=category).grid(row=i+1, column=0, pady=5, sticky="w")
        label = ctk.CTkLabel(expense_by_categories_frame, text=text).grid(row=i+1, column=1, pady=5, sticky="w")

def update_period(self, period):
    self.period = period

    expenses_page(self)