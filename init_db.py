import sqlite3

connection = sqlite3.connect('todos.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO tasks (name, radio) VALUES (?, ?)",
            ('Ler um livro', 1,))
cur.execute("INSERT INTO tasks (name, radio) VALUES (?, ?)",
            ('Comprar pão', 1,))

connection.commit()
connection.close()
