# Converter 查询意图与首屏模块规格

## 文档用途

本文件把 6 个 converter 页的 GSC 查询数据转成产品和前端可执行的首屏模块规格。

配套文件：

- `phase2_wave1_converter_gsc_queries.csv`
- `phase2_wave1_converter_query_summary.csv`
- `phase2_wave1_converter_ux_modules.csv`
- `phase2_wave1_converter_cms_handoff.csv`

## 数据发现

Converter 页的曝光不是只来自币种对短词，而是大量来自具体金额查询。

例子：

- `1000日元兌港元`
- `3000欧元等于多少美元`
- `20000泰铢等于多少美金`
- `100万日元等于多少美金`
- `1000比索是多少美元`
- `685000 dirham to pkr`

因此，converter 首屏必须有 amount chips，不能只显示一个默认换算框。

## 统一首屏模块

每个 converter 页首屏必须包含：

- 实时汇率结果
- 更新时间
- amount 输入框
- 推荐金额 chips
- 手续费 / spread 提醒
- 转账或比较 CTA
- 逆向币对或 compare 页入口

## 推荐金额 chips

### JPY-HKD

- `100 JPY`
- `1,000 JPY`
- `2,000 JPY`
- `30,000 JPY`
- `44,000 JPY`
- `9,000,000 JPY`

### EUR-USD

- `1 EUR`
- `15 EUR`
- `1,000 EUR`
- `1,500 EUR`
- `3,000 EUR`

### THB-USD

- `200 THB`
- `1,000 THB`
- `20,000 THB`
- `50,000 THB`

### JPY-USD

- `500,000 JPY`
- `1,000,000 JPY`
- `2,000,000 JPY`
- `15,000,000 JPY`

### PHP-USD

- `1 PHP`
- `1,000 PHP`
- `10,000 PHP`
- `20,000 PHP`
- `50,000 PHP`

### AED-PKR

- `1,100 AED`
- `1,350 AED`
- `179,000 AED`
- `685,000 AED`

## FAQ 模块

每个 converter 页保留 4-5 个 FAQ，不要泛泛解释外汇。

统一方向：

- 汇率多久更新一次
- 换算结果是否包含手续费
- 大额金额和小额金额是否一样
- 实际转账到账金额为什么可能不同
- 如何查看相关币种对或最佳汇率

## 内链模块

每页至少链接：

- 逆向币对 converter
- 对应 compare 页面
- 相关 transfer corridor
- 1-2 个相邻币种对

如果 compare 页面仍为 `500`，先保留入口设计，但上线时不要放死链或错误页入口。

## 埋点要求

建议新增或确认以下事件：

- `converter_amount_change`
- `converter_chip_click`
- `converter_compare_click`
- `converter_transfer_click`
- `converter_download_click`

这些事件用于判断 converter 页是否只带来信息流量，还是能承接到业务动作。

## 发布优先级

先发布曝光最高且 live 正常的页面：

1. `JPY-HKD`
2. `EUR-USD`
3. `THB-USD`
4. `JPY-USD`
5. `PHP-USD`
6. `AED-PKR`

## 当前结论

Converter 模板不应只改 title/meta。

这一批的核心改造是：

- 用真实查询驱动 amount chips
- 首屏工具感前置
- 用 CTA 和埋点验证业务承接