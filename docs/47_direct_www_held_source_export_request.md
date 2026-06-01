# `www` 挂起 Direct 桶 source 导出请求包

这个文档解决的是动作桶之后的下一个执行问题：

既然 `hold_content_tool_direct` 和 `hold_tool_intent_direct` 还不能并入 clean Direct，那么下一轮到底该向数据团队申请什么导出，先看哪些路径？

## 输入

- `queries/direct_www_action_buckets.sql`
- `queries/direct_www_held_source_export_priority.sql`
- `docs/phase1_direct_www_held_source_export_priority.csv`
- `docs/46_direct_www_action_bucket_pack.md`

## 挂起桶优先级

两类挂起桶合计 `602,724` sessions。下一轮 source/referrer 导出不需要全量泛抓，可以先按以下优先级申请：

| export_priority | action_bucket | path_group | sessions | pct_of_all_held |
|---|---|---|---:|---:|
| `export_now` | `hold_content_tool_direct` | `swift` | 211,685 | 35.12% |
| `export_now` | `hold_content_tool_direct` | `blogdetail` | 113,103 | 18.77% |
| `export_now` | `hold_content_tool_direct` | `stock` | 97,494 | 16.18% |
| `export_now` | `hold_tool_intent_direct` | `sendmoney` | 85,832 | 14.24% |
| `export_now` | `hold_tool_intent_direct` | `compare` | 44,783 | 7.43% |
| `export_after_p1` | `hold_content_tool_direct` | `other` | 37,030 | 6.14% |
| `export_after_p1` | `hold_tool_intent_direct` | `converter` | 12,797 | 2.12% |

前五个分组已经覆盖 `91.74%` 的 held Direct 体量，因此下一轮导出优先做这五类就足够支撑新一轮 clean Direct 判断。

## 建议导出字段

最小可用字段集：

- `date`
- `hostname`
- `landing page + query string`
- `session default channel group`
- `session source`
- `session medium`
- `full referrer`
- `sessions`

如果能多给一层，建议再带：

- `campaign`
- `source platform`
- `page referrer` 或等价的入口 referrer 字段

## 建议过滤条件

为了节约导出和复核成本，建议数据团队先按以下条件出一版：

- `hostname = www.biyapay.com`
- 时间窗与当前 3-host workbook 保持一致
- `session default channel group = Direct`
- 仅包含 `swift`、`blogdetail`、`stock`、`sendmoney`、`compare` 五类 landing path

## 为什么先这样导

1. 这五类已经覆盖绝大多数 held Direct 体量。
2. `sendmoney` 和 `compare` 直接连接商业转化路径，判断价值高。
3. `swift`、`blogdetail`、`stock` 是当前最大的内容/工具混合区，不拆开就无法继续收紧老板周报口径。
4. `compare` 还叠加模板级 `500` 阻塞，修复前后都需要单独复核其归因质量。

## 拿到导出后的判断规则

下一轮复核重点不是看总量，而是看这些 held Direct 是否被以下来源吞没：

- 搜索或社交流量被误归到 Direct
- App/WebView/内嵌容器回流
- campaign 或 deep-link 流量
- 内部跳转或技术归因缺失

拿到导出后，可继续把五类路径拆成：

- `keep_as_clean_direct_candidate`
- `move_to_search_or_referral`
- `move_to_app_or_webview_return`
- `move_to_campaign_or_promo`
- `still_needs_log_level_review`

## 下一步

1. 以这个请求包向数据团队申请主站 source/referrer 导出。
2. 先只复核 `export_now` 五类路径，不做全站铺开。
3. 导出回来后，再更新 `www` clean Direct 中间口径和老板周报字段。
