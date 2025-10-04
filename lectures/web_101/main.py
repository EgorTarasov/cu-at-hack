from pydantic import BaseModel
from fastapi import FastAPI, HTTPException


class Todo(BaseModel):
    id: int  # добавляем поле id для идентификации задачи.
    title: str
    description: str | None = None
    completed: bool = False


app = FastAPI()

# Хранилище задач в памяти
db = {}


@app.get("/")
def index():
    return {"Hello": "World"}


@app.post("/todos/")
def create_todo(todo: Todo):
    if todo.id in db:
        raise HTTPException(status_code=400, detail="Todo with this ID already exists")
    db[todo.id] = todo
    return todo


@app.get("/todos/")
def get_all_todos():
    return list(db.values())


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del db[todo_id]
    return {"message": "Todo deleted successfully"}
