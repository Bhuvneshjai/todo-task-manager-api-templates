import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import create_tables, get_connection
import sqlite3

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    create_tables()

@pytest.fixture(scope="function", autouse=True)
def clear_database():
    # Clear tasks table after each test
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()

def test_create_task():
    response = client.post("/api/tasks", json={"title": "Test Task", "description": "Desc", "due_date": "2023-12-31", "status": "pending"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data

def test_get_tasks():
    # Create a task first
    client.post("/api/tasks", json={"title": "Test Task", "description": "Desc", "due_date": "2023-12-31", "status": "pending"})
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 1

def test_update_task():
    # Create a task and get its ID
    create_response = client.post("/api/tasks", json={"title": "Test Task", "description": "Desc", "due_date": "2023-12-31", "status": "pending"})
    task_id = create_response.json()["id"]
    # Update it
    response = client.put(f"/api/tasks/{task_id}", json={"title": "Updated", "description": "Desc", "due_date": "2023-12-31", "status": "completed"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

def test_delete_task():
    # Create a task and get its ID
    create_response = client.post("/api/tasks", json={"title": "Test Task", "description": "Desc", "due_date": "2023-12-31", "status": "pending"})
    task_id = create_response.json()["id"]
    # Delete it
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    # Verify it's gone
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404