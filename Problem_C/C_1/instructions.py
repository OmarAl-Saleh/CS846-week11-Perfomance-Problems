import random

random.seed(42)
numbers = [random.randint(1, 100000) for _ in range(1_000_000)]

# Find the difference between the smallest and largest numbers
# whose digits sum to 30.