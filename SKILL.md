---
name: business-opportunity-report
description: Use for generating a 商机挖掘报告 (商机挖掘, 销售线索, 客户评估, 商业机会, 销售评估). Directly connects to 6 MCP servers (enterprise / operation / bidding / news / cloudmigration / recruitment), pulls raw data, and runs cross-domain analysis — sales lead matching, digital touchpoints, market reputation, expansion momentum — producing a scored opportunity assessment report. Trigger when users ask for "商机挖掘", "销售线索", "客户评估", "商业机会", "销售评估". Infer the enterprise name, connect MCPs, cross-analyze, and produce a radar + gauge + verdict report.
---

# 商机挖掘报告

## 定位

销售线索 / 商机评估 skill。**直接连接 6 个 MCP server**（工商 / 经营 / 标讯 / 舆情 / 上云 / 招聘），获取多源原始数据，运行**跨维度交叉分析**。

- MCP 返回的嵌套 JSON 字符串（如金额 `{"coinType":"人民币","value":430000000.0}`、地址 `{"city":"杭州市",...}`）必须解析为可读文本（如"4.30 亿 人民币"、"浙江省杭州市"），绝不在报告正文、表格或指标中输出原始 JSON 字符串。
- 报告所有章节标题、指标卡标签必须用中文；`core_analysis.sections` 的 `title` 字段必须中文，不可显示英文 key（如 `holders`、`investments`）。
- 指标值必须可读化：金额格式为"X 亿/万 + 币种"，地址拼接省市区，比率显示百分号。详见 `references/report-output.md` 的「数据格式约束」。

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
| 专项评分 | 商业活跃度 / 数字化程度 / 经营动能 / 市场潜力（0-100） |
| 商机评估 | 优质商机 / 一般商机 / 需培育 / 暂无机会 |
| 跨维度洞察 | 销售线索匹配 / 数字化触点 / 市场口碑 / 扩张动能 |

## 脚本速查

```bash
# 默认：直连多 MCP
python scripts/compose_fusion_report.py --enterprise "某公司" --output output/商机.json --report-output output/商机.html
# dry-run
python scripts/compose_fusion_report.py --enterprise "某公司" --dry-run --output output/商机.json --report-output output/商机.html
```
