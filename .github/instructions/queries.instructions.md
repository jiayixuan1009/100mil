---
description: "Use when creating or editing DuckDB SQL in queries/. Covers reusable analysis, naming, and validation requirements for warehouse queries."
applyTo: "queries/**/*.sql"
---
# Query Instructions

- Prefer reusable SQL entry points over one-off ad hoc snippets.
- Name queries by the business question they answer, not by temporary investigation steps.
- Keep queries compatible with the local DuckDB warehouse at `data/warehouse/biyapay.duckdb`.
- Use stable derived buckets and explicit `case` logic when creating reporting classifications.
- After changing a query, execute it against the warehouse before concluding.
- If a query depends on missing source fields, document the data gap in a nearby doc or issue.
