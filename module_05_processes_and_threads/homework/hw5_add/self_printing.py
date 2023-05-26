import inspect


result = 0
for n in range(1, 11):
    result += n ** 2


# Get path to the current file:
file_path = inspect.getfile(inspect.currentframe())

with open(file_path, 'r', encoding='utf-8') as file:
    code = file.read()

print(code)
