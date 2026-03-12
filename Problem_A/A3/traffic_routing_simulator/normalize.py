from typing import Any, Dict, List, Optional

from .models import RouteRequest, TrafficUpdate


def _normalize_updates(update_payloads: Optional[List[Dict[str, Any]]]) -> List[TrafficUpdate]:
    if not update_payloads:
        return []

    normalized: List[TrafficUpdate] = []
    for item in update_payloads:
        normalized.append(
            TrafficUpdate(
                tick=item["tick"],
                road_id=item["road_id"],
                new_multiplier=item.get("new_multiplier"),
                close_road=item.get("close_road", False),
                reopen_road=item.get("reopen_road", False),
                accident_penalty=item.get("accident_penalty"),
            )
        )
    return normalized


def _normalize_requests(request_payloads: List[Dict[str, Any]]) -> List[RouteRequest]:
    normalized: List[RouteRequest] = []
    for item in request_payloads:
        normalized.append(
            RouteRequest(
                request_id=item["request_id"],
                start=item["start"],
                end=item["end"],
                departure_tick=item.get("departure_tick", 0),
                avoid_closed=item.get("avoid_closed", True),
                avoid_congested=item.get("avoid_congested", False),
                congestion_threshold=item.get("congestion_threshold", 3.0),
            )
        )
    return normalized
