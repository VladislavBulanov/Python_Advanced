import logging
import requests
import time


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='example_disable_1_1.log',
    filemode='a',
    format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
)

# начальное время
start_time = time.time()

for i in range(100):
    response = requests.get('http://127.0.0.1:5000')

# конечное время
end_time = time.time()

# разница между конечным и начальным временем
elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)
logger.info(f'Elapsed time: {elapsed_time}')

# 0.32118701934814453 1.1
# 0.23755598068237305 disable 1.1
