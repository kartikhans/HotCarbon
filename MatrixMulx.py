import random
import time
from datetime import datetime


def generate_random_number():
    return random.randint(1, 100)


class MatrixMulx:
    def __init__(self, n):
        self.matrixB = None
        self.matrixA = None
        self.n = n
        self.result = None

    def create_matrix(self):
        self.matrixA = [[0 for i in range(self.n)] for j in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                self.matrixA[i][j] = generate_random_number()

        self.matrixB = [[0 for i in range(self.n)] for j in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                self.matrixB[i][j] = generate_random_number()

        self.result = [[0 for i in range(self.n)] for j in range(self.n)]

    def multiply(self):
        # iterate through rows of X
        self.create_matrix()
        for i in range(self.n):
            # iterate through columns of Y
            for j in range(self.n):
                # iterate through rows of Y
                for k in range(self.n):
                    self.result[i][j] += self.matrixA[i][k] * self.matrixB[k][j]

    def execute(self):
        start_time = time.time()
        self.multiply()
        print(time.time() - start_time)


if __name__ == '__main__':
    print(datetime.now())
    instance = MatrixMulx(800)
    instance.execute()
    print(datetime.now())
