import Manager
from Manager import force_add_tasks

# Creates task manager object
task_manager = Manager.TaskManager()

#Creates infinite loop that manages the user's actions
is_on = True

# Welcome message, lists possible operations that can be performed by the task manager
print("\nWelcome to your personal Task Manager!\n")
print("To view your tasks, input 'v'. Input 'a' to Add a task, input 'd' to Delete tasks,"
                           f" or input 'c' to mark a task as Completed. Input 'R' to Redo an action "
      f"or 'U' to Undo an action.\nDeleting and Marking tasks as Complete may be canceled by inputting 'Cancel'.")

# Infinite loop sequence that operates the task manager
while is_on:
    user_choice = task_manager.get_user_input()
    if user_choice == "v":
        task_manager.print_tasks()
    elif user_choice == "a":
        task_manager.add_task()
    elif user_choice == "c":
        # Checks that the user has a task to even mark complete
        if task_manager.total_tasks > 0:
            task_manager.mark_task_complete()
        else:
            force_add_tasks("mark as completed")
    elif user_choice == "d":
        # Checks that the user has a task to even delete
        if len(task_manager.task_list) > 0:
            task_manager.delete_task()
        # If the user does not have a task to delete, the user is forced to add a task.
        else:
            force_add_tasks("delete")
    elif user_choice == "r":
        task_manager.redo()
    elif user_choice == "u":
        task_manager.undo()
    elif user_choice == "off":
        is_on = False
    elif user_choice == "t":
        task_manager.print_background_tasks()
    else:
        print(f"\nError, {user_choice} is not a valid input. Please select an option again: ")
