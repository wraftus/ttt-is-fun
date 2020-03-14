#!/usr/bin/env python3
from enum import Enum
import copy
import os

class Piece(Enum):
    X = True
    O = False
    Empty = None

disp_board = [ch for ch in """
    A     B     C
       |     |
1   %  |  %  |  %   
  -----+-----+-----
2   %  |  %  |  %
  -----+-----+-----
3   %  |  %  |  %
       |     |
"""]

# holds state of the board
board = [[Piece.Empty for col in range(3)] for row in range(3)]

# draws board to the screen
def redraw():
    to_disp = []
    row, col = 0, 0
    for ch in disp_board:
        if ch == '%':
            piece = board[row][col]
            to_disp.append(' ' if piece == Piece.Empty else 'X' if piece == Piece.X else 'O')
            row = row + 1 if col == 2 else row
            col = 0 if col == 2 else col + 1
        else:
            to_disp.append(ch)

    print("".join(to_disp))

def check_winner(board):
    # check horizontal and vertical from [0][0] square (left col and top row)
    if board [0][0] != Piece.Empty:
        if board[0][0] == board[0][1] and board[0][1] == board[0][2]:
            return board[0][0]
        if board[0][0] == board[1][0] and board[1][0] == board[2][0]:
            return board[0][0]
    
    # check horizontal and vertical form [2][2] square (right col and bot row)
    if board [2][2] != Piece.Empty:
        if board[2][0] == board[2][1] and board[2][1] == board[2][2]:
            return board[2][2]
        if board[0][2] == board[1][2] and board[1][2] == board[2][2]:
            return board[2][2]

    # check diagonal with horizontal and vertical from [1][1] (middle col and row)
    if board [1][1] != Piece.Empty:
        if board[1][0] == board[1][1] and board[1][1] == board[1][2]:
            return board[1][1]
        if board[0][1] == board[1][1] and board[1][1] == board[2][1]:
            return board[1][1]
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[1][1]
        if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[1][1]
    
    # check if it's a tie
    if len(get_valid_moves(board)) == 0:
        return Piece.Empty

    # no winner, return None
    return None

def get_valid_moves(board):
    return [[row, col] for col in range(3) for row in range(3) if board[row][col] == Piece.Empty]

# minimax function for the baord
def minimax(board, playing, max_player):
    # check if game is still playable
    winner = check_winner(board)
    if winner == Piece.Empty:
        return 0
    if winner != None:
        return 1 if winner == max_player else -1

    # calculate minimax for all sub moves
    sub_move_results = []
    next_player = Piece.X if playing == Piece.O else Piece.O
    for m_row, m_col in get_valid_moves(board):
        board[m_row][m_col] = playing
        sub_move_results.append(minimax(board, next_player, max_player))
        board[m_row][m_col] = Piece.Empty

    return max(sub_move_results) if playing == max_player else min(sub_move_results)
    
# parse and execute command from user
def parse_and_exec_cmd(cmd):
    # make sure command is valid
    if len(cmd) != 2:
        return False

    col, row = (ord(cmd[0]) - ord('A')), (ord(cmd[1]) - ord('1'))
    if not 0 <= col < 3 or not 0 <= row < 3:
        return False
    if not [row, col] in get_valid_moves(board):
        return False

    # execute command
    board[row][col] = Piece.X
    return True

def computer_turn():
    # find best move from minimax
    best_row, best_col = -1, -1
    best_val = -2
    for move_row, move_col in get_valid_moves(board):
        board[move_row][move_col] = Piece.O
        val = minimax(board, Piece.X, Piece.O)
        board[move_row][move_col] = Piece.Empty
        if val > best_val:
            best_val = val
            best_row, best_col = move_row, move_col
    
    # make computers move
    board[best_row][best_col] = Piece.O

if __name__ == "__main__":
    move_valid = True
    while(check_winner(board) == None):
        os.system('clear')
        print("\r\n--------------- Welcome to Tic Tac Toe! ---------------")
        redraw()
        if not move_valid:
            print("Invalid Move!")
            move_valid = True

        if parse_and_exec_cmd(input("Type in a position to play: ")):
            if check_winner(board) == None:
                computer_turn()
            else:
                break
        else:
            move_valid = False
   
    os.system('clear')
    print("\r\n--------------- Welcome to Tic Tac Toe! ---------------")
    redraw()
    winner = check_winner(board)
    if winner == Piece.Empty:
        print("Tie!")
    else:
        print(('X' if winner == Piece.X else 'O') + " won!")
