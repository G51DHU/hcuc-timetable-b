from typing import List
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from helper_funcs import *
from bson.objectid import ObjectId

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://10.52.23.208:3000",
    "http://192.168.1.211:3000",
    "http://192.168.182.1:3000",
    "http://192.168.206.1:3000"
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
    return BsonToJson(response)

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
    return {"Object": {"assigned_id": str(response.inserted_id)}}


class SoftwareToDelete(BaseModel):
    software_list: List[str]

@app.delete("/delete_software")
async def DeleteSoftware(software:SoftwareToDelete):
    COLLECTION["software"].delete_many({"_id": {"$in": [ObjectId(each_software) for each_software in software.software_list]}})


class Rooms(BaseModel):
    block: str


@app.post("/add_rooms")
async def AddRooms(rooms:rooms):
    """Endpoint for users to add new types of software.

    Args:
        software (Software): Takes in an object corresponding to the "Software" schema.

    Returns:
        _type_: dict
    """
    response = COLLECTION["software"].insert_one(rooms.__dict__)
    return {"Object": {"assigned_id": str(response.inserted_id)}}


@app.get("/list_of_rooms")
async def ListRooms():
    response = COLLECTION["rooms"].find({})
    return BsonToJson(response)

