# Copilot Instructions For 100mil

Use `AGENTS.md` at the repository root as the primary shared instruction file.

Additional Copilot-specific expectations:

## Default Approach

- Start from the nearest concrete artifact: issue, doc, query, script, or failing URL.
- Keep repository changes small and traceable.
- Turn analysis into durable repo outputs instead of long chat-only summaries.

## Priority Order

1. Data trust and reporting cleanup.
2. Existing page and template lift.
3. Technical blockers that prevent SEO execution.
4. Team workflow artifacts that improve repeatability across AI tools.

## Repository Conventions

- New docs go in `docs/` and must usually be indexed in `docs/README.md`.
- Reusable analysis should become SQL in `queries/` when practical.
- One-off or repeatable logic should become a script in `scripts/`.
- Do not commit generated warehouse data under `data/warehouse/`.

## Validation Expectations

- Execute new SQL before concluding.
- Run diagnostics on changed docs and CSVs.
- If you update GitHub issues or milestones, verify they were created or commented successfully.

## When Production Code Is Missing

If a user asks to fix something that is not implemented in this repository, do not stop at "cannot fix here".

Instead:

- reproduce the live failure if possible
- narrow the likely fault domain
- write a diagnostic artifact or engineering handoff
- update the relevant GitHub issue

## Cross-AI Goal

This repository is intentionally shared across multiple AI development tools. Favor neutral, explicit instructions and durable documentation so Claude, Copilot, Cursor, and similar tools can all continue the same work without hidden context.