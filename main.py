# IMPORTS
import os
import customtkinter as ck
import json
import requests
import sqlite3
import time
import tkinter as tk
from tkinter import ttk

from PIL import Image

# Clear console for development
os.system("cls" if os.name == 'nt' else 'clear')

# /////////// /////////// /////////// /////////// /////////// 
# TEST KEYS
with open("config.json", "r") as f:
    config = json.load(f)

TEST_API_KEY = config["API_KEY"]
TEST_TOKEN = config["TOKEN"]
TEST_BOARD_ID = config["BOARD_ID"]

# /////////// /////////// /////////// /////////// /////////// 
# COLORS
FIELD_ON = "#8D8D8D"
FIELD_OFF= "#636363"
DEFAULT_BLUE = "#1F6AA5"
SUCCESS_GREEN = "#39FF14"
COPY_PASTA_YELLOW = "#FFFF85"
AUTHENTICATING_YELLOW = "#FFFF00"

# /////////// /////////// /////////// /////////// /////////// 
# LOGIN FIELD FUNCTIONS
# Copy
def copy_to_clipboard(text, button):
    try:
        root.clipboard_clear()
        root.clipboard_append(text)
        button.configure(state="disabled", fg_color=COPY_PASTA_YELLOW)
        button.after(5000, lambda: button.configure(state="normal", fg_color=DEFAULT_BLUE))
    except tk.TclError as e:
        print(f"Clipboard copy error: {e}")
        
# Paste
def paste_to_clipboard(entry_field, button):
    try:
        entry_field.delete(0, "end")
        entry_field.insert(0, root.clipboard_get())
        button.configure(state="disabled", fg_color=COPY_PASTA_YELLOW)
        button.after(5000, lambda: button.configure(state="normal", fg_color=DEFAULT_BLUE))
    except tk.TclError as e:
        print(f"Clipboard paste error: ", e)
        
    
def clear_clipboard(entry_field, button):
    entry_field.delete(0, "end")
    button.configure(state="disabled", fg_color=COPY_PASTA_YELLOW)
    button.after(5000, lambda: button.configure(state="normal", fg_color=DEFAULT_BLUE))  

# /////////// /////////// /////////// /////////// /////////// 
# VERIFICATION FUNCTIONS
# Authentication
def key_token_validation(API_KEY, TOKEN):
    try:
        url = f"https://api.trello.com/1/members/me/boards?key={API_KEY}&token={TOKEN}"
        query = {
            'key': API_KEY,
            'token': TOKEN
        }
        
        response = requests.get(
            url, 
            params=query
        )
        print(json.dumps(response.json(), indent=4))
        return response.status_code
    except Exception as e:
        print("Validation error: ", e)
    
# API
def submit_api():
    # print("btn triggered.")
    user_api_key = api_key_input.get()
    user_token = api_token_input.get()
    username = username_input.get()
    
    time.sleep(.3)
    connect_status.configure(text="AUTHENTICATING", text_color=AUTHENTICATING_YELLOW)
    api_key_input.configure(state="disabled", fg_color=FIELD_OFF)
    api_token_input.configure(state="disabled", fg_color=FIELD_OFF)
    connect_status.update()
    api_key_input.update()
    api_token_input.update()
    api_submit_btn.configure(state="disabled")
    
    if key_token_validation(user_api_key, user_token) == 200:
        time.sleep(1)
        connect_status.configure(text="VALID", text_color=SUCCESS_GREEN)
        connect_status.update()
        
        con = sqlite3.connect("key.db")
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS credentials(user_name, api_key, token)")
        con.commit()
        
        cursor.execute(f"INSERT OR IGNORE INTO credentials (user_name, api_key, token) VALUES (?, ?, ?)", (username, user_api_key, user_token))
        
        cursor.execute("SELECT user_name FROM credentials")
        api_keys = cursor.fetchall()
        
        for api_keys in api_keys:
            print(api_keys[0])
        
        con.commit()
        con.close()
        
        root.withdraw()
        main_program()
    else:
        time.sleep(1)
        connect_status.configure(text="INVALID; RECHECK KEY OR TOKEN.", text_color="red")
        connect_status.update()
        api_key_input.configure(state="normal", fg_color=FIELD_ON)
        api_token_input.configure(state="normal", fg_color=FIELD_ON)
        api_submit_btn.configure(state="normal")
        
def validateKeyExists():
    con = sqlite3.connect("key.db")
    cursor = con.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master where type='table' AND name='credentials'")
    table_exists = cursor.fetchone()
    if not table_exists:
        cursor.execute("CREATE TABLE credentials (username TEXT unique, api_key TEXT unique, token TEXT) unique")
        con.commit()
        return False
    
    
    # Check if API exists in table
    cursor.execute("SELECT 1 FROM credentials LIMIT 1")
    result = cursor.fetchone()
    con.close()
    if result:
        return True
    else:
        return False

# /////////// /////////// /////////// /////////// /////////// 
# MAIN
def initialize_login_gui():
    # Images
    copy_img = ck.CTkImage(light_image=Image.open("img/copy.png"), size=(15, 20))
    paste_img = ck.CTkImage(light_image=Image.open("img/paste.png"), size=(15, 20))
    clear_img = ck.CTkImage(light_image=Image.open("img/clear.png"), size=(15, 20))

    global root, tabview, help_holder
    global connect_status, api_key_input, api_token_input, api_submit_btn, username_input
    
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
    
    # CONNECT TAB
    connect_tab.grid_columnconfigure(0, weight=1)
    connect_tab.grid_columnconfigure(1, weight=0)
    connect_tab.grid_columnconfigure(2, weight=0)
    connect_tab.grid_columnconfigure(3, weight=0)
    connect_tab.grid_columnconfigure(4, weight=1)

    connect_tab.grid_rowconfigure(0, weight=1)
    connect_tab.grid_rowconfigure(4, weight=1)

    status_label = ck.CTkLabel(master=connect_tab, text="STATUS: ", font=("Arial", 14, "bold"))
    connect_status = ck.CTkLabel(master=connect_tab, text="AWAITING KEY", font=("Arial", 12, "bold"), text_color="red")
    status_label.grid(row=1, column=0, sticky="e", pady=10)
    connect_status.grid(row=1, column=1, sticky="w")

    api_key_label = ck.CTkLabel(master=connect_tab, text="API_KEY: ", font=("Arial", 14, "bold"))
    api_key_input = ck.CTkEntry(master=connect_tab, placeholder_text="[paste api key]", width=275, fg_color=FIELD_ON, placeholder_text_color="#5D5D5D")
    api_key_label.grid(row=2, column=0, sticky="e")
    api_key_input.grid(row=2, column=1, sticky="w")

    token_label = ck.CTkLabel(master=connect_tab, text="TOKEN: ", font=("Arial", 14, "bold"))
    api_token_input = ck.CTkEntry(master=connect_tab, placeholder_text="[paste token]", width=275, fg_color=FIELD_ON, placeholder_text_color="#5D5D5D")
    token_label.grid(row=3, column=0, sticky="e")
    api_token_input.grid(row=3, column=1, sticky="w", pady=5)
    
    username_label = ck.CTkLabel(master=connect_tab, text="USER: ", font=("Arial", 14, "bold"))
    username_input = ck.CTkEntry(master=connect_tab, placeholder_text="[enter name for entry]", width=275, fg_color=FIELD_ON, placeholder_text_color="#5D5D5D")
    username_label.grid(row=4, column=0, sticky="e")
    username_input.grid(row=4, column=1, sticky="w")

    api_submit_btn = ck.CTkButton(master=connect_tab, text="Connect", width=275, command=submit_api)
    api_submit_btn.grid(row=5, column=1, sticky="w", pady=10)

    paste_btn_apikey = ck.CTkButton(master=connect_tab, width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: paste_to_clipboard(api_key_input, paste_btn_apikey), image=paste_img)
    paste_btn_apikey.grid(row=2, column=2, padx=5, sticky="w")

    clear_btn_apikey = ck.CTkButton(master=connect_tab, width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: clear_clipboard(api_key_input, clear_btn_apikey), image=clear_img)
    clear_btn_apikey.grid(row=2, column=3, padx=0, sticky="w")

    paste_btn_token = ck.CTkButton(master=connect_tab, width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: paste_to_clipboard(api_token_input, paste_btn_token), image=paste_img)
    paste_btn_token.grid(row=3, column=2, padx=5, sticky="w")

    clear_btn_token = ck.CTkButton(master=connect_tab, width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: clear_clipboard(api_token_input, clear_btn_token), image=clear_img)
    clear_btn_token.grid(row=3, column=3, padx=0, sticky="w")
    
    # HELP TAB
    # Centers the entry boxes in help tab]
    help_tab.grid_columnconfigure(0, weight=1)
    help_tab.grid_columnconfigure(1, weight=0)
    help_tab.grid_columnconfigure(2, weight=0)
    help_tab.grid_columnconfigure(3, weight=1)

    help_tab.grid_rowconfigure(0, weight=1)
    help_tab.grid_rowconfigure(4, weight=1)

    developer_label = ck.CTkEntry(master=help_tab, placeholder_text="Developer: Danny Doan", width=250)
    developer_label.configure(state="disabled")
    developer_label.grid(row=1, column=1, padx=0, pady=5, sticky="w")

    developer_linkedin = ck.CTkEntry(master=help_tab, placeholder_text="LinkedIn: linkedin.com/in/dbdoan", width=250)
    developer_linkedin.configure(state="disabled")
    developer_linkedin.grid(row=2, column=1, padx=0, pady=5, sticky="w")

    developer_github = ck.CTkEntry(master=help_tab, placeholder_text="Github: github.com/dbdoan", width=250)
    developer_github.configure(state="disabled")
    developer_github.grid(row=3, column=1, padx=0, pady=5, sticky="w")

    copy_btn_lnkin = ck.CTkButton(master=help_tab, width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: copy_to_clipboard("linkedin.com/in/dbdoan", copy_btn_lnkin), image=copy_img)
    copy_btn_lnkin.grid(row=2, column=2, padx=5, sticky="w")
    copy_btn_gh = ck.CTkButton(master=help_tab, width=20, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: copy_to_clipboard("github.com/dbdoan", copy_btn_gh), image=copy_img)
    copy_btn_gh.grid(row=3, column=2, padx=5, sticky="w")

def initialize_toplevel_gui():
    global tabview_toplevel
    toplevel = ck.CTkToplevel(root)
    toplevel.title("TkTrello - TempAdmin")

    # Centering frame in respects to window
    toplevel.grid_columnconfigure(0, weight=1)
    toplevel.grid_rowconfigure(0, weight=1)
    
    tabview_toplevel = ck.CTkTabview(master=toplevel, width=500, height=250)
    tabview_toplevel.grid(row=0, column=0, padx=0, pady=0)
    
    main_tab = tabview_toplevel.add("Main")
    settings_tab = tabview_toplevel.add("Settings")
    
    # Settings Tab centering
    settings_tab.grid_columnconfigure(0, weight=1)
    settings_tab.grid_columnconfigure(1, weight=0)
    settings_tab.grid_columnconfigure(1, weight=0)
    settings_tab.grid_columnconfigure(2, weight=0)
    settings_tab.grid_columnconfigure(3, weight=1)
    settings_tab.grid_rowconfigure(0, weight=1)
    settings_tab.grid_rowconfigure(3, weight=1)
    
    
    api_user_label  = ck.CTkLabel(master=settings_tab,text="api key: ",font=("Arial", 14, "bold"))
    api_user_label.grid(row=1, column=0, sticky="e", pady=10)
    api_key_display = ck.CTkEntry(master=settings_tab, placeholder_text="[api_key_here]", width=275, height=100, fg_color=FIELD_OFF, placeholder_text_color="#5D5D5D")
    api_key_display.grid(row=1, column=1, sticky="w", pady=5)
    signout_btn = ck.CTkButton(master=settings_tab,width=275, text="logout", fg_color="#B23B3B")
    signout_btn.grid(row=2, column=1)
    
    main_tab.grid_columnconfigure(0, weight=1)
    main_tab.grid_columnconfigure(1, weight=1)
    main_tab.grid_rowconfigure(0, weight=1)
    main_tab.grid_rowconfigure(1, weight=1)
    
    toplevel.geometry("600x300")

# MAIN PROGRAM (TOP_LEVEL)
def main_program():
    initialize_toplevel_gui()
    
# /////////// /////////// /////////// /////////// /////////// 
# LOGIN START
initialize_login_gui()

if validateKeyExists():
    root.withdraw()
    main_program()
else:
    root.mainloop()

# /////////// /////////// /////////// /////////// /////////// 
# Root End
root.geometry("600x300")
root.mainloop()