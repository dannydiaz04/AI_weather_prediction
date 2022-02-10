from asyncio import selector_events
from pydoc import text
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("600x400")
root.resizable(False, False)
root.title("Widget Examples")

selected_weekday = tk.StringVar()
weekday = ttk.Combobox(root, textvariable=selected_weekday)
weekday["values"] = ("Monday", "Tuesday", "Wednesday", "Thurday", "Friday")
weekday["state"] = "readonly"
weekday.pack()

def handle_selection(event):
    print("today is", selected_weekday.get())
    print("but we're gonna change it to Friday")
    selected_weekday.set("Friday")
    print(weekday.current())

weekday.bind("<<ComboboxSelected>>", handle_selection)

root.mainloop()

print(selected_weekday.get(), " was selected")