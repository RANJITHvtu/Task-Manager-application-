from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
app = Flask(__name__)

# Create a database connection and cursor
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create tasks and categories tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        FOREIGN KEY (category) REFERENCES categories (name)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Fetch tasks
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    # Fetch categories
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()

    conn.close()

    return render_template('index.html', tasks=tasks, categories=categories)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    category = request.form['category']

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Insert task into the 'tasks' table
    cursor.execute('INSERT INTO tasks (title, description, category) VALUES (?, ?, ?)', (title, description, category))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = request.form['name']

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Insert category into the 'categories' table
    cursor.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/delete_category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Category deleted successfully'})

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    try:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()

        title = request.form['title']
        description = request.form['description']

        cursor.execute('UPDATE tasks SET title=?, description=? WHERE id=?', (title, description, task_id))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Task updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

# New route for updating categories
@app.route('/update_category/<int:category_id>', methods=['POST'])
def update_category(category_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    name = request.form['name']

    cursor.execute('UPDATE categories SET name=? WHERE id=?', (name, category_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Category updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
