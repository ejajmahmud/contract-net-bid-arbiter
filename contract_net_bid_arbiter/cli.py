"""CLI for contract-net-bid-arbiter."""
import sys
import argparse
from .arbiter import ContractNetBidArbiter, TaskAnnouncement, AgentBid


def main():
    parser = argparse.ArgumentParser(description="Contract Net Bid Arbiter CLI")
    parser.add_argument("--demo", action="store_true", help="Run contract net bid arbitration demo")
    args = parser.parse_args()

    if args.demo:
        arbiter = ContractNetBidArbiter()
        task = TaskAnnouncement("ast_refactor", max_cost=1.0, max_latency_ms=1000)
        bids = [
            AgentBid("agent_fast", cost=0.8, latency_ms=200, reputation=0.9),
            AgentBid("agent_cheap", cost=0.2, latency_ms=800, reputation=0.95),
            AgentBid("agent_over_budget", cost=1.5, latency_ms=100, reputation=1.0)
        ]
        winner = arbiter.evaluate_bids(task, bids)
        print(f"[+] Task '{task.task_id}' awarded to winning bidder: '{winner}'")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
