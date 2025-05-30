from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from typing import Union
import os

load_dotenv()

# =======================
# DATABASE CONFIGURATION
# =======================
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# =======================
# LIFESPAN EVENT HANDLER
# =======================
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="./static"), name="static")
app.add_middleware(GZipMiddleware)
app.add_middleware(SessionMiddleware, secret_key="key")

# =======================
# MODELS
# =======================


class Todo(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    name: str
    description: str
    start_time: datetime
    end_time: datetime


class TodoCreate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime


# =======================
# ROUTES
# =======================
@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: SessionDep):
    todos = session.exec(select(Todo)).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})


@app.get("/todos/create", response_class=HTMLResponse)
async def show_create_todo_form(request: Request):
    return templates.TemplateResponse("create_todo.html", {"request": request})


@app.post('/todos/create', response_class=HTMLResponse)
async def create_todo(request: Request, session: SessionDep):
    content_type = request.headers.get("content-type", "")

    todo_data = None

    if "application/json" in content_type:
        data = await request.json()
        todo_data = TodoCreate(**data)
    else:  # Assume it's form-encoded
        form = await request.form()
        todo_data = TodoCreate(
            name=form["name"],
            description=form["description"],
            start_time=form["start_time"],
            end_time=form["end_time"]
        )

    todo = Todo(**todo_data.model_dump())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    request.session["flash"] = "Todo created successfully!" # Flash message
    return RedirectResponse(url='/', status_code=303)


@app.get("/todos/{todo_id}", response_class=HTMLResponse)
def get_todo(todo_id: int, request: Request, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse("todo_detail.html", {"request": request, "todo": todo})


@app.get("/todos/{todo_id}/edit", response_class=HTMLResponse)
def edit_todo_form(todo_id: int, request: Request, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse("edit_todo.html", {"request": request, "todo": todo})

from datetime import datetime

@app.post("/todos/update/{todo_id}")
async def update_todo(
    todo_id: int,
    request: Request,
    session: SessionDep,
    name: str = Form(...),
    description: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    try:
        # Convert the strings to datetime objects
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    todo.name = name
    todo.description = description
    todo.start_time = start_dt
    todo.end_time = end_dt

    session.add(todo)
    session.commit()

    request.session["flash"] = "Todo updated successfully!"
    return RedirectResponse(url="/", status_code=303)


@app.post("/todos/delete/{todo_id}")
async def delete_todo(todo_id: int, request: Request, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo)
    session.commit()

    request.session["flash"] = "Todo deleted successfully!"
    return RedirectResponse(url="/", status_code=303)
