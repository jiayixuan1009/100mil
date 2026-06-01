# Wave 1 第一批 5 页实时 Metadata 审计

## 审计时间

2026-06-01

## 审计结论

修正 URL 后，第一批 5 页当前均返回：

- `200`
- `index, follow`
- self canonical

这推翻了旧执行判断中的一部分技术阻塞结论。当前主要问题不是页面不可用，而是 title / meta 长度、SERP 匹配和 Chase 主题重叠。

## 页面状态

### 2320 Chase 页面

URL：`https://www.biyapay.com/en/blogdetail/2320-how-the-chase-withdrawal-limit-works-for-your-acco`

- Status：`200`
- Robots：`index, follow`
- Canonical：self
- Current title length：68
- Current meta length：144
- 当前动作：可以写稿，但发布前需和 `1071` 做查询分工。

### 1071 Chase 页面

URL：`https://www.biyapay.com/en/blogdetail/1071-what-is-the-withdrawal-limit-of-chase-and-can-it-b`

- Status：`200`
- Robots：`index, follow`
- Canonical：self
- Current title length：77
- Current meta length：291
- 当前动作：优先压缩 meta，并和 `2320` 做 overlap review。

### 1058 +52 country code 页面

URL：`https://www.biyapay.com/en/blogdetail/1058-telephone-area-codes-in-mexico-country-code-52-sim`

- Status：`200`
- Robots：`index, follow`
- Canonical：self
- Current title length：100
- Current meta length：291
- 当前动作：可进入第一波发布，重点压缩 title/meta 并强化首屏直答。

### 1054 Bank of America 页面

URL：`https://www.biyapay.com/en/blogdetail/1054-what-is-the-withdrawal-limit-of-bank-of-america-at`

- Status：`200`
- Robots：`index, follow`
- Canonical：self
- Current title length：68
- Current meta length：268
- 当前动作：可进入第一波发布，重点压缩 meta 并补跨境费用桥接。

### 2572 WeChat 页面

URL：`https://www.biyapay.com/en/blogdetail/2572-wechat-realname-authentication-how-overseas-users`

- Status：`200`
- Robots：`index, follow`
- Canonical：self
- Current title length：111
- Current meta length：230
- 当前动作：可进入第一波发布，重点压缩 title/meta 并减少重复词。

## 当前优先级调整

### 第一批可上线

- `1058`
- `1054`
- `2572`

### 需先做 overlap review

- `2320`
- `1071`

## 发布前新增规则

每个 Wave 1 页面发布前必须补一行 live 校验：

- status code
- final URL
- canonical
- robots
- title length
- meta length

这一步优先级高于旧 crawl 表。