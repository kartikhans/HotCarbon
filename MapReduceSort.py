import time
import random
from multiprocessing import Pool
import heapq
from datetime import datetime


def generate_random_list(size):
    return random.sample(range(size), size)


class MapReduceSort:
    def __init__(self, data_size, chunk_size, num_processes):
        self.chunk_size = chunk_size
        self.data = generate_random_list(data_size)
        self.num_processes = num_processes

    def mapper(self, chunk):
        return sorted(chunk)

    def reducer(self, sorted_chunks):
        merged_data = heapq.merge(*sorted_chunks)
        return list(merged_data)

    def map_reducer(self):
        chunks = [self.data[i: i + self.chunk_size] for i in range(0, len(self.data), self.chunk_size)]

        with Pool(self.num_processes) as pool:
            sorted_chunks = pool.map(self.mapper, chunks)

        return self.reducer(sorted_chunks)


if __name__ == '__main__':
    print(datetime.now())
    start_time = time.time()

    chunk_size = 10

    num_processes = 4

    sorted_data = MapReduceSort(data_size=5000000, chunk_size=chunk_size, num_processes=num_processes).map_reducer()

    print(time.time() - start_time)
    print(datetime.now())