# Cornifer — Project Context

You are helping build **Cornifer**, an AI agent written from scratch in Python — a
project for the sheer fun of understanding how agents work all the way down, with no
agent frameworks, one capability at a time. It's built in the open and meant to be
read, not just run: anyone curious is welcome to follow along or take it apart.
Milestones get written up as they land, but the build itself is the point. This file is the stable working contract.

## What this project is

- A real AI agent grown one capability at a time, from a bare loop to memory,
  context management, consolidation, and cost-aware routing.
- Each milestone ships one tightly-scoped capability to this single evolving codebase.
- Built in public for the love of it — the fun is understanding how agents work all
  the way down. Code is read as much as run: much of it ends up shown verbatim to
  whoever's following along, so it should read well for a curious stranger.

## The bar this sets

- **Readability is a feature.** Prefer clear, explicit code over clever code. Someone
  reading a diff cold should understand it without running it.
- **Comments explain *why*, not *what*.** The interesting decisions are the lesson.
- Small, self-contained, reviewable changes. The diff between two milestones *is* the
  teaching artifact — keep it legible.

## Non-negotiable: the no-framework rule

"No framework" means **no agent-scaffolding framework** — not "no dependencies."

The test for any library: *does it make a decision on the agent's behalf, or does it
just move bytes?*

- **Allowed (infrastructure):** HTTP clients (`httpx`/`requests`), the official
  model-provider SDK, cloud/Google API clients, vector-DB clients (Chroma/Qdrant/…),
  `pydantic`, `tiktoken`. These move bytes or do I/O.
- **Forbidden (agentic scaffolding):** LangChain/LlamaIndex agent layers, LangGraph,
  CrewAI, AutoGPT-style scaffolds — anything that hands us a pre-built loop, planner,
  tool router, or memory manager. Those hide the exact mechanism the project exists to
  expose.
- The loop, tool dispatch, context assembly, retrieval logic, planning, and routing
  are **always hand-written**, even when a library could do them "for free."
- Before adding any dependency, state which side of the test it falls on. If it's
  borderline, ask rather than assume.

## Stack

- Python, raw API calls. Standard library + the infrastructure deps above.
- One codebase on `main`. **No per-milestone folders** — the evolution is the story.

## Repo workflow (important)

- **Annotated git tag per milestone:** `milestone-03-tool-calling`. The tagged state
  must be runnable on its own.
- **The diff is the lesson:** changes for a milestone should read cleanly as
  `compare/milestone-02...milestone-03`. Avoid mixing unrelated refactors into a
  feature commit.
- **ADRs in `/decisions`:** when a real architectural choice is made (e.g. retrieval
  over full history), write a 2-paragraph decision record. Propose one whenever a
  decision is non-obvious.
- **README is the index:** keep the milestone → tag → diff → write-up-URL table
  updated when a milestone's work lands.
- Commit messages: clear and present-tense; they may be read publicly.

## Refactoring

An evolving codebase accumulates cruft; refactors are expected. The rule that keeps
the diffs teachable:

- **A refactor is its own commit — never bundled into a feature commit.** Someone
  reading `compare/milestone-06...milestone-07` to learn one capability shouldn't have
  to mentally subtract an unrelated rename.
- **Small, adjacent cleanups** (a rename or extracted helper in code the feature is
  already touching) can stay in the feature commit. Anything spanning unrelated files
  gets split out.
- **A refactor a milestone needs first** → a separate prelude commit *before* the
  feature, e.g. `refactor: extract MessageHistory ahead of context management`.
  Narrate it in the milestone's write-up if it clarifies the design.
- **A large, cross-cutting refactor that belongs to no single milestone** → its own
  interstitial tag (`refactor-01-tool-dispatch`) between milestone tags, listed in the
  README as housekeeping. Do not fold it into a feature commit.
- **Does it earn its own milestone? Redesign yes, cleanup no.** If the public API or
  the mental model moves — there's a transferable "the general lesson here is…" — flag
  it as a possible milestone. If behavior is identical and only the internals are
  neater, it never gets its own milestone, no matter how large the diff. Size doesn't
  decide this; a transferable lesson does.
- **Reversing an earlier decision supersedes its ADR** — write a new numbered ADR;
  never edit the old one.
- Any interstitial refactor tag must be runnable on its own — same bar as a milestone
  tag.

## Per-milestone working discipline

- **Honor the scope.** Each milestone has an explicit *Deferred* list in the plan. Do
  not pull deferred work forward — flag it as a future milestone instead. Fighting
  scope creep is a goal, not an accident.
- **Instrument early.** From Milestone 2 on, a tracing layer records
  tokens/latency/cost. New features should surface before/after numbers through it.
- **Evals from Milestone 5 on.** When a feature claims an improvement, run it against
  the eval scoreboard and report whether the number moved.
- **End every feature with its token/cost angle** — the "Token Cost" note. These
  consolidate into the cheat-sheet milestone.

## How to work with me

- For anything beyond a small change, **plan first and show the plan** before editing.
- Ask before: adding a dependency, widening a milestone's scope, or refactoring across
  unrelated modules.
- When you make a non-obvious decision, surface it (and offer an ADR) rather than
  burying it in a diff.
- The framing spine throughout: **an agent loop is a distributed system** — unreliable
  components, retries, timeouts, partial failure. Lean into that when designing.
