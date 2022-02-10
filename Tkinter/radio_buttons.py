from asyncio import selector_events
from pydoc import text
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("600x400")
root.resizable(False, False)
root.title("Widget Examples")

storage_variable = tk.StringVar()

option_one = ttk.Radiobutton(
    root,
    text="option 1",
    variable=storage_variable,
    value="first option"
)

option_two = ttk.Radiobutton(
    root,
    text="option 2",
    variable=storage_variable,
    value="second option"
)

option_three = ttk.Radiobutton(
    root,
    text="option 3",
    variable=storage_variable,
    value="third option"
)

option_one.pack()
option_two.pack()
option_three.pack()
root.mainloop()