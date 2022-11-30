import tkinter as tk
import database as db
from tkinter import *
from tkinter import ttk

# input user name
user = str(input('Enter your name: '))
currentCategory = 'study'

# get user_id from database, if user does not exist, create a new user to database
try:
    user_id = db.get_user_id(user)
except:
    print('Welcome new user!')
    email = str(input('Enter your email: '))
    db.add_user(user, email)


# set window
window = tk.Tk()
window.title("To-do-list")
window.configure(bg='#d3d3d3')

# define treeview, all the todo list items will be shown in the treeview based on category selected
columns = ('todoitems', 'priority')
tree = ttk.Treeview(window, columns=columns, show='headings')
# define headings
tree.heading('todoitems', text='To-do items')
tree.heading('priority', text='Priority')
tree.grid(row=0, column=0, sticky='nsew')
tree.place(x=15, y=80)
list = db.get_todo_list(db.get_user_id(user), db.get_category_id(currentCategory))
for row in list:
    tree.insert('', tk.END, values=(row[0], row[1]))

# Create new todo item label and input box
new_todo_item = tk.Label(text = "New To-do Item", foreground="black", background="#d3d3d3")
new_todo_item.place(x=450, y=30)
toDoItemEntry = tk.Entry(width=12)
toDoItemEntry.place(x=450, y=60)

# Create priority number label and input box
priority_number = tk.Label(text = "Priority", foreground="black", background="#d3d3d3")
priority_number.place(x=580, y=30)
priorityEntry = tk.Entry(width=6)
priorityEntry.place(x=580, y=60)

# when click add button, add new item to the tree
def handle_add_button():
    tree.insert('', tk.END, values=(toDoItemEntry.get(), priorityEntry.get()))
    db.add_item(toDoItemEntry.get(), priorityEntry.get(), db.get_user_id(user), db.get_category_id(currentCategory))

# when click delete button, delete selected item
def handle_delete_button():
    cur_item = tree.focus()
    item_name = tree.item(cur_item)['values'][0]
    item_priority = tree.item(cur_item)['values'][1]
    tree.delete(tree.selection())
    db.delete_item(db.get_user_id(user), db.get_category_id(currentCategory), item_name, item_priority)

# when click sort button, sort items based on priority number in descending order
def handle_sort_button():
    # delete all items in treeview
    for item in tree.get_children():
        tree.delete(item)
    # sort items in descending order and display items in treeview
    list = db.sort_by_priority(db.get_user_id(user), db.get_category_id(currentCategory))
    for row in list:
        tree.insert('', tk.END, values=(row[0], row[1]))

# change button color, when category is selected
def handle_button_color_change(category):
    # default color is black
    study_button['fg'] = 'black'
    work_button['fg'] = 'black'
    life_button['fg'] = 'black'
    # change color to red when category is selected
    if(category == 'study'):
        study_button['fg'] = 'blue'
    elif(category == 'work'):
        work_button['fg'] = 'blue'
    else:
        life_button['fg'] = 'blue'

# change to do list based on category selected
def handle_category_button(category):
    global currentCategory
    currentCategory = category
    #category_label['text'] = "Current category: " + category
    handle_button_color_change(category)
    for item in tree.get_children():
        tree.delete(item)
    # display items in treeview
    list = db.get_todo_list(db.get_user_id(user), db.get_category_id(currentCategory))
    for row in list:
        tree.insert('', tk.END, values=(row[0], row[1]))

# study button settings
study_button = tk.Button(text="Study", width=5, fg="blue", command=lambda: handle_category_button('study'))
study_button.place(x=30, y=35)

# work button settings
work_button = tk.Button(text="Work", width=5, command=lambda: handle_category_button('work'))
work_button.place(x=100, y=35)

# life button settings
life_button = tk.Button(text="Life", width=5, command=lambda: handle_category_button('life'))
life_button.place(x=170, y=35)

# add button settings
add_button = tk.Button(text="Add", width=15, height=2, command=handle_add_button)
add_button.place(x=450, y=110)

# delete button settings
delete_button = tk.Button(text="Delete", width=15, height=2, command=handle_delete_button)
delete_button.place(x=450, y=160)

# sort button settings
sort_button = tk.Button(text="Sort", width=15, height=2, command=handle_sort_button)
sort_button.place(x=450, y=210)

# category_label = tk.Label(text = "Current category: "+currentCategory, foreground="blue", background="#d3d3d3")
# category_label.place(x=30, y=60)

window.geometry('720x500')
window.mainloop()
