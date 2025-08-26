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

students = {
    1: {
        "name":"John Doe",
        "age": 18,
        "class": "Grade 12th"
    },
    2: {
        "name":"Divya Rajput",
        "age": 31,
        "class": "Grade 9th"
    },
    3: {
        "name":"Gaurav",
        "age": 28,
        "class": "Grade 6th"
    }
}

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

class Student(BaseModel):
    name: str
    age: int
    class_name: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    class_name: Optional[str] = None

@app.get("/")
def index():
    return { "name": "First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="Id is a required parameter",gt=0,lt=10)):
    # read from database instead of students dict
    if student_id not in students:
        return {"Error": "Student not found"}
    return students[student_id]

@app.get("/get-by-name")
def get_student(name: str):
    # read from database instead of students dict
    for student_id in students:
        if students[student_id]["name"] == name:
            print(students[student_id].keys())
            return students[student_id]
    return {"Data": "Not Found"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    # Add to database instead of students dict
    if student_id in students:
        return {"Error": "Student Exists"}
    students[student_id] = student.dict()  # Convert to dict    
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    # Udpate in database instead of students dict
    if student_id not in students:
        return {"Error": "Student does not exist"}
    if student.name is not None:
        students[student_id]["name"] = student.name
    if student.age is not None:
        students[student_id]["age"] = student.age
    if student.class_name is not None:
        students[student_id]["class"] = student.class_name
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    # Soft delete in database instead of students dict
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}