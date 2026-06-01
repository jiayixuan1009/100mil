# BiyaPay 100 万月流量增长项目

这个仓库用于沉淀 BiyaPay 网站增长项目的方案、分析、SQL 查询、执行文档和交付表。

项目目标不是追求虚高流量，而是把 `biyapay.com` 体系的月真实可运营流量提升到 100 万级，并把过程变成可复用的执行系统。

## 当前重点

- 优先清洗 Direct 流量、hostname 污染和跨域归因问题。
- 优先修复 compare 模板 `500` 阻塞，再进入 SEO handoff。
- 优先放大已有曝光页面，而不是继续堆新页面。
- 所有专项都沉淀为独立文档、CSV 和 SQL，便于复盘与协作。

## 多 AI 协作

这个仓库现在包含跨 AI 协作基线，供团队使用不同 AI 工具时共享同一套上下文和规则：

- `AGENTS.md`：跨工具的仓库级单一事实源。
- `.github/copilot-instructions.md`：GitHub Copilot 工作区指令。
- `.github/instructions/`：按 `docs/`、`queries/`、`scripts/` 分类的文件级规则。
- `.github/prompts/`：团队可复用的标准任务 prompt。

团队如果使用不同 AI，请优先让它们读取这两个文件，再开始具体任务。

## 仓库结构

- `docs/`：项目主文档、专项方案、阶段报告和结构化 CSV 交付物。
- `queries/`：DuckDB 查询入口，用于复盘机会页、Direct 清洗、模板健康和回归验证。
- `scripts/`：本地仓库构建、raw 导入、大文件抽取和 live 校验脚本。
- `data/warehouse/`：本地分析仓库目录，包含 DuckDB、SQLite、Parquet 和抽取结果。该目录下的大文件默认不进入版本库。
- `.vscode/settings.json`：当前工作区 MCP 相关配置。

## 快速开始

安装依赖：

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

构建本地 catalog 和 SEO warehouse：

```bash
.venv/bin/python scripts/build_raw_data_catalog.py
.venv/bin/python scripts/build_seo_warehouse.py
```

导入精选 raw 数据并运行 Direct 相关 SQL：

```bash
.venv/bin/python scripts/ingest_selected_raw_sources.py
.venv/bin/python - <<'PY'
import duckdb
conn = duckdb.connect('data/warehouse/biyapay.duckdb')
for sql_file in [
    'queries/direct_hostname_audit.sql',
    'queries/page_location_audit_flags.sql',
    'queries/direct_cleanup_priority_summary.sql',
]:
    print(sql_file)
    for row in conn.sql(open(sql_file).read()).fetchall():
        print(row)
PY
```

## 推荐阅读顺序

- `docs/00_overall_growth_roadmap.md`：先看总路线。
- `docs/02_execution_master_plan.md`：再看执行顺序和交付机制。
- `docs/33_raw_data_warehouse_setup.md`：了解本地仓库结构。
- `docs/35_raw_warehouse_initial_findings.md`：了解 raw layer 第一轮结论。
- `docs/41_direct_traffic_cleanup_execution_pack.md`：查看当前最新的 Direct 清洗动作包。

完整文档索引见 `docs/README.md`。

## 当前可复用入口

- Direct 口径：`queries/direct_hostname_audit.sql`、`queries/page_location_audit_flags.sql`、`queries/direct_cleanup_priority_summary.sql`
- Compare 修复回归：`scripts/validate_compare_live_urls.py` 和 `queries/compare_postfix_live_regression_summary.sql`
- 大文件主题抽取：`scripts/extract_large_pattern_sources.py`

## 注意事项

- `data/warehouse/` 下的 DuckDB、SQLite、Parquet 和 extracts 体积很大，默认不提交。
- `secrets/`、`.secrets/`、服务账号文件和本地缓存默认不提交。
- 本仓库默认把文档、SQL 和脚本作为主要协作载体，而不是保存原始大数据。# BiyaPay 100 万月流量增长项目

这个仓库用于沉淀 BiyaPay 网站增长项目的方案、执行文档、分析 SQL 和辅助脚本。目标不是做一堆零散 SEO 建议，而是把“可信数据口径 + 可执行页面动作 + 技术验收标准”持续写进仓库，便于后续协作、复盘和 GitHub 跟踪。

## 当前重点

- 修正 GA4 / Direct 口径，先分清真实可运营流量和污染流量。
- 优先修复 compare 模板级 `500` 阻塞，恢复可抓取和可交付状态。
- 从现有高曝光页面中拿点击和转化增量，而不是盲目新增页面。

## 仓库结构

- `docs/`：阶段文档、专项文档、交付说明和配套 CSV。
- `queries/`：DuckDB 查询入口，直接复用本地仓库视图做验证和专项分析。
- `scripts/`：本地 catalog、DuckDB 导入、超大文件抽取、live 校验脚本。
- `data/warehouse/`：本地分析数据库和抽取结果；已被 `.gitignore` 排除，不推到 GitHub。

## 快速开始

安装依赖：

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

重建 catalog 和基础仓库：

```bash
.venv/bin/python scripts/build_raw_data_catalog.py
.venv/bin/python scripts/build_seo_warehouse.py
```

导入精选 raw 数据：

```bash
.venv/bin/python scripts/ingest_selected_raw_sources.py
```

运行 compare 修复后回归：

```bash
.venv/bin/python scripts/validate_compare_live_urls.py
```

## 关键入口

- 文档总索引：`docs/README.md`
- 总体路线图：`docs/00_overall_growth_roadmap.md`
- 主执行计划：`docs/02_execution_master_plan.md`
- Direct 专项方案：`docs/04_direct_traffic_special_plan.md`
- Direct 清洗执行包：`docs/41_direct_traffic_cleanup_execution_pack.md`
- Compare 修复后验收：`docs/40_compare_postfix_validation_pack.md`

## 当前分析约束

- 原始仓库体量很大，`data/warehouse/` 本地约 26G，只在本地查询，不进版本库。
- 仓库内文档和 SQL 以复用为主，避免重复读取超大 CSV。
- 所有增长判断优先基于真实可运营流量，而不是 GA4 表面总量。