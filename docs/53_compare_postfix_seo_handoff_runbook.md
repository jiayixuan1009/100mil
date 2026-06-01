# Compare 修复后 SEO Handoff Runbook

这个 runbook 只在 compare P0 工程修复通过后使用。

当前 compare 仍是 `12 checked / 0 passed / 12 failed`，因此本文件不是发布指令，而是修复通过后的预案，避免工程修好后 SEO 侧再重新排序和准备。

## 启动条件

必须先运行：

```bash
.venv/bin/python scripts/validate_compare_live_urls.py
```

只有 12 个 P0 URL 全部满足以下条件，才启动本 handoff：

- status = `200`
- title 非空
- meta description 非空
- H1 非空
- canonical 非空
- robots 可索引
- 页面保留 pair 和 amount 语境

## 优先级种子

配套 CSV：`docs/phase3_compare_postfix_seo_handoff_seed.csv`

第一批先做前 5 个：

1. `USD-PHP amount=1500`
2. `AED-INR amount=3000`
3. `AED-INR amount=1500`
4. `USD-PKR amount=1500`
5. `USD-GBP amount=1500`

原因：曝光最高、当前 CTR 低、修复后最容易先验证 template lift。

## Handoff 内容

每个 URL 修复通过后再补：

- final title
- final meta description
- H1
- 首屏 exchange-rate 摘要
- fee / spread / delivery-time 模块要求
- FAQ
- CTA
- converter / sendmoney / related compare 内链
- canonical 策略确认

## 当前不做什么

- 不在 `12/12 pass` 前写最终 CMS handoff。
- 不让内容团队先改 compare 页面。
- 不把 compare 放入上线 tracker。

## 状态流转

1. 当前：`waiting_on_12_of_12_pass`
2. 工程修复后：运行 live regression
3. 如果 `12/12 pass`：把 seed CSV 的前 5 个改成 `ready_for_seo_handoff`
4. 生成 compare title/meta/CMS handoff
5. 上线后进入 measurement tracker
