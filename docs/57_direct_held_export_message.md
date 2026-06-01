# Direct held export message

Use this message to request the next Direct cleanup input from the data team.

```text
Hi team - we need one scoped GA4 export for the `www` held Direct cleanup.

Purpose:
Split the current held Direct bucket into clean Direct, search/referral leakage, app/webview return, campaign/promo, and log-level-review buckets.

Date range:
Use the same window as the current 3-host workbook: 2025-11-20 to 2026-05-19.

Filters:
- hostname = www.biyapay.com
- session default channel group = Direct
- landing page path group is one of:
  - swift
  - blogdetail
  - stock
  - sendmoney
  - compare

Required columns:
- date
- hostname
- landing page + query string
- session default channel group
- session source
- session medium
- full referrer
- sessions

Optional but useful columns:
- campaign
- source platform
- page referrer
- device category
- country

Please return as CSV, preferably named:
www_direct_held_source_referrer_2025-11-20_2026-05-19.csv

Validation on our side:
We will run:
.venv/bin/python scripts/import_direct_held_source_referrer.py --input <returned_csv>

The importer now fails fast if rows are outside hostname/channel/path scope, so please keep the export strictly scoped.
```

Supporting repo artifacts:

- `docs/50_direct_www_source_export_template.md`
- `docs/52_direct_held_source_referrer_import_runbook.md`
- `docs/phase3_direct_held_source_referrer_expected_columns.csv`
- `scripts/import_direct_held_source_referrer.py`
