from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import os
import json
from bson import json_util, ObjectId
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["students_db"]  
students_collection = db["students"]  

def parse_json(data):
    return json.loads(json_util.dumps(data))

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

@app.on_event("startup")
async def startup_event():
    try:
        await client.server_info()  
        print("Connected to MongoDB")
    except Exception as e:
        print("Error connecting to MongoDB:", e)

@app.on_event("shutdown")
async def shutdown_event():
    client.close()

@app.post("/students", response_model=dict)
async def create_student(student: Student):
    result = await students_collection.insert_one(student.dict())
    return {"id": str(result.inserted_id), "message": "Student created successfully"}

@app.get("/students", response_model=List[dict])
async def list_students(
    country: Optional[str] = Query(None, description="To apply filter of country. If not given or empty, this filter should be applied."),
    age: Optional[int] = Query(None, description="Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied"),
):
    filters = {}
    
    if country:
        filters["address.country"] = country
    if age is not None:
        filters["age"] = {"$gte": age}
    
    students = await students_collection.find(filters).to_list(100)
    return [parse_json(student) for student in students]

@app.get("/students/{id}", response_model=dict)
async def fetch_student(id: str):
    try:
        student = await students_collection.find_one({"_id": ObjectId(id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return parse_json(student)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@app.patch("/students/{id}", response_model=dict)
async def update_student(id: str, student: Student):
    try:
        result = await students_collection.update_one({"_id": ObjectId(id)}, {"$set": student.dict()})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"id": id, "message": "Student updated successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@app.delete("/students/{id}", response_model=dict)
async def delete_student(id: str):
    try:
        result = await students_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"id": id, "message": "Student deleted successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
