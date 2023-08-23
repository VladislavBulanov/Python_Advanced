import requests
import time

# начальное время
start_time = time.time()

for i in range(100):
    response = requests.get('http://127.0.0.1:5000')

# конечное время
end_time = time.time()

# разница между конечным и начальным временем
elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)

# 0.32118701934814453 1.1
# 0.23755598068237305 disable 1.1
