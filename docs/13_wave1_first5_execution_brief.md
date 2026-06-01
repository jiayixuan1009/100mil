# Wave 1 第一批 5 页执行 Brief

## 文档目标

本 brief 用于将 Wave 1 前 5 个优先页面拆成真正可执行的动作，并明确哪些页面可以直接改稿，哪些页面需要先做 overlap review 或 live 校验。

## 页面范围

当前前 5 页全部属于 `blogdetail` 高曝光页：

1. `chase atm withdrawal limit` 对应英文页
2. `chase atm withdrawal limit` 对应另一条主站页
3. `+52 country code`
4. `atm withdrawal limit bank of america`
5. `wechat real name verification`

## 当前分流结论

更新说明：2026-06-01 已完成 live URL 校验，详见 [22_wave1_live_url_validation_update.md](22_wave1_live_url_validation_update.md) 和 [24_wave1_live_metadata_audit.md](24_wave1_live_metadata_audit.md)。旧判断中关于 Chase 页面 `502 / Non-Indexable` 的状态已过期；当前 5 个修正后 URL 均为 `200 / index, follow / self canonical`。

### A 组：可直接推进改稿

这些页面当前技术门槛可控，可以先做标题、meta、首屏、FAQ、桥接模块：

- `+52 country code`
- `atm withdrawal limit bank of america`
- `wechat real name verification`

共同特征：

- 状态码 `200`
- `Indexable`
- 主要问题集中在 `title too long`、`meta too long`
- 适合先做 CTR 提升和商业桥接测试

### B 组：先做 overlap review，再决定是否同时发布

这些页面当前不适合不加判断地同时进入发布：

- `chase atm withdrawal limit` 2320 英文页：当前 live 校验已恢复 `200`
- `chase atm withdrawal limit` 1071 英文页：当前修正 URL 后 live 校验为 `200`

结论：

- 第 1 页和第 2 页先判断 query overlap、canonical 分工和内链主推版本。
- 两页可以先写稿，但不建议同时上线同方向改稿。

## A 组执行要求

### 标题

- 用精确问题词开头。
- 避免“guide”“complete guide”式空泛标题。
- 明确结果或用户关心的变量，如费用、限制、是否可行、替代方案。

### Meta Description

- 第一段直接预告答案。
- 第二段补结果边界，如限制、费用、国际使用条件。
- 最后给一个与 BiyaPay 相关的合理桥接动作。

### 首屏

- 开头 2-4 行直接回答问题。
- 紧接一个 3 点摘要。
- 不要用大段铺垫或纯背景解释。

### FAQ

- 围绕用户接下来最可能问的 4-6 个问题。
- 不做泛 FAQ。

### 商业桥接

- 费率相关页：引导到 compare / converter / start transfer。
- 身份验证或工具相关页：引导到工具页、汇率页或下载页。
- 桥接必须解释“为什么这个下一步对当前问题有帮助”。

## 每页重点

### 1. +52 country code

重点：

- 这是工具型信息意图，不要硬切金融广告。
- 商业桥接应偏“国际沟通/跨境场景下一步”。
- 可以弱桥接到汇率或跨境工具，而不是强卖产品。

### 2. ATM withdrawal limit bank of america

重点：

- 用户更关心限额、费用、跨境取现可行性。
- 可以桥接到低成本跨境转账/换汇方案。

### 3. WeChat real name verification

重点：

- 这是很强的海外用户场景问题。
- 桥接应围绕海外身份验证、跨境支付、转账替代方案。

## 技术先行动作

### chase atm withdrawal limit 两页

- 先确认 2320 与 1071 的查询分工
- 先确认站内链接主推哪一页
- 先决定是否一页主打 `ATM withdrawal limit`，另一页主打 `increase Chase withdrawal limit`
- 如无法区分意图，只发布其中一页，另一页先不大改

## 输出要求

这 5 页推进时，必须至少输出：

- 标题定稿
- meta description 定稿
- 首屏摘要文案骨架
- FAQ 主题清单
- 商业桥接模块文案骨架
- CTA 和内链建议