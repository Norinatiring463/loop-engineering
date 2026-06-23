# Loop Patterns: Trigger Types

Every autonomous loop is defined first by *what wakes it up*. There are four
patterns. Most production systems combine two or three (e.g. a hook handles
incoming work, a heartbeat watches an escalation queue, a cron emits a daily
report).

## Heartbeat (interval-anchored)
Wakes on a fixed interval (every 5 min, every hour), checks whether there's work,
acts if so, sleeps otherwise. Cost is bounded by frequency.
- **Use when:** you need to poll state that has no event to hook onto.
- **Failure mode:** without **idempotency**, two overlapping cycles process the
  same item twice. Design idempotency in earlier than feels necessary.

## Cron (time-anchored)
Fires at specific times (Monday 9am, end of month) whether or not there's work.
Highly predictable.
- **Use when:** the cadence is the point (reports, digests, scheduled refreshes).
- **Failure mode:** **stale prompt** — a prompt written six months ago runs
  against a changed model or changed assumptions, and no one notices. Re-validate
  cron prompts periodically.

## Hook (event-triggered)
Fires on an external event (email arrives, webhook, DB insert). Responds to real
work as it lands.
- **Use when:** latency matters and there's a clean event to subscribe to.
- **Failure mode:** **webhook storm** — a burst of events spawns a burst of runs
  and drains the budget in minutes. Every hook loop needs **rate limiting** and a
  **backpressure** mechanism.

## Goal (goal-anchored)
No schedule. The agent self-prompts and iterates until a strictly verified goal is
met. This is the "Ralph loop" shape: `while not done: work; verify`.
- **Use when:** the task is "keep going until X is true" and X is checkable.
- **Failure mode:** the most dangerous one. A vague goal ("research the landscape")
  has no convergence criterion and iterates until the budget is gone. A goal loop
  is only safe with a **machine-checkable success condition** plus hard budget and
  no-progress caps.

## The Ralph loop (a goal-pattern style)
A specific, influential implementation of the goal pattern: a `while true` shell
loop that feeds the agent the *same prompt file* every iteration, each iteration
starting with a **fresh context window**. State survives *not* in conversation
history but on disk — the codebase, a TODO/PRD file, git history. The evaluator
checks the result; if not done, another iteration runs with context from prior
attempts (via the files, not the chat).
- **Why it works:** ruthless context resets dodge context rot; the filesystem is
  the memory. Best for brownfield work with a clear PRD and a real verifier.
- **Where it fails:** greenfield with no spec, or no deterministic verifier — then
  it just produces volume ("PR slop") with no convergence.
- **Related method (RPI):** Research → Plan → Implement as separate passes, so the
  expensive context-gathering happens once and feeds cheap, repeatable implement
  cycles.

## Pattern selection framework
Ask, in order:
1. Time-anchored or state-anchored?
2. Is there an external event to trigger on?
3. Does it run until a goal is met?
4. What's the per-cycle cost ceiling?
5. What's the failure escalation path?

The answers map directly onto the four patterns above and onto the exits/guardrails
in the main skill (Principle 4).
