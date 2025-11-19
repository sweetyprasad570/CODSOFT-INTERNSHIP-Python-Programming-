import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os
from datetime import datetime

FILE = "tasks.json"

# ----------------- Load / Save -----------------
def load_tasks():
    if os.path.exists(FILE):
        return json.load(open(FILE, "r", encoding="utf-8"))
    return []

def save_tasks():
    json.dump(tasks, open(FILE, "w", encoding="utf-8"), indent=4)

# ----------------- Helpers -----------------
def selected_index():
    if root.sel_i is None:
        messagebox.showinfo("Select Task", "Please select a task first!")
        return None
    return root.sel_i

# ----------------- Task Functions -----------------
def add_task():
    t = task_entry.get().strip()
    if t == "":
        messagebox.showwarning("Empty", "Please enter a task")
        return

    tasks.append({
        "title": t,
        "done": False,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "priority": pr_box.get()
    })
    save_tasks()
    task_entry.delete(0, tk.END)
    show_tasks()

def mark_done():
    i = selected_index()
    if i is not None:
        tasks[i]["done"] = True
        save_tasks()
        show_tasks()

def delete_task():
    i = selected_index()
    if i is not None:
        if messagebox.askyesno("Delete", "Delete this task?"):
            tasks.pop(i)
            save_tasks()
            show_tasks()

def edit_task():
    i = selected_index()
    if i is not None:
        t = tasks[i]
        new_title = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=t["title"])
        if new_title:
            t["title"] = new_title.strip()
            save_tasks()
            show_tasks()

# ----------------- Canvas Display -----------------
def show_tasks(filter_text=""):
    canvas.delete("all")
    card_list.clear()
    root.sel_i = None

    y = 10
    for i, t in enumerate(tasks):
        if filter_text and filter_text not in t["title"].lower():
            continue

        x1, x2 = 15, canvas.winfo_width() - 20
        h = 80

        bg = "#2b0a6f" if not t["done"] else "#1e1e1e"
        canvas.create_rectangle(x1, y, x2, y + h, fill=bg, outline="")

        canvas.create_text(x1 + 15, y + 15, anchor="nw",
                           text=t["title"], fill="white",
                           font=("Segoe UI", 14, "bold"))

        canvas.create_text(x1 + 15, y + 42, anchor="nw",
                           text=f"{t['priority']}  •  {t['time']}",
                           fill="#d8caff", font=("Segoe UI", 10))

        icon = "⏳" if not t["done"] else "✅"
        canvas.create_text(x2 - 25, y + 20, text=icon,
                           fill="white", font=("Segoe UI", 18))

        card_list.append({"i": i, "box": (x1, y, x2, y + h)})
        y += h + 10

    canvas.config(scrollregion=canvas.bbox("all"))
    total_lbl.config(text=f"Total: {len(tasks)}")

# ----------------- Select Task -----------------
def click_canvas(e):
    x = canvas.canvasx(e.x)
    y = canvas.canvasy(e.y)

    for c in card_list:
        x1, y1, x2, y2 = c["box"]
        if x1 <= x <= x2 and y1 <= y <= y2:
            root.sel_i = c["i"]
            canvas.create_rectangle(x1, y1, x2, y2, outline="#cfa0ff", width=3)
            break

# ----------------- UI BUILD -----------------
root = tk.Tk()
root.title("To-Do List")
root.state("zoomed")
root.sel_i = None

header = tk.Label(root, text="⚡ To-Do List ",
                  bg="#3b1366", fg="white",
                  font=("Segoe UI", 20))
header.pack(fill="x")

main = tk.Frame(root)
main.pack(fill="both", expand=True, padx=10, pady=10)

main.rowconfigure(0, weight=1)
main.columnconfigure(0, weight=3)
main.columnconfigure(1, weight=1)

# ---------------- LEFT ----------------
left = tk.Frame(main)
left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

search_frame = tk.Frame(left, bg="#8b2969")
search_frame.pack(fill="x", pady=5)

search_entry = tk.Entry(search_frame, font=("Segoe UI", 12))
search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
search_entry.bind("<KeyRelease>", lambda e: show_tasks(search_entry.get().lower()))

tk.Button(search_frame, text="Search", command=lambda: show_tasks(search_entry.get().lower())).pack(side="left", padx=5)
tk.Button(search_frame, text="Show All", command=lambda: show_tasks("")).pack(side="left", padx=5)

canvas = tk.Canvas(left, bg="#c7ffd8")
canvas.pack(fill="both", expand=True)
canvas.bind("<Button-1>", click_canvas)

# ---------------- RIGHT ----------------
right = tk.Frame(main, bg="#d2ddff")
right.grid(row=0, column=1, sticky="nsew")

tk.Label(right, text="Add New Task",
         font=("Segoe UI", 16, "bold"),
         bg="#d2ddff").pack(pady=10)

task_entry = tk.Entry(right, font=("Segoe UI", 12))
task_entry.pack(fill="x", padx=15, pady=5, ipady=7)

pr_box = ttk.Combobox(right, values=["High", "Medium", "Low"], state="readonly")
pr_box.set("Medium")
pr_box.pack(fill="x", padx=15, pady=5)

# ADD BUTTON
add_btn = tk.Button(right, text="➕ ADD TASK", command=add_task,
                    font=("Segoe UI", 14, "bold"), bg="#6a0dad",
                    fg="white", relief="flat", bd=0, padx=10, pady=10)
add_btn.pack(fill="x", padx=15, pady=10)

# DONE
tk.Button(right, text="✔ DONE", command=mark_done,
          font=("Segoe UI", 14, "bold"),
          bg="#0a8f47", fg="white").pack(fill="x", padx=15, pady=8)

# DELETE
tk.Button(right, text="🗑 DELETE", command=delete_task,
          font=("Segoe UI", 14, "bold"),
          bg="#c1121f", fg="white").pack(fill="x", padx=15, pady=8)

# EDIT
tk.Button(right, text="✏ EDIT", command=edit_task,
          font=("Segoe UI", 14, "bold"),
          bg="#1d4ed8", fg="white").pack(fill="x", padx=15, pady=8)

total_lbl = tk.Label(right, text="Total: 0", bg="#d2ddff", font=("Segoe UI", 12))
total_lbl.pack(pady=10)

# ---------------- START ----------------
tasks = load_tasks()
card_list = []

root.after(100, show_tasks)
root.mainloop()
