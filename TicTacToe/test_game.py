import itertools
from tic_tac_toe import *
from training_self_play import update_state, initialize_state_values


def trained_policy(state, states_dict, state_value, player):
    """
    Based on the trained state value, return the action to take.
    Selects the action with max value on the given state.
    :param state: numpy.array - Current state in 2D array
    :param states_dict: dict - all states enumerated
    :param state_value: numpy.array - Values for all states
    :param player: int - player in the game -1 or 1
    :return: int - Best possible action to take in the given state
    """
    possible_actions = []
    state_action_values = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if state[i][j] == 0:
                # Append the position of empty cells: 1, 2, 3, 4, 5, 6, 7, 8, 9
                possible_actions.append(i*3 + (j+1))

    # From a given state, check all the possible next states
    for action in possible_actions:
        new_state = np.copy(state)
        update_state(new_state, player, action)
        next_state_idx = list(states_dict.keys())[list(states_dict.values()).index(new_state.tolist())]
        state_action_values.append(state_value[next_state_idx])

    print("Possible actions = " + str(possible_actions))
    print("State action values = " + str(state_action_values))
    best_action_idx = np.argmax(state_action_values)

    action_to_take = possible_actions[int(best_action_idx)]
    return action_to_take


if __name__ == "__main__":
    # Script to test the trained state-value against a human player in terminal,
    # Player_O (1) is Bot, Player_X (-1) is human

    states = [PLAYER_X, PLAYER_O, UNOCCUPIED]
    states_dict = {}
    all_possible_states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in itertools.product(states, repeat=9)]
    n_states = len(all_possible_states)
    n_actions = 9
    # State value with Player X as RL agent
    state_value = np.full((n_states), 0.0)

    print("n_states = %i \nn_actions = %i" % (n_states, n_actions))
    for i in range(n_states):
        states_dict[i] = all_possible_states[i]

    state_value = np.loadtxt("1_RLvsRL_state_values_player_O_trained_10k_0_4.txt", dtype=np.float64)
    # Files:
    # RLvsRL_state_values_player_X_trained
    # trained_state_values_X
    # state_values_player_X_trained.txt
    # bkp_trained_state_values_O.txt

    current_player = np.random.choice([PLAYER_X, PLAYER_O])
    game = TTTGame(turn=current_player)
    result = GAME_NOT_OVER

    while result == GAME_NOT_OVER:
        curr_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game.board.tolist())]

        # Player X - Agent's turn
        if current_player == PLAYER_O:
            print("\nPlayer O (Agent)")
            action_choice = trained_policy(game.board, states_dict, state_value, PLAYER_O)
            position_x = int((action_choice - 1) // 3)
            position_y = int((action_choice - 1) % 3)
            game.play_move(PLAYER_O, position_x, position_y)

        # User's turn
        else:
            user_pos = tuple(input("Enter position (comma separated): "))
            game.play_move(PLAYER_X, int(user_pos[0]), int(user_pos[2]))

        print(game.board)
        result = game.check_terminal_state()

        if result == PLAYER_X_WINS:
            print("Result: Player X won")
        elif result == PLAYER_O_WINS:
            print("Result: Player O won")
        elif result == GAME_DRAW:
            print("Result: Draw")
        elif result == GAME_NOT_OVER:
            current_player = -current_player
