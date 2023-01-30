
# Работа с файлами


# Основные методы

# with open('./file1.txt', mode='w', encoding='utf-8') as file1:
#     file1.write("Hello! This is contents of file1!")
#
# with open('./file1.txt', mode='r', encoding='utf-8') as file1:
#     s = file1.read()
#
# print(s)

#

with open('./file2.txt', 'w') as file2:
    file2.writelines(
        ['asd1', 'asd2\n', 'asd3\n\n', 'asd4']
    )

# with open('./file2.txt', 'r') as file2:
#     print(file2.readlines())

# with open('./file2.txt', 'r') as file1:
#     print(f'{file1.readline() = }')
#     print(file1.readline())
#     print(file1.readlines())

with open('./a.txt', 'w') as file1:
    print(file1.write('asd1\n'))
    file1.write('asd2\n')
    file1.write('asd3')
    file1.write('asd4\n')








