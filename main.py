from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class Task(BaseModel):
    """Модель задачи"""
    id: str
    title: str
    completed: bool = False


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class BookPost(BaseModel):
    book: str


tasks: list[Task] = []
book : str = ""

@app.post("/book", response_model=str, status_code=status.HTTP_200_OK)
def post_book(payload: BookPost):
    global book
    book = payload.book
    return book

@app.get("/tasks", response_model=str)
def get_tasks():
    """Получить список задач"""
    global book
    if book:
        return "Любимая книга " + book
    return "Любимой книги нет"


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """Создать новую задачу"""
    task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task