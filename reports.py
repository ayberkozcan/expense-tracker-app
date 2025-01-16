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

    net_balance = ctk.CTkLabel(self.content_frame, text="500$", text_color="yellow", font=("Helvetica", 30)).grid(row=0, column=0, columnspan=2, pady=20)

    # Top Frame
    top_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
    top_frame.grid(row=1, column=0, columnspan=2, padx=20, sticky="nsew")
    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_columnconfigure(1, weight=1)

    # Chart Frame
    chart_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
    chart_frame.grid(row=0, column=0, sticky="w")

    x = list(range(1, days_in_month + 1))
    y = [i * 2 for i in x]

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(x, y, marker='o', linestyle='-', color='g')
    ax.set_xlabel("Days")
    ax.set_ylabel("Dollars")
    ax.grid(True)

    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    
    canvas.get_tk_widget().grid(row=1, column=0, pady=(10, 5), columnspan=4, sticky="nsew")

    # Period Buttons
    this_week_button = ctk.CTkButton(chart_frame, text="This Week", width=40).grid(row=0, column=0)
    this_month_button = ctk.CTkButton(chart_frame, text="This Month", width=40).grid(row=0, column=1)
    this_year_button = ctk.CTkButton(chart_frame, text="This Year", width=40).grid(row=0, column=2)
    all_time_button = ctk.CTkButton(chart_frame, text="All Time", width=40).grid(row=0, column=3)

    # Summary Frame
    summary_frame = ctk.CTkScrollableFrame(top_frame, fg_color="transparent")
    summary_frame.grid(row=0, column=1, sticky="nsew")

    summary_header = ctk.CTkLabel(summary_frame, text="Summary (Last 10)", font=("Helvetica", 20)).grid(row=0, column=0, pady=(5, 20), sticky="w")
    
    # Last 10 Records in Summary Frame
    money = 0 # Delete later
    for i in range(10):
        money += 100
        label = ctk.CTkLabel(summary_frame, text="*"+str(money).join(" $")+" (Category)").grid(row=i+1, column=0, pady=5, sticky="w")
        details = ctk.CTkButton(summary_frame, text="Details", width=20).grid(row=i+1, column=1)