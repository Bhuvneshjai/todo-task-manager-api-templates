from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import create_tables
from app.schemas import TaskCreate
from app import crud
import logging

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
@app.get("/", response_class=HTMLResponse)
def list_tasks(request: Request):
    tasks = crud.get_tasks()
    return templates.TemplateResponse(
        "list_tasks.html", 
        {"request": request, "tasks": tasks}
    )

@app.get("/add", response_class=HTMLResponse)
def add_task_form(request: Request):
    return templates.TemplateResponse(
        "add_task.html", 
        {"request": request, "action": "Add"}
    )

@app.post("/add")
def add_task(
    title: str = Form(...),
    description: str = Form(None),
    due_date: str = Form(None),
    status: str = Form("pending")
):
    task = TaskCreate(title=title, description=description, due_date=due_date, status=status)
    crud.create_task(task)
    logging.info(f"Task added via UI: {title}")
    return RedirectResponse(url="/", status_code=302)

@app.get("/update/{task_id}", response_class=HTMLResponse)
def update_task_form(request: Request, task_id: int):
    task = crud.get_task_by_id(task_id)
    return templates.TemplateResponse(
        "add_task.html",
        {"request": request, "task": task, "action": "Update"}
    )

@app.post("/update/{task_id}")
def update_task(task_id: int, title: str = Form(...), description: str = Form(None), due_date: str = Form(None), status: str = Form("pending")):
    task = TaskCreate(title=title, description=description, due_date=due_date, status=status)
    crud.update_task(task_id, task)
    return RedirectResponse(url="/", status_code=302)

@app.post("/delete/{task_id}")
def delete_task(task_id: int):
    crud.delete_task(task_id)
    return RedirectResponse(url="/", status_code=302)
