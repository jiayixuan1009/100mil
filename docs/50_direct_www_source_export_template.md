# `www` held Direct source/referrer 导出申请模板

本模板用于向数据团队申请下一轮最小必要 GA4 导出。目标是继续拆 `www` held Direct，而不是全站泛导。

## 请求目的

请导出 `www.biyapay.com` 上五类 held Direct landing path 的 source/referrer 明细，用于判断它们应保留为 clean Direct，还是改归到搜索、Referral、App/WebView、Campaign 或技术归因缺失。

当前五类路径覆盖 `91.74%` 的 held Direct，因此先导这五类即可。

## 时间范围

请与当前三站 landing-channel workbook 保持一致：

- start date：`2025-11-20`
- end date：`2026-05-19`

如果 GA4 导出窗口不支持该完整范围，请先提供最近 `90` 天版本，并在文件名中标注日期范围。

## 过滤条件

必须过滤：

- `hostname = www.biyapay.com`
- `session default channel group = Direct`
- landing page path 匹配以下五类之一：
  - `/swift%`、`/en/swift%`、`/zh/swift%`
  - `/blogdetail%`、`/en/blogdetail%`、`/zh/blogdetail%`
  - `/stock%`、`/en/stock%`、`/zh/stock%`
  - `/sendmoney%`、`/en/sendmoney%`、`/zh/sendmoney%`
  - `/compare%`、`/en/compare%`、`/zh/compare%`

## 必需维度

请至少包含：

- `date`
- `hostname`
- `landing page + query string`
- `session default channel group`
- `session source`
- `session medium`
- `full referrer`

## 必需指标

请至少包含：

- `sessions`

## 建议附加维度

如果导出系统允许，请追加：

- `campaign`
- `source platform`
- `page referrer`
- `device category`
- `country`

## 输出格式

优先 CSV。

建议文件名：

```text
www_direct_held_source_referrer_2025-11-20_2026-05-19.csv
```

如果按最近 90 天导出：

```text
www_direct_held_source_referrer_last90_YYYY-MM-DD_YYYY-MM-DD.csv
```

## 回传后判断规则

拿到文件后，SEO/数据侧按以下规则重新分桶：

| 新桶 | 判断依据 |
|---|---|
| `keep_as_clean_direct_candidate` | source/medium/referrer 均无明显搜索、广告、社交、App/WebView、Campaign 信号 |
| `move_to_search_or_referral` | source/referrer 指向搜索、外链或 referral 来源 |
| `move_to_app_or_webview_return` | referrer 或参数显示 App/WebView/内嵌容器回流 |
| `move_to_campaign_or_promo` | campaign、utm、deep-link 或活动来源明显 |
| `still_needs_log_level_review` | GA4 仍无法判断，需要服务端日志或埋点补充 |

## 请求正文可复制版本

请帮忙导出 GA4 明细，用于拆分 `www.biyapay.com` 的 held Direct 流量。

范围：`2025-11-20` 到 `2026-05-19`。

过滤条件：`hostname = www.biyapay.com`，`session default channel group = Direct`，landing path 仅包含 `swift`、`blogdetail`、`stock`、`sendmoney`、`compare` 五类。

字段：`date`、`hostname`、`landing page + query string`、`session default channel group`、`session source`、`session medium`、`full referrer`、`sessions`。如果可以，请追加 `campaign`、`source platform`、`page referrer`、`device category`、`country`。

文件格式请用 CSV，文件名建议为 `www_direct_held_source_referrer_2025-11-20_2026-05-19.csv`。
