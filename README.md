# To-Do List Application

A web-based To-Do list application built with FastAPI, featuring RESTful APIs for task management, HTML templates for the user interface, and SQLite for data storage. The app supports CRUD operations (Create, Read, Update, Delete) on tasks, with dark mode support and responsive design.

## Features
- **RESTful APIs:** JSON-based endpoints for task operations.
- **Web Interface:** HTML templates for adding, viewing, updating, and deleting tasks.
- **Database:** SQLite for simple, file-based storage.
- **Testing:** Pytest-based unit tests for API endpoints.
- **Dark Mode:** Toggleable theme in the web UI.
- **Error Handling:** Logging and exception handling for robustness.

## Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)
- A web browser for testing the UI

## Installation

1. **Clone the Repository:** <br>
```https://github.com/Bhuvneshjai/todo-task-manager-api-templates.git```

2. **Create a Virtual Environment (Recommended):** <br>
```python -m venv venv``` <br>
```venv/bin/activate``` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; #for windows

3. **Install Dependencies:** <br>
```pip install -r requirements.txt```

4. **Set Up the Database:**
    - The database (`tasks.db`) is created automatically when the app starts.
    - No manual setup required.

## Usage
### Running the Application
1. **Start the Server:** <br>
```uvicorn app.main:app --reload```

    - The app will run on `http://127.0.0.1:8000` (or `http://localhost:8000`).

2. **Access the Web Interface:** <br>
    - Open your browser and go to `http://127.0.0.1:8000`.
    - Use the UI to add, view, update, or delete tasks.
    - Toggle dark mode using the button in the top-right corner.

3. **API Documentation:** <br>
    - Interactive API docs are available at `http://127.0.0.1:8000/docs` (Swagger UI) or `http://127.0.0.1:8000/redoc` (ReDoc).

### API Endpoints
The app provides the following RESTful JSON APIs:

- **GET /api/tasks**  
Retrieve all tasks.  
Response: `[{"id": 1, "title": "Task Title", "description": "Description", "due_date": "2023-12-31", "status": "pending"}, ...]`

- **POST /api/tasks**  
Create a new task.  
Request Body: `{"title": "Task Title", "description": "Description", "due_date": "2023-12-31", "status": "pending"}`  
Response: The created task object.

- **GET /api/tasks/{task_id}**  
Retrieve a specific task by ID.  
Response: Task object or 404 if not found.

- **PUT /api/tasks/{task_id}**  
Update an existing task.  
Request Body: Same as POST.  
Response: Updated task object or 404 if not found.

- **DELETE /api/tasks/{task_id}**  
Delete a task by ID.  
Response: `{"message": "Task deleted"}` or 404 if not found.

**Notes:**
- Use tools like Postman or curl for API testing.
- Example curl: `curl -X GET http://127.0.0.1:8000/api/tasks`
- Authentication: None (add if needed for production).

## Testing
1. **Run Tests:**
pytest app/tests/test_tasks.py
    - Tests cover API endpoints for create, read, update, and delete operations.
    - Ensure the app is running in the background if tests involve httpx calls (though current tests use TestClient).

2. **Test Coverage:**
    - Unit tests for CRUD functions.
    - API response validation.
    - Database cleanup between tests.

## Deployment
### Local Deployment
- Follow the "Running the Application" steps above.

### Production Deployment
1. **Use a WSGI Server:**
```pip install gunicorn gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000```


2. **Environment Variables:**
    - For production, set `DB_NAME` in `database.py` or use environment variables for configuration (e.g., via `python-dotenv`).
    - Example: Add a `.env` file with `DATABASE_URL=sqlite:///tasks.db`.

3. **Hosting Options:**
    - Deploy on platforms like Heroku, AWS, or DigitalOcean.
    - Ensure Python and dependencies are installed on the server.
    - For HTTPS, use a reverse proxy like Nginx.

4. **Security Considerations:**
    - Add authentication (e.g., OAuth) if exposing APIs publicly.
    - Sanitize inputs (Pydantic helps).
    - Monitor logs for errors.

## Project Structure
todo_app/ <br>
│ <br>
├── app/ <br>
│   &nbsp;&nbsp;&nbsp; ├── main.py <br>
│   &nbsp;&nbsp;&nbsp; ├── database.py <br>
│   &nbsp;&nbsp;&nbsp; ├── models.py <br>
│   &nbsp;&nbsp;&nbsp; ├── crud.py <br>
│   &nbsp;&nbsp;&nbsp; ├── schemas.py <br>
│   &nbsp;&nbsp;&nbsp; ├── templates/ <br>
│   &nbsp;&nbsp;&nbsp; │   &nbsp;&nbsp;&nbsp; ├── base.html <br> 
│   &nbsp;&nbsp;&nbsp; │   &nbsp;&nbsp;&nbsp; ├── list_tasks.html <br>
│   &nbsp;&nbsp;&nbsp; │   &nbsp;&nbsp;&nbsp; └── add_task.html <br>
│   &nbsp;&nbsp;&nbsp; ├── static/ <br>
│   &nbsp;&nbsp;&nbsp; │   &nbsp;&nbsp;&nbsp; └── styles.css <br>
│   &nbsp;&nbsp;&nbsp; └── tests/ <br>
│   &nbsp;&nbsp;&nbsp; │   &nbsp;&nbsp;&nbsp; └── test_tasks.py <br>
├── requirements.txt <br>
├── README.md <br>
└── .env (optional) <br>



## Troubleshooting
- **App Won't Start:** Ensure all dependencies are installed and Python version is compatible.
- **Tasks Not Displaying:** Check browser console for errors; verify templates are updated for dict access.
- **API Errors:** Use `/docs` for testing; ensure correct JSON format.
- **Database Issues:** Delete `tasks.db` and restart to recreate.
- **Port Conflicts:** Change the port in uvicorn command if 8000 is in use.

## Contributing
- Fork the repo, make changes, and submit a pull request.
- Follow PEP 8 for code style.
- Add tests for new features.