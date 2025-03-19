import logging
from flask import Flask, jsonify, request
from utils.db import tasks
from utils.helpers import generate_id

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retrieve all tasks.
    """
    try:
        return jsonify({"tasks": tasks})
    except Exception as e:
        logging.error(f"Error fetching tasks: {e}")
        return jsonify({"error": "An error occurred while fetching tasks"}), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task.
    """
    try:
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
    except Exception as e:
        logging.error(f"Error creating task: {e}")
        return jsonify({"error": "An error occurred while creating the task"}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Toggle the 'completed' status of a task.
    """
    try:
        for task in tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                return jsonify(task)
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        logging.error(f"Error updating task {task_id}: {e}")
        return jsonify({"error": "An error occurred while updating the task"}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task by its ID.
    """
    try:
        for idx, task in enumerate(tasks):
            if task['id'] == task_id:
                removed_task = tasks.pop(idx)
                return jsonify({"message": "Task deleted", "task": removed_task})
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        logging.error(f"Error deleting task {task_id}: {e}")
        return jsonify({"error": "An error occurred while deleting the task"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800, debug=True)
