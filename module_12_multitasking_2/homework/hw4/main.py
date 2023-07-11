import requests
import threading
import time
from queue import Queue
from typing import List


log_file_name: str = "logs.log"
logs_queue: Queue = Queue()
total_threads: int = 10
thread_life_seconds: int = 20


def work_thread(number: int) -> None:
    """
    The function describes the work of the one thread.
    :param number: the number of the thread
    """

    print(f"Thread {number} started")
    for _ in range(thread_life_seconds):
        current_timestamp = int(time.time())
        logs_queue.put(current_timestamp)
        time.sleep(1)
    print(f"Thread {number} finished")


def write_logs() -> None:
    """The function for writing logs to the file."""

    while not logs_queue.empty():
        timestamp = logs_queue.get()
        date = get_date_by_timestamp(timestamp)
        with open(log_file_name, "a", encoding="utf-8") as file:
            file.write(f"{timestamp} {date}\n")


def get_date_by_timestamp(src_timestamp: int) -> str:
    """
    The function returns current date by specified timestamp.
    :param src_timestamp: the current timestamp
    """

    url = f"http://127.0.0.1:8080/timestamp/{src_timestamp}"
    response = requests.get(url).text
    return response


def main() -> None:
    """The main function of the app."""

    writer_thread = threading.Thread(target=write_logs)
    writer_thread.start()

    threads: List[threading.Thread] = []
    for thread_number in range(1, total_threads + 1):
        thread = threading.Thread(target=work_thread, args=(thread_number,))
        thread.start()
        threads.append(thread)
        time.sleep(1)

    for thread in threads:
        thread.join()

    writer_thread.join()


if __name__ == "__main__":
    main()
