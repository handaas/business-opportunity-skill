# 零售企业数字化商机

- 用户需求：评估永辉超市股份有限公司的经营、云资产、招聘与新闻信号，寻找零售数字化商机。
- 决策用途：支持零售行业解决方案拓客。
- 本轮结果：**本轮检查通过**
- 实际工具调用：15；失败 0
- 章节覆盖率：100%（不代表证据质量）

## 预期业务检查（不自动宣称通过）

- 云资产与招聘信号相互独立
- 经营趋势不被新闻数量替代
- 商机触点注明推断依据
- 数据缺口明确列出

## 本轮自动检查发现


## 使用局限

- 不能仅凭公开数据确认系统采购计划
- 门店经营细节不在本报告覆盖范围

## 证据与复现

- [审计结果](result.json)
- [工具调用、结果形态与响应摘要哈希](calls.json)
- [JSON](report.json) / [HTML](report.html) / [Markdown](report.md)

```bash
python3 business-opportunity-skill/scripts/compose_fusion_report.py --enterprise '永辉超市股份有限公司' --keyword-type name --output business-opportunity-skill/output/06-regional-retail/report.json --report-output business-opportunity-skill/output/06-regional-retail/report.html
```

## 逐场景业务复核

当前冻结产物逐项满足场景契约；结论仅限本轮公开数据和报告口径。

- **pass** 云资产与招聘信号相互独立：通过：cloudmigration_cloud_assets=data，云资产字段数=10；有效域名数=20；HTML/MD均呈现当前口径限制=True。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=永辉超市股份有限公司，resolved=True；metrics[标讯记录总量=281；中标标的统计合计=14；当前招聘公开数=1323；近三月招聘公开数=1323；有效域名数=20；舆情统计总量=3904；负面舆情统计=717]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_enterprise_rankings=data(10/33)；operation:operation_insight_company_trends=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/281)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/84)；enterprise:enterprise_get_enterprise_main_person_info=data(10/10)]
- **pass** 经营趋势不被新闻数量替代：通过：generated_at=2026-10-26T18:03:06+08:00；招聘章节={"current": 1323, "last_3m": 1323, "avg_salary": 8187.6161021955, "welfare": []}；当前招聘公开数=1323、近三月招聘公开数=1323；趋势/章节注=。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=永辉超市股份有限公司，resolved=True；metrics[标讯记录总量=281；中标标的统计合计=14；当前招聘公开数=1323；近三月招聘公开数=1323；有效域名数=20；舆情统计总量=3904；负面舆情统计=717]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_enterprise_rankings=data(10/33)；operation:operation_insight_company_trends=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/281)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/84)；enterprise:enterprise_get_enterprise_main_person_info=data(10/10)]
- **pass** 商机触点注明推断依据：通过：subject.resolved=True；quality={"total_sections": 6, "populated_sections": 6, "empty_sections": 0, "coverage_pct": 100}；metrics=[{"label": "标讯记录总量", "value": "281", "hint": "含投标/中标公开记录，不等同采购需求"}, {"label": "中标标的统计合计", "value": "14", "hint": "供应方历史中标分布，不能替代买方采购意向"}, {"label": "当前招聘公开数", "value": "1323", "hint": "招聘活跃线索，不代表采购计划"}, {"label": "近三月招聘公开数", "value": "1323", "hint": "招聘接口口径，需结合采集时点"}, {"label": "有效域名数", "value": "20", "hint": "云资产触点，不代表数字化成熟度或预算"}, {"label": "舆情统计总量", "value": "3904",；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=永辉超市股份有限公司，resolved=True；metrics[标讯记录总量=281；中标标的统计合计=14；当前招聘公开数=1323；近三月招聘公开数=1323；有效域名数=20；舆情统计总量=3904；负面舆情统计=717]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_enterprise_rankings=data(10/33)；operation:operation_insight_company_trends=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/281)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/84)；enterprise:enterprise_get_enterprise_main_person_info=data(10/10)]
- **pass** 数据缺口明确列出：通过：subject.resolved=True；quality={"total_sections": 6, "populated_sections": 6, "empty_sections": 0, "coverage_pct": 100}；metrics=[{"label": "标讯记录总量", "value": "281", "hint": "含投标/中标公开记录，不等同采购需求"}, {"label": "中标标的统计合计", "value": "14", "hint": "供应方历史中标分布，不能替代买方采购意向"}, {"label": "当前招聘公开数", "value": "1323", "hint": "招聘活跃线索，不代表采购计划"}, {"label": "近三月招聘公开数", "value": "1323", "hint": "招聘接口口径，需结合采集时点"}, {"label": "有效域名数", "value": "20", "hint": "云资产触点，不代表数字化成熟度或预算"}, {"label": "舆情统计总量", "value": "3904",；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=永辉超市股份有限公司，resolved=True；metrics[标讯记录总量=281；中标标的统计合计=14；当前招聘公开数=1323；近三月招聘公开数=1323；有效域名数=20；舆情统计总量=3904；负面舆情统计=717]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_enterprise_rankings=data(10/33)；operation:operation_insight_company_trends=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/281)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/84)；enterprise:enterprise_get_enterprise_main_person_info=data(10/10)]

## 离线浏览器检查

[Ego Lite 离线图表、页面溢出和脚本检查](browser-check.json)