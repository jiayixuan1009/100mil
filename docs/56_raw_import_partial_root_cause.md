# Raw import partial root cause

## Current status

`scripts/ingest_selected_raw_sources.py` was rerun after adding skipped-row classification and encoding-risk visibility.

Current selected raw source status:

| import_status | files |
|---|---:|
| `imported` | 69 |
| `partial` | 5 |
| `failed` | 1 |

Current skipped-row / source-risk classification:

| import_status | skipped_row_kind | files |
|---|---|---:|
| `failed` | `encoding_blocked` | 1 |
| `partial` | `encoding_blocked` | 1 |
| `partial` | `metadata_preamble_skipped` | 4 |
| `imported` | `expected_empty_export` | 3 |
| `imported` | `metadata_preamble_skipped` | 20 |
| `imported` | `none` | 46 |

Evidence CSV: `docs/phase3_raw_import_partial_evidence.csv`

## What partial means here

The `partial` label now means the source was imported but still needs a reporting caveat because either:

- DuckDB imported fewer business rows than the inspected CSV shape indicates.
- The source file is not UTF-8 and may contain mojibake in labels or headers.

It does not always mean business data was lost. Several GA4 exports include metadata and preamble rows before the real header:

- `# ----------------------------------------`
- account/property labels
- date range labels
- blank rows
- sometimes a total row

DuckDB's tolerant import skips those rows so downstream views still get the expected business columns. The importer now records those cases as `metadata_preamble_skipped` instead of treating all skipped rows as the same failure mode.

## Root cause categories

### 1. GA4 export preamble rows

Examples:

- `ga4/ga4_page_location_pii_token_check_2025-11-20_2026-05-19.csv`
- `5-22/ga4_hostname_audit_28d_2026-04-24_to_2026-05-21.csv`
- `cross/www_to_invest_ga4_cross_domain_funnel_2025-11-20_2026-05-19.csv`

Finding: 24 GA4 files include metadata preamble rows. Of those, 20 imported cleanly after the preamble and 4 remain `partial` because inspected business rows exceed imported rows.

### 2. Non-UTF-8 source file

Two raw files are currently encoded as `iso-8859-1` and should be re-exported as UTF-8 before being used as durable evidence:

- `03 news/gsc/news_coverage_examples.csv`: `failed`, imports `0` rows under the current DuckDB path.
- `03 news/ga/ga4-news_hostname_daily_90d.csv`: `partial`, rows load but source labels are mojibake.

Observed cause: `file -I` identifies both as `iso-8859-1`; reading them as Latin-1 yields rows, but Chinese text becomes mojibake. These files should not be used as coverage or hostname evidence until re-exported as UTF-8 or normalized through a controlled transcode.

### 3. Legitimate zero-row GSC export tabs

Three GSC export tabs currently classify as `expected_empty_export`. They import `0` rows because the export tab has no data rows, not because the importer failed:

- `02 invest/invest_gsc_16m_query_page_date_country_device_2026-05-19/搜索结果呈现.csv`
- `02_invest/gsc/2026-05-19/invest_gsc_16m_query_page_date_country_device_2026-05-19/搜索结果呈现.csv`
- `03 news/news_gsc_16m_query_page_date_country_device_2026-05-19/搜索结果呈现.csv`

## Decision

Do not treat all `partial` rows as broken data. Use this rule:

1. GA4 exports with preamble rows: acceptable for current views, but cite the skipped-row caveat.
2. Non-UTF-8 files: blocked until re-exported or explicitly transcoded.
3. Zero-row export tabs: acceptable if the source export tab is expected to be empty.

## Next action

Data/SEO should request UTF-8 re-exports for the two `encoding_blocked` files, then rerun:

```bash
.venv/bin/python scripts/ingest_selected_raw_sources.py
```

Acceptance check: `v_raw_import_failures` should no longer contain `encoding_blocked` rows.
