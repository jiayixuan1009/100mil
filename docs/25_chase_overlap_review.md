# Chase 两页查询重叠专项 Review

## 文档用途

本文件用于决定两个 Chase 页面是否应该同时改稿，以及谁应作为 `chase atm withdrawal limit` 查询簇的主推页面。

配套数据文件：

- `phase2_chase_overlap_queries.csv`
- `phase2_wave1_first5_gsc_url_variants_live.csv`

## 数据口径

时间范围：2026-03-01 至 2026-05-31

数据源：GSC `sc-domain:biyapay.com`

聚合方式：按文章 ID 聚合 URL 变体，而不是只看当前 canonical URL。

原因：

- 旧 GSC 数据中存在截断 slug、旧 slug、语言路径等 URL 变体。
- 如果只按 exact URL 拉取，会低估历史曝光。
- 本次用 `/2320-` 和 `/1071-` 聚合，判断更接近真实查询分布。

## 核心发现

### 1. 两页确实高度重叠

Top overlap 查询包括：

- `chase atm withdrawal limit`
- `chase atm limit`
- `how much can i withdraw from chase atm`
- `chase withdrawal limit`
- `chase bank atm withdrawal limit`

这些词不是边缘重叠，而是核心词重叠。

### 2. 1071 在聚合口径下更适合作为主推页

按 URL 变体聚合后，Top 查询中 `1071` 通常获得更多曝光：

- `chase atm withdrawal limit`：1071 高于 2320
- `chase atm limit`：1071 高于 2320
- `how much can i withdraw from chase atm`：1071 高于 2320
- `chase withdrawal limit`：1071 高于 2320
- `chase bank atm withdrawal limit`：1071 高于 2320

结论：

- `1071` 更适合承接 Chase ATM withdrawal limit 主查询簇。
- `2320` 不建议和 `1071` 同时用相似标题、相似首屏去抢同一批词。

### 3. 2320 适合做差异化定位

`2320` 可以转向更具体的角度，例如：

- account-specific withdrawal rules
- how Chase withdrawal limits work by account
- how to check or manage withdrawal limit
- fees and alternatives for international cash access

这能减少 cannibalization，同时保留页面资产。

## 推荐分工

### 1071 主推方向

主查询簇：

- `chase atm withdrawal limit`
- `chase atm limit`
- `chase withdrawal limit`
- `how much can i withdraw from chase atm`

建议标题：

- `Chase ATM Withdrawal Limit: Daily Caps, Fees, and How to Increase It`

首屏重点：

- 直接回答每日 ATM 取现限额不是固定值
- 给出典型范围与影响因素
- 解释如何检查或提高限额
- 补充国际使用成本和替代方案

### 2320 差异化方向

主查询簇：

- `how the Chase withdrawal limit works`
- `Chase withdrawal limit by account`
- `Chase debit card limit`
- `how to change Chase ATM withdrawal limit`

建议标题：

- `How the Chase Withdrawal Limit Works by Account, Card, and ATM`

首屏重点：

- 解释账户、卡、ATM 网络如何影响限额
- 不抢 `What is the Chase ATM withdrawal limit` 这个主答案位
- 作为 1071 的补充说明页

## 内链策略

- 从 2320 链到 1071，锚文本使用 `Chase ATM withdrawal limit`。
- 从 1071 链到 2320，锚文本使用 `how Chase withdrawal limits work by account`。
- 不要两个页面都用同一组内部锚文本抢 `chase atm withdrawal limit`。

## 发布规则

### 第一轮只建议发布一个主 Chase 页面

优先发布：

- `1071`

暂缓大改：

- `2320`

### 2320 的处理方式

- 可以微调 title/meta，避免过度重复。
- 不做与 1071 一样的首屏结构。
- 等 1071 发布 14-28 天后，看查询分布再决定是否改 2320。

## 复盘指标

- `1071` 是否获得更多核心查询点击
- `2320` 的核心查询曝光是否被自然分流到长尾解释词
- 两页合计点击是否提升
- 是否出现其中一页 impressions 大幅掉、另一页未补上的情况

## 当前结论

Chase 两页不能作为普通“两个可上线页面”处理。它们是同主题页面组，需要按查询簇分工。

本轮建议：

- `1071` 作为 Chase 主推页进入下一批发布。
- `2320` 作为解释型补充页暂缓大改。