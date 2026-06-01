# Wave 1 第一批 5 页标题候选说明

## 文档用途

本文件说明 `phase2_wave1_first5_title_candidates.csv` 的使用方法。

目标不是一次性拍脑袋定标题，而是把第一批 5 页的标题决策标准固定下来，避免继续出现：

- 工具型查询被写成金融广告标题
- 标题过长
- 标题虽然带词，但没有直接回答查询意图

## 当前文件

- `phase2_wave1_first5_title_candidates.csv`

字段包括：

- `url`
- `primary_query`
- `recommended_title`
- `title_option_2`
- `title_option_3`
- `publish_status`
- `reason`

## 标题决策原则

### 1. 问题词前置

- 让标题尽量贴近真实搜索问题。
- 对问答型页面，优先用 `What Is`、`How to`、`X for Y` 这样的结构。

### 2. 变量要真实

- 金融问答页可以强调 `daily cap`、`fees`、`international use`。
- 工具型页不能乱带 `fees`、`limits` 这类不相关变量。

### 3. 少空话，多结果

- 避免 `complete guide`、`everything you need to know` 这类宽泛词。
- 标题应让用户看到“这页能给我什么答案”。

## 当前分组

### 暂缓同时发布，先做 overlap review

- 两个 `chase atm withdrawal limit` 页面先保留候选标题，但不建议同时发布同方向改稿。

原因：

- 2026-06-01 live 校验后，两页修正 URL 均为 `200 / index, follow / self canonical`
- 当前风险是两个页面共同覆盖 Chase ATM withdrawal limit 查询簇
- 发布前应先决定主打页面和内链主推版本

### 可进入第一波改稿

- `+52 country code`
- `atm withdrawal limit bank of america`
- `wechat real name verification`

这些页的共同特征是：

- 当前可索引
- 当前主要问题集中在标题、Meta 过长
- 已经具备进入编辑和发布检查的基础条件

## 推荐使用方式

1. 先以 `recommended_title` 为主候选。
2. 编辑审稿时，仅在不改变搜索意图的前提下，从 `title_option_2/3` 中替换。
3. 发布后在 GSC 中跟踪 2-3 周 CTR 变化，再决定是否二次迭代标题。

## 本轮结论

当前真正应该先发的，不是所有前 5 页，而是前 5 页中的 3 页：

- `+52 country code`
- `Bank of America ATM withdrawal limit`
- `WeChat real name verification`

这 3 页更适合成为 Wave 1 的第一批上线样板。