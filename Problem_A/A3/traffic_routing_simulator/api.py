from typing import Any, Dict, List, Optional

from .normalize import _normalize_requests, _normalize_updates
from .simulator import TrafficRoutingSimulator


def find_route(
    network_data: Dict[str, Any],
    request_payload: Dict[str, Any],
    update_payloads: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Return the best route for one request on the given network."""
    simulator = TrafficRoutingSimulator(network_data)
    updates = _normalize_updates(update_payloads)
    requests = _normalize_requests([request_payload])
    return simulator.process_single_request(requests[0], updates)


def process_route_batch(
    network_data: Dict[str, Any],
    request_payloads: List[Dict[str, Any]],
    update_payloads: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Process many route requests and return a summary of the results."""
    simulator = TrafficRoutingSimulator(network_data)
    updates = _normalize_updates(update_payloads)
    requests = _normalize_requests(request_payloads)
    return simulator.process_request_batch(requests, updates)


def top_congested_roads(
    network_data: Dict[str, Any],
    request_payloads: List[Dict[str, Any]],
    update_payloads: Optional[List[Dict[str, Any]]] = None,
    top_k: int = 5,
) -> List[str]:
    """Return the roads that were used the most after processing requests."""
    simulator = TrafficRoutingSimulator(network_data)
    updates = _normalize_updates(update_payloads)
    requests = _normalize_requests(request_payloads)
    simulator.process_request_batch(requests, updates)
    return simulator.get_top_congested_roads(top_k)


def delivery_schedule_cost(
    network_data: Dict[str, Any],
    delivery_groups: List[Dict[str, Any]],
    update_payloads: Optional[List[Dict[str, Any]]] = None,
) -> float:
    """Estimate the total cost of completing the delivery groups."""
    simulator = TrafficRoutingSimulator(network_data)
    updates = _normalize_updates(update_payloads)
    return simulator.estimate_delivery_schedule_cost(delivery_groups, updates)
