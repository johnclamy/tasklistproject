from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


dummyTasks = [
    {
        'id': 1,
        'name': 'John Doe',
        'title': 'Complete the project',
        'status': False,
        'role': 'admin',
        'email': 'john.doe@example.com',
        'date_created': datetime.now(timezone.utc)
    }
]


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(100), default='admin')
    email = db.Column(db.String(100), nullable=False)    
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Task {self.title}>'


with app.app_context():
    if not os.path.exists('tasks.db'):
        db.create_all()


@app.get('/')
def home():
    # tasks = Task.query.all()
    return render_template('index.html', tasks=dummyTasks)


@app.post('/add')
def add():
    title = request.form.get('title', '').strip()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()

    if not title:
        flash("Please enter title for the task.")
        return redirect(url_for('home'))

    if not name:
        flash("Please enter name for the task.")
        return redirect(url_for('home'))

    if not email:
        flash("Please enter email for the task.")
        return redirect(url_for('home'))
    new_task = Task()
    new_task.title = title
    new_task.name = name
    new_task.email = email
    # new_task.description = description

    db.session.add(new_task)
    db.session.commit()
    flash("Task added successfully.")

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
