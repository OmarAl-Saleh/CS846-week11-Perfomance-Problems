import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.baselines.baseline_A1 import (
    baseline_first_unique_value,
    baseline_count_subarrays_equal_k,
)

from Problem_A.A1.array_bruteforce import (
    first_unique_value,
    count_subarrays_equal_k,
)

from utils.performance_utils import (
    evaluate_performance_static_speedup,
    color,
    C,
)

# Correctness tests


def test_a1_correctness():
    cases = [
        ([2, 3, 2, 4, 4], 3),
        ([1, 1, 2, 2, 3], 3),
        ([7, 7, 7], -1),
        ([5], 5),
        ([9, 8, 8, 9, 10], 10),
        ([4, 5, 4, 6, 5, 7, 6], 7),
    ]

    for nums, expected in cases:
        assert first_unique_value(nums) == expected

    print(color("A_1 correctness passed.", C.GREEN))


def test_a2_correctness():
    cases = [
        (([1, 1, 1], 2), 2),
        (([1, 2, 3], 3), 2),
        (([1, -1, 0], 0), 3),
        (([0, 0, 0], 0), 6),
        (([5], 5), 1),
        (([3, 4, 7, 2, -3, 1, 4, 2], 7), 4),
    ]

    for (nums, k), expected in cases:
        assert count_subarrays_equal_k(nums, k) == expected

    print(color("A_2 correctness passed.", C.GREEN))


# Static performance datasets

A1_PERF_DATA = [i % 250 for i in range(12000)] + [9999991]

A2_PERF_DATA = (
    ([3, -1, 2, 5, -2, 4, -3, 1, 2, -4] * 140),
    5,
)


# Static target speedups

A1_TARGET_SPEEDUP = 1150.84
A2_TARGET_SPEEDUP = 11061.60


# Performance evaluation

def run_a1_performance():
    evaluate_performance_static_speedup(
        problem_name="A_1 - First Unique Value",
        baseline_func=baseline_first_unique_value,
        student_func=first_unique_value,
        args=(A1_PERF_DATA,),
        target_speedup=A1_TARGET_SPEEDUP,
        repeats=3,
    )


def run_a2_performance():
    nums, k = A2_PERF_DATA
    evaluate_performance_static_speedup(
        problem_name="A_2 - Count Subarrays Equal to K",
        baseline_func=baseline_count_subarrays_equal_k,
        student_func=count_subarrays_equal_k,
        args=(nums, k),
        target_speedup=A2_TARGET_SPEEDUP,
        repeats=3,
    )


if __name__ == "__main__":
    print(color("\nRunning Problem A tests...", C.BOLD + C.CYAN))
    test_a1_correctness()
    run_a1_performance()

    test_a2_correctness()
    run_a2_performance()