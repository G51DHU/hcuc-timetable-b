from typing import List
from pydantic import BaseModel
from fastapi import APIRouter
from pymongo import MongoClient
from .helper_funcs import *

#
# Initial Setup
#
client = MongoClient('localhost', 27017)["hcuc-timetable"]
router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)

#
# Schemas
#
class Rooms(BaseModel):
    name: str
    block: str
    software_id: List[str]

#
# Functions
#
@router.post("/add")
async def AddRooms(rooms:Rooms):
    """
        Endpoint for users to add new types of software.
    """
    response = client["rooms"].insert_one(rooms.__dict__)
    return {"Object": {"assigned_id": str(response.inserted_id)}}


@router.get("/")
async def AllRooms():
    response = client["rooms"].find({})
    return BsonToJson(response)

@router.get("/by_block")
async def RoomsByBlock(block_letter:str):
    response = client["rooms"].find({"name": {"$in": block_letter}})
    return BsonToJson(response)