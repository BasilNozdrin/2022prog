import turtle as ttl


def Koch(side_length=100, iterations=5):
    if iterations == 1:
        draw_side = lambda side_length, iterations: ttl.fd(side_length)
    else:
        draw_side = lambda side_length, iterations: Koch(side_length//3, iterations-1)

    draw_side(side_length, iterations)
    ttl.lt(60)
    draw_side(side_length, iterations)
    ttl.rt(120)
    draw_side(side_length, iterations)
    ttl.lt(60)
    draw_side(side_length, iterations)


def main(iterations):
    ttl.ht()
    ttl.speed(0)
    ttl.color('black', 'cyan')
    ttl.pu()
    ttl.setpos(-500,200)
    ttl.pd()

    ttl.begin_fill()
    Koch(3**5, iterations)
    ttl.rt(120)
    Koch(3**5, iterations)
    ttl.rt(120)
    Koch(3**5, iterations)
    ttl.end_fill()

    ttl.done()


if __name__ == "__main__":
    main(5)

