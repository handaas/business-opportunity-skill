# 舆情风险商机筛查

- 用户需求：分析恒大地产集团有限公司的经营、采购和舆情风险，判断是否应暂缓销售投入。
- 决策用途：避免在高风险客户上投入不匹配的销售资源。
- 本轮结果：**本轮检查通过**
- 实际工具调用：15；失败 0
- 章节覆盖率：83%（不代表证据质量）

## 预期业务检查（不自动宣称通过）

- 负面舆情有数量或记录依据
- 风险信号不会被高采购量完全抵消
- 商机结论说明数据时点
- 不输出信用违约法律结论

## 本轮自动检查发现


## 使用局限

- 舆情不是完整信用评估
- 实际回款与合同风险需独立调查

## 证据与复现

- [审计结果](result.json)
- [工具调用、结果形态与响应摘要哈希](calls.json)
- [JSON](report.json) / [HTML](report.html) / [Markdown](report.md)

```bash
python3 business-opportunity-skill/scripts/compose_fusion_report.py --enterprise '恒大地产集团有限公司' --keyword-type name --output business-opportunity-skill/output/05-reputation-screening/report.json --report-output business-opportunity-skill/output/05-reputation-screening/report.html
```

## 逐场景业务复核

当前冻结产物逐项满足场景契约；结论仅限本轮公开数据和报告口径。

- **pass** 负面舆情有数量或记录依据：通过：舆情统计总量=3164、负面舆情统计=1019；news_bigdata_news_stats=data；HTML/MD风险限制同时可见=True。；本轮当前产物：technical=passed，successful_data_calls=13；subject.enterprise=恒大地产集团有限公司，resolved=True；metrics[标讯记录总量=68；中标标的统计合计=13；当前招聘公开数=1220；近三月招聘公开数=1220；舆情统计总量=3164；负面舆情统计=1019]；quality={'total_sections': 6, 'populated_sections': 5, 'empty_sections': 1, 'coverage_pct': 83}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '招聘公开线索']；代表记录=6；calls[cloudmigration:cloudmigration_cloud_assets=empty；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/68)；bidding:bid_bigdata_procurement_stats=empty；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(10/11)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/195)；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_main_person_info=data(6/6)]
- **pass** 风险信号不会被高采购量完全抵消：通过：标讯记录总量=68、中标标的统计合计=13；采购统计调用=empty、中标统计调用=data；报告章节=dict。；本轮当前产物：technical=passed，successful_data_calls=13；subject.enterprise=恒大地产集团有限公司，resolved=True；metrics[标讯记录总量=68；中标标的统计合计=13；当前招聘公开数=1220；近三月招聘公开数=1220；舆情统计总量=3164；负面舆情统计=1019]；quality={'total_sections': 6, 'populated_sections': 5, 'empty_sections': 1, 'coverage_pct': 83}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '招聘公开线索']；代表记录=6；calls[cloudmigration:cloudmigration_cloud_assets=empty；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/68)；bidding:bid_bigdata_procurement_stats=empty；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(10/11)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/195)；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_main_person_info=data(6/6)]
- **pass** 商机结论说明数据时点：通过：generated_at=2026-10-26T18:03:06+08:00；招聘章节={"current": 1220, "last_3m": 1220, "avg_salary": 15304.2904321228, "welfare": []}；当前招聘公开数=1220、近三月招聘公开数=1220；趋势/章节注=。；本轮当前产物：technical=passed，successful_data_calls=13；subject.enterprise=恒大地产集团有限公司，resolved=True；metrics[标讯记录总量=68；中标标的统计合计=13；当前招聘公开数=1220；近三月招聘公开数=1220；舆情统计总量=3164；负面舆情统计=1019]；quality={'total_sections': 6, 'populated_sections': 5, 'empty_sections': 1, 'coverage_pct': 83}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '招聘公开线索']；代表记录=6；calls[cloudmigration:cloudmigration_cloud_assets=empty；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/68)；bidding:bid_bigdata_procurement_stats=empty；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(10/11)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/195)；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_main_person_info=data(6/6)]
- **pass** 不输出信用违约法律结论：通过：abstract=本报告对「恒大地产集团有限公司」进行商机事实整理。报告仅列示可核验的采购、中标、经营、招聘、云资产和舆情事实，不生成商机分或成交概率。；评分指标=无对应指标；coverage=83%，insights=[{"feature": "中标业绩边界", "evidence": "中标标的统计项 5、标讯记录总量 68。", "interpretation": "仅说明供应方历史市场活动；采购侧统计为空，不能据此宣称该企业存在采购需求。"}, {"feature": "扩张活动交叉线索", "evidence": "经营趋势命中 2 项；当前招聘 1220、近三月招聘 1220。", "interpretation": "经营与招聘两个独立域同时出现活动信号；仅构成扩张观察，不能推定采购预算。"}, {"feature": "负面舆情提示", "evidence": "情感统计中负面 1019 条，总量 3164 条。", "interpretation": "应人工复核负面样本、时间和相关性；本报告未查询司法/合规风险，不作信用或法律结论。"}]。；本轮当前产物：technical=passed，successful_data_calls=13；subject.enterprise=恒大地产集团有限公司，resolved=True；metrics[标讯记录总量=68；中标标的统计合计=13；当前招聘公开数=1220；近三月招聘公开数=1220；舆情统计总量=3164；负面舆情统计=1019]；quality={'total_sections': 6, 'populated_sections': 5, 'empty_sections': 1, 'coverage_pct': 83}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '招聘公开线索']；代表记录=6；calls[cloudmigration:cloudmigration_cloud_assets=empty；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/68)；bidding:bid_bigdata_procurement_stats=empty；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(10/11)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/195)；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_main_person_info=data(6/6)]

## 离线浏览器检查

[Ego Lite 离线图表、页面溢出和脚本检查](browser-check.json)