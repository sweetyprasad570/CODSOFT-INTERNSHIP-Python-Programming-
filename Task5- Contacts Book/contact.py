import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, random, csv

# ------------------ Data Storage ------------------ #
FILE_NAME = "contacts.json"

def load_contacts():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_contacts():
    with open(FILE_NAME, "w") as f:
        json.dump(contacts, f, indent=4)

# ------------------ Core Functions ------------------ #
def add_contact():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()
    address = address_var.get().strip()

    if not name or not phone:
        show_message("⚠️ Enter Name and Phone!", "#4d82ff")
        return

    if name in contacts:
        show_message(f"❌ '{name}' already exists!", "#ef5350")
        return

    contacts[name] = {"Phone": phone, "Email": email, "Address": address}
    save_contacts()
    update_contact_list()
    clear_fields()
    show_message(f"✅ '{name}' added successfully!", "#81c784")

def update_contact():
    selected = contact_tree.selection()
    if not selected:
        show_message("❌ Select a contact to update!", "#ef5350")
        return

    old_name = contact_tree.item(selected[0])["values"][0]   # original name
    new_name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()
    address = address_var.get().strip()

    # Remove old entry if name changed
    if old_name != new_name:
        contacts.pop(old_name, None)

    contacts[new_name] = {
        "Phone": phone,
        "Email": email,
        "Address": address
    }

    save_contacts()
    update_contact_list()
    show_message(f"🔄 '{new_name}' updated!", "#64b5f6")


def delete_contact():
    name = name_var.get().strip()
    if name not in contacts:
        show_message("❌ Contact not found!", "#ef5350")
        return

    if messagebox.askyesno("Delete Contact", f"Delete '{name}' permanently?"):
        contacts.pop(name)
        save_contacts()
        update_contact_list()
        clear_fields()
        show_message(f"🗑️ '{name}' deleted!", "#f06292")

def search_contact():
    query = search_var.get().strip().lower()
    contact_tree.delete(*contact_tree.get_children())
    for name, info in contacts.items():
        if query in name.lower() or query in info["Phone"]:
            contact_tree.insert("", "end", values=(name, info["Phone"]))
    flash_tree_color("#ffe082")

def show_all_contacts():
    update_contact_list()
    flash_tree_color("#b3e5fc")

def on_select(event):
    selected = contact_tree.selection()
    if selected:
        item = contact_tree.item(selected[0])
        name = item["values"][0]
        info = contacts[name]
        name_var.set(name)
        phone_var.set(info["Phone"])
        email_var.set(info["Email"])
        address_var.set(info["Address"])

def clear_fields():
    for var in (name_var, phone_var, email_var, address_var, search_var):
        var.set("")

def update_contact_list():
    contact_tree.delete(*contact_tree.get_children())
    for name, info in contacts.items():
        contact_tree.insert("", "end", values=(name, info["Phone"]))
    count_label.config(text=f"📇 Total Contacts: {len(contacts)}")

# ------------------ New Features ------------------ #
def export_contacts():
    file = "contacts.csv"   # auto-create in project folder
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email", "Address"])
        for name, info in contacts.items():
            writer.writerow([name, info["Phone"], info["Email"], info["Address"]])
    show_message("💾 contacts.csv exported successfully!", "#4caf50")


def import_contacts():
    file = "contacts.csv"   # auto-read from project folder

    if not os.path.exists(file):
        show_message("❌ contacts.csv not found!", "#ef5350")
        return

    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts[row["Name"]] = {
                "Phone": row["Phone"],
                "Email": row["Email"],
                "Address": row["Address"]
            }

    save_contacts()
    update_contact_list()
    show_message("📥 contacts.csv imported successfully!", "#039be5")


dark_mode = False
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.config(bg="#212121")
        form.config(bg="#424242", fg="white")
        title_label.config(bg="#212121", fg="#ffeb3b")
        style.configure("Treeview", background="#424242", foreground="white", fieldbackground="#424242")
        show_message("🌙 Dark Mode Enabled", "#ffeb3b")
    else:
        root.config(bg="#fafafa")
        form.config(bg="#fafafa", fg="black")
        title_label.config(bg="#fafafa", fg="#1a237e")
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
        show_message("☀️ Light Mode Enabled", "#0288d1")

# ------------------ Animation Helpers ------------------ #
def show_message(text, color):
    msg_label.config(text=text, fg=color)
    msg_label.place(relx=0.5, rely=0.95, anchor="center")
    fade_message(0, color)

def fade_message(alpha, color):
    if alpha <= 1:
        msg_label.config(fg=color)
        root.after(100, fade_message, alpha + 0.1, color)
    else:
        root.after(2000, msg_label.place_forget)

def flash_tree_color(color):
    style.configure("Treeview", background=color)
    root.after(300, lambda: style.configure("Treeview", background="white"))

# ------------------ Fancy Gradient Background ------------------ #
def animate_bg():
    global bg_colors, current_color_index
    next_index = (current_color_index + 1) % len(bg_colors)
    color1 = bg_colors[current_color_index]
    color2 = bg_colors[next_index]
    r1, g1, b1 = root.winfo_rgb(color1)
    r2, g2, b2 = root.winfo_rgb(color2)
    r = (r1 + r2)//2 // 256
    g = (g1 + g2)//2 // 256
    b = (b1 + b2)//2 // 256
    mixed = f"#{r:02x}{g:02x}{b:02x}"

    root.config(bg=mixed)
    title_label.config(bg=mixed)
    form.config(bg=mixed)
    btn_frame.config(bg=mixed)
    search_frame.config(bg=mixed)
    msg_label.config(bg=mixed)
    title_label.config(fg=random.choice(["#1a237e", "#004d40", "#880e4f", "#4a148c"]))
    current_color_index = next_index
    root.after(1200, animate_bg)

# ------------------ UI Setup ------------------ #
root = tk.Tk()
root.title("🌈 Animated Contact Book 🌈")
root.geometry("850x600")

contacts = load_contacts()

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", foreground="black", rowheight=28, fieldbackground="white")
style.map("Treeview", background=[("selected", "#90caf9")])
style.configure("TButton", font=("Arial", 10, "bold"), padding=5)

# Variables
name_var, phone_var, email_var, address_var, search_var = (tk.StringVar() for _ in range(5))

# ------------------ Title Label ------------------ #
title_label = tk.Label(root, text="📔 CONTACTS — My Phonebook ☎️", font=("Segoe UI", 20, "bold"))
title_label.pack(pady=10)

# ------------------ Form Frame ------------------ #
form = tk.LabelFrame(root, text="Contact Details", font=("Arial", 11, "bold"), padx=10, pady=10)
form.pack(padx=10, pady=5, fill="x")

tk.Label(form, text="Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
tk.Entry(form, textvariable=name_var, width=25).grid(row=0, column=1, padx=5)

tk.Label(form, text="Phone:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w")
tk.Entry(form, textvariable=phone_var, width=25).grid(row=1, column=1, padx=5)

tk.Label(form, text="Email:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w")
tk.Entry(form, textvariable=email_var, width=25).grid(row=0, column=3, padx=5)

tk.Label(form, text="Address:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky="w")
tk.Entry(form, textvariable=address_var, width=25).grid(row=1, column=3, padx=5)

# ------------------ Buttons ------------------ #
btn_frame = tk.Frame(root, bg="#ffffff")
btn_frame.pack(pady=12)

def make_button(parent, text, cmd, color, col):
    btn = tk.Button(
        parent, text=text, command=cmd, bg=color, fg="white",
        font=("Arial", 10, "bold"), width=12, relief="flat",
        activebackground=color, cursor="hand2", bd=3
    )
    btn.grid(row=0, column=col, padx=8, pady=5)
    def on_enter(e): btn.config(bg="white", fg=color, relief="raised", bd=4)
    def on_leave(e): btn.config(bg=color, fg="white", relief="flat", bd=3)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

make_button(btn_frame, "➕ Add", add_contact, "#43a047", 0)
make_button(btn_frame, "✏️ Update", update_contact, "#1976d2", 1)
make_button(btn_frame, "🗑️ Delete", delete_contact, "#e53935", 2)
make_button(btn_frame, "🧹 Clear", clear_fields, "#8e24aa", 3)
make_button(btn_frame, "📥 Import CSV", import_contacts, "#0097a7", 4)
make_button(btn_frame, "💾 Export CSV", export_contacts, "#f57f17", 5)
make_button(btn_frame, "🌙 Theme", toggle_theme, "#5e35b1", 6)


# ------------------ Search ------------------ #
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
tk.Label(search_frame, text="🔍 Search:", font=("Arial", 10, "bold")).pack(side="left")
tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left", padx=5)
tk.Button(search_frame, text="Go", command=search_contact, bg="#0288d1", fg="white").pack(side="left", padx=5)
tk.Button(search_frame, text="Show All", command=show_all_contacts, bg="#ffb300", fg="white").pack(side="left", padx=5)

# ------------------ Contact Table ------------------ #
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("Name", "Phone")
contact_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
contact_tree.heading("Name", text="Name")
contact_tree.heading("Phone", text="Phone")
contact_tree.column("Name", width=300)
contact_tree.column("Phone", width=200)
contact_tree.pack(fill="both", expand=True)
contact_tree.bind("<<TreeviewSelect>>", on_select)

# ------------------ Contact Count ------------------ #
count_label = tk.Label(root, text="", font=("Arial", 10, "bold"), bg="white", fg="#004d40")
count_label.pack(pady=3)

# ------------------ Animated Message Label ------------------ #
msg_label = tk.Label(root, text="", font=("Arial", 11, "bold"))

# ------------------ Start Background Animation ------------------ #
bg_colors = ["#fce4ec", "#e1bee7", "#bbdefb", "#c8e6c9", "#fff9c4", "#ffccbc", "#d1c4e9"]
current_color_index = 0
animate_bg()

update_contact_list()
root.mainloop()
