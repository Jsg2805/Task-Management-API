from models.task import Task
from models.user import User
from utils.exceptions import UserAlreadyExistsError, TaskAlreadyExistsError, EntityNotFoundError
from utils.db import get_connection
from datetime import datetime

class TaskManager:
    def __init__(self):
        pass

    def create_user(self, user_id, name, email):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise UserAlreadyExistsError("User already exists.")

        cursor.execute(
            "INSERT INTO users (user_id, uname, uemail) VALUES (%s, %s, %s)",
            (user_id, name, email)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return User(user_id, name, email)

    def create_task(self, task_id, title, description, due_date, priority="MEDIUM", user_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise TaskAlreadyExistsError("Task already exists.")

        valid_priorities = [p.upper() for p in Task.VALID_PRIORITIES]
        priority = priority.upper()
        if priority not in valid_priorities:
            priority = "MEDIUM"

        cursor.execute(
            """INSERT INTO tasks (task_id, title, description, due_date, priority, status, user_id) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (task_id, title, description, due_date, priority, "TO DO", user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return Task(task_id, title, description, due_date, priority)

    def assign_task_to_user(self, task_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise EntityNotFoundError("Task not found.")

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise EntityNotFoundError("User not found.")

        cursor.execute(
            "UPDATE tasks SET user_id = %s WHERE task_id = %s",
            (user_id, task_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def list_all_tasks(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT t.task_id, t.title, t.description, t.due_date, t.priority, t.status, 
                   t.user_id, u.uname
            FROM tasks t
            LEFT JOIN users u ON t.user_id = u.user_id
        """)
        tasks = []
        for row in cursor.fetchall():
            task_id, title, description, due_date, priority, status, user_id, user_name = row
            task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
            tasks.append(task)

        cursor.close()
        conn.close()
        return tasks

    def list_tasks_by_user(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise EntityNotFoundError("User not found.")

        cursor.execute("""
            SELECT task_id, title, description, due_date, priority, status, user_id
            FROM tasks WHERE user_id = %s
        """, (user_id,))
        tasks = []
        for row in cursor.fetchall():
            task_id, title, description, due_date, priority, status, user_id = row
            task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
            tasks.append(task)

        cursor.close()
        conn.close()
        return tasks

    def list_tasks_by_status(self, status):
        conn = get_connection()
        cursor = conn.cursor()

        valid_statuses = [s.upper() for s in Task.VALID_STATUSES]
        status = status.upper()
        if status not in valid_statuses:
            cursor.close()
            conn.close()
            return []

        cursor.execute("""
            SELECT t.task_id, t.title, t.description, t.due_date, t.priority, t.status, 
                   t.user_id, u.uname
            FROM tasks t
            LEFT JOIN users u ON t.user_id = u.user_id
            WHERE t.status = %s
        """, (status,))
        tasks = []
        for row in cursor.fetchall():
            task_id, title, description, due_date, priority, status, user_id, user_name = row
            task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
            tasks.append(task)

        cursor.close()
        conn.close()
        return tasks

    def update_task(self, task_id, **kwargs):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise EntityNotFoundError("Task not found.")

        allowed_fields = {'title', 'description', 'due_date', 'priority', 'status', 'user_id'}
        set_clauses = []
        params = []

        for key, value in kwargs.items():
            if key in allowed_fields:
                if key == 'priority' and isinstance(value, str):
                    value = value.upper()
                    if value not in [p.upper() for p in Task.VALID_PRIORITIES]:
                        continue
                elif key == 'status' and isinstance(value, str):
                    value = value.upper()
                    if value not in [s.upper() for s in Task.VALID_STATUSES]:
                        continue
                set_clauses.append(f"{key} = %s")
                params.append(value)

        if set_clauses:
            sql = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE task_id = %s"
            params.append(task_id)
            cursor.execute(sql, params)
            conn.commit()

        cursor.close()
        conn.close()

    def delete_task(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise EntityNotFoundError("Task not found.")

        cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def get_task(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT t.task_id, t.title, t.description, t.due_date, t.priority, t.status, 
                   t.user_id, u.uname
            FROM tasks t
            LEFT JOIN users u ON t.user_id = u.user_id
            WHERE t.task_id = %s
        """, (task_id,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return None

        task_id, title, description, due_date, priority, status, user_id, user_name = row
        task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
        cursor.close()
        conn.close()
        return task

    def delete_user(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise EntityNotFoundError("User not found.")

        cursor.execute("UPDATE tasks SET user_id = NULL WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def get_user(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, uname, uemail FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return None

        user_id, name, email = row
        user = User(user_id, name, email)

        cursor.execute("SELECT task_id, title, description, due_date, priority, status FROM tasks WHERE user_id = %s", (user_id,))
        for task_row in cursor.fetchall():
            task_id, title, description, due_date, priority, status = task_row
            task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
            user.add_task(task)

        cursor.close()
        conn.close()
        return user

    def get_all_users(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, uname, uemail FROM users")
        users = []
        for row in cursor.fetchall():
            user_id, name, email = row
            user = User(user_id, name, email)
            users.append(user)

        cursor.close()
        conn.close()
        return users

    def update_task_status(self, task_id, new_status):
        new_status = new_status.upper()
        if new_status not in Task.VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(Task.VALID_STATUSES)}")
        return self.update_task(task_id, status=new_status)

    def update_task_priority(self, task_id, new_priority):
        new_priority = new_priority.upper()
        if new_priority not in Task.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority. Must be one of: {', '.join(Task.VALID_PRIORITIES)}")
        return self.update_task(task_id, priority=new_priority)
