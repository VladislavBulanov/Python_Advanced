import json
import subprocess
from collections import Counter
from typing import Dict


with open('skillbox_json_messages.log', 'r') as file:
    logs = [json.loads(line) for line in file]


def task_1_calculate_message_quantity_of_each_level() -> Dict[str, int]:
    """The function returns dictionary with levels as keys
    and quantity of messages of each level as values."""

    levels_count = dict(Counter(log['level'] for log in logs))
    return levels_count


def task_2_get_hour_with_max_number_of_logs() -> int:
    """The function returns value of hour when quantity of logs was maximum."""

    logs_by_hour = Counter(log['time'][:2] for log in logs)
    max_hour = max(logs_by_hour, key=logs_by_hour.get)
    return max_hour


def task_3_get_quantity_of_critical_logs_in_specified_period() -> int:
    """The function returns quantity
    of critical logs in specified period."""

    critical_logs_count = sum(
        1 for log in logs if log['level'] == 'CRITICAL' and
        '05:00:00' <= log['time'] <= '05:20:00'
    )
    return critical_logs_count


def task_4_get_quantity_of_dog_word() -> int:
    """The function returns quantity of word 'dog' in log messages."""

    command = ['grep', '-c', '-i', 'dog', 'skillbox_json_messages.log']
    result = subprocess.Popen(command, stdout=subprocess.PIPE)
    logs_with_dog = int(result.communicate()[0].decode('utf-8').strip())
    return logs_with_dog


# # Without 'grep':
# def task_4_get_quantity_of_dog_word() -> int:
#     """The function returns quantity of word 'dog' in log messages."""
#
#     logs_with_dog = sum(1 for log in logs if 'dog' in log['message'])
#     return logs_with_dog


def task_5_get_the_most_common_word_in_warning_logs() -> str:
    """The function returns the most common word in warning logs."""

    warning_messages = [
        log['message'].lower().split()
        for log in logs
        if log['level'] == 'WARNING'
    ]
    warning_words = [word for words in warning_messages for word in words]
    most_common_word = Counter(warning_words).most_common(1)[0][0]
    return most_common_word


if __name__ == '__main__':
    tasks = (
        task_1_calculate_message_quantity_of_each_level,
        task_2_get_hour_with_max_number_of_logs,
        task_3_get_quantity_of_critical_logs_in_specified_period,
        task_4_get_quantity_of_dog_word,
        task_5_get_the_most_common_word_in_warning_logs,
    )
    for index, task_function in enumerate(tasks, 1):
        task_answer = task_function()
        print(f'{index}. {task_answer}')
