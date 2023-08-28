from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)

# Create the database tables
with app.app_context():
    db.create_all()


# Route to fetch all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Todo.query.all()
    tasks_json = [{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks]
    return jsonify({'tasks': tasks_json})


# Route to create Tasks
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Todo(title=data['title'], description=data.get('description', ''), completed=False)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully', 'task': {'id': new_task.id, 'title': new_task.title, 'description': new_task.description, 'completed': new_task.completed}}), 201


# Route to fetch a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Todo.query.get(task_id)
    if task:
        return jsonify({'task': {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}})
    return jsonify({'message': 'Task not found'}), 404


# Route to update a specific task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Todo.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully', 'task': {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}})


# Route to delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Todo.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task Deleted Successfully!'})
    return jsonify({'message': 'Task not found'}), 404
    

if __name__=="__main__":
    app.run(debug=True)