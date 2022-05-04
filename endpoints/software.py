from typing import List
from pydantic import BaseModel
from fastapi import APIRouter
from pymongo import MongoClient
from bson.objectid import ObjectId
from .helper_funcs import *

#
# Initial setup
#
client = MongoClient('localhost', 27017)["hcuc-timetable"]

router = APIRouter(
    prefix="/software",
    tags=["Software"],
)

#
# Schemas
#
class Software(BaseModel):
    name: str
    version: str

class SoftwareToDelete(BaseModel):
    software_list: List[str]


#
# Functions
#
@router.get("")
async def AllSoftware():
    response = client["software"].find({})
    return BsonToJson(response)

@router.post("")
async def AddSoftware(software:Software):
    """
        Endpoint for users to add new types of software.
    """
    response = client["software"].insert_one(software.__dict__)
    return {"Object": {"assigned_id": str(response.inserted_id)}}

@router.get("/id")
async def FindSoftwareByID(software_list: List[str]):
    """
        Endpoint for users to find all software by ID.
    """
    response = client["software"].find({"_id": {"$in": [ObjectId(each_software) for each_software in software_list] }})
    return BsonToJson(response)
    
@router.delete("")
async def DeleteSoftware(software:SoftwareToDelete):
    """
        Endpoint to delete software.
    """
    client["software"].delete_many({"_id": {"$in": [ObjectId(each_software) for each_software in software.software_list]}})
