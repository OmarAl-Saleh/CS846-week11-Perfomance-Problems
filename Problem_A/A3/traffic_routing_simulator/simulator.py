from typing import Any, Dict, List, Optional, Tuple

from .models import RoadSegment, RouteRequest, TrafficUpdate


class TrafficRoutingSimulator:
   

    def __init__(self, network_data: Dict[str, Any]) -> None:
        self.nodes: List[int] = list(network_data.get("nodes", []))
        self.roads: List[RoadSegment] = self._load_roads(network_data.get("roads", []))
        self.current_tick: int = 0

        self.route_history: List[Dict[str, Any]] = []
        self.processed_request_count: int = 0
        self.unreachable_request_count: int = 0
        self._applied_update_keys: set[Tuple[int, str]] = set()

    def _load_roads(self, road_payloads: List[Dict[str, Any]]) -> List[RoadSegment]:
        loaded: List[RoadSegment] = []
        for item in road_payloads:
            loaded.append(
                RoadSegment(
                    road_id=item["road_id"],
                    source=item["source"],
                    target=item["target"],
                    base_travel_time=item["base_travel_time"],
                    capacity=item["capacity"],
                    is_closed=item.get("is_closed", False),
                    traffic_multiplier=item.get("traffic_multiplier", 1.0),
                    accident_penalty=item.get("accident_penalty", 0.0),
                )
            )
        return loaded

    def _find_road_by_id(self, road_id: str) -> Optional[RoadSegment]:
        # Intentional bottleneck: linear scan lookup
        for road in self.roads:
            if road.road_id == road_id:
                return road
        return None

    def _apply_updates_up_to_tick(self, updates: List[TrafficUpdate], tick: int) -> None:
        for update in updates:
            update_key = (update.tick, update.road_id)
            if update.tick <= tick and update_key not in self._applied_update_keys:
                self._apply_single_update(update)
                self._applied_update_keys.add(update_key)

    def _apply_single_update(self, update: TrafficUpdate) -> None:
        road = self._find_road_by_id(update.road_id)
        if road is None:
            return

        if update.close_road:
            road.is_closed = True
        if update.reopen_road:
            road.is_closed = False
        if update.new_multiplier is not None:
            road.traffic_multiplier = float(update.new_multiplier)
        if update.accident_penalty is not None:
            road.accident_penalty = float(update.accident_penalty)

        road.last_updated_tick = max(road.last_updated_tick, update.tick)

    def _count_usage_for_road(self, road_id: str) -> int:
        # Intentional bottleneck: scans full history every time
        count = 0
        for record in self.route_history:
            for used_road_id in record.get("road_ids", []):
                if used_road_id == road_id:
                    count += 1
        return count

    def _usage_penalty_for_road(self, road: RoadSegment) -> float:
        usage_count = self._count_usage_for_road(road.road_id)
        if road.capacity <= 0:
            return float(usage_count)
        overload = usage_count / road.capacity
        if overload <= 1.0:
            return 0.0
        return overload - 1.0

    def _is_effectively_blocked(self, road: RoadSegment, request: RouteRequest) -> bool:
        if request.avoid_closed and road.is_closed:
            return True
        if request.avoid_congested and road.traffic_multiplier >= request.congestion_threshold:
            return True
        return False

    def _effective_travel_time(self, road: RoadSegment, request: RouteRequest) -> float:
        if self._is_effectively_blocked(road, request):
            return float("inf")

        usage_penalty = self._usage_penalty_for_road(road)
        base_component = road.base_travel_time * road.traffic_multiplier
        return base_component + road.accident_penalty + usage_penalty

    def _build_adjacency(self) -> Dict[int, List[RoadSegment]]:
        # Intentional bottleneck: rebuilt from scratch on every route computation
        adjacency: Dict[int, List[RoadSegment]] = {}
        for node in self.nodes:
            adjacency[node] = []

        for road in self.roads:
            if road.source not in adjacency:
                adjacency[road.source] = []
            adjacency[road.source].append(road)

        return adjacency

    def _extract_min_frontier_index(self, frontier: List[Tuple[int, float]]) -> int:
        # Intentional bottleneck: linear scan min instead of heap
        best_index = 0
        best_distance = frontier[0][1]

        for i in range(1, len(frontier)):
            if frontier[i][1] < best_distance:
                best_distance = frontier[i][1]
                best_index = i

        return best_index

    def _reconstruct_route(
        self,
        previous_nodes: Dict[int, Optional[int]],
        previous_roads: Dict[int, Optional[str]],
        start: int,
        end: int,
    ) -> Dict[str, Any]:
        if end not in previous_nodes and start != end:
            return {
                "reachable": False,
                "path_nodes": [],
                "road_ids": [],
                "cost": float("inf"),
            }

        node_path: List[int] = [end]
        road_path: List[str] = []
        cursor = end

        while cursor != start:
            prev_node = previous_nodes.get(cursor)
            prev_road = previous_roads.get(cursor)

            if prev_node is None or prev_road is None:
                return {
                    "reachable": False,
                    "path_nodes": [],
                    "road_ids": [],
                    "cost": float("inf"),
                }

            road_path.append(prev_road)
            node_path.append(prev_node)
            cursor = prev_node

        node_path.reverse()
        road_path.reverse()

        return {
            "reachable": True,
            "path_nodes": node_path,
            "road_ids": road_path,
        }

    def find_best_route(self, request: RouteRequest) -> Dict[str, Any]:
        adjacency = self._build_adjacency()

        distances: Dict[int, float] = {node: float("inf") for node in self.nodes}
        previous_nodes: Dict[int, Optional[int]] = {}
        previous_roads: Dict[int, Optional[str]] = {}
        visited: set[int] = set()
        frontier: List[Tuple[int, float]] = []

        distances[request.start] = 0.0
        frontier.append((request.start, 0.0))

        while frontier:
            min_index = self._extract_min_frontier_index(frontier)
            current_node, current_distance = frontier.pop(min_index)

            if current_node in visited:
                continue

            visited.add(current_node)

            if current_node == request.end:
                break

            outgoing_roads = adjacency.get(current_node, [])
            for road in outgoing_roads:
                edge_cost = self._effective_travel_time(road, request)
                if edge_cost == float("inf"):
                    continue

                candidate_distance = current_distance + edge_cost
                if candidate_distance < distances.get(road.target, float("inf")):
                    distances[road.target] = candidate_distance
                    previous_nodes[road.target] = current_node
                    previous_roads[road.target] = road.road_id
                    frontier.append((road.target, candidate_distance))

        route = self._reconstruct_route(
            previous_nodes=previous_nodes,
            previous_roads=previous_roads,
            start=request.start,
            end=request.end,
        )

        if not route["reachable"]:
            route["cost"] = float("inf")
            return route

        route["cost"] = distances.get(request.end, float("inf"))
        return route

    def process_single_request(
        self,
        request: RouteRequest,
        updates: List[TrafficUpdate],
    ) -> Dict[str, Any]:
        self._apply_updates_up_to_tick(updates, request.departure_tick)
        self.current_tick = max(self.current_tick, request.departure_tick)

        route = self.find_best_route(request)

        record = {
            "request_id": request.request_id,
            "start": request.start,
            "end": request.end,
            "departure_tick": request.departure_tick,
            "reachable": route["reachable"],
            "cost": route["cost"],
            "road_ids": list(route["road_ids"]),
            "path_nodes": list(route["path_nodes"]),
        }

        self.route_history.append(record)
        self.processed_request_count += 1
        if not route["reachable"]:
            self.unreachable_request_count += 1

        return record

    def process_request_batch(
        self,
        requests: List[RouteRequest],
        updates: List[TrafficUpdate],
    ) -> Dict[str, Any]:
        total_cost = 0.0
        reachable_count = 0
        unreachable_count = 0
        longest_path_hops = 0

        for request in requests:
            result = self.process_single_request(request, updates)
            if result["reachable"]:
                reachable_count += 1
                total_cost += result["cost"]
                hop_count = max(0, len(result["path_nodes"]) - 1)
                if hop_count > longest_path_hops:
                    longest_path_hops = hop_count
            else:
                unreachable_count += 1

        average_cost = total_cost / reachable_count if reachable_count else 0.0

        return {
            "processed_requests": len(requests),
            "reachable_count": reachable_count,
            "unreachable_count": unreachable_count,
            "total_cost": total_cost,
            "average_cost": average_cost,
            "longest_path_hops": longest_path_hops,
        }

    def get_top_congested_roads(self, top_k: int) -> List[str]:
        counts: Dict[str, int] = {}
        for record in self.route_history:
            for road_id in record.get("road_ids", []):
                counts[road_id] = counts.get(road_id, 0) + 1

        sortable: List[Tuple[int, str]] = []
        for road in self.roads:
            road_count = counts.get(road.road_id, 0)
            sortable.append((road_count, road.road_id))

        sortable.sort(key=lambda item: (-item[0], item[1]))
        return [road_id for _, road_id in sortable[:top_k]]

    def summarize_network_state(self) -> Dict[str, Any]:
        closed_count = 0
        overloaded_count = 0
        total_multiplier = 0.0

        for road in self.roads:
            if road.is_closed:
                closed_count += 1
            if road.traffic_multiplier > 2.0:
                overloaded_count += 1
            total_multiplier += road.traffic_multiplier

        avg_multiplier = total_multiplier / len(self.roads) if self.roads else 0.0

        return {
            "roads": len(self.roads),
            "processed_requests": self.processed_request_count,
            "unreachable_requests": self.unreachable_request_count,
            "closed_roads": closed_count,
            "high_multiplier_roads": overloaded_count,
            "average_multiplier": avg_multiplier,
        }

    def estimate_delivery_schedule_cost(
        self,
        delivery_groups: List[Dict[str, Any]],
        updates: List[TrafficUpdate],
    ) -> float:
        total_cost = 0.0

        for group_index, group in enumerate(delivery_groups):
            current_start = group["depot"]
            departure_tick = group.get("departure_tick", 0)
            stops = group.get("stops", [])

            for stop_index, stop in enumerate(stops):
                request = RouteRequest(
                    request_id=f"delivery_{group_index}_{stop_index}",
                    start=current_start,
                    end=stop,
                    departure_tick=departure_tick + stop_index,
                    avoid_closed=True,
                    avoid_congested=False,
                )
                result = self.process_single_request(request, updates)
                if not result["reachable"]:
                    return -1.0
                total_cost += result["cost"]
                current_start = stop

        return total_cost
