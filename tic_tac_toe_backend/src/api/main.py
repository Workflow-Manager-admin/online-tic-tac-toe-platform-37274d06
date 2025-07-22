from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from src.models.models import (
    UserCreate, User, Game, GameMove
)
from src.database.database import db
from src.game.game_logic import GameLogic
from src.auth.auth import create_access_token, get_current_user

app = FastAPI(
    title="Tic Tac Toe API",
    description="Backend API for the Tic Tac Toe game",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PUBLIC_INTERFACE
@app.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    """
    Register a new user.
    """
    if db.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = db.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    return user

# PUBLIC_INTERFACE
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login to get access token.
    """
    user = db.verify_password(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

# PUBLIC_INTERFACE
@app.post("/games", response_model=Game)
async def create_game(opponent_id: int, current_user: dict = Depends(get_current_user)):
    """
    Create a new game with specified opponent.
    """
    if not db.get_user(opponent_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opponent not found"
        )
    game = db.create_game(current_user["id"], opponent_id)
    return game

# PUBLIC_INTERFACE
@app.post("/games/{game_id}/move", response_model=Game)
async def make_move(
    game_id: int,
    move: GameMove,
    current_user: dict = Depends(get_current_user)
):
    """
    Make a move in the specified game.
    """
    game = db.get_game(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )

    # Verify it's the user's turn
    current_player = game["state"]["current_player"]
    if ((current_player == "X" and game["player_x"] != current_user["id"]) or
        (current_player == "O" and game["player_o"] != current_user["id"])):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not your turn"
        )

    # Make the move
    board, valid = GameLogic.make_move(
        game["state"]["board"],
        move.row,
        move.col,
        current_player
    )
    
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid move"
        )

    # Update game state
    winner, is_draw = GameLogic.get_game_status(board)
    
    new_state = {
        "board": board,
        "current_player": "O" if current_player == "X" else "X",
        "winner": winner,
        "is_draw": is_draw
    }
    
    updated_game = db.update_game(game_id, new_state)

    # If game ended, create history entry
    if winner or is_draw:
        winner_id = None
        if winner == "X":
            winner_id = game["player_x"]
        elif winner == "O":
            winner_id = game["player_o"]
        
        db.create_game_history(game_id, winner_id, is_draw)

    return updated_game

# PUBLIC_INTERFACE
@app.get("/games/{game_id}", response_model=Game)
async def get_game(game_id: int, current_user: dict = Depends(get_current_user)):
    """
    Get the current state of a game.
    """
    game = db.get_game(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game

# PUBLIC_INTERFACE
@app.get("/games/history", response_model=list[Game])
async def get_game_history(current_user: dict = Depends(get_current_user)):
    """
    Get the game history for the current user.
    """
    history = db.get_user_game_history(current_user["id"])
    return history

@app.get("/")
def health_check():
    """
    Health check endpoint.
    """
    return {"message": "Healthy"}
