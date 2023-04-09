# Работа с файлами. Основные методы

# Открываем файл в режиме записи (w - write)
with open('file1.txt', mode='w', encoding='utf-8') as file1:
    # Пишем в файл
    file1.write("Hello! This is contents of file1!\n")
    file1.write("This is second line in file1.txt\n")
    line_3 = "This is third line in file1.txt\n"
    write_return = file1.write(line_3)
    print(f'{write_return = }, {len(line_3) = }', end='\n'+'~'*30+'\n')

# Открываем файл в режиме чтения (r - read)
with open('file1.txt', mode='r', encoding='utf-8') as file1:
    # читаем полностью файл
    s = file1.read()
print(s, end='\n'+'~'*30+'\n')

with open('file2.txt', 'w') as file2:
    # пример использования метода для записи массива строк
    file2.writelines(
        ['asd1', 'asd2\n', 'asd3\n\n', 'asd4']
    )

    # for x in ['asd1', 'asd2\n', 'asd3\n\n', 'asd4']:
    #     file2.write(x)

    # file2.write('asd1')
    # file2.write('asd2\n')
    # file2.write('asd3\n\n')
    # file2.write('asd4')

with open('file2.txt', 'r') as file2:
    # пример использования метода для чтения файла в формате массива строк
    strings = file2.readlines()
    print(strings)
    counter = 0
    for s in strings:
        print(s, end='')
    print('\n'+'~'*30+'\n')

with open('file2.txt', 'r') as file1:
    # При открытии файла на самом деле создается специальный объект,
    # (в данном примере) мы его храним в переменной file1
    # Этот объект - файловый дескриптор.
    # Он двигается по файлу, считывая информацию символ за символом.
    # В Python методы позволяют считывать сразу множество символов

    # Метод readline считывает одну строку, до символа переноса строки '\n' (включительно)
    print(f'{file1.readline() = }')

    # Повторный вызов будет считывать уже вторую строку
    print(file1.readline())

    # Вызов функции readlines будет немного нестандартным -
    # уже считанные ранее строки не будут считываться второй раз
    print(file1.readlines(), end='\n'+'~'*30+'\n')

