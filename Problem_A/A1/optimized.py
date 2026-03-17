from typing import List


def first_unique_value(nums: List[int]) -> int:
    """
    Optimized A_1
    Return the first unique value in the list.
    If none exists, return -1.

    Time: O(n)
    Space: O(n)
    """
    freq = {}
    for value in nums:
        freq[value] = freq.get(value, 0) + 1

    for value in nums:
        if freq[value] == 1:
            return value

    return -1


def count_subarrays_equal_k(nums: List[int], k: int) -> int:
    """
    Optimized A_2
    Return the number of continuous subarrays whose sum equals k.

    Time: O(n)
    Space: O(n)
    """
    prefix_counts = {0: 1}
    prefix_sum = 0
    count = 0

    for value in nums:
        prefix_sum += value
        count += prefix_counts.get(prefix_sum - k, 0)
        prefix_counts[prefix_sum] = prefix_counts.get(prefix_sum, 0) + 1

    return count