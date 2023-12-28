# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2023
# Lab 3
# Adversarial Search / Game Playing
# This module implements Connect four controller python file
# Student ID: 801344820
import games
from games import *


def gen_state(to_move, game_board, h=6, v=7):
    """Given whose turn it is to move, the positions of X's on the board, the
    positions of O's on the board, and, (optionally) number of rows, columns
    and how many consecutive X's or O's required to win, return the corresponding
    game state"""

    moves = []
    board = {}

    for row in range(h):
        for col in range(v):
            pos = (row, col)
            if game_board[row][col] == 'X':
                board[pos] = 'X'
            elif game_board[row][col] == 'O':
                board[pos] = 'O'
            else:
                if pos not in moves:
                    moves.append(pos)
    return games.GameState(to_move=to_move, utility=0, board=board, moves=moves)
def get_ai_move(game_board,player_type,to_move):

    state = gen_state(to_move, game_board)
    cf_game = games.ConnectFour()
    explored_states = state.moves
    if player_type == "MINMAX":
        return games.minmax_decision(state, cf_game), len(explored_states)
    elif player_type == "ALPHA-BETA PRUNING":
        return games.alpha_beta_search(state, cf_game), len(explored_states)
    else :
        return games.alpha_beta_cutoff_search(state, cf_game) , len(explored_states)




