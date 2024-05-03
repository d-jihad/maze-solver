from dataclasses import dataclass
from tkinter import Tk, Canvas


@dataclass
class Point:
    x: int
    y: int


class Line:

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def draw(self, canvas: Canvas, fill_color: str = 'black'):
        canvas.create_line(
            self.start.x, self.start.y,
            self.end.x, self.end.y,
            fill=fill_color, width=2
        )

class Window:

    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title('Maze solver')
        self.__root.geometry(f'{width}x{height}')
        self.__canvas = Canvas(self.__root, bg='white')
        self.__canvas.pack(side='top', fill='both', expand=True)
        self.__is_running: bool = False
        self.__root.protocol('WM_DELETE_WINDOW', self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

    def close(self):
        self.__is_running = False
    
    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)


class Cell:

    def __init__(self, has_left_wall: bool, has_right_wall: bool, has_top_wall: bool, has_bottom_wall: bool, x1: int, x2: int, y1: int, y2: int, win: Window):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
    
    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(
                Point(self._x1, self._y1),
                Point(self._x1, self._y2)
            ), 'black')
        if self.has_right_wall:
            self._win.draw_line(Line(
                Point(self._x2, self._y1),
                Point(self._x2, self._y2)
            ), 'black')
        if self.has_bottom_wall:
            self._win.draw_line(Line(
                Point(self._x1, self._y1),
                Point(self._x2, self._y1)
            ), 'black')
        if self.has_top_wall:
            self._win.draw_line(Line(
                Point(self._x1, self._y2),
                Point(self._x2, self._y2)
            ), 'black')

    def draw_move(self, to_cell: Cell, undo: bool = False):
        pass



def main():
    print('Running maze solver')
    win = Window(800, 600)
    cell = Cell(True, False, True, True, 10, 50, 10, 50, win)
    cell.draw()
    win.wait_for_close()


main()
