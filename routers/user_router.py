from flask import Blueprint, request, jsonify
from manager.task_manager import TaskManager
from utils.exceptions import UserAlreadyExistsError, EntityNotFoundError
from utils.validators import validate_email

user_bp = Blueprint("users", __name__)
tm = TaskManager()

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        
        validate_email(data["email"])
        user = tm.create_user(data["user_id"], data["name"], data["email"])
        return jsonify({"message": "User created successfully", "user": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }}), 201
    except UserAlreadyExistsError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@user_bp.route("/", methods=["GET"])
def list_users():
    try:
        users = tm.get_all_users() if hasattr(tm, 'get_all_users') else []
        return jsonify({"users": [{"user_id": user.user_id, "name": user.name, "email": user.email} 
                                  for user in users]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = tm.get_user(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        
        tasks = tm.list_tasks_by_user(user_id)
        
        return jsonify({
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "tasks": [task.to_dict() for task in tasks]
            }
        }), 200
    except EntityNotFoundError:
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
