from fastapi import FastAPI, BackgroundTasks, File, Query, UploadFile, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from database.database import SessionLocal, get_db
from routers import users, login, metadata, projects, pages, voices


import uvicorn

app = FastAPI(title="Login API", 
              description="Login API", 
              version="1.0.0", 
              contact={"name" : "James Kim", "email" : "sjkim.skw.laa@gmail.com"})

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers= ["*"]
)


app.include_router(login.router)     
app.include_router(users.router)
app.include_router(metadata.router)
app.include_router(projects.router)
app.include_router(pages.router)
app.include_router(voices.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)