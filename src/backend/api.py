import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("../database/sqlite.db")
c = conn.cursor()

c.execute('''
            SELECT leftside, rightside, support FROM Rules;
            ''')
db = pd.DataFrame(c.fetchall(), columns=["leftside", "rightside", "support"]).sort_values(by="support", ascending=False)

c.execute('''
            SELECT * FROM Playlist;
            ''')
playlist_db = pd.DataFrame(c.fetchall(), columns=["index", "content"])


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

class Search(BaseModel):
    query: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/recommend")
async def post_recommendation(listen: Listen):
    mask = db.leftside.str.contains(listen.artist, case=False)
    list = db[mask]["rightside"].tolist()[:5]
    return list

@app.post("/search")
async def post_search(query: Search):
    mask = db.leftside.str.contains(query.query, case=False)
    list = set(db[mask]["leftside"].tolist()[:3])
    return list

@app.get("/stats")
async def get_stats():
    artists = len(pd.unique(db['leftside']))
    playlists = len(pd.unique(playlist_db["index"]))

    return {
        "nb_of_artist": artists,
        "nb_of_playlists": playlists
    }