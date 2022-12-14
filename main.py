from datetime import datetime
import tkinter as tk
import database as db
from tkinter import *
from tkinter import ttk
import re

# input user name
user = str(input('Enter your name: '))
# set current category with initial value 'study'
currentCategory = 'study'

# user enter email address and system validate email address
def get_email():
    # input and check email address. if email address is invalid, ask user to enter again
    # three attempts in total
    for i in range(3):
        email = str(input('Enter your email: '))
        # validate email address
        if len(email) > 7:
            if re.match("^.+@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
                return email 
        else:
            print('Invalid email address, please enter try again!')
    print('Too many attempts, exit!')
    exit()

# get user_id from database, if user does not exist, create a new user to the database
try:
    user_id = db.get_user_id(user)
except:
    print('Welcome new user!')
    email = get_email()
    db.add_user(user, email)
    print('User created successfully!')


# set window configuration
window = tk.Tk()
window.title("To-do-list")
window.configure(bg='#d3d3d3')

# display greeting message, like "Hi, Josh!"
greeting = tk.Label(text = "Hi, " + user + "!", foreground="black", background="#d3d3d3")
greeting.place(x=5, y=0)

# define treeview, all the todo list items will be shown in the treeview based on category selected
columns = ('todoitems', 'priority', 'due_date', 'tag')
tree = ttk.Treeview(window, columns=columns, show='headings')
# define headings
tree.heading('todoitems', text='To-do items')
tree.column('priority', width=180)
tree.heading('priority', text='Priority')
tree.column('priority', width=120)
tree.heading('due_date', text='Due date')
tree.column('due_date', width=120)
tree.heading('tag', text='Tag')
tree.column('tag', width=120)
tree.grid(row=0, column=0, sticky='nsew')
tree.place(x=15, y=80)
tree.tag_configure('overdue', background='red')

# get current date
today = datetime.today()
today_date = today.strftime("%Y-%m-%d")

# if task is overdue, change the background color to red
def add_overdue_tag():
    listOfEntriesInTreeView=tree.get_children()
    for each in listOfEntriesInTreeView:
        due_date = datetime.strptime(tree.item(each)['values'][2], "%Y-%m-%d")
        if(due_date < today):
            tree.item(each, tags='overdue')

# display items in treeview
list = db.get_todo_list(db.get_user_id(user), db.get_category_id(currentCategory))
for row in list:
    tree.insert('', tk.END, iid=row[0], values=(row[1], row[2], row[3], row[4]))
# add tag to overdue items
add_overdue_tag()

# Create new todo item label and input box
new_todo_item = tk.Label(text = "New To-do Item", foreground="black", background="#d3d3d3")
new_todo_item.place(x=600, y=50)
todo_item_entry = tk.Entry(width=12)
todo_item_entry.place(x=600, y=80)

# Create priority number label and input box
priority = tk.Label(text = "Priority", foreground="black", background="#d3d3d3")
priority.place(x=726, y=50)
priority_entry = tk.Entry(width=5)
priority_entry.place(x=726, y=80)

# Create due date label and input box
due_date = tk.Label(text = "Due date", foreground="black", background="#d3d3d3")
due_date.place(x=790, y=50)
due_date_entry = tk.Entry(width=9)
due_date_entry.place(x=790, y=80)

# Create due date label and input box
tag = tk.Label(text = "Tag", foreground="black", background="#d3d3d3")
tag.place(x=890, y=50)
tag_entry = tk.Entry(width=8)
tag_entry.place(x=890, y=80)

# when click add button, add new item to the tree
def handle_add_button():
    item_id = db.add_item(todo_item_entry.get(), priority_entry.get(), due_date_entry.get(), tag_entry.get(), db.get_user_id(user), db.get_category_id(currentCategory))
    tree.insert('', tk.END, iid=item_id, values=(todo_item_entry.get(), priority_entry.get(), due_date_entry.get(), tag_entry.get()))
    add_overdue_tag()

# when click edit button, edit selected item
def handle_edit_button():
    item_id = tree.focus()
    db.update_item(db.get_user_id(user), db.get_category_id(currentCategory), item_id, todo_item_entry.get(), priority_entry.get(), due_date_entry.get(), tag_entry.get())
    tree.item(item_id, values=(todo_item_entry.get(), priority_entry.get(), due_date_entry.get(), tag_entry.get()))
    add_overdue_tag()
    
# when click delete button, delete selected item
def handle_delete_button():
    item_id = tree.focus()
    db.delete_item(db.get_user_id(user), db.get_category_id(currentCategory), item_id)
    tree.delete(tree.selection())

# when click sort button, sort items based on priority number in descending order
def handle_sort_button():
    # delete all items in treeview
    for item in tree.get_children():
        tree.delete(item)
    # sort items in descending order and display items in treeview
    list = db.sort_by_due_date_and_priority(db.get_user_id(user), db.get_category_id(currentCategory))
    for row in list:
        tree.insert('', tk.END, iid=row[0], values=(row[1], row[2], row[3], row[4]))
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
        tree.insert('', tk.END, iid=row[0], values=(row[1], row[2], row[3], row[4]))
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
add_button = tk.Button(text="Add", width=18, height=2, command=handle_add_button)
add_button.place(x=600, y=120)

# edit button settings
edit_button = tk.Button(text="Edit", width=18, height=2, command=handle_edit_button)
edit_button.place(x=600, y=170)

# delete button settings
delete_button = tk.Button(text="Delete", width=18, height=2, command=handle_delete_button)
delete_button.place(x=600, y=220)

# sort button settings
sort_button = tk.Button(text="Sort", width=18, height=2, command=handle_sort_button)
sort_button.place(x=600, y=270)

window.geometry('1000x500')
window.mainloop()