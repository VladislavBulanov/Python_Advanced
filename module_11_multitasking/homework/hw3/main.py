import logging
import random
import threading
import time
from typing import List

SELLERS_QUANTITY: int = 4
TOTAL_TICKETS: int = 10
SEATS_LEFT: int = 20  # Total capacity = TOTAL_TICKETS + SEATS_LEFT

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    """The child class of threading.Thread class describing the seller."""

    def __init__(
            self,
            semaphore: threading.Semaphore,
            director_event: threading.Event,
    ) -> None:
        """
        The class' constructor.
        :param semaphore: the semaphore of threading.Semaphore class
        :param director_event: the event to coordinate with the director
        """

        super().__init__()
        self.semaphore: threading.Semaphore = semaphore
        self.director_event: threading.Event = director_event
        self.tickets_sold: int = 0
        logger.info(f'Seller {self.name} started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.semaphore:
                if not TOTAL_TICKETS and not SEATS_LEFT:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
                if TOTAL_TICKETS <= SELLERS_QUANTITY:
                    # Notify the director to replenish tickets:
                    self.director_event.set()
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    @staticmethod
    def random_sleep() -> None:
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    """The child class of threading.Thread class describing the director."""

    def __init__(
            self,
            semaphore: threading.Semaphore,
            director_event: threading.Event,
    ) -> None:
        """
        The class' constructor.
        :param semaphore: the semaphore of threading.Semaphore class
        :param director_event: the event to coordinate with the director
        """

        super().__init__()
        self.semaphore: threading.Semaphore = semaphore
        self.director_event: threading.Event = director_event

    def run(self) -> None:
        global TOTAL_TICKETS, SEATS_LEFT
        while True:
            # Wait for the event triggered by sellers:
            self.director_event.wait()
            if SEATS_LEFT:
                # Calculate the number of tickets to replenish:
                tickets_to_replenish = random.randint(1, SEATS_LEFT)
                SEATS_LEFT -= tickets_to_replenish
                TOTAL_TICKETS += tickets_to_replenish
                logger.info(
                    f'Director replenished {tickets_to_replenish} '
                    f'tickets; {TOTAL_TICKETS} left'
                )
                self.director_event.clear()
            else:
                break


def main() -> None:
    """The main function of application."""

    semaphore: threading.Semaphore = threading.Semaphore()
    director_event: threading.Event = threading.Event()

    sellers: List[Seller] = []
    for _ in range(SELLERS_QUANTITY):
        seller = Seller(semaphore, director_event)
        seller.start()
        sellers.append(seller)

    director = Director(semaphore, director_event)
    director.start()

    for seller in sellers:
        seller.join()

    director.join()

    return


if __name__ == '__main__':
    main()
