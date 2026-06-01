# 阶段一：数据口径与 SEO 机会页执行方案

## 阶段目标

阶段一周期为 7-10 天，目标是先建立可信增长判断，再输出第一批可执行 SEO 页面清单。

阶段一不以大规模改页面为主，而是完成以下五件事：

- 把 GA4 数据污染清出来。
- 把 Direct 流量拆清楚。
- 把注册、KYC、入金、交易漏斗缺口列清楚。
- 把 GSC 第一批高价值机会 URL 排出来。
- 把 Top 200 URL 的基础技术状态补齐。

## 一、GA4 hostname 清洗

### 背景

历史审计数据已经发现 GA4 存在 hostname 污染。除核心生产域外，还出现了 signup、active、PRV、DEV、localhost、内网 IP 等来源。

### 数据维度

需要拉取近 90 天 GA4 数据：

- hostname。
- default channel group。
- landing page + query string。
- country。
- device category。
- browser。
- operating system。
- sessions。
- active users。
- engaged sessions。
- key events。

### 分类规则

生产和业务域：

- www.biyapay.com：保留，主站增长核心。
- invest.biyapay.com：保留，单独分析。
- news.biyapay.com：保留，单独分析。
- signup.biyapay.com：保留为转化域，但不作为 SEO 着陆增长页。

异常或污染域：

- localhost。
- 内网 IP。
- PRV / DEV / test 环境。
- prv.cn.biyapay.io。
- prv.www.biyapay.io。
- 其他非生产 hostname。

### 交付物

输出 `phase1_ga4_hostname_cleaning.csv`，字段建议：

- hostname。
- sessions。
- active_users。
- engaged_sessions。
- key_events。
- top_channel。
- top_landing_page。
- top_country。
- top_device。
- hostname_type。
- include_in_growth_reporting。
- issue。
- recommendation。

### 判断标准

- 正式增长报表只统计生产和业务域。
- signup 域进入转化链路分析，但不计入 SEO 着陆页增长页。
- 测试、预发、本地、内网来源必须从正式增长口径中排除。

## 二、Direct 流量专项

### 背景

近 90 天 GA4 Direct sessions 占比异常高，必须判断其中多少是真实直接访问，多少是归因丢失、跨域断裂、App/WebView、测试环境、爬虫或异常访问。

### 拆解维度

需要拉取并交叉分析：

- Direct × landing page。
- Direct × hostname。
- Direct × country。
- Direct × device。
- Direct × browser。
- Direct × operating system。
- Direct × page referrer。
- Direct × first user source / medium。
- Direct × session source / medium。
- Direct × event name。

### 重点异常入口

优先检查：

- `(not set)`。
- `/download`。
- `/login`。
- `/404`。
- `/zh?id=...` 参数页。
- signup 域。
- invest / www / news 跨域跳转。
- Windows 桌面异常集中流量。
- 单国家、单设备、单浏览器异常集中流量。
- 无 engagement、无 key event、会话时长极短的 Direct。

### Direct 分类

将 Direct 分成七类：

- A 类：真实品牌或直接访问。
- B 类：跨域归因丢失。
- C 类：App/WebView 或下载页回流。
- D 类：登录、注册、支付回跳。
- E 类：测试环境污染。
- F 类：爬虫、机器流量或异常访问。
- G 类：暂时无法判断，需要日志复核。

### 交付物

输出 `phase1_direct_traffic_breakdown.csv`，字段建议：

- landing_page。
- hostname。
- sessions。
- active_users。
- engaged_sessions。
- avg_engagement_time。
- key_events。
- country。
- device。
- browser。
- operating_system。
- suspected_type。
- evidence。
- recommendation。

### 阶段结论格式

Direct 专项最终需要回答：

- 90 天总 Direct sessions 是多少。
- 可解释 Direct 占比是多少。
- 应排除的污染 Direct 占比是多少。
- 需要技术修复的 Direct 类型有哪些。
- 哪些 Direct 应进入日志层复核。

## 三、转化事件审计

### 背景

当前已知 `user_register` 存在，但 deposit / trade 事件缺失或未映射。阶段一必须明确漏斗缺口，避免用不完整事件误判 SEO 质量。

### 必查事件

- user_register。
- kyc_start。
- kyc_success。
- deposit_start。
- deposit_success。
- trade_start。
- trade_success。
- download_app。
- click_signup。
- click_download。

### 交付物

输出 `phase1_conversion_event_audit.csv`，字段建议：

- business_action。
- ga4_event_exists。
- current_event_name。
- is_key_event。
- hostname。
- cross_domain_risk。
- data_owner。
- priority。
- fix_requirement。

### 判断标准

- 有事件且能跨域串联，才进入正式转化漏斗。
- 没有 deposit/trade 事件时，不得对 SEO 入金/交易转化下结论。
- 阶段一至少要产出埋点修复需求。

## 四、GSC Top 200 SEO 机会页

### 筛选规则

从近 90 天和 16 个月 GSC 数据中筛选：

- impressions >= 1000。
- average position > 3。
- average position <= 20。
- CTR 低于同排名预期。
- 优先商业价值高页面。

### 优先页面类型

- converter。
- compare。
- sendmoney。
- iban。
- swift。
- bank code。
- high-impression blogdetail。
- download / homepage / language homepage。

### 分层规则

- A 类：排名 4-10，CTR 低，最快提点击。
- B 类：排名 11-20，曝光高，适合内容增强和内链。
- C 类：曝光高但排名差，适合重构、合并或重新匹配搜索意图。
- D 类：有点击但转化差，适合 CTA 和产品路径优化。

### 交付物

输出 `phase1_gsc_top200_seo_opportunities.csv`，字段建议：

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
- priority。
- owner。

### 第一批执行建议

阶段一结束时，从 Top 200 中挑出 Top 30，进入阶段二页面优化。

Top 30 优先条件：

- impressions 高。
- position 在 4-10。
- CTR 明显偏低。
- 页面商业意图强。
- 技术状态可快速修复。

## 五、Top 200 技术状态补充

### 数据源

使用 Screaming Frog、GSC 和 live URL 检查补齐 Top 200 的技术状态。

### 检查项

- status code。
- indexability。
- canonical。
- hreflang。
- title。
- meta description。
- H1。
- inlinks。
- orphan status。
- structured data。
- response time 或 CWV 风险。

### 交付物

输出 `phase1_top200_technical_status.csv`，字段建议：

- url。
- status_code。
- indexability。
- canonical。
- hreflang_status。
- title。
- title_issue。
- meta_description。
- meta_issue。
- h1。
- h1_issue。
- inlinks。
- orphan_status。
- structured_data_status。
- technical_priority。
- fix_recommendation。

## 六、日程安排

### Day 1

- 拉 GA4 hostname、channel、landing、device、country 数据。
- 初步标记生产域、业务域、测试域、异常域。

### Day 2

- 拆 Direct × landing / hostname / device / country。
- 初步识别异常 Direct 类型。

### Day 3

- 核对 GA4 事件。
- 输出 register / KYC / deposit / trade 漏斗缺口。

### Day 4

- 拉 GSC 页面 + 查询数据。
- 生成 Top 200 SEO 机会页初版。

### Day 5

- 用 Screaming Frog 数据补充 Top 200 的 title、meta、H1、canonical、indexability、inlinks。

### Day 6

- 合并 GA4、GSC、Screaming Frog 数据。
- 给每个 URL 标记优先级和动作。

### Day 7

- 输出阶段一报告。
- 确定阶段二第一批 Top 30 页面。

## 七、阶段一最终交付包

阶段一结束时必须交付：

- `phase1_ga4_hostname_cleaning.csv`。
- `phase1_direct_traffic_breakdown.csv`。
- `phase1_conversion_event_audit.csv`。
- `phase1_gsc_top200_seo_opportunities.csv`。
- `phase1_top200_technical_status.csv`。
- 阶段一总结报告。
- 阶段二 Top 30 页面执行清单。

## 八、成功标准

- 能说清 90 天总流量里有多少是真实可运营流量。
- 能说清 Direct 里最大的 5 类来源。
- 能说清 GA4 漏斗缺了哪些事件。
- 能拿出 200 个具体 URL，而不是泛泛 SEO 建议。
- 能确定阶段二第一批要改的 30 个页面。

## 九、下一步

阶段一应从 Direct 流量专项和 hostname 清洗开始，同时并行拉 GSC Top 200 机会页。这样第一周结束时既有可信数据口径，也有可执行 SEO 页面清单。