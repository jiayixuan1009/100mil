# Raw Warehouse Initial Findings

本报告记录 raw analysis layer 建成后的第一轮 SQL 验证结果。数据来自 `data/warehouse/biyapay.duckdb`，查询入口在 `queries/`。

## 验证范围

- 精选 raw CSV 导入：75 个文件，0 个失败。
- raw source inventory：5 个来源分组。
- 语义化查询：Direct/hostname、page location audit、AI search visibility、cross stock overlap、orphan page types。

## Raw Source Inventory

| source_group | files | size_mb | imported_rows | failed_files |
|---|---:|---:|---:|---:|
| technical_seo | 6 | 109.06 | 2,042,037 | 0 |
| gsc | 37 | 21.13 | 115,035 | 0 |
| cross_domain | 4 | 21.03 | 96,003 | 0 |
| ga4 | 27 | 20.58 | 223,241 | 0 |
| ai_search | 1 | 0.02 | 90 | 0 |

## Direct / Hostname Findings

`queries/direct_hostname_audit.sql` 显示，核心 host 之外仍有明显流量进入 GA4：

| hostname_class | hostname | active_users | engaged_sessions | key_events |
|---|---|---:|---:|---:|
| core | www.biyapay.com | 139,940 | 17,106 | 257,402 |
| subdomain | signup.biyapay.com | 7,370 | 5,045 | 21,211 |
| subdomain | invest.biyapay.com | 7,189 | 2,541 | 12,642 |
| pollution_or_external | active.biyagl.com | 3,229 | 2,171 | 8,341 |
| pollution_or_external | prv.cn.biyapay.io | 2,399 | 13 | 4,190 |

结论：Direct 专项下一步要把 `signup.biyapay.com`、`invest.biyapay.com` 和 `active.biyagl.com` 分开处理。`prv.*.biyapay.io` 属于测试/预发污染，应该从正式报表口径中排除或单独过滤。

## Page Location Audit Findings

`queries/page_location_audit_flags.sql` 已能直接抓取非核心 host 和疑似敏感 URL。当前 Top rows 包括：

- `signup.biyapay.com/download`：sessions `36,593`，active users `21,986`。
- `invest.biyapay.com/en/404`：sessions `4,209`。
- `invest.biyapay.com/zh/login`：sessions `2,145`。
- `invest.biyapay.com/en/spot/btc-usd`：sessions `2,013`。

结论：Direct 流量不能直接看总量，必须先按 hostname/page_location 清洗，否则 signup/download、invest、404/login 等路径会污染主站增长判断。

## AI Search Visibility Findings

`queries/ai_search_visibility.sql` 显示多个非品牌分类在 AI answer 中引用率为 0：

- 汇款：ChatGPT、DeepSeek 均 0%。
- 美港股：ChatGPT、DeepSeek 均 0%。
- 加密：ChatGPT 0%。

结论：AI SEO/GEO 后续不应只做品牌介绍页，应针对汇款、美港股、加密等非品牌意图建设可引用答案、事实页、对比页和结构化数据。

## Cross Stock Overlap Findings

`queries/cross_stock_overlap.sql` 显示 stock URL 映射存在大规模待处理项：

- `www / stock`：95,194 URLs，16 个月 impressions `62,079`，pending `95,194`。
- `invest / us-stock`：416 URLs，impressions `15,055`，overlap URLs `380`。
- `invest / hk-stock`：316 URLs，impressions `17,216`。

结论：stock 页不是当前第一优先级流量池，但存在明显 host/URL overlap 和 pending 处理压力。应在 compare P0 修复后单独开 stock overlap 专项。

## Orphan Findings

`queries/www_orphan_page_types.sql` 显示 0518 crawl 中 orphan 来源主要来自 sitemap 和 GA4：

- `other / SITEMAP`：332,750 URLs。
- `other / GA4`：12,964 URLs。
- `stock / GA4`：9,703 URLs。
- `stock / SITEMAP`：4,192 URLs。
- `compare / GA4`：3,644 URLs。

结论：compare 和 stock 模板既有技术问题，也有 crawl/internal-link 问题。compare 仍先修 `500`，修复后再用 orphan 和 inlink 数据补内链。

## 下一步

1. Direct 专项：基于 `v_raw_ga4_hostname_audit` 和 `v_raw_ga4_page_location_events` 生成正式清洗规则和报表口径。
2. AI SEO 专项：把 0 引用的非品牌意图拆成内容/结构化数据/权威引用任务。
3. Stock overlap 专项：用 `v_raw_cross_stock_mapping` 分出 www/invest 主次和 canonical 规则。
4. Compare 修复后：用 orphan + live health 复查 crawlability 和内链恢复情况。