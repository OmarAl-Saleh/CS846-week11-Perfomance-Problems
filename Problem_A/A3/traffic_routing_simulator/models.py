from typing import Optional


class RoadSegment:
    def __init__(
        self,
        road_id: str,
        source: int,
        target: int,
        base_travel_time: float,
        capacity: int,
        is_closed: bool = False,
        traffic_multiplier: float = 1.0,
        accident_penalty: float = 0.0,
    ) -> None:
        self.road_id = road_id
        self.source = source
        self.target = target
        self.base_travel_time = float(base_travel_time)
        self.capacity = int(capacity)
        self.is_closed = bool(is_closed)
        self.traffic_multiplier = float(traffic_multiplier)
        self.accident_penalty = float(accident_penalty)
        self.last_updated_tick = 0

    def clone(self) -> "RoadSegment":
        copied = RoadSegment(
            road_id=self.road_id,
            source=self.source,
            target=self.target,
            base_travel_time=self.base_travel_time,
            capacity=self.capacity,
            is_closed=self.is_closed,
            traffic_multiplier=self.traffic_multiplier,
            accident_penalty=self.accident_penalty,
        )
        copied.last_updated_tick = self.last_updated_tick
        return copied


class TrafficUpdate:
    def __init__(
        self,
        tick: int,
        road_id: str,
        new_multiplier: Optional[float] = None,
        close_road: bool = False,
        reopen_road: bool = False,
        accident_penalty: Optional[float] = None,
    ) -> None:
        self.tick = int(tick)
        self.road_id = road_id
        self.new_multiplier = new_multiplier
        self.close_road = close_road
        self.reopen_road = reopen_road
        self.accident_penalty = accident_penalty


class RouteRequest:
    def __init__(
        self,
        request_id: str,
        start: int,
        end: int,
        departure_tick: int = 0,
        avoid_closed: bool = True,
        avoid_congested: bool = False,
        congestion_threshold: float = 3.0,
    ) -> None:
        self.request_id = request_id
        self.start = int(start)
        self.end = int(end)
        self.departure_tick = int(departure_tick)
        self.avoid_closed = bool(avoid_closed)
        self.avoid_congested = bool(avoid_congested)
        self.congestion_threshold = float(congestion_threshold)
