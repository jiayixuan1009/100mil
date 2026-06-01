# Raw Data Warehouse Setup

本仓库已增加一个本地 SEO 数据仓库，用来减少反复读取大 CSV 和长文档造成的 token 浪费。

## 目标

- 把原始备份目录和当前执行 CSV 建成可检索目录。
- 把 `docs/*.csv` 导入 DuckDB，形成可直接 SQL 查询的工作表。
- 对大文件只建索引，不默认全量导入，避免 13GB Screaming Frog 文件拖慢工作流。
- 固化常用视图，服务后续 Wave 2、Direct 专项、converter 扩展和 compare 修复验收。

## 文件结构

```text
data/warehouse/
  catalog.sqlite
  biyapay.duckdb
  catalog_exports/
    raw_files.csv
    workspace_doc_files.csv
  parquet/docs/

scripts/
  build_raw_data_catalog.py
  build_seo_warehouse.py

queries/
  warehouse_smoke_test.sql
  compare_blockers.sql
  converter_low_ctr.sql
  top_opportunities.sql
```

## 构建命令

首次使用先创建项目虚拟环境：

```bash
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

然后构建 catalog 和 DuckDB：

```bash
.venv/bin/python scripts/build_raw_data_catalog.py
.venv/bin/python scripts/build_seo_warehouse.py
```

## 数据库职责

`catalog.sqlite` 负责文件级索引：路径、文件名、扩展名、大小、mtime、可安全统计的行数、表头和建议导入策略。

`biyapay.duckdb` 负责分析查询：当前会导入所有 `docs/*.csv`，并把每张表同步导出为 Parquet。

## 当前视图

- `v_compare_blockers`：compare 模板 `500` 技术阻塞 URL。
- `v_converter_low_ctr`：converter 查询表现和低 CTR 页面。
- `v_top_gsc_opportunities`：Top 200 GSC 机会页。
- `v_technical_p0_p1`：技术 SEO P0/P1 项。
- `v_wave1_cms_handoff`：Wave 1 CMS 交付页。
- `v_workspace_tables`：当前 DuckDB 内所有表。

## 示例查询

```bash
.venv/bin/python - <<'PY'
import duckdb
conn = duckdb.connect('data/warehouse/biyapay.duckdb')
for row in conn.sql(open('queries/warehouse_smoke_test.sql').read()).fetchall():
  print(row)
PY
```

后续如果要查 converter、compare 或 Top opportunities，优先查询 `queries/` 下的 SQL，不再重新把 CSV 全文读进上下文。

## 注意事项

- `01 www/sf/0518 all_inlinks.csv` 等超大 Screaming Frog 文件只进入 catalog，不默认导入。
- 旧 crawl 状态只能作为历史证据，live 校验结果优先级更高。
- URL 分析要优先按 canonical、article ID 或 URL pattern 聚合，避免精确 URL 漏掉历史变体。