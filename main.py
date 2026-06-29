"""
Cornifer — Milestone 1: The Loop

An agent is just: while not done: history += model(history).
This file is the entry point. It parses the user's goal from the command line
and hands it to the agent loop.
"""

import argparse


def run(goal: str, max_iterations: int = 10) -> None:
    """Run the agent loop for the given goal."""
    # Milestone 1 implementation lives here.
    pass


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cornifer",
        description="A bare-loop AI agent, built from scratch.",
    )
    parser.add_argument("goal", help="The goal for the agent to work toward.")
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        # Cap iterations now — an uncapped loop is a token bonfire.
        help="Maximum number of loop iterations (default: 10).",
    )
    args = parser.parse_args()

    run(goal=args.goal, max_iterations=args.max_iterations)


if __name__ == "__main__":
    main()
