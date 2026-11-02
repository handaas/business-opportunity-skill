---
name: business-opportunity-report
description: Use for generating a 商机挖掘报告 (商机挖掘, 销售线索, 客户评估, 商业机会, 销售评估). Directly connects to 6 MCP servers (enterprise / operation / bidding / news / cloudmigration / recruitment), pulls raw data, and runs cross-domain analysis — sales lead matching, digital touchpoints, market reputation, expansion momentum — producing an evidence-bound lead observation report, not an opportunity score or purchase-intent prediction. Trigger when users ask for "商机挖掘", "销售线索", "客户评估", "商业机会", "销售评估". Infer the enterprise name, connect MCPs, cross-analyze, and produce factual metrics, evidence gaps, and a manual-verification boundary.
---

# 商机挖掘报告

## 定位

销售线索 / 商机评估 skill。**直接连接 6 个 MCP server**（工商 / 经营 / 标讯 / 舆情 / 上云 / 招聘），获取多源原始数据，运行**跨维度交叉分析**。

- MCP 返回的嵌套 JSON 字符串（如金额 `{"coinType":"人民币","value":430000000.0}`、地址 `{"city":"杭州市",...}`）必须解析为可读文本（如"4.30 亿 人民币"、"浙江省杭州市"），绝不在报告正文、表格或指标中输出原始 JSON 字符串。
- 报告所有章节标题、指标卡标签必须用中文；`core_analysis.sections` 的 `title` 字段必须中文，不可显示英文 key（如 `holders`、`investments`）。
- 指标值必须可读化：金额格式为"X 亿/万 + 币种"，地址拼接省市区，比率显示百分号。详见 `references/report-output.md` 的「数据格式约束」。

## 默认路径边界

默认 direct-mcp 不生成自定义综合/专项分、雷达图或评分仪表盘。`--reports-dir`、`--skills-dir`、`--no-direct-mcp` 的历史融合路径不纳入本轮直连验收，不能用其历史分数作决策。空值和主体未确认须保留，不将未查询司法风险解释为低风险。

## 查询成本与分页纪律（必读）

1. **每次调用、每一页都计费。** 想算总页数/总数不是拉全量的授权；没有明确预算时绝不自动翻到 total。
2. **先规划后调用。** 动手前先明确：报告需要哪些结论、每个结论需要哪些数据维度、要调哪些工具和参数、每接口必要页数、最大调用预算。总数未知时，第一页明细既是数据也是 total 发现，**同一页绝不付第二次费**。
3. **优先统计/画像/聚合接口。** 能由统计口径回答的不用明细接口；只取结论、图表、代表性记录或明确"全量/计数"需求所需的明细。只有用户真要求综合报告才跑全管线，绝不"因为工具存在就全调"。
4. **用 schema 允许且合理的大 pageSize，够了就停。** 在明确预算内取到所需证据/样本即停止；追加调用必须来自"缺结论"，而不是"想填满所有章节"。不得用样本分布冒充全量结论来省调用。
5. **同一任务内复用相同请求。** 相同 tool+参数只调一次（含第一页规划数据，一律复用）；渲染只用已落盘 JSON，不重跑 compose/MCP；不自动重试、不重复取统计/明细、不并行取相同数据。补充查询必须先列出具体缺口并复用已有记录。
6. **total_pages/remaining_pages 是按请求 pageSize 的估算。** 预算内短页但上游仍有剩余记录时继续翻页；只有稳定有效的 total 与实际扫描条数相等才算"完整"。错误、提前空页、重复页、total 漂移/缺失、超量都算"不完整"。预算或样本截停是部分采集，**绝不宣称全量**。禁止无关工具/维度调用。

预算不足以支撑关键结论时：先在报告中说明证据缺口与预计需要的额外页数，再请求扩大授权；不得悄悄降级结论，也不得擅自扩大计费范围。

### 分页实现口径

- `compose_fusion_report.py` 新增 `--max-pages N`（正整数，默认 1 页）；每接口的分页明细页数预算，非法值在任何真实调用前被拒绝。
- 直连模式下，分页明细接口（`bid_bigdata_bidding_info` 每页 ≤50、`operation_insight_enterprise_rankings` 每页 ≤10）走统一的 total 驱动采集：第 1 页同时用于分析与上游 total 发现，不重复计费；后续页仅在预算内按 total 规划翻页。
- 报告 `data_source.pagination` 与 `data_source.call_usage` 会披露每接口的上游 total、预计页数、实际请求页数、取得/未纳入条数与停止原因；`abstract`/`summary`/`caliber.limit` 同步可见。
- 模糊查询主体确认（`enterprise_get_keyword_search`）不做分页；统计/画像接口（news_stats、bid_win_stats、procurement_stats、financing_info、business_scale、trends、recruitment trend/profile、cloud_assets 等）单次调用不翻页；`enterprise_get_enterprise_invest_info` 与 `enterprise_get_enterprise_main_person_info` 返回 resultList+total 但工具参数不含分页，保持单次调用并在报告中披露 total 与未纳入条数。

## 直连的 6 个 MCP

| MCP server | 工具 | 数据用途 |
| --- | --- | --- |
| enterprise-mcp-server | base_info / holders / invest / main_person | 工商基础、股权 |
| enterprise-operation-mcp-server | business_scale / financing / trends / rankings | 经营规模、资本运作 |
| bidding-mcp-server | procurement_stats / bid_win_stats / bidding_info | 采购需求、中标能力 |
| news-mcp-server | news_stats | 舆情健康、市场口碑 |
| cloudmigration-mcp-server | cloudmigration_stats | 数字化程度、云资产 |
| recruitment-mcp-server | trend / employer_profile | 招聘活跃度、扩张信号 |

## 交叉分析产出

| 产出 | 说明 |
| --- | --- |
| 事实指标 | 采购、中标、经营、招聘、云资产和舆情的可追溯字段，不生成商机分或成交概率 |
| 线索观察 | 数据缺口、未查询的司法/合规边界及人工核验项；不将平台记录当采购意向 |
| 跨维度洞察 | 销售线索匹配 / 数字化触点 / 市场口碑 / 扩张动能 |

## 脚本速查

```bash
# 默认：直连多 MCP（明细接口按默认 1 页预算采集并披露 total）
python scripts/compose_fusion_report.py --enterprise "某公司" --output output/商机.json --report-output output/商机.html
# 明确扩大明细页数预算（每页计费，先规划结论与维度再定）
python scripts/compose_fusion_report.py --enterprise "某公司" --max-pages 3 --output output/商机.json --report-output output/商机.html
# dry-run
python scripts/compose_fusion_report.py --enterprise "某公司" --dry-run --output output/商机.json --report-output output/商机.html
```

### 付费主体校验与批次

- 主体模糊查询也是付费请求，计入本任务调用次数并进入同一请求复用范围；存在多个候选或无法确认时立即停止其他维度查询，返回候选名称供选择，不能为不确定主体继续购买数据。显式企业标识不额外做名称模糊查询。
- 可分页标讯、开庭、限高和渠道明细采用接口允许的 50 条批次；企业上榜保持 schema 上限 10 条，减少相同采集范围的分页调用。预算仍为每数据源最多页数，不是全报告总调用次数。
- 招聘画像已包含趋势汇总所需字段，只购买一次同主体统计结果，在本地复用，不再另查招聘趋势工具。
