# Chase 两页技术排查清单

## 文档用途

本文件用于单独处理当前前 5 页中最不适合直接发布的两页 Chase 页面。

目标是先回答一个简单问题：

这两页里，谁才是应该保留并继续优化的主版本？

## 页面范围

### 页面 A

`https://www.biyapay.com/en/blogdetail/2320-how-the-chase-withdrawal-limit-works-for-your-acco`

当前更新：

- 旧 0518 抓取中为 `502 / Non-Indexable / P0`
- 2026-06-01 线上复查为 `200 / index, follow / self canonical`
- 当前风险从“技术死页”转为“与 1071 页面主题重叠”

### 页面 B

`https://www.biyapay.com/en/blogdetail/1071-what-is-the-withdrawal-limit-of-chase-and-can-it-b`

当前更新：

- 旧执行表中使用了截断/非英文路径
- 2026-06-01 修正为英文 canonical 路径后，线上复查为 `200 / index, follow / self canonical`
- 当前风险是与 2320 页面共同覆盖 `chase atm withdrawal limit` 查询簇

## 排查顺序

### 1. 先查线上真实状态

- 页面 A 是否持续返回 `200`
- 页面 B 是否持续返回 `200`
- 两页是否都可访问

### 2. 再查索引与 canonical

- 哪一页是 canonical 主版本
- 是否存在互相 canonical、重定向或重复内容关系
- 是否有一页只是旧版本或异常版本

### 3. 再查内部链接状态

- 当前站内主要链接是否指向页面 A
- 当前站内主要链接是否指向页面 B
- 页面 B 的 `orphan` 是真实孤立，还是 crawl 覆盖缺失造成

### 4. 再决定内容动作

- 如果 A 恢复正常且是主版本，则保留 A，B 做合并或重定向策略评估
- 如果 B 才是主版本，则 A 不应继续作为优先优化目标
- 如果两页都有效且服务不同语言/路径逻辑，需先补清 canonical 和内链逻辑

## 必查字段

- status code
- indexability
- canonical
- meta robots
- title
- meta description
- H1
- inlinks
- last modified

## 暂停规则

在以下任一情况未明确前，Chase 两页不应同时进入内容发布：

- 两页查询分工不明确
- canonical 主版本不明确
- 内链主推页面不明确
- 页面意图无法区分，存在 cannibalization 风险

## 完成标准

当以下问题都回答清楚后，Chase 两页才算具备进入下一步内容优化的条件：

- 哪个 URL 是主版本
- 另一个 URL 应保留、合并还是重定向
- 主版本是否可索引且可抓取
- 主版本是否已经具备 title/meta/H1 优化条件