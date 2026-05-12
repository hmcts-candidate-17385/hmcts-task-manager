from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app.extensions import db
from app.models import Task
from app.schemas import TaskCreateSchema, TaskStatusUpdateSchema

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


def _json_body():
    if not request.is_json:
        return None, (jsonify({"message": "Content-Type must be application/json"}), 415)
    data = request.get_json(silent=True)
    if data is None:
        return None, (jsonify({"message": "Invalid JSON body"}), 400)
    if not isinstance(data, dict):
        return None, (jsonify({"message": "JSON body must be an object"}), 400)
    return data, None


class TaskCollection(MethodView):
    def get(self):
        tasks = Task.query.order_by(Task.id).all()
        return jsonify([t.to_dict() for t in tasks]), 200

    def post(self):
        data, err = _json_body()
        if err:
            return err
        payload = TaskCreateSchema().load(data)
        task = Task(
            title=payload["title"],
            description=payload.get("description"),
            status=payload["status"],
            due_date=payload["due_date"],
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201


class TaskDetail(MethodView):
    def get(self, task_id: int):
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"message": "Task not found"}), 404
        return jsonify(task.to_dict()), 200

    def patch(self, task_id: int):
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"message": "Task not found"}), 404
        data, err = _json_body()
        if err:
            return err
        payload = TaskStatusUpdateSchema().load(data)
        task.status = payload["status"]
        db.session.commit()
        return jsonify(task.to_dict()), 200

    def delete(self, task_id: int):
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"message": "Task not found"}), 404
        db.session.delete(task)
        db.session.commit()
        return "", 204


tasks_bp.add_url_rule(
    "",
    view_func=TaskCollection.as_view("task_collection"),
    methods=["GET", "POST"],
    strict_slashes=False,
)
tasks_bp.add_url_rule(
    "/<int:task_id>",
    view_func=TaskDetail.as_view("task_detail"),
    methods=["GET", "PATCH", "DELETE"],
    strict_slashes=False,
)
