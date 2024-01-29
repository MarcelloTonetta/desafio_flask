from flask import Flask, render_template, url_for, request, redirect
import random
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('todos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
@app.route("/tasks", methods=["GET", "POST"])
def home():
    if(request.method == 'POST'):
        todo_name = request.form["todo_name"]
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (name, checked) VALUES (?, ?)',
                         (todo_name, 0))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template("index.html", items=todos)

@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    checked = is_checked(request.form.get('checked'))
    conn = get_db_connection()
    _ = conn.execute('UPDATE tasks SET checked = ? WHERE id = ?', (checked, todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>", methods = ["POST"])
def delete_todo(todo_id):
    conn = get_db_connection()
    _ = conn.execute('DELETE FROM tasks WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

def is_checked(value):
    if value == 'on':
        return 1
    return 0

if __name__ == "__main__":
    app.run(debug=True)