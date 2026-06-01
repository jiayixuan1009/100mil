# Compare Large Pattern Evidence

本报告使用 `data/warehouse/biyapay.duckdb` 中的大文件抽取层，补充 compare 模板 `500` 工程 ticket 的历史 crawl 和内链证据。

## 输入数据

- `v_large_pattern_response_codes`
- `v_large_pattern_internal_all`
- `v_large_pattern_inlinks`
- `docs_phase2_compare_top30_live_health`

输出 CSV：

- `phase3_template_large_pattern_status_distribution.csv`
- `phase3_compare_large_pattern_target_evidence.csv`
- `phase3_compare_top_inlink_destinations.csv`

## Template-Level Evidence

历史 Screaming Frog 大表中，compare 相关 URL 已经出现明显技术不稳定：

| source | status_code | indexability | indexability_status | rows |
|---|---:|---|---|---:|
| response_codes | 200 | Indexable |  | 1,515 |
| response_codes | 502 | Non-Indexable | Server Error | 1,415 |
| response_codes | 0 | Non-Indexable | No Response | 1,155 |
| response_codes | 500 | Non-Indexable | Server Error | 553 |
| internal_all | 200 | Non-Indexable | Canonicalised | 29,400 |
| internal_all | 200 | Indexable |  | 3,089 |
| internal_all | 502 | Non-Indexable | Server Error | 1,415 |
| internal_all | 500 | Non-Indexable | Server Error | 1,281 |
| internal_all | 0 | Non-Indexable | No Response | 1,155 |

结论：当前 live Top30 compare 全部 `500` 不是偶发单页问题。历史 crawl 已显示 compare 体系存在 server error、timeout/no response、canonicalized URL 大量堆积的问题。

## Live Top30 Target Evidence

`phase3_compare_large_pattern_target_evidence.csv` 中 12 个 live blocker URL 的 exact/base match 历史 inlink 结果均为 0。

这不是说页面没有 SEO 价值，而是说明当前 live blocker URL 与历史 crawl 中的 compare URL 形态不完全一致，或者这些 amount/query 路由没有被历史 crawl 作为稳定可访问 URL 捕获。结合 live health 中 12 个 URL 全部 `500`，工程验收必须以 live URL 为准。

## Internal Link Context

compare 模板整体有大量全局/模板级内链入口。Top destinations 包括：

- `/en/compare` 和 `/zh/compare`：各约 30,975 inlink rows。
- download、sendmoney、academy、referral 等全局路径大量互链。
- compare detail URL 中也存在大量 amount 参数互链，例如 `best-GBP-PKR-exchange-rate?amount=30000`。

结论：修 compare `500` 时不能只修 12 个 URL。需要保证：

1. `/compare` 列表页可用。
2. singular/plural detail route 都可用。
3. `amount` query 参数不触发 server error。
4. canonical 收敛到稳定 detail URL。
5. template 内部推荐金额链接不继续生成 500/502/no-response URL。

## Engineering Acceptance Addendum

在 [32_compare_template_engineering_ticket.md](32_compare_template_engineering_ticket.md) 的基础上，追加以下验收：

- 修复后重跑 `queries/large_pattern_response_codes.sql`，compare 相关 `500/502/0` 不应继续出现在新 crawl 中。
- 12 个 live blocker URL 必须全部返回 `200` 或明确 `301/308` 到可索引 canonical。
- compare detail 页必须输出 title、meta、H1、canonical、robots。
- amount 参数必须只改变计算结果，不改变 canonical 主体。
- 对历史 canonicalized URL 建 redirect/canonical 策略，避免继续堆积重复 URL。

## Priority

compare 仍是 P0。理由：

- live Top30 compare URLs 全部 `500`。
- 历史 crawl 已有大量 compare server error 和 timeout 证据。
- compare 模板有大量内链入口，错误会浪费 crawl budget 并伤害模板信任度。