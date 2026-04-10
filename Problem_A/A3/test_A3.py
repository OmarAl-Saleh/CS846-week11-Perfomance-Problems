import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.baselines.baseline_A3 import (
    baseline_find_route,
    baseline_process_route_batch,
    baseline_top_congested_roads,
    baseline_delivery_schedule_cost,
)

from Problem_A.A3.traffic_routing_simulator import (
    find_route,
    process_route_batch,
    top_congested_roads,
    delivery_schedule_cost,
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


# =========================================================
# Small correctness dataset
# =========================================================

SMALL_NETWORK = {
    "nodes": [0, 1, 2, 3],
    "roads": [
        {"road_id": "r01", "source": 0, "target": 1, "base_travel_time": 2, "capacity": 10},
        {"road_id": "r12", "source": 1, "target": 2, "base_travel_time": 2, "capacity": 10},
        {"road_id": "r23", "source": 2, "target": 3, "base_travel_time": 1, "capacity": 10},
        {"road_id": "r02", "source": 0, "target": 2, "base_travel_time": 10, "capacity": 10},
        {"road_id": "r13", "source": 1, "target": 3, "base_travel_time": 5, "capacity": 10},
        {"road_id": "r03", "source": 0, "target": 3, "base_travel_time": 20, "capacity": 10},
    ],
}

SMALL_UPDATES = [
    {"tick": 2, "road_id": "r12", "close_road": True},
]

SMALL_REQUEST = {
    "request_id": "q1",
    "start": 0,
    "end": 3,
    "departure_tick": 0,
}

SMALL_REQUEST_AFTER_UPDATE = {
    "request_id": "q2",
    "start": 0,
    "end": 3,
    "departure_tick": 3,
}

SMALL_BATCH_REQUESTS = [
    {"request_id": "b1", "start": 0, "end": 3, "departure_tick": 0},
    {"request_id": "b2", "start": 0, "end": 2, "departure_tick": 0},
    {"request_id": "b3", "start": 1, "end": 3, "departure_tick": 0},
]

SMALL_DELIVERY_GROUPS = [
    {"depot": 0, "stops": [2, 3], "departure_tick": 0},
]


# =========================================================
# Correctness tests
# =========================================================

def test_problem_1_correctness():
    result = find_route(SMALL_NETWORK, SMALL_REQUEST, [])
    expected = {
        "reachable": True,
        "cost": 5.0,
        "road_ids": ["r01", "r12", "r23"],
        "path_nodes": [0, 1, 2, 3],
    }

    got = {
        "reachable": result["reachable"],
        "cost": float(result["cost"]),
        "road_ids": result["road_ids"],
        "path_nodes": result["path_nodes"],
    }

    if got != expected:
        return fail_correctness("Problem 1", SMALL_REQUEST, expected, got)

    result_after = find_route(SMALL_NETWORK, SMALL_REQUEST_AFTER_UPDATE, SMALL_UPDATES)
    expected_after = {
        "reachable": True,
        "cost": 7.0,
        "road_ids": ["r01", "r13"],
        "path_nodes": [0, 1, 3],
    }

    got_after = {
        "reachable": result_after["reachable"],
        "cost": float(result_after["cost"]),
        "road_ids": result_after["road_ids"],
        "path_nodes": result_after["path_nodes"],
    }

    if got_after != expected_after:
        return fail_correctness("Problem 1", SMALL_REQUEST_AFTER_UPDATE, expected_after, got_after)

    print(color("Problem 1 correctness passed. ✓", C.GREEN))
    return True


def test_problem_2_correctness():
    result = process_route_batch(SMALL_NETWORK, SMALL_BATCH_REQUESTS, [])
    expected = {
        "processed_requests": 3,
        "reachable_count": 3,
        "unreachable_count": 0,
        "total_cost": 12.0,
        "average_cost": 4.0,
        "longest_path_hops": 3,
    }

    comparable = {
        "processed_requests": result["processed_requests"],
        "reachable_count": result["reachable_count"],
        "unreachable_count": result["unreachable_count"],
        "total_cost": float(result["total_cost"]),
        "average_cost": float(result["average_cost"]),
        "longest_path_hops": result["longest_path_hops"],
    }

    if comparable != expected:
        return fail_correctness("Problem 2", SMALL_BATCH_REQUESTS, expected, comparable)

    print(color("Problem 2 correctness passed. ✓", C.GREEN))
    return True


def test_problem_3_correctness():
    result = top_congested_roads(SMALL_NETWORK, SMALL_BATCH_REQUESTS, [], top_k=2)
    expected = ["r12", "r01"]

    if result != expected:
        return fail_correctness("Problem 3", {"top_k": 2, "requests": SMALL_BATCH_REQUESTS}, expected, result)

    print(color("Problem 3 correctness passed. ✓", C.GREEN))
    return True


def test_problem_4_correctness():
    result = delivery_schedule_cost(SMALL_NETWORK, SMALL_DELIVERY_GROUPS, [])
    expected = 5.0

    if float(result) != expected:
        return fail_correctness("Problem 4", SMALL_DELIVERY_GROUPS, expected, result)

    print(color("Problem 4 correctness passed. ✓", C.GREEN))
    return True

# =========================================================
# Deterministic large performance datasets
# Tuned down so the baseline still completes on student machines
# =========================================================

def build_perf_network():
    node_count = 220
    nodes = list(range(node_count))
    roads = []

    for i in range(node_count - 1):
        roads.append(
            {
                "road_id": f"chain_{i}",
                "source": i,
                "target": i + 1,
                "base_travel_time": 2 + (i % 3),
                "capacity": 25,
            }
        )

    for i in range(node_count - 2):
        roads.append(
            {
                "road_id": f"skip2_{i}",
                "source": i,
                "target": i + 2,
                "base_travel_time": 3 + (i % 4),
                "capacity": 22,
            }
        )

    for i in range(node_count - 5):
        roads.append(
            {
                "road_id": f"skip5_{i}",
                "source": i,
                "target": i + 5,
                "base_travel_time": 5 + (i % 5),
                "capacity": 18,
            }
        )

    for i in range(0, node_count - 20, 4):
        roads.append(
            {
                "road_id": f"express_{i}",
                "source": i,
                "target": i + 20,
                "base_travel_time": 11 + (i % 6),
                "capacity": 30,
            }
        )

    return {"nodes": nodes, "roads": roads}


def build_perf_updates():
    updates = []

    for i in range(0, 50):
        road_index = i * 2
        updates.append(
            {
                "tick": i,
                "road_id": f"chain_{road_index}" if road_index < 219 else "chain_0",
                "new_multiplier": 1.2 + (i % 5) * 0.2,
                "accident_penalty": float(i % 3),
            }
        )

    for i in range(20, 60, 10):
        updates.append(
            {
                "tick": i,
                "road_id": f"skip2_{i}",
                "close_road": True,
            }
        )

    for i in range(25, 65, 10):
        updates.append(
            {
                "tick": i,
                "road_id": f"skip2_{i - 5}",
                "reopen_road": True,
            }
        )

    return updates


def build_perf_requests():
    requests = []
    for i in range(120):
        start = (i * 7) % 90
        end = min(219, start + 30 + (i % 20))
        requests.append(
            {
                "request_id": f"req_{i}",
                "start": start,
                "end": end,
                "departure_tick": i % 50,
                "avoid_closed": True,
                "avoid_congested": False,
            }
        )
    return requests


def build_perf_delivery_groups():
    groups = []
    for i in range(30):
        depot = (i * 3) % 60
        stops = [
            min(219, depot + 15 + (i % 7)),
            min(219, depot + 28 + (i % 9)),
            min(219, depot + 40 + (i % 11)),
        ]
        groups.append(
            {
                "depot": depot,
                "stops": stops,
                "departure_tick": i % 40,
            }
        )
    return groups


PERF_NETWORK = build_perf_network()
PERF_UPDATES = build_perf_updates()
PERF_REQUESTS = build_perf_requests()
PERF_DELIVERY_GROUPS = build_perf_delivery_groups()


# =========================================================
# Static target speedups
# Replace with your calibrated values later
# =========================================================

PROBLEM_1_TARGET_SPEEDUP = 2.64
PROBLEM_2_TARGET_SPEEDUP = 15.21
PROBLEM_3_TARGET_SPEEDUP = 14.57
PROBLEM_4_TARGET_SPEEDUP = 8.73


# =========================================================
# Performance evaluation
# =========================================================

def run_problem_1_performance():
    request = {
        "request_id": "perf_single",
        "start": 0,
        "end": 150,
        "departure_tick": 25,
        "avoid_closed": True,
        "avoid_congested": False,
    }
    evaluate_performance_static_speedup(
        problem_name="Problem 1 - Single Route Search",
        baseline_func=baseline_find_route,
        student_func=find_route,
        args=(PERF_NETWORK, request, PERF_UPDATES),
        target_speedup=PROBLEM_1_TARGET_SPEEDUP,
        repeats=3,
        enforce_correctness=False,
    )


def run_problem_2_performance():
    evaluate_performance_static_speedup(
        problem_name="Problem 2 - Batch Route Processing",
        baseline_func=baseline_process_route_batch,
        student_func=process_route_batch,
        args=(PERF_NETWORK, PERF_REQUESTS, PERF_UPDATES),
        target_speedup=PROBLEM_2_TARGET_SPEEDUP,
        repeats=3,
        enforce_correctness=False,  
    )


def run_problem_3_performance():
    evaluate_performance_static_speedup(
        problem_name="Problem 3 - Top Congested Roads",
        baseline_func=baseline_top_congested_roads,
        student_func=top_congested_roads,
        args=(PERF_NETWORK, PERF_REQUESTS, PERF_UPDATES, 10),
        target_speedup=PROBLEM_3_TARGET_SPEEDUP,
        repeats=3,
        enforce_correctness=False,
    )


def run_problem_4_performance():
    evaluate_performance_static_speedup(
        problem_name="Problem 4 - Delivery Schedule Cost",
        baseline_func=baseline_delivery_schedule_cost,
        student_func=delivery_schedule_cost,
        args=(PERF_NETWORK, PERF_DELIVERY_GROUPS, PERF_UPDATES),
        target_speedup=PROBLEM_4_TARGET_SPEEDUP,
        repeats=3,
        enforce_correctness=False,
    )


if __name__ == "__main__":
    print(color("\nRunning A3 tests...", C.BOLD + C.CYAN))

    if not test_problem_1_correctness():
        sys.exit(1)
    run_problem_1_performance()

    if not test_problem_2_correctness():
        sys.exit(1)
    run_problem_2_performance()

    if not test_problem_3_correctness():
        sys.exit(1)
    run_problem_3_performance()

    if not test_problem_4_correctness():
        sys.exit(1)
    run_problem_4_performance()