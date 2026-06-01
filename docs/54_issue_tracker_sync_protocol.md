# Issue 与 Tracker 同步规则

本规则用于避免 GitHub issue、CSV tracker、老板一页纸之间状态不一致。

当前单一执行入口是：

- `docs/51_p0_execution_tracker.md`
- `docs/phase3_p0_execution_tracker.csv`

## 更新顺序

任何 blocker 状态变化，都按以下顺序更新：

1. 先更新 `docs/phase3_p0_execution_tracker.csv`。
2. 再更新对应专项文档或 runbook。
3. 再更新 `docs/49_boss_one_page_current_status.md`。
4. 最后评论对应 GitHub issue。

## Issue 对应关系

| workstream | primary issue | repo artifact |
|---|---|---|
| Boss weekly status / reporting trust | `#1` | `docs/49_boss_one_page_current_status.md` |
| `www` held Direct export and reclassification | `#4` | `docs/52_direct_held_source_referrer_import_runbook.md` |
| Compare Next.js `500` fix | `#5` | `docs/48_compare_nextjs_500_diagnostic_handoff.md` |
| Compare post-fix SEO handoff | `#5` | `docs/53_compare_postfix_seo_handoff_runbook.md` |

## 状态词

统一使用以下状态，避免每个 AI 写一套：

- `ready`
- `in_progress`
- `blocked_on_data`
- `blocked_on_engineering`
- `ready_for_engineering`
- `waiting_on_p0`
- `ready_for_seo_handoff`
- `completed`

## 什么时候必须评论 issue

以下情况必须评论对应 issue：

- Direct source/referrer CSV 回传。
- Direct 分桶结果变化。
- compare 工程修复上线。
- compare live regression 从 fail 变为 pass，或失败指纹变化。
- 老板周报口径数字变化。

## 评论格式

建议使用：

```text
Status changed: <old_status> -> <new_status>

Evidence:
- <artifact path>
- <key metric/result>

Next action:
- <owner + action + acceptance>
```

## 不需要评论的情况

- 纯格式修正。
- 没有改变状态或数字的文字润色。
- 本地临时验证失败且未改变结论。
