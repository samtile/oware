import threading
import tkinter.messagebox
from tkinter import *
import time
from tkinter import messagebox

pots = []
player_one_pots = [0, 1, 2, 3, 4, 5]
player_two_pots = [6, 7, 8, 9, 10, 11]


def check_and_process_capture(pots_to_check):
    for i in pots_to_check:
        if pots[i] in [2, 3]:
            game.scores[game.current_player] += pots[i]
            pots[i] = 0
    refresh_screen()


# When a button is pressed, run the main game turn
def process_turn(pot_number):
    disable_buttons()
    pots_sown = []
    remaining_beans = pots[pot_number]
    current_pot = pot_number
    pot_fields[current_pot].configure(relief="solid")
    previous_pot = -1
    while remaining_beans > 0:
        if previous_pot != -1:
            pot_fields[previous_pot].configure(relief="groove")
        if current_pot == 11:
            current_pot = 0
        else:
            current_pot += 1
        pots[current_pot] += 1
        pots_sown.append(current_pot)
        pots[pot_number] -= 1
        remaining_beans -= 1
        time.sleep(0.5)
        refresh_screen()
        previous_pot = current_pot
    pot_fields[previous_pot].configure(relief="ridge")
    time.sleep(0.5)

    check_and_process_capture(set(player_two_pots) & set(pots_sown) if game.current_player == 0 else set(player_one_pots) & set(pots_sown))

    for x in range(12):
        pot_fields[x].configure(relief="ridge")
    check_for_win()
    game.current_player = 1 if game.current_player == 0 else 0
    enable_buttons()

# GUI stuff
window = Tk()
window.title("Oware")

ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
w = 700
h = 200
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

window.geometry('%dx%d+%d+%d' % (w, h, x, y))

frame = Frame(window, width=800, height=500)
frame.grid(row=10, column=10, padx=10, pady=5)

player_labels = [Label(frame, height=1, width=10, borderwidth=3, relief="flat"),
                Label(frame, height=1, width=10, borderwidth=3, relief="flat")]

score_fields = [Label(frame, height=1, width=10, borderwidth=3, relief="ridge"),
                Label(frame, height=1, width=10, borderwidth=3, relief="ridge")]

pot_buttons = []
pot_fields = []

for i in range(2):
    for j in range(6):
        k = j
        if i == 1:
            k += 6
        pot_buttons.append(
            Button(frame, text="+", command=lambda ztemp=k: threading.Thread(target=process_turn, args=[ztemp]).start()))
        if k < 6:
            pot_buttons[k].grid(row=i + 1, column=j, padx=5, pady=3, ipadx=10)
        else:
            pot_buttons[k].grid(row=i + 4, column=5 - j, padx=5, pady=3, ipadx=10)

for i in range(2):
    for j in range(6):
        k = j
        if i == 1:
            k += 6
        pot_fields.append(Label(frame, height=1, width=10, borderwidth=3, relief="ridge"))
        if k < 6:
            pot_fields[k].grid(row=i + 2, column=j, padx=5, pady=3, ipadx=10)
        else:
            pot_fields[k].grid(row=i + 3, column=5 - j, padx=5, pady=3, ipadx=10)


# end GUI stuff


class GameState:
    current_player = 0
    scores = [0, 0]


def refresh_screen():
    for x in range(12):
        pot_fields[x].configure(text=pots[x])
    for y in range(2):
        score_fields[y].configure(text=game.scores[y])


def enable_buttons():
    for i in player_one_pots if game.current_player == 1 else player_two_pots:
        pot_buttons[i].configure(state="disabled")
        pot_buttons[i].configure(relief="sunken")
    for j in player_one_pots if game.current_player == 0 else player_two_pots:
        pot_buttons[j].configure(state="normal")
        pot_buttons[j].configure(relief="raised")
    for k in range(12):
        if pots[k]==0:
            pot_buttons[k].configure(state="disabled")
            pot_buttons[k].configure(relief="sunken")


def disable_buttons():
    for i in range(12):
        pot_buttons[i].configure(state="disabled")
        pot_buttons[i].configure(relief="sunken")


def check_for_win():
    if game.scores[0] >= 25:
        messagebox.showinfo(message="Player 1 has won!")
        new_game()
    if game.scores[1] >= 25:
        messagebox.showinfo(message="Player 2 has won!")
        new_game()
    if game.scores[0] == 24 and game.scores[1] == 24:
        messagebox.showinfo(message="It is a draw!")
        new_game()


def new_game():
    disable_buttons()
    game = GameState()
    for i in range(12):
        pots[i] = 4
    enable_buttons()
    refresh_screen()


for x in range(12):
    pots.append(4)
game = GameState()
refresh_screen()

player_labels[0].grid(row=0, column=0, padx=5, pady=3, ipadx=10)
score_fields[0].grid(row=0, column=1, padx=5, pady=3, ipadx=10)
player_labels[1].grid(row=6, column=0, padx=5, pady=3, ipadx=10)
score_fields[1].grid(row=6, column=1, padx=5, pady=3, ipadx=10)
player_labels[0].configure(text="Player 1 Score:")
player_labels[1].configure(text="Player 2 Score:")
enable_buttons()
window.mainloop()