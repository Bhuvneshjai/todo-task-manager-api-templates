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

def get_task():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()
    return rows