import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("600x400")
root.resizable(False, False)
root.title("Widget Examples")

def handle_scale_change(event):
    print(scale.get())

current_value = tk.DoubleVar()

scale = ttk.Scale(
    root, 
    orient="horizontal",
    from_=0, to=10,
    command=handle_scale_change,
    variable=current_value)

scale.pack(fill="x")

root.mainloop()