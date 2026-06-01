# Raw Selected Source Ingestion

本步骤把原始备份目录中的高价值、小中型 CSV 导入 DuckDB，作为 `docs` 执行表之外的 raw analysis layer。

## 导入原则

- 默认只导入 `60MB` 以下 CSV。
- 文件必须命中高价值关键词：`gsc`、`ga4`、`cross`、`ai-search`、`hostname`、`mapping`、`indexability`、`orphan`。
- `0518 all_inlinks.csv`、`internal_all.csv`、`query_date_api_rows.csv` 等超大文件继续只保留 catalog 索引，后续按 URL pattern stream/filter。
- 所有导入结果写入 `raw_import_manifest`，避免忘记某张表来自哪里。

## 执行命令

```bash
.venv/bin/python scripts/build_raw_data_catalog.py
.venv/bin/python scripts/build_seo_warehouse.py
.venv/bin/python scripts/ingest_selected_raw_sources.py
```

如需调大单文件上限：

```bash
.venv/bin/python scripts/ingest_selected_raw_sources.py --max-mb 120
```

## 新增视图

- `v_raw_source_inventory`：按来源分组统计已导入 raw 表数量、体积和行数。
- `v_raw_imported_tables`：列出每张 raw 表的表名、原始路径、行数和大小。
- `v_raw_import_failures`：列出导入失败的文件和错误。
- `v_raw_ga4_hostname_audit`：GA4 hostname 审计，用于识别核心 host、子域和污染 host。
- `v_raw_ga4_page_location_events`：GA4 page location 事件审计，用于识别非核心 host 和疑似敏感 URL。
- `v_raw_cross_stock_mapping`：invest/www 股票 URL 映射和 overlap 数据。
- `v_raw_ai_search_baseline`：AI search baseline 可见性数据。
- `v_raw_www_orphan_pages_0518`：www 0518 orphan pages，并附简单 page type guess。

## 查询入口

```bash
.venv/bin/python - <<'PY'
import duckdb
conn = duckdb.connect('data/warehouse/biyapay.duckdb')
for row in conn.sql(open('queries/raw_source_inventory.sql').read()).fetchall():
    print(row)
PY
```

## 使用方式

先通过 `v_raw_imported_tables` 找到目标 raw 表，再对具体表做 SQL 查询。这样以后分析 GSC、GA4、cross-domain、technical SEO 时，不需要重新读取原始 CSV。

常用查询文件：

- `queries/direct_hostname_audit.sql`
- `queries/page_location_audit_flags.sql`
- `queries/ai_search_visibility.sql`
- `queries/cross_stock_overlap.sql`
- `queries/www_orphan_page_types.sql`