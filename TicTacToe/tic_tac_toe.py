import numpy as np
import pdb
import logging

# Global constants
BOARD_SIZE = 3
BOARD_SHAPE = (BOARD_SIZE, BOARD_SIZE)

PLAYER_X = -1   # 'X'
PLAYER_O = 1    # 'O'
UNOCCUPIED = 0  # '-'

# Player O is RL bot
PLAYER_X_WINS = -1
PLAYER_O_WINS = 1
GAME_DRAW = 0
GAME_NOT_OVER = 2


class TTTGame:
    """
    Class for Tic Tac Toe game
    """
    def __init__(self, turn=PLAYER_X):
        """
        Initialize a tic tac toe board.
        :param turn: int - player (-1 or 1) indicating next turn in the game
        """
        self.board = np.zeros(BOARD_SHAPE, dtype=int)
        self.turn = turn

    def check_terminal_state(self):
        """
        Checks if the game has reached terminal state and returns the constants based on the status.
        :return: int - Coded constants based on the status
        """

        # 3 rows, 3 columns, 2 diagonals
        diagonals = [self.board.diagonal(), np.rot90(self.board).diagonal()]
        rows = [r for r in self.board[:BOARD_SIZE, :]]
        cols = [c for c in np.rot90(self.board)[:BOARD_SIZE, :]]

        for row in rows:
            if np.all(row == PLAYER_X):
                return PLAYER_X_WINS
            if np.all(row == PLAYER_O):
                return PLAYER_O_WINS

        for col in cols:
            if np.all(col == PLAYER_X):
                return PLAYER_X_WINS
            if np.all(col == PLAYER_O):
                return PLAYER_O_WINS

        for diag in diagonals:
            if np.all(diag == PLAYER_X):
                return PLAYER_X_WINS
            if np.all(diag == PLAYER_O):
                return PLAYER_O_WINS

        if UNOCCUPIED not in self.board:
            return GAME_DRAW

        return GAME_NOT_OVER

    def play_move(self, player, position_x, position_y):
        """
        Updates the board based on the play by the player.
        :param player: int - player (-1 or 1)
        :param position_x: int - x coordinate of 2D array of board
        :param position_y: int - y coordinate of 2D array of board
        :return: None
        """
        if self.board[position_x][position_y] == UNOCCUPIED:
            if self.turn == player:
                self.board[position_x][position_y] = player
                self.turn = -player
            else:
                raise ValueError("Player {} turn invalid".format(player))
        else:
            # raise ValueError("{},{} is occupied".format(position_x, position_y))
            print("{},{} is occupied".format(position_x, position_y))
            user_pos = tuple(input("Enter new position: "))
            self.play_move(player, int(user_pos[0]), int(user_pos[2]))


