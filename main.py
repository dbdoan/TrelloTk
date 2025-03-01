# IMPORTS
import os
import customtkinter as ck
import json
import pyperclip
import requests
import sqlite3
import time
import tkinter as tk
from tkinter import ttk

from PIL import Image

# Clear console for development
os.system("cls" if os.name == 'nt' else 'clear')

# /////////// /////////// /////////// /////////// /////////// 
# KEYS
with open("config.json", "r") as f:
    config = json.load(f)

TEST_API_KEY = config["API_KEY"]
TEST_TOKEN = config["TOKEN"]
TEST_BOARD_ID = config["BOARD_ID"]

# /////////// /////////// /////////// /////////// /////////// 
# STARTER
root = tk.Tk()
root.title("TkTrello")
frm = ttk.Frame(root, padding=10)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

tabview = ck.CTkTabview(master=root, width=500, height=250)
tabview.grid(row=0, column=0, padx=0, pady=0)

help_holder = "Help"
# Tabs
connect_tab = tabview.add("Connect")
help_tab = tabview.add(f"{help_holder}")

# Images
copy_img = ck.CTkImage(light_image=Image.open("img/copy.png"), size=(15, 20))
paste_img = ck.CTkImage(light_image=Image.open("img/paste.png"), size=(15, 20))

# /////////// /////////// /////////// /////////// /////////// 
# FUNCTIONS

# Copy
def copy_to_clipboard(text, button):
    pyperclip.copy(text)
    button.configure(state="disabled", fg_color="#FFFF00")
    button.after(8000, lambda: button.configure(state="normal", fg_color="#1F6AA5"))
        
# Paste
def paste_to_clipboard(entry_field, button):
    entry_field.delete(0, "end")
    entry_field.insert(0, pyperclip.paste())
    button.configure(state="disabled", fg_color="#FFFF00")
    button.after(8000, lambda: button.configure(state="normal", fg_color="#1F6AA5"))

# Authentication
def key_token_validation(API_KEY, TOKEN):
    url = f"https://api.trello.com/1/members/me/boards?key={API_KEY}&token={TOKEN}"
    query = {
        'key': API_KEY,
        'token': TOKEN
    }
    
    response = requests.get(
        url, 
        params=query
    )
    
    return response.status_code
    
# API
def submit_api():
    # print("btn triggered.")
    user_api_key = api_key_input.get()
    user_token = api_token_input.get()
    
    time.sleep(.3)
    connect_status.configure(text="AUTHENTICATING", text_color="#FFFF00")
    connect_status.update()
    api_key_input.configure(state="disabled", fg_color="gray")
    api_token_input.configure(state="disabled", fg_color="gray")
    api_submit_btn.configure(state="disabled")
    
    if len(api_key_input.get()) < 1:
        api_key_input.delete(0, "end")
        api_key_input.configure(placeholder_text="oops, it seems you left this field empty!")
    elif len(api_token_input.get()) < 1:
        api_token_input.delete(0, "end")
        api_token_input.configure(placeholder_text="oops, it seems you left this field empty!")
    else:
        if key_token_validation(user_api_key, user_token) == 200:
            time.sleep(1)
            connect_status.configure(text="VALID", text_color="#39FF14")
            connect_status.update()
        else:
            time.sleep(1)
            connect_status.configure(text="INVALID; RECHECK KEY OR TOKEN.", text_color="red")
            connect_status.update()
            api_key_input.configure(state="normal")
            api_token_input.configure(state="normal")
            api_submit_btn.configure(state="normal")

# /////////// /////////// /////////// /////////// /////////// 
# CONNECT TAB
tabview.tab("Connect").grid_columnconfigure(0, weight=1)
tabview.tab("Connect").grid_columnconfigure(1, weight=0)
tabview.tab("Connect").grid_columnconfigure(2, weight=0)
tabview.tab("Connect").grid_columnconfigure(3, weight=0)
tabview.tab("Connect").grid_columnconfigure(4, weight=1)

tabview.tab("Connect").grid_rowconfigure(0, weight=1)
tabview.tab("Connect").grid_rowconfigure(4, weight=1)

status_label = ck.CTkLabel(master=tabview.tab("Connect"), text="STATUS: ", font=("Arial", 14, "bold"))
connect_status = ck.CTkLabel(master=tabview.tab("Connect"), text="AWAITING KEY", font=("Arial", 12, "bold"), text_color="red")
status_label.grid(row=1, column=0, sticky="e", pady=10)
connect_status.grid(row=1, column=1, sticky="w")

api_key_label = ck.CTkLabel(master=tabview.tab("Connect"), text="API_KEY: ", font=("Arial", 14, "bold"))
api_key_input = ck.CTkEntry(master=tabview.tab("Connect"), placeholder_text="[paste api key]", width=275, fg_color="gray", placeholder_text_color="#A8A8A8")
api_key_label.grid(row=2, column=0, sticky="e")
api_key_input.grid(row=2, column=1, sticky="w")

token_label = ck.CTkLabel(master=tabview.tab("Connect"), text="TOKEN: ", font=("Arial", 14, "bold"))
api_token_input = ck.CTkEntry(master=tabview.tab("Connect"), placeholder_text="[paste token]", width=275, fg_color="gray", placeholder_text_color="#A8A8A8")
token_label.grid(row=3, column=0, sticky="e")
api_token_input.grid(row=3, column=1, sticky="w", pady=5)

api_submit_btn = ck.CTkButton(master=tabview.tab("Connect"), text="Connect", width=275, command=submit_api)
api_submit_btn.grid(row=4, column=1, sticky="w", pady=10)

paste_btn_apikey = ck.CTkButton(master=tabview.tab("Connect"), width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: paste_to_clipboard(api_key_input, paste_btn_apikey), image=paste_img)
paste_btn_apikey.grid(row=2, column=2, padx=5, sticky="w")

paste_btn_token = ck.CTkButton(master=tabview.tab("Connect"), width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: paste_to_clipboard(api_token_input, paste_btn_token), image=paste_img)
paste_btn_token.grid(row=3, column=2, padx=5, sticky="w")

# /////////// /////////// /////////// /////////// /////////// 
# HELP TAB
# Centers the entry boxes in help tab]
tabview.tab(f"{help_holder}").grid_columnconfigure(0, weight=1)
tabview.tab(f"{help_holder}").grid_columnconfigure(1, weight=0)
tabview.tab(f"{help_holder}").grid_columnconfigure(2, weight=0)
tabview.tab(f"{help_holder}").grid_columnconfigure(3, weight=1)

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

copy_btn_lnkin = ck.CTkButton(master=tabview.tab(f"{help_holder}"), width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: copy_to_clipboard("linkedin.com/in/dbdoan", copy_btn_lnkin), image=copy_img)
copy_btn_lnkin.grid(row=2, column=2, padx=5, sticky="w")
copy_btn_gh = ck.CTkButton(master=tabview.tab(f"{help_holder}"), width=20, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: copy_to_clipboard("github.com/dbdoan", copy_btn_gh), image=copy_img)
copy_btn_gh.grid(row=3, column=2, padx=5, sticky="w")

# /////////// /////////// /////////// /////////// /////////// 
# Root End
root.geometry("600x300")
root.mainloop()