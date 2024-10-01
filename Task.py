class Task:
    def __init__(self, text, task_number):
        self.text = text
        self.task_number = task_number
        self.status = "Incomplete"

    def provide_template(self):
        template = f'''
        -------------------------
        
        Task {self.task_number}:
    
        {self.text}
    
        Status: {self.status}
    
        -------------------------
        '''

        print(template)
