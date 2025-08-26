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
        CREATE TABLE IF NOT EXISTS student (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            class INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            active BOOLEAN NOT NULL
        );
    """)
    conn.commit()
    cursor.close()

migrate()


@app.post("/create-student")
def create_student(student: dict):
    # Add to database instead of students dict
    cursor = conn.cursor()
    query = sql.SQL("INSERT INTO student (name, age, class, active) VALUES (%s, %s, %s, %s) RETURNING id")
    cursor.execute(query, (
        student['name'],
        student['age'],
        student['class'],
        student['active'],
    ))
    student_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    if student:
        # If you don't have a 'completed' column, remove 'completed': todo[2]
        return {"id": student[0], "name": student[1], "age": student[2], "class": student[3], "active": student[4]}
    return {"Error": "Todo not found"}

@app.get("/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student to retrieve", gt=0)):
    cursor = conn.cursor()
    query = sql.SQL("SELECT * FROM student WHERE id = %s and active = true")
    cursor.execute(query,(student_id,))
    student = cursor.fetchone()
    print(student)
    conn.commit()
    cursor.close()
    if student:
        return {"id": student[0], "name": student[1], "age": student[2], "class": student[3], "active": student[6]}
    return {"Error": "Todo not found"}
    

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: dict):
    cursor = conn.cursor()
    query = sql.SQL("""
        UPDATE student
        SET name = %s, age = %s, class = %s, active = %s
        WHERE id = %s
        RETURNING id
    """)
    cursor.execute(query, (
        student['name'],
        student['age'],
        student['class'],
        student['active'],
        student_id)
    )
    updated_id = cursor.fetchone()
    conn.commit()
    cursor.close()

    if updated_id:
        return {"message": "Student updated successfully", "id": updated_id[0]}
    return {"Error": "Student not found or update failed"}

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    cursor = conn.cursor()
    query = sql.SQL("UPDATE student SET active = false WHERE id = %s RETURNING id")
    cursor.execute(query, (student_id,))
    deleted_id = cursor.fetchone()
    conn.commit()
    cursor.close()

    if deleted_id:
        return {"message": "Student deactivated", "id": deleted_id[0]}
    return {"Error": "Student not found or already inactive"}
