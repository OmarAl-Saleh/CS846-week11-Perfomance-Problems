# Digit Sum Range Finder
#
# Given 1 million random integers between 1 and 100,000, find the difference
# between the smallest and largest numbers whose digits sum to 30.
# Optimize for performance.

import random
import time

random.seed(42)
numbers = [random.randint(1, 100000) for _ in range(1_000_000)]


def find_difference(numbers):
    # TODO: Implement your solution here
    pass


if __name__ == "__main__":
    start = time.perf_counter()
    result = find_difference(numbers)
    elapsed = time.perf_counter() - start

    print(f"Result: {result}")
    print(f"Time: {elapsed:.3f}s")
