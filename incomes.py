import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def incomes_page(self):
    self.clear_content_frame()
    self.header.configure(text="Incomes")

    self.content_frame.grid_rowconfigure(0, weight=1)
    self.content_frame.grid_columnconfigure(0, weight=1)

    chart_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    chart_frame.grid(row=0, column=0, columnspan=2)
    chart_frame.grid_rowconfigure(0, weight=1)
    chart_frame.grid_columnconfigure(0, weight=1)

    labels = ['Category 1', 'Category 2', 'Category 3', 'Category 4']
    sizes = [25, 35, 20, 20]

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()

    canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")