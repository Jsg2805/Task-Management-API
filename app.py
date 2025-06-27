from flask import Flask, render_template
from flask_cors import CORS
from routers.task_router import task_bp
from routers.user_router import user_bp
from utils.db import db_creation

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(task_bp, url_prefix='/tasks')
    app.register_blueprint(user_bp, url_prefix='/users')

    @app.route("/")
    def show_form():
        return render_template("taskform.html")

    return app

if __name__ == "__main__":
    db_creation()
    app = create_app()
    app.run(debug=True)
