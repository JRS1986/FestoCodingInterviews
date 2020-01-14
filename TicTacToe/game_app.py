import pygame
import sys
import itertools

from tic_tac_toe import *
from test_game import trained_policy

# Global constants for colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


def main():
    """
    Tic Tac Toe game UI using pygame.
    :return: None
    """
    pygame.init()

    DISPLAY = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Tic Tac Toe")
    DISPLAY.fill(WHITE)

    SQUARE_SIZE = 100
    GAP = 20

    # Draw 9 boxes for the game
    box1 = pygame.draw.rect(DISPLAY, GRAY, (10, 10, SQUARE_SIZE, SQUARE_SIZE))
    box4 = pygame.draw.rect(DISPLAY, GRAY, (10, SQUARE_SIZE + GAP, SQUARE_SIZE, SQUARE_SIZE))
    box7 = pygame.draw.rect(DISPLAY, GRAY, (10, 2*(SQUARE_SIZE + GAP), SQUARE_SIZE, SQUARE_SIZE))

    box2 = pygame.draw.rect(DISPLAY, GRAY, (SQUARE_SIZE + GAP, 10, SQUARE_SIZE, SQUARE_SIZE))
    box5 = pygame.draw.rect(DISPLAY, GRAY, (SQUARE_SIZE + GAP, SQUARE_SIZE + GAP, SQUARE_SIZE, SQUARE_SIZE))
    box8 = pygame.draw.rect(DISPLAY, GRAY, (SQUARE_SIZE + GAP, 2*(SQUARE_SIZE + GAP), SQUARE_SIZE, SQUARE_SIZE))

    box3 = pygame.draw.rect(DISPLAY, GRAY, (2*(SQUARE_SIZE + GAP), 10, SQUARE_SIZE, SQUARE_SIZE))
    box6 = pygame.draw.rect(DISPLAY, GRAY, (2*(SQUARE_SIZE + GAP), SQUARE_SIZE + GAP, SQUARE_SIZE, SQUARE_SIZE))
    box9 = pygame.draw.rect(DISPLAY, GRAY, (2*(SQUARE_SIZE + GAP), 2 * (SQUARE_SIZE + GAP), SQUARE_SIZE, SQUARE_SIZE))

    boxes = [box1, box2, box3, box4, box5, box6, box7, box8, box9]
    boxes_dict = {1: box1, 2: box2, 3: box3, 4: box4, 5: box5, 6: box6, 7: box7, 8: box8, 9: box9}

    def find_clicked_box(x, y):
        """
        Find the clicked box based on x and y positions
        :param x: int - x coordinate on screen
        :param y: int - y coordinate on screen
        :return: pygame.draw.rect - Corresponding box (rectangle)
        """
        for box in boxes:
            if box.collidepoint(x, y):
                return box

    states = [PLAYER_X, PLAYER_O, UNOCCUPIED]
    states_dict = {}
    all_possible_states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in itertools.product(states, repeat=9)]
    n_states = len(all_possible_states)
    n_actions = 9
    # State value with Player X as RL agent
    # state_value = np.full((n_states), 0.0)

    print("n_states = %i \nn_actions = %i" % (n_states, n_actions))
    for i in range(n_states):
        states_dict[i] = all_possible_states[i]

    # Text files to use
    # 1_RLvsRL_state_values_player_O_trained_10k_0_4
    # 2_RLvsRL_state_values_player_O_trained_100k_0_4
    # 3_RLvsRL_state_values_player_O_trained_10k_0_2

    state_value = np.loadtxt("1_RLvsRL_state_values_player_O_trained_10k_0_4.txt", dtype=np.float64)
    current_player = np.random.choice([PLAYER_X, PLAYER_O])
    # current_player = 1
    game = TTTGame(turn=current_player)
    if current_player == -1:
        starting_player = "User"
    else:
        starting_player = "BOT"

    print("Starting player: ", starting_player)
    result = GAME_NOT_OVER
    while True:
        while result == GAME_NOT_OVER:
            # (Player O) Agent's turn - BLACK circle
            if current_player == PLAYER_O:
                print("\nPlayer O (Agent)")
                action = trained_policy(game.board, states_dict, state_value, PLAYER_O)
                position_x = int((action - 1) // 3)
                position_y = int((action - 1) % 3)
                game.play_move(PLAYER_O, position_x, position_y)

                box = boxes_dict[action]
                pygame.draw.circle(DISPLAY, BLACK, box.center, 20, 0)

            # (Player X) User's turn - RED circle
            else:
                mouse_clicked = False
                # Wait for user reponse by mouse click
                while not mouse_clicked:
                    pygame.display.update()
                    for event in pygame.event.get():
                        # Mouse click event
                        if event.type == pygame.MOUSEBUTTONUP:

                            mousex, mousey = event.pos
                            # TODO: if clicked outside, set mouse clicked to False
                            mouse_clicked = True

                            # find the box
                            box = find_clicked_box(mousex, mousey)
                            pygame.draw.circle(DISPLAY, RED, box.center, 20, 0)

                            action = list(boxes_dict.keys())[list(boxes_dict.values()).index(box)]
                            position_x = int((action - 1) // 3)
                            position_y = int((action - 1) % 3)
                            game.play_move(PLAYER_X, position_x, position_y)

                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

            pygame.display.update()

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

        for event in pygame.event.get():
            # Restart the game if clicked on the game
            if event.type == pygame.MOUSEBUTTONUP:
                main()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()



