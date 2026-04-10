import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.baselines.baseline_A2 import (
    baseline_min_path_cost,
    baseline_search_documents,
    baseline_count_target_submatrices,
    baseline_answer_reachability_queries,
)

from Problem_A.A2.grid_matrix_graph_search import (
    min_path_cost,
    search_documents,
    count_target_submatrices,
    answer_reachability_queries,
)

from utils.performance_utils import (
    evaluate_performance_static_speedup,
    color,
    C,
)



# Helper

def fail_correctness(problem_label, input_data, expected, got):
    print(color(f"\n{problem_label} correctness FAILED ❌", C.RED))
    print(f"Input   : {input_data}")
    print(f"Expected: {expected}")
    print(f"Got     : {got}")
    return False



# Correctness tests


def test_problem_1_correctness():
    cases = [
        ([[1]], 1),
        ([[1, 2], [1, 1]], 3),
        ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
        ([[5, 1, 3], [2, 8, 2], [4, 1, 1]], 12),
    ]

    for grid, expected in cases:
        result = min_path_cost(grid)
        if result != expected:
            return fail_correctness(
                "Problem 1",
                grid,
                expected,
                result,
            )

    print(color("Problem 1 correctness passed. ✓", C.GREEN))
    return True


def test_problem_2_correctness():
    docs = [
        "python data search engine",
        "graph tree hash array",
        "python token query document",
        "system network path cost",
        "python data token query search",
    ]

    cases = [
        ((docs, "python data"), [0, 4]),
        ((docs, "graph hash"), [1]),
        ((docs, "query token"), [2, 4]),
        ((docs, "memory cache"), []),
    ]

    for (documents, query), expected in cases:
        result = search_documents(documents, query)
        if result != expected:
            return fail_correctness(
                "Problem 2",
                {"query": query, "documents_count": len(documents)},
                expected,
                result,
            )

    print(color("Problem 2 correctness passed. ✓", C.GREEN))
    return True

def test_problem_2_mutation_correctness():
    docs = [
        "python data search engine",
        "graph tree hash array",
        "python token query document",
    ]

    # First call
    result1 = search_documents(docs, "python")
    if result1 != [0, 2]:
        return fail_correctness(
            "Problem 2 Mutation",
            {"step": "initial"},
            [0, 2],
            result1,
        )

    # Mutate documents
    docs[0] = "memory cache window sum"

    # Second call MUST reflect change
    result2 = search_documents(docs, "python")
    if result2 != [2]:
        return fail_correctness(
            "Problem 2 Mutation",
            {"step": "after mutation"},
            [2],
            result2,
        )

    print(color("Problem 2 mutation correctness passed. ✓", C.GREEN))
    return True


def test_problem_3_correctness():
    cases = [
        (
            [
                [1, -1],
                [-1, 1],
            ],
            0,
            5,
        ),
        (
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0],
            ],
            0,
            4,
        ),
        (
            [[1]],
            1,
            1,
        ),
    ]

    for matrix, target, expected in cases:
        result = count_target_submatrices(matrix, target)
        if result != expected:
            return fail_correctness(
                "Problem 3",
                {"matrix": matrix, "target": target},
                expected,
                result,
            )

    print(color("Problem 3 correctness passed. ✓", C.GREEN))
    return True


def test_problem_4_correctness():
    num_courses = 5
    prerequisites = [(0, 1), (1, 2), (2, 3), (0, 4)]
    queries = [(0, 3), (1, 4), (0, 4), (2, 3), (4, 3)]

    expected = [True, False, True, True, False]
    result = answer_reachability_queries(num_courses, prerequisites, queries)

    if result != expected:
        return fail_correctness(
            "Problem 4",
            {
                "num_courses": num_courses,
                "prerequisites": prerequisites,
                "queries": queries,
            },
            expected,
            result,
        )

    print(color("Problem 4 correctness passed. ✓", C.GREEN))
    return True



# Static performance datasets


GRID_PERF_DATA = [
    [3, 1, 4, 2, 8, 6, 7, 5, 2, 1],
    [5, 9, 2, 1, 3, 4, 8, 7, 6, 2],
    [8, 6, 1, 5, 2, 9, 4, 3, 7, 1],
    [4, 2, 7, 3, 6, 1, 5, 8, 9, 2],
    [9, 5, 3, 8, 1, 7, 2, 6, 4, 3],
    [6, 8, 5, 4, 7, 2, 1, 9, 3, 4],
    [7, 3, 8, 6, 4, 5, 9, 1, 2, 5],
    [2, 4, 9, 7, 5, 3, 6, 2, 8, 6],
    [1, 7, 6, 9, 8, 4, 3, 5, 1, 7],
    [5, 2, 4, 1, 9, 8, 7, 6, 3, 2],
]

DOCUMENTS_PERF = [
    "python data search engine graph tree hash array token query document system",
    "network path cost window sum cache memory python graph search token query",
    "array graph path tree token query search engine memory data system hash",
    "python python data data token token query query search search engine engine",
] * 1500

QUERY_PERF = "python data token query"

MATRIX_PERF = [
    [1, -1, 2, 0, 3, -2, 1, 4, -1, 2],
    [0, 2, -2, 1, -1, 3, 2, -3, 0, 1],
    [3, 1, -1, 2, -2, 0, 4, 1, -3, 2],
    [2, 0, 1, -1, 3, -2, 2, 1, 0, -1],
    [-1, 3, 2, 0, 1, -3, 4, 2, -2, 1],
    [1, -2, 0, 3, 2, 1, -1, 0, 2, 3],
    [2, 1, -3, 4, 0, 2, 1, -2, 3, 0],
    [0, 2, 1, -1, 3, 4, -2, 1, 0, 2],
    [1, 0, 3, -2, 2, 1, -1, 4, 2, -3],
    [2, -1, 1, 0, 4, -2, 3, 1, -1, 2],
]
MATRIX_TARGET = 3

COURSE_COUNT = 220
PREREQUISITES_PERF = [(i, i + 1) for i in range(COURSE_COUNT - 1)]
PREREQUISITES_PERF += [(i, i + 2) for i in range(COURSE_COUNT - 2)]
PREREQUISITES_PERF += [(i, i + 5) for i in range(COURSE_COUNT - 5)]
QUERIES_PERF = [(0, COURSE_COUNT - 1)] * 3000 + [(10, 150)] * 2000 + [(20, 90)] * 1500



# Static target speedups


PROBLEM_1_TARGET_SPEEDUP = 6221.64
PROBLEM_2_TARGET_SPEEDUP = 1.18
PROBLEM_3_TARGET_SPEEDUP = 23.62
PROBLEM_4_TARGET_SPEEDUP = 55.94


# =========================================================
# Performance evaluation
# =========================================================

def run_problem_1_performance():
    evaluate_performance_static_speedup(
        problem_name="Problem 1 - Grid Minimum Path Cost",
        baseline_func=baseline_min_path_cost,
        student_func=min_path_cost,
        args=(GRID_PERF_DATA,),
        target_speedup=PROBLEM_1_TARGET_SPEEDUP,
        repeats=3,
    )


def run_problem_2_performance():
    evaluate_performance_static_speedup(
        problem_name="Problem 2 - Document Search",
        baseline_func=baseline_search_documents,
        student_func=search_documents,
        args=(DOCUMENTS_PERF, QUERY_PERF),
        target_speedup=PROBLEM_2_TARGET_SPEEDUP,
        repeats=3,
    )


def run_problem_3_performance():
    evaluate_performance_static_speedup(
        problem_name="Problem 3 - Target Submatrix Count",
        baseline_func=baseline_count_target_submatrices,
        student_func=count_target_submatrices,
        args=(MATRIX_PERF, MATRIX_TARGET),
        target_speedup=PROBLEM_3_TARGET_SPEEDUP,
        repeats=3,
    )


def run_problem_4_performance():
    evaluate_performance_static_speedup(
        problem_name="Problem 4 - Course Reachability Queries",
        baseline_func=baseline_answer_reachability_queries,
        student_func=answer_reachability_queries,
        args=(COURSE_COUNT, PREREQUISITES_PERF, QUERIES_PERF),
        target_speedup=PROBLEM_4_TARGET_SPEEDUP,
        repeats=3,
    )


if __name__ == "__main__":
    print(color("\nRunning A2 tests...", C.BOLD + C.CYAN))

    if not test_problem_1_correctness():
        sys.exit(1)
    run_problem_1_performance()

    if not test_problem_2_correctness():
        sys.exit(1)
    run_problem_2_performance()

    if not test_problem_2_mutation_correctness():
        sys.exit(1)
    

    if not test_problem_3_correctness():
        sys.exit(1)
    run_problem_3_performance()

    if not test_problem_4_correctness():
        sys.exit(1)
    run_problem_4_performance()