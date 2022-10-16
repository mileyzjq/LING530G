import tkinter as tk

window = tk.Tk()
window.title("To-do-list")
window.configure(bg='#d3d3d3')
lst =list()

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
    width=25,
)
menu.insert(0, "python")
menu.insert(1, "java")
lst.append("python")
lst.append("java")

menu.place(x=30, y=40)

text = tk.Text(
    borderwidth=5,
    height=1,
    width=20,
)
text.place(x=360, y=40)

def handle_click(event):
    lst.sort()
    n = len(lst)
    menu.delete(0, n)
    for i in range(n):
        menu.insert(i, lst[i])


button = tk.Button(text="sort")

button.bind("<Button-1>", handle_click)

button.place(x=360, y=80)

window.geometry('600x450')
window.mainloop()