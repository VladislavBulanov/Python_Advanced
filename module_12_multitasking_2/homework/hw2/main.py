import psutil
import subprocess


def process_count(username: str) -> int:
    """
    The function returns the quantity of
    processes running under specified user.
    :param username: the source username
    """

    command = f'ps -u {username} -o pid --no-headers | wc -l'
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    count = int(result.stdout.strip())
    return count


def total_memory_usage(src_root_pid: int) -> float:
    """
    The function returns the total memory consumption
    (in percent) of processes tree with root 'root_pid'.
    :param src_root_pid: the source root of processes tree
    """

    total_memory = psutil.virtual_memory().total
    command = f'pgrep -P {src_root_pid} | xargs ps -o rss --no-headers | awk \'{{sum+=$1}} END {{print sum}}\''
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    memory_usage = float(result.stdout.strip())
    memory_usage_percent = (memory_usage / total_memory) * 100
    return memory_usage_percent


if __name__ == "__main__":
    user = subprocess.run(
        'whoami', shell=True, capture_output=True, text=True
    ).stdout.strip()

    print("The quantity of processes running "
          f"under {user}: {process_count(user)}")

    root_pid = 1796
    memory = total_memory_usage(root_pid)
    print("Total memory usage for process tree with "
          f"root PID {root_pid}: {memory:.2f}%")
