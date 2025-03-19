import logging
from flask import Flask, jsonify, request
from utils.db import tasks
from utils.helpers import generate_id

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)

@app.before_request
def log_request_info():
    """
    Log each incoming request with its method and URL.
    """
    logging.info("Received %s request to %s", request.method, request.url)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    try:
        return jsonify({"status": "OK"}), 200
    except Exception as e:
        logging.error(f"Error in health check: {e}")
        return jsonify({"error": "Health check failed"}), 500

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

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Retrieve a single task by its ID.
    """
    try:
        for task in tasks:
            if task['id'] == task_id:
                return jsonify(task)
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving task {task_id}: {e}")
        return jsonify({"error": "An error occurred while retrieving the task"}), 500

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

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def patch_task(task_id):
    """
    Partially update a task. Allows updating the title and/or completed status.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided for update"}), 400

        for task in tasks:
            if task['id'] == task_id:
                if 'title' in data:
                    task['title'] = data['title']
                if 'completed' in data:
                    task['completed'] = data['completed']
                return jsonify(task)
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        logging.error(f"Error patching task {task_id}: {e}")
        return jsonify({"error": "An error occurred while updating the task"}), 500



@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task by its ID.
    """
    try:
        # Find the task by its ID
        for index, task in enumerate(tasks):
            if task['id'] == task_id:
                # Remove the task from the list
                deleted_task = tasks.pop(index)
                return jsonify({"message": "Task deleted", "task": deleted_task}), 200
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        logging.error(f"Error deleting task {task_id}: {e}")
        return jsonify({"error": "An error occurred while deleting the task"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800, debug=True)
