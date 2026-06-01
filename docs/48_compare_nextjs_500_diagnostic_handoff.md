# Compare Next.js `500` 诊断交接包

本包把最新 live 回归结果从“页面失败”推进到“工程可定位的故障指纹”。

当前结论：12 个 P0 compare URL 仍然全部失败，而且失败指纹完全一致。这更像 compare 模板的 Next.js 服务端渲染、路由解析或数据加载共性异常，不像单个币种 pair 或单个 URL 的内容问题。

## 支撑文件

- `scripts/validate_compare_live_urls.py`
- `docs/phase3_compare_live_regression_current.csv`
- `docs/phase3_compare_live_error_fingerprint.csv`
- `docs/phase2_compare_p0_fix_acceptance.csv`
- `docs/40_compare_postfix_validation_pack.md`

## 最新回归结果

2026-06-01 重新运行：

```bash
.venv/bin/python scripts/validate_compare_live_urls.py
```

结果：

- checked：`12`
- passed：`0`
- failed：`12`
- status：`500` for all checked URLs
- `x-powered-by`：`Next.js` for all checked URLs
- body bytes：`21` for all checked URLs
- body preview：`Internal Server Error` for all checked URLs
- body hash：`e41656eb2ba6c6293bf6dd928e5a88cdbc50535cab661c1969e0f598e497ed62` for all checked URLs

## 为什么这比上一版证据更强

上一版只能说明 compare URL 返回 `500`。

新版脚本已经记录：

- 响应头
- `x-powered-by`
- body byte size
- body SHA-256
- body preview

12 个 URL 的指纹完全一致，说明问题应优先从共享模板/runtime 层查，而不是逐条 URL 做内容修复。

## 受影响 URL 类型

失败覆盖了：

- singular route：`exchange-rate`
- plural route：`exchange-rates`
- 不同币种 pair：`USD-PHP`、`AED-INR`、`JPY-USD`、`HKD-USD` 等
- 不同 amount：`1500`、`3000`、`20000`

因此最可疑故障域为：

1. compare route slug parser 无法稳定解析 `best-XXX-YYY-exchange-rate(s)`。
2. `amount` query 参数进入 SSR/data loader 后触发未捕获异常。
3. 汇率/报价 provider 对某些 pair 或 amount 返回空值，模板没有 fallback。
4. Next.js server component / `getServerSideProps` / route handler 中有未捕获异常。
5. plural 与 singular canonical 逻辑在服务端加载阶段崩溃。

## 工程排查建议

请工程侧按这个顺序查：

1. 在生产日志中按这 12 个 request path 搜索 500 stack trace。
2. 日志必须带出 `fromCurrency`、`toCurrency`、`amount`、route slug、provider response status。
3. 先用 `USD-PHP amount=1500` 和 `AED-INR amount=3000` 本地复现。
4. 临时关闭实时 provider 后，用缓存或静态 fallback 渲染页面，判断是否仍 500。
5. 分别测试无 `amount`、非法 `amount`、plural route、singular route。

## 最小修复标准

修复不是只让页面不报错。验收必须满足：

- 12 个 P0 URL 全部返回 `200`
- title 非空
- meta description 非空
- H1 非空
- canonical 非空
- robots 包含 `index`
- 页面首屏保留 pair 和 amount 语境
- provider 异常时页面有 fallback，不返回 `500`

## 修复后验证

工程修复后立即运行：

```bash
.venv/bin/python scripts/validate_compare_live_urls.py
.venv/bin/python - <<'PY'
import duckdb
conn = duckdb.connect('data/warehouse/biyapay.duckdb')
for sql_file in [
    'queries/compare_postfix_live_regression_summary.sql',
    'queries/compare_postfix_large_pattern_health.sql',
    'queries/compare_postfix_target_inlinks.sql',
]:
    print(sql_file)
    for row in conn.sql(open(sql_file).read()).fetchall():
        print(row)
PY
```

只有 `12/12 pass` 后，compare 才进入 SEO handoff。

## 当前执行结论

compare 仍是 P0 技术阻塞。

SEO 团队当前不应继续为 compare 写最终 title/meta 或 CMS 交付表。下一步 owner 是工程：修 compare route/runtime/data fallback，并用本包脚本回归。
