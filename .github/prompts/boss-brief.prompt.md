---
description: "Use when preparing a boss-facing progress brief from the latest repository evidence, especially for Direct cleanup, template blockers, and current execution priorities."
name: "Boss Brief"
argument-hint: "Describe the reporting window or priority to summarize"
agent: "agent"
model: ["GPT-5 (copilot)", "Claude Sonnet 4.5 (copilot)"]
---
Prepare a boss-facing progress brief from the current repository state.

Requirements:
- Read [AGENTS.md](../AGENTS.md), [README.md](../README.md), and the nearest current execution docs in [docs](../docs).
- Prefer decision-ready wording over exhaustive detail.
- Separate clean, trustworthy metrics from raw or polluted metrics.
- Highlight blockers, business impact, and the next required action.
- If possible, write the brief back into the repository as a doc instead of only replying in chat.

Expected output:
- one concise brief suitable for leadership
- explicit blockers and owners
- the next 1-3 priorities
