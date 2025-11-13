import tkinter as tk
import math

# Memory value
memory_value = 0

# Create window
app = tk.Tk()
app.title("Smart Calculator")
app.geometry("360x520")
app.configure(bg="#f0f8ff")  # Light background

# Title label
heading = tk.Label(app, text="🧮 Smart Calculator 🧮", font=("Arial", 20, "bold"), fg="#0077b6", bg="#f0f8ff")
heading.grid(row=0, column=0, columnspan=4, pady=(10, 0))

# Display box
input_box = tk.Entry(app, font=("Arial", 24), bd=8, relief="ridge", justify="right", bg="white")
input_box.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

# Add number or symbol to input
def add_to_input(value):
    input_box.insert(tk.END, value)

# Clear input
def clear_input():
    input_box.delete(0, tk.END)

# Delete last character
def delete_last():
    current_text = input_box.get()
    input_box.delete(0, tk.END)
    input_box.insert(tk.END, current_text[:-1])

# Calculate result
def get_result():
    try:
        result = eval(input_box.get())
        input_box.delete(0, tk.END)
        input_box.insert(tk.END, result)
    except:
        input_box.delete(0, tk.END)
        input_box.insert(tk.END, "Error")

# Square root
def find_sqrt():
    try:
        number = float(input_box.get())
        input_box.delete(0, tk.END)
        input_box.insert(tk.END, math.sqrt(number))
    except:
        input_box.delete(0, tk.END)
        input_box.insert(tk.END, "Error")

# Memory functions
def memory_plus():
    global memory_value
    try:
        memory_value += float(input_box.get())
    except:
        pass

def memory_minus():
    global memory_value
    try:
        memory_value -= float(input_box.get())
    except:
        pass

def memory_show():
    input_box.delete(0, tk.END)
    input_box.insert(tk.END, memory_value)

def memory_reset():
    global memory_value
    memory_value = 0

# Button style
button_style = {"font": ("Arial", 14), "width": 5, "height": 2, "bg": "#d1e7dd", "bd": 3}

# Number and operator buttons
button_rows = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', '.', '%', '+')
]

for row_index, row_values in enumerate(button_rows):
    for col_index, label in enumerate(row_values):
        tk.Button(app, text=label, command=lambda val=label: add_to_input(val), **button_style).grid(row=row_index+2, column=col_index, padx=5, pady=5)

# Special buttons
tk.Button(app, text="C", command=clear_input, font=("Arial", 14), width=5, height=2, bg="#f8d7da", bd=3).grid(row=6, column=0, padx=5, pady=5)
tk.Button(app, text="←", command=delete_last, font=("Arial", 14), width=5, height=2, bg="#f8d7da", bd=3).grid(row=6, column=1, padx=5, pady=5)
tk.Button(app, text="√", command=find_sqrt, font=("Arial", 14), width=5, height=2, bg="#cfe2ff", bd=3).grid(row=6, column=2, padx=5, pady=5)
tk.Button(app, text="=", command=get_result, font=("Arial", 14), width=5, height=2, bg="#b6d4fe", bd=3).grid(row=6, column=3, padx=5, pady=5)

# Memory buttons
tk.Button(app, text="M+", command=memory_plus, font=("Arial", 12), width=5, height=2, bg="#e2e3e5", bd=3).grid(row=7, column=0, padx=5, pady=5)
tk.Button(app, text="M-", command=memory_minus, font=("Arial", 12), width=5, height=2, bg="#e2e3e5", bd=3).grid(row=7, column=1, padx=5, pady=5)
tk.Button(app, text="MR", command=memory_show, font=("Arial", 12), width=5, height=2, bg="#e2e3e5", bd=3).grid(row=7, column=2, padx=5, pady=5)
tk.Button(app, text="MC", command=memory_reset, font=("Arial", 12), width=5, height=2, bg="#e2e3e5", bd=3).grid(row=7, column=3, padx=5, pady=5)

# Exit button
tk.Button(app, text="Exit", command=app.quit, font=("Arial", 14), width=20, height=2, bg="#ffccd5", bd=3).grid(row=8, column=0, columnspan=4, pady=15)

# Start the app
app.mainloop()
