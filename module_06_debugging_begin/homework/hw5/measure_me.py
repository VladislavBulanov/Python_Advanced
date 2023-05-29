import json
import logging
import random
from datetime import datetime
from typing import List


class JsonAdapter(logging.LoggerAdapter):
    """The class for create an instance of LoggerAdapter
    initialized with an underlying Logger instance
    and a dict-like object."""

    def process(self, message, kwargs):
        """
        Modifies the message and/or keyword arguments
        passed to a logging call in order to insert
        contextual information.
        :param message: source message
        :param kwargs: kwargs
        :return: JSON-message
        """
        json_message = json.dumps(message)
        return json_message, kwargs


def get_data_line(sz: int) -> List[int]:
    try:
        logger.debug("Enter get_data_line")
        return [random.randint(-(2 ** 31), 2 ** 31 - 1) for _ in range(sz)]
    finally:
        logger.debug("Leave get_data_line")


def measure_me(nums: List[int]) -> List[List[int]]:
    logger.info("Enter measure_me")
    results = []
    nums.sort()

    for i in range(len(nums) - 2):
        logger.debug(f"Iteration {i}")
        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    logger.debug(f"Found {target}")
                    results.append([nums[i], nums[left], nums[right]])
                    logger.debug(
                        f"Appended {[nums[i], nums[left], nums[right]]} to result"
                    )
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    logger.debug(f"Increment left (left, right) = {left, right}")
                    left += 1
                else:
                    logger.debug(f"Decrement right (left, right) = {left, right}")

                    right -= 1

    logger.info("Leave measure_me")

    return results


def get_average_time_of_function_performing(filename='logs.log') -> float:
    """The function returns average time of function performing via logs."""

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            logs = [json.loads(line) for line in file]

    except FileNotFoundError:
        print("Source file doesn't exist")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(filename='logs.log', mode='w')
    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger = JsonAdapter(logger)

    for it in range(15):
        data_line = get_data_line(10 ** 3)
        measure_me(data_line)

    print(get_average_time_of_function_performing())
