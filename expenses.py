import customtkinter as ctk

def expenses_page(app):
    app.clear_content_frame()
    app.header.configure(text="Expenses")
    label = ctk.CTkLabel(app.content_frame, text="This is Expenses")
    label.grid(row=0, column=0)