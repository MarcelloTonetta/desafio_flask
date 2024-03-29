from flask import Flask, render_template, url_for, request, redirect
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
        conn.execute('INSERT INTO tasks (name, radio) VALUES (?, ?)',
                         (todo_name, 0))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template("index.html", items=todos)

@app.route("/radio/<int:todo_id>", methods=["POST"])
def radio_todo(todo_id):
    radio = is_radio(int(request.form.get('rad'))) 
    conn = get_db_connection()
    _ = conn.execute('UPDATE tasks SET radio = ? WHERE id = ?', (radio, todo_id))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))


@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit_todo(todo_id):
    conn = get_db_connection()
    todo = conn.execute('SELECT * FROM tasks WHERE id = ?', (todo_id,)).fetchone()
    
    if request.method == 'POST':
        new_name = request.form['new_name']
        conn.execute('UPDATE tasks SET name = ? WHERE id = ?', (new_name, todo_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    conn.close()
    return render_template("edit.html", todo=todo)

@app.route("/delete/<int:todo_id>", methods = ["POST"])
def delete_todo(todo_id):
    conn = get_db_connection()
    _ = conn.execute('DELETE FROM tasks WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

def is_radio(value):
    return value if value in (1, 2, 3) else 0

if __name__ == "__main__":
    app.run(debug=True)
