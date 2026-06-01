# 100 万月流量目标拆解模型

这个模型用于回答老板最可能追问的问题：这些 P0 修完后，离 100 万月流量到底靠什么增长？

配套 CSV：`docs/phase3_1m_monthly_traffic_target_model.csv`

## 核心判断

100 万月流量不能靠 raw Direct 堆出来。当前策略是先把可运营流量底座修干净，再按已有曝光、模板恢复、内容桥接和规模化页面扩展逐层放大。

## 当前分层

| channel_or_workstream | 当前状态 | 目标角色 | 下一步解锁 |
|---|---|---|---|
| clean Direct | `15,671` | 可信 baseline，不是主要放量来源 | 拆清五类 held Direct |
| held Direct source review | `602,724` | 找出可保留、应排除、应改归因流量 | 数据团队回传 source/referrer |
| compare recovery | 0 个 P0 URL 可用 | 恢复已有搜索需求承接 | 工程修复 Next.js `500` |
| compare SEO handoff | 12 个 URL 已排优先级 | 修复后进入 SEO 提升 | `12/12 pass` 后启动前 5 个 handoff |
| converter template lift | Wave 1 已有资产 | 在 compare blocked 时继续推进 | 继续模板上线和监控 |
| blogdetail bridge | 高曝光内容路径 | 把信息流量导向产品路径 | Direct 拆分后定优先级 |
| programmatic expansion reserve | 未启动 | 后期规模化增量 | 数据口径和模板健康后再开 |

## 为什么现在不能直接承诺 100 万

当前最大问题不是“没有增长动作”，而是：

- Direct 仍有 `602,724` sessions 等待归因拆分。
- compare 已有 11 万级曝光，但 P0 URL 当前仍是 `500`。
- 如果现在扩页面，会把技术债和归因污染放大。

## 先后顺序

1. Direct：先把 held Direct 拆成 clean / search / app / campaign / log-review。
2. Compare：先修 `500`，再做 SEO handoff。
3. Converter：保持已可用模板的上线和监控。
4. Blogdetail：用桥接模块把内容页流量导到工具/转化路径。
5. Programmatic：等模板健康后再规模化。

## 老板可听版本

现在不是马上把数字做大，而是先保证增长数字是真的。

一旦 Direct 口径可信、compare 能承接、converter 和 blogdetail 能持续上线，100 万月流量才有可复用的增长路径。否则只是把脏数据和坏页面一起放大。
