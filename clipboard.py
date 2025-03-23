import tkinter as tk

# /////////// /////////// /////////// /////////// /////////// 
# COLORS
FIELD_ON = "#8D8D8D"
FIELD_OFF= "#636363"
DEFAULT_BLUE = "#1F6AA5"
SUCCESS_GREEN = "#39FF14"
COPY_PASTA_YELLOW = "#FFFF85"
AUTHENTICATING_YELLOW = "#FFFF00"

# /////////// /////////// /////////// /////////// /////////// 

def copy_to_clipboard(root, text, button):
    try:
        root.clipboard_clear()
        root.clipboard_append(text)
        button.configure(state="disabled", fg_color=COPY_PASTA_YELLOW)
        button.after(5000, lambda: button.configure(state="normal", fg_color=DEFAULT_BLUE))
    except tk.TclError as e:
        print(f"Clipboard copy error: {e}")
        
# Paste
def paste_to_clipboard(root, entry_field, button):
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