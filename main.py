from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = ""
        self.__canvas = Canvas(self.__root)
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
    def __init__(self, point_1, point_2, window, left=True, right=True, top=True, bottom=True):
        self._x1 = point_1.x
        self._y1 = point_1.y
        self._x2 = point_2.x
        self._y2 = point_2.y
        self._win = window
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom

    def left_right_x(self):
        if self._x1 < self._x2:
            return (self._x1, self._x2)
        return (self._x2, self._x1)

    def top_bottom_y(self):
        if self._y1 > self._y2:
            return (self._y1, self._y2)
        return (self._y2, self._y1)
    
    def draw_cell(self):
        x_left, x_right = self.left_right_x()
        y_top, y_bottom = self.top_bottom_y()
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x_left, y_top), Point(x_left, y_bottom)), fill_color="red")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x_right, y_top), Point(x_right, y_bottom)), fill_color="red")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x_left, y_top), Point(x_right, y_top)), fill_color="red")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x_left, y_bottom), Point(x_right, y_bottom)), fill_color="red")
        
def main():
    win = Window(800, 600)
    #win.draw_line(Line(Point(10,15), Point(8, 92)), fill_color="red")
    #win.draw_line(Line(Point(15,15), Point(92, 92)), fill_color="black")
    c1 = Cell(Point(10, 35), Point(50, 70), window=win, right=False)
    c1.draw_cell()
    win.wait_for_close()

main()