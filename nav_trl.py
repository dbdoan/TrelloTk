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
    data = response.json()

    # print(json.dumps(json.loads(response.text), indent=4))
    board_map ={}
    for board in data:
        if not board.get('closed', False):
            board_map[board['name'].title()] = board['id']
            
    # return (board_map)
    return board_map


def get_all_lists(board_id):
    active_key = get_active_key()
    api_key = active_key[0]
    token = active_key[1]
    url = f"https://api.trello.com/1/boards/{board_id}/lists?key={api_key}&token={token}"

    headers=  {
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    list_names = []
    for lst in data:
        if not lst.get("closed", False):
            list_names.append(lst["name"])
    return list_names
    
    
    