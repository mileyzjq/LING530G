import tkinter as tk
import database as db
from tkinter import *
from tkinter import ttk

user = input('Enter your name: ')
currentCategory = 'study'
# check whether the input is a valid string
try:
    user = str(user)
    user_id = db.get_user_id(user)
except:
    print("Invalid input")

# set window
window = tk.Tk()
window.title("To-do-list")
window.configure(bg='#d3d3d3')

columns = ('todoitems', 'priority')
tree = ttk.Treeview(window, columns=columns, show='headings')
# define headings
tree.heading('todoitems', text='To-do items')
tree.heading('priority', text='Priority')
tree.grid(row=0, column=0, sticky='nsew')
tree.place(x=10, y=100)
list = db.get_todo_list(db.get_user_id(user), db.get_category_id(currentCategory))
for row in list:
    tree.insert('', tk.END, values=(row[0], row[1]))

# Create text input box
toDoItemEntry = tk.Entry(width=10)
toDoItemEntry.place(x=420, y=10)

priorityEntry = tk.Entry(width=3)
priorityEntry.place(x=540, y=10)

def handle_add_button():
    tree.insert('', tk.END, values=(toDoItemEntry.get(), priorityEntry.get()))
    db.add_item(toDoItemEntry.get(), priorityEntry.get(), db.get_user_id(user), db.get_category_id(currentCategory))

def handle_delete_button():
    tree.delete(tree.selection())
    db.delete_item(db.get_user_id(user), db.get_category_id(currentCategory))

def handle_sort_button():
    for item in tree.get_children():
        tree.delete(item)
    list = db.sort_by_priority(db.get_user_id(user), db.get_category_id(currentCategory))
    for row in list:
        tree.insert('', tk.END, values=(row[0], row[1]))

def handle_category_button(category):
    global currentCategory
    currentCategory = category
    for item in tree.get_children():
        tree.delete(item)
    list = db.get_todo_list(db.get_user_id(user), db.get_category_id(currentCategory))
    for row in list:
        tree.insert('', tk.END, values=(row[0], row[1]))

studyButton = tk.Button(text="Study", width=5, command=lambda: handle_category_button('study'))
studyButton.place(x=30, y=35)

workButton = tk.Button(text="Work", width=5, command=lambda: handle_category_button('work'))
workButton.place(x=100, y=35)

lifeButton = tk.Button(text="Life", width=5, command=lambda: handle_category_button('life'))
lifeButton.place(x=170, y=35)

add_button = tk.Button(text="Add", width=15, height=2,
                       command=handle_add_button)
add_button.place(x=420, y=80)

delete_button = tk.Button(text="Delete", width=15, height=2,
                   command=handle_delete_button)
delete_button.place(x=420, y=130)

sort_button = tk.Button(text="Sort", width=15, height=2, command=handle_sort_button)
sort_button.place(x=420, y=180)

window.geometry('800x600')
window.mainloop()
