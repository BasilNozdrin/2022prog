
# Работа с файлами

# with open('./file1.txt', 'w') as file1:
#     file1.write("Hello! This is contents of file1!")

# with open('./file1.txt', 'r') as file1:
#     s = file1.read()
#     print(s)

with open('./file2.txt', 'w') as file1:
    file1.writelines(
        ['asd1', 'asd2\n', 'asd3\n', 'asd4\n']
    )

with open('./file2.txt', 'r') as file1:
    print(file1.readlines())

with open('./file2.txt', 'r') as file1:
    print(file1.readline())
    print(file1.readline())
    print(file1.readlines())




