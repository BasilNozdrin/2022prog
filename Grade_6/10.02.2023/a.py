
def main():
    x1, x2, x3 = 5, 10, -999
    print(list(map(some_function, [x1, x2, x3])))


def some_function(x):
    return x * 2


if __name__ == "__main__":
    main()
