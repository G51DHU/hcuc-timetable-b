from typing import List, Dict
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from helper_funcs import *
from bson.objectid import ObjectId
from bson.json_util import dumps as bson_dumps
from json import loads as json_loads

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
    response = COLLECTION["software"].delete_many({"_id": {"$in": [ObjectId(each_software) for each_software in software.software_list]}})
    print((response))