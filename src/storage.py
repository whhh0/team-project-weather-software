from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
STORAGE_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/tasks", methods=["POST"])
def create_task():
    task = request.json
    tasks = load_tasks()
    task["id"] = len(tasks) + 1
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t.get("id") != task_id]
    save_tasks(tasks)
    return jsonify({"status": "deleted"}), 200

if __name__ == "__main__":
    app.run(port=5001)

