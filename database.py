# adopted from roster.py in the course material
import sqlite3

try:
    conn = sqlite3.connect('todoList.sqlite')
    cur = conn.cursor()
except:
    print('Error: fail to connect database')

# Create User, TodoItems and Category tables
cur.executescript('''
CREATE TABLE IF NOT EXISTS User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE,
    email   TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Category (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    category_name   TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS TodoItems (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    item_name   TEXT,
    priority_number  INTEGER,
    due_date  TEXT,
    tag  TEXT,
    user_id     INTEGER,
    category_id   INTEGER,
    FOREIGN KEY (user_id) REFERENCES User (id),
    FOREIGN Key (category_id) REFERENCES Category (id)
);
''')

# id: 1, category_name: 'study'
# id: 2, category_name: 'life'
# id: 3, category_name: 'work'
# put pre-defined categories into database
category_lst = ['study', 'life', 'work']
for category in category_lst:
    cur.execute('''INSERT OR IGNORE INTO Category (category_name)
        VALUES ( ? )''', ( category, ) )
    conn.commit()

# id: 1, name: 'Josh', email: 'Josh@gmail.com'
# id: 2, name: 'Bob', email: 'Bob@gmail.com'
# put pre-defined users into database
user_lst = [('Josh','Josh@gmail.com'), ('Bob', 'Bob@gmail.com')]
for user in user_lst:
    cur.execute('''INSERT OR IGNORE INTO User (name, email)
        VALUES ( ?,? )''', ( user[0], user[1]) )
    conn.commit()

# add a new user to database
def add_user(user_name, user_email):
    cur.execute('''INSERT OR IGNORE INTO User (name, email)
        VALUES ( ?,? )''', ( user_name, user_email) )
    conn.commit()

# add a todo list item to database, and return the item id
def add_item(item_name, priority_number, due_date, tag, user_id, category_id):
    cur.execute('''INSERT OR IGNORE INTO TodoItems (item_name, priority_number, due_date, tag, user_id, category_id)
        VALUES ( ?,?,?,?,?,? )''', (item_name, priority_number, due_date, tag, user_id, category_id) )
    conn.commit()
    return cur.lastrowid

# update a todo list item in database
def update_item(user_id, category_id, item_id, new_item_name, new_priority_number, new_due_date, new_tag):
    cur.execute('''UPDATE TodoItems SET item_name = ?, priority_number = ?, due_date = ?, tag = ? WHERE user_id = ? AND category_id = ? AND id = ?''',
                (new_item_name, new_priority_number, new_due_date, new_tag, user_id, category_id, item_id))
    conn.commit()

# delete a todo list item from database based on item_id
def delete_item(user_id, category_id, item_id):
    cur.execute('''DELETE FROM TodoItems WHERE user_id = ? AND category_id = ? AND id = ?''', (user_id, category_id, item_id))
    conn.commit()

# get user id based on user name
def get_user_id(user_name):
    cur.execute('''SELECT id FROM User WHERE name = ?''', (user_name,))
    user_id = cur.fetchone()[0]
    return user_id    

# get category name based on category id
def get_category_id(category_name):
    cur.execute('''SELECT id FROM Category WHERE category_name = ?''', (category_name,))
    category_id = cur.fetchone()[0]
    return category_id

# sort todo list based on priority number
def sort_by_due_date_and_priority(user_id, category_name):
    cur.execute('''SELECT id, item_name, priority_number, due_date, tag FROM TodoItems WHERE user_id = ? AND category_id = ? ORDER BY due_date ASC, priority_number DESC''', (user_id, category_name,) )
    lst = cur.fetchall()
    return lst

# get todo list based on user id and category id
def get_todo_list(user_id, category_id):
    cur.execute('''SELECT id, item_name, priority_number, due_date, tag FROM TodoItems WHERE user_id = ? AND category_id = ?''', (user_id, category_id))
    lst = cur.fetchall()
    return lst


conn.commit()
