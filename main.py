from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = ""
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack()
        self.__window_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running:
            self.redraw()
    
    def close(self):
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.__p1 = p1
        self.__p2 = p2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.__p1.x, self.__p1.y, self.__p2.x, self.__p2.y,
            fill=fill_color, width = 2
        )
        canvas.pack()

class Cell:
    def __init__(self, window=None, left=True, right=True, top=True, bottom=True):
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = window
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom
        self.visited = False

    def left_right_x(self):
        if self._x1 < self._x2:
            return (self._x1, self._x2)
        return (self._x2, self._x1)

    def top_bottom_y(self):
        if self._y1 < self._y2: #changed bacause of how the canvas works
            return (self._y1, self._y2)
        return (self._y2, self._y1)
    
    def draw_cell(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        x_left, x_right = self.left_right_x()
        y_top, y_bottom = self.top_bottom_y()
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x_left, y_top), Point(x_left, y_bottom)), fill_color="black")
        else:
            self._win.draw_line(Line(Point(x_left, y_top), Point(x_left, y_bottom)), fill_color="white")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x_right, y_top), Point(x_right, y_bottom)), fill_color="black")
        else:
            self._win.draw_line(Line(Point(x_right, y_top), Point(x_right, y_bottom)), fill_color="white")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x_left, y_top), Point(x_right, y_top)), fill_color="black")
        else:
            self._win.draw_line(Line(Point(x_left, y_top), Point(x_right, y_top)), fill_color="white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x_left, y_bottom), Point(x_right, y_bottom)), fill_color="black")
        else:
            self._win.draw_line(Line(Point(x_left, y_bottom), Point(x_right, y_bottom)), fill_color="white")

    def mid_point(self):
        x_left, x_right = self.left_right_x()
        y_top, y_bottom = self.top_bottom_y()
        x_mid = (x_right + x_left)/2
        y_mid = (y_top + y_bottom)/2
        return (x_mid, y_mid)
    
    def draw_move(self, to_cell, undo=False):
        c1_x_mid, c1_y_mid = self.mid_point()
        c2_x_mid, c2_y_mid = to_cell.mid_point()
        if undo:
            col = "gray"
        else:
            col = "red"
        self._win.draw_line(Line(Point(c1_x_mid, c1_y_mid), Point(c2_x_mid, c2_y_mid)), fill_color=col)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed != None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            cols_cells = []
            for j in range(self._num_rows):
                cols_cells.append(Cell(self._win))
            self._cells.append(cols_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cells(i, j)

    def _draw_cells(self, i, j):
        if self._win is None:
            return
        
        x_initial = self._x1 + (i * self._cell_size_x)
        y_initial = self._y1 + (j * self._cell_size_y)
        x_final = x_initial + self._cell_size_x
        y_final = y_initial +  self._cell_size_y          
        self._cells[i][j].draw_cell(x_initial, y_initial, x_final, y_final)     
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        top_cell = self._cells[0][0]
        top_cell.has_top_wall = False
        self._draw_cells(0, 0)
        bottom_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        bottom_cell.has_bottom_wall = False
        self._draw_cells(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            direction_tracker = []
            if i > 0 and not self._cells[i-1][j].visited:
                direction_tracker.append((i-1, j))
            if i < self._num_cols-1 and not self._cells[i+1][j].visited:
                direction_tracker.append((i+1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                direction_tracker.append((i, j-1))
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                direction_tracker.append((i, j+1))
            
            if direction_tracker == []:
                self._draw_cells(i, j)
                return
            else:
                direction = random.randint(0, len(direction_tracker)-1)
                i1, j1 = direction_tracker[direction]
                if j == j1:
                    if i > i1:
                        current_cell.has_left_wall = False
                        self._cells[i1][j].has_right_wall = False
                    else:
                        current_cell.has_right_wall = False
                        self._cells[i1][j].has_left_wall = False
                if i == i1:
                    if j > j1:
                        current_cell.has_top_wall = False
                        self._cells[i][j1].has_bottom_wall = False
                    else:
                        current_cell.has_bottom_wall = False
                        self._cells[i][j1].has_top_wall = False
            
            self._break_walls_r(i1, j1)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(i=0, j=0)
    
    def _solve_r(self, i, j):
        if self._num_cols - 1 == i:
            if self._num_rows - 1 == j:
                return True
            if self._num_rows - 2 == j:
                return True
        if self._num_cols - 2 == i and self._num_rows - 1 == j:
            return True
        
        self._animate()
        self._cells[i][j].visited = True

        while True:
            if i == self._num_cols-1 and j == self._num_rows-1:
                return True
            if i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i-1][j].visited:
                self._cells[i][j].draw_move(self._cells[i-1][j])
                if self._solve_r(i-1, j):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i-1][j], undo=True)
            if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i+1][j].visited:
                self._cells[i][j].draw_move(self._cells[i+1][j])
                if self._solve_r(i+1, j):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i+1][j], undo=True)
            if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].visited:
                self._cells[i][j].draw_move(self._cells[i][j-1])
                if self._solve_r(i, j-1):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i][j-1], undo=True)
            if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
                self._cells[i][j].draw_move(self._cells[i][j+1])
                if self._solve_r(i, j+1):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[i][j+1], undo=True)
            return False



def main():
    win = Window(800, 600)
    #win.draw_line(Line(Point(10,15), Point(8, 92)), fill_color="red")
    #win.draw_line(Line(Point(15,15), Point(92, 92)), fill_color="black")
    #c1 = Cell(Point(10, 35), Point(50, 70), window=win)
    #c1.draw_cell()
    #c2 = Cell(Point(100, 135), Point(70, 200), window=win)
    #c2.draw_cell()
    #c2.draw_move(c1)
    m = Maze(10, 20, 20, 10, 20, 20, win)
    m.solve()
    win.wait_for_close()

main()