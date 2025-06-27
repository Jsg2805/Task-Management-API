class User:
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.task_list = []

    def add_task(self, task):
        self.task_list.append(task)

    def remove_task(self, task_id):
        self.task_list = [task for task in self.task_list if task.task_id != task_id]

    def view_tasks_by_status(self, status):
        return [task for task in self.task_list if task.status == status]
