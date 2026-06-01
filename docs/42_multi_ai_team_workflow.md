# 多 AI 团队协作工作流

本文件定义这个仓库如何同时服务多个 AI 开发工具，而不让项目上下文散掉。

## 目标

让团队成员即使使用不同 AI，也能在同一个项目里沿着同一套目标、优先级、验证规则和交付标准推进。

适用对象包括但不限于：

- GitHub Copilot
- Claude Code / Claude in IDE
- Cursor / 其他编辑器内 AI
- 任何支持读取仓库说明文件的 agent

## 当前做法

### 1. 单一事实源

- `AGENTS.md` 是跨 AI 的共用仓库说明。
- `.github/copilot-instructions.md` 是 Copilot 的补充层。
- `.github/instructions/` 提供文件类型级别的明确规则。
- `.github/prompts/` 提供团队可复用的标准任务入口。
- `README.md` 和 `docs/README.md` 是项目入口，不承载隐藏规则。

### 2. 持久化优先于聊天

任何 AI 产出，优先落成以下一种：

- 文档
- CSV
- SQL
- 脚本
- GitHub issue / comment

这样换一个 AI 或换一个人接手时，不需要依赖历史聊天记录。

### 3. 任务入口固定

不同 AI 开始新任务时，优先顺序应一致：

1. 看 GitHub issue。
2. 看相关专项文档。
3. 看相关 SQL / script。
4. 再做最小补充分析。

### 4. 验证口径固定

- SQL 要执行。
- 脚本要跑最小验证。
- 文档与 CSV 要过诊断检查。
- GitHub 动作要确认已创建或已评论。

## 推荐团队分工

### AI A：数据与口径

负责：

- Direct 清洗
- hostname/cross-domain 复核
- DuckDB SQL 与仓库视图
- 老板汇报口径

### AI B：技术阻塞与验收

负责：

- compare / converter / template blocker 诊断
- live URL 校验
- 工程 handoff
- 验收脚本与结果文档

### AI C：内容与 rollout

负责：

- Wave 1 页面 brief
- CMS handoff
- title/meta/FAQ/CTA 模块
- launch tracker 与复盘

## 协作边界

- 不把大仓库产物提交进 Git。
- 不重复生成已有文档的同义版本。
- 不绕过 GitHub issue 自己重新定义优先级，除非写明依据并更新 issue。
- 不把 raw Direct 当成 clean Direct 使用。

## 新 AI 接手步骤

新接手的 AI 建议按这个顺序：

1. 读 `AGENTS.md`
2. 读 `.github/copilot-instructions.md`（如果当前工具支持）
3. 看 `.github/instructions/` 与当前文件类型最相关的规则
4. 读 `README.md`
5. 读 `docs/README.md`
6. 如果当前工具支持 prompt files，优先使用 `.github/prompts/`
7. 打开当前 GitHub issue
8. 只读取最近邻的文档 / SQL / 脚本

## 当前建议

目前这个仓库最适合继续按三条并行线推进：

1. Direct clean reporting 与 `www` 大桶深挖。
2. compare 模板阻塞诊断与验证闭环。
3. Wave 1 内容/模板上线和监控。

## 完成标准

当团队换一个 AI 工具继续工作时，仍然能做到：

- 知道当前项目目标和优先级。
- 找到最近的真实执行入口。
- 不把历史聊天当成唯一上下文。
- 产出继续沉淀到仓库和 GitHub，而不是只留在会话里。