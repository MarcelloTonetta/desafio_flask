import sqlite3

connection = sqlite3.connect('todos.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO tasks (name, checked) VALUES (?, ?)",
            ('Ler um livro', 0,))
cur.execute("INSERT INTO tasks (name, checked) VALUES (?, ?)",
            ('Comprar pão', 0,))

connection.commit()
connection.close()
