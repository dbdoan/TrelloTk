# Imports
import os
import customtkinter as ck
import pyperclip
import sqlite3

import tkinter as tk
from tkinter import ttk

# Clear console for development
os.system("cls" if os.name == 'nt' else 'clear')

# /////////// /////////// /////////// /////////// /////////// 
# Starter
root = tk.Tk()
root.title("TkTrello")
frm = ttk.Frame(root, padding=10)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

tabview = ck.CTkTabview(master=root, width=500, height=200)
tabview.grid(row=0, column=0, padx=0, pady=0)

help_holder = "Help"
# Tabs
connect_tab = tabview.add("Connect")
help_tab = tabview.add(f"{help_holder}")


# /////////// /////////// /////////// /////////// /////////// 
# Fucntions

# Copy
def copy_to_clipboard(text, button):
    try:
        pyperclip.copy(text)
        button.configure(state="disabled", text="copied", fg_color="#FFFF00", text_color="black")
        button.after(8000, lambda: button.configure(state="enabled", fg_color="#1F6AA5", text="copy"))
    except:
        button.configure(text="error", fg_color="red", text_color="black")
        button.after(8000, lambda: button.configure(state="enabled", fg_color="#1F6AA5", text="copy"))

# API
def submit_api():
    print("btn triggered")
    if len(connect_entry.get()) < 1 or len(connect_entry.get()) != 32:
        connect_entry.delete(0, "end")
        connect_entry.configure(placeholder_text="Please enter a valid API_KEY")
    else:
        connect_status.configure(text="AUTHENTICATING", text_color="#FFFF00")
        connect_status.update()
        connect_entry.configure(state="disabled", fg_color="gray")
        api_submit_btn.configure(state="disabled")

# /////////// /////////// /////////// /////////// /////////// 
# Connect Tab
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
connect_entry = ck.CTkEntry(master=tabview.tab("Connect"), placeholder_text="Enter API Key", width=275, fg_color="gray")
api_key_label.grid(row=2, column=0, sticky="e")
connect_entry.grid(row=2, column=1, sticky="w")

api_submit_btn = ck.CTkButton(master=tabview.tab("Connect"), text="Submit", width=275, command=submit_api)
api_submit_btn.grid(row=3, column=1, sticky="w", pady=10)

# /////////// /////////// /////////// /////////// /////////// 
# Help Tab
# Centers the entry boxes in help tab
tabview.tab(f"{help_holder}").grid_columnconfigure(0, weight=1)
tabview.tab(f"{help_holder}").grid_columnconfigure(1, weight=0)
tabview.tab(f"{help_holder}").grid_columnconfigure(2, weight=0)
tabview.tab(f"{help_holder}").grid_columnconfigure(3, weight=1)
# tabview.tab(f"{help_holder}").grid_columnconfigure(4, weight=1)

tabview.tab(f"{help_holder}").grid_rowconfigure(0, weight=1)
tabview.tab(f"{help_holder}").grid_rowconfigure(4, weight=1)

developer_label = ck.CTkEntry(master=tabview.tab(f"{help_holder}"), placeholder_text="Developer: Danny Doan", width=250)
developer_label.configure(state="disabled")
developer_label.grid(row=1, column=1, padx=0, pady=5, sticky="w")

developer_linkedin = ck.CTkEntry(master=tabview.tab(f"{help_holder}"), placeholder_text="LinkedIn: linkedin.com/in/dbdoan", width=250)
developer_linkedin.configure(state="disabled")
developer_linkedin.grid(row=2, column=1, padx=0, pady=5, sticky="w")

developer_github = ck.CTkEntry(master=tabview.tab(f"{help_holder}"), placeholder_text="Github: github.com/dbdoan", width=250)
developer_github.configure(state="disabled")
developer_github.grid(row=3, column=1, padx=0, pady=5, sticky="w")

copy_paste_btn_lnkin = ck.CTkButton(master=tabview.tab(f"{help_holder}"), text="copy", width=50, font=("Arial", 14), hover_color="#a5a5a5", text_color="black", command=lambda: copy_to_clipboard("linkedin.com/in/dbdoan", copy_paste_btn_lnkin))
copy_paste_btn_lnkin.grid(row=2, column=2, padx=5, sticky="w")
copy_paste_btn_gh = ck.CTkButton(master=tabview.tab(f"{help_holder}"), text="copy", width=50, font=("Arial", 14), hover_color="#a5a5a5", text_color="black", command=lambda: copy_to_clipboard("github.com/dbdoan", copy_paste_btn_gh))
copy_paste_btn_gh.grid(row=3, column=2, padx=5, sticky="w")

# /////////// /////////// /////////// /////////// /////////// 
# Root End
root.geometry("600x250")
root.mainloop()