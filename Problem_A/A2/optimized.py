from typing import List, Tuple
from collections import defaultdict
from typing import List, Dict, Set


def min_path_cost(grid: List[List[int]]) -> int:
    """
    Problem 1:
    Minimum cost path from top-left to bottom-right
    moving only right or down.

    Strong canonical solution:
    - O(rows * cols) time
    - O(cols) extra space
    """
    rows = len(grid)
    cols = len(grid[0])

    dp = [0] * cols
    dp[0] = grid[0][0]

    for c in range(1, cols):
        dp[c] = dp[c - 1] + grid[0][c]

    for r in range(1, rows):
        row = grid[r]
        dp[0] += row[0]
        for c in range(1, cols):
            if dp[c - 1] < dp[c]:
                dp[c] = dp[c - 1] + row[c]
            else:
                dp[c] = dp[c] + row[c]

    return dp[-1]



def search_documents(documents: List[str], query: str) -> List[int]:
    """
    Problem 2:
    Return indices of documents that contain all terms in the query.
    """
    query_terms = set(query.lower().split())
    if not query_terms:
        return list(range(len(documents)))

    result = []

    for index, doc in enumerate(documents):
        words = set(doc.lower().split())
        if query_terms.issubset(words):
            result.append(index)

    return result


def count_target_submatrices(matrix: List[List[int]], target: int) -> int:
    """
    Problem 3:
    Count the number of submatrices whose sum equals target.

    Optimized:
    Compress rows and reduce to the 1D subarray-sum-equals-k problem.

    Time: O(rows^2 * cols)
    Space: O(cols)
    """
    rows = len(matrix)
    cols = len(matrix[0])
    count = 0

    for top in range(rows):
        col_sums = [0] * cols

        for bottom in range(top, rows):
            for c in range(cols):
                col_sums[c] += matrix[bottom][c]

            prefix_counts = {0: 1}
            prefix_sum = 0

            for value in col_sums:
                prefix_sum += value
                count += prefix_counts.get(prefix_sum - target, 0)
                prefix_counts[prefix_sum] = prefix_counts.get(prefix_sum, 0) + 1

    return count


def answer_reachability_queries(
    num_courses: int,
    prerequisites: List[Tuple[int, int]],
    queries: List[Tuple[int, int]],
) -> List[bool]:
    """
    Problem 4:
    For each query (src, dst), return whether dst is reachable from src.

    Optimized:
    Build graph once, then memoize reachability per start node.

    Good when many queries reuse the same source nodes.

    Time:
    - Graph build: O(E)
    - Each distinct source: O(V + E)
    - Query answering after that: O(1) membership check
    """
    graph = [[] for _ in range(num_courses)]
    for src, dst in prerequisites:
        graph[src].append(dst)

    reachable_cache = {}

    def compute_reachable(start: int) -> set[int]:
        if start in reachable_cache:
            return reachable_cache[start]

        visited = set()
        stack = [start]

        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt not in visited:
                    visited.add(nxt)
                    stack.append(nxt)

        reachable_cache[start] = visited
        return visited

    return [dst in compute_reachable(src) for src, dst in queries]