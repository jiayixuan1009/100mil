# `www` Direct 动作桶执行包

本包把 `43_direct_www_signal_followup.md` 和 `45_www_channel_gap_fill.md` 的结果收口成下一版可执行口径。目标不是继续描述问题，而是先回答一个更实用的问题：

当前 `www` 这些 Direct-like 流量里，哪些可以马上排掉，哪些可以暂时保留，哪些必须挂起继续查？

## 输入

- `queries/direct_www_action_buckets.sql`
- `docs/phase1_direct_www_action_buckets.csv`
- `queries/direct_www_channel_group_matrix.sql`
- `queries/direct_www_query_signal_summary.sql`
- `queries/direct_www_path_query_signal_matrix.sql`

## 动作桶结果

当前 `www` 路径族按动作桶汇总如下：

| action_bucket | sessions | 含义 |
|---|---:|---|
| `hold_content_tool_direct` | 459,312 | `swift`、`blogdetail`、`stock`、`other` 等高量级内容/工具路径看起来是 Direct，但现在还不能进 clean Direct |
| `hold_tool_intent_direct` | 143,412 | `compare`、`converter`、`sendmoney` 这类工具意图路径应继续挂在 needs-review |
| `exclude_home_unassigned_or_nonclean` | 79,812 | 首页与 `(not set)` 中的 `Unassigned` / `Referral` / `Organic Social` 不应进入 clean Direct |
| `review_with_more_source_detail` | 57,810 | 剩余混合渠道仍需下一轮 source/referrer 明细 |
| `exclude_promo_announcement` | 16,190 | 活动/公告流量应按 promo 处理，不进 clean Direct |
| `keep_home_direct_candidate` | 15,671 | 当前唯一相对可保留的主站 clean Direct 候选桶 |
| `exclude_lifecycle_paths` | 10,607 | login / download / register 直接按生命周期流量处理 |

## 这一步解决了什么

之前的 Direct 清洗结果已经证明：

- raw Direct 不能直接上老板周报
- `www` 大桶里混有 amount、campaign、webview 信号
- 主站内容/工具路径在默认渠道组里又大多显示为 `Direct`

但直到这一轮，还没有一个明确的“先按什么动作处理”的中间口径。

现在可以先执行以下规则：

1. 先排：`exclude_lifecycle_paths`、`exclude_home_unassigned_or_nonclean`、`exclude_promo_announcement`
2. 暂挂：`hold_tool_intent_direct`、`hold_content_tool_direct`
3. 暂留：`keep_home_direct_candidate`
4. 补数后再判：`review_with_more_source_detail`

## 当前最重要的业务判断

主站 `www` 里，当前真正能作为 provisional clean Direct 基线保留的只有 `15,671` sessions。

与之相比：

- 必须继续挂起或排除的量合计超过 `700k` sessions
- 仅 `hold_content_tool_direct + hold_tool_intent_direct` 就有 `602,724` sessions

这说明老板若继续看 raw Direct，总体判断仍会明显偏高。

## 建议口径

### 对老板周报

- `provisional_clean_direct`
- `excluded_lifecycle_or_promo`
- `excluded_home_nonclean`
- `held_for_source_review`

### 对执行团队

- `hold_content_tool_direct` 优先追 `swift`、`blogdetail`、`stock`
- `hold_tool_intent_direct` 优先追 `compare`、`sendmoney`、`converter`
- `review_with_more_source_detail` 等下一轮主站 `source/medium/referrer` 导出

## 下一步

1. 用这个动作桶替换上一轮过于宽泛的 `needs_review` 中间口径。
2. 对 `hold_content_tool_direct` 和 `hold_tool_intent_direct` 申请主站 `source / medium / referrer` 导出。
3. compare 修复完成后，优先复查 `hold_tool_intent_direct` 中的 compare 分组是否仍应保留在挂起桶中。
