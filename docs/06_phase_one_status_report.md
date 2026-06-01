# 阶段一当前进展报告

## 当前状态

阶段一已经从方案阶段进入实际产出阶段。当前已完成 5 份核心实物：

- `phase1_ga4_hostname_cleaning.csv`
- `phase1_direct_traffic_breakdown.csv`
- `phase1_conversion_event_audit.csv`
- `phase1_gsc_top200_seo_opportunities.csv`
- `phase1_top200_technical_status.csv`

这 5 份文件分别解决五个问题：

- 哪些 hostname 应进入正式增长口径，哪些应排除或单独分析。
- 当前 Direct 流量里，哪些更像真实 Direct，哪些更像归因丢失、下载回流、登录回跳、异常 host 或 404 异常入口。
- 注册、KYC、入金、交易相关事件在 GA4 里是否存在，是否可用于正式漏斗。
- 哪 200 个 GSC 页面最值得优先优化。
- 这 200 个页面目前有哪些基础技术问题。

## 一、已完成工作

### 1. GA4 hostname 清洗表

数据来源：

- `5-22/ga4_hostname_audit_28d_2026-04-24_to_2026-05-21.csv`

产出文件：

- `phase1_ga4_hostname_cleaning.csv`

当前共识别出 27 个 hostname，并按以下类型做了初步分类：

- `production_site`
- `conversion_domain`
- `preprod_or_test`
- `local_or_internal`
- `non_core_business_or_unknown`
- `external_or_invalid`

### 2. Direct 流量第一版拆解表

数据来源：

- live GA4 `properties/405662310`
- 时间范围：近 90 天
- 条件：`sessionDefaultChannelGroup = Direct`

产出文件：

- `phase1_direct_traffic_breakdown.csv`

当前已拉取并分类前 500 条 Direct 组合，维度包含：

- hostname
- landing page
- country
- device category
- browser
- operating system
- sessions
- active users
- engaged sessions
- average session duration
- key events

### 3. 转化事件审计表

数据来源：

- live GA4 `properties/405662310`
- 时间范围：近 180 天
- 方式：对候选事件名清单做精确探测

产出文件：

- `phase1_conversion_event_audit.csv`

审计目标覆盖：

- register
- KYC start / success
- deposit start / success
- trade start / success
- download app
- click signup
- click download

### 4. GSC Top 200 机会页表

数据来源：

- live GSC `sc-domain:biyapay.com`
- 时间范围：2026-03-03 至 2026-05-31
- 维度：`page` 与 `page + query`

产出文件：

- `phase1_gsc_top200_seo_opportunities.csv`

当前已从 716 个候选机会页中输出 Top 200，补充了：

- page type
- primary query
- secondary queries
- opportunity class
- current problem
- recommended action
- estimated click uplift
- estimated business value

### 5. Top 200 技术状态表

数据来源：

- `01 www/sf/0518 response_codes_all.csv`
- `01 www/sf/0518 page_titles_all.csv`
- `01 www/sf/0518 meta_description_all.csv`
- `01 www/sf/0518 h1_all.csv`
- `01 www/sf/0518 canonicals_all.csv`
- `01 www/sf/0518 orphan_pages.csv`

产出文件：

- `phase1_top200_technical_status.csv`

当前已补充的技术字段包括：

- status code
- indexability
- canonical
- meta robots / x-robots-tag
- title / title length
- meta description / meta length
- H1
- inlinks
- orphan status

## 二、阶段一当前发现

### 1. 生产域仍然是流量主体，但污染明显存在

按当前 28 天 hostname 审计结果汇总：

- `production_site`：3 个 host，约 147,800 active users
- `conversion_domain`：1 个 host，约 7,370 active users
- `preprod_or_test`：7 个 host，约 3,439 active users
- `non_core_business_or_unknown`：1 个 host，约 3,229 active users
- `external_or_invalid`：11 个 host，约 1,356 active users
- `local_or_internal`：4 个 host，约 66 active users

说明：

- 核心生产域仍是主要流量来源。
- 但预发、测试、非核心业务域和异常外部 host 已经足够进入阶段一治理范围，不能继续混在正式增长口径里。

### 2. 当前 hostname 风险最高的非核心 host

当前最值得优先关注的异常或需复核 host：

- `active.biyagl.com`
- `prv.cn.biyapay.io`
- `www.biyapays.com`
- `prv.www.biyapay.io`
- `prv.invest.biyapay.com`
- `www.biyaglobal.com`
- `localhost`
- `192.168.110.190`

其中：

- `active.biyagl.com` 目前被标记为 `non_core_business_or_unknown`，需要确认它是否应被纳入业务体系，或从正式增长报表中排除。
- `prv.*`、`localhost`、内网 IP 等已可直接判定为不应进入正式增长口径。

### 3. Direct 的头部异常已经足够明确

第一版 Direct 拆解结果中，按 `suspected_type` 汇总的 sessions 约为：

- `B_cross_domain_or_signup_attribution_loss`：19,563
- `G_needs_manual_review`：11,598
- `C_app_or_download_return_flow`：9,736
- `A_probable_true_direct_or_brand`：7,831
- `F_non_core_or_suspicious_host`：4,587
- `D_login_or_signup_return_flow`：2,598
- `F_broken_route_or_invalid_entry`：2,458
- `G_measurement_gap`：538
- `E_test_or_preprod_pollution`：284

这说明：

- 当前 Direct 里最大的可解释问题不是“真实品牌直访”，而是 `signup` 归因丢失和下载回流。
- `invest.biyapay.com /en/404` 已经出现在 Direct 头部，说明有明显的异常入口或错误路由问题。
- 真正可以比较放心计入“品牌/直接访问”的部分，目前在头部样本里并不是最大块。

### 4. 当前最明显的 Direct 异常入口

头部样本中最显著的页面包括：

- `signup.biyapay.com (not set)`
- `signup.biyapay.com /download`
- `invest.biyapay.com /en/404`
- `www.biyapay.com /en`
- `www.biyapay.com /en/login`
- `www.biyapay.com (not set)`
- `active.biyagl.com /zh?id=...`
- `www.biyapay.com /zh/login`
- `www.biyapay.com /zh/download`

这批结果足以支撑一个阶段判断：

- Direct 不能直接当“自然增长之外的真实直接访问”来看。
- 需要先把 signup、download、login、404、参数页等生命周期和异常入口从获客分析中拆出去。

### 5. 转化事件结论已经可以下初步判断

在 180 天 live GA4 候选事件探测中，当前明确命中的核心业务事件只有：

- `user_register`

并且它不仅出现在生产域，也出现在预发、测试、本地或异常 host 上，例如：

- `prv.invest.biyapay.com`
- `dev.invest.biyapay.com`
- `www.biyapays.com`
- `192.168.110.190`
- `localhost`

当前没有命中明确候选事件名的动作包括：

- `kyc_start`
- `kyc_success`
- `deposit_start`
- `deposit_success`
- `trade_start`
- `trade_success`
- `download_app`
- `click_signup`
- `click_download`

这意味着：

- 当前注册漏斗可以初步看，但必须先过滤非生产 host。
- KYC、入金、交易漏斗目前不能作为正式增长判断指标使用。
- 阶段一可以正式把这些动作列为“缺失或未映射埋点”，而不是继续假设它们存在。

### 6. GSC Top 200 机会页已经形成初版

当前已基于近 90 天 live GSC 数据生成 `phase1_gsc_top200_seo_opportunities.csv`。

结果摘要：

- 候选机会页总量：716
- 已输出 Top 200 页面机会表
- 当前头部机会页以 `blogdetail` 为主，也混入了 `stock`、`homepage`、`download` 等页面类型

这说明：

- 主站当前确实已经有足够大的机会页池，不缺“找机会”这一步。
- 但头部机会页里大量是泛金融高曝光博客，阶段二必须同时判断“点击增量价值”和“业务价值”，不能只按曝光排序。

### 7. Top 200 技术状态第一版已经完成

当前已把 Top 200 机会 URL 和 0518 版 Screaming Frog 主站导出做了第一轮映射，生成 `phase1_top200_technical_status.csv`。

关键发现：

- 200 个 URL 中，137 个能在 `www_0518` crawl 中找到
- 63 个 URL 不在 `www_0518` crawl 范围内，暂标记为 `out_of_www_0518_scope`
- 135 个 URL 当前状态码为 `200`
- 1 个 URL 状态码为 `502`
- 99 个 URL title 过长
- 66 个 URL title 缺失或不在当前 crawl 范围
- 68 个 URL meta description 过长
- 66 个 URL meta description 缺失或不在当前 crawl 范围
- 36 个 URL 在 0518 orphan 导出中被标记为孤岛页
- 技术优先级分布：`P1 = 182`、`P2 = 16`、`P0 = 2`

这说明：

- 当前 Top 200 里，技术问题最多的不是大规模不可索引，而是标题过长、描述过长、部分 URL 不在当前 crawl 范围，以及一批高价值孤岛页。
- 阶段二可以先抓“200 状态 + 可索引 + 标题/描述可改 + 有明确机会关键词”的页面做快速执行。

## 三、当前文件清单

当前阶段一已形成的实物文件：

- [phase1_ga4_hostname_cleaning.csv](phase1_ga4_hostname_cleaning.csv)
- [phase1_direct_traffic_breakdown.csv](phase1_direct_traffic_breakdown.csv)
- [phase1_conversion_event_audit.csv](phase1_conversion_event_audit.csv)
- [phase1_gsc_top200_seo_opportunities.csv](phase1_gsc_top200_seo_opportunities.csv)
- [phase1_top200_technical_status.csv](phase1_top200_technical_status.csv)

已形成的配套文档：

- [01_phase_one_data_and_opportunity_plan.md](01_phase_one_data_and_opportunity_plan.md)
- [03_phase_one_report_template.md](03_phase_one_report_template.md)
- [04_direct_traffic_special_plan.md](04_direct_traffic_special_plan.md)
- [05_gsc_top200_opportunity_plan.md](05_gsc_top200_opportunity_plan.md)

## 四、当前风险与不足

- 当前 Direct 表是第一版规则分类，还需要继续补 `page referrer`、`session source / medium`、`first user source / medium`，增强判断准确度。
- `active.biyagl.com` 的业务归属还未最终确认。
- 63 个 Top 200 URL 不在当前 `www_0518` crawl 范围，后续要补 invest 或其他 host 的 crawl 结果。
- 当前 Top 200 机会页仍需结合业务价值进一步收敛为阶段二 Top 30。

## 五、下一步

阶段一下一步按以下顺序推进：

1. 从 Top 200 机会页中收敛出阶段二 Top 30 页面名单。
2. 对 Top 30 做页面级动作拆分：标题、描述、首屏、内链、FAQ、CTA。
3. 对 `out_of_www_0518_scope` 的高优先 URL 补独立 crawl 或另找技术数据源。
4. 持续补 Direct 判断证据，增强分类准确度。
