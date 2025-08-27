from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
from psycopg2 import connect, sql

app = FastAPI()
conn = connect(
    dbname="test",
    user="admin",
    password="admin",
    host="localhost",
    port=5432
)

# Migration: Create table if not exists
def migrate():
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()

migrate()

@app.get("/{todo_id}")
def read_todo(todo_id: int = Path(..., description="The ID of the todo to retrieve", gt=0)):
    cursor = conn.cursor()
    query = sql.SQL("SELECT * FROM todos WHERE id = %s")
    cursor.execute(query, (todo_id,))
    todo = cursor.fetchone()
    cursor.close()
    if todo:
        # If you don't have a 'completed' column, remove 'completed': todo[2]
        return {"id": todo[0], "task": todo[1]}
    return {"Error": "Todo not found"}

@app.post("/create-todo")
def create_todo(todo: dict):
    cursor = conn.cursor()
    query = sql.SQL("INSERT INTO todos (task) VALUES (%s) RETURNING id")
    cursor.execute(query, (todo['task'],))
    todo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"id": todo_id}

@app.put("/update-todo/{todo_id}")
def update_todo(todo_id: int, todo: dict):
    cursor = conn.cursor()
    query = sql.SQL("UPDATE todos SET task = %s where id = %s RETURNING id")
    cursor.execute(query,(todo['task'],todo_id))
    updated_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    if updated_id:
        return {"message": "Task updated successfully", "id": updated_id[0]}
    return{"Error": "Task update failed due to no task id was found"}

@app.delete("/delete-task/{todo_id}")
def delete_task(todo_id: int):
    cursor = conn.cursor()
    query = sql.SQL("DELETE FROM todos where id = %s RETURNING id")
    cursor.execute(query,(todo_id,))
    deleted_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    if deleted_id:
        return {"message": "Task deleted successfully", "id": deleted_id[0]}
    return {"Error": "No task to delete"}