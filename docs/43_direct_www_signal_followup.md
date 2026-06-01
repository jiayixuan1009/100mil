# `www` Direct 大桶信号跟进

本文件承接 `41_direct_traffic_cleanup_execution_pack.md`，继续把 `review_www_content_or_tool_direct` 拆细。当前仓库没有主站 `referrer/source/medium` 的现成 raw 导出，因此这一轮先用 URL query signal 和 path family 做第二层判别。

## 输入

- `queries/direct_www_query_signal_summary.sql`
- `queries/direct_www_path_query_signal_matrix.sql`
- `docs/phase1_direct_www_query_signal_summary.csv`
- `docs/phase1_direct_www_path_query_signal_matrix.csv`

## 本轮新增结论

`www` 内容/工具 Direct 大桶不只是“无 referrer 的直接访问”。至少已经能确认混入三类显式信号：

1. `amount=` 参数流量：`69,143` sessions。
2. `utm_` 活动参数流量：`5,344` sessions。
3. 明显 WebView/embed 参数流量：`2,817` sessions。

这意味着即使暂时没有主站 `referrer/source/medium` raw 表，也已经足够证明这个大桶不能整体进入 clean Direct。

## Query Signal Rollup

| query_bucket | sessions | active_users | 解读 |
|---|---:|---:|---|
| `no_query_string` | 588,328 | 570,773 | 仍是最大残留桶，需要下轮补 source/referrer 或 logs |
| `other_query_params` | 70,425 | 64,143 | 说明存在大量内部状态或其他参数化访问 |
| `amount_param` | 69,143 | 69,113 | 强烈指向 calculator/template intent，不是简单品牌直达 |
| `utm_campaign_or_source` | 5,344 | 4,983 | 活动标记流量不应留在 clean Direct |
| `webview_embed_params` | 2,817 | 2,531 | 明显 App/WebView 嵌入流量 |

## Path Family x Signal

当前最值得优先追的组合：

| path_group | query_bucket | sessions | 解读 |
|---|---:|---:|---|
| `compare` | `amount_param` | 18,386 | compare 流量高度金额驱动，且 live 仍为模板级 `500` |
| `sendmoney` | `amount_param` | 18,233 | sendmoney 也明显不是纯品牌直达 |
| `converter` | `amount_param` | 7,465 | converter 当前最适合接 SEO + UX 改版验证 |
| `announcement` | `utm_campaign_or_source` | 3,970 | 活动流量已带显式 campaign 参数，必须从 clean Direct 移走 |
| `announcement` | `webview_embed_params` | 2,653 | 活动页还带明显 WebView 参数 |

同时，`blogdetail`、`swift`、`stock`、`sendmoney` 的 `no_query_string` 量级仍然很大，说明下一轮要么补 source/referrer 导出，要么接 access log 做佐证。

## 数据缺口

当前本地 warehouse 已导入的主站 GA4 表没有 `session source / medium`、`default channel group` 或 `referrer` 维度。已存在类似结构的只有 `invest` 和 `news` 的 `landing_event_hostname_channel` 表。

因此当前最有价值的新导出是：

- 主站 `landing page + query string`
- `default channel group`
- `session source / medium`
- `page referrer`
- `country`
- `device`

## 建议动作

### P0

- 先把 `utm_`、`_channel_track_key`、`height=44/language=zh-cn` 这类信号排出 clean Direct。
- 把 `amount_param` 相关路径全部保留在 `needs_review`，不要并入品牌直达。

### P1

- 导出主站 `landing_event_hostname_channel` 等价表。
- 如果短期拿不到 GA4 导出，则对 `blogdetail`、`swift`、`sendmoney`、`stock` 接 access log / edge log 复核。

### P2

- 把 `compare`、`converter`、`sendmoney` 的 `amount_param` 流量与模板提效工作统一到一个专项口径里。

## 当前结论

`review_www_content_or_tool_direct` 不是一个可直接纳入 clean Direct 的业务桶。仅靠这一轮 query signal 复核，就已经能证明它混有模板 intent、活动参数和 WebView/embed 回流。下轮不是继续争论是否“可能是 Direct”，而是补主站 source/referrer 导出或日志证据。
