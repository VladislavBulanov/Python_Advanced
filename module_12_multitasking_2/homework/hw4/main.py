import datetime
import logging
import threading
import time
from multiprocessing import Queue
from typing import Optional, List, Dict

import requests


URL: str = "http://127.0.0.1:8080/timestamp/{}"
WORKERS_COUNT: int = 10
WORKER_REQUESTS: int = 20

queue: Queue = Queue(WORKERS_COUNT * WORKER_REQUESTS)
data: Dict[float, Optional[str]] = {}


class Worker(threading.Thread):
    """The child class of 'threading.Thread'
    class describing the one thread."""

    def run(self) -> None:
        for _ in range(WORKER_REQUESTS):
            timestamp: float = datetime.datetime.now().timestamp()
            data[timestamp] = None

            queue.put(timestamp)
            date: str = get_date(timestamp)
            data[timestamp] = date

            time.sleep(1)


def get_date(timestamp: float) -> str:
    """
    The function returns date by specified timestamp.
    :param timestamp: the source timestamp
    """

    return requests.get(URL.format(timestamp)).text


def main() -> None:
    """The main function of the app."""

    logging.basicConfig(
        level='INFO',
        filename='sorted_logs.log',
        format='%(asctime)s | %(message)s',
    )

    threads: List[Worker] = []

    for _ in range(WORKERS_COUNT):
        thread: Worker = Worker()
        thread.start()
        threads.append(thread)
        time.sleep(1)

    for _ in range(queue.qsize()):
        timestamp: float = queue.get()
        while data.get(timestamp) is None:
            continue
        logging.info(f'{timestamp} -- {data[timestamp]}')

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
