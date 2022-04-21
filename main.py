from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from helper_funcs import *

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient('localhost', 27017)["hcuc-timetable"]

COLLECTION = {
    "software": client["software"]
}

@app.get("/list_of_software")
async def ListSoftware():
    response = COLLECTION["software"].find({})
    return [BsonToJson(response)]

class Software(BaseModel):
    name: str
    version: str

@app.post("/add_software")
async def AddSoftware(software:Software):
    """Endpoint for users to add new types of software.

    Args:
        software (Software): Takes in an object corresponding to the "Software" schema.

    Returns:
        _type_: dict
    """
    response = COLLECTION["software"].insert_one(software.__dict__)
    return {"Object": {"assigned_id": BsonToJson(response.inserted_id)}}