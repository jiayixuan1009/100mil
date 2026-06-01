---
description: "Use when continuing Direct traffic cleanup, refining clean reporting buckets, or investigating www content/tool Direct anomalies."
name: "Direct Cleanup Follow-up"
argument-hint: "Describe the Direct cleanup slice to continue"
agent: "agent"
model: ["GPT-5 (copilot)", "Claude Sonnet 4.5 (copilot)"]
---
Continue the Direct traffic cleanup work for this repository.

Requirements:
- Read [AGENTS.md](../AGENTS.md), [README.md](../README.md), and [docs/41_direct_traffic_cleanup_execution_pack.md](../docs/41_direct_traffic_cleanup_execution_pack.md) first.
- Reuse existing SQL under [queries](../queries) before inventing new analysis.
- Prefer durable outputs: update docs, CSV, SQL, or GitHub issues instead of writing a chat-only summary.
- If the current warehouse lacks a needed dimension, document the exact data gap and the next required export.
- Validate any new SQL you add against `data/warehouse/biyapay.duckdb`.

Expected output:
- one updated or new repo artifact
- one validation step
- one concise next-step recommendation
