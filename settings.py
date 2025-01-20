import customtkinter as ctk
from tkinter import messagebox

def settings_page(self):
    
    self.clear_content_frame()
    self.header.configure(text="Settings")

    # Currency Frame
    currency_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    currency_frame.grid(row=0, column=0, padx=20, columnspan=2, sticky="nsew")

    label = ctk.CTkLabel(currency_frame, text="Currency", font=("Helvetica", 20))
    label.grid(row=0, column=0, pady=10, sticky="w")

    currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "TRY"]
    selected_currency = ctk.StringVar(value=self.currency)
    categories_selectBox = ctk.CTkOptionMenu(currency_frame, values=currencies, variable=selected_currency, font=("Helvetica", 14), height=40)
    categories_selectBox.grid(row=1, column=0, sticky="w")

    selectBox_submit_button = ctk.CTkButton(currency_frame, text="Submit", width=50, height=40, command=lambda: change_currency(self, selected_currency.get()))
    selectBox_submit_button.grid(row=1, column=1, padx=10, sticky="w")

    # Theme & Color Frame
    theme_color_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    theme_color_frame.grid(row=1, column=0, padx=20, columnspan=2, sticky="nsew")

    label = ctk.CTkLabel(theme_color_frame, text="Theme", font=("Helvetica", 20))
    label.grid(row=0, column=0, pady=10, sticky="w")

    themes = [
        {"text": "dark", "theme": "dark"},
        {"text": "light", "theme": "light"},
        {"text": "system", "theme": "system"}
    ]

    for i, theme in enumerate(themes):
        button = ctk.CTkButton(theme_color_frame, text=theme["text"], width=50, height=40, corner_radius=10, font=("Helvetica", 14), command=lambda theme=theme: set_theme(theme["theme"]))
        button.grid(row=1, column=i, padx=(0, 10), sticky="nsew")
    
    label = ctk.CTkLabel(theme_color_frame, text="Color", font=("Helvetica", 20))
    label.grid(row=2, column=0, pady=(20, 10), sticky="w")

    colors = [
        {"text": "blue", "color": "blue"},
        {"text": "dark-blue", "color": "dark-blue"},
        {"text": "green", "color": "green"},
    ]

    for i, color in enumerate(colors):
        button = ctk.CTkButton(theme_color_frame, text=color["text"], width=50, height=40, corner_radius=10, font=("Helvetica", 14), command=lambda color=color: set_color(self, color["color"]))
        button.grid(row=3, column=i, padx=(0, 10), sticky="w")
    
    categories_button = ctk.CTkButton(self.content_frame, text="Manage Categories", height=40, command=lambda: manage_categories_screen(self))
    categories_button.grid(row=2, column=0, padx=20, columnspan=2, sticky="w")

    # Languages Frame
    languages_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    languages_frame.grid(row=3, column=0, padx=20, columnspan=2, sticky="nsew")

    label = ctk.CTkLabel(languages_frame, text="Language", font=("Helvetica", 20))
    label.grid(row=0, column=0, pady=10, sticky="w")
    
    languages = ["English", "Turkish", "German", "Spanish"]

    for i, language in enumerate(languages):
        button = ctk.CTkButton(languages_frame, text=language, fg_color="transparent", hover=None, font=("Helvetica", 14))
        # button.grid(row=1, column=i, sticky="w")

    # Delete Data
    delete_data = ctk.CTkButton(
        self.content_frame, 
        text="Delete All Data", 
        fg_color="red", 
        hover_color="darkred", 
        height=40,
        font=("Helvetica", 20),
        corner_radius=10
    )
    delete_data.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="w")

def change_currency(self, temp_currency):
    response = messagebox.askyesno(
        "Warning",
        f"Are you sure you want to change currency to {temp_currency}?"
    )
    if response:
        self.currency = temp_currency
        messagebox.showinfo(
            "Success",
            "Currency changed successfully!"
        )
        settings_page(self)

    settings_page(self)

    # Save to file

def set_theme(theme):
    ctk.set_appearance_mode(theme)

    # Save to file

def set_color(self, color):
    ctk.set_default_color_theme(color)

    settings_page(self)

    # Save to file

def create_category_frame(self, category_type, categories, row, column):
    category_label = ctk.CTkLabel(self.content_frame, text=f"{category_type}\nCategories", font=("Helvetica", 25))
    category_label.grid(row=row, column=column)

    category_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    category_frame.grid(row=row + 1, column=column, padx=40, pady=20, sticky="nsew")
    category_frame.grid_columnconfigure(0, weight=8)
    category_frame.grid_columnconfigure(1, weight=1)
    category_frame.grid_columnconfigure(2, weight=1)

    for i, category in enumerate(categories):
        label = ctk.CTkLabel(category_frame, text=category, font=("Helvetica", 15))
        label.grid(row=i, column=0, pady=10, sticky="w")
        edit_button = ctk.CTkButton(category_frame, text="Edit", width=20, fg_color="green", hover_color="darkgreen")
        edit_button.grid(row=i, column=1, sticky="e")
        delete_button = ctk.CTkButton(category_frame, text="Delete", width=20, fg_color="red", hover_color="darkred")
        delete_button.grid(row=i, column=2, sticky="e")

def manage_categories_screen(self):
    self.clear_content_frame()
    self.header.configure(text="Manage Categories")
    
    create_category_frame(self, "Income", self.income_categories, 0, 0)
    
    create_category_frame(self, "Expense", self.expense_categories, 0, 1)

    button1 = ctk.CTkButton(self.content_frame, text="Add Category", height=40, corner_radius=5, fg_color="green", hover_color="darkgreen")
    button1.grid(row=2, column=0)

    button2 = ctk.CTkButton(self.content_frame, text="Add Category", height=40, corner_radius=5, fg_color="green", hover_color="darkgreen")
    button2.grid(row=2, column=1)
