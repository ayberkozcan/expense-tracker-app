import customtkinter as ctk

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x800")
        self.title("Expense Tracker")

        ctk.set_appearance_mode("dark-blue")

        self.homepage()

    def homepage(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        self.header_frame.grid_rowconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.menu_frame = ctk.CTkFrame(self, fg_color="#008f11")
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2, rowspan=2)
        for i in range(7):
            if i != 0:
                self.menu_frame.grid_rowconfigure(i, weight=1)
            else:
                self.menu_frame.grid_rowconfigure(i, weight=3)
        self.menu_frame.grid_columnconfigure(0, weight=1)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkLabel(self.header_frame, text="Dashboard", font=("Helvetica", 25))
        self.header.grid(row=0, column=0, padx=20, pady=20)

        header = ctk.CTkLabel(self.menu_frame, text="", font=("Helvetica", 25))
        header.grid(row=0, column=0, padx=20, pady=20)

        dashboard_button = ctk.CTkButton(self.menu_frame, text="Dashboard", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=self.dashboard_page)
        dashboard_button.grid(row=1, column=0, padx=0, pady=30)

        expenses_button = ctk.CTkButton(self.menu_frame, text="Expenses", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=self.expenses_page)
        expenses_button.grid(row=2, column=0, padx=0, pady=30)

        incomes_button = ctk.CTkButton(self.menu_frame, text="Incomes", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=self.incomes_page)
        incomes_button.grid(row=3, column=0, padx=0, pady=30)

        reports_button = ctk.CTkButton(self.menu_frame, text="Reports", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=self.reports_page)
        reports_button.grid(row=4, column=0, padx=0, pady=30)

        settings_button = ctk.CTkButton(self.menu_frame, text="Settings", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=self.settings_page)
        settings_button.grid(row=5, column=0, padx=0, pady=30)

        exit_button = ctk.CTkButton(self.menu_frame, text="Exit", font=("Helvetica", 20), fg_color="transparent", hover_color="#00690c", command=self.exit)
        exit_button.grid(row=6, column=0, padx=0, pady=30)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def dashboard_page(self):
        self.clear_content_frame()
        self.header.configure(text="Dashboard")
        label = ctk.CTkLabel(self.content_frame, text="This is Dashboard")
        label.grid(row=0, column=0)
        return

    def expenses_page(self):
        self.clear_content_frame()
        self.header.configure(text="Expenses")
        label = ctk.CTkLabel(self.content_frame, text="This is Expenses")
        label.grid(row=0, column=0)
        return
    
    def incomes_page(self):
        self.clear_content_frame()
        self.header.configure(text="Incomes")
        label = ctk.CTkLabel(self.content_frame, text="This is Incomes")
        label.grid(row=0, column=0)
        return
    
    def reports_page(self):
        self.clear_content_frame()
        self.header.configure(text="Reports")
        label = ctk.CTkLabel(self.content_frame, text="This is Reports")
        label.grid(row=0, column=0)
        return
    
    def settings_page(self):
        self.clear_content_frame()
        self.header.configure(text="Settings")
        label = ctk.CTkLabel(self.content_frame, text="This is Settings")
        label.grid(row=0, column=0)
        return
    
    def exit(self):
        self.destroy()

if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()