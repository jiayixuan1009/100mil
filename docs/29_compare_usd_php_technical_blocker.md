# USD-PHP Compare 页技术阻塞说明

## 页面

`https://www.biyapay.com/compare/best-USD-PHP-exchange-rate?amount=1500`

## 当前发现

2026-06-01 live metadata 校验结果：

- Status：`500`
- Title：空
- Meta：空
- Canonical：空
- Robots：空

## 为什么这是 P0 阻塞

该页面在 GSC/Top30 中有明显机会：

- impressions：22,598
- avg position：7.89
- CTR：0.0%
- primary query：`1500 dollars to philippine peso`

但当前 live 页面返回 `500`，因此不能直接做 SEO 文案上线。

## 先修复什么

### 必须先满足

- 页面返回 `200`
- 页面可被抓取
- robots 为 `index, follow` 或等价可索引状态
- canonical 明确
- amount 参数不会导致服务端异常
- 无 amount 参数和有 amount 参数的 canonical 规则明确

### 再进入 SEO 改造

修复后再推进：

- Title
- Meta description
- H1
- 首屏结果摘要
- amount 输入/展示
- 费用、汇率、到账说明
- 相关 converter / compare 内链
- CTA

## 修复后建议标题

- `Best USD to PHP Exchange Rate Today for 1500 USD`

## 修复后建议 H1

- `Best USD to PHP Exchange Rate for 1500 USD`

## 修复后 Meta 方向

- Compare the best USD to PHP exchange rate for 1500 USD, see estimated PHP received, check fees and spread, and choose the next transfer action.

## 验收标准

修复完成后，必须重新生成或更新：

- `phase2_wave1_template_live_metadata.csv`
- `phase2_wave1_template_launch_tracker.csv`

并确认：

- live status 为 `200`
- canonical 不丢 amount 意图，或有清晰的 canonical 策略
- GSC 中该 URL 或对应 canonical 能继续承接 `1500 dollars to philippine peso`

## 当前结论

该 compare 页不进入本轮 CMS 发布。

先发布 6 个 converter 模板页；compare 页等 `500` 修复后再进入下一轮模板灰度。