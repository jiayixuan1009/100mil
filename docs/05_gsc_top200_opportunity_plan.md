# GSC Top 200 机会页专项文档

## 专项目标

从 BiyaPay 当前已经获得 Google 曝光的页面中，筛出最值得优先优化的 200 个 URL，并给出明确的页面分层、问题判断、执行动作和预估点击增量。

## 为什么先做这个专项

当前增长重点不是继续堆页面数量，而是把已有曝光和已有排名转成点击和业务路径。GSC 机会页是最快产生增量的资产池。

## 数据来源

- live GSC 查询数据。
- 已读取的 16 个月 GSC 导出数据。
- 页面类型识别规则。
- Screaming Frog 技术字段。
- GA4 着陆页和转化辅助信息。

## 筛选规则

基础筛选条件：

- impressions >= 1000。
- average position > 3。
- average position <= 20。
- CTR 低于同排名预期。
- 页面具备明确商业意图或可导向业务路径。

## 优先页面类型

- compare。
- converter。
- sendmoney。
- iban。
- swift。
- bank code。
- homepage / language homepage。
- high-impression blogdetail。
- download / product-intent 页面。

## 机会页分层

### A 类：高曝光、4-10 名、CTR 低

特点：

- 最容易通过改标题、摘要、首屏内容和结构提升点击。

### B 类：高曝光、11-20 名

特点：

- 需要内容增强、内链加强、模板字段补齐。

### C 类：高曝光、低排名或意图错配

特点：

- 需要重构页面或重新匹配搜索意图。

### D 类：有点击但转化差

特点：

- 需要产品 CTA、模块、路径设计优化。

## 交付表结构

输出表：`phase1_gsc_top200_seo_opportunities.csv`

建议字段：

- url。
- page_type。
- clicks。
- impressions。
- ctr。
- avg_position。
- primary_query。
- secondary_queries。
- opportunity_class。
- current_problem。
- recommended_action。
- estimated_click_uplift。
- estimated_business_value。
- priority。
- owner。

## 动作模板

### 标题和摘要改造

适用情况：

- 排名尚可但 CTR 偏低。

动作：

- 改 title。
- 改 meta description。
- 对齐搜索意图。
- 加入更明确的年份、范围、费用、到账时间、地区等信息。

### 首屏和结构增强

适用情况：

- 排名 8-20，需要更强的主题匹配和信息完整度。

动作：

- 改 H1。
- 增加首屏摘要。
- 增加 FAQ。
- 增加结构化字段。
- 增加更新时间和数据来源。

### 内链和模板升级

适用情况：

- 工具页、线路页、比较页、汇率页。

动作：

- 增加相关国家、币种、银行、工具页内链。
- 增加产品 CTA。
- 增加相关问题模块。

## 第一批执行要求

Top 200 里必须先筛出 Top 30 页面，作为阶段二第一批执行名单。

Top 30 优先标准：

- 曝光高。
- 排名 4-10。
- CTR 明显低于预期。
- 页面商业价值高。
- 技术状态可短期修复。

## 阶段二输入

本专项结束后，必须给阶段二提供：

- Top 30 URL 名单。
- 每个 URL 的问题判断。
- 每个 URL 的动作建议。
- 每个 URL 的技术状态摘要。
- 每个 URL 的预估点击增量。