import uvicorn
from routes.news import news
from routes.workshop import workshop
from routes.specialty import specialty
from routes.user import user
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Routes

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(specialty)
app.include_router(workshop)
app.include_router(news)

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info")
