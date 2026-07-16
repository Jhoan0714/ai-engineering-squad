"""Minimal in-memory Todo API (demo-only stack: Python / Flask)."""

from __future__ import annotations

from flask import Flask, jsonify, request

app = Flask(__name__)

_todos: list[dict] = []
_next_id = 1


def reset_store() -> None:
    """Test helper: clear in-memory state."""
    global _todos, _next_id
    _todos = []
    _next_id = 1


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/todos")
def list_todos():
    return jsonify({"todos": list(_todos)})


@app.post("/todos")
def create_todo():
    global _next_id
    body = request.get_json(silent=True) or {}
    title = body.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({"error": "title is required"}), 400

    priority = body.get("priority", "medium")
    if priority not in ("low", "medium", "high"):
        return jsonify({"error": "priority must be low, medium, or high"}), 400

    todo = {
        "id": _next_id,
        "title": title.strip(),
        "priority": priority,
        "done": False,
    }
    _next_id += 1
    _todos.append(todo)
    return jsonify(todo), 201


@app.patch("/todos/<int:todo_id>")
def update_todo(todo_id: int):
    body = request.get_json(silent=True) or {}
    for todo in _todos:
        if todo["id"] == todo_id:
            if "done" in body:
                todo["done"] = bool(body["done"])
            if "priority" in body:
                priority = body["priority"]
                if priority not in ("low", "medium", "high"):
                    return jsonify({"error": "priority must be low, medium, or high"}), 400
                todo["priority"] = priority
            return jsonify(todo)
    return jsonify({"error": "not found"}), 404


if __name__ == "__main__":
    app.run(port=5055, debug=True)
