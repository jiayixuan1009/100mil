# Wave 1 上线监控方案

## 文档用途

本文件定义 Wave 1 页面上线后的观察方式，避免只发布、不复盘。

配套数据文件：

- `phase2_wave1_first5_launch_baseline_by_id.csv`
- `phase2_wave1_ready3_launch_baseline.csv`
- `phase2_wave1_launch_tracker.csv`
- `phase2_wave1_first5_gsc_url_variants_live.csv`

## 基线口径

时间范围：2026-03-01 至 2026-05-31

数据源：GSC `sc-domain:biyapay.com`

聚合方式：按文章 ID 聚合 URL 变体。

原因：

- 第一批页面存在旧 slug、截断 slug、语言路径等历史 URL 变体。
- 直接按当前 canonical exact match 会低估历史曝光。
- 上线复盘必须看“页面资产组”，不是只看某一个 URL 字符串。

## 当前基线摘要

### 1058：+52 country code

- Baseline clicks：13
- Baseline impressions：50,701
- Baseline CTR：0.03%
- Baseline avg position：6.47
- 状态：ready for editor review

观察重点：

- CTR 是否从极低水平提升
- title/meta 压缩后是否改善点击
- 工具型查询是否继续稳定曝光

### 1054：Bank of America ATM withdrawal limit

- Baseline clicks：17
- Baseline impressions：25,987
- Baseline CTR：0.07%
- Baseline avg position：9.28
- 状态：ready for editor review

观察重点：

- CTR 是否提升
- 平均排名是否靠近首页上半区
- CTA 点击是否能带到 compare/converter/sendmoney 路径

### 2572：WeChat real name verification

- Baseline clicks：46
- Baseline impressions：5,464
- Baseline CTR：0.84%
- Baseline avg position：6.04
- 状态：ready for editor review

观察重点：

- title 去重后 CTR 是否提升
- FAQ 是否覆盖海外用户验证失败原因
- 是否带来支付/下载路径点击

### 1071：Chase 主推候选页

- Baseline clicks：62
- Baseline impressions：53,942
- Baseline CTR：0.11%
- Baseline avg position：4.95
- 状态：overlap review required

观察重点：

- 是否作为 Chase 主页面承接核心查询
- 发布后是否吸收 2320 的重叠查询
- 两页合计点击是否提升

### 2320：Chase 补充候选页

- Baseline clicks：33
- Baseline impressions：35,732
- Baseline CTR：0.09%
- Baseline avg position：5.15
- 状态：overlap review required

观察重点：

- 是否应该差异化为 account/card/ATM rules 解释页
- 不建议与 1071 同时做同主题大改

## 上线顺序

### 第一批直接发布

1. `1058 +52 country code`
2. `1054 Bank of America ATM withdrawal limit`
3. `2572 WeChat real name verification`

### Chase 页面发布策略

1. 先发布 `1071` 作为 Chase 主推页。
2. `2320` 只做轻量去重和内链配合。
3. 14-28 天后，根据 GSC 查询分布决定是否深改 `2320`。

## 观察窗口

- T+0：记录发布时间、最终 title、meta、canonical、robots
- T+7：检查是否被抓取和是否开始出现新数据
- T+14：第一次 CTR / position 复盘
- T+28：决定保留、二次改标题、调整内链或拆分主题

## 成功标准

页面不需要一次达到最终目标，但至少应满足一个条件：

- CTR 提升
- 平均排名提升
- 页面点击提升
- 相关 CTA 点击提升
- 查询分布更清晰，减少互抢排名

## 失败处理规则

### CTR 没有提升

- 先改 title
- 再改 meta
- 再检查 SERP intent 是否匹配

### 排名下降

- 检查是否改动过大
- 检查是否丢失原有关键词覆盖
- 检查是否 cannibalization 加剧

### 曝光下降但点击不升

- 回看主查询是否被另一个页面吸走
- 检查 canonical 和内链指向
- 检查是否 title 偏离主词

## 下一步

- 将 `phase2_wave1_launch_tracker.csv` 作为上线后复盘主表。
- 每个页面发布后补充实际发布日期和最终 title/meta。
- 下一轮从 Top 30 中继续选择 compare/converter 页面进入同样流程。