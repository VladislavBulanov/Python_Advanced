import subprocess

def process_count(username: str) -> int:
    # Количество процессов, запущенных из-под текущего пользователя username
    command = f'ps -u {username} -o pid --no-headers | wc -l'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    count = int(result.stdout.strip())
    return count

def total_memory_usage(root_pid: int) -> float:
    # Суммарное потребление памяти древа процессов с корнем root_pid в процентах
    command = f'pgrep -P {root_pid} | xargs ps -o rss --no-headers | awk \'{{sum+=$1}} END {{print sum}}\''
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    memory_usage = float(result.stdout.strip())
    return memory_usage
