# Large Pattern Extraction Results

本报告记录 2026-06-01 超大 CSV 主题抽取的实际结果和修正过程。

## 执行结论

- 6 个超大源文件均已完成扫描、抽取和 DuckDB 导入。
- 总匹配并导入行数：68,252,043。
- 抽取表已写入 `large_pattern_extract_manifest`。
- 查询视图已可用：`v_large_pattern_extract_inventory`、`v_large_pattern_summary`、`v_large_pattern_inlinks`、`v_large_pattern_structured_data`、`v_large_pattern_response_codes`、`v_large_pattern_internal_all`、`v_large_pattern_gsc_query_date`。

## 修正记录

初版脚本按文本行解析 CSV，遇到多行字段时会导致 `internal_all` 地址列错位。已修正为 `csv.reader` 记录级流式解析，并只在 URL 相关字段中匹配 pattern。

修正后验证：`v_large_pattern_internal_all` 中未发现 `Address not like 'http%'` 的错位样例。

## Inventory

当前磁盘占用：

- `data/warehouse`：约 26G。
- `data/warehouse/biyapay.duckdb`：约 5.9G。
- `data/warehouse/extracts`：约 20G。
- `data/warehouse/parquet`：约 849M。

| source_kind | scanned_rows | matched_rows | imported_rows |
|---|---:|---:|---:|
| inlinks | 46,370,068 | 45,747,596 | 45,747,596 |
| structured_data | 21,087,459 | 20,730,525 | 20,730,525 |
| response_codes | 1,956,914 | 649,535 | 649,535 |
| internal_all 0513 | 627,579 | 564,924 | 564,924 |
| internal_all 0518 | 570,689 | 559,040 | 559,040 |
| gsc_query_date | 3,926,800 | 423 | 423 |

## Pattern Summary

Top matched groups from `queries/large_pattern_summary.sql`：

| source_kind | matched_patterns | rows |
|---|---|---:|
| inlinks | swift | 16,617,095 |
| structured_data | swift | 16,499,505 |
| inlinks | sendmoney | 7,321,745 |
| inlinks | compare | 5,377,270 |
| inlinks | stock | 4,913,466 |
| inlinks | converter | 4,759,043 |
| inlinks | swift\|download | 1,682,017 |
| structured_data | converter | 1,624,000 |

## Practical Interpretation

这次结果说明 BiyaPay 的站内模板和结构化数据覆盖非常密集，`swift`、`sendmoney`、`compare`、`converter` 不是小众路径，而是大规模模板体系。因此这批数据已经接近一个可查询的局部 link graph。

后续不要频繁默认全量重跑。日常分析优先窄范围执行：

```bash
.venv/bin/python scripts/extract_large_pattern_sources.py --source inlinks --pattern compare --pattern converter
.venv/bin/python scripts/extract_large_pattern_sources.py --source response_codes --pattern compare
.venv/bin/python scripts/extract_large_pattern_sources.py --source internal_all --pattern converter
```

## Next Analysis Uses

1. Compare 修复后，用 `v_large_pattern_response_codes` 和 `v_large_pattern_internal_all` 复查状态码、indexability、canonical 和 inlinks。
2. Converter 扩展前，用 `v_large_pattern_inlinks` 查看哪些 converter 页有足够内链支持。
3. SWIFT/IBAN/sendmoney 专项可以从这批数据中直接抽技术健康、结构化数据和内链关系。
4. Stock overlap 专项需要进一步过滤 stock 子集，避免把全量模板噪音当成优先级。