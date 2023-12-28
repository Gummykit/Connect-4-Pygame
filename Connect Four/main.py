# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2023
# Lab 3
# Adversarial Search / Game Playing
# This module implements Connect four main python file
# Student ID: 801344820
import pygame
import time

from controller import *

# Game constants
GRID_SIZE = 100
ROWS, COLUMNS = 6, 7
GRID_COLOR = (255, 255, 255)
player1_color = (0, 255, 0)
player2_color = (204, 204, 0)
LINE_COLOR = (255, 255, 255)
# Initialize Pygame
pygame.init()
# Defining font for text render
font = pygame.font.Font(None, 36)

# AI algorithm to be selected
selected_algorithm = "minimax"
ai_move_time = 0

# Rendering UI for AI selection
algorithm_selection = pygame.Rect(50, 10, 200, 40)
algorithm_options = ["minimax", "alpha-beta pruning"]
selected_option = 0
# Set up the Pygame window
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Connect Four")

# Creating the game board for the same
game_board = [['' for j in range(COLUMNS)] for i in range(ROWS)]

# Rendering the game board
def draw_board():
    for row in range(ROWS):
        for col in range(COLUMNS):
            pygame.draw.rect(screen, GRID_COLOR, (col * GRID_SIZE, (row + 1) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
            pygame.draw.circle(screen, (0, 0, 0), (col * GRID_SIZE + GRID_SIZE // 2, (row + 1) * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 5)

# Function to check if a column is full

def draw_time(elapsed_time):
    pygame.draw.rect(screen, (0, 0, 0), (400, 50, 250, 20))
    font = pygame.font.Font(None, 20)
    text = font.render(f"Time: {elapsed_time:.8f} seconds", False, LINE_COLOR)
    screen.blit(text, (400, 50))

def draw_msg_box(msg):
    pygame.draw.rect(screen, (0, 0, 0), (100, 50, 250, 16))
    font = pygame.font.Font(None, 16)
    text = font.render(f"{msg}", False, LINE_COLOR)
    screen.blit(text, (100, 50))

def draw_move_box(msg):
    pygame.draw.rect(screen, (255, 255, 255), (100, 80, 250, 16))
    font = pygame.font.Font(None, 16)
    text = font.render(f"{msg}", False, (0, 0, 0))
    screen.blit(text, (100, 80))
def is_column_full(col):
    return game_board[0][col] != ''

# Token placement
def place(col, player):
    for row in range(ROWS - 1, -1, -1):
        if game_board[row][col] == '':
            game_board[row][col] = player
            return True
    return False

# Win condition check
def check_for_win(player):
    # Check horizontal
    print("player check ",player)
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(game_board[row][col + i] == player for i in range(4)) and player != '':
                print("row match :", player)
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(game_board[row + i][col] == player for i in range(4)) and player != '':
                print("column match :", player)
                return True

    # Diagonal check (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(game_board[row + i][col + i] == player for i in range(4)) and player != '':
                print("diag match :", player)
                return True

    # Diagonal check(bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(game_board[row - i][col + i] == player for i in range(4)) and player != '':
                print("diag match :", player)
                return True

    return False


# Draw condition check
def check_for_draw():
    return all(is_column_full(col) for col in range(COLUMNS))

def draw_reset_button():
    reset_button_rect = pygame.draw.rect(screen, player1_color, (700 - 100, 10, 90, 40))
    font = pygame.font.Font(None, 20)
    text = font.render("Reset", True, LINE_COLOR)
    screen.blit(text, (700 - 90, 15))
    return reset_button_rect

def draw_exit_button(reset_button_rect):
    exit_button_rect = pygame.draw.rect(screen, (255, 0, 0), (700 - 100, reset_button_rect.bottom + 10, 90, 40))
    font = pygame.font.Font(None, 20)
    text = font.render("Exit", True, (255, 255, 255))
    screen.blit(text, (700 - 90, reset_button_rect.bottom + 15))
    return exit_button_rect
    

def draw_dropdown(options, selected_option):
    # Dropdown area
    # Adjusting drop down dimensions
    dropdown_rect = pygame.draw.rect(screen, (255, 0, 255), (100, 10, 200, 20))

    # Selected option
    font = pygame.font.Font(None, 20)
    selected_text = font.render(options[selected_option], True, LINE_COLOR)
    screen.blit(selected_text, (110, 10))  # Slightly adjust the X-coordinate to center the text


    pygame.draw.polygon(screen, LINE_COLOR, [(280, 15), (290, 15), (285, 20)])

    return dropdown_rect


options = ["select Algorithm","minimax", "alpha-beta pruning"]
selected_option = 0
algo_selected = options[1]
dropdown_rect = draw_dropdown(options, selected_option)
count = 0

reset_button_rect = draw_reset_button()
exit_button_rect = draw_exit_button(reset_button_rect)
player_turn = "Human"
running = True
game_over = False

winner = ""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN :
            if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
            elif reset_button_rect.collidepoint(event.pos):
                    game_board = [['' for j in range(COLUMNS)] for i in range(ROWS)]
                    draw_msg_box("")
                    draw_time(0)
                    nos = 0
                    draw_move_box("NO of  game states explored :" + str(nos))
                    break
            elif dropdown_rect.collidepoint(event.pos):
                selected_option = (selected_option + 1) % len(options)
                algo_selected = options[selected_option]
                dropdown_rect = draw_dropdown(options, selected_option)
            elif player_turn == "Human" and not game_over:
                # Get the mouse position
                if selected_option == 0 :
                    draw_msg_box("choose a search Algorithm")
                    break
                else:
                    draw_msg_box("")
                draw_msg_box("Human turn")
                x, _ = pygame.mouse.get_pos()
                # Select column where token placement needs to be done
                column = x // GRID_SIZE
                # Move validation
                if not is_column_full(column):
                    if player_turn == "Human" :
                        if place(column, 'X'):
                            if check_for_win('X'):
                                winner = 'X'
                                game_over = True
                                break
                            elif check_for_draw():
                                game_over = True
                            player_turn = "AI"
                            draw_msg_box(player_turn + " turn")

        if player_turn == "AI" and running:

            draw_msg_box(player_turn + " turn")
            start_time = time.time()
            ai_move , nos = get_ai_move(game_board, options[selected_option], 'O')
            draw_move_box("states explored :" + str(nos))
            end_time = time.time()
            ai_move_time = end_time - start_time
            ai_col = ai_move[1]
            if not is_column_full(ai_col):
                place(ai_col, 'O')
                if check_for_win('O'):
                    game_over = True
                    winner = 'O'
                elif check_for_draw():
                    running = False
                    game_over = True
                player_turn = "Human"
                draw_msg_box("")

    draw_board()  # Draw the empty game board

    if winner == 'X':
        draw_msg_box("Player 1 wins!")

    elif winner == 'O':
        draw_msg_box("Player AI wins!")

    #else:
        #draw_msg_box("DRAW!")


    # Draw player tokens
    for row in range(ROWS):
        for col in range(COLUMNS):
            if game_board[row][col] == 'X':
                pygame.draw.circle(screen, player1_color, (col * GRID_SIZE + GRID_SIZE // 2, (row + 1) * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 5)
            elif game_board[row][col] == 'O':
                pygame.draw.circle(screen, player2_color, (col * GRID_SIZE + GRID_SIZE // 2, (row + 1) * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 5)



    # Display AI moves
    ai_move_time_text = font.render(f"Time: {ai_move_time:.2f} seconds", True, (255, 255, 255))
    draw_time(ai_move_time)
    pygame.display.update()




# Quit Pygame
draw_msg_box("")

#pygame.quit()



