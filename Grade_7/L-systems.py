import turtle
import numpy as np

turtle.tracer(1, 0)
turtle.ht()
turtle.width(2)


def make_string(axiom, *rules, iterations=5):
    result = axiom
    for _ in range(iterations):
        for (xs, ys) in rules:
            result = result.replace(xs, ys.lower())
        result = result.upper()
    return result


def draw_string(string, step_size=10, angle=90, colors=None):
    counter = 0
    for c in string:
        if c == 'F':
            turtle.fd(step_size)
        if c == 'R':
            turtle.rt(angle)
        if c == 'L':
            turtle.lt(angle)
        if c == 'G':
            turtle.pu()
            turtle.fd(step_size)
            turtle.pd()
        if c == 'C':
            if colors is None:
                continue
            turtle.color(colors[counter % len(colors)])
            counter += 1


def koch(iterations):
    turtle.width(5)
    turtle.pu()
    turtle.setpos(-400, -200)
    turtle.pd()
    koch_str = make_string('F', ('F', 'FLFRRFLF'), iterations=iterations)
    koch_str = koch_str.replace('F', 'CF')
    colors_len = koch_str.count('C')
    colors = list(map(lambda row: tuple(row), np.linspace([0, 1, 0], [1, 1, 0], num=colors_len)))
    draw_string(koch_str, step_size=5, angle=60, colors=colors)


def dragon(iterations):
    turtle.width(3)
    dragon_str = make_string('FX', ('FX', 'FXRFYR'), ('FY', 'LFXLFY'), iterations=iterations)
    draw_string(dragon_str, step_size=10, angle=90)


def gilbert(iterations):
    gilbert_str = make_string('X', ("X", "RYFLXFXLFYR"), ("Y", "LXFRYFYRFXL"), iterations=iterations)
    draw_string(gilbert_str, step_size=5, angle=90)


def serp(iterations):
    serp_str = make_string('FXFRFFRFF', ('F', 'FF'), ('X', 'RFXFLFXFLFXFR'), iterations=iterations)
    draw_string(serp_str, step_size=10, angle=120)


koch(5)
# dragon(3)
# serp(5)
turtle.done()

# print(len(make_string('F', ('F', 'FLFRRFLF'), iterations=5)))
