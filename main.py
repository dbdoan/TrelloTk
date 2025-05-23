import os
import customtkinter as ck
import json
import requests
import sqlite3
import time
import tkinter as tk
from tkinter import ttk

from PIL import Image

from clipboard import copy_to_clipboard, paste_to_clipboard, clear_clipboard
from nav_trl import get_all_boards, get_all_lists, get_all_cards

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
        
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS credentials(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT,
                           api_key TEXT, 
                           token TEXT,
                           is_active BOOLEAN DEFAULT 0
                           )
                           """)
        con.commit()
        
        cursor.execute("SELECT id FROM credentials WHERE api_key = ? AND token = ?", (user_api_key, user_token))
        existing_profile = cursor.fetchone()
        
        if existing_profile:
            cursor.execute("UPDATE credentials SET is_active = 1 WHERE id = ?", (existing_profile[0],))
        else: 
            cursor.execute(f"INSERT OR IGNORE INTO credentials (username, api_key, token, is_active) VALUES (?, ?, ?, 1)", (username, user_api_key, user_token))
        
        cursor.execute("SELECT username FROM credentials")
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
    
    # Check if API exists in table
    if table_exists:
        cursor.execute("SELECT * FROM credentials WHERE is_active = 1")
        result = cursor.fetchone()
        con.close()
    
        if result:
            return True
        else:
            return False
    else:
        print("The database table does not exist!")

# /////////// /////////// /////////// /////////// /////////// 
# MAIN

def profile_selector_callback(username):
    con = sqlite3.connect('key.db')
    cursor = con.cursor()
    cursor.execute("SELECT api_key, token FROM credentials WHERE username = ?", (username,))
    
    result = cursor.fetchone()
    
    con.close()
    
    if result:
        api_key, token = result
        api_key_input.delete(0, "end")
        api_token_input.delete(0, "end")
        username_input.delete(0, "end")
        
        api_key_input.insert(0, api_key)
        api_token_input.insert(0, token)
        username_input.insert(0, username)
    
    else:
        print("Did not find profile key-pair in database!")
        return None, None
    
def get_usersnames_from_db():
    con = sqlite3.connect('key.db')
    cursor = con.cursor()
    
    cursor.execute("SELECT username FROM credentials")
    usernames = cursor.fetchall()
    
    con.close
    
    return [username[0] for username in usernames]

def logout(toplevel):
    con = sqlite3.connect('key.db')
    cursor = con.cursor()
    
    cursor.execute("UPDATE credentials SET is_active = 0")
    con.commit()
    con.close()
    toplevel.withdraw()
    initialize_login_gui()
    root.deiconify()
    
def initialize_login_gui():
    # Images
    copy_img = ck.CTkImage(light_image=Image.open("img/copy.png"), size=(15, 20))
    paste_img = ck.CTkImage(light_image=Image.open("img/paste.png"), size=(15, 20))
    clear_img = ck.CTkImage(light_image=Image.open("img/clear.png"), size=(15, 20))

    global root, tabview, help_holder
    global connect_status, api_key_input, api_token_input, api_submit_btn, username_input
    
    root.title("TkTrello")
    frm = ttk.Frame(root, padding=10)
    root.geometry("600x300")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    tabview = ck.CTkTabview(master=root, width=500, height=250)
    tabview.grid(row=0, column=0, padx=0, pady=0)

    help_holder = "Contact"
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
    
    profile_label = ck.CTkLabel(master=connect_tab, text="PROFILES: ", font=("Arial", 14, "bold"))
    
    usernames = get_usersnames_from_db()
    default_username = usernames[0] if usernames else "No Profiles"
    selected_profile = ck.StringVar(value=default_username)
    profile_options = ck.CTkOptionMenu(master=connect_tab, values=usernames, command=profile_selector_callback, variable=selected_profile, width=275)
    profile_options.set(default_username)
    profile_label.grid(row=5, column=0, sticky="e")
    profile_options.grid(row=5, column=1, sticky="w", pady=5)

    api_submit_btn = ck.CTkButton(master=connect_tab, text="Connect", width=275, command=submit_api)
    api_submit_btn.grid(row=6, column=1, sticky="w", pady=10)

    paste_btn_apikey = ck.CTkButton(master=connect_tab, width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: paste_to_clipboard(root=root, entry_field=api_key_input, button=paste_btn_apikey), image=paste_img)
    paste_btn_apikey.grid(row=2, column=2, padx=5, sticky="w")

    clear_btn_apikey = ck.CTkButton(master=connect_tab, width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: clear_clipboard(api_key_input, clear_btn_apikey), image=clear_img)
    clear_btn_apikey.grid(row=2, column=3, padx=0, sticky="w")

    paste_btn_token = ck.CTkButton(master=connect_tab, width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: paste_to_clipboard(root=root, entry_field=api_token_input, button=paste_btn_token), image=paste_img)
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

    copy_btn_lnkin = ck.CTkButton(master=help_tab, width=15, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: copy_to_clipboard(root=root, text="linkedin.com/in/dbdoan", button=copy_btn_lnkin), image=copy_img)
    copy_btn_lnkin.grid(row=2, column=2, padx=5, sticky="w")
    copy_btn_gh = ck.CTkButton(master=help_tab, width=20, text="", font=("Arial", 14), hover_color="#A5A5A5", text_color="#FFFFFF", command=lambda: copy_to_clipboard(root=root, text="github.com/dbdoan", button=copy_btn_gh), image=copy_img)
    copy_btn_gh.grid(row=3, column=2, padx=5, sticky="w")

def initialize_toplevel_gui():
    global tabview_toplevel
    toplevel = ck.CTkToplevel(root)
    toplevel.title("TkTrello - TempAdmin")

    # Centering frame in respects to window
    toplevel.grid_columnconfigure(0, weight=1)
    # toplevel.grid_rowconfigure(0, weight=1)
    
    tabview_toplevel = ck.CTkTabview(master=toplevel, width=500, height=575)
    tabview_toplevel.grid(row=0, column=0, padx=0, pady=0)
    
    main_tab = tabview_toplevel.add("Main")
    settings_tab = tabview_toplevel.add("Logout")
    
    # Settings Tab centering
    settings_tab.grid_columnconfigure(0, weight=1)
    settings_tab.grid_columnconfigure(1, weight=0)
    settings_tab.grid_columnconfigure(1, weight=0)
    settings_tab.grid_columnconfigure(2, weight=0)
    settings_tab.grid_columnconfigure(3, weight=1)
    settings_tab.grid_rowconfigure(0, weight=1)
    settings_tab.grid_rowconfigure(3, weight=1)
    
    con = sqlite3.connect("key.db")
    cursor = con.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master where type='table' AND name='credentials'")
    
    table_exists = cursor.fetchone()
    
    if table_exists:
        cursor.execute("SELECT username, api_key, token FROM credentials WHERE is_active = 1")
        result = cursor.fetchone()
        
        if result: 
            username, api_key, token = result
        else:
            print("No active profile found!")
            username, api_key, token = "No active profile", "No API key", "No token"
        
    else:
        print("Table does not exist!")
        toplevel_error = ck.CTkToplevel(toplevel)
        toplevel_error.title("Error!")
        toplevel_error.focus_force()
        toplevel_error.grid_columnconfigure(0, weight=1)
        toplevel_error.grid_rowconfigure(0, weight=1)
        error_text = ck.CTkLabel(master=toplevel_error, text="table is missing!", font=("Arial", 40, "bold"), text_color="red")
        error_text.grid(row=0, column=0)
        toplevel_error.geometry("400x200")
    
    profile_name_label = ck.CTkLabel(master=settings_tab, text="profile: ", font=("Arial", 14, "bold"))
    profile_name_label.grid(row=1, column=0, sticky="e", pady=10)
    profile_name_display = ck.CTkEntry(master=settings_tab, placeholder_text=f"{username}", width=355, height=20, placeholder_text_color="#ADADAD", font=("Arial", 20))
    profile_name_display.configure(state="disabled", height=40, fg_color=FIELD_OFF)
    profile_name_display.grid(row=1, column=1, sticky="w", pady=5)
    
    api_user_label = ck.CTkLabel(master=settings_tab, text="api key: ", font=("Arial", 14, "bold"))
    api_user_label.grid(row=2, column=0, sticky="e", pady=10)
    api_key_display = ck.CTkEntry(master=settings_tab, placeholder_text=f"{api_key}", width=355, height=20, placeholder_text_color='#ADADAD', font=("Arial", 20))
    api_key_display.configure(state="disabled", height=40, fg_color=FIELD_OFF)
    api_key_display.grid(row=2, column=1, sticky="w", pady=5)

    signout_btn = ck.CTkButton(master=settings_tab,width=355, text="LOGOUT", fg_color="#B23B3B", hover_color="#7A2020", command=lambda: logout(toplevel))
    signout_btn.grid(row=3, column=1, sticky="n", pady=5)
    
    main_tab.grid_columnconfigure(0, weight=1)
    main_tab.grid_columnconfigure(1, weight=1)
    main_tab.grid_columnconfigure(2, weight=1)
    
    global list_selector_box
    list_selector_box = None
    
    board_map = get_all_boards()
    board_names = list(board_map.keys())
    
    def set_selected_board(choice):
        print("Option clicked:", choice)
        selected_board_id = board_map.get(choice)
        
        if selected_board_id:
            list_map = get_all_lists(selected_board_id)
            list_names = list(list_map.keys())
            list_selector_label.grid(column=1, row=2)
            list_selector_box.grid(column=1, row=3, pady=5)
            
            if list_selector_box:
                list_selector_box.configure(values=list_names)
                list_selector_box.set("")

    board_selector_label = ck.CTkLabel(master=main_tab, text="Select Board:")
    board_selector_box = ck.CTkOptionMenu(master=main_tab, values=board_names, command=set_selected_board, dynamic_resizing=False, width=300)
    board_selector_box.set("-")
    board_selector_label.grid(column=1, row=0)
    board_selector_box.grid(column=1, row=1, pady=5) 
    
    def set_selected_list(choice):
        print("Option clicked:", choice)
        selected_board_id = board_map.get(board_selector_box.get())
        list_map = get_all_lists(selected_board_id)
        selected_list_id = list_map.get(choice)     
        
        if selected_list_id:
            card_map = get_all_cards(selected_list_id)
            card_names = list(card_map.keys())
            
            card_selector_label.grid(column=1, row=4)
            card_selector_box.grid(column=1, row=5)
            card_selector_box.configure(values=card_names)

    list_selector_label = ck.CTkLabel(master=main_tab, text="Select List:")
    list_selector_box = ck.CTkOptionMenu(master=main_tab, values=[], command=set_selected_list, dynamic_resizing=False, width=300)
    list_selector_box.set("-")

    def set_selected_card(choice):
        print("Option clicked:", choice)
    
    card_selector_label = ck.CTkLabel(master=main_tab, text="Select Card:")

    card_selector_box = ck.CTkOptionMenu(master=main_tab, values=[], command=set_selected_card, dynamic_resizing=False, width=300)
    card_selector_box.set("-")
    
    toplevel.geometry("600x600")

# MAIN PROGRAM (TOP_LEVEL)
def main_program():
    print("Opening main program...")
    initialize_toplevel_gui()

# /////////// /////////// /////////// /////////// /////////// 
# Root End
if __name__ == "__main__":
    root = tk.Tk()
        
    print("Checking if an active profile exists...")
    if validateKeyExists():
        print("Active profile found. Hiding login window...")
        root.withdraw()
        main_program()
    else:
        print("No active profile found. Showing login window...")
        initialize_login_gui()
        root.deiconify()
    root.mainloop()