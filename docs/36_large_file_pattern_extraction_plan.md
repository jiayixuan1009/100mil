# Large File Pattern Extraction Plan

本步骤用于处理不适合全量导入的超大原始 CSV。策略不是把 20GB+ 文件整体导入 DuckDB，而是按业务 URL pattern 抽取可行动子集。

## 抽取目标

默认匹配以下 URL pattern：

- `/compare/`
- `/converter/`
- `/blogdetail/` 和 `/blogDetail/`
- `/stock/`、`/us-stock/`、`/hk-stock/`
- `/iban`
- `/swift`
- `/sendmoney`
- `/download`

## 默认来源

- `01 www/sf/0518 all_inlinks.csv`
- `01 www/sf/0518 contains_structured_data_detailed_report.csv`
- `01 www/sf/0513 response_codes_all.csv`
- `01 www/sf/0518 internal_all.csv`
- `01 www/sf/0513 internal_all.csv`
- `01 www/gsc/api_cube_2026-05-22/query_date_api_rows.csv`

## 执行命令

```bash
.venv/bin/python scripts/extract_large_pattern_sources.py
```

可只跑某一类来源：

```bash
.venv/bin/python scripts/extract_large_pattern_sources.py --source inlinks
.venv/bin/python scripts/extract_large_pattern_sources.py --source internal_all
```

可只抽某一类 URL pattern：

```bash
.venv/bin/python scripts/extract_large_pattern_sources.py --pattern compare
.venv/bin/python scripts/extract_large_pattern_sources.py --pattern converter
.venv/bin/python scripts/extract_large_pattern_sources.py --source inlinks --pattern compare --pattern converter
```

调试时可限制每个源文件输出行数：

```bash
.venv/bin/python scripts/extract_large_pattern_sources.py --max-rows-per-source 10000
```

## 输出位置

```text
data/warehouse/extracts/large_patterns/
data/warehouse/parquet/large_patterns/
```

## DuckDB 视图

- `v_large_pattern_extract_inventory`
- `v_large_pattern_summary`
- `v_large_pattern_inlinks`
- `v_large_pattern_structured_data`
- `v_large_pattern_response_codes`
- `v_large_pattern_internal_all`
- `v_large_pattern_gsc_query_date`

## 查询入口

- `queries/large_pattern_extract_inventory.sql`
- `queries/large_pattern_summary.sql`
- `queries/large_pattern_compare_inlinks.sql`
- `queries/large_pattern_internal_health.sql`
- `queries/large_pattern_response_codes.sql`

## 原则

- 原始大文件只读不改。
- 抽取结果可重复生成。
- 先服务当前增长路径：compare、converter、blogdetail、stock、IBAN/SWIFT/sendmoney/download。
- 如未来需要全站 link graph，再单独做全量图谱任务。

## 当前运行结果

2026-06-01 已完成一次全量 pattern 抽取。6 个超大源文件均完成扫描和导入：

| source_kind | source | scanned_rows | matched_rows | imported_rows |
|---|---|---:|---:|---:|
| inlinks | `01 www/sf/0518 all_inlinks.csv` | 46,370,068 | 45,747,596 | 45,747,596 |
| structured_data | `01 www/sf/0518 contains_structured_data_detailed_report.csv` | 21,087,459 | 20,730,525 | 20,730,525 |
| response_codes | `01 www/sf/0513 response_codes_all.csv` | 1,956,914 | 649,535 | 649,535 |
| internal_all | `01 www/sf/0513 internal_all.csv` | 627,579 | 564,924 | 564,924 |
| internal_all | `01 www/sf/0518 internal_all.csv` | 570,689 | 559,040 | 559,040 |
| gsc_query_date | `01 www/gsc/api_cube_2026-05-22/query_date_api_rows.csv` | 3,926,800 | 423 | 423 |

注意：这次运行证明 `swift`、`sendmoney`、`compare`、`stock` 等 pattern 在站内覆盖非常广，尤其 inlinks 和 structured data 子集接近全量。后续日常重跑应优先使用 `--pattern compare`、`--pattern converter` 或 `--source response_codes` 等窄范围命令。