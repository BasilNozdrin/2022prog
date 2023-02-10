from turtle import *


def gradient_1d(a, b, t):
    return (1 - t) * a + t * b


def gradient_2d(a, b, c, d, t, w):
    return (1 - t) * (1 - w) * a + t * (1 - w) * b + (1 - t) * w * c + t * w * d


def gradient_line(length, line_width, color1, color2):
    width(line_width)
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    for x in range(length + 1):
        t = x / length
        r = (1 - t) * r1 + t * r2
        g = (1 - t) * g1 + t * g2
        b = (1 - t) * b1 + t * b2
        color(r, g, b)
        fd(1)


def gradient_square(x, y, size, color1, color2, color3, color4, smoothness=100):
    width(size/smoothness)
    for h in range(smoothness+1):
        t = h / smoothness
        pu()
        setpos(x+h*size/smoothness, y)
        seth(90)
        pd()
        for v in range(smoothness+1):
            w = v / smoothness
            new_color = tuple(gradient_2d(a, b, c, d, t, w) for a, b, c, d in zip(color1, color2, color3, color4))
            color(new_color)
            fd(size/smoothness)


if __name__ == "__main__":
    ht()
    tracer(1, 0)
    colormode(1.)

    gradient_square(-400, -400, 800, (1, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))
    # gradient_square(0, 0, 100, (1, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))
    done()
