import concurrent.futures
import os
import time
from datetime import datetime


# A CPU-bound task: computing a large number of Fibonacci numbers
def compute_fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    # Number of Fibonacci numbers to compute (large enough to be CPU-intensive)
    start_time = time.time()
    print(datetime.now())
    n = 2000000

    # Determine the number of workers to use (half of the CPU cores)
    num_workers = 8
    print(f"Using {num_workers} workers out of {os.cpu_count()} available cores.")


    # Create a list of tasks to run in parallel
    tasks = [n] * num_workers

    # Execute the tasks in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(compute_fibonacci, tasks))

    end_time = time.time()
    print(datetime.now())
    print(f"Time taken: {end_time - start_time} seconds")
