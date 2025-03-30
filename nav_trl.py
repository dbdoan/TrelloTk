import json
import sqlite3
import requests

def get_active_key():
    con = sqlite3.connect('key.db')
    cursor = con.cursor()
    
    cursor.execute("SELECT api_key, token FROM credentials WHERE is_active = 1")
    result = cursor.fetchone()
    
    if result:
        api_key, token = result
    else:
        print("No active API key. (How are you even logged in??)")
        api_key = "No API key"
        token = "no token"
    return result

def get_all_boards():
    active_key = get_active_key()
    api_key = active_key[0]
    token = active_key[1]
    url = f"https://api.trello.com/1/members/me/boards?key={api_key}&token={token}"
    
    headers=  {
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)

    print(json.dumps(json.loads(response.text), indent=4))