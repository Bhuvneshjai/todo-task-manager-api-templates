from app.database import get_connection
import logging
from fastapi import HTTPException

def create_task(task):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, due_date, status)
            VALUES (?, ?, ?, ?)
        ''', (task.title, task.description, task.due_date, task.status))
        task_id = cursor.lastrowid  # Get the inserted ID
        conn.commit()
        conn.close()
        return task_id
    except Exception as e:
        logging.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Database error")

def get_tasks():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        logging.error(f"Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail="Database error")

def get_task_by_id(task_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        conn.close()
        return task
    except Exception as e:
        logging.error(f"Error fetching task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error")

def update_task(task_id, task):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title=?, description=?, due_date=?, status=? WHERE id=?",
            (task.title, task.description, task.due_date, task.status, task_id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error updating task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error")

def delete_task(task_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error deleting task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error")