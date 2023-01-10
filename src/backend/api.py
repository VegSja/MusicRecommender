import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
db = pd.read_csv("../../data/rules.csv")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
class Listen(BaseModel):
    userID: str
    artist: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/recommend")
async def post_recommendation(listen: Listen):
    return db.loc[db["Left_Hand_Side"] == listen.artist]["Right_Hand_Side"].tolist()