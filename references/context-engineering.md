# Context Engineering for Long-Horizon Loops

A loop that runs for hundreds of iterations will exhaust or pollute its context
window unless you manage it actively. Context is a **finite resource with
diminishing marginal returns** — every token spends the model's attention budget,
and recall degrades as the window fills ("context rot"). The goal each cycle is the
*smallest set of high-signal tokens* that reliably produces the right action, not
the largest set of possibly-useful ones.

A useful fact for prioritizing: **tool outputs are usually the token hog**, often
the majority of what the agent actually sees — far more than the system prompt. So
trimming raw tool results (paginate reads, extract only the needed fields, edit
surgically) is usually higher-leverage than optimizing the prompt.

## The three levers for long-horizon loops

Pick by task shape; they compose.

### Compaction
When the window nears its limit, summarize the conversation and reinitialize a new
window from the summary. Keep architectural decisions, unresolved bugs, and
implementation details; drop redundant tool output and old messages. Optimize the
summary for **recall first** (don't lose a load-bearing detail), then tighten for
precision. Trigger proactively (~80% full) rather than waiting for overflow.
- **Best for:** tasks with lots of back-and-forth that must preserve a conversational thread.
- **Risk:** over-aggressive compaction drops context that looked minor but mattered later.

### Structured note-taking (agentic memory)
The agent periodically writes notes to persistent storage *outside* the context
window — a PROGRESS file, a state JSON, a memory tool — and pulls them back when
needed. Very low overhead, durable across context resets and sessions.
- **Best for:** iterative development with clear milestones; anything that must
  survive a reset.
- **Pattern:** keep the drift-prone facts (counts, status, in-flight work) in a
  machine-written state file, and the narrative (decisions, lessons) in a
  human-readable log. Re-read the state file each cycle; don't trust a remembered number.

### Sub-agent architectures
Instead of one agent holding all project state, delegate focused tasks to
sub-agents with **clean context windows**. A sub-agent can spend tens of thousands
of tokens exploring, then return a condensed 1–2k-token summary. The main agent
holds the high-level plan and coordinates.
- **Best for:** parallelizable exploration — deep research, multi-file analysis,
  diff review — where detail-heavy search should be isolated from the main thread.
- **Payoff:** clean separation of concerns; the main loop never sees the raw search
  context, only the conclusion.

## Just-in-time retrieval
Don't pre-load everything. Have the agent hold lightweight references (file paths,
stored queries, links) and load the actual data at runtime via tools — the way a
human uses a filesystem or bookmarks instead of memorizing a corpus. Metadata
(folder layout, naming conventions, timestamps) is itself signal about when and how
to use something. Combine with **progressive disclosure**: let the agent discover
relevant context by exploring, keeping working memory lean. A hybrid (some
pre-loaded context like a CLAUDE.md, plus runtime exploration via grep/glob) is
often the sweet spot.

## System prompt altitude
Calibrate instructions to the right level of abstraction. Too low (hardcoded
brittle logic) is unmaintainable; too high (vague guidance) lacks signal. Aim for
the band that is specific enough to steer behavior yet flexible enough to give the
model strong heuristics — and explain the *why*, so the model can generalize beyond
the literal instruction.
