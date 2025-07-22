from datetime import datetime
from typing import Dict, List, Optional
import bcrypt

# Simulated database using in-memory storage
class Database:
    def __init__(self):
        self.users: Dict[int, dict] = {}
        self.games: Dict[int, dict] = {}
        self.game_history: Dict[int, dict] = {}
        self.user_counter = 1
        self.game_counter = 1
        self.history_counter = 1

    def create_user(self, username: str, email: str, password: str) -> dict:
        # Hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        user = {
            'id': self.user_counter,
            'username': username,
            'email': email,
            'password_hash': hashed,
            'created_at': datetime.now()
        }
        self.users[self.user_counter] = user
        self.user_counter += 1
        return user

    def get_user(self, user_id: int) -> Optional[dict]:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[dict]:
        for user in self.users.values():
            if user['email'] == email:
                return user
        return None

    def verify_password(self, email: str, password: str) -> Optional[dict]:
        user = self.get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            return user
        return None

    def create_game(self, player_x_id: int, player_o_id: int) -> dict:
        game = {
            'id': self.game_counter,
            'player_x': player_x_id,
            'player_o': player_o_id,
            'state': {
                'board': [[None, None, None] for _ in range(3)],
                'current_player': 'X',
                'winner': None,
                'is_draw': False
            },
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        self.games[self.game_counter] = game
        self.game_counter += 1
        return game

    def get_game(self, game_id: int) -> Optional[dict]:
        return self.games.get(game_id)

    def update_game(self, game_id: int, game_state: dict) -> Optional[dict]:
        if game_id in self.games:
            self.games[game_id]['state'] = game_state
            self.games[game_id]['updated_at'] = datetime.now()
            return self.games[game_id]
        return None

    def create_game_history(self, game_id: int, winner_id: Optional[int], is_draw: bool) -> dict:
        history = {
            'id': self.history_counter,
            'game_id': game_id,
            'winner_id': winner_id,
            'is_draw': is_draw,
            'created_at': datetime.now()
        }
        self.game_history[self.history_counter] = history
        self.history_counter += 1
        return history

    def get_user_game_history(self, user_id: int) -> List[dict]:
        history = []
        for game in self.games.values():
            if game['player_x'] == user_id or game['player_o'] == user_id:
                history.append(game)
        return history

# Global database instance
db = Database()
