# 100 万月流量周执行板

这个执行板用于把 `docs/59_1m_traffic_execution_plan.md` 变成每周可推进的动作。

工程完美不是目标。目标是每周都让 `biyapay.com` 离月 100 万真实可运营流量更近一步。

配套 CSV：`docs/phase3_1m_weekly_execution_board.csv`

## 本周只盯五件事

| priority | action | 当前状态 | 本周推进标准 |
|---|---|---|---|
| P0 | Direct held source/referrer 回传 | blocked_on_data | 数据团队给出 CSV 或明确无法导出的原因 |
| P0 | Compare 500 修复 | blocked_on_engineering | 工程给出修复分支、日志证据或上线时间 |
| P0 | 2 个非 UTF-8 source 重导 | blocked_on_data | 收到 UTF-8 新文件，或确认这两个 source 不进入老板口径 |
| P1 | Converter / blogdetail 继续上线 | ready | 不等 compare，先推进可上线页面和桥接模块 |
| P1 | Top 30 页面执行状态 | ready | 每个 URL 有 owner、状态、下一步和观察窗口 |

## 推进原则

1. Direct 数据没回传前，不把 raw Direct 当成 100 万进展。
2. Compare 没有 `12/12 pass` 前，不承诺 compare SEO 增量。
3. Compare 卡住时，不空等，继续推进 converter、blogdetail、swift、sendmoney、stock 的可上线动作。
4. raw 数据的风险标签必须转成动作：重导、排除、或报告 caveat。
5. 每周只问能推动增长的问题：这个动作能恢复已有曝光、提升 CTR、减少脏流量，还是提高转化承接？

## 升级规则

### Direct

如果 3 个工作日内没有 source/referrer CSV：

- 用 `docs/57_direct_held_export_message.md` 再发一次。
- 同步提醒：五类路径覆盖 `91.74%` held Direct，不需要全站泛导。
- 如果仍拿不到，先把 `602,724` held Direct 全部留在 held，不进入 clean traffic。

### Compare

如果 3 个工作日内没有工程修复进展：

- issue `#5` 继续保持 P0。
- 不做 compare CMS handoff。
- SEO 执行切到 converter / blogdetail / swift / sendmoney / stock。

### Raw source

如果 2 个非 UTF-8 source 暂时拿不到新文件：

- `03 news/gsc/news_coverage_examples.csv` 不进入 coverage 证据。
- `03 news/ga/ga4-news_hostname_daily_90d.csv` 不作为最终 hostname 证据。
- 老板口径只写“需重导”，不写“数据已失效”。

## 本周不做

- 不新增大规模页面库。
- 不为 compare 写 SEO handoff，除非 live regression 先过。
- 不把 100 万目标拆成虚假的 raw traffic 数字。
- 不继续优化 importer 细节，除非它直接影响报告判断。

## 周会固定输出

每周更新一次：

1. clean Direct、held Direct、excluded Direct 是否变化。
2. compare regression 是 `0/12`、部分通过，还是 `12/12 pass`。
3. 本周上线或交接了哪些 converter / blogdetail / template 页面。
4. 哪些数据源被排除、重导或允许带 caveat 使用。
5. 下一周唯一最重要的 unblocker。

## 当前最重要 unblocker

第一：Direct source/referrer CSV。

第二：Compare Next.js `500` 修复。

第三：不要让这两个 blocker 停掉其它可上线页面。
