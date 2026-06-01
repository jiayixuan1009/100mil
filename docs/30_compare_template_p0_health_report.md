# Compare 模板 P0 Live Health 专项

## 文档用途

本文件用于升级 compare 页面问题的优先级。

最初只发现 `USD-PHP amount=1500` 返回 `500`。继续检查 Top30 里的 compare 页面后，确认这不是单页问题，而是 compare 模板/路由级问题。

配套数据文件：

- `phase2_compare_top30_live_health.csv`

## 检查范围

Top30 中全部 compare 页面，共 12 个。

包括：

- `USD-PHP amount=1500`
- `AED-INR amount=3000`
- `AED-INR amount=1500`
- `USD-PKR amount=1500`
- `USD-GBP amount=1500`
- `JPY-USD amount=1500`
- `USD-INR amount=1500`
- `USD-AUD amount=1500`
- `PHP-USD amount=20000`
- `EUR-USD amount=1500`
- `JPY-USD amount=1500`
- `HKD-USD amount=1500`

## 结果

12 个 compare URL 当前全部返回：

- Status：`500`
- Title：空
- Meta：空
- Canonical：空
- Robots：空

## 影响

这批页面在 GSC 中已经有明显曝光，但线上 live 状态不可用。

仅 Top30 中这 12 个 compare 页合计曝光已经超过 11 万级别，且多数 CTR 接近 0。

这意味着：

- 页面已经有搜索需求
- 页面当前无法承接点击和转化
- 继续做 title/meta 改稿没有意义
- 必须先修模板路由或服务端渲染问题

## P0 修复目标

Compare 模板修复必须一次性覆盖：

- `best-XXX-YYY-exchange-rate`
- `best-XXX-YYY-exchange-rates`
- `amount` query parameter
- 不同金额值
- 不同币种 pair

## 验收标准

修复完成后，至少抽样验证：

- Top30 里的 12 个 compare URL 全部返回 `200`
- title 非空
- meta description 非空
- canonical 明确
- robots 可索引
- amount 参数不会触发 `500`
- plural/singular route 都有明确处理策略

## SEO 改造暂缓规则

在 compare 模板修复前：

- 不进入 CMS 发布
- 不写最终 title/meta handoff
- 不做内容团队派工
- 只保留 SEO 模板规格和修复后标题方向

## 修复后优先顺序

修复通过后，优先处理：

1. `USD-PHP amount=1500`
2. `AED-INR amount=3000`
3. `AED-INR amount=1500`
4. `USD-PKR amount=1500`
5. `USD-GBP amount=1500`

原因：

- 曝光最高
- CTR 极低
- 商业价值高

## 当前结论

Compare 不是内容问题，当前是技术可用性问题。

Wave 1 模板页执行顺序应调整为：

1. 先发布 6 个 converter 页面
2. 并行修复 compare 模板 `500`
3. compare 修复验收后，再进入 compare SEO handoff