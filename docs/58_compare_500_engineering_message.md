# Compare 500 engineering message

Use this message to hand the current compare blocker to engineering.

```text
Compare P0 is still blocked after the latest live regression.

Command run:
.venv/bin/python scripts/validate_compare_live_urls.py

Latest result:
- 12 checked
- 0 passed
- 12 failed
- all 12 return HTTP 500
- x-powered-by: Next.js
- body bytes: 21
- body preview: Internal Server Error
- body SHA-256: e41656eb2ba6c6293bf6dd928e5a88cdbc50535cab661c1969e0f598e497ed62

Evidence file:
docs/phase3_compare_live_regression_current.csv

This looks like a shared compare route/server/data fallback failure, not a single URL content issue.

Please check in this order:
1. compare route parser for singular/plural `exchange-rate` and `exchange-rates`
2. amount query handling, especially `?amount=1500` and `?amount=20000`
3. provider/rate data fallback when a pair is missing or delayed
4. SSR/Next.js error boundary and logging for these URLs
5. canonical/meta generation after the route returns 200

Acceptance:
Rerun `.venv/bin/python scripts/validate_compare_live_urls.py`.
Do not unblock compare SEO handoff until it returns 12/12 pass.
```

Supporting repo artifacts:

- `docs/40_compare_postfix_validation_pack.md`
- `docs/48_compare_nextjs_500_diagnostic_handoff.md`
- `docs/phase3_compare_engineering_fix_checklist.csv`
- `docs/phase3_compare_live_regression_current.csv`
- `scripts/validate_compare_live_urls.py`
