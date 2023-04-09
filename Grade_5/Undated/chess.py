from turtle import *


def draw_square(x, y, side_size):
    """
    Функция рисует квадрат со стороной side_size в точке (x,y)
    """
    pu()
    setpos(x, y)
    pd()
    begin_fill()
    setpos(x + side_size, y)
    setpos(x + side_size, y + side_size)
    setpos(x, y + side_size)
    setpos(x, y)
    end_fill()


def draw_chessboard(x, y, size):
    pu()
    setpos(x, y)
    pd()
    setpos(x + size, y)
    setpos(x + size, y + size)
    setpos(x, y + size)
    setpos(x, y)

    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                draw_square(x + i * size // 8, y + j * size // 8, size // 8)


if __name__ == "__main__":
    ht()
    speed(0)
    colormode(1.)
    color(0, 0, 0)
    draw_chessboard(-300, -300, 640)
    done()
