# 阶段二 Top 30 执行种子说明

## 文档用途

本文件说明 `phase2_top30_execution_seed.csv` 的用途和使用方式。

该文件不是最终页面改稿文档，而是阶段二的执行入口。它将阶段一的两张核心表做了合并：

- `phase1_gsc_top200_seo_opportunities.csv`
- `phase1_top200_technical_status.csv`

目标是从 Top 200 机会页中，先筛出最适合进入第一波执行的 30 个 URL。

## 当前筛选逻辑

Top 30 的种子排序综合考虑：

- 预估点击增量。
- 页面类型的业务价值权重。
- 技术状态是否在当前 crawl 范围。
- 是否存在明显技术阻塞。

当前的业务权重更偏向这些页面类型：

- compare
- converter
- sendmoney
- iban
- swift
- bank_code_or_tool
- download
- homepage / homepage_lang

同时保留一部分高曝光、高增量的 blogdetail 页面进入第一波，因为它们在当前 GSC 机会池里体量很大。

## 文件说明

当前输出文件：

- `phase2_top30_execution_seed.csv`

字段包括：

- url
- page_type
- primary_query
- impressions
- ctr
- avg_position
- estimated_click_uplift
- estimated_business_value
- technical_scope
- status_code
- technical_priority
- current_problem
- recommended_action
- selection_score
- execution_wave

## 如何使用

阶段二启动时，应按以下顺序使用这张表：

1. 先看 `execution_wave = wave_1` 的页面。
2. 再看 `technical_priority`，优先处理没有明显技术阻塞的页面。
3. 再按 `page_type` 分组，避免页面改造方式过于零散。
4. 对每个 URL 生成页面级动作卡片：标题、描述、首屏、FAQ、内链、CTA。

## 当前注意事项

- 当前 Top 30 仍是种子表，不是最终定稿名单。
- 其中部分页面虽然点击增量高，但业务价值未必最高，需要结合产品目标再筛一轮。
- `out_of_www_0518_scope` 的页面需要补 crawl 或额外技术数据，否则改稿前缺少技术基线。

## 下一步

基于 `phase2_top30_execution_seed.csv`，继续产出：

- Top 30 页面逐页动作卡。
- 按模板类型拆分的执行清单。
- 第一波页面优化实施文档。