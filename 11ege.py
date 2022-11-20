def main26():
    with open('./Доп.файлы/Задание 26/26.txt', 'r') as f:
        data = list(map(lambda s: int(s.strip()), f.readlines()))[1::]
    data = sorted(data)
    three_boxes = [0, 1, 2]
    min_lens = [data[0], data[1], data[2]]
    counters = [1, 1, 1]
    for i in range(1, len(data)):
        for j in range(len(three_boxes)):
            if data[i] >= data[three_boxes[j]] + 3:
                three_boxes[j] = i
                counters[j] += 1
    print(counters, min_lens)
    return counters[min_lens.index(max(min_lens))], max(min_lens)


def main27():
    with open('./Доп.файлы/Задание 27/27_B.txt', 'r') as f:
        data = list(map(lambda s: int(s.strip()), f.readlines()))[1::]
    return 0


if __name__ == "__main__":
    print(main26())
