# Compare 模板 500 工程修复 Ticket

## Ticket 标题

修复 compare 模板 `amount` 页面批量返回 `500` 的服务端错误

## 背景

在 Wave 1 Top30 页面中，12 个 compare URL 全部 live 校验为 `500`。

这说明问题不是某一个 USD-PHP 页面，而是 compare 模板/路由/服务端渲染的共性问题。

配套文件：

- `phase2_compare_top30_live_health.csv`
- `phase2_compare_p0_fix_acceptance.csv`
- [30_compare_template_p0_health_report.md](30_compare_template_p0_health_report.md)

## 影响范围

当前确认受影响的 URL 模式：

- `/compare/best-USD-PHP-exchange-rate?amount=1500`
- `/compare/best-AED-INR-exchange-rates?amount=3000`
- `/compare/best-AED-INR-exchange-rate?amount=1500`
- `/compare/best-USD-PKR-exchange-rate?amount=1500`
- `/compare/best-USD-GBP-exchange-rate?amount=1500`
- `/compare/best-JPY-USD-exchange-rates?amount=1500`
- `/compare/best-USD-INR-exchange-rate?amount=1500`
- `/compare/best-USD-AUD-exchange-rate?amount=1500`
- `/compare/best-PHP-USD-exchange-rates?amount=20000`
- `/compare/best-EUR-USD-exchange-rates?amount=1500`
- `/compare/best-JPY-USD-exchange-rate?amount=1500`
- `/compare/best-HKD-USD-exchange-rate?amount=1500`

## 当前现象

所有受检 URL 均为：

- HTTP status：`500`
- title：空
- meta：空
- canonical：空
- robots：空

## 业务影响

这些页面已经在 GSC 中产生曝光，Top30 中 12 个 compare URL 合计曝光超过 11 万级别。

当前 `500` 会导致：

- 搜索点击无法承接
- 页面无法转化
- Google 继续抓取时可能降低信任
- SEO 团队无法推进 compare 模板改稿

## 修复要求

### 路由层

- 同时支持 `exchange-rate` 和 `exchange-rates`
- 支持 `amount` query parameter
- 对非法 amount 有兜底，不返回 `500`
- 对未知币种 pair 有明确 404 或 fallback 策略

### 数据层

- 当实时汇率源异常时，不应让整页 500
- 至少展示降级状态或缓存数据
- 错误日志要记录 pair、amount、request path

### SEO 层

- title 非空
- meta description 非空
- canonical 明确
- robots 可索引
- H1 非空

### Canonical 策略

必须明确：

- 带 amount 的 URL 是否 self canonical
- 如果 canonical 到不带 amount 的 URL，页面如何保留 amount 搜索意图
- plural/singular route 是否 canonical 到同一个标准路径

## 验收方式

修复后运行 `phase2_compare_p0_fix_acceptance.csv` 中的 12 个 URL。

每个 URL 必须满足：

- status = `200`
- title 非空
- meta description 非空
- canonical 非空
- robots 包含 `index`
- 页面首屏能展示 pair 和 amount 语境

## 修复完成后的 SEO 下一步

修复验收通过后，再生成：

- compare CMS handoff
- compare title/meta 批量表
- compare launch tracker
- compare internal link map

## 当前优先级

P0。

原因：这些 URL 已有搜索曝光，但 live 页面不可用。先修可用性，再谈 SEO 改稿。