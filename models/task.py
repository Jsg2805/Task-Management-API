from datetime import datetime

class Task:
    VALID_STATUSES = ["TO DO", "IN PROGRESS", "DONE"]
    VALID_PRIORITIES = ["LOW", "MEDIUM", "HIGH"]

    def __init__(self, task_id, title, description, due_date, priority="MEDIUM", status="TO DO", assigned_to=None, user_id=None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.user_id = user_id

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format.")
        
        self.due_date = due_date
        self.priority = priority if priority in self.VALID_PRIORITIES else "MEDIUM"
        self.status = status if status in self.VALID_STATUSES else "TO DO"
        self.assigned_to = assigned_to

    def update_status(self, new_status):
        if new_status in self.VALID_STATUSES:
            self.status = new_status
        else:
            raise ValueError("Invalid status")

    def update_priority(self, new_priority):
        if new_priority in self.VALID_PRIORITIES:
            self.priority = new_priority
        else:
            raise ValueError("Invalid priority")

    def assign_to(self, user):
        self.assigned_to = user

    def display_info(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to.name if self.assigned_to else None,
            "user_id": self.user_id,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date
        }

    def to_dict(self):
        """Convert task object to dictionary for API responses"""
        return self.display_info()
