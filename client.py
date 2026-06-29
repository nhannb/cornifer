"""
OpenAI client wrapper.

Centralises all openai imports so the rest of the codebase never touches
the openai package directly.
"""

from __future__ import annotations

import functools
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI as _OpenAI

load_dotenv()


@functools.lru_cache(maxsize=1)
def _get_client() -> _OpenAI:
    """Return a cached OpenAI client, failing clearly if the key is absent."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            "ERROR: OPENAI_API_KEY is not set. "
            "Add it to your environment or to a .env file.",
            file=sys.stderr,
        )
        raise RuntimeError("OPENAI_API_KEY is missing — cannot initialise the OpenAI client.")
    return _OpenAI(api_key=api_key)


def chat(messages: list[dict]) -> tuple[str, dict]:
    """Send *messages* to the model and return the assistant reply and token usage."""
    response = _get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    content = response.choices[0].message.content
    if content is None:
        raise ValueError(
            f"Model returned no content (finish_reason={response.choices[0].finish_reason!r})"
        )
    usage = response.usage
    reasoning_tokens = None
    if usage and usage.completion_tokens_details:
        reasoning_tokens = usage.completion_tokens_details.reasoning_tokens
    token_counts = {
        "completion_tokens": usage.completion_tokens if usage else None,
        "prompt_tokens": usage.prompt_tokens if usage else None,
        "total_tokens": usage.total_tokens if usage else None,
        "reasoning_tokens": reasoning_tokens,
    }
    return content, token_counts
