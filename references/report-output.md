# 商机报告内容规范（direct-mcp 事实版）

本文件约束默认 direct-mcp 报告的**内容**。默认路径不生成商机分、成交概率、雷达图或评分仪表盘；历史融合路径的评分不得写入本报告。

## 一、章节与字段

1. 查询对象与口径：主体全称、匹配方式、覆盖域、时间、缺口。
2. 数据总览：只放可追溯事实指标，每个指标带口径提示。
3. 核心分析：主体/经营/采购中标/舆情/云资产/招聘，按有效数据动态出现；空章节整体跳过。
4. 代表性记录：来自同报告指标，不重新计算。
5. 特征与洞察：证据字段 + 解释 + 边界；不把平台记录当采购意向。
6. 数据口径与来源：MCP 数量、模式、生成时间。

## 二、内容整理（原始值 → 标签 → 证据）

| 原始字段 | 规范展示 | 证据位置 | 禁止 |
| --- | --- | --- | --- |
| `financingAmount` / `investorList` | 时间、轮次、金额、投资方逐项文本 | `core_analysis.operation.融资记录` | 输出 JSON/引号/大括号 |
| `win_subjects` / `win_areas` / `win_amounts` | “标的 数量 条，占比 X%” | `core_analysis.bidding` | 合并成“采购需求” |
| `bidding_total` | 标讯记录总量 | metrics / bidding | 当作中标次数或采购预算 |
| `sentiment` | 负面/中立/正面/未知分别列示 | `core_analysis.news.情感分布` | 只报正面占比、隐瞒负面 |
| `cloud_servers` / `cdn_servers` | 去重后逐项列表 | `core_analysis.cloudmigration` | 推断数字化成熟度或迁移意向 |
| `recruitingCurrentCount` / `recruitingLastThreeMonthCount` | 同值时合并为一个观察并注明窗口不可区分 | metrics / recruitment | 当作两次独立扩张信号 |
| `recruitingAvgWorkingSalary` | 保留两位小数 + 元/月 | recruitment | 用整数抹掉精度差异后冒充原值 |
| `is*` 经营趋势标记（值为 `1`） | 逐项中文标签并保留上游字段=1 证据；未收录标签保留原字段并标“未收录标准标签” | `core_analysis.operation.经营趋势命中` | 丢弃未映射命中或为未知标记臆造含义 |

- 数值逐项保留；英文 key 必须转为中文标签。未知值写“未知/未返回”，不得写成 `0`。
- 经营趋势章节的命中条数必须与洞察“经营趋势命中 N 项”一致；值为 `0` 的标记不是命中，不列入命中清单。
- 名称不拼接：标的、区域、服务商、榜单名称按上游原值展示，不做同义词合并或主体拼接。
- 比例保留上游精度；金额统一“X 亿/万 + 币种”；地址按省市区拼接。

## 三、语义审校门禁

1. **相关性**：采购/中标数量只说明供应方历史市场活动；招聘、云资产、域名不等于预算或采购计划。
2. **主题归类**：只有上游字段明确支持时才归入“扩张、采购、数字化、舆情”主题；同义标签合并需两个以上记录或上游明确别名。
3. **时间口径**：招聘、舆情、标讯注明接口窗口；跨时点数值不得直接相加或比较。
4. **主体口径**：主体未确认时，所有章节改为“同名检索线索”，指标提示追加“不归属该主体”。
5. **冲突处理**：上游字段互相矛盾时并列展示并标“待核验”，不擅自取高/取低。
6. **置信度**：样本/单页数据必须写“样本”“当前展示”或“未纳入条数”，不得冒充全量。
7. **保留风险**：负面舆情、数据缺口、未查询的司法/合规边界不删除；不得以“未查询”推导“低风险”。

## 四、AI 审校交付门禁（草稿 → final）

`compose_*` 正常生成与 `--dry-run` 只产出草稿：JSON 标记 `data_source.semantic_review.status=pending`，同名 HTML/Markdown 带“数据草稿（待AI语义审校）”提示，不能交付。`apply_content_review`/`organize_report` 是确定性整理，不是 AI 审校。

```bash
python scripts/review_report.py --input output/draft.json --request output/review-request.json
# 当前 AI 阅读请求中的 report 后写 output/ai-review.json
python scripts/review_report.py --input output/draft.json --review output/ai-review.json \
  --output output/final/report.json --report-output output/final/report.html
```

请求含 `source_sha256`、`report`、`visible_section_keys`、`instructions`、`response_fields`；响应：

```json
{
  "source_sha256": "<与请求一致>",
  "summary": [{"text": "逐句摘要", "sources": ["/core_analysis/..."], "kind": "fact"}],
  "normalizations": [{"sources": ["/core_analysis/..."], "category": "类别", "normalized": "规范表达", "evidence": "原文摘录", "reason": "理由"}],
  "insights": [{"feature": "特征", "evidence": "证据摘录", "interpretation": "解读", "sources": ["/metrics/0"]}]
}
```

- `source_sha256` 必须与请求一致；不一致须重新请求，不能沿用旧判断。
- `sources` 使用 JSON Pointer，只能指向本报告实际存在的 `/subject/…`、`/core_analysis/…`、`/metrics/…`、`/caliber/…`、`/data_source/…`、`/analysis_request/…`；`/core_analysis/sections`、`/data_source/semantic_review` 与旧 `abstract`/`summary`/`insights` 不是事实依据。
- 每项至少一个来源且不能重复路径；同一来源可支持多项判断；不能借其他企业、案例、记录或常识补本记录。
- `summary` 写 3–5 句有信息量的逐句摘要，`kind` 只能是 `fact`/`interpretation`/`limitation`；无数据依据只能写 `limitation`。`normalizations` 是独立视图，原文不改写；`evidence` 必填，由当前 AI 选择简洁可读的原文摘录作为“原文依据”列，并由同项 `sources` 支撑，完整原值仍保留在 draft/request 与来源 SHA 记录中；必须保留否定、最高、至少、至多、试用期、转正后、仅限、部分、疑似、待定、已失效等限定；不同主体、互斥金额或比例不能合并；没有实际归类需要时可为空；`insights` 的 `feature`、`evidence`、`interpretation` 都须由同一 `sources` 支撑；`evidence` 是实际 AI 写的简洁可读证据摘录，保留来源数字、单位与限定。
- 所有文本（含 `normalized`、`category`、`reason`、`evidence`、洞察）中的数字必须逐字出现在所引 values 中，不新造派生数字、不改精度；需要派生指标先在脚本计算再引用。
- 只使用本次数据，不调用 MCP/外部模型 API/新增查询。应用后 `status=reviewed` 并记录来源 SHA-256、原 `generated_at`、审校时间与判断证据；原查询时间和原件不变。`summary` 写入 `abstract`/`summary`/`executive_summary`，`normalizations` 写入 `core_analysis.ai_normalization`（独立表格），`insights` 写入 `insights`；原始字段不改写。

**展示与交付**：空板块连标题和目录一起隐藏，但只能影响展示，不能从 `quality_report` 分母抹去未覆盖维度或提高覆盖率；真实 `0`/`False` 保留，缺失/未查询不等于 0；失败只写口径限制，不推断“无风险”。AI 标准化/摘要是解释视图，不新增数据来源或覆盖率。核对最终 JSON/HTML/Markdown 后才交付；请求文件、草稿或手工润色件不算完成。

## 五、离线复核

已冻结报告可用 `compose_direct.apply_content_review(report, calls=None)` 做纯本地整理：
递归复制报告，将嵌套字段转为中文可读文本，合并同值招聘指标，改写对应洞察证据，逐项保留经营趋势命中（含未收录标签的上游字段），并在 `caliber.limit` 注明“未新增推断”。该函数不调用 MCP，不改变证据文件。

正常生成 `compose_direct.build_direct_payload`（`compose_fusion_report.py` 默认直连模式）在返回前调用同一函数，JSON/HTML/Markdown 使用同一整理结果；重复调用保持幂等。整理只重算章节填充数并保留构建时声明的章节总数，缺失维度不会被折叠成 100% 覆盖；`data["calls"]` / `_meta["calls"]` 存在时作为既有调用证据传入，不触发二次查询。

审校复核：完整保留有来源的摘要句子及采集层“数据缺口／主体解析受阻”提示；重审不得引用 `/core_analysis/ai_normalization` 等既有 AI 视图作为原始证据。HTML 与 Markdown 应使用一致的样本数量、趋势顺序及数据列，单元格中的竖线和换行不得破坏表格结构。
