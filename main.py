import tkinter as tk
import database as db

name = input('Enter your name: ')
# check whether the input is a valid string
try:
    name = str(name)
except:
    print("Invalid input")

# set window
window = tk.Tk()
window.title("To-do-list")
window.configure(bg='#d3d3d3')
lst =list()

button = tk.Button(text="A", width=5)
button.bind("<Button-1>")
button.place(x=30, y=35)

button = tk.Button(text="B", width=5)
button.bind("<Button-1>")
button.place(x=100, y=35)

button = tk.Button(text="C", width=5)
button.bind("<Button-1>")
button.place(x=170, y=35)

# set label
title = tk.Label(
    text="To-do List Board",
    foreground="white",  # Set the text color to white
    background="blue",
    width=20,
)
title.pack()

menu = tk.Listbox(
    bd=2,
    height=20,
    width=30,
)
menu.insert(0, "python")
menu.insert(1, "java")
lst.append("python")
lst.append("java")

menu.place(x=30, y=55)

text = tk.Text(
    borderwidth=5,
    height=1,
    width=20,
)
text.place(x=360, y=55)

def handle_click(event):
    lst.sort()
    n = len(lst)
    menu.delete(0, n)
    for i in range(n): 
        menu.insert(i, lst[i])

button = tk.Button(text="Add", width=15, height=2)
button.bind("<Button-1>", handle_click)
button.place(x=360, y=100)

button = tk.Button(text="Delete", width=15, height=2)
button.bind("<Button-1>", handle_click)
button.place(x=360, y=150)

button = tk.Button(text="Sort", width=15, height=2)
button.bind("<Button-1>", handle_click)
button.place(x=360, y=200)

window.geometry('600x450')
window.mainloop()