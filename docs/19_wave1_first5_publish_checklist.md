# Wave 1 第一批 5 页发布检查说明

## 文档用途

本文件说明 `phase2_wave1_first5_publish_checklist.csv` 的用途。

它的作用不是替代编辑流程，而是让 SEO、内容、产品在发布前用同一套口径检查：

- 哪些页面已经具备上线条件
- 哪些页面仍然卡在技术门槛
- 哪些内容模块已经准备齐

## 当前文件

- `phase2_wave1_first5_publish_checklist.csv`

字段包括：

- `url`
- `primary_query`
- `technical_gate`
- `title_meta_ready`
- `hero_summary_ready`
- `faq_ready`
- `internal_links_ready`
- `cta_ready`
- `publish_ready`
- `owner`

## 发布判断规则

### 可以进入编辑发布流

需要同时满足：

- `technical_gate = ok_with_minor_fixes`
- `title_meta_ready = yes`
- `hero_summary_ready = yes`
- `faq_ready = yes`
- `internal_links_ready = yes`
- `cta_ready = yes`

### 必须暂缓或先做 review

出现以下任一情况时先不发布：

- 页面返回异常状态码
- 页面不可索引
- canonical 主版本不明确
- 技术 crawl 覆盖缺失，无法判断真实页面状态
- 同查询簇页面过于重叠，可能互相抢排名

## 当前执行判断

### 可以优先上线评估的页面

- `https://www.biyapay.com/en/blogdetail/1058-telephone-area-codes-in-mexico-country-code-52-sim`
- `https://www.biyapay.com/en/blogdetail/1054-what-is-the-withdrawal-limit-of-bank-of-america-at`
- `https://www.biyapay.com/en/blogdetail/2572-wechat-realname-authentication-how-overseas-users`

### 必须先做 overlap review 的页面

- `https://www.biyapay.com/en/blogdetail/2320-how-the-chase-withdrawal-limit-works-for-your-acco`
- `https://www.biyapay.com/en/blogdetail/1071-what-is-the-withdrawal-limit-of-chase-and-can-it-b`

## 建议发布顺序

1. 先发 `+52 country code`
2. 再发 `Bank of America ATM withdrawal limit`
3. 再发 `WeChat real name verification`

这样做的好处是：

- 同时覆盖工具型问题页和金融问答页
- 能更快观察不同意图类型的 CTR / 展现变化
- 不会被 Chase 两页的技术问题拖慢第一波上线节奏

## 下一步

基于本清单，下一轮继续补：

- 这 3 个可上线页面的页面级最终改稿说明
- Chase 两页的技术排查清单
- 第一波上线后的 GSC 观察指标表