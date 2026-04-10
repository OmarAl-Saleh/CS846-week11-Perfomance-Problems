from typing import List, Tuple


def min_path_cost(grid: List[List[int]]) -> int:
    """
    Problem 1:
    Return the minimum cost path from top-left to bottom-right
    moving only right or down.
    """
    rows = len(grid)
    cols = len(grid[0])

    def solve(r: int, c: int) -> int:
        if r == rows - 1 and c == cols - 1:
            return grid[r][c]

        best = float("inf")

        if r + 1 < rows:
            best = min(best, grid[r][c] + solve(r + 1, c))

        if c + 1 < cols:
            best = min(best, grid[r][c] + solve(r, c + 1))

        return best

    return solve(0, 0)


# def search_documents(documents: List[str], query: str) -> List[int]:
#     """
#     Problem 2:
#     Return indices of documents that contain all terms in the query.

#     """
#     query_terms = query.lower().split()
#     result = []

#     for index, doc in enumerate(documents):
#         words = doc.lower().split()
#         if all(term in words for term in query_terms):
#             result.append(index)

#     return result

def search_documents(documents: List[str], query: str) -> List[int]:
    """
    Problem 2:
    Return indices of documents that contain all terms in the query.
    """
    query_terms = query.lower().split()
    result = []

    for index, doc in enumerate(documents):
        matched_all = True

        for term in query_terms:
            words = doc.lower().split()
            if term not in words:
                matched_all = False
                break

        if matched_all:
            result.append(index)

    return result



def count_target_submatrices(matrix: List[List[int]], target: int) -> int:
    """
    Problem 3:
    Count the number of submatrices whose sum equals target.

    """
    rows = len(matrix)
    cols = len(matrix[0])
    count = 0

    for r1 in range(rows):
        for c1 in range(cols):
            for r2 in range(r1, rows):
                for c2 in range(c1, cols):
                    total = 0
                    for r in range(r1, r2 + 1):
                        for c in range(c1, c2 + 1):
                            total += matrix[r][c]
                    if total == target:
                        count += 1

    return count


def answer_reachability_queries(
    num_courses: int,
    prerequisites: List[Tuple[int, int]],
    queries: List[Tuple[int, int]],
) -> List[bool]:
    """
    Problem 4:
    For each query (src, dst), return whether dst is reachable from src.

    """
    graph = {i: [] for i in range(num_courses)}
    for src, dst in prerequisites:
        graph[src].append(dst)

    def can_reach(start: int, target: int) -> bool:
        stack = [start]
        visited = set()

        while stack:
            node = stack.pop()
            if node == target:
                return True

            if node in visited:
                continue

            visited.add(node)
            for nxt in graph[node]:
                stack.append(nxt)

        return False

    return [can_reach(src, dst) for src, dst in queries]