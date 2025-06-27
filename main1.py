import re
from manager.task_manager import TaskManager
from datetime import datetime
from utils.exceptions import EntityNotFoundError

def print_menu():
    print("\nTask Management System")
    print("1. Create User")
    print("2. Create Task")
    print("3. Assign Task to User")
    print("4. View All Tasks")
    print("5. View Tasks by User ID")
    print("6. View Tasks by Status")
    print("7. Delete User")
    print("8. Delete Task")
    print("9. Exit")

def get_date_input(prompt):
    """
    Prompt the user to enter a date in 'YYYY-MM-DD' format and return it as a datetime.date object.
    """
    while True:
        try:
            date_str = input(prompt + " (YYYY-MM-DD): ")
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Try again.")

def validate_name(name):
    """
    Validates that the name contains only letters and spaces.
    Raises ValueError if invalid.
    """
    if not name.strip():
        raise ValueError("Name cannot be empty.")
    if not re.fullmatch(r"[A-Za-z ]+", name):
        raise ValueError("Name must contain only alphabets and spaces.")

def main():
    """
    Main function to run the task management system.
    """
    tm = TaskManager()

    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            uid = input("Enter user ID: ")
            name = input("Enter name: ")
            try:
                validate_name(name)
                email = input("Enter email: ")
                tm.create_user(uid, name, email)
                print("User created successfully.")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "2":
            tid = input("Enter task ID: ")
            title = input("Enter task title: ")
            desc = input("Enter description: ")
            due_obj = get_date_input("Enter due date")
            due = due_obj.strftime("%Y-%m-%d")
            priority = input("Enter priority (Low/Medium/High) [default=Medium]: ") or "Medium"
            try:
                tm.create_task(tid, title, desc, due, priority)
                print("Task created successfully.")
            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == "3":
            tid = input("Enter task ID to assign: ")
            uid = input("Enter user ID to assign to: ")
            try:
                tm.assign_task_to_user(tid, uid)
                print("Task assigned successfully.")
            except EntityNotFoundError as ve:
                print(f"Error: {ve}")

        elif choice == "4":
            tasks = tm.list_all_tasks()
            if tasks:
                for task in tasks:
                    print(task.display_info())
            else:
                print("No tasks available.")

        elif choice == "5":
            uid = input("Enter user ID: ")
            tasks = tm.list_tasks_by_user(uid)
            if tasks:
                for task in tasks:
                    print(task.display_info())
            else:
                print("No tasks found for that user.")

        elif choice == "6":
            status = input("Enter status (To Do/In Progress/Done): ").upper()
            valid_statuses = {"TO DO", "IN PROGRESS", "DONE"}
            if status not in valid_statuses:
                print("Invalid status.")
                continue
            tasks = tm.list_tasks_by_status(status)
            if tasks:
                for task in tasks:
                    print(task.display_info())
            else:
                print("No tasks with that status.")
                

        elif choice == "7":
            uid = input("Enter user ID to delete: ")
            try:
                tm.delete_user(uid)
                print("User deleted successfully.")
            except EntityNotFoundError:
                print(f"User with ID '{uid}' not found.")

            

        elif choice == "8":
            tid = input("Enter task ID to delete: ")
            try:
                tm.delete_task(tid)
                print("Task deleted successfully.")
            except EntityNotFoundError:
                print(f"Task with ID '{tid}' not found.")

        elif choice == "9":
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
