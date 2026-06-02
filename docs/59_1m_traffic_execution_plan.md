# BiyaPay 月 100 万总流量执行方案

## 目标定义

最终目标不是把 GA4 表面流量推到 100 万，而是把 `biyapay.com` 体系月真实可运营流量推到 100 万级。

这里的可运营流量必须满足三个条件：

1. 能在 GA4 / GSC 中稳定识别来源、落地页和站点归属。
2. 不是测试、污染 hostname、异常爬虫、应用回流误归因或无法解释的 raw Direct。
3. 能进入注册、KYC、入金、交易或至少可衡量的产品导流路径。

配套 CSV：`docs/phase3_1m_traffic_execution_plan.csv`

周执行板：`docs/60_1m_weekly_execution_board.md`

## 当前判断

现在最重要的不是立刻新增大量页面，而是先把已有资产修到可以承接流量。

- Direct 表面量很大，但 clean baseline 只有 `15,671` sessions，另有 `602,724` sessions 仍在 held review。
- compare 有 11 万级已有 GSC 曝光，但 12 个 P0 URL 当前统一 `500`，无法承接搜索点击。
- converter、blogdetail、swift、sendmoney、stock 等路径已有曝光和站内入口，适合在技术阻塞解除后做模板化提效。
- raw 数据现在已能区分干净导入、metadata preamble、expected empty export 和 encoding blocked。它是判断口径，不是增长本身。

## 执行路线

### 阶段 0：数据可信和技术止血

周期：现在到 2 周。

目标：避免把脏流量、坏页面和不可解释数据写进 100 万方案。

必须完成：

- Direct：拿到五类 held Direct 的 source / medium / full referrer，拆成 clean、search、app/webview、campaign、log-review。
- Compare：修复 shared Next.js `500`，让 12 个 P0 URL 全部通过 live regression。
- Raw：重导 2 个非 UTF-8 source，让 `encoding_blocked` 从 raw import failures 中清零。

解锁标准：

- 周报不再使用 raw Direct 做 KPI。
- `scripts/validate_compare_live_urls.py` 返回 `12/12 pass`。
- `v_raw_import_failures` 不再出现 `encoding_blocked`。

### 阶段 1：吃掉已有曝光的快速增量

周期：2-6 周。

目标：先从已有 GSC 曝光中拿点击，而不是盲目扩页面。

必须完成：

- Top 200 SEO opportunity 重新分层，优先做高曝光、低 CTR、排名 4-20 的 URL。
- Top 30 页面按页面类型分批交付：compare 修复后先做前 5 个，converter / blogdetail 同步推进。
- 每个页面改动必须包含 title、meta、H1、首屏意图匹配、FAQ、相关内链和产品 CTA。

解锁标准：

- Top 30 每个 URL 都有 owner、动作、上线状态和 28 天观察窗口。
- 第一批页面完成 CMS 或工程上线交接。
- GSC 观察表能看到点击、CTR、平均排名变化。

### 阶段 2：模板恢复和规模化提效

周期：1-3 个月。

目标：把已有模板页从“批量 URL”升级为可排名、可点击、可转化的工具资产。

优先模板：

- compare：汇率对比、金额参数、canonical、provider fallback、结构化数据。
- converter：金额意图、实时汇率、双向币对、相关 compare / sendmoney 内链。
- sendmoney：国家/线路、费用、到账时间、可用支付方式、合规说明。
- swift / bank code / iban：查询工具、银行字段、FAQ 和交易路径。
- blogdetail：高曝光信息页加产品桥接模块。

解锁标准：

- 每类模板有字段规格、内链规则、CTA 规则和验收 checklist。
- 模板页面不再批量出现 `500`、noindex、canonical 错误或空首屏。
- 每个模板都能追踪到点击、注册或产品导流事件。

### 阶段 3：商业意图内容集群

周期：2-6 个月。

目标：在模板健康后扩大真实搜索覆盖。

优先主题：

- 跨境汇款：美国到香港、美国到中国、香港到内地、新加坡到香港。
- USDT 出金：USDT 到香港银行、费用、风险、合规路径。
- 银行工具：SWIFT、IBAN、routing number、分行代码、ATM 和转账限额。
- 汇率换汇：HKD/USD、USD/CNH、TWD/USD、SGD/HKD。
- 竞品对比：BiyaPay vs Wise、Remitly、Revolut、PayPal、Western Union。
- 信任合规：牌照、安全、KYC、资金保护、适用国家。

解锁标准：

- 每个主题都有 keyword map、目标页面、内链入口和商业 CTA。
- 新增页面只在模板健康、数据口径稳定后启动。
- 新页面以 28 / 60 / 90 天为观察周期，不用首周流量判断成败。

### 阶段 4：权威、引用和 AI 可见性

周期：长期。

目标：让搜索引擎和 AI 搜索把 BiyaPay 当作可信跨境金融工具源。

必须完成：

- 建立信任中心和合规中心。
- 输出可被引用的数据资产，如费用、到账时间、国家线路、银行代码资料。
- 修复 lost backlinks，争取金融媒体、华人社区、工具站和合作方引用。
- 跟踪 ChatGPT、Gemini、Perplexity 等 AI 搜索是否引用 BiyaPay。

解锁标准：

- 品牌实体信息一致。
- 关键商业主题能被外部引用源支撑。
- AI search baseline 持续记录 cited / position / competitor gap。

## 里程碑

| 时间 | 必须看到的结果 | 主要 owner |
|---|---|---|
| 7 天 | Direct 导出已回传或明确 blocker；compare 修复有工程进展；raw encoding blocker 有重导请求 | data_team / engineering / seo_data |
| 14 天 | compare 12 个 P0 URL 通过；Direct held 有第一版 reclassification | engineering / seo_data |
| 30 天 | Top 30 首批页面进入上线和观察；周报只看 clean / held / excluded | SEO / Content / Product |
| 60 天 | compare、converter、blogdetail 三类页面形成稳定模板交付节奏 | Product / Frontend / SEO |
| 90 天 | 商业意图内容集群开始规模化，但只在模板健康后扩张 | SEO / Content / Partnerships |

## 当前 P0 决策

1. 不把 raw Direct 当作 100 万目标进展。
2. 不在 compare `500` 修复前承诺 compare SEO 增量。
3. 不在 held Direct 拆清前承诺可运营流量占比。
4. 不先大规模新建页面，先修已有曝光和模板承接能力。
5. 数据可以有风险标签，但风险标签必须转化成重导、修复或 caveat，而不是停留在告警。

## 成功口径

这个方案成功的标志不是“文档齐了”，而是每周都能回答四个问题：

1. 本周 clean traffic baseline 变了吗？
2. 本周有多少已有曝光 URL 从 blocked / weak 变成可承接？
3. 本周上线了哪些页面或模板改动，观察窗口是什么？
4. 本周新增流量能否进入注册、KYC、入金、交易或产品导流判断？
