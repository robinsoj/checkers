from tkinter import Tk, BOTH, Canvas
from graphic_primatives import *
from board import Board
from piece import Piece
from board_model import Board_Model

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Checkers"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.bind("<Button-1>", self.on_click)
        self.__canvas.bind("<B1-Motion>", self.on_drag)
        self.__canvas.pack()
        self.__clickables = []
        self.__drawables = []
        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True;
        while self.running:
            self.redraw()
            self.update_screen()

    def close(self):
        self.running = False
        self.__root.after(0, self.__root.quit)
        self.__root.destroy()

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)

    def on_click(self, event):
        for clickable in self.__clickables:
            clickable.on_click(event)

    def on_drag(self, event):
        pass #determine where it is dropped

    def get_canvas(self):
        return self.__canvas

    def register_clickable(self, obj):
        self.__clickables.append(obj)

    def register_drawable(self, obj):
        self.__drawables.append(obj)

    def update_screen(self):
        if not self.running:
            return
        red_piece = False
        black_piece = False
        self.__canvas.delete("all")

        items_to_remove = [drawable for drawable in self.__drawables if isinstance(drawable, Piece) and drawable.delete]
        for drawable in items_to_remove:
            self.__drawables.remove(drawable)
        for drawable in self.__drawables:
            if type(drawable) == Piece:
                if drawable.color == "#000000":
                    black_piece = True
                if drawable.color == "#FF0000":
                    red_piece = True
            drawable.draw(self.__canvas)
        self.running = red_piece and black_piece
        if not self.running:
            if red_piece:
                winner = "Red Wins"
            elif black_piece:
                winner = "Black Wins"
            else:
                winner = "Game Over?"
            self.__canvas.create_text(self.__canvas.winfo_width()/2,
                                      self.__canvas.winfo_height()/2,
                                      text=winner, anchor="w",
                                      font=("Helvetica", 36),
                                      fill="green")

    def report_drawables(self):
        print(len(self.__drawables))

def main():
    win = Window(800, 600)
    cell_size = int(560/8)
    bm = Board_Model()
    turn_ind = Turn_Indicator(675, 200, 125, 25)
    board = Board(550, 550, cell_size, bm, turn_ind)
    
    win.register_drawable(board)

    pieces = []
    for row in range(len(bm.board_state)):
        for col in range(len(bm.board_state[row])):
            if bm.board_state[col][row] not in ['x', 0]:
                pieces.append(Piece(row, col, cell_size/2.25,
                                    bm.board_state[col][row] > 0,
                                    abs(bm.board_state[col][row]) == 3,
                                    cell_size))
    for piece in pieces:
        win.register_drawable(piece)

    board.add_pieces(pieces)
    win.register_drawable(turn_ind)
    win.register_clickable(board)
    win.wait_for_close()


if __name__ == '__main__':
    main()
