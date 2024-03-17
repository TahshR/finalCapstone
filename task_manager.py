import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# Function to register a new user
def reg_user():
    # - Request input of a new username
    new_username = input("\nNew Username: ")
    if new_username in username_password:
        print("Username already exists.")
        return

    # - Request input of a new password    
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")
   
    # - Check if the new password and confirmed password are the same.
    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    # - If they are the same, add them to the user.txt file,     
    username_password[new_username] = new_password
    with open("user.txt", "a") as user_file:
        user_file.write(f"\n{new_username};{new_password}")
    print("New user added.")

# Function to add a new task
def add_task():
    task_username = input("\nName of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    
    # Then get the current date.
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    with open("tasks.txt", "a") as task_file:
        str_attrs = [
            new_task['username'],
            new_task['title'],
            new_task['description'],
            new_task['due_date'].strftime(DATETIME_STRING_FORMAT),
            new_task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
            "No" if not new_task['completed'] else "Yes"
        ]
        task_file.write("\n" + ";".join(str_attrs))
    print("Task successfully added.")

# Function to view all tasks
def view_all():
    for idx, t in enumerate(task_list, start=1):
        disp_str = f"\nTask {idx}:\n"
        disp_str += f"Title: {t['title']}\n"
        disp_str += f"Assigned to: {t['username']}\n"
        disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: {t['description']}\n"
        disp_str += f"Task has been completed: {t['completed']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine():
    for idx, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            disp_str = f"\nTask {idx}:\n"
            disp_str += f"Title: {t['title']}\n"
            disp_str += f"Assigned to: {t['username']}\n"
            disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: {t['description']}\n"
            disp_str += f"Task has been completed: {t['completed']}\n"
            print(disp_str)

# Function to mark a task as complete
def mark_task_complete():
    if not task_list:
        print("\nNo tasks available.")
        return

    print("\nTasks:")
    for idx, task in enumerate(task_list, start=1):
        print(f"{idx}. {task['title']}")

    task_idx = int(input("\nEnter the task number to mark as complete: "))
    if 1 <= task_idx <= len(task_list):
        task_list[task_idx - 1]['completed'] = True
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task marked as complete.")
    else:
        print("Invalid task number.")

# Function to edit a task
def edit_task():
    if not task_list:
        print("\nNo tasks available.")
        return

    print("\nTasks:")
    for idx, task in enumerate(task_list, start=1):
        print(f"{idx}. {task['title']}")

    task_idx = int(input("\nEnter the task number to edit: "))
    if 1 <= task_idx <= len(task_list):
        task = task_list[task_idx - 1]
        if not task['completed']:
            new_username = input("New Username (press enter to keep current): ")
            if new_username and new_username in username_password:
                task['username'] = new_username
            new_due_date = input("New Due Date (YYYY-MM-DD) (press enter to keep current): ")
            if new_due_date:
                try:
                    task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                except ValueError:
                    print("Invalid datetime format. Task due date remains unchanged.")
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
            print("Task edited successfully.")
        else:
            print("Completed tasks cannot be edited.")
    else:
        print("Invalid task number.")

# Display statistics
def dis_stat():
    if curr_user == 'admin':
        
        num_users = len(username_password.keys())
        num_tasks = len(task_list)
        completed_tasks = sum(1 for task in task_list if task['completed'])
        incomplete_tasks = num_tasks - completed_tasks
        overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())


        print("\n-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print(f"Number of completed tasks: \t {completed_tasks}")
        print(f"Number of uncompleted tasks: \t {incomplete_tasks}")
        print(f"Number of overdue tasks: \t {overdue_tasks}")
        print("-----------------------------------")    
    
    elif curr_user != 'admin':
        print("\nAccess denied. This option is only available to administrators.")
        return


# Function to generate reports
def generate_reports():
    num_users = len(username_password)
    num_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    incomplete_tasks = num_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total number of tasks: {num_tasks}\n")
        task_overview_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Total number of uncompleted tasks: {incomplete_tasks}\n")
        task_overview_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of tasks incomplete: {(incomplete_tasks / num_tasks) * 100:.2f}%\n")
        task_overview_file.write(f"Percentage of tasks overdue: {(overdue_tasks / num_tasks) * 100:.2f}%\n")

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total number of users: {num_users}\n")
        user_overview_file.write(f"Total number of tasks: {num_tasks}\n")
        for user, password in username_password.items():
            user_tasks = sum(1 for task in task_list if task['username'] == user)
            user_completed_tasks = sum(1 for task in task_list if task['username'] == user and task['completed'])
            user_incomplete_tasks = user_tasks - user_completed_tasks
            user_overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())
            user_overview_file.write(f"\nUser: {user}\n")
            user_overview_file.write(f"Total number of tasks assigned: {user_tasks}\n")
            user_overview_file.write(f"Percentage of total tasks assigned: {(user_tasks / num_tasks) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of completed tasks: {(user_completed_tasks / user_tasks) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of incomplete tasks: {(user_incomplete_tasks / user_tasks) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {(user_overdue_tasks / user_tasks) * 100:.2f}%\n")

while True:
    print()
    menu = input('''Select one of the following Options below:
\nr - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
mc - Mark a task as complete
et - Edit a task
ds - Display statistics
g - Generate reports
e - Exit
\n:''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'mc':
        mark_task_complete()

    elif menu == 'et':
        edit_task()
    
    elif menu == 'ds':
        dis_stat()

    elif menu == 'g' and curr_user == 'admin':
        generate_reports()

    elif menu == 'e':
        print('Goodbye!!!')
        break

    else:
        print("You have made a wrong choice, Please Try again")
