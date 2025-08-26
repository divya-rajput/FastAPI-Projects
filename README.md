# FastAPI Student CRUD API

This project is a simple FastAPI application for managing student records. It demonstrates basic CRUD operations (Create, Read, Update, Delete) using FastAPI and Pydantic.

## Features

- Get student by ID
- Get student by name
- Create a new student
- Update an existing student
- Delete a student

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn

## Installation

1. Clone the repository or copy the files to your local machine.
2. Install dependencies:

    ```
    pip install fastapi uvicorn
    ```

## Running the API

Start the server with:

```
python -m uvicorn myapi:app --reload
```

- The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

| Method | Endpoint                        | Description                  |
|--------|---------------------------------|------------------------------|
| GET    | `/get-student/{student_id}`     | Get student by ID            |
| GET    | `/get-by-name?name={name}`      | Get student by name          |
| POST   | `/create-student/{student_id}`  | Create a new student         |
| PUT    | `/update-student/{student_id}`  | Update an existing student   |
| DELETE | `/delete-student/{student_id}`  | Delete a student             |

## Example Student Object

```json
{
  "name": "Jane Doe",
  "age": 20,
  "class_name": "Grade 10th"
}
```

## License

This project is for educational purposes.
