# Cornifer

> An AI agent built from scratch, one capability at a time.

Cornifer is a build-in-public project that grows a real AI agent from a bare loop into something capable, instrumented, and cost-aware — no agent frameworks, just Python and raw API calls.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- Python 3.14+
- An OpenAI API key

## Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/nhannb/cornifer.git
   cd cornifer
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Set your API key**

   Create a `.env` file in the project root:

   ```bash
   echo "OPENAI_API_KEY=sk-..." > .env
   ```

   Or export it directly in your shell:

   ```bash
   export OPENAI_API_KEY=sk-...
   ```

## Running the agent

```bash
uv run main.py "your goal here"
```

Or, if you've installed the package:

```bash
uv run cornifer "your goal here"
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--max-iterations` | `10` | Maximum number of loop iterations before stopping |

**Example:**

```bash
uv run main.py "List the first 5 prime numbers" --max-iterations 5
```

## Running tests

```bash
uv run pytest
```

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Entry point — argument parsing and the agent loop |
| `client.py` | OpenAI API client wrapper |
| `pyproject.toml` | Project metadata and dependencies |
| `decisions/` | Architecture Decision Records (ADRs) |
| `ROADMAP.md` | Full milestone plan |

## Milestones

| Milestone | Tag | Description |
|---|---|---|
| 1 | `milestone-01-the-loop` | The bare agent loop |

---

Follow the build: each milestone ships a tightly-scoped capability. The diff between two tags *is* the lesson.
