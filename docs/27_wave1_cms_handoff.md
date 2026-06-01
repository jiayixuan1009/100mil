# Wave 1 CMS Handoff 说明

## 文档用途

本文件说明 `phase2_wave1_cms_handoff.csv` 的使用方式。

这张表是给内容、运营、CMS 发布同事使用的交付表，避免他们再从多个策略文档里拼 title、meta、H1、CTA。

## 配套文件

- `phase2_wave1_cms_handoff.csv`

字段包括：

- `publish_order`
- `page_key`
- `canonical_url`
- `status`
- `final_title`
- `final_h1`
- `meta_description`
- `first_screen_answer`
- `primary_cta`
- `secondary_cta`
- `internal_link_notes`
- `measurement_key`

## 发布顺序

### 直接进入编辑发布流

1. `country_code_1058`
2. `boa_1054`
3. `wechat_2572`

这 3 页已完成：

- live URL 校验
- title/meta/H1 方向
- 首屏直答骨架
- CTA 和内链方向
- GSC 基线
- 上线后监控规则

### Chase 页面

4. `chase_1071`

发布前动作：

- 先确认 1071 作为 Chase ATM withdrawal limit 主推页。
- 站内主锚文本优先指向 1071。
- 2320 不同步做同方向大改。

暂缓：

- `chase_2320`

处理方式：

- 只做轻量去重。
- 定位为 account/card/ATM rules 补充解释页。
- 等 1071 发布 14-28 天后再决定是否深改。

## 发布前检查

每个页面进入 CMS 前需要确认：

- URL 与 `canonical_url` 一致
- final title 没有被 CMS 自动追加后变得过长
- meta description 没有被截断或覆盖
- H1 与页面主意图一致
- CTA 链接可点击
- 内链锚文本没有互相抢主关键词

## 发布后记录

发布后应在 `phase2_wave1_launch_tracker.csv` 中补：

- 实际发布时间
- 最终上线 title
- 最终上线 meta
- 发布人
- 是否改动了 URL/canonical

当前 tracker 还没有这些实际发布字段，下一轮可以扩展。

## 当前结论

Wave 1 已经具备从 SEO 策略进入 CMS 执行的条件。

先发布 3 个 ready 页面，再处理 Chase 主次分工，是当前风险最低、速度最快的顺序。