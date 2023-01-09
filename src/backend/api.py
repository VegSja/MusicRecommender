import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
db = pd.read_csv("../../data/rules.csv")

class Listen(BaseModel):
    userID: str
    artist: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/recommend")
async def post_recommendation(listen: Listen):
    return db.loc[db["Left_Hand_Side"] == listen.artist]["Right_Hand_Side"].tolist()