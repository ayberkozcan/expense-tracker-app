import customtkinter as ctk

def settings_page(self):
    self.clear_content_frame()
    self.header.configure(text="Settings")
    label = ctk.CTkLabel(self.content_frame, text="This is Settings")
    label.grid(row=0, column=0)