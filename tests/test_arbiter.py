"""Unit tests for contract-net-bid-arbiter."""
import unittest
from contract_net_bid_arbiter.arbiter import ContractNetBidArbiter, TaskAnnouncement, AgentBid


class TestContractNetBidArbiter(unittest.TestCase):
    def test_award_best_bid(self):
        arb = ContractNetBidArbiter(cost_weight=0.8, latency_weight=0.2)
        task = TaskAnnouncement("t1", max_cost=10.0, max_latency_ms=500.0)
        bids = [
            AgentBid("agent_expensive", 9.0, 100.0),
            AgentBid("agent_cheap", 2.0, 400.0)
        ]
        winner = arb.evaluate_bids(task, bids)
        self.assertEqual(winner, "agent_cheap")

    def test_no_eligible_bids(self):
        arb = ContractNetBidArbiter()
        task = TaskAnnouncement("t1", max_cost=5.0, max_latency_ms=100.0)
        bids = [AgentBid("too_slow", 2.0, 500.0)]
        self.assertIsNone(arb.evaluate_bids(task, bids))
