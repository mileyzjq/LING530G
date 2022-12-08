from datetime import datetime
import tkinter as tk
import database as db
from tkinter import *
from tkinter import ttk

# input user name
user = str(input('Enter your name: '))
# set current category with initial value 'study'
currentCategory = 'study'

# get user_id from database, if user does not exist, create a new user to the database
try:
    user_id = db.get_user_id(user)
except:
    print('Welcome new user!')
    email = str(input('Enter your email: '))
    db.add_user(user, email)
    print('User created successfully!')


# set window
window = tk.Tk()
window.title("To-do-list")
window.configure(bg='#d3d3d3')

# display greeting message, like "Hi, Josh!"
greeting = tk.Label(text = "Hi, " + user + "!", foreground="black", background="#d3d3d3")
greeting.place(x=5, y=0)

# define treeview, all the todo list items will be shown in the treeview based on category selected
columns = ('todoitems', 'priority', 'due_date')
tree = ttk.Treeview(window, columns=columns, show='headings')
# define headings
tree.heading('todoitems', text='To-do items')
tree.heading('priority', text='Priority')
tree.heading('due_date', text='Due date')
tree.grid(row=0, column=0, sticky='nsew')
tree.place(x=15, y=80)
tree.tag_configure('overdue', background='red')
today = datetime.today()
today_date = today.strftime("%Y-%m-%d")
list = db.get_todo_list(db.get_user_id(user), db.get_category_id(currentCategory))
for row in list:
    tree.insert('', tk.END, values=(row[0], row[1], row[2]))
def add_overdue_tag():
    listOfEntriesInTreeView=tree.get_children()
    for each in listOfEntriesInTreeView:
        due_date = datetime.strptime(tree.item(each)['values'][2], "%Y-%m-%d")
        if(due_date < today):
            tree.item(each, tags='overdue')
add_overdue_tag()

# Create new todo item label and input box
new_todo_item = tk.Label(text = "New To-do Item", foreground="black", background="#d3d3d3")
new_todo_item.place(x=650, y=50)
toDoItemEntry = tk.Entry(width=12)
toDoItemEntry.place(x=650, y=80)

# Create priority number label and input box
priority_number = tk.Label(text = "Priority", foreground="black", background="#d3d3d3")
priority_number.place(x=780, y=50)
priorityEntry = tk.Entry(width=6)
priorityEntry.place(x=780, y=80)

# Create due date label and input box
due_date = tk.Label(text = "Due date", foreground="black", background="#d3d3d3")
due_date.place(x=860, y=50)
due_dateEntry = tk.Entry(width=6)
due_dateEntry.place(x=860, y=80)

# when click add button, add new item to the tree
def handle_add_button():
    tree.insert('', tk.END, values=(toDoItemEntry.get(), priorityEntry.get(), due_dateEntry.get()))
    db.add_item(toDoItemEntry.get(), priorityEntry.get(), due_dateEntry.get(), db.get_user_id(user), db.get_category_id(currentCategory))
    add_overdue_tag()

# when click delete button, delete selected item
def handle_delete_button():
    cur_item = tree.focus()
    item_name = tree.item(cur_item)['values'][0]
    item_priority = tree.item(cur_item)['values'][1]
    due_date = tree.item(cur_item)['values'][2]
    tree.delete(tree.selection())
    db.delete_item(db.get_user_id(user), db.get_category_id(currentCategory), item_name, item_priority, due_date)

# when click sort button, sort items based on priority number in descending order
def handle_sort_button():
    # delete all items in treeview
    for item in tree.get_children():
        tree.delete(item)
    # sort items in descending order and display items in treeview
    list = db.sort_by_due_date_and_priority(db.get_user_id(user), db.get_category_id(currentCategory))
    for row in list:
        tree.insert('', tk.END, values=(row[0], row[1], row[2]))
    add_overdue_tag()
    
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
        tree.insert('', tk.END, values=(row[0], row[1], row[2]))
    add_overdue_tag()

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
add_button.place(x=650, y=120)

# delete button settings
delete_button = tk.Button(text="Delete", width=15, height=2, command=handle_delete_button)
delete_button.place(x=650, y=170)

# sort button settings
sort_button = tk.Button(text="Sort", width=15, height=2, command=handle_sort_button)
sort_button.place(x=650, y=220)

window.geometry('960x500')
window.mainloop()