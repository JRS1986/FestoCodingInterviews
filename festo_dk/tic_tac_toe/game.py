import numpy as np
import random
import time

empty_id = 0
characters = {  -1: 'X',
                1: 'O',
                empty_id: ' '}

player_id = [-1, 1]

class TicTacToe:
    
    def __init__(self, player0, player1):
        self.game_state = np.zeros((3,3))
        self.players = [player0, player1]


    def render(self):
        """
        Print the board on terminal.
        
            :param state: current state of the board
        """

        str_line = '---------------'

        print('\n' + str_line)
        for row in self.game_state:
            for cell in row:
                symbol = characters[cell]
                print(f'| {symbol} |', end='')
            print('\n' + str_line)

    
    def set_move(self, cell, player):
        x, y = cell
        self.game_state[x, y] = player


    def game_finished(self):
        winner = evaluate(self.game_state)

        print("Game finished!")

        if winner == -1: 
            print(self.players[0].name)
        elif winner == 1:
            print(self.players[1].name)
        else:
            print("Draw")
        
        return winner


    def play(self):
        player2move = 0
        while game_over(self.game_state) == 0:
            self.render()

            player = player_id[player2move]
            cell = self.players[player2move].make_move(self.game_state, player)
            self.set_move(cell, player)

            player2move = (player2move+1) % 2
        
        self.render()
        self.game_finished()


class MinimaxPlayer:

    def __init__(self, name=None):

        if name is None:
            self.name = "Minimax" + str(int(random.random()*100))
        else:
            self.name = name

    def make_move(self, state, player):
        best = minimax(state, player)
        
        return best['pos']


def minimax(state, player):
    
    best = {'pos': None, 'score': (-10) * player}

    if game_over(state):
        score = evaluate(state)
        return {'pos': None, 'score': score}

    for x, y in get_empty_cells(state):
        state[x, y] = player
        move = minimax(state, -1*player)
        state[x,y] = empty_id
        move['pos'] = [x, y]

        if player == 1:
            if move['score'] > best['score']:
                best = move  # max value
        else:
            if move['score'] < best['score']:
                best = move  # min value

    return best


class AlphabetaPlayer:

    def __init__(self, name=None):

        if name is None:
            self.name = "Alphabeta" + str(int(random.random()*100))
        else:
            self.name = name

    def make_move(self, state, player):
        best = alphabeta(state, player, -2, 2)
        
        return best['pos']


def alphabeta(state, player, alpha, beta):
    
    best = {'pos': None, 'score': (-2) * player}

    if game_over(state):
        score = evaluate(state)
        return {'pos': None, 'score': score}

    for x, y in get_empty_cells(state):
        state[x, y] = player
        move = alphabeta(state, -1*player, alpha, beta)
        state[x,y] = empty_id
        move['pos'] = [x, y]

        if player == 1:
            if move['score'] > best['score']:
                best = move  # max value
            if move['score'] >= beta:
                return move
            if move['score'] > alpha:
                alpha = move['score']
        else:
            if move['score'] < best['score']:
                best = move  # min value
            if move['score'] <= alpha:
                return move
            if move['score'] < beta:
                beta = move['score']

    return best


class HumanPlayer:

    def __init__(self, name=None):

        if name is None:
            self.name = "Leonardo" + str(int(random.random()*100))
        else:
            self.name = name

    def make_move(self, state, player):
        move = -1
        while move < 0 or move > 8:
            try:
                move = int(input('Use numpad {0, ..., 8}: '))
                x, y = move//3, move%3
                coord = [x,y]

                if not valid_move(state, coord):
                    print('Move not valid. Try again!')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

        return coord


# Game logic:
def valid_move(state, cell):
    """
    A move is valid if the chosen cell is empty
    
        :param x: X coordinate
        :param y: Y coordinate
        
        :return: True if the board[x][y] is empty
    """
    if cell in get_empty_cells(state):
        return True
    else:
        return False


def evaluate(state):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows
    * Three cols
    * Two diagonals
        
        :param state: the state of the current board
        :param player: a human or a computer
        
        :return: player if someone wins, otherwise none
    """

    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]

    for player in [-1, 1]:
        if [player, player, player] in win_state:
            return player
    
    return 0


def game_over(state):
    """
    Checks if the game is over.
        
        :param state: the state of the current board
        
        :return: True if the game is over, False otherwise
    """

    winner = evaluate(state)
    if (winner == 0) and (empty_id in state):
        return False
    
    return True


def get_empty_cells(state):
    """
    Each empty cell will be added into cells' list
        
        :param state: the state of the current board
        
        :return: a list of empty cells
    """

    return np.dstack(np.where(state == empty_id))[0, ...]