# Wave 1 第一批 5 页实时 URL 校验更新

## 本次更新目的

本次更新用于修正第一批 5 页执行包中的两个问题：

- 部分 URL 来自旧表时被截断，导致线上校验时误判为 `404`
- 部分技术状态来自 0518 抓取，已经落后于当前线上状态

## 最新校验结论

### 当前确认返回 200 的页面

- `https://www.biyapay.com/en/blogdetail/2320-how-the-chase-withdrawal-limit-works-for-your-acco`
- `https://www.biyapay.com/en/blogdetail/1071-what-is-the-withdrawal-limit-of-chase-and-can-it-b`
- `https://www.biyapay.com/en/blogdetail/1058-telephone-area-codes-in-mexico-country-code-52-sim`
- `https://www.biyapay.com/en/blogdetail/1054-what-is-the-withdrawal-limit-of-bank-of-america-at`
- `https://www.biyapay.com/en/blogdetail/2572-wechat-realname-authentication-how-overseas-users`

## 本次发现

### 1. 第一批执行表里存在截断 URL

旧执行表中至少以下路径需要修正：

- `1071`：旧路径缺少 `/en/` 且 slug 版本不对
- `1058`：旧路径使用了旧 slug，当前应使用 `...country-code-52-sim`
- `1054`：旧路径使用了较短 slug，当前 live 版本应使用 `...bank-of-america-at`

### 2. 0518 技术表里有过期判断

- `2320` 在旧表里是 `502 / Non-Indexable / P0`
- 当前线上复查已返回 `200`

这说明阶段二执行时，不能完全依赖 0518 抓取结果，至少对 Wave 1 页面要做一次 live 校验。

### 3. Chase 两页的风险从“死页”变成“重叠”

当前更大的风险已经不是 `502`，而是：

- `2320` 与 `1071` 都是 live 页面
- 两页都覆盖 `chase atm withdrawal limit` 附近查询
- 如果同时大幅改稿并同时推，会有 cannibalization 风险

## 执行影响

### 可以直接继续推进的页面

- `1058`
- `1054`
- `2572`

### 可以继续准备文案，但发布前要加一道判断的页面

- `2320`
- `1071`

建议：

- Chase 两页先选一个主打版本进入第一波发布。
- 另一个版本先保留 draft，待 canonical / 内链 / 查询分工更清楚后再动。

## 本次同步动作

本次已同步修正：

- `phase2_wave1_first5_title_candidates.csv`
- `phase2_wave1_first5_publish_checklist.csv`
- `phase2_wave1_first5_support_modules.csv`

## 后续要求

- Wave 1 页面上线前，增加 live URL 校验步骤。
- 对高曝光重复主题页，发布前增加 query overlap review。