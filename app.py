import logging
from flask import Flask, jsonify, request
from utils.db import tasks
from utils.helpers import generate_id

# Minimal logging setup (not ideal for production)
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Very basic request logging (no structured info)
@app.before_request
def before():
    logging.debug("Got a " + request.method + " request at " + request.url)

# Health check without error handling
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

# Retrieve all tasks without try/except or docstrings
@app.route('/tasks', methods=['GET'])
def tasks_get():
    return jsonify({"tasks": tasks})

# Retrieve a single task by id (barebones)
@app.route('/tasks/<int:tid>', methods=['GET'])
def task_get(tid):
    for t in tasks:
        if t['id'] == tid:
            return jsonify(t)
    return jsonify({"error": "not found"}), 404

# Create task without proper validation and error handling
@app.route('/tasks', methods=['POST'])
def task_create():
    data = request.json
    # No check if data is None or 'title' exists
    t = {"id": generate_id(), "title": data["title"], "completed": False}
    tasks.append(t)
    return jsonify(t), 201

# Toggle completed status (no logging of failures)
@app.route('/tasks/<int:tid>', methods=['PUT'])
def task_update(tid):
    for t in tasks:
        if t['id'] == tid:
            t['completed'] = not t['completed']
            return jsonify(t)
    return jsonify({"error": "not found"}), 404

# Partial update (PATCH) with minimal checks
@app.route('/tasks/<int:tid>', methods=['PATCH'])
def task_patch(tid):
    data = request.json
    for t in tasks:
        if t['id'] == tid:
            if "title" in data:
                t["title"] = data["title"]
            if "completed" in data:
                t["completed"] = data["completed"]
            return jsonify(t)
    return jsonify({"error": "not found"}), 404

# DELETE endpoint with basic logic and no error handling
@app.route('/tasks/<int:tid>', methods=['DELETE'])
def task_delete(tid):
    for i in range(len(tasks)):
        if tasks[i]['id'] == tid:
            del tasks[i]
            return jsonify({"msg": "deleted"})
    return jsonify({"error": "not found"}), 404

if __name__ == '__main__':
    # Running with debug True and minimal configuration
    app.run(host='0.0.0.0', port=5800, debug=True)
