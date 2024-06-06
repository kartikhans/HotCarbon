import concurrent.futures
import os
import time
from datetime import datetime

def sieve_of_eratosthenes(n):
    is_prime = [True] * (n + 1)
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    return [p for p in range(2, n + 1) if is_prime[p]]

if __name__ == "__main__":
    n = 10**8  # Find primes up to this number
    print(datetime.now())
    num_workers = 8
    print(f"Using {num_workers} workers out of {os.cpu_count()} available cores.")

    start_time = time.time()

    chunk_size = n // num_workers
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_workers)]
    if n % num_workers != 0:
        ranges.append((num_workers * chunk_size, n))

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(sieve_of_eratosthenes, end) for start, end in ranges]
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())

    results = sorted(set(results))
    end_time = time.time()
    print(datetime.now())

    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Number of primes found: {len(results)}")

