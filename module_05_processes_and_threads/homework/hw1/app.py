import os
import signal
import subprocess
from shlex import quote
from typing import List

from flask import Flask

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    The function returns a list of PIDs of processes
    occupying the specified port.
    :param port: specified port
    """

    if not isinstance(port, int):
        raise ValueError

    pids: List[int] = []
    try:
        command: List[str] = ["lsof", "-t", "-i" f":{port}"]
        clear_command = [quote(element) for element in command]
        output = subprocess.check_output(clear_command)
        pids = [int(pid) for pid in output.decode().split("\n") if pid]
    except subprocess.CalledProcessError:
        pass

    return pids


def free_port(port: int) -> None:
    """
    The function terminates specified busy port.
    :param port: busy port
    """

    pids: List[int] = get_pids(port)
    for pid in pids:
        os.kill(pid, signal.SIGTERM)


def run(port: int) -> None:
    """
    The function runs Flask app on the specified port.
    If port is busy by some process the function terminates that process.
    Запускает flask-приложение по переданному порту.
    :param port: specified port
    """

    free_port(port)
    app.run(port=port)


if __name__ == '__main__':
    run(5000)
