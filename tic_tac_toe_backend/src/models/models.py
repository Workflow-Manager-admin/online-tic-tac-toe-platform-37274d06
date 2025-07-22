from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., description="User's username")
    email: str = Field(..., description="User's email address")

class UserCreate(UserBase):
    password: str = Field(..., description="User's password")

class User(UserBase):
    id: int = Field(..., description="User's unique identifier")
    created_at: datetime = Field(..., description="User creation timestamp")

class GameState(BaseModel):
    board: List[List[Optional[str]]] = Field(
        ...,
        description="3x3 game board where each cell can be 'X', 'O', or None"
    )
    current_player: str = Field(..., description="Current player's turn ('X' or 'O')")
    winner: Optional[str] = Field(None, description="Winner of the game ('X', 'O', or None)")
    is_draw: bool = Field(False, description="Whether the game ended in a draw")

class Game(BaseModel):
    id: int = Field(..., description="Game's unique identifier")
    player_x: int = Field(..., description="ID of player using 'X'")
    player_o: int = Field(..., description="ID of player using 'O'")
    state: GameState = Field(..., description="Current state of the game")
    created_at: datetime = Field(..., description="Game creation timestamp")
    updated_at: datetime = Field(..., description="Last game update timestamp")

class GameMove(BaseModel):
    row: int = Field(..., ge=0, lt=3, description="Row index of the move (0-2)")
    col: int = Field(..., ge=0, lt=3, description="Column index of the move (0-2)")

class GameHistory(BaseModel):
    id: int = Field(..., description="Game history entry unique identifier")
    game_id: int = Field(..., description="ID of the game")
    winner_id: Optional[int] = Field(None, description="ID of the winning player")
    is_draw: bool = Field(False, description="Whether the game ended in a draw")
    created_at: datetime = Field(..., description="When the game ended")
