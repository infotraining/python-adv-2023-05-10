import threading
import time
from typing import Callable

total = 0
lock_total = threading.Lock()

def unsafe_increment(n: int, barrier: threading.Barrier) -> None:
    global total
    barrier.wait()
    for i in range(n):
        total += 1


def safe_increment(n: int, barrier: threading.Barrier) -> None:
    global total
    barrier.wait()
    for i in range(n):
        lock_total.acquire()
        total += 1
        lock_total.release()


def run_in_threads(thread_count: int, func: Callable) -> None:
    threads = [threading.Thread(target=func) for i in range(thread_count)]
    global total
    total = 0
    print(f'Starting {thread_count} threads...')

    begin = time.time()
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.time()

    print(f'finished in {end-begin}s.\ntotal: {total}')


if __name__ == "__main__":
    no_of_threads = 100
    n = 100000
    barrier = threading.Barrier(no_of_threads)


    run_in_threads(no_of_threads, lambda : unsafe_increment(n, barrier))

    run_in_threads(no_of_threads, lambda : safe_increment(n, barrier))
