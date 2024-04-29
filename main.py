from dataclasses import dataclass
from tkinter import Tk, BOTH, Canvas


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
            fill=fill_color, width=1
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


def main():
    print('Running maze solver')
    win = Window(800, 600)
    line = Line(Point(0, 0), Point(800, 600))
    win.draw_line(line, 'red')
    win.wait_for_close()


main()
