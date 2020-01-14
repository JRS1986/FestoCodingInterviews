import itertools
import time
from tic_tac_toe import *


def timer(start, end):
    """
    Computes and returns the elapsed time.
    :param start: time.time - Start time
    :param end: time.time - End time
    :return: str - Elapsed time as string with hours, minutes, seconds format
    """
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:02}:{:02}:{:05.2f}".format(int(hours), int(minutes), seconds)


def randomPlayer(board):
    """
    Random player: returns the random empty position.
    :param board: numpy.array - Tic Tac Toe board in 2D array
    :return: tuple - random x and y positions on the 2D array
    """
    avail_positions = np.where(board == UNOCCUPIED)
    rand_index = np.random.choice(range(0, len(avail_positions[0])))
    return (avail_positions[0][rand_index], avail_positions[1][rand_index])


def initialize_state_values():
    """
    Initializes state values by checking if it is a winning combination for players.
    Updates state_dict and state_value for player X and O.
    :return: None
    """
    game = TTTGame()
    for i in range(n_states):
        states_dict[i] = all_possible_states[i]
        game.board = np.array(states_dict[i])
        reward = game.check_terminal_state()
        if reward == PLAYER_X_WINS:
            state_value_X[i] = 1
            state_value_O[i] = -1
        elif reward == PLAYER_O_WINS:
            state_value_X[i] = -1
            state_value_O[i] = 1


def update_state(board, player, action):
    """
    Simulation of the board in the game based on action by policy.
    :param board: numpy.array - Tic Tac Toe board as 2D array
    :param player: int - player (-1 or 1)
    :param action: int - action indicating the position on the 2D array
    :return:
    """
    # Convert into coordinates on a 2D grid
    position_x = int((action - 1) // 3)
    position_y = int((action - 1) % 3)
    if board[position_x][position_y] == UNOCCUPIED:
        board[position_x][position_y] = player


def training_policy(state, state_value, player, epsilon):
    """
    Epsilon-greedy policy used during training.
    :param state: numpy.array - Tic Tac Toe board as 2D array
    :param state_value: numpy.array - 1D array of state values
    :param player: int - player (-1 or 1)
    :param epsilon: float - parameter for controlling exploration-exploitation during training
    :return: int - action to take based on the current policy
    """
    # Epsilon greedy policy to select action
    possible_actions = []
    state_action_values = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if state[i][j] == UNOCCUPIED:
                # Append the position of empty cells: 1, 2, 3, 4, 5, 6, 7, 8, 9
                possible_actions.append(i*3 + (j+1))

    # From a given state, check all the possible next states
    for action in possible_actions:
        new_state = np.copy(state)
        update_state(new_state, player, action)
        next_state_idx = list(states_dict.keys())[list(states_dict.values()).index(new_state.tolist())]
        state_action_values.append(state_value[next_state_idx])

    # print("Possible actions = " + str(possible_actions))
    # print("State action values = " + str(state_action_values))
    best_action_idx = np.argmax(state_action_values)

    if np.random.uniform(0, 1) <= epsilon:
        # Random action in epsilon % probability
        action_to_take = np.random.choice(possible_actions)
        # Reduce the value of epsilon
        epsilon *= 0.99
    else:
        # Exploit with ((1-epsilon)*100)% probability
        action_to_take = possible_actions[int(best_action_idx)]

    return action_to_take


def update_value_function(state_value, curr_state_idx, next_state_idx, step_size):
    """
    Updates the state values based on one-step lookahead.
    :param state_value: numpy.array - Value function for all states
    :param curr_state_idx: int - Index of current state in states_dict
    :param next_state_idx: int - Index of next state in states_dict
    :param step_size: float - Step size or learning rate to update the current estimate
    :return: None
    """
    new_value = state_value[curr_state_idx] + step_size * (state_value[next_state_idx] - state_value[curr_state_idx])
    state_value[curr_state_idx] = new_value


def train_agent():
    """
    Trains a RL agent based on one step lookahead Temporal Difference learning.
    Two policies are used against each other by playing out games.
    :return: None
    """

    step_size = 0.2
    epsilon = 0.3
    num_games = 10000
    num_X_wins = 0
    num_O_wins = 0
    # 100k => 01:38:24

    for iteration in range(num_games):
        current_player = np.random.choice([PLAYER_X, PLAYER_O])
        game = TTTGame(turn=current_player)
        print("Iteration ", iteration)
        result = GAME_NOT_OVER

        while result == GAME_NOT_OVER:

            curr_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game.board.tolist())]
            # Player X's turn
            if current_player == PLAYER_X:
                action_choice = training_policy(game.board, state_value_X, PLAYER_X, epsilon)
                position_x = int((action_choice - 1) // 3)
                position_y = int((action_choice - 1) % 3)
                game.play_move(PLAYER_X, position_x, position_y)
                new_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game.board.tolist())]

            # Random player O's turn
            else:
                action_choice = training_policy(game.board, state_value_O, PLAYER_O, epsilon)
                position_x = int((action_choice - 1) // 3)
                position_y = int((action_choice - 1) % 3)
                game.play_move(PLAYER_O, position_x, position_y)
                new_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game.board.tolist())]

                # To train against a player acting randomly
                # random_pos = randomPlayer(game.board)
                # game.play_move(PLAYER_O, random_pos[0], random_pos[1])

            # Update the value functions
            update_value_function(state_value_X, curr_state_idx, new_state_idx, step_size)
            update_value_function(state_value_O, curr_state_idx, new_state_idx, step_size)

            # print(game.board)
            result = game.check_terminal_state()

            if result == PLAYER_X_WINS:
                num_X_wins += 1
                # print("Result: Player X won")
            elif result == PLAYER_O_WINS:
                num_O_wins += 1
                # print("Result: Player O won")
            elif result == GAME_DRAW:
                pass
                # print("Result: Draw")
            elif result == GAME_NOT_OVER:
                current_player = -current_player

    print("Number of X player wins: {} \nNumber of O player wins: {}".format(num_X_wins, num_O_wins))


if __name__ == "__main__":
    # Script to run training of RL agent

    # TODO: replace print by logging level, logging.basicConfig(level=logging.DEBUG)
    states = [PLAYER_X, PLAYER_O, UNOCCUPIED]
    states_dict = {}
    all_possible_states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in itertools.product(states, repeat=9)]
    n_states = len(all_possible_states)
    n_actions = 9  # 9 actions in action space

    # State values initialized to 0
    state_value_X = np.full((n_states), 0.0)
    state_value_O = np.full((n_states), 0.0)

    print("Num of states: {} \nNum of actions: {}".format(n_states, n_actions))

    initialize_state_values()

    start_time = time.time()
    train_agent()

    print("Training time: ", timer(start_time, time.time()))

    # Save the trained state values
    np.savetxt("RLvsRL_state_values_player_X_trained_10k_0_2.txt", state_value_X, fmt="%.6f")
    np.savetxt("RLvsRL_state_values_player_O_trained_10k_0_2.txt", state_value_O, fmt="%.6f")
