# Raw import partial root cause

## Current status

`scripts/ingest_selected_raw_sources.py` was rerun after adding partial-import visibility.

Current selected raw source status:

| import_status | files |
|---|---:|
| `imported` | 47 |
| `partial` | 28 |

Evidence CSV: `docs/phase3_raw_import_partial_evidence.csv`

## What partial means here

The `partial` label currently means DuckDB imported fewer rows than the simple `line_count - 1` expectation.

That is useful as a warning, but it does not always mean business data was lost. Several GA4 exports include metadata and preamble rows before the real header:

- `# ----------------------------------------`
- account/property labels
- date range labels
- blank rows
- sometimes a total row

DuckDB's tolerant import skips those rows so downstream views still get the expected business columns.

## Root cause categories

### 1. GA4 export preamble rows

Examples:

- `ga4/ga4_page_location_pii_token_check_2025-11-20_2026-05-19.csv`
- `5-22/ga4_hostname_audit_28d_2026-04-24_to_2026-05-21.csv`
- `cross/www_to_invest_ga4_cross_domain_funnel_2025-11-20_2026-05-19.csv`

Finding: the skipped rows are mostly export metadata, not normal data rows. The current DuckDB views remain usable, but reports should cite `skipped_rows` until the importer can distinguish metadata rows from true rejected rows.

### 2. Non-UTF-8 source file

`03 news/gsc/news_coverage_examples.csv` imports `0` rows under the current DuckDB path.

Observed cause: DuckDB reports an invalid Unicode byte sequence. `file -I` identifies the source as `iso-8859-1`; reading it as Latin-1 yields rows, but Chinese text becomes mojibake. This file should not be used as coverage evidence until it is re-exported as UTF-8 or normalized through a controlled transcode.

### 3. Legitimate zero-row GSC export tabs

Some GSC export tabs such as `搜索结果呈现.csv` can legitimately import `0` rows. These should be kept separate from failed imports and not treated as data loss without checking the source export context.

## Decision

Do not treat all `partial` rows as broken data. Use this rule:

1. GA4 exports with preamble rows: acceptable for current views, but cite the skipped-row caveat.
2. Non-UTF-8 files: blocked until re-exported or explicitly transcoded.
3. Zero-row export tabs: acceptable if the source export tab is expected to be empty.

## Next action

Update the raw importer later to classify skipped rows into:

- `metadata_preamble_skipped`
- `encoding_blocked`
- `true_row_rejects`
- `expected_empty_export`
