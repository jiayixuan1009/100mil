# 100mil Agent Guide

This repository is designed to be used by multiple AI coding assistants and human operators on the same SEO growth program.

Use this file as the canonical, tool-agnostic instruction source.

## Mission

The project goal is to grow `biyapay.com` toward 1M monthly real, operable traffic without inflating metrics with test traffic, attribution loss, or non-actionable sessions.

All work should help one of these tracks:

1. Data trust: clean GA4, Direct, hostname, cross-domain, and reporting logic.
2. Existing page lift: improve already-indexed, already-impressioned URLs first.
3. Template recovery and rollout: compare, converter, sendmoney, bank code, swift, iban, blogdetail.
4. Execution system: every meaningful step becomes a document, CSV, SQL query, script, GitHub issue, or validation artifact.

## Source Of Truth

- Project overview: `README.md`
- Full document index: `docs/README.md`
- Growth roadmap: `docs/00_overall_growth_roadmap.md`
- Execution plan: `docs/02_execution_master_plan.md`
- Direct cleanup execution pack: `docs/41_direct_traffic_cleanup_execution_pack.md`
- Compare recovery pack: `docs/40_compare_postfix_validation_pack.md`
- GitHub planning queue: milestone and issue set in `jiayixuan1009/100mil`

Before starting a new task, read the most relevant nearby document instead of exploring broadly.

## Repository Layout

- `docs/`: strategy docs, execution briefs, status docs, and CSV deliverables.
- `queries/`: DuckDB SQL entry points for reusable analysis.
- `scripts/`: warehouse build, raw ingestion, extraction, and validation scripts.
- `data/warehouse/`: local analysis outputs only; do not commit generated DB, parquet, or extract artifacts.

## Working Rules

1. Prefer root-cause fixes over cosmetic summaries.
2. Do not treat raw Direct traffic as a valid KPI without cleaning buckets first.
3. Do not propose large new page creation until existing high-impression assets are reviewed.
4. Keep compare recovery blocked until live validation passes.
5. Preserve generated evidence: docs, CSVs, SQL, validation scripts, and issue comments should stay aligned.
6. If a task cannot be implemented in this repo because the production app code is absent, produce the sharpest possible diagnostic artifact, acceptance criteria, and handoff instead of stalling.

## Safe Editing Boundaries

- Commit docs, SQL, scripts, GitHub workflow artifacts, and lightweight config.
- Do not commit secrets, service-account files, local caches, `.venv/`, or `data/warehouse/` generated storage.
- Avoid reformatting unrelated files.
- Assume the worktree may contain user changes; do not revert unrelated modifications.

## Preferred Validation

Use the narrowest real validation available after each change:

- SQL added or changed: execute it against `data/warehouse/biyapay.duckdb`.
- Script added or changed: run the touched script or a minimal invocation.
- Docs/CSV changes: run file diagnostics and confirm links or referenced files exist.
- GitHub planning changes: confirm created issues, milestones, or comments.

## Standard Commands

Create or refresh local warehouse:

```bash
.venv/bin/python scripts/build_raw_data_catalog.py
.venv/bin/python scripts/build_seo_warehouse.py
.venv/bin/python scripts/ingest_selected_raw_sources.py
```

Run compare live regression:

```bash
.venv/bin/python scripts/validate_compare_live_urls.py
```

Run reusable SQL from the warehouse:

```bash
.venv/bin/python - <<'PY'
import duckdb
conn = duckdb.connect('data/warehouse/biyapay.duckdb')
for sql_file in [
    'queries/direct_cleanup_priority_summary.sql',
    'queries/direct_www_content_path_groups.sql',
]:
    print(sql_file)
    for row in conn.sql(open(sql_file).read()).fetchall():
        print(row)
PY
```

## Multi-AI Collaboration Contract

When multiple AI tools are used on this repository:

1. Treat `AGENTS.md` as the shared baseline.
2. Prefer writing durable repo artifacts over chat-only advice.
3. Update GitHub issues when a finding changes execution priority.
4. Reference existing docs and queries instead of regenerating equivalent analysis.
5. If you discover a missing team convention, add it here or to `docs/README.md` / `README.md`.

## Current Priorities

1. Finish Direct cleanup refinement for `www` content/tool traffic.
2. Keep compare recovery pressure on with concrete live evidence and validation criteria.
3. Preserve boss-facing reporting in clean, decision-ready form.

## Handoff Standard

Every non-trivial task should end with at least one of:

- updated document
- new or updated CSV
- new or updated SQL
- new or updated script
- GitHub issue or issue comment
- pushed commit with validation result

If work is blocked by missing production code or missing exports, document the blocker and the exact next required input.