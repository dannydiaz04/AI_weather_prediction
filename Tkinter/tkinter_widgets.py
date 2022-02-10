import imp
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("600x400")
root.resizable(False, False)
root.title("Widget Examples")

image = Image.open("logo.png")
photo = ImageTk.PhotoImage(image)
label = ttk.Label(root, image=photo, padding=5)
label.pack()


root.mainloop()