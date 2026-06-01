# Converter 模板执行规格

## 目标

Converter 页的目标不是只显示一个汇率，而是把“查汇率”升级成“可继续转账/换汇/决策”的工具页。

## 适用页面

- `/converter/XXX-YYY-converter`
- 中英文币对转换页

## 标题规则

- 标题直接体现币种对和转换意图。
- 可结合用户常见表达，例如“兑换”“等于多少”“实时汇率”。
- 优先匹配 GSC 中出现的自然语言查询。

示例方向：

- `JPY to HKD Converter: Live Exchange Rate and Amount Guide`
- `EUR to USD Converter With Live Rate and Transfer Context`
- `泰铢兑美元汇率换算：实时结果与金额示例`

## Meta Description 规则

- 说明该页面提供实时换算结果。
- 说明是否适合查大额/常用金额。
- 加入转账或费率上下文。
- 给出下一步动作。

## 首屏模块

首屏必须包含：

- 当前币种对结果。
- 更新时间。
- 常用金额 chips。
- 简短费率/用途说明。
- 主 CTA。

建议：

- 结果区域不要被长文案压下去。
- 优先把工具感做强，而不是写成长文章页。

## 内容模块

建议模块顺序：

1. 实时结果区
2. 常见金额示例
3. 历史或波动说明
4. 手续费 / 汇款 / 到账上下文
5. 相关币对和逆向币对
6. FAQ
7. 产品 CTA

## FAQ 方向

- 汇率多久更新一次。
- 转换结果是否包含手续费。
- 大额换汇和小额换汇是否一样。
- 转账时实际到账金额会受什么影响。
- 相关币种对如何查看。

## 内链规则

- 逆向币对页。
- 相邻币对页。
- 对应 compare 页。
- 对应 sendmoney corridor 页。

## CTA 规则

主 CTA：

- `Check Live Rate`
- `Start Transfer`

次 CTA：

- `Download App`
- `Compare Best Rate`

## 执行注意事项

- Converter 页最适合批量执行，必须先沉淀统一模板规则。
- 标题和首屏语言要贴近真实 query，而不是只保留内部命名。
- 页内一定要加产品承接，避免只拿到信息型流量。