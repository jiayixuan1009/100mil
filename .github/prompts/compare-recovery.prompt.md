---
description: "Use when diagnosing compare template blockers, updating live failure evidence, or preparing compare engineering handoff and validation."
name: "Compare Recovery"
argument-hint: "Describe the compare blocker or validation task"
agent: "agent"
model: ["GPT-5 (copilot)", "Claude Sonnet 4.5 (copilot)"]
---
Continue the compare recovery work for this repository.

Requirements:
- Start from [docs/32_compare_template_engineering_ticket.md](../docs/32_compare_template_engineering_ticket.md) and [docs/40_compare_postfix_validation_pack.md](../docs/40_compare_postfix_validation_pack.md).
- Reproduce the current live failure when possible.
- If production code is absent from this repo, produce a sharper diagnostic artifact or issue update instead of stopping.
- Keep the acceptance criteria aligned with `docs/phase2_compare_p0_fix_acceptance.csv`.
- Validate any new query or script before concluding.

Expected output:
- one updated diagnostic artifact or validation artifact
- one concrete engineering-facing conclusion
- one repo or GitHub update
