import tkinter as tk
import random
import pygame

# --- setup sound ---
pygame.mixer.init()

# --- sound files ---
S_WIN = "win.mp3"
S_LOSE = "lose.mp3"
S_TIE = "tie.mp3"
S_RESET = "reset.mp3"

# --- play sound safely ---
def sound_play(file):
    try:
        pygame.mixer.Sound(file).play()
    except:
        print("sound not found:", file)

# --- window setup ---
win = tk.Tk()
win.title("Rock Paper Scissors")
win.geometry("450x700")
win.config(bg="#0b0335")

player = 0
cpu = 0
items = ["Rock", "Paper", "Scissors"]

# --- main game logic ---
def start_game(pick):
    global player, cpu
    bot = random.choice(items)

    if pick == bot:
        msg = "It's a Tie!"
        color = "#ffff66"
        sound_play(S_TIE)
    elif (pick == "Rock" and bot == "Scissors") or \
         (pick == "Paper" and bot == "Rock") or \
         (pick == "Scissors" and bot == "Paper"):
        player += 1
        msg = "You Win!"
        color = "#00ff99"
        sound_play(S_WIN)
    else:
        cpu += 1
        msg = "You Lose!"
        color = "#ff4d4d"
        sound_play(S_LOSE)

    lbl_result.config(text=msg, fg=color)
    lbl_you.config(text=f"You chose: {pick}")
    lbl_cpu.config(text=f"Computer chose: {bot}")
    lbl_score.config(text=f"Score – You: {player}  |  Computer: {cpu}")

    move = f"You: {pick} | Computer: {bot} → {msg}"
    list_moves.insert(tk.END, move)
    list_moves.yview(tk.END)

# --- reset button ---
def reset_all():
    global player, cpu
    sound_play(S_RESET)
    player = 0
    cpu = 0
    lbl_result.config(text="")
    lbl_you.config(text="")
    lbl_cpu.config(text="")
    lbl_score.config(text="Score – You: 0  |  Computer: 0")
    list_moves.delete(0, tk.END)

# --- rainbow title ---
def rainbow_text(root, text):
    colors = ["#ff005c", "#ff8c00", "#ffe600", "#00ff99", "#00ccff", "#9933ff"]
    box = tk.Frame(root, bg="#0b0335")
    box.pack(pady=30)
    for i, t in enumerate(text):
        c = colors[i % len(colors)]
        tk.Label(box, text=t, font=("Arial Black", 21, "bold"), fg=c, bg="#0b0335").pack(side="left")
    return box

rainbow_text(win, "⚡✊R🅾CK⚡📄PAPΞR⚡🖖SCI💥SS🅾RS⚡")

# --- choose text ---
tk.Label(win, text="Choose your move!", font=("Arial", 14, "bold"),
         bg="#180052", fg="white", padx=20, pady=10).pack(pady=10)

# --- buttons ---
frame_btn = tk.Frame(win, bg="#0b0335")
frame_btn.pack(pady=25)
style = {"width": 6, "height": 2, "font": ("Arial", 28), "relief": "flat"}

tk.Button(frame_btn, text="✊", bg="#00bfff", fg="white",
          activebackground="#00a0e0", command=lambda: start_game("Rock"), **style).grid(row=0, column=0, padx=15)
tk.Button(frame_btn, text="📄", bg="#ff5aa4", fg="white",
          activebackground="#ff4794", command=lambda: start_game("Paper"), **style).grid(row=0, column=1, padx=15)
tk.Button(frame_btn, text="✌️", bg="#ff8c00", fg="white",
          activebackground="#ff7700", command=lambda: start_game("Scissors"), **style).grid(row=0, column=2, padx=15)

# --- labels ---
lbl_result = tk.Label(win, text="", font=("Arial", 16, "bold"), bg="#0b0335", fg="white")
lbl_result.pack(pady=15)

lbl_you = tk.Label(win, text="", font=("Arial", 12), bg="#0b0335", fg="white")
lbl_you.pack()

lbl_cpu = tk.Label(win, text="", font=("Arial", 12), bg="#0b0335", fg="white")
lbl_cpu.pack()

lbl_score = tk.Label(win, text="Score – You: 0  |  Computer: 0",
                     font=("Arial", 14, "bold"), bg="#180052", fg="white", padx=20, pady=10)
lbl_score.pack(pady=25)

# --- play again button ---
tk.Button(win, text="🔁 PLAY AGAIN", command=reset_all,
          font=("Arial Black", 16), bg="#6a0dad", fg="white",
          activebackground="#7b68ee", activeforeground="white",
          relief="flat", padx=20, pady=10).pack(pady=10)

# --- move history ---
tk.Label(win, text="📜 Move History", font=("Arial", 14, "bold"),
         bg="#0b0335", fg="#ffcc00").pack(pady=(20, 5))

frame_hist = tk.Frame(win, bg="#0b0335")
frame_hist.pack(pady=5)

scroll = tk.Scrollbar(frame_hist)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

list_moves = tk.Listbox(frame_hist, width=45, height=8, bg="#1a004d", fg="white",
                        font=("Arial", 11), yscrollcommand=scroll.set,
                        selectbackground="#6a0dad", highlightthickness=0, relief="flat")
list_moves.pack(side=tk.LEFT, fill=tk.BOTH)
scroll.config(command=list_moves.yview)

# --- run window ---
win.mainloop()
