# 老板一页纸：100 万月流量当前状态

## 一句话结论

当前不是缺“做 SEO 动作”，而是必须先把数据口径和技术承接修干净。否则 100 万月流量会混入大量不可运营、不可归因、不可复用的流量。

## 当前真实进度

### 1. Direct 已经从黑箱拆成可执行口径

现在不建议再看 raw Direct。

最新可用于周报的主站 `provisional clean Direct` 候选值为 `15,671` sessions。

需要继续拆的 held Direct 为 `602,724` sessions：

- `hold_content_tool_direct`：`459,312`
- `hold_tool_intent_direct`：`143,412`

这说明 raw Direct 中仍有大量工具页、内容页、回流、活动或归因缺失流量，不能直接当品牌增长。

### 2. 下一轮 Direct 只需要追五类路径

数据团队不需要全站泛导。

下一轮先要这五类 `www + Direct + landing path` 的 `source / medium / full referrer`：

| path_group | sessions | 处理优先级 |
|---|---:|---|
| `swift` | 211,685 | 立即导出 |
| `blogdetail` | 113,103 | 立即导出 |
| `stock` | 97,494 | 立即导出 |
| `sendmoney` | 85,832 | 立即导出 |
| `compare` | 44,783 | 立即导出 |

这五类覆盖 `91.74%` 的 held Direct，足够决定下一版 clean Direct 口径。

### 3. compare 是当前最大的技术阻塞

12 个 P0 compare URL 仍然全部失败：`12 checked / 0 passed / 12 failed`。

失败不是单页内容问题，而是统一的 Next.js 运行时指纹：

- status：`500`
- `x-powered-by`：`Next.js`
- body bytes：`21`
- body preview：`Internal Server Error`
- body SHA-256：`e41656eb2ba6c6293bf6dd928e5a88cdbc50535cab661c1969e0f598e497ed62`

这些 compare URL 已有 11 万级 GSC 曝光，但当前页面无法承接点击、抓取和转化。

### 4. raw layer 已暴露 partial 导入风险

`scripts/ingest_selected_raw_sources.py` 已重跑。75 个 selected raw source 中有 28 个被标记为 `partial`，明细见 `docs/phase3_raw_import_partial_evidence.csv`，根因说明见 `docs/56_raw_import_partial_root_cause.md`。

这不是说当前所有结论失效，而是说明 raw layer 不能再只写“imported”。后续涉及 GA4 page-location、hostname audit、GSC coverage 的判断，必须同时看 skipped-row 类型：

- 多数 GA4 partial 是导出元数据/空行/总计行被跳过，不等同于业务数据丢失。
- news GSC coverage examples 是非 UTF-8 编码问题，当前导入 `0` 行，暂不能作为 coverage 证据。

## 本周最该拍板的事

1. 数据团队按 `docs/50_direct_www_source_export_template.md` 导出五类 held Direct 的 source/referrer。
2. 工程团队按 `docs/48_compare_nextjs_500_diagnostic_handoff.md` 修 compare 共享 500。
3. 数据/SEO 按 `docs/56_raw_import_partial_root_cause.md` 处理 raw partial source，优先重导非 UTF-8 coverage 文件。
4. 周报口径立即改为 clean Direct / held Direct / excluded Direct，不再汇报 raw Direct。

## 对 100 万月流量目标的影响

短期内，这些动作不会把流量数字“做大”，但会把虚高、污染和不可运营流量先清掉。

修完后会得到三个增长基础：

- Direct 能分清真实品牌直达和归因污染。
- compare 能重新承接已有搜索曝光。
- 团队能按路径、模板和 owner 推进，而不是泛泛做 SEO。

## 当前老板口径

- 真实可汇报：`provisional_clean_direct = 15,671`
- 必须继续复核：`held_for_source_review = 602,724`
- 已排除首页非 clean：`excluded_home_nonclean = 79,812`
- 已排除生命周期/活动：`excluded_lifecycle_or_promo = 26,797`
- 技术 P0：compare 模板统一 Next.js `500`
- 数据质量 P0：raw selected import 有 `28` 个 partial source，需按 `skipped_rows` 加 caveat

## 下一次更新标准

下一次向老板更新时，只看两件事：

1. 五类 held Direct 是否已拿到 source/referrer 并重新归类。
2. compare 12 个 P0 URL 是否达到 `12/12 pass`。

日常执行状态以 `docs/51_p0_execution_tracker.md` 和 `docs/phase3_p0_execution_tracker.csv` 为准，优先更新 P0 blocker 的 owner、next action 和 acceptance check。
