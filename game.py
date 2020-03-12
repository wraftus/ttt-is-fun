#!/usr/bin/env python3
from enum import Enum

class Piece(Enum):
    X = -1
    O = 1
    Empty = 0

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

board = [[Piece.Empty for row in range(3)] for col in range(3)]

    
def redraw():
    to_disp = []
    col, row = 0, 0
    for ch in disp_board:
        if ch == '%':
            piece = board[col][row]
            to_disp.append(' ' if piece == Piece.Empty else 'X' if piece == Piece.Empty else 'O')
            row = row + 1 if col == 2 else row
            col = 0 if col == 2 else col + 1
        else:
            to_disp.append(ch)

    print("".join(to_disp))


def minimax(self):
    pass

if __name__ == "__main__":
    redraw()

