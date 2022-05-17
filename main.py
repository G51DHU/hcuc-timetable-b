from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import rooms, software, courses

app = FastAPI(
    title="HCUC-Timetable"
)

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

app.include_router(rooms.router)
app.include_router(software.router)
app.include_router(courses.router)



