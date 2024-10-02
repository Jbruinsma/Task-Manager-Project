import Task

def force_add_tasks(operation):
    """
    Prints statement telling the user they have no tasks to use the desired operation on
    """
    print(f"\nYou have no tasks to {operation}, add some!")

def cancel_operation(user_input):
    """
    Checks if the user wants to cancel the operation they chose
    """
    # Checks if the user wants to cancel the operation they chose
    if user_input == "cancel":
        print("\nCanceled")
        return True
    else:
        return False
        
def check_for_errors(user_input, operation):
    """
    Checks if the input the user enters is allowed by that operation
    """
    # Checks if the user entered a numbered task or a string that would not be supported
    try:
        int(user_input)
    except ValueError:
        # Checks if the user wants to cancel the operation they chose or simply entered an incorrect input
        if cancel_operation(user_input.lower()):
            return True
        else:
            print(f"\nPlease enter a valid numbered task to {operation}.")
            return True
    else:
        return False


class TaskManager:
    def __init__(self):
        self.completed_tasks = 0
        self.task_list = {}
        self.stack = []
        self.total_tasks = len(self.task_list)
        self.current_action = -1
        
    def print_background_tasks(self):
        """
        Prints background tasks, used for development purposes
        """
        print(f"\nStack: {self.stack}")
        print(f"Stack Len: {len(self.stack)}")
        print(f"Stack Current Action Index: {self.current_action}")
        print(f"Task List: {self.task_list}")
        
    def check_value(self, user_input, operation):
        """
        Checks the value of the input by the user, typically what task number they wish to delete, mark as completed, ect.
        """
        # Checks if the user input is greater than the len of the task list
        if len(self.task_list) < user_input:
            print(f"\nYou have entered an invalid task number to {operation}, please input a valid task.")
            return False
        else:
            return True
            
    def modify_current_task(self, operation):
        """
        Modifies the task managers current task, which is the index of the stack
        """
        if operation == "add" or operation == "delete" or operation == "complete":
            self.current_action += 1
        elif operation == "undo":
            self.current_action -= 1
            return
        elif operation == "redo":
            self.current_action += 1
            return
        else:
            #Error code used for development
            print("error, function was called with incorrect inputs. Fix (Line 55)")
            
# If the operation the user is performing is after an action has been undone, the task the user undid from will be deleted
# Undo and Redo functions skip this step
        if self.current_action < len(self.stack) - 1:
            self.stack.pop(self.current_action)
            
    def get_user_input(self):
        """
        Gets the input of what operation the user wishes to perform
        """
        if self.total_tasks == self.completed_tasks and self.total_tasks > 0 and self.completed_tasks > 0:
            print("\ncongratulations, you have completed all your tasks!")
            choice = input("\n-----------------------\nInput:").lower()
        else:
            if self.total_tasks == 1 and self.completed_tasks == 1:
                plural = "task", "is"
            elif self.total_tasks == 1 and self.completed_tasks == 0:
                plural = "task", "are"
            elif self.total_tasks > 1 and self.completed_tasks == 1:
                plural = "tasks", "is"
            else: plural = "tasks", "are"
            choice = input(f"\nYou have {self.total_tasks} {plural[0]}, {self.completed_tasks} {plural[1]} completed.\n-----------------------\nInput:").lower()
        return choice
        
    def add_task(self):
        """
        Adds a task that the user wishes to complete
        """
        # Asks the user for a description of the task they want to add
        text = input("\nInput a description of the task: \n")
        # Updates the total task list
        self.total_tasks += 1
        # Creates the task object with a description of the task(text), and the task number(total tasks)
        task = Task.Task(text=text, task_number=self.total_tasks)
        # Appends the task object into task list of the task manager
        self.task_list[f"{self.total_tasks}"] = {"task": task}
        # Adds the action of adding a task to the stack
        self.stack.append(["added_task", self.total_tasks, {"task": task}])
        # Updates the current task in the stack
        self.modify_current_task(operation= "add")
        
    def delete_task(self):
        """
        Deletes task from task list
        """
        user_input = input("\nWhat task would you like to delete?\nTask#:")
        if check_for_errors(user_input= user_input, operation= "delete"):
            return
        else:
            #Checks if user input is a valid list number that can be deleted
            valid_input = self.check_value(user_input= int(user_input), operation= "delete")
            # If the user has entered a valid input, the task the user is deleting is checked to see if marked  as complete
            if valid_input:
                deleted_task = self.task_list[f'{user_input}']
                if deleted_task["task"].status == "Complete":
                    # If the task desired to be deleted is marked as complete, the total amount of completed tasks is lowered
                    self.completed_tasks -= 1
                # The action of deleting a task, what task # was deleted as well as the task object is added to the stack
                self.stack.append(["deleted_task", user_input , deleted_task])
                #The desired task is deleted from the task list, lowering the total tasks value
                del self.task_list[f'{user_input}']
                self.total_tasks = len(self.task_list)
                self.modify_task_list(index= None, operation= "")
                self.print_tasks()
                # self.update_task_number(operation= "delete", index= user_input)
            else:
                self.delete_task()
            # Updates the current task in the stack
            self.modify_current_task(operation= "delete")
            
    def mark_task_complete(self):
        """
        Marks a task complete. User inputs what task they wish to mark completed
        """

        def check_if_already_complete(u_input):
            if self.task_list[f"{u_input}"]["task"].status == "Complete":
                print(f"\nYou have already marked task #{u_input} complete, Good job!")
                return False
            else:
                return True

        task_number = False

        user_input = input("\nWhat task would you like to mark as complete?\nTask#:")
        if check_for_errors(user_input= user_input, operation= "mark as complete"):
            return
        else:
            user_input = int(user_input)
            valid_input = self.check_value(user_input= user_input, operation= "mark as complete")
            if valid_input:
                 task_number = check_if_already_complete(user_input)
            if valid_input and task_number:
                completed_task = self.task_list[f'{user_input}']
                # If the user enters a valid input, and the task they are marking complete is not already marked as complete, the inputted task will be marked as complete
                self.task_list[f"{user_input}"]["task"].status = "Complete"
                # The action of marking a task as complete and what task # was affected is added to the stack
                self.stack.append(["completed_task", user_input, completed_task])
                #The list of current tasks is printed out, showing updated changes
                self.print_tasks()
                self.completed_tasks += 1
            elif not task_number:
                return
            else:
                # If user input is invalid, they are directed to re-input a valid task to mark as completed
                self.mark_task_complete()
            self.modify_current_task("complete")
            
    def print_tasks(self):
        """
        Prints tasks from the task list for the user to view
        """
        if self.total_tasks > 0:
            for i in self.task_list:
                self.task_list[f"{i}"]["task"].provide_template()
        else:
            force_add_tasks("view")
            
    def undo(self):
        """
        Allows the user to undo an action they've performed
        """
        if self.current_action == -1:
            print("\nNo actions to undo")
        else:
            # Checks if tasks exist/ actions to undo
            if len(self.stack) > 0:
                # Checks what the action of the current action: added a task or deleted a task
                if \
                self.stack[self.current_action][0] == "deleted_task" or self.stack[self.current_action][0] == "added_task":
                    # "index" variable is set to the index of the current action that took place. Ex: Deleted task "2"
                    index = self.stack[self.current_action][1]
                    self.modify_task_list(index= int(self.stack[self.current_action][1]), operation= self.stack[self.current_action][0])
                    self.total_tasks = len(self.task_list)
                elif self.stack[self.current_action][0] == "completed_task":
                    self.task_list[f"{self.stack[self.current_action][1]}"]["task"].status = "Incomplete"
                    self.completed_tasks -= 1
                else:
                    print("Error, no action found")

                self.modify_current_task("undo")
                self.update_total_task_values()
                self.print_tasks()

            else:
                print("\nYou have no actions to undo")
                
    def redo(self):
        """
        Allows the user to redo an action they undid
        """
        if self.current_action == len(self.stack) - 1:
            print("\nNo actions to redo")
            return
        else:

            next_task_operation = self.stack[self.current_action + 1][0]
            next_task_modified_operation = ""

            if next_task_operation == "added_task":
                next_task_modified_operation = "deleted_task"
            elif next_task_operation == "deleted_task":
                next_task_modified_operation = "added_task"
            elif self.stack[self.current_action + 1][0] == "completed_task":
                self.stack[self.current_action + 1][2]["task"].status = "Complete"

            self.modify_current_task(operation="redo")
            self.modify_task_list(index= int(self.stack[self.current_action][1]), operation= next_task_modified_operation)
            self.update_total_task_values()
            self.print_tasks()
            
    def modify_task_list(self, index, operation):
        """
        Modifies the task list when deleting tasks, and adding tasks. Corrects list order when needed
        """
        # Temporary variables used to recreate and modify the manager's task list
        temp_task_list = []
        new_task_list = {}
        
        def create_temp_task_list():
            """
            Creates the temporary task list of existing tasks in the official task list
            """
            for existing_task in self.task_list:
                temp_task_list.append(self.task_list[f"{existing_task}"])
                
        def create_finalized_task_list():
            """
            Creates the finalized task list that will become the official task list
            """
            temp_task_list_index = 0
            while temp_task_list_index < len(temp_task_list):
                new_task_list[f"{temp_task_list_index + 1}"] = temp_task_list[temp_task_list_index]
                temp_task_list_index += 1
                
        def re_number_task_list():
            """
            Renumbers the task list in ascending order after an operation has been performed
            """
            for key in new_task_list:
                new_task_list[f"{key}"]["task"].task_number = key

        # Calls the function to create a temporary task list no matter the operation being performed
        create_temp_task_list()

        # Checks the operation being performed
        if operation == "deleted_task":
            # Adds the deleted task back into the task manager's task list at its original index
            temp_task_list.insert(index - 1, self.stack[self.current_action][2])
            # Calls the function to create the finalized task list with the deleted task inserted
            create_finalized_task_list()
            # Renumbers the finalized task list
            re_number_task_list()
        elif operation == "added_task":
            # Deletes an added task from the task manager's task list
            temp_task_list.pop(index - 1)
            # Calls the function to create the finalized task list with the added task deleted
            create_finalized_task_list()
            # Renumbers the finalized task list
            re_number_task_list()

        # If the operation being performed is not adding or deleting a task, the task list is simply finalized
        else:
            create_finalized_task_list()
            re_number_task_list()

        self.task_list = new_task_list
        self.total_tasks = len(self.task_list)

    def update_total_task_values(self):
        """
        Updates the total task value and checks how many tasks are marked as complete after performing an operation
        """
        completed_tasks = 0
        total_tasks = len(self.task_list)
        for key in self.task_list:
            if self.task_list[f"{key}"]["task"].status == "Complete":
                completed_tasks += 1
        self.completed_tasks = completed_tasks
        self.total_tasks = total_tasks
