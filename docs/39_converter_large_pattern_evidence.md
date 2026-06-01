# Converter Large Pattern Evidence

本报告使用大文件抽取层补充 converter Wave 1 的技术和内链证据，用于支持 converter 首屏 UX 改造和内链增强。

## 输入数据

- `v_large_pattern_internal_all`
- `v_large_pattern_inlinks`
- `docs_phase2_wave1_converter_query_summary`

输出 CSV：

- `phase3_converter_large_pattern_target_evidence.csv`
- `phase3_converter_top_inlink_destinations.csv`
- `phase3_template_large_pattern_status_distribution.csv`

## Wave 1 Target Evidence

6 个 converter 目标页均在历史 crawl 中有稳定技术信号：

| page_key | impressions | avg_position | historical_internal_status | inlink_rows | source_urls |
|---|---:|---:|---|---:|---:|
| converter_thb_usd | 4,466 | 9.07 | 200/canonicalized + 200/indexable | 1,622 | 1,122 |
| converter_jpy_hkd | 2,393 | 12.55 | 200/canonicalized + 200/indexable | 1,621 | 1,121 |
| converter_php_usd | 2,172 | 9.84 | 200/canonicalized + 200/indexable | 1,622 | 1,122 |
| converter_eur_usd | 2,010 | 11.46 | 200/canonicalized + 200/indexable | 11,720 | 1,122 |
| converter_jpy_usd | 1,419 | 10.31 | 200/canonicalized + 200/indexable | 1,622 | 1,122 |
| converter_aed_pkr | 26 | 15.38 | 200/canonicalized + 200/indexable | 1,621 | 1,121 |

结论：converter Wave 1 不是技术 P0。它的问题更像是 query intent/CTR/首屏信息密度不足，而不是 crawl 阻塞。

## Internal Link Signal

目标 converter 页普遍有 1,100+ distinct source URLs。Top anchors 多来自 sendmoney/country templates：

- `汇款到 泰国`
- `汇款到 日本`
- `汇款到 菲律宾`
- `汇款到 奥地利`
- `Send money to United Arab Emirates`

这说明 converter 当前内链来源更偏“汇款目的地”，而不是“具体金额换算”和“币种对比较”。

## Action Implications

converter 的下一步不应优先做技术抢修，而应做三件事：

1. 首屏回答真实 query：直接展示金额结果、更新时间、费率/点差说明。
2. 把 GSC query 中的金额 chips 接进页面：例如 `1,000 JPY`、`3,000 EUR`、`20,000 THB`、`100万日元`、`1,000 PHP`。
3. 增加 contextual inlinks：从相关币种、国家汇款、compare、sendmoney 页面指向对应 converter，不只依赖模板导航。

## QA Requirements

- 保持 self canonical 和 `index, follow`。
- 不因为 amount chip 生成大量可索引重复 URL。
- amount 交互优先使用前端状态或 query 参数，但 canonical 仍指向主 converter URL。
- 埋点必须覆盖 `converter_amount_change`、`converter_chip_click`、`converter_compare_click`、`converter_transfer_click`、`converter_download_click`。

## Priority

converter 是 P1 增长项。当前曝光已在 page 1/page 2 边界，技术基础可用，最适合通过首屏意图匹配和内链增强提高 CTR 与点击量。