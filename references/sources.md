# Sources

The 12 articles this skill distills (gathered 2026-06). Use for deeper reading or
to cite origins. Grouped by angle.

## The concept (loop engineering as the successor to prompt engineering)
- **MindStudio — "What Is Loop Engineering?"** — overview of loop engineering as
  the new meta. https://www.mindstudio.ai/blog/what-is-loop-engineering-ai-coding-agents
- **Agent Shortlist — "Loop Engineering: Self-Prompting AI Agents"** — the four
  trigger patterns (heartbeat/cron/hook/goal), the four guardrails, the
  whiteboard-five framework. https://agentshortlist.com/articles/loop-engineering
- **Tosea.ai — "From Prompt to Harness Engineering"** — the
  prompt → context → harness → loop progression; checkable endpoints; Reflexion.
  https://tosea.ai/blog/loop-engineering-ai-agents-complete-guide-2026
- **AI Builder Club — "Loop Engineering Guide 2026"** — the shift to "defining done
  and good"; verifier-first; closed vs open loops.
  https://www.aibuilderclub.com/blog/loop-engineering-guide-2026

## Loop architecture
- **Oracle — "What Is the AI Agent Loop?"** — ReAct/Reflexion;
  assemble-context → reason → act → observe; harness vs model separation;
  observability & cost. https://blogs.oracle.com/developers/what-is-the-ai-agent-loop-the-core-architecture-behind-autonomous-ai-systems
- **Steve Kinney — "The Anatomy of an Agent Loop"** — the loop is 30 lines, the
  complexity is all around it; early-stopping; loop fingerprinting; tool outputs as
  the token hog; Ralph Wiggum drift. https://stevekinney.com/writing/agent-loops
- **Claude Code Docs — "How the agent loop works"** — gather context → take action
  → verify work → repeat; subagents; compaction; stop conditions.
  https://code.claude.com/docs/en/agent-sdk/agent-loop

## Building & verification
- **MindStudio — "How to Build an Agentic Loop with Claude Code"** — the three exit
  types (success/failure/budget), `stop_reason`, max_turns / max_budget, runaway
  risks. https://www.mindstudio.ai/blog/how-to-build-agentic-loop-claude-code
- **MindStudio — "The PIV Loop"** — Plan → Implement → Validate; "a five-minute plan
  saves a twenty-minute debug." https://www.mindstudio.ai/blog/agentic-coding-workflow-piv-loop-explained

## Foundational / one-hand sources
- **Anthropic — "Effective Context Engineering for AI Agents"** — context as a
  finite resource; context rot; smallest-high-signal-token-set; just-in-time
  retrieval; compaction, structured note-taking, sub-agent architectures.
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **LinearB — "Ralph loops & the RPI methodology"** — `while true` + fresh context
  each iteration; filesystem as memory; ruthless context resets; Research-Plan-
  Implement. https://linearb.io/blog/dex-horthy-humanlayer-rpi-methodology-ralph-loop
- **Addy Osmani — "Self-Improving Coding Agents"** — stateless-but-iterative loops
  that accumulate knowledge via AGENTS.md / git / progress logs; evaluator-optimizer.
  https://addyosmani.com/blog/self-improving-agents/

## A worked example
The `oss-issue-pick` project (`~/side/oss-issue-pick`) is a real semi-autonomous
loop engineered along these lines: sense → triage → draft, stopping before any
outward-facing action. Its `loop-policy.md`, `gates/`, and `records/state/` map
onto Principles 2–7 and make a good concrete reference for what these ideas look
like in practice.
