from typing import List
from pydantic import BaseModel
from fastapi import APIRouter
from pymongo import MongoClient
from bson.objectid import ObjectId
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


@router.get("")
async def AllRooms():
    """
        Endpoint, that returns all rooms stored in the database.
    """
    response = client["rooms"].find({})
    return BsonToJson(response)

@router.get("/by_block")
async def RoomsByBlock(block_letter:str):
    """
        Endpoint, that returns all rooms, located within a certain block stored in the database.
    """
    response = client["rooms"].find({"name": {"$in": block_letter}})
    return BsonToJson(response)

@router.delete("")
async def DeleteRooms(room_ids:List[str]):
    """
        Endpoint to delete rooms.
    """
    client["software"].delete_many({"_id": {"$in": [ObjectId(id) for id in room_ids]}})
