import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("600x400")
root.resizable(False, False)
root.title("Widget Examples")

initial_value = tk.IntVar(value=20)
spin_box = ttk.Spinbox(
    root,
    values=(5,10,15,20,25,30),
    textvariable=initial_value,
    wrap=False
)

print(spin_box.get())

spin_box.pack()

root.mainloop()