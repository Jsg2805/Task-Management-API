from flask import Blueprint, request
from manager.task_manager import TaskManager
from utils.exceptions import EntityNotFoundError

task_bp = Blueprint('task_routes', __name__)
tm = TaskManager()

# --- CREATE ---
@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    try:
        task = tm.create_task(
            data["task_id"],
            data["title"],
            data["description"],
            data["due_date"],
            data.get("priority", "MEDIUM"),
            data.get("user_id")
        )
        if data.get("user_id"):
            try:
                tm.assign_task_to_user(data["task_id"], data["user_id"])
            except Exception as e:
                return {"message": f"Task created but assignment failed: {str(e)}"}, 201
        return {"message": "Task created successfully", "task": task.to_dict()}, 201
    except Exception as e:
        return {"error": str(e)}, 400

# --- READ ALL ---
@task_bp.route('/', methods=['GET'])
def list_tasks():
    status = request.args.get('status')
    user_id = request.args.get('user_id')
    try:
        if status:
            tasks = tm.list_tasks_by_status(status)
        elif user_id:
            tasks = tm.list_tasks_by_user(user_id)
        else:
            tasks = tm.list_all_tasks()
        return {"tasks": [t.to_dict() for t in tasks]}, 200
    except Exception as e:
        return {"error": str(e)}, 400


@task_bp.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = tm.get_task(task_id)
        if not task:
            return {"error": "Task not found"}, 404
        return {"task": task.to_dict()}, 200
    except Exception as e:
        return {"error": str(e)}, 400


@task_bp.route('/<task_id>/status', methods=['PUT'])
def update_status(task_id):
    data = request.get_json()
    try:
        tm.update_task_status(task_id, data["status"])
        return {"message": "Status updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 400


@task_bp.route('/<task_id>/priority', methods=['PUT'])
def update_priority(task_id):
    data = request.get_json()
    try:
        tm.update_task_priority(task_id, data["priority"])
        return {"message": "Priority updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 400


@task_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    try:
        if "task_id" in data:
            del data["task_id"]  
        tm.update_task(task_id, **data)
        return {"message": "Task updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 400


@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        tm.delete_task(task_id)
        return {"message": "Task deleted successfully"}, 200
    except EntityNotFoundError as e:
        return {"error": str(e)}, 404
    except Exception as e:
        return {"error": str(e)}, 400
