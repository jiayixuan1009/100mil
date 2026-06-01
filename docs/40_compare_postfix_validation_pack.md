# Compare Post-Fix Validation Pack

本包用于 compare 模板工程修复后的回归验收。它把 live URL 检查、DuckDB 历史大表证据和上线判断标准放在一起，避免修复后只凭浏览器手工点几个页面。

## 输入

- `phase2_compare_p0_fix_acceptance.csv`：12 个 P0 live URL 和验收要求。
- `phase2_compare_top30_live_health.csv`：当前 live health 基线。
- `v_large_pattern_response_codes`、`v_large_pattern_internal_all`、`v_large_pattern_inlinks`：历史 crawl/内链证据。

## Live 回归脚本

```bash
.venv/bin/python scripts/validate_compare_live_urls.py
```

默认输出：

```text
docs/phase3_compare_live_regression_current.csv
```

每个 URL 会检查：

- HTTP status
- final URL
- title
- meta description
- H1
- canonical
- robots
- status/title/meta/canonical/robots/H1 是否通过

## 通过标准

12 个 URL 必须全部满足：

- `status = 200`
- title 非空
- meta description 非空
- H1 非空
- canonical 非空
- robots 包含 `index`
- 页面首屏保留 pair 和 amount 语境

如果 canonical 到不带 amount 的 URL，必须保证页面仍能回答 amount 查询意图，并且 canonical 策略已由工程/SEO确认。

## DuckDB 复查 SQL

```bash
.venv/bin/python - <<'PY'
import duckdb
conn = duckdb.connect('data/warehouse/biyapay.duckdb')
for sql_file in [
    'queries/compare_postfix_large_pattern_health.sql',
    'queries/compare_postfix_target_inlinks.sql',
    'queries/compare_postfix_live_regression_summary.sql',
]:
    print(sql_file)
    for row in conn.sql(open(sql_file).read()).fetchall():
        print(row)
PY
```

## 验收解读

- `compare_postfix_live_regression_summary.sql` 用来判断 12 个 live URL 是否全部通过。
- `compare_postfix_large_pattern_health.sql` 用来复查历史 crawl 中 compare 的 server error/no response/canonicalized 分布。
- `compare_postfix_target_inlinks.sql` 用来确认目标 URL 是否有历史 exact/base 内链；当前结果为 0 时，说明验收要以 live URL 为准，不能依赖旧 crawl exact match。

## 当前状态

截至本包创建时，compare 仍为 P0：12 个目标 URL 的历史 live health 均为 `500 / technical_blocker`。本包应在工程修复后立即重跑，只有 12/12 pass 才能进入 compare SEO handoff。

## 下一步

1. 工程修复 compare route/server/data fallback。
2. 运行 `scripts/validate_compare_live_urls.py`。
3. 如果 12/12 pass，生成 compare title/meta/CMS handoff。
4. 如果仍有 fail，按 CSV 中失败字段退回工程修复。