"""Core Contract Net Bid Arbiter implementation."""
from typing import List, Dict, Optional, Any


class TaskAnnouncement:
    def __init__(self, task_id: str, max_cost: float, max_latency_ms: float):
        self.task_id = task_id
        self.max_cost = max_cost
        self.max_latency_ms = max_latency_ms


class AgentBid:
    def __init__(self, agent_id: str, cost: float, latency_ms: float, reputation: float = 1.0):
        self.agent_id = agent_id
        self.cost = cost
        self.latency_ms = latency_ms
        self.reputation = reputation


class ContractNetBidArbiter:
    def __init__(self, cost_weight: float = 0.5, latency_weight: float = 0.5):
        self.cost_weight = cost_weight
        self.latency_weight = latency_weight

    def evaluate_bids(self, task: TaskAnnouncement, bids: List[AgentBid]) -> Optional[str]:
        # Filter valid bids within SLA
        eligible = [b for b in bids if b.cost <= task.max_cost and b.latency_ms <= task.max_latency_ms]
        if not eligible:
            return None

        # Score bids: lower is better (cost/max_cost * w_cost + latency/max_lat * w_lat) / rep
        def score(b: AgentBid) -> float:
            c_norm = b.cost / max(0.001, task.max_cost)
            l_norm = b.latency_ms / max(0.001, task.max_latency_ms)
            raw = (c_norm * self.cost_weight) + (l_norm * self.latency_weight)
            return raw / max(0.1, b.reputation)

        winner = min(eligible, key=score)
        return winner.agent_id
