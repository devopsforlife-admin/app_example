from flask import Flask, jsonify, request
from utils.db import tasks
from utils.helpers import generate_id

app = Flask(__name__)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    task = {
        "id": generate_id(),
        "title": data['title'],
        "completed": False
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


# DELETE

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800, debug=True)    
