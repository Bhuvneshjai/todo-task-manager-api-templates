from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import create_tables
from app.schemas import TaskCreate, Task
from app import crud
import logging
import httpx
from datetime import date

# ---- 1. Create FastAPI app ----
app = FastAPI(title="To-do List API")

# ---- 2. Mount static files ----
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ---- 3. Templates ----
templates = Jinja2Templates(directory="app/templates")

logging.basicConfig(level=logging.INFO)

# ---- 4. Startup event ----
@app.on_event("startup")
def startup():
    create_tables()
    logging.info("Database tables created or verified.")

# ---- 5. Routes ----
# Web Routes (HTML-based, calling APIs internally)
@app.get("/", response_class=HTMLResponse)
async def list_tasks(request: Request):
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/api/tasks")
        response.raise_for_status()  # Raise error if not 200
        tasks = response.json()
    return templates.TemplateResponse("list_tasks.html", {"request": request, "tasks": tasks})

@app.get("/add", response_class=HTMLResponse)
def add_task_form(request: Request):
    today = date.today().isoformat()
    return templates.TemplateResponse("add_task.html", {"request": request, "action": "Add", "today": today})

@app.post("/add")
async def add_task(title: str = Form(...), description: str = Form(None), due_date: str = Form(None), status: str = Form("pending")):
    task_data = {"title": title, "description": description, "due_date": due_date, "status": status}
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/api/tasks", json=task_data)
        response.raise_for_status()
    logging.info(f"Task added via web: {title}")
    return RedirectResponse(url="/", status_code=302)

@app.get("/update/{task_id}", response_class=HTMLResponse)
async def update_task_form(request: Request, task_id: int):
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get(f"/api/tasks/{task_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Task not found")
        response.raise_for_status()
        task = response.json()
    today = date.today().isoformat()
    return templates.TemplateResponse("add_task.html", {"request": request, "task": task, "action": "Update", "today": today})

@app.post("/update/{task_id}")
async def update_task(task_id: int, title: str = Form(...), description: str = Form(None), due_date: str = Form(None), status: str = Form("pending")):
    task_data = {"title": title, "description": description, "due_date": due_date, "status": status}
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.put(f"/api/tasks/{task_id}", json=task_data)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Task not found")
        response.raise_for_status()
    logging.info(f"Task updated via web: {task_id}")
    return RedirectResponse(url="/", status_code=302)

@app.post("/delete/{task_id}")
async def delete_task(task_id: int):
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.delete(f"/api/tasks/{task_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Task not found")
        response.raise_for_status()
    logging.info(f"Task deleted via web: {task_id}")
    return RedirectResponse(url="/", status_code=302)

# API Endpoints (JSON-based)
@app.get("/api/tasks", response_model=list[Task], description="Retrieve all tasks")
def api_get_tasks():
    tasks = crud.get_tasks()
    return [Task(id=t[0], title=t[1], description=t[2], due_date=t[3], status=t[4]) for t in tasks]

@app.post("/api/tasks", response_model=Task)
def api_create_task(task: TaskCreate):
    task_id = crud.create_task(task)
    return Task(id=task_id, title=task.title, description=task.description, due_date=task.due_date, status=task.status)

@app.get("/api/tasks/{task_id}", response_model=Task)
def api_get_task(task_id: int):
    task = crud.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(id=task[0], title=task[1], description=task[2], due_date=task[3], status=task[4])

@app.put("/api/tasks/{task_id}", response_model=Task)
def api_update_task(task_id: int, task: TaskCreate):
    existing = crud.get_task_by_id(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.update_task(task_id, task)
    return Task(id=task_id, title=task.title, description=task.description, due_date=task.due_date, status=task.status)

@app.delete("/api/tasks/{task_id}")
def api_delete_task(task_id: int):
    existing = crud.get_task_by_id(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(task_id)
    return {"message": "Task deleted"}