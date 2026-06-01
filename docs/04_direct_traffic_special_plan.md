# Direct 流量专项施工文档

## 专项目标

识别 BiyaPay 近 90 天 Direct 流量中哪些属于真实直接访问，哪些属于归因丢失、跨域断裂、App/WebView、登录回跳、测试环境、爬虫或异常访问，并产出可执行修复清单。

## 为什么先做这个专项

当前 Direct 流量体量异常大。如果不先拆清，会导致：

- 月流量判断失真。
- SEO 增长结果被错误归因。
- 漏斗表现被错误解读。
- 老板看到的增长数字掺杂污染流量。

## 分析范围

- 时间范围：近 90 天为主，必要时看 180 天趋势。
- 数据源：GA4 live 数据、历史 hostname 审计、cross-domain 数据、访问日志、页面路径结构。
- 分析对象：默认渠道组为 Direct 的 sessions 和相关事件。

## 核心维度

必须提取的维度和指标：

- landing page + query string。
- hostname。
- country。
- device category。
- browser。
- operating system。
- page referrer。
- first user source / medium。
- session source / medium。
- sessions。
- active users。
- engaged sessions。
- avg engagement time。
- key events。

## 优先排查入口

- `(not set)`。
- `/download`。
- `/login`。
- `/404`。
- `/zh?id=...` 参数页。
- signup 域。
- invest / www / news 跨域跳转。
- 高比例 Windows 桌面流量。
- 高集中单国家流量。
- 会话时长极短且无 engagement 的页面。

## 分类框架

### A 类：真实品牌或直接访问

特征：

- 品牌词相关。
- 首页、下载页、登录页有合理直接访问。
- engagement 和关键事件正常。

### B 类：跨域归因丢失

特征：

- 域之间跳转后变成 Direct。
- 与 signup / invest / news 切换相关。
- 来源应该属于 Organic、Referral 或其他渠道。

### C 类：App / WebView / 下载回流

特征：

- 下载页、打开 App、WebView 场景明显。
- referrer 信息缺失但设备、路径特征明显。

### D 类：登录 / 注册 / 支付回跳

特征：

- `/login`、注册、支付完成、回跳页进入 Direct。
- 渠道不应被当成新获客流量。

### E 类：测试环境污染

特征：

- PRV / DEV / localhost / 内网 IP / 非生产 hostname。

### F 类：爬虫、机器流量或异常访问

特征：

- 极短会话。
- 无 engagement。
- 单设备、单浏览器、单国家异常集中。
- 落地页不合理。

### G 类：待日志复核

特征：

- 仅靠 GA4 无法充分解释，需要 access log 或防护日志佐证。

## 交付表结构

输出表：`phase1_direct_traffic_breakdown.csv`

建议字段：

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
- reporting_action。

## 专项结论必须回答的问题

- 总 Direct sessions 中，真实 Direct 占多少。
- 有多少 Direct 实际是归因丢失。
- 有多少 Direct 应从增长口径排除。
- 有多少 Direct 需要产品、前端或埋点修复。
- 有多少 Direct 需要日志层进一步核实。

## 修复动作类型

- 报表口径修正。
- 跨域配置修正。
- 埋点修正。
- 异常 hostname 过滤。
- 生产与测试环境分离。
- 登录、支付、下载路径口径拆分。
- 异常流量标记或排除。