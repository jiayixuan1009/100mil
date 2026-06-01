# Wave 1 Converter 模板页灰度上线方案

## 文档用途

本文件用于推进 Top30 中第一批 converter 模板页，避免只做单页博客优化。

配套文件：

- `phase2_wave1_converter_cms_handoff.csv`
- `phase2_wave1_template_live_metadata.csv`
- `phase2_wave1_template_launch_tracker.csv`

## 页面范围

本轮 converter 灰度页共 6 个：

- `JPY-HKD`
- `EUR-USD`
- `THB-USD`
- `JPY-USD`
- `PHP-USD`
- `AED-PKR`

这些页面当前均已 live 校验：

- `200`
- `index, follow`
- self canonical

## 当前主要问题

### 1. H1 过于通用

中文 converter 当前 H1 多为 `实时汇率`，没有体现币种对。

建议改为：

- `日元兑港元汇率换算`
- `欧元兑美元汇率换算`
- `泰铢兑美元汇率换算`
- `日元兑美元汇率换算`
- `菲律宾比索兑美元汇率换算`

### 2. 标题可更贴近自然查询

当前标题能表达币种对，但缺少金额示例和实时汇率上下文。

建议模板：

- 中文：`{币种A}兑{币种B}汇率换算：{PAIR} 实时汇率与金额示例`
- 英文：`{PAIR} Converter: Live {Currency A} to {Currency B} Rate`

### 3. 首屏需要更像工具

首屏必须优先展示：

- 实时汇率结果
- 更新时间
- amount 输入或常用金额 chips
- 费用/到账上下文
- CTA

不要把工具页做成文章页。

## 发布顺序

建议按曝光优先发布：

1. `JPY-HKD`
2. `EUR-USD`
3. `THB-USD`
4. `JPY-USD`
5. `PHP-USD`
6. `AED-PKR`

## CMS 交付口径

所有最终 title、H1、meta、首屏答案、CTA、内链说明，统一使用：

- `phase2_wave1_converter_cms_handoff.csv`

不要在 CMS 中临时重写标题，否则无法复盘模板效果。

## 监控口径

上线后用：

- `phase2_wave1_template_launch_tracker.csv`

观察窗口：

- T+14
- T+28

观察指标：

- CTR
- average position
- impressions
- converter 到 compare / transfer / download 的点击

## 成功标准

至少满足一个：

- CTR 提升
- 平均排名提升
- 页面点击提升
- 工具交互或 CTA 点击提升

## 失败处理

### CTR 不动

- 先调整 title
- 再调整 meta
- 再调整金额 chips 和首屏文案

### 排名下降

- 检查是否标题偏离原始查询
- 检查是否误删关键词
- 检查是否内链变化造成权重流失

## 下一步

第一批 6 个 converter 发布 14 天后，判断是否把同一模板扩展到 Top30 中的 compare 页面和更多 converter 页面。