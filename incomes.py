import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def incomes_page(self):
    self.clear_content_frame()
    self.header.configure(text="Incomes")

    self.content_frame.grid_rowconfigure(0, weight=2)
    self.content_frame.grid_rowconfigure(1, weight=4)
    self.content_frame.grid_rowconfigure(2, weight=4)

    self.content_frame.grid_columnconfigure(0, weight=1)
    self.content_frame.grid_columnconfigure(1, weight=1)

    net_income = ctk.CTkLabel(self.content_frame, text="2000$", text_color="darkgreen", font=("Helvetica", 30)).grid(row=0, column=0, columnspan=2, pady=20)

    # Top Frame
    top_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    top_frame.grid(row=1, column=0, columnspan=2, padx=20, sticky="nsew")
    top_frame.grid_columnconfigure((0, 1), weight=1)

    # Chart Frame
    chart_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
    chart_frame.grid(row=0, column=0, sticky="w")

    labels = ['Category 1', 'Category 2', 'Category 3', 'Category 4']
    sizes = [25, 35, 20, 20]

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

    summary_header = ctk.CTkLabel(summary_frame, text="Latest Incomes", font=("Helvetica", 20)).grid(row=0, column=0, pady=(5, 20), sticky="w")
    
    # Last Records in Summary Frame
    label = ctk.CTkLabel(summary_frame, text="Amount").grid(row=1, column=0, pady=5, sticky="w")
    label = ctk.CTkLabel(summary_frame, text="Category").grid(row=1, column=1, pady=5, sticky="w")
    incomes = self.get_latest_transactions("income", 6)
    for i, amount in enumerate(incomes):
        label = ctk.CTkLabel(summary_frame, text=f"{incomes[i][0]} $").grid(row=i+2, column=0, pady=5, sticky="w")
        category = ctk.CTkLabel(summary_frame, text=incomes[i][1]).grid(row=i+2, column=1, sticky="w")
        details = ctk.CTkButton(summary_frame, text="Details", width=20)
        details.grid(row=i+2, column=2, sticky="")

    # Period Buttons
    this_week_button = ctk.CTkButton(chart_frame, text="This Week", width=40).grid(row=0, column=0, sticky="w")
    this_month_button = ctk.CTkButton(chart_frame, text="This Month", width=40).grid(row=0, column=1, sticky="")
    this_year_button = ctk.CTkButton(chart_frame, text="This Year", width=40).grid(row=0, column=2, sticky="")
    all_time_button = ctk.CTkButton(chart_frame, text="All Time", width=40).grid(row=0, column=3, sticky="e")

    # Footer Frame
    footer_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    footer_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
    footer_frame.grid_columnconfigure((0, 1), weight=1)
    
    categories = []
    for i, category in enumerate(self.income_categories):
        categories.append(category[0])
    
    selected_category = ctk.StringVar(value=categories[0])

    categories_selectBox = ctk.CTkOptionMenu(footer_frame, values=categories, variable=selected_category)
    categories_selectBox.grid(row=0, column=0, pady=5, sticky="w")

    # Left Footer Frame
    records_by_categories_frame = ctk.CTkScrollableFrame(footer_frame, fg_color="transparent")
    records_by_categories_frame.grid(row=1, column=0, sticky="nsew")
    records_by_categories_frame.grid_columnconfigure((0, 1), weight=1)

    incomes = self.get_latest_transactions_by_category("income", "Other", 10)

    for i, amount in enumerate(incomes):
        label = ctk.CTkLabel(records_by_categories_frame, text=f"{incomes[i][0]} $").grid(row=i+2, column=0, pady=5, sticky="w")
        details = ctk.CTkButton(records_by_categories_frame, text="Details", width=20)
        details.grid(row=i+2, column=1, sticky="")
        delete = ctk.CTkButton(records_by_categories_frame, text="Delete", width=20, fg_color="red", hover_color="darkred")
        delete.grid(row=i+2, column=1, sticky="e")

    label = ctk.CTkLabel(footer_frame, text="Total Income by Categories "+"This Week", font=("Helvetica", 15)).grid(row=0, column=1, sticky="w")

    # Right Footer Frame
    income_by_categories_frame = ctk.CTkScrollableFrame(footer_frame, fg_color="transparent")
    income_by_categories_frame.grid(row=1, column=1, sticky="nsew")

    for i, category in enumerate(categories, start=1):
        label = ctk.CTkLabel(income_by_categories_frame, text="* "+category).grid(row=i, column=0, pady=5, sticky="w")