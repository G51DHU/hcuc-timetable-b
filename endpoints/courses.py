from typing import Dict, List
from typing_extensions import TypedDict
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
    prefix="/courses",
    tags=["courses"],
)

#
# Schemas
#
class Courses(BaseModel):
    class Units(TypedDict):
        name: str
        code: str
        software: Dict[str,str]
        teacher: str
        timetabledHours: int

    name: str
    code: str
    units: List[Units]

class CoursesToDelete(BaseModel):
    course_list: List[str]

#
# Functions
#
@router.post("")
async def AddCourses(courses:Courses):
    """
        Endpoint for users to add new courses.
    """
    response = client["courses"].insert_one(courses.__dict__)
    return {"Object": {"assigned_id": str(response.inserted_id)}}

@router.get("")
async def AllCourses():
    """
        Endpoint, that returns all courses stored in the database.
    """
    response = client["courses"].find({})
    return BsonToJson(response)

@router.delete("")
async def Deletecourses(courses:CoursesToDelete):
    """
        Endpoint to delete courses.
    """
    client["courses"].delete_many({"_id": {"$in": [ObjectId(each_course) for each_course in courses.course_list]}})