from typing import List, Optional, Tuple

class GameLogic:
    @staticmethod
    def check_winner(board: List[List[Optional[str]]]) -> Optional[str]:
        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]

        # Check columns
        for col in range(3):
            if (board[0][col] == board[1][col] == board[2][col] and 
                board[0][col] is not None):
                return board[0][col]

        # Check diagonals
        if (board[0][0] == board[1][1] == board[2][2] and 
            board[0][0] is not None):
            return board[0][0]
        
        if (board[0][2] == board[1][1] == board[2][0] and 
            board[0][2] is not None):
            return board[0][2]

        return None

    @staticmethod
    def is_draw(board: List[List[Optional[str]]]) -> bool:
        return all(cell is not None for row in board for cell in row)

    @staticmethod
    def is_valid_move(board: List[List[Optional[str]]], row: int, col: int) -> bool:
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        return board[row][col] is None

    @staticmethod
    def make_move(board: List[List[Optional[str]]], row: int, col: int, player: str) -> Tuple[List[List[Optional[str]]], bool]:
        if not GameLogic.is_valid_move(board, row, col):
            return board, False
        
        board[row][col] = player
        return board, True

    @staticmethod
    def get_game_status(board: List[List[Optional[str]]]) -> Tuple[Optional[str], bool]:
        winner = GameLogic.check_winner(board)
        is_draw = GameLogic.is_draw(board) if not winner else False
        return winner, is_draw
