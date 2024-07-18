from tkinter import *
import math
import pygame
from datetime import datetime
import os
import sys

# Initialize pygame mixer
pygame.mixer.init()

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
DEFAULT_WORK_MIN = 40
DEFAULT_SHORT_BREAK_MIN = 5
DEFAULT_LONG_BREAK_MIN = 30
reps = 0
timer = None
pried = 1


# Path to resources
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global reps
    global pried
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    bell_label.config(text="Timer")
    reps = 0
    pried = 1

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    global pried

    start_from = int(start_from_entry.get())
    if reps < start_from:
        reps = start_from - 1
        pried = (start_from + 1) // 2

    reps += 1

    if pried > 8:
        play_bells(1)
        window.after(300000, play_sound, "long_bell.wav")  # Wait 5 minutes (300,000 ms) before playing the long bell
        reset_timer()
        return

    work_min = int(work_min_entry.get())
    short_break_min = int(short_break_min_entry.get())
    long_break_min = int(long_break_min_entry.get())

    work_sec = work_min * 60
    short_break_sec = short_break_min * 60
    long_break_sec = long_break_min * 60

    if reps % 10 == 0:
        count_down(long_break_sec)
        bell_label.config(text="Lunch Break", fg=RED)
        play_sound("long_bell.wav")
    elif reps % 2 == 0:
        count_down(work_sec, True)
        bell_label.config(text=f"Teaching Pried:{pried}", fg=PINK)
        play_bells(pried)
    else:
        count_down(short_break_sec)
        bell_label.config(text="Intimation Time", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count, teaching_time=False):
    global pried

    count_min = math.floor(count / 60)
    if count_min < 10:
        count_min = f"0{count_min}"

    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1, teaching_time)
    else:
        if teaching_time:
            pried += 1
        start_timer()

# ---------------------------- BELL SOUND MECHANISM ------------------------------- #


def play_sound(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()


def play_bells(times):
    for _ in range(times):
        play_sound("short_bell.wav")
        while pygame.mixer.music.get_busy():
            pass

# ---------------------------- TIME DISPLAY MECHANISM ------------------------------- #


def update_current_time():
    now = datetime.now().strftime("%H:%M:%S")
    current_time_label.config(text=f"Time: {now}")
    window.after(1000, update_current_time)

# ---------------------------- AUTO START MECHANISM ------------------------------- #


def schedule_start():
    start_hour = int(start_hour_entry.get())
    start_minute = int(start_minute_entry.get())
    now = datetime.now()
    start_time = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
    if now >= start_time:
        start_timer()
    else:
        delay = (start_time - now).total_seconds()
        window.after(int(delay * 1000), start_timer)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("School Bell")
window.config(padx=20, pady=20, bg=YELLOW)

# Configure grid
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_rowconfigure(5, weight=1)
window.grid_rowconfigure(6, weight=1)
window.grid_rowconfigure(7, weight=1)
window.grid_rowconfigure(8, weight=1)
window.grid_rowconfigure(9, weight=1)

title_label = Label(window, text="MLM H/S Lal Bazar", fg=RED, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
title_label.grid(column=0, row=0, columnspan=4, pady=10)

bell_label = Label(window, text="Bell Time", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 25, "bold"))
bell_label.grid(column=0, row=1, columnspan=4, pady=10)

canvas = Canvas(window, width=300, height=124, bg=YELLOW, highlightthickness=0)
timer_text = canvas.create_text(150, 50, text="00:00", fill="blue", font=(FONT_NAME, 65, "bold"))
canvas.grid(column=0, row=2, columnspan=4, pady=10)

work_min_label = Label(window, text="Class Duration:", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
work_min_label.grid(column=0, row=3, pady=10)
work_min_entry = Entry(window, width=5)
work_min_entry.grid(column=1, row=3, pady=10)
work_min_entry.insert(END, str(DEFAULT_WORK_MIN))

short_break_min_label = Label(window, text="Intimation Time:", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
short_break_min_label.grid(column=0, row=5, pady=10)
short_break_min_entry = Entry(window, width=5)
short_break_min_entry.grid(column=1, row=5, pady=10)
short_break_min_entry.insert(END, str(DEFAULT_SHORT_BREAK_MIN))

long_break_min_label = Label(window, text="Lunch Break:", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
long_break_min_label.grid(column=0, row=4, pady=10)
long_break_min_entry = Entry(window, width=5)
long_break_min_entry.grid(column=1, row=4, pady=10)
long_break_min_entry.insert(END, str(DEFAULT_LONG_BREAK_MIN))

start_hour_label = Label(window, text="Start Hour(24h):", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
start_hour_label.grid(column=2, row=3, pady=10)
start_hour_entry = Entry(window, width=5)
start_hour_entry.grid(column=3, row=3, pady=10)
start_hour_entry.insert(END, "8")

start_minute_label = Label(window, text="Start Minute:", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
start_minute_label.grid(column=2, row=4, pady=10)
start_minute_entry = Entry(window, width=5)
start_minute_entry.grid(column=3, row=4, pady=10)
start_minute_entry.insert(END, "0")

start_from_label = Label(window, text="Start From:", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
start_from_label.grid(column=2, row=5, pady=10)
start_from_entry = Entry(window, width=5)
start_from_entry.grid(column=3, row=5, pady=10)
start_from_entry.insert(END, "1")

current_time_label = Label(window, text="Time: ", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
current_time_label.grid(column=3, row=7, columnspan=2, pady=10)

start_now_label = Button(window, text="Start Now", highlightthickness=0, command=start_timer)
start_now_label.grid(column=0, row=6, pady=10)

reset_label = Button(window, text="Reset", highlightthickness=0, command=reset_timer)
reset_label.grid(column=1, row=6, pady=10)

schedule_label = Button(window, text="Schedule Start", highlightthickness=0, command=schedule_start)
schedule_label.grid(column=0, row=7, pady=10)

play_long_bell_label = Button(window, text="Play Long Bell", highlightthickness=0,
                              command=lambda: play_sound("long_bell.wav"))
play_long_bell_label.grid(column=3, row=6, pady=10)

play_short_bell_label = Button(window, text="Play Short Bell", highlightthickness=0, command=lambda: play_bells(1))
play_short_bell_label.grid(column=2, row=6, pady=10)

update_current_time()

window.mainloop()


