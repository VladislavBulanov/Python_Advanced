import threading
import time
from typing import List
from random import randint
from queue import PriorityQueue


class Task:
    """The class describing a task."""

    def __init__(self, priority: int, id: int, description: str) -> None:
        """
        The class' constructor.
        :param priority: the specified priority of the task
        :param id: the ID of the task
        :param description: the description of the task
        """

        self.priority = priority
        self.id = id
        self.description = description

    def __lt__(self, other: "Task") -> bool:
        """
        Less-than comparison method for Task objects.
        This method compares the priority of two Task objects
        and determines if the current Task object has a lower
        priority than the other Task object.
        :param other: the other Task object to compare with
        """

        if self.priority == other.priority:
            return self.id < other.id
        return self.priority < other.priority


class Producer(threading.Thread):
    """The child class of 'threading.Thread' class
    describing the producer of the tasks."""

    def __init__(self, queue: PriorityQueue) -> None:
        """
        The class' constructor.
        :param queue: the instance of 'PriorityQueue' class
        """

        super().__init__()
        self.queue = queue

    def run(self):
        print("Producer: Running")

        tasks: List[Task] = [
            Task(0, 0, "Task_1"),
            Task(1, 1, "Task_2"),
            Task(0, 2, "Task_3"),
            Task(2, 3, "Task_4"),
            Task(1, 4, "Task_5"),
            Task(2, 5, "Task_6"),
            Task(3, 6, "Task_7"),
            Task(3, 7, "Task_8"),
            Task(4, 8, "Task_9"),
            Task(6, 9, "Task_10"),
        ]

        for task in tasks:
            self.queue.put(task)

        print("Producer: Done")


class Consumer(threading.Thread):
    """The child class of 'threading.Thread' class
    describing the consumer of the tasks."""

    def __init__(self, queue: PriorityQueue) -> None:
        """
        The class' constructor.
        :param queue: the instance of 'PriorityQueue' class
        """

        super().__init__()
        self.queue = queue

    def run(self):
        print("Consumer: Running")

        while not self.queue.empty():
            task = self.queue.get()

            time_sleep = randint(0, 1)
            print(
                f">running {task.description}(priority={task.priority})."
                f"\t\tsleep({time_sleep})"
            )
            time.sleep(time_sleep)

            self.queue.task_done()

        print("Consumer: Done")


def main() -> None:
    """The main function of the app."""

    queue = PriorityQueue()

    producer = Producer(queue)
    consumer = Consumer(queue)

    producer.start()
    consumer.start()
    consumer.join()
    producer.join()


if __name__ == "__main__":
    main()
