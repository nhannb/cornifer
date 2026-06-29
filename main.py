"""
Cornifer — Milestone 1: The Loop

An agent is just: while not done: history += model(history).
This file is the entry point. It parses the user's goal from the command line
and hands it to the agent loop.
"""

import argparse

from client import chat

SYSTEM_PROMPT = (
    "You are a helpful agent working toward a goal. "
    "Think step by step. When the goal is fully complete, "
    "end your final reply with the word DONE on its own line."
)
DONE_SENTINEL = "DONE"


def run(goal: str, max_iterations: int = 10) -> None:
    """Run the agent loop for the given goal."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": goal},
    ]

    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Iteration {iteration} ---")
        reply, usage = chat(messages)
        print(reply)

        if DONE_SENTINEL in reply:
            print("\nAgent signalled completion.")
            return
        messages.append({"role": "assistant", "content": reply})

    # Reached only when the cap is hit without a DONE signal.
    print(
        f"\nReached max iterations ({max_iterations}) without completion. "
        "Increase --max-iterations or refine the goal."
    )


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
