from graphic_primatives import *
from tkinter import Tk, BOTH, Canvas
from board_model import *
from piece import Piece

class Board:
    def __init__(self, width, height, cell_size, board_model, turn_indicator):
        cell_width = cell_size
        cell_height = cell_size
        self.width = width
        self.height = height
        self.board_model = board_model
        self.turn_indicator = turn_indicator
        self.cells = []
        self.first_click = True
        self.moves = None
        self.first_x = -1
        self.first_y = -1
        self.pieces = None
        
        cell_number = 0
        for x in range(8):
            row = []
            for y in range(8):
                if cell_number % 2 == 0:
                    color = '#ad7230'
                else:
                    color = '#573722'
                cell_number += 1
                row.append(Square(x * cell_width + 10,
                                  y * cell_height + 10,
                                  (x + 1) * cell_width + 10,
                                  (y + 1) * cell_height + 10,
                                  color))
            cell_number += 1
            self.cells.append(row)

    def draw(self, canvas):
        for x in range(8):
            for y in range(8):
                self.cells[x][y].draw(canvas)
                

    def on_click(self, event):
        x = event.x - 10
        y = event.y - 10
        board_size = self.width
        cell_size = board_size / 8
        if x < 0 or y < 0 or x > board_size or y > board_size:
            return None
        cell_x = int(x // cell_size)
        cell_y = int(y // cell_size)
        cell_value = self.board_model.board_state[cell_y][cell_x]
        if cell_value != 'x':
            click_turn = cell_value > 0
#            print(self.first_click, self.turn_indicator.active, click_turn, cell_value)
            if self.first_click and self.turn_indicator.active == click_turn and cell_value != 0:
                moves = []
                moves.append((cell_y-1, cell_x-1, Movements.NOJUMP))
                moves.append((cell_y-1, cell_x+1, Movements.NOJUMP))
                moves.append((cell_y+1, cell_x-1, Movements.NOJUMP))
                moves.append((cell_y+1, cell_x+1, Movements.NOJUMP))
                moves.append((cell_y-2, cell_x-2, Movements.JUMP))
                moves.append((cell_y-2, cell_x+2, Movements.JUMP))
                moves.append((cell_y+2, cell_x-2, Movements.JUMP))
                moves.append((cell_y+2, cell_x+2, Movements.JUMP))
                self.moves = self.board_model.validate_moves(moves, cell_x, cell_y)
                if len(self.moves) > 0:
                    self.first_x = cell_x
                    self.first_y = cell_y
                    self.first_click = False
            else:
                if (cell_y, cell_x) in self.moves:
                    self.board_model = self.board_model.adjust_board(
                        self.first_y, self.first_x, cell_y, cell_x)
                    self.turn_indicator.flip_turn()
                    remove_piece = None
                    for piece in self.pieces:
                        if piece.x == self.first_x and piece.y == self.first_y:
                            jump = abs(cell_y - piece.y) == 2
                            remove_y = 0
                            remove_x = 0
                            if jump:
                                remove_y = (cell_y + piece.y)//2
                                remove_x = (cell_x + piece.x)//2
                                piece_value = self.board_model.board_state[remove_y][remove_x]
                                remove_piece = Piece(remove_x, remove_y, piece.r, piece_value > 0, abs(piece_value) == 3, piece.cell_size)
                                self.board_model.board_state[remove_y][remove_x] = 0
                            piece.x = cell_x
                            piece.y = cell_y
                            if not piece.king and ((cell_y == 0 and self.board_model.board_state[cell_y][cell_x] == 1) or (cell_y == 7 and self.board_model.board_state[cell_y][cell_x] == -1)):
                                self.board_model.board_state[cell_y][cell_x] *= 3
                                piece.king = True
                            piece.update_location()
                    if remove_piece is not None:
                        #remove_piece.delete = True
                        i = self.pieces.index(remove_piece)
                        self.pieces[i].delete = True
                        self.pieces.remove(remove_piece)
                    self.first_x = -1
                    self.first_y = -1
                    self.first_click = True

    def add_pieces(self, pieces):
        self.pieces = pieces

    def __eq__(self, rhs):
        if isinstance(rhs, Board):
            return self.width == rhs.width and self.height == rhs.height
        return False
                
