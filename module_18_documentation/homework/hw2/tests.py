import logging
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Tuple, Callable, Optional


BASE_URL: str = "http://127.0.0.1:5000/api/books"
AMOUNT_OF_REQUESTS: Tuple[int] = (10, 100, 1000)


class RequestPerformanceTester:
    """A class for testing performance of HTTP requests by different ways."""

    def __init__(self, url: str, src_logger: logging.Logger) -> None:
        """The class constructor."""
        self.url = url
        self.logger = src_logger

    def measure_performance(
            self,
            request_amounts: Tuple[int],
            use_session: bool = False,
            use_parallel: bool = False,
    ) -> None:
        """
        The function measures time of performance of specified quantity of
        requests by specified way (with/without using session, with/without
        using threads), displays and logs it to logfile.
        :param request_amounts: a collection with amounts of requests
        :param use_session: determines if session will be used or not
        :param use_parallel: determines if threads will be used or not
        """

        # Choose type of requests: with the using session or not:
        request_function: Callable = (
            self._send_request_with_session
            if use_session else self._send_request
        )

        # Determine if threads will be used or not:
        executor: Optional[ThreadPoolExecutor] = (
            ThreadPoolExecutor() if use_parallel else None
        )

        for requests_qty in request_amounts:
            method_name = "parallel" if use_parallel else "sequential"
            if use_session:
                method_name += " with session"

            self.logger.info(
                f"==========START {method_name.upper()} REQUESTING=========="
            )
            start_time = datetime.now()

            if use_parallel:
                futures = [
                    executor.submit(request_function)
                    for _ in range(requests_qty)
                ]
                for future in futures:
                    future.result()
            else:
                for _ in range(requests_qty):
                    request_function()

            finish_time = datetime.now()
            elapsed_time = finish_time - start_time
            result = (
                f"Result time of performing {requests_qty} "
                f"{method_name} requests is {elapsed_time}"
            )
            self.logger.info(result)
            print(result)

    def _send_request(self) -> None:
        """Method for sending request without session."""
        requests.get(self.url)

    def _send_request_with_session(self) -> None:
        """Method for sending request via session."""
        with requests.Session() as session:
            session.get(self.url)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename='tests.log',
        filemode='a',
        format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG,
    )

    tester = RequestPerformanceTester(BASE_URL, logger)

    tester.measure_performance(AMOUNT_OF_REQUESTS)
    tester.measure_performance(AMOUNT_OF_REQUESTS, use_session=True)
    tester.measure_performance(AMOUNT_OF_REQUESTS, use_parallel=True)
    tester.measure_performance(
        AMOUNT_OF_REQUESTS,
        use_session=True,
        use_parallel=True,
    )
