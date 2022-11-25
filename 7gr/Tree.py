from turtle import *


def save_state():
    """
    Функция возвращает текущее положение и направление черепашки
    :return: пара (p,h), где p - (x,y) координаты черепашки, а h - направление черепашки
    """
    return pos(), heading()


def load_state(state):
    """
    Функция устанавливает переданные положение и направление черепашки
    :param state: пара (p,h), где p - (x,y) координаты черепашки, а h - направление черепашки
    """
    pu()
    seth(state[1])
    setpos(state[0])
    pd()


def draw_tree(iterations=5, side_length=100., angle=30., k=0.8):
    fd(side_length)
    if iterations < 1:
        return
    state = save_state()

    # рисуем левую ветку
    lt(angle)
    color((0.7, 0.9, 0))
    draw_tree(iterations-1, side_length*k, angle, k)

    load_state(state)

    # рисуем правую ветку
    rt(angle)
    color((0, 0.8, 0.5))
    draw_tree(iterations - 1, side_length * k, angle, k)


if __name__ == "__main__":
    ht()                        # скрыть стрелочку (ускоряет процесс рисования)
    speed(0)                    # установить максимальную скорость рисования
    pu()
    setpos((-100, -200))        # сдвинуть начало рисования вниз на 100px и влево на 200px
    pd()
    seth(90)                    # поставить начальное направление вверх
    color('brown')              # сменить цвет на коричневый
    width(3)                    # установить толщину линии в 3px
    draw_tree()                 # рисование дерева
    done()                      # команда, чтобы окно не закрылось после рисования
