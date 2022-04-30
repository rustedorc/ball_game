from typing import NamedTuple
from random import randint
from time import perf_counter
class Circle(NamedTuple):
    x: int
    y: int
    radius: int

def compute_colli_sqrt(c1: Circle, c2: Circle) -> bool:
    return ((((c1.x - c2.x) ** 2) + (c1.y - c2.y) ** 2) ** (1/2)) < (c1.radius + c2.radius)

def compute_colli_nsqrt(c1: Circle, c2: Circle) -> bool:
    return (((c1.x - c2.x) ** 2) + (c1.y - c2.y) ** 2) < ((c1.radius + c2.radius) ** 2)


def test_method():
    for _ in range(1000):
        num1, num2, num3, num4 = randint(0, 5), randint(0, 5), randint(0, 5), randint(0, 5)

        c1 = Circle(num1, num2, num3)
        c2 = Circle(num4, num3, num2)

        assert compute_colli_sqrt(c1, c2) is compute_colli_nsqrt(c1, c2)

def calc_sqrt_perf():
    items = [randint(1, 8) for _ in range(100_000_000)]
    start = perf_counter()
    for _ in range(1_000_000):
        c1 = Circle(items.pop(), items.pop(), items.pop())
        c2 = Circle(items.pop(), items.pop(), items.pop())
        compute_colli_sqrt(c1, c2)
    end = perf_counter()

    total = end - start
    print('SQRT')
    print(f'Total time = {total}\naverage time = {total / 1_000}')

def calc_nsqrt_perf():
    items = [randint(1, 8) for _ in range(100_000_000)]
    start = perf_counter()
    for _ in range(1_000_000):
        c1 = Circle(items.pop(), items.pop(), items.pop())
        c2 = Circle(items.pop(), items.pop(), items.pop())
        compute_colli_nsqrt(c1, c2)
    end = perf_counter()

    total = end - start
    print('NOT SQRT')
    print(f'Total time = {total}\naverage time = {total / 1_000}')



if __name__ == '__main__':
    calc_sqrt_perf()
    calc_nsqrt_perf()