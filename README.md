# LING530G Final Project - To-do List Application

## Introduction
Inspired by some popular to-do list applications like Trello and Google Tasks, we plan to build a useful and user-friendly To-do List application. We can benefit from using this to-do list application because we manage our schedules better and avoid missing tasks. It helps time management and improves work efficiency.

## Functionality
- We can retrieve existing user information from the database and create a user by inputting the username and user email.
- A user can add a to-do item by filling out the item name, priority, due date, and tag information.
- A user can now choose to edit/update the selected to-do item in the list by changing the name, priority, due date, and tag.
- A user can delete a selected item.
- The program will auto-detect if the to-do item passes the due date based on the current date, if so, a red highlighting will be applied.
- A user can sort the to-do items by the due date and priority. The sorting is applied to the due date first and if the due date is the same then it will be sorted per priority.
- A tag is added to further clarify the status of the to-do item within the same category, i.e. done, working-on, and to-do status.

## Database
We mainly created three database tables – User, TodoItems, and Category. The User, TodoItems, and Category tables store user, item, and category information separately. TodoItems tables have two foreign keys ‘user_id’ and ‘category_id’ points to primary keys in the User and Category tables separately. The relationship between the User and TodoItems table is ‘one-to-many’ the same as the relationship between Category and TodoItems table. 

## Related Technology
Python, Tkinter, Database(SQLite)

## Files
- <code>main.py</code> main file - including Tkinter interface and operation functions
- <code>database.py</code> database file - including all the database functionalities 
(adopted from roster.py in the course material)

## Compile
Please install Python3! <br/>
Please use the command below to run the program. If you have any questions, please contact us.
```bash
$ python3 main.py
```

## Links
Demo Link: https://youtu.be/vGnu_Q-bdW8 <br/>
GitHub Link: https://github.com/mileyzjq/LING530G <br/>

## Group Members
Group 2 <br/>
Jiaqi Zhang (63174551) <br/>
Justina Bruns (70581079)  <br/>
Yang Du (78265148)  <br/>
