import random
import time
from dataclasses import dataclass
from tkinter import Tk, Canvas
from typing import Optional


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

    def __init__(self, has_left_wall: bool, has_right_wall: bool, has_top_wall: bool, has_bottom_wall: bool,
                 x1: int, x2: int, y1: int, y2: int, win: Optional[Window] = None, visited: bool = False):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.visited = visited

    def _draw_cell_wall(self, sx: int, sy: int, ex: int, ey: int, is_wall: bool):
        p1 = Point(sx, sy)
        p2 = Point(ex, ey)
        color = 'black' if is_wall else 'white'
        self._win.draw_line(Line(p1, p2), fill_color=color)

    def draw(self):
        if not self._win:
            return

        self._draw_cell_wall(self._x1, self._y1, self._x1, self._y2, self.has_left_wall)
        self._draw_cell_wall(self._x2, self._y1, self._x2, self._y2, self.has_right_wall)
        self._draw_cell_wall(self._x1, self._y1, self._x2, self._y1, self.has_top_wall)
        self._draw_cell_wall(self._x1, self._y2, self._x2, self._y2, self.has_bottom_wall)

    def draw_move(self, to_cell: 'Cell', undo: bool = False):
        start = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        end = Point((to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2)

        if not self._win:
            return

        color = 'gray' if undo else 'red'
        self._win.draw_line(Line(start, end), color)


class Maze:

    def __init__(self, x1: int, y1: int, num_rows: int, num_cols: int, cell_size_x: int, cell_size_y: int,
                 win: Optional[Window] = None, seed: Optional[int] = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_rows):
            row = []

            cell_y1 = self.y1 + self.cell_size_y * i
            cell_y2 = cell_y1 + self.cell_size_y

            for j in range(self.num_cols):
                cell_x1 = self.x1 + self.cell_size_x * j
                cell_x2 = cell_x1 + self.cell_size_x

                row.append(
                    Cell(True, True, True, True,
                         cell_x1, cell_x2, cell_y1, cell_y2,
                         self.win)
                )

            self._cells.append(row)

        self._draw_maze()

    def _draw_maze(self):
        for j in range(self.num_cols):
            for i in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        if not self.win:
            return
        time.sleep(0.05)
        self.win.redraw()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_rows - 1][self.num_cols - 1].has_right_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_cells_walls(self, i: int, j: int, adj_i: int, adj_j: int):
        if adj_i > i:
            self._cells[i][j].has_bottom_wall = False
            self._cells[adj_i][adj_j].has_top_wall = False
        elif adj_i < i:
            self._cells[i][j].has_top_wall = False
            self._cells[adj_i][adj_j].has_bottom_wall = False

        if adj_j > j:
            self._cells[i][j].has_right_wall = False
            self._cells[adj_i][adj_j].has_left_wall = False
        elif adj_j < j:
            self._cells[i][j].has_left_wall = False
            self._cells[adj_i][adj_j].has_right_wall = False

    def _break_walls_r(self, i: int, j: int):
        self._cells[i][j].visited = True
        while True:
            to_visit = []

            if i < self.num_rows - 1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))

            if j < self.num_cols - 1 and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1))

            if not to_visit:
                return

            adj_i, adj_j = random.choice(to_visit)
            self._break_cells_walls(i, j, adj_i, adj_j)

            self._draw_cell(i, j)
            self._draw_cell(adj_i, adj_j)

            self._break_walls_r(adj_i, adj_j)

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False


def main():
    print('Running maze solver')

    pad_x = 50
    pad_y = 50
    num_rows = 14
    num_cols = 18
    cell_size_x = 50
    cell_size_y = 50

    width = num_cols * cell_size_x + (pad_x * 2)
    height = num_rows * cell_size_y + (pad_y * 2)

    win = Window(width, height)
    _ = Maze(pad_x, pad_y, num_rows, num_cols, cell_size_x, cell_size_y, win)
    win.wait_for_close()


if __name__ == '__main__':
    main()
