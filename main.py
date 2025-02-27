# Imports
import os
import customtkinter as ck
import sqlite3

import tkinter as tk
from tkinter import ttk

# clear console for development
os.system("cls" if os.name == 'nt' else 'clear')

# /////////// /////////// /////////// /////////// /////////// 
root = tk.Tk()
root.title("TkTrello")
frm = ttk.Frame(root, padding=10)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

tabview = ck.CTkTabview(master=root, width=500, height=200)
tabview.grid(row=0, column=0, padx=0, pady=0)

# tabs
connect_tab = tabview.add("Connect")
help_tab = tabview.add("Help")

# /////////// /////////// /////////// /////////// /////////// 
# Functions
def submit_api():
    print("btn triggered")
    connect_status.configure(text="AUTHENTICATING", text_color="#FFFF00")
    connect_status.update()
    connect_entry.configure(state="disabled", fg_color="gray")
    api_submit_btn.configure(state="disabled")
    # connect_status.configure(state="disabled")

# /////////// /////////// /////////// /////////// /////////// 
# Connect Tab Entries
tabview.tab("Connect").grid_columnconfigure(0, weight=1)
tabview.tab("Connect").grid_columnconfigure(1, weight=0)
tabview.tab("Connect").grid_columnconfigure(2, weight=0)
tabview.tab("Connect").grid_columnconfigure(3, weight=0)
tabview.tab("Connect").grid_columnconfigure(4, weight=1)

tabview.tab("Connect").grid_rowconfigure(0, weight=1)
tabview.tab("Connect").grid_rowconfigure(4, weight=1)

status_label = ck.CTkLabel(master=tabview.tab("Connect"), text="STATUS: ", font=("Arial", 14, "bold"))
connect_status = ck.CTkLabel(master=tabview.tab("Connect"), text="AWAITING KEY", text_color="red")
status_label.grid(row=1, column=0, sticky="e", pady=10)
connect_status.grid(row=1, column=1, sticky="w")

api_key_label = ck.CTkLabel(master=tabview.tab("Connect"), text="API_KEY: ", font=("Arial", 14, "bold"))
connect_entry = ck.CTkEntry(master=tabview.tab("Connect"), placeholder_text="Enter API Key", width=275)
api_key_label.grid(row=2, column=0, sticky="e")
connect_entry.grid(row=2, column=1, sticky="w")

api_submit_btn = ck.CTkButton(master=tabview.tab("Connect"), text="Submit", width=275, command=submit_api)
api_submit_btn.grid(row=3, column=1, sticky="w", pady=10)

# /////////// /////////// /////////// /////////// /////////// 
# Help Tab Entries
# Centers the entry boxes in help tab
tabview.tab("Help").grid_columnconfigure(0, weight=1)
tabview.tab("Help").columnconfigure(1, weight=0)
tabview.tab("Help").columnconfigure(2, weight=0)

tabview.tab("Help").grid_rowconfigure(0, weight=1)
tabview.tab("Help").grid_rowconfigure(4, weight=1)

developer_label = ck.CTkEntry(master=tabview.tab("Help"), placeholder_text="Developer: Danny Doan", width=250)
developer_label.configure(state="disabled")
developer_label.grid(row=1, column=0, padx=0, pady=5)

developer_linkedin = ck.CTkEntry(master=tabview.tab("Help"), placeholder_text="LinkedIn: linkedin.com/in/dbdoan", width=250)
developer_linkedin.configure(state="disabled")
developer_linkedin.grid(row=2, column=0, padx=0, pady=5)

developer_github = ck.CTkEntry(master=tabview.tab("Help"), placeholder_text="Github: github.com/dbdoan", width=250)
developer_github.configure(state="disabled")
developer_github.grid(row=3, column=0, padx=0, pady=5)

# /////////// /////////// /////////// /////////// /////////// 

# Login size
root.geometry("600x250")
root.mainloop()