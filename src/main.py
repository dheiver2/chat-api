from fastapi import FastAPI
from .chat_handler import app as chat_app
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_app, prefix="/chat")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à FastAPI!"}
