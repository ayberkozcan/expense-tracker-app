import customtkinter as ctk

def reports_page(self):
    self.clear_content_frame()
    self.header.configure(text="Reports")
    label = ctk.CTkLabel(self.content_frame, text="This is Reports")
    label.grid(row=0, column=0)