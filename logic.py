from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
STORAGE_URL = "http://localhost:5001"

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    task = {
        "title": data.get("title"),
        "description": data.get("description", ""),
        "done": False
    }
    response = requests.post(f"{STORAGE_URL}/tasks", json=task)
    return jsonify(response.json()), response.status_code

@app.route("/tasks/<int:task_id>/done", methods=["PUT"])
def mark_done(task_id):
    response = requests.get(f"{STORAGE_URL}/tasks")
    tasks = response.json()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            requests.post(f"{STORAGE_URL}/tasks", json=task)
            return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(port=5002)
