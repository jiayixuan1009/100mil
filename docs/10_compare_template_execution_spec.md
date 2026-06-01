# Compare 模板执行规格

## 目标

Compare 页的目标不是只生成一个 `best exchange rate` URL，而是让用户和搜索引擎一眼看懂：

- 比较的是什么币种对。
- 比较的是哪个金额。
- 当前结果对用户有什么决策价值。
- 用户下一步可以直接做什么。

## 适用页面

- `/compare/best-XXX-YYY-exchange-rate`
- 带 `amount` 参数的 compare 页面
- 其他币种/金额对比页

## 标题规则

- 直接包含币种对和比较意图。
- 优先覆盖“today / best / exchange rate / amount”这类高意图信号。
- 不写泛泛模板文案，不重复品牌词堆砌。

示例方向：

- `Best USD to PHP Exchange Rate Today for 1500 USD`
- `Compare the Best AED to INR Exchange Rate for 3000 AED`
- `USD to GBP: Best Exchange Rate Today With Amount Guide`

## Meta Description 规则

- 先给结果导向的摘要。
- 明确金额上下文。
- 点出费用、汇率差、到账场景或实用价值。
- 最后给一个下一步动作。

## 首屏模块

首屏必须包含：

- 明确的页面 H1。
- 当前比较结果摘要。
- amount 输入或展示区域。
- 更新时间。
- 简短说明为何该结果有用。
- 主 CTA。

首屏不应出现：

- 长篇背景介绍。
- 与对比主题无关的品牌铺垫。
- 无更新时间的静态结论。

## 内容模块

建议模块顺序：

1. 结果摘要
2. amount 和币种上下文
3. 手续费 / spread / 到账时间说明
4. 为什么该 pair 会波动
5. 相关币种或相邻金额推荐
6. FAQ
7. 产品 CTA

## FAQ 方向

- 哪个金额下汇率更划算。
- 是否有隐藏价差或手续费。
- 汇率多久更新一次。
- 大额转账时应该注意什么。
- 与银行 / 钱包 / remittance provider 的差异是什么。

## 内链规则

- 链接到对应 converter 页。
- 链接到相关 sendmoney corridor 页。
- 链接到相邻金额 compare 页。
- 链接到相关银行/工具页（若有业务关联）。

## CTA 规则

主 CTA：

- `Check Live Rate`
- `Start Transfer`

次 CTA：

- `Download App`
- `Compare Another Amount`

## 执行注意事项

- Compare 页必须优先确认技术基线，尤其是当前 `out_of_www_0518_scope` 的页面。
- 同一模板内的 copy 和模块顺序要统一，方便批量迭代。
- 不要只改 title，不改首屏和 CTA。