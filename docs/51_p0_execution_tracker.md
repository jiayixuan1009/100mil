# P0 执行总控 Tracker

这个 tracker 用来把当前最重要的工作从“文档齐了”推进到“每天能按 owner 和验收标准推进”。

配套 CSV：`docs/phase3_p0_execution_tracker.csv`

## 当前执行顺序

| priority | workstream | status | owner | next_action | acceptance_check |
|---|---|---|---|---|---|
| P0 | Direct reporting trust | `in_progress` | seo_data | 周报只用 clean / held / excluded Direct | 周报不再使用 raw Direct 作为 KPI |
| P0 | `www` held Direct source/referrer export | `blocked_on_data` | data_team | 按五类路径导出 source / medium / full referrer | CSV 回传且字段完整 |
| P0 | Compare Next.js 500 fix | `blocked_on_engineering` | engineering | 排查 compare SSR / route parser / data-loader / provider fallback | 12 个 P0 URL 通过 live regression |
| P0 | Compare engineering checklist | `ready_for_engineering` | engineering | 按 checklist 修 route、amount、provider、metadata、日志 | checklist 全部 pass，live regression `12/12 pass` |
| P1 | Compare SEO handoff | `waiting_on_p0` | seo_content | compare 通过后再生成 SEO handoff | 通过后再进入 title/meta/CMS |
| P1 | Boss weekly status cadence | `ready` | ops | 用一页纸和 tracker 做周报 | 每周更新 clean Direct、held Direct、compare pass/fail |

## 今天最重要的两个外部输入

### 数据团队输入

需要按 `docs/50_direct_www_source_export_template.md` 回传 CSV。

必须包含：

- `date`
- `hostname`
- `landing page + query string`
- `session default channel group`
- `session source`
- `session medium`
- `full referrer`
- `sessions`

过滤范围只看：`swift`、`blogdetail`、`stock`、`sendmoney`、`compare`。

### 工程团队输入

需要按 `docs/48_compare_nextjs_500_diagnostic_handoff.md` 和 `docs/phase3_compare_engineering_fix_checklist.csv` 处理 compare 共享 `500`。

当前统一失败指纹：

- status：`500`
- `x-powered-by`：`Next.js`
- body bytes：`21`
- body preview：`Internal Server Error`
- body SHA-256：`e41656eb2ba6c6293bf6dd928e5a88cdbc50535cab661c1969e0f598e497ed62`

## 每日推进规则

1. 如果数据 CSV 回传，优先更新 Direct clean / held / excluded 桶。
2. 如果 compare 工程修复上线，立即运行 `scripts/validate_compare_live_urls.py`。
3. 如果 compare 达到 `12/12 pass`，再进入 compare SEO handoff。
4. 如果两条 P0 都未解除，不新增大规模页面生产任务。

## 当前不做什么

- 不把 raw Direct 当增长 KPI。
- 不在 compare `500` 未修复前做最终 CMS handoff。
- 不在 held Direct 未拆清前承诺 100 万月流量的可运营占比。
- 不先做大规模新增页面，先修已有曝光和可承接路径。

## 下一次更新入口

更新顺序：

1. 更新 `docs/phase3_p0_execution_tracker.csv` 的 `status` 和 `next_action`。
2. 同步更新 `docs/49_boss_one_page_current_status.md` 的当前老板口径。
3. 如果 compare 状态变化，重跑 `scripts/validate_compare_live_urls.py` 并更新 issue `#5`。
4. 如果 Direct 导出回来，新增导入/分析脚本或查询，并更新 issue `#4`。
