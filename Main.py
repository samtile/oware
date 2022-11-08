import threading
from tkinter import *
import time

PotArray = []


def distribute_beans(pot_number):
    print(pot_number)
    if PotArray[pot_number] == 0:
        return
    remaining_beans = PotArray[pot_number]
    current_pot = pot_number
    while remaining_beans > 0:
        print("Remaining", remaining_beans)
        Pots[current_pot].configure(relief="ridge")
        if current_pot == 11:
            current_pot = 0
        else:
            current_pot += 1
        print("Current ", current_pot)
        PotArray[current_pot] += 1
        PotArray[pot_number] -= 1
        remaining_beans -= 1
        time.sleep(0.5)
        refresh_pots_on_screen()


# GUI stuff
window = Tk()

ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
w = 800  # width for the Tk root
h = 500  # height for the Tk root
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

window.geometry('%dx%d+%d+%d' % (w, h, x, y))

frame = Frame(window, width=800, height=500)
frame.grid(row=10, column=10, padx=10, pady=5)

Buttons = []
Pots = []

for i in range(2):
    for j in range(6):
        k = j
        if i == 1:
            k += 6
        Buttons.append(Button(frame, text="", command= lambda ztemp=k: threading.Thread(target=distribute_beans, args=[ztemp]).start()))
        if k < 6:
            Buttons[k].grid(row=i, column=j, padx=5, pady=3, ipadx=10)
        else:
            Buttons[k].grid(row=i + 2, column=5-j, padx=5, pady=3, ipadx=10)

for i in range(2):
    for j in range(6):
        k = j
        if i == 1:
            k += 6
        Pots.append(Label(frame, height=1, width=10, borderwidth=3, relief="solid"))
        if k < 6:
            Pots[k].grid(row=i + 1, column=j, padx=5, pady=3, ipadx=10)
        else:
            Pots[k].grid(row=i + 1, column=5-j, padx=5, pady=3, ipadx=10)
# end GUI stuff


def refresh_pots_on_screen():
    for x in range(12):
        Pots[x].configure(text=PotArray[x])


for x in range(12):
    PotArray.append(4)

refresh_pots_on_screen()
window.mainloop()
