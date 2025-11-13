import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import time
import threading

# Function to make password
def generate_password(length, strength):
    if strength == "Easy":
        chars = string.ascii_lowercase
    elif strength == "Medium":
        chars = string.ascii_letters + string.digits
    else:
        chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# Function to change between light & dark theme
def toggle_theme():
    dark_bg = "#191970"
    light_bg = "#e0f7fa"
    button_bg = "#003366"
    text_color = "#ffffff"
    accent_color = "#00ffff"

    if root.cget("bg") == light_bg:
        root.configure(bg=dark_bg)
        frame.configure(bg=dark_bg)
        button_frame.configure(bg=dark_bg)
        result_label.configure(bg=dark_bg, fg=accent_color)
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=dark_bg, fg=text_color)
            elif isinstance(widget, tk.Button):
                widget.configure(bg=button_bg, fg=text_color)
    else:
        root.configure(bg=light_bg)
        frame.configure(bg=light_bg)
        button_frame.configure(bg=light_bg)
        result_label.configure(bg=light_bg, fg="black")
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=light_bg, fg="#4a90e2")
            elif isinstance(widget, tk.Button):
                widget.configure(bg="#4a90e2", fg="white")

# Function to show text with color changing animation
def animate_label(text, label, colors=["red", "green", "blue", "purple", "orange"]):
    label.config(text="")
    for i, char in enumerate(text):
        label.config(text=label.cget("text") + char, fg=colors[i % len(colors)])
        label.update()
        time.sleep(0.05)

# Function to start password making
def start_generation():
    try:
        length = int(length_entry.get())
        strength = strength_var.get()
        animate_label("🔄 Generating password...", result_label)
        time.sleep(1)
        password = generate_password(length, strength)
        result_label.config(text=f"✅ Your password is:\n{password}", fg="green")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for length.")

# Function to save password in file
def save_password():
    password = result_label.cget("text").split("\n")[-1]
    if password and "Your password is:" in result_label.cget("text"):
        with open("my_password.txt", "w") as f:
            f.write("Generated Password: " + password)
        animate_label("📁 Password saved to 'my_password.txt'", result_label)
    else:
        messagebox.showwarning("No Password", "Generate a password first!")

# Function to see saved password
def view_saved_passwords():
    try:
        with open("my_password.txt", "r") as f:
            saved = f.read()
        messagebox.showinfo("Saved Passwords", saved)
    except:
        messagebox.showwarning("No File", "No saved passwords found.")

# Function to copy password
def copy_to_clipboard():
    password = result_label.cget("text").split("\n")[-1]
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# Button hover effects
def on_enter(e):
    e.widget.config(bg="#d1e0ff", fg="black")

def on_leave(e):
    e.widget.config(bg="#4a90e2", fg="white")

# GUI window setup
root = tk.Tk()
root.state('zoomed')
root.title("🌈 Password Generator")
root.geometry("420x360")
root.configure(bg="#e0f7fa")
root.resizable(False, False)

# Animated title
def animate_title(text, label, colors=["#ff4d4d", "#ffa64d", "#ffff4d", "#4dff4d", "#4dd2ff", "#b84dff"]):
    label.config(text="")
    for i, char in enumerate(text):
        label.config(text=label.cget("text") + char, fg=colors[i % len(colors)])
        label.update()
        time.sleep(0.05)

title_label = tk.Label(root, text="", font=("Arial Black", 28, "bold"), bg="#e0f7fa")
title_label.pack(pady=20)
threading.Thread(target=lambda: animate_title("🔐 Password Generator", title_label)).start()

frame = tk.Frame(root, bg="#e0f7fa")
frame.pack(pady=5)

# Input fields
tk.Label(frame, text="Length:", bg="#e0f7fa", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
length_entry = tk.Entry(frame, width=10, font=("Arial", 12))
length_entry.grid(row=0, column=1)

tk.Label(frame, text="Strength:", bg="#e0f7fa", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
strength_var = tk.StringVar(value="Strong")
strength_menu = ttk.Combobox(frame, textvariable=strength_var, values=["Easy", "Medium", "Strong"], state="readonly", font=("Arial", 12))
strength_menu.grid(row=1, column=1)

# Buttons area
button_frame = tk.Frame(root, bg="#e0f7fa")
button_frame.pack(pady=10)

buttons = [
    ("Generate Password", lambda: threading.Thread(target=start_generation).start()),
    ("Regenerate", lambda: threading.Thread(target=start_generation).start()),
    ("Save Password", save_password),
    ("View Saved", view_saved_passwords),
    ("Copy Password", copy_to_clipboard),
    ("Toggle Theme", toggle_theme)
]

# Create buttons in 3 rows, 2 columns
for i, (text, cmd) in enumerate(buttons):
    btn = tk.Button(button_frame, text=text, width=18, font=("Arial", 12), bg="#4a90e2", fg="white", command=cmd)
    btn.grid(row=i // 2, column=i % 2, padx=10, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Result label (shows output)
result_label = tk.Label(
    root,
    text="",
    font=("Courier", 20, "bold"),
    wraplength=800,
    justify="center",
    bg="#e0f7fa",
    fg="black",
    borderwidth=2,
    relief="groove",
    padx=10,
    pady=10
)
result_label.pack(pady=20)

root.mainloop()
