from functools import reduce
from queue import Queue
import random
import math
import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import threading


def show_results(n: int, pi: float) -> None:
    print(f"No of iterations: {n:n}")
    print(f"Pi: {pi}")
    print(f"Accuracy: {(abs(math.pi - pi) / math.pi) * 100}%")


def show_elapsed_time(start: float, end: float) -> None:
    print(f"Elapsed time: {end - start}s")

#############################################################################


def calculate_hits(n: int) -> int:
    rnd = random.Random()
    rnd.seed(threading.current_thread().native_id)
    hits = 0
    for i in range(n):
        x = rnd.random()
        y = rnd.random()
        if (x * x + y * y <= 1.0):
            hits += 1
    return hits

#############################################################################


def monte_carlo_pi_single_thread(n: int) -> float:
    hits = calculate_hits(n)
    mc_pi = (hits / n) * 4
    return mc_pi

#############################################################################


def monte_carlo_pi_multithreading(n: int) -> float:
    threads_count = mp.cpu_count()
    n_per_thread = n // threads_count
    args = [n_per_thread for _ in range(threads_count)]

    with ThreadPoolExecutor(max_workers=threads_count) as executor:
        hits = executor.map(calculate_hits, args)

    mc_pi = (sum(hits) / n) * 4
    return mc_pi

#############################################################################


def monte_carlo_pi_multiprocessing(n: int) -> float:
    threads_count = mp.cpu_count()
    n_per_thread = n // threads_count
    args = [n_per_thread for _ in range(threads_count)]

    with ProcessPoolExecutor(max_workers=threads_count) as executor:
        hits = executor.map(calculate_hits, args)

    mc_pi = (sum(hits) / n) * 4
    return mc_pi


#############################################################################

if __name__ == "__main__":
    n = 1200000000
    print(f"CPU count: {mp.cpu_count()}")

    start = time.perf_counter()
    mc_pi = monte_carlo_pi_single_thread(n)
    end = time.perf_counter()
    show_results(n, mc_pi)
    show_elapsed_time(start, end)

    print("-" * 40)

    start = time.perf_counter()
    mc_pi = monte_carlo_pi_multithreading(n)
    end = time.perf_counter()
    show_results(n, mc_pi)
    show_elapsed_time(start, end)

    print("-" * 40)

    start = time.perf_counter()
    mc_pi = monte_carlo_pi_multiprocessing(n)
    end = time.perf_counter()
    show_results(n, mc_pi)
    show_elapsed_time(start, end)
