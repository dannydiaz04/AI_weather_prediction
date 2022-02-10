import tkinter as tk
import tkinter.font as font
from tkinter import ttk

from matplotlib.pyplot import text

root = tk.Tk()
root.title("Distance Converter")

font.nametofont("TkDefaultFont").configure(size=15)

meters_value = tk.StringVar()
feet_value = tk.StringVar()

main = ttk.Frame(root, padding=(30, 15))
main.grid()

def calculate_feet(*args):
    try:
        meters = float(meters_value.get())
        feet = meters * 3.28084
        feet_value.set(f"{feet:.3f}")
    except ValueError:
        pass

root.columnconfigure(0, weight=1)

meters_label = ttk.Label(main, text="Meters: ")
meters_input = ttk.Entry(main, width=10, textvariable=meters_value, font=("Segoe UI", 15))
feet_label = ttk.Label(main, text="Feet: ")
feet_display = ttk.Label(main, textvariable=feet_value)
calc_button = ttk.Button(main, text="Calculate", command=calculate_feet)

meters_label.grid(column=0, row=0, sticky="W")
meters_input.grid(column=1, row=0, sticky="EW")
meters_input.focus()

feet_label.grid(column=0, row=1, sticky="W")
feet_display.grid(column=1, row=1, sticky="EW")

calc_button.grid(column=0, row=2, columnspan=2, sticky="EW")

for child in main.winfo_children():
    child.grid_configure(padx=15, pady=15)

root.bind("<Return>", calculate_feet)
root.bind("<KP_Enter>", calculate_feet)

root.mainloop()  

# 720-865-4600 5 1 9