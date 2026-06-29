"""
Tests for the agent loop in main.py.

The key technique for simulating multiple calls: patch `main.chat` with a
`side_effect` list. Each call to `chat()` consumes the next value in the list,
so we can drive the loop through as many iterations as we like without hitting
the real API.
"""

from unittest.mock import patch

from main import run


def test_single_iteration_done():
    """Loop exits after one call when the model immediately signals DONE."""
    with patch("main.chat", return_value=("All done.\nDONE", {"completion_tokens": 5, "prompt_tokens": 10, "total_tokens": 15})) as mock_chat:
        run(goal="say hello", max_iterations=5)

    assert mock_chat.call_count == 1


def test_multiple_calls_before_done():
    """Loop runs several iterations before the model signals DONE.

    side_effect drives each successive call to return a different value,
    which is the standard way to simulate multiple API round-trips in tests.
    """
    usage = {"completion_tokens": 5, "prompt_tokens": 10, "total_tokens": 15}
    replies = [
        ("Still thinking…", usage),       # iteration 1 — no DONE
        ("Getting closer…", usage),       # iteration 2 — no DONE
        ("Finished.\nDONE", usage),       # iteration 3 — signals completion
    ]

    with patch("main.chat", side_effect=replies) as mock_chat:
        run(goal="count to three", max_iterations=10)

    assert mock_chat.call_count == 3


def test_max_iterations_cap():
    """Loop stops at max_iterations even when DONE is never returned."""
    with patch("main.chat", return_value=("Still going…", {"completion_tokens": 5, "prompt_tokens": 10, "total_tokens": 15})) as mock_chat:
        run(goal="never finish", max_iterations=4)

    assert mock_chat.call_count == 4


def test_history_grows_with_each_iteration():
    """Each assistant reply is appended to the message history passed to chat().

    chat() is called with the history *before* the current reply is appended,
    so the third call receives: system + user + reply1 + reply2 = 4 messages.
    The first call receives system + user = 2 messages.

    Because the loop passes the same list object each time, call_args would
    reflect the mutated final state. We capture deep copies inside a side-effect
    function to snapshot the history at the moment of each call.
    """
    import copy

    usage = {"completion_tokens": 5, "prompt_tokens": 10, "total_tokens": 15}
    replies = ["Step one.", "Step two.", "Step three.\nDONE"]
    snapshots: list[list[dict]] = []

    def capturing_chat(messages: list[dict]) -> tuple[str, dict]:
        snapshots.append(copy.deepcopy(messages))
        return replies[len(snapshots) - 1], usage

    with patch("main.chat", side_effect=capturing_chat):
        run(goal="multi-step task", max_iterations=10)

    assert len(snapshots) == 3
    # First call: system + user (2 messages)
    assert len(snapshots[0]) == 2
    # Second call: system + user + reply1 (3 messages)
    assert len(snapshots[1]) == 3
    assert snapshots[1][-1] == {"role": "assistant", "content": "Step one."}
    # Third call: system + user + reply1 + reply2 (4 messages)
    assert len(snapshots[2]) == 4
    assert snapshots[2][-1] == {"role": "assistant", "content": "Step two."}
