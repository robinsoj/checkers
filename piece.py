from graphic_primatives import *
from tkinter import Tk, BOTH, Canvas

class Piece:
    def __init__(self, x, y, r, side, king, cell_size):
        self.x = x
        self.y = y
        self.r = r
        self.king = king
        if side:
            self.color = "#000000"
            self.color2 = "#FF0000"
        else:
            self.color = "#FF0000"
            self.color2 = "#000000"
        self.cell_size = cell_size
        self.update_location()
        self.delete = False

    def update_location(self):
        x = self.x
        y = self.y
        r = self.r
        cell_size = self.cell_size
        
        center_x = (x + .5) * cell_size + 10
        center_y = (y + .5) * cell_size + 10
        if self.king:
            points = []
            points.append(Point(int(center_x - 2/3 * r), int(center_y - 1/3 * r)))
            points.append(Point(int(center_x - 2/3 * r), int(center_y + 1/3 * r)))
            points.append(Point(int(center_x + 2/3 * r), int(center_y + 1/3 * r)))
            points.append(Point(int(center_x + 2/3 * r), int(center_y - 1/3 * r)))
            points.append(Point(int(center_x + 1/3 * r), int(center_y - 1/6 * r)))
            points.append(Point(int(center_x), int(center_y - 1/3 * r)))
            points.append(Point(int(center_x - 1/3 * r), int(center_y - 1/6 * r)))
            self.crown = Polygon(x, y, self.color2, points)
        else:
            self.crown = None
        self.circle = Circle(center_x, center_y, r, self.color)
        
    def draw(self, canvas):
        if canvas is None:
            return
        self.circle.draw(canvas)
        if self.crown is not None:
            self.crown.draw(canvas)

    def __str__(self):
        ret_str = ""

        ret_str += f"X: {self.x}\nY: {self.y}\nR: {self.r}\nColor: {self.color}/{self.color2}\nDelete: {self.delete}\n"
        if self.crown is not None:
            for pts in self.crown:
                ret_str += f"\t({pts.x}, {pts.y}\n"

        return ret_str

    def __eq__(self, rhs):
        if isinstance(rhs, Piece):
            return self.x == rhs.x and self.y == rhs.y
        return False
