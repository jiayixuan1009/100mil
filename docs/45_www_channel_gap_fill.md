# `www` 渠道维度缺口补齐

本文件补的是 `43_direct_www_signal_followup.md` 里最关键的数据缺口：主站 `www` 缺少可复用的 `landing + default channel group` 维度。原始 raw 包里没有主站单独的 channel CSV，但存在一份三站合并 workbook：

- `cross/cross_ga4_3host_hostname_landing_channel_2025-11-20_2026-05-19.xlsx`

这一轮已经把它导入本地仓库，并生成视图：

- `v_cross_ga4_3host_landing_channel`

## 导入入口

```bash
.venv/bin/python scripts/import_cross_host_landing_channel_xlsx.py
```

脚本会：

1. 解析 workbook 第一张 sheet。
2. 抽取 `hostname`、`landing_page_query`、`default_channel_group`、`active_users`、`sessions`、`key_events`、`event_count`。
3. 写出本地 CSV 到 `data/warehouse/extracts/`。
4. 导入 DuckDB 表 `raw_cross_ga4_3host_landing_channel_xlsx`。
5. 创建视图 `v_cross_ga4_3host_landing_channel`。

## 这个补齐解决了什么

它还不能替代完整的 `session source / medium` 或 `page referrer` 导出，但已经足够回答一个更具体的问题：

`www` 大桶中的不同路径族，当前到底是 `Direct`、`Organic Search`、`Unassigned`、还是其他默认渠道组在主导？

## 新查询

`queries/direct_www_channel_group_matrix.sql` 用来回答上面这个问题。

它把主站 `www` 的 landing path 拆成：

- `home_or_not_set`
- `login`
- `download`
- `compare`
- `converter`
- `sendmoney`
- `blogdetail`
- `swift`
- `stock`
- `announcement`
- `register`
- `other`

再按 `default_channel_group` 汇总。

## 当前价值

这一步的意义不是“终于有完整归因了”，而是把下一轮 Direct 清洗从“纯推测”推进到“至少有默认渠道组佐证”。

这会直接帮助三件事：

1. 判断 `www` 大桶里哪些路径族其实主要不是 Direct。
2. 更准确地筛出真正需要主站 `source/referrer` 补导出的路径族。
3. 给老板周报提供更可靠的 clean vs raw 解释框架。

## 首轮结果

`queries/direct_www_channel_group_matrix.sql` 已运行通过。当前主站 `www` 的高量级路径族里，默认渠道组结果如下：

| path_group | default_channel_group | sessions | active_users |
|---|---|---:|---:|
| `swift` | `Direct` | 211,685 | 211,652 |
| `blogdetail` | `Direct` | 113,103 | 112,791 |
| `stock` | `Direct` | 97,494 | 97,367 |
| `sendmoney` | `Direct` | 85,832 | 85,762 |
| `home_or_not_set` | `Unassigned` | 75,538 | 74,946 |
| `compare` | `Direct` | 44,783 | 44,781 |
| `converter` | `Direct` | 12,797 | 12,787 |
| `announcement` | `Direct` | 12,146 | 11,607 |

同时也能看到，不同路径族并不是完全没有非 Direct 渠道：

- `blogdetail / Organic Search`：`23,900` sessions
- `other / Organic Search`：`15,397` sessions
- `home_or_not_set / Organic Search`：`13,733` sessions

这说明两件事同时成立：

1. 主站工具/内容模板在默认渠道组里确实被大规模记为 `Direct`。
2. 这并不等于它们都应该进入 clean Direct，因为同一批路径族仍混着 `Organic Search`、`Unassigned`、`Referral` 等渠道，并且前一轮 query signal 已证明其中混有 amount、campaign、webview 参数流量。

## 当前可执行结论

- `swift`、`blogdetail`、`stock`、`sendmoney`、`compare`、`converter` 不能被简单归为“品牌直达”。
- `home_or_not_set` 的 `Unassigned` 量级过大，说明仅看 raw Direct 仍会误判首页和 `(not set)` 桶。
- 下一轮最应该补的不是全站所有维度，而是主站这些高量级路径族的 `source / medium / referrer` 细项。

## 下一步

1. 运行 `queries/direct_www_channel_group_matrix.sql`，把主站路径族和默认渠道组的结果沉淀成下一轮清洗结论。
2. 继续申请主站单独的 `landing + source/medium + referrer` 导出。
3. 将 `default channel group` 结果与 `43_direct_www_signal_followup.md` 的 query-signal 结果合并判断。