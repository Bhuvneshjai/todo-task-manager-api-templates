from app.database import get_connection

def create_task(task):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, status)
        VALUES (?, ?, ?, ?)
    ''', (task.title, task.description, task.due_date, task.status))
    conn.commit()
    conn.close()

def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def update_task(task_id, task):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title=?, description=?, due_date=?, status=? WHERE id=?",
        (task.title, task.description, task.due_date, task.status, task_id)
    )
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()