from typing import Dict, List, Optional, Tuple, Any
import heapq


# =========================================================
# Core Simulator
# =========================================================

class TrafficRoutingSimulator:

    def __init__(self, network_data: Dict[str, Any]) -> None:
        self.nodes = network_data["nodes"]
        self.roads = network_data["roads"]

        # Build fast road lookup
        self.road_by_id = {}
        self.adjacency = {}

        for node in self.nodes:
            self.adjacency[node] = []

        for r in self.roads:
            road = r.copy()
            road.setdefault("traffic_multiplier", 1.0)
            road.setdefault("accident_penalty", 0.0)
            road.setdefault("is_closed", False)

            self.road_by_id[road["road_id"]] = road
            self.adjacency[road["source"]].append(road)

        self.current_tick = 0
        self.road_usage = {r["road_id"]: 0 for r in self.roads}

        # Pre-index updates by tick for O(1) application
        self.updates_by_tick = {}

    # =========================================================
    # Update handling
    # =========================================================

    def _index_updates(self, updates):
        if self.updates_by_tick:
            return
        for u in updates:
            self.updates_by_tick.setdefault(u["tick"], []).append(u)

    def _apply_updates_up_to(self, updates, tick):
        self._index_updates(updates)

        for t in range(self.current_tick, tick + 1):
            for u in self.updates_by_tick.get(t, []):
                road = self.road_by_id.get(u["road_id"])
                if not road:
                    continue
                if u.get("close_road"):
                    road["is_closed"] = True
                if u.get("reopen_road"):
                    road["is_closed"] = False
                if "new_multiplier" in u:
                    road["traffic_multiplier"] = u["new_multiplier"]
                if "accident_penalty" in u:
                    road["accident_penalty"] = u["accident_penalty"]

        self.current_tick = max(self.current_tick, tick)

    # =========================================================
    # Edge cost
    # =========================================================

    def _edge_cost(self, road):
        if road["is_closed"]:
            return float("inf")

        usage_penalty = 0.0
        capacity = road["capacity"]
        if capacity > 0:
            overload = self.road_usage[road["road_id"]] / capacity
            if overload > 1.0:
                usage_penalty = overload - 1.0

        return (
            road["base_travel_time"] * road["traffic_multiplier"]
            + road["accident_penalty"]
            + usage_penalty
        )

    # =========================================================
    # Fast Dijkstra
    # =========================================================

    def _shortest_path(self, start, end):
        dist = {node: float("inf") for node in self.nodes}
        prev_node = {}
        prev_road = {}

        dist[start] = 0.0
        heap = [(0.0, start)]

        while heap:
            d, node = heapq.heappop(heap)

            if node == end:
                break

            if d > dist[node]:
                continue

            for road in self.adjacency[node]:
                cost = self._edge_cost(road)
                if cost == float("inf"):
                    continue

                nxt = road["target"]
                new_d = d + cost

                if new_d < dist[nxt]:
                    dist[nxt] = new_d
                    prev_node[nxt] = node
                    prev_road[nxt] = road["road_id"]
                    heapq.heappush(heap, (new_d, nxt))

        if dist[end] == float("inf"):
            return {
                "reachable": False,
                "path_nodes": [],
                "road_ids": [],
                "cost": float("inf"),
            }

        # reconstruct path
        nodes = []
        roads = []
        cur = end
        while cur != start:
            nodes.append(cur)
            roads.append(prev_road[cur])
            cur = prev_node[cur]
        nodes.append(start)

        nodes.reverse()
        roads.reverse()

        return {
            "reachable": True,
            "path_nodes": nodes,
            "road_ids": roads,
            "cost": dist[end],
        }

    # =========================================================
    # Public operations
    # =========================================================

    def find_route(self, request, updates):
        self._apply_updates_up_to(updates, request["departure_tick"])
        result = self._shortest_path(request["start"], request["end"])

        if result["reachable"]:
            for r in result["road_ids"]:
                self.road_usage[r] += 1

        return result

    def process_route_batch(self, requests, updates):
        total_cost = 0.0
        reachable = 0
        unreachable = 0
        longest = 0

        for req in requests:
            result = self.find_route(req, updates)

            if result["reachable"]:
                reachable += 1
                total_cost += result["cost"]
                longest = max(longest, len(result["path_nodes"]) - 1)
            else:
                unreachable += 1

        avg = total_cost / reachable if reachable else 0.0

        return {
            "processed_requests": len(requests),
            "reachable_count": reachable,
            "unreachable_count": unreachable,
            "total_cost": total_cost,
            "average_cost": avg,
            "longest_path_hops": longest,
        }

    def top_congested_roads(self, requests, updates, top_k):
        self.process_route_batch(requests, updates)

        return [
            road_id
            for road_id, _ in sorted(
                self.road_usage.items(),
                key=lambda x: (-x[1], x[0]),
            )[:top_k]
        ]

    def delivery_schedule_cost(self, groups, updates):
        total = 0.0

        for g in groups:
            current = g["depot"]
            tick = g.get("departure_tick", 0)

            for stop in g["stops"]:
                result = self.find_route(
                    {
                        "request_id": "delivery",
                        "start": current,
                        "end": stop,
                        "departure_tick": tick,
                    },
                    updates,
                )
                if not result["reachable"]:
                    return -1.0

                total += result["cost"]
                current = stop
                tick += 1

        return total


# =========================================================
# Public wrapper functions
# =========================================================

def find_route(network, request, updates=None):
    sim = TrafficRoutingSimulator(network)
    return sim.find_route(request, updates or [])


def process_route_batch(network, requests, updates=None):
    sim = TrafficRoutingSimulator(network)
    return sim.process_route_batch(requests, updates or [])


def top_congested_roads(network, requests, updates=None, top_k=5):
    sim = TrafficRoutingSimulator(network)
    return sim.top_congested_roads(requests, updates or [], top_k)


def delivery_schedule_cost(network, groups, updates=None):
    sim = TrafficRoutingSimulator(network)
    return sim.delivery_schedule_cost(groups, updates or [])