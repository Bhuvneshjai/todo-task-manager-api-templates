from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import create_tables
from app.schemas import TaskCreate
from app import crud
import logging

app = FastAPI(title="To-do List API")
templates = Jinja2Templates(directory="app/templates")
logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
def startup():
    create_tables()
    logging.info("Database tables created or verified.")

# ---- API Endpoints ----

@app.post("api/tasks/")
def create_task_api(task: TaskCreate):
    try:
        crud.create_task(task)
        logging.info(f"Task created: {task.title}")
        return {"message": "Task created successfully"}
    except Exception as e:
        logging.error(f"Error creating task: {str(e)}")
        return {"error": "Failed to create task"}
    
@app.get("/api/tasks/")
def get_tasks_api():
    tasks = crud.get_task()
    return {"tasks": tasks}

# ---- Web Interface ----

@app.get("/", response_class=HTMLResponse)
def list_tasks(request: Request):
    tasks = crud.get_task()
    return templates.TemplateResponse(
        "list_tasks.html", 
        {"request": request, "tasks": tasks}
    )

@app.post("/add", response_class=HTMLResponse)
def add_task_form(request: Request):
    return templates.TemplateResponse("add_task.html", {"request": request})    

@app.post("/add")
def add_task(
    title: str = Form(...), 
    description: str = Form(None), 
    due_date: str = Form(None), 
    status: str = Form("pending")
):
    task = TaskCreate(
        title=title, 
        description=description, 
        due_date=due_date, 
        status=status
    )
    crud.create_task(task)
    return RedirectResponse(url="/", status_code=302)