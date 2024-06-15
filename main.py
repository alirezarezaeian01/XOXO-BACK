from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal

# database connections

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

# url connections

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

# base model used in app

class Game(BaseModel):
    player1: str = Field(min_length=1)
    player2: str = Field(min_length=1)

# the @xxx.method() things

@app.get("/")
async def hello_world():
    return {"hello": "world"}

# home page

@app.get("/homePage")
async def home_page():
    return {"home": "page"}

# table page

@app.get("/table")
async def show_status_table(db: Session = Depends(get_db)):
    status_table = db.query(models.Status).order_by(models.Status.score.desc()).all()
    return status_table

# login page

@app.post("/login/")
async def login_to_game(game: Game):
    players[game.player1] = 0
    players[game.player2] = 0
    return {"message": "2 players added to game successfully"}

# game page

players = {}
board = [None] * 9

current_player = "X"

@app.get("/game_design")
async def game_design():
    return {"board": board}

# playing game

@app.put("/game_design/{position}")
async def game_play(position: int):
    global current_player
    if board[position] is not None:
        raise HTTPException(status_code=400, detail="Duplicate Position")
    
    board[position] = current_player
    
    current_player = "O" if current_player == "X" else "X"
    return {"message": "Done successfully"}

# result of game

@app.get("/game_design/winner/")
async def check_winner(player1: str, player2: str, db: Session = Depends(get_db)):
    
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    
    for condition in win_conditions:
        if board[condition[0]] is not None:
            if board[condition[0]] == board[condition[1]] == board[condition[2]]:
                
                p1 = db.query(models.Status).filter(models.Status.player == player1).first()
                p1.score += 1
                db.add(p1)
                
                p2 = db.query(models.Status).filter(models.Status.player == player2).first()
                p2.score -= 1
                db.add(p2)
                
                db.commit()
                                
                return {"winner": board[condition[0]]}
    return {"winner": None}
