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

def main():
    win = Window(800, 600)
    win.draw_line(Line(Point(10,15), Point(8, 92)), fill_color="red")
    win.draw_line(Line(Point(15,15), Point(92, 92)), fill_color="black")
    win.wait_for_close()

main()