from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Priority
from repo import TaskRepository
from services import TaskService
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = "dev-secret"  # replace for prod
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "planception.sqlite")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    repo = TaskRepository()
    svc  = TaskService(repo)

    @app.route("/", methods=["GET"])
    def index():
        tasks = svc.list_tasks()
        overdue = svc.list_overdue()
        today = svc.list_today()
        return render_template("index.html", tasks=tasks, overdue=overdue, today=today, Priority=Priority)

    @app.route("/add", methods=["POST"])
    def add():
        name     = request.form.get("name", "")
        due_date = request.form.get("due_date", "")
        priority = request.form.get("priority", "med")
        category = request.form.get("category", "")
        ok = svc.create_task(name, due_date, priority, category)
        flash("Task created" if ok else "Invalid task; please check inputs.")
        return redirect(url_for("index"))

    @app.route("/delete/<name>", methods=["POST"])
    def delete(name):
        ok = svc.remove_task(name)
        flash("Task removed" if ok else "Task not found")
        return redirect(url_for("index"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
