# Direct held source/referrer 导入分桶 Runbook

本 runbook 接在 `docs/50_direct_www_source_export_template.md` 后面使用。数据团队按模板回传 CSV 后，直接用这里的脚本导入 DuckDB 并生成下一版 clean Direct 分桶。

## 脚本

`scripts/import_direct_held_source_referrer.py`

## 输入文件

数据团队回传的 CSV，建议文件名：

```text
www_direct_held_source_referrer_2025-11-20_2026-05-19.csv
```

必需字段：

- `date`
- `hostname`
- `landing page + query string`
- `session default channel group`
- `session source`
- `session medium`
- `full referrer`
- `sessions`

字段对照表：`docs/phase3_direct_held_source_referrer_expected_columns.csv`

脚本支持常见英文与中文 GA4 字段名，会统一映射成内部 canonical columns。

## 运行方式

查看字段要求：

```bash
.venv/bin/python scripts/import_direct_held_source_referrer.py --print-required-columns
```

导入真实 CSV：

```bash
.venv/bin/python scripts/import_direct_held_source_referrer.py \
  --input data/warehouse/extracts/www_direct_held_source_referrer_2025-11-20_2026-05-19.csv
```

默认输出：

- DuckDB table：`raw_direct_held_source_referrer_import`
- DuckDB view：`v_direct_held_source_referrer_classified`
- normalized CSV：`data/warehouse/extracts/direct_held_source_referrer_normalized.csv`
- summary CSV：`docs/phase3_direct_held_source_referrer_classification_summary.csv`

## 分桶规则

脚本会把回传数据分成：

| bucket | 含义 |
|---|---|
| `keep_as_clean_direct_candidate` | source / medium / referrer 没有明显非 Direct 信号 |
| `move_to_search_or_referral` | source、medium 或 referrer 显示搜索、外链或 referral 来源 |
| `move_to_app_or_webview_return` | source platform、source、medium、referrer 显示 App/WebView/deep-link 回流 |
| `move_to_campaign_or_promo` | campaign 或 `utm_` 参数显示活动来源 |
| `still_needs_log_level_review` | GA4 字段仍无法判断，需要日志或埋点继续查 |
| `out_of_scope` | 回传文件包含模板外路径，需退回或单独处理 |

## 验收标准

脚本会在导入前先校验回传范围：

- `hostname` 必须全部为 `www.biyapay.com`
- `session default channel group` 必须全部为 `Direct`
- landing path 必须属于 `swift`、`blogdetail`、`stock`、`sendmoney`、`compare`

导入完成后，必须检查：

1. `keep_as_clean_direct_candidate` 是否明显小于原 held Direct。
2. `move_to_search_or_referral`、`move_to_app_or_webview_return`、`move_to_campaign_or_promo` 是否能解释大部分 held Direct。
3. `still_needs_log_level_review` 如果仍很大，说明需要服务端日志或埋点补充。

## 后续更新

拿到真实 CSV 并运行脚本后，更新：

- `docs/phase3_direct_held_source_referrer_classification_summary.csv`
- `docs/49_boss_one_page_current_status.md`
- `docs/51_p0_execution_tracker.md`
- GitHub issue `#4`
