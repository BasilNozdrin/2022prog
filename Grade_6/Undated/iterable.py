class StrangeArray:
    def __init__(self, data: list):
        for row in data:
            if len(row) != len(data):
                raise ValueError('data must be square array')
        self.data = data

    def __iter__(self):
        return StrangeIterator(self)

    def __repr__(self):
        return self.data.__repr__()


class StrangeIterator:
    def __init__(self, strange_array):
        self.iterable = strange_array
        self.diagonal = 0
        self.counter = 0
        self.data_size = len(self.iterable.data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.diagonal > self.data_size * 2 - 1:
            raise StopIteration()

        dif = 0 if self.diagonal < self.data_size else self.diagonal - self.data_size + 1

        row = self.counter
        col = self.diagonal - self.counter

        if row >= self.data_size or col >= self.data_size:
            raise StopIteration

        self.counter += 1
        if self.counter == self.diagonal + 1 - dif:
            self.diagonal += 1
            self.counter = 0 if self.diagonal < self.data_size else self.diagonal - self.data_size + 1

        return self.iterable.data[row][col]


def main():
    size = 5
    data = [[i + row_n * size + 1 for i in range(size)] for row_n in range(size)]
    classic = StrangeArray(data)

    for row in data:
        print(*row)
    print('\n\n')

    for haha in classic:
        print(haha, end=' ')
    print()

    print(', '.join(map(str, classic)))


if __name__ == '__main__':
    main()
