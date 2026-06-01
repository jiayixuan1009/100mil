# 老板周报口径简报

## 本周最重要结论

### 1. Direct 总量不能再直接作为增长 KPI

当前真正可直接保留为主站品牌直达的核心首页桶只有 `37,783` sessions。

但同时存在：

- `signup/download + fastreg`：`43,262` sessions
- 非生产/外部 host：`37,842` sessions
- 主站内容/工具 Direct 大桶：`736,111` sessions

结论：如果继续直接汇报 raw Direct，会把下载回流、活动流量、模板流量和污染 host 当成真实增长。

### 2. 主站内容/工具 Direct 大桶已经确认混入非真实直达信号

最新复核显示，`www` 大桶中至少包括：

- `69,143` sessions 带 `amount=` 参数
- `5,344` sessions 带 `utm_` 活动参数
- `2,817` sessions 带明显 WebView/embed 参数

结论：这部分不能整体并入 clean Direct，必须继续补 source/referrer 或日志证据。

### 3. compare 仍是模板级 P0 阻塞

live 检查显示：

- compare 的有 `amount` / 无 `amount`
- 单数 route / 复数 route
- 不同币种 pair

全部返回同一个 21 字节 `Internal Server Error`，说明不是单条 URL 问题，而是更早的 Next.js 服务端渲染/数据加载失败。

结论：compare 还不能进入 SEO handoff，必须先修模板级技术阻塞。

## 当前优先级

1. 给老板看 clean Direct，不再看 raw Direct。
2. 补主站 `source/referrer/channel` 导出，继续拆 `www` 大桶。
3. 推进 compare 模板工程修复并重跑回归验收。

## 风险

- 如果不先修口径，100 万流量目标会继续建立在污染数据上。
- 如果 compare 不修，已有曝光无法承接，SEO 动作无法闭环。
- 如果 `www` 大桶不继续拆，后续任何增长归因都会失真。

## 需要团队本周给的输入

- 主站 GA4 `landing page + channel/source/referrer` 导出
- compare 模板服务端错误日志或工程控制代码位置
- `cn.biyapay.com / biyapay.com` 的当前迁移与跳转策略确认

## 当前建议汇报口径

- 对外/对老板：`clean Direct`、`host pollution`、`lifecycle/app return`、`needs review`
- 对执行团队：继续用 raw 明细排查，但不把 raw Direct 当结果 KPI
