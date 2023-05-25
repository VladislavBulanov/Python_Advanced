import inspect


result = 0
for n in range(1, 11):
    result += n ** 2


# Получаем путь к текущему файлу
file_path = inspect.getfile(inspect.currentframe())

# Открываем файл и читаем его содержимое
with open(file_path, 'r', encoding='utf-8') as file:
    code = file.read()

# Выводим содержимое файла
print(code)
