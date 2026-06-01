# Direct 流量清洗执行包

本包是对 `04_direct_traffic_special_plan.md` 的本轮落地延伸。目标不是继续描述方法，而是把当前仓库里的 raw 视图转成可执行的口径、分桶和任务。

## 输入

- `v_raw_ga4_hostname_audit`
- `v_raw_ga4_page_location_events`
- `queries/direct_hostname_audit.sql`
- `queries/page_location_audit_flags.sql`
- `queries/direct_cleanup_priority_summary.sql`
- `queries/direct_www_content_path_groups.sql`
- `docs/phase1_direct_cleanup_priority_summary.csv`

## 本轮结论

当前 Direct 相关 page-location 数据中，真正可以直接保留为“核心品牌直达”的只剩主站首页与语言首页三条入口：

- `https://www.biyapay.com/`
- `https://www.biyapay.com/en`
- `https://www.biyapay.com/zh`

这三条入口合计 `37,783` sessions，而以下三个桶的规模都已经接近或超过它：

- `signup.biyapay.com/download / fastreg`：`43,262` sessions
- 非生产或外部 host：`37,842` sessions
- 主站 auth/download/measurement bucket：`26,642` sessions

结论：当前 Direct 不能作为增长汇报口径直接使用，必须先按 host、路径和业务语义切开。

## Priority Bucket Rollup

总计纳入本轮分桶的 page-location sessions 约 `962,762`。建议按下表处理：

| priority_bucket | sessions | active_users | 判断 | reporting_action |
|---|---:|---:|---|---|
| review_www_content_or_tool_direct | 736,111 | 711,596 | 主站内容/工具/活动页被大量记为 Direct，远超首页品牌直达 | 暂不计入 clean Direct，先按路径族和 referrer/source 再拆 |
| separate_signup_download_or_fastreg | 43,262 | 26,736 | signup 下载和 fastreg 更像 app return / lifecycle traffic | 从获客口径剥离，单列 app/注册回流视图 |
| exclude_non_prod_or_external_host | 37,842 | 24,824 | `active.biyagl.com`、`www.biyapays.com`、`prv.*`、`localhost` 等明显污染 | 直接排除出 clean reporting，并补 host ownership 审计 |
| keep_core_home_brand_direct | 37,783 | 28,889 | 主站首页/语言首页，最接近真实品牌或手输直达 | 保留在 clean Direct 基线中 |
| review_invest_product_traffic | 29,141 | 20,341 | invest 子域产品页被计入 Direct | 与主站 SEO 增长口径拆分，单列 invest 直达审计 |
| separate_www_auth_download_measurement | 26,642 | 22,011 | 主站登录/下载回流与 `(not set)` 测量缺口混在 Direct | 从获客口径剥离并修复跨域/登录链路测量 |
| separate_or_migrate_legacy_cn_host | 25,441 | 21,483 | `cn.biyapay.com` / `biyapay.com` 仍在承接大量 Direct | 明确镜像/迁移策略、redirect/canonical 和报表处理 |
| separate_invest_auth_404_download | 17,763 | 11,741 | invest 的 `404`、login、download、assets 参数路由污染 Direct | 作为产品/技术流量处理，不纳入主站增长汇报 |
| other_review | 5,874 | 3,834 | 少量未归类样本 | 用 referrer/source/logs 补充核验 |
| review_news_subdomain_direct | 2,892 | 1,880 | news 子域也被记为 Direct | 保持独立视图，不并入主站 clean Direct |
| fix_signup_cross_domain_or_not_set | 11 | 11 | signup 根路径残余测量缺口 | 作为边角测量修复处理 |

## Largest Bucket: 主站内容/工具页 Direct 不是“自然品牌直达”

最大桶 `review_www_content_or_tool_direct` 占全部分桶 sessions 的大头，必须继续拆。当前按路径族分组，前几类是：

| path_group | sessions | active_users | 解释 |
|---|---:|---:|---|
| other | 167,643 | 164,881 | 各类未归到模板族的路径，优先再看 referrer/source 和 campaign 参数 |
| blogdetail | 136,639 | 133,769 | 博客/资讯页大量被记为 Direct，不能直接当品牌访问 |
| swift | 122,301 | 122,118 | 工具页 Direct 量异常大，需核验分享、WebView、埋点和 referrer 丢失 |
| sendmoney | 83,964 | 83,595 | 商业意图强，但不能直接认定为 Direct 获客 |
| stock | 81,150 | 80,361 | 需要与 invest / stock overlap 一起看 |
| compare | 22,311 | 22,250 | compare 仍有模板级技术阻塞，Direct 口径更不能直接解释 |
| announcement | 19,642 | 17,847 | 活动/公告类路径显著，存在 campaign 或 App/WebView 回流特征 |
| converter | 12,539 | 12,477 | converter 适合后续结合 GSC 和 UX 改版一起复查 |

结论：如果老板只看 Direct 总量，当前会把大量活动页、工具页、镜像 host、下载回流和非生产流量误当“真实直接访问”。

## Top Risk Samples

- `signup.biyapay.com/download`：`36,593` sessions，明显应单列为下载或 app 回流。
- `invest.biyapay.com/en/404`：`4,209` sessions，属于错误路径进入，不应被当成获客。
- `www.biyapays.com/`：`1,327` sessions，属于污染或外部 host。
- `active.biyagl.com/zh?id=6`：`1,305` sessions，属于非核心 host。
- `cn.biyapay.com/`：`3,250` sessions，说明 legacy/mirror host 仍有真实承接量。

## Reporting Rule

本项目后续汇报建议至少拆成四层：

1. `Clean Direct`：仅保留主站首页/语言首页，必要时再补充少量经 referrer/source 证实的真实直达。
2. `Lifecycle / App Return`：signup download、fastreg、主站/子域 login、download、注册回流。
3. `Host Pollution / Legacy Host`：`active.biyagl.com`、`www.biyapays.com`、`prv.*`、`localhost`、`cn.biyapay.com`、裸域等。
4. `Needs Review`：主站内容页、工具页、invest/news 子域产品页，继续结合 referrer、session source、日志与跨域配置复核。

## 执行动作

### P0

- 在 clean reporting 中排除非生产、外部和 legacy host。
- 把 signup download / fastreg、www/login/download、invest/login/404/download 从获客视图剥离。
- 为 Direct 汇报增加 `clean_direct`、`lifecycle_return`、`host_pollution`、`needs_review` 四层口径。

### P1

- 复核 `signup.biyapay.com`、`invest.biyapay.com`、`news.biyapay.com` 的跨域和 session continuity。
- 单独追踪 `cn.biyapay.com` 是否仍需承接流量，明确 redirect/canonical/报表策略。
- 对 `www` 内容/工具大桶补充 referrer、session source/medium、WebView 和 campaign 参数核验。

### P2

- 在 compare P0 修复后，把 compare/converter/sendmoney/swift/blogdetail 的 Direct 与 GSC/SEO 提效一起复盘。
- 若 logs 可用，补一轮 `needs_review` 桶的 access-log 佐证。

## 交付物

- `docs/phase1_direct_cleanup_priority_summary.csv`
- `queries/direct_cleanup_priority_summary.sql`
- `queries/direct_www_content_path_groups.sql`

## 下一步

1. 按本包创建 GitHub milestone 和 issues，拆成 analytics、engineering、product 三类动作。
2. 将 clean Direct 口径加入老板周报，停止直接引用未清洗的 Direct 总量。
3. 继续补 referrer/source/logs 维度，先拆 `review_www_content_or_tool_direct`。# Direct 流量清洗执行包

本包在 `04_direct_traffic_special_plan.md` 的方法论基础上，补上当前 DuckDB 语义层已经可以直接执行的清洗口径、优先级和责任分工。目标是把“Direct 看起来很大”改成“哪些该保留、哪些该排除、哪些该修”。

## 输入

- `v_raw_ga4_hostname_audit`
- `v_raw_ga4_page_location_events`
- `queries/direct_cleanup_priority_summary.sql`
- `queries/direct_www_content_path_groups.sql`
- `docs/phase1_direct_cleanup_priority_summary.csv`

## 结论摘要

当前 Direct 不能直接作为增长汇报口径，原因不是只有 `signup` 或测试环境，而是 `www` 上大量内容、工具、活动和产品路径也在 Direct 中堆积，规模已经明显超过首页品牌直达。

现阶段最重要的判断：

1. `www` 非首页内容/工具/活动路径合计 `736,111` sessions，是当前最大桶，必须二次分层，不能直接当作真实品牌直达。
2. `signup.biyapay.com/download` 和 `fastreg` 合计 `43,262` sessions，应从获客增长口径中拆出，单独看 App/WebView/注册回流。
3. 非生产或外部 hostname 合计 `37,842` sessions，应先从 clean reporting 中排除。
4. 真正可直接保留为品牌直达的核心首页桶只有 `37,783` sessions，量级并不大。
5. `cn.biyapay.com` / `biyapay.com` 这类 legacy host 还有 `25,441` sessions，需要确认是否迁移、跳转或残留入口问题。

## Direct 清洗优先级

| priority_bucket | sessions | active_users | event_count | 处理方式 |
|---|---:|---:|---:|---|
| `review_www_content_or_tool_direct` | 736,111 | 711,596 | 790,582 | 二次分层，先拆 promo / tool / blog / product / app-return，再决定哪些进入 clean Direct |
| `separate_signup_download_or_fastreg` | 43,262 | 26,736 | 82,197 | 从获客口径剥离，改入注册/下载/回流专项 |
| `exclude_non_prod_or_external_host` | 37,842 | 24,824 | 69,810 | 直接从 clean reporting 排除 |
| `keep_core_home_brand_direct` | 37,783 | 28,889 | 62,612 | 作为真实品牌/直接访问基准桶保留 |
| `review_invest_product_traffic` | 29,141 | 20,341 | 44,708 | 单独做 invest Direct 复核，不并入主站 SEO 增长 |
| `separate_www_auth_download_measurement` | 26,642 | 22,011 | 38,215 | 拆到登录/下载回流口径 |
| `separate_or_migrate_legacy_cn_host` | 25,441 | 21,483 | 33,194 | 确认 legacy host 策略，默认不并入主站 clean Direct |
| `separate_invest_auth_404_download` | 17,763 | 11,741 | 29,944 | 从增长口径剥离，按 broken route / auth / app flow 处理 |
| `review_news_subdomain_direct` | 2,892 | 1,880 | 4,992 | 保持独立口径，暂不并入主站增长 |
| `other_review` | 5,874 | 3,834 | 14,233 | 逐条复核剩余异常 host/path |

## 最大污染桶拆解：`www` 内容 / 工具 / 活动 / 产品路径

`queries/direct_www_content_path_groups.sql` 显示，这个桶内部不是单一类型，而是多个产品和内容入口混在一起：

| path_group | sessions | active_users |
|---|---:|---:|
| `other` | 167,643 | 164,881 |
| `blogdetail` | 136,639 | 133,769 |
| `swift` | 122,301 | 122,118 |
| `sendmoney` | 83,964 | 83,595 |
| `stock` | 81,150 | 80,361 |
| `compare` | 22,311 | 22,250 |
| `announcement` | 19,642 | 17,847 |
| `converter` | 12,539 | 12,477 |

这说明当前 Direct 里至少混着 4 类不同口径：

- 真正的品牌/书签/直接访问。
- App / WebView / 活动页回流。
- 历史跨域、跳转或 referrer 丢失。
- 本该归到 Organic / Referral / Internal lifecycle 的内容和工具页访问。

## 代表性证据

### 1. `signup` 下载与注册回流

- `https://signup.biyapay.com/download`：`36,593` sessions。
- `https://signup.biyapay.com/fastreg`：`821` sessions。

结论：这部分更像注册或下载回流，不应继续被用来证明 SEO 或品牌获客增长。

### 2. `invest` 登录和 404 污染

- `https://invest.biyapay.com/en/404`：`4,209` sessions。
- `https://invest.biyapay.com/zh/login`：`2,145` sessions。

结论：至少存在 broken route / 错误跳转 / 生命周期入口混入 Direct 的问题。

### 3. 非生产和外部 hostname

- `active.biyagl.com`：`3,229` active users。
- `prv.cn.biyapay.io`：`2,399` active users。
- `www.biyapays.com`：`1,258` active users。

结论：这些主机必须先排除，否则报表会持续被污染。

### 4. legacy host 残留

- `cn.biyapay.com/`：`3,250` sessions。
- `cn.biyapay.com/login`：`1,533` sessions。
- `cn.biyapay.com/assets`：`1,091` sessions。

结论：`cn.biyapay.com` 不是当前主站增长口径的一部分，但仍持续进数，说明仍有历史入口、跳转缺口或旧 App/WebView 引流残留。

## 报表处理规则

给老板的 clean Direct 口径建议按下面规则执行：

1. 先保留 `www.biyapay.com` 首页 / 语言首页桶作为真实 Direct 基准。
2. 先排除非生产、外部和明显 legacy host。
3. `signup` / `invest` / `news` 默认单独成报表，不合并进主站 clean Direct。
4. `www` 登录、下载、注册、活动页默认划入 lifecycle / app-return / promo，不记为新获客。
5. `www` 内容和工具页继续做第二轮 referrer / source / WebView / log 复核，在复核前不把这部分全部算成真实 Direct。

## 本轮执行动作

### P0：立即处理

- GA4 clean reporting 先排除 `active.biyagl.com`、`prv.*`、`localhost`、IP、`www.biyapays.com`。
- 给 Direct 看板新增 `hostname_group` 和 `traffic_bucket` 两层分类。
- 把 `signup/download`、`fastreg`、`www/login`、`www/download` 从老板周报口径剥离。

### P1：本周完成

- 复核 `signup / invest / news / www` 跨域、session continuity 和 referrer 继承。
- 确认 `cn.biyapay.com` / `biyapay.com` 的迁移和跳转策略。
- 补一版 referrer / source / medium 粒度的 Direct 复核表，专门拆 `www` 内容/工具流量。

### P2：专项继续推进

- 把 `blogdetail`、`swift`、`sendmoney`、`stock`、`compare`、`converter` 六类 URL 再拆成“真实直达 / 归因丢失 / 生命周期回流 / 可排除”四类。
- 接 access log 或边缘日志复核 `other` 和 `cn` 残留桶。

## 复跑方式

```bash
.venv/bin/python - <<'PY'
import duckdb
conn = duckdb.connect('data/warehouse/biyapay.duckdb')
for sql_file in [
    'queries/direct_cleanup_priority_summary.sql',
    'queries/direct_www_content_path_groups.sql',
]:
    print(sql_file)
    for row in conn.sql(open(sql_file).read()).fetchall():
        print(row)
PY
```

## 下一步

1. 把本包中的 bucket 直接变成 GitHub issue 执行队列。
2. 追加一轮 referrer / source / medium 分析，专门清洗 `www` 内容/工具大桶。
3. 更新老板汇报口径：先报 clean Direct，再报 raw Direct，避免继续混淆增长结果。