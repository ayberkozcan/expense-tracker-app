import customtkinter as ctk

def settings_page(self):
    self.clear_content_frame()
    self.header.configure(text="Settings")

    # Currency Frame
    currency_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    currency_frame.grid(row=0, column=0, padx=20, columnspan=2, sticky="nsew")

    label = ctk.CTkLabel(currency_frame, text="Currency", font=("Helvetica", 20))
    label.grid(row=0, column=0, pady=10, sticky="w")

    currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "TRY"]
    selected_currency = ctk.StringVar(value=currencies[0])
    categories_selectBox = ctk.CTkOptionMenu(currency_frame, values=currencies, variable=selected_currency, font=("Helvetica", 14), height=40)
    categories_selectBox.grid(row=1, column=0, sticky="w")

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
        button = ctk.CTkButton(theme_color_frame, text=theme["text"], width=50, height=40, corner_radius=10, font=("Helvetica", 14))
        button.grid(row=1, column=i, padx=(0, 10), sticky="nsew")
    
    label = ctk.CTkLabel(theme_color_frame, text="Color", font=("Helvetica", 20))
    label.grid(row=2, column=0, pady=(20, 10), sticky="w")

    colors = [
        {"text": "blue", "color": "blue"},
        {"text": "dark-blue", "color": "dark-blue"},
        {"text": "green", "color": "green"},
    ]

    for i, theme in enumerate(colors):
        button = ctk.CTkButton(theme_color_frame, text=theme["text"], width=50, height=40, corner_radius=10, font=("Helvetica", 14))
        button.grid(row=3, column=i, padx=(0, 10), sticky="w")
    
    # Languages Frame
    languages_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    languages_frame.grid(row=2, column=0, padx=20, columnspan=2, sticky="nsew")

    label = ctk.CTkLabel(languages_frame, text="Language", font=("Helvetica", 20))
    label.grid(row=0, column=0, pady=10, sticky="w")
    
    languages = ["English", "Turkish", "German", "Spanish"]

    for i, language in enumerate(languages):
        button = ctk.CTkButton(languages_frame, text=language, fg_color="transparent", hover=None, font=("Helvetica", 14))
        button.grid(row=1, column=i, sticky="w")

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
    delete_data.grid(row=3, column=0, padx=20, pady=10, sticky="w")
