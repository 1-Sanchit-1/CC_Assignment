
## Features

- **Create a Student**: Add new students to the database.
- **List Students**: Retrieve a list of students with optional filtering by `country` and `age`.
- **Fetch Student**: Retrieve a student by their unique ID.
- **Update Student**: Update an existing student's information by ID.
- **Delete Student**: Remove a student from the database by ID.

---

## Requirements

- Python 3.7+
- FastAPI
- MongoDB
- Motor (AsyncIO MongoDB driver)
- Pydantic

---

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/student-management-api.git
cd student-management-api
```

### Step 2: Set up a virtual environment

```bash
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure `.env`

Create a `.env` file with the following content:

```plaintext
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/students_db?retryWrites=true&w=majority
```

Replace `<username>`, `<password>`, and `<cluster-url>` with your MongoDB connection details.

### Step 5: Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## API Endpoints

### **1. Root Endpoint**

- **URL**: `/`
- **Method**: `GET`
- **Description**: Provides a welcome message and a list of available endpoints.

**Response Example**:
```json
{
  "message": "Welcome to the Student Management API! Use the following endpoints:",
  "endpoints": [
    {"method": "POST", "url": "/students", "description": "Create a new student"},
    {"method": "GET", "url": "/students", "description": "List all students with optional filters"},
    {"method": "GET", "url": "/students/{id}", "description": "Fetch a specific student by ID"},
    {"method": "PATCH", "url": "/students/{id}", "description": "Update a student's details"},
    {"method": "DELETE", "url": "/students/{id}", "description": "Delete a student by ID"}
  ]
}
```

---

### **2. Create a Student**

- **URL**: `/students`
- **Method**: `POST`
- **Description**: Add a new student to the database.

**Request Body**:
```json
{
  "name": "John Doe",
  "age": 22,
  "address": {
    "city": "New York",
    "country": "USA"
  }
}
```

**Response Example**:
```json
{
  "id": "64b2fa7f4a4d3e5898c12345",
  "message": "Student created successfully"
}
```

---

### **3. List Students**

- **URL**: `/students`
- **Method**: `GET`
- **Description**: Retrieve all students, with optional filters for `country` and `age`.

**Query Parameters**:
- `country` (optional): Filter by country.
- `age` (optional): Filter by age (students with age greater than or equal to the given value).

**Response Example**:
```json
[
  {
    "id": "64b2fa7f4a4d3e5898c12345",
    "student": {
      "name": "John Doe",
      "age": 22,
      "address": {
        "city": "New York",
        "country": "USA"
      }
    }
  }
]
```

---

### **4. Fetch a Student**

- **URL**: `/students/{id}`
- **Method**: `GET`
- **Description**: Retrieve a student by their unique ID.

**Response Example**:
```json
{
  "id": "64b2fa7f4a4d3e5898c12345",
  "student": {
    "name": "John Doe",
    "age": 22,
    "address": {
      "city": "New York",
      "country": "USA"
    }
  }
}
```

---

### **5. Update a Student**

- **URL**: `/students/{id}`
- **Method**: `PATCH`
- **Description**: Update an existing student's details by ID.

**Request Body**:
```json
{
  "name": "Jane Doe",
  "age": 23,
  "address": {
    "city": "Los Angeles",
    "country": "USA"
  }
}
```

**Response Example**:
```json
{
  "id": "64b2fa7f4a4d3e5898c12345",
  "message": "Student updated successfully"
}
```

---

### **6. Delete a Student**

- **URL**: `/students/{id}`
- **Method**: `DELETE`
- **Description**: Delete a student by their unique ID.

**Response Example**:
```json
{
  "id": "64b2fa7f4a4d3e5898c12345",
  "message": "Student deleted successfully"
}
```

---

## Error Codes

- `400 Bad Request`: Invalid input or parameters.
- `404 Not Found`: Resource not found.
- `500 Internal Server Error`: Server encountered an issue.

---

## Testing the API

You can test the API using tools like **Postman**, **curl**, or the **Swagger UI** provided by FastAPI. The Swagger UI is available at:

```
http://localhost:8000/docs
```

Alternatively, you can use the ReDoc interface at:

```
http://localhost:8000/redoc
```

--- 
