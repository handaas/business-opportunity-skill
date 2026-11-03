# 扩张型企业销售线索

- 用户需求：分析比亚迪股份有限公司的招聘、经营和招采活跃度，判断扩张带来的企业服务需求。
- 决策用途：识别扩张期潜在采购需求。
- 本轮结果：**本轮检查通过**
- 实际工具调用：15；失败 0
- 章节覆盖率：100%（不代表证据质量）

## 预期业务检查（不自动宣称通过）

- 招聘趋势和采购记录时间口径清楚
- 扩张判断引用多个维度
- 中标能力与采购需求不混淆
- 异常空数据不转为零

## 本轮自动检查发现


## 使用局限

- 招聘增长不必然产生外部采购
- 报告不预测具体采购金额

## 证据与复现

- [审计结果](result.json)
- [工具调用、结果形态与响应摘要哈希](calls.json)
- [JSON](report.json) / [HTML](report.html) / [Markdown](report.md)

```bash
python3 business-opportunity-skill/scripts/compose_fusion_report.py --enterprise '比亚迪股份有限公司' --keyword-type name --output business-opportunity-skill/output/03-rapid-hiring/report.json --report-output business-opportunity-skill/output/03-rapid-hiring/report.html
```

## 逐场景业务复核

当前冻结产物逐项满足场景契约；结论仅限本轮公开数据和报告口径。

- **pass** 招聘趋势和采购记录时间口径清楚：通过：generated_at=2026-10-26T18:02:59+08:00；招聘章节={"current": 125052, "last_3m": 125052, "avg_salary": 7864.3639030064, "welfare": []}；当前招聘公开数=125052、近三月招聘公开数=125052；趋势/章节注=。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=比亚迪股份有限公司，resolved=True；metrics[标讯记录总量=1000；中标标的统计合计=9；当前招聘公开数=126960；近三月招聘公开数=126960；有效域名数=127；舆情统计总量=5131；负面舆情统计=156]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/1000)；operation:operation_insight_financing_info=data；operation:operation_insight_business_scale=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(10/76)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/109)；enterprise:enterprise_get_enterprise_main_person_info=data(6/6)]
- **pass** 扩张判断引用多个维度：通过：招聘工具状态=data/data，招聘章节={"current": 125052, "last_3m": 125052, "avg_salary": 7864.3639030064, "welfare": []}；当前招聘公开数=125052、近三月招聘公开数=125052。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=比亚迪股份有限公司，resolved=True；metrics[标讯记录总量=1000；中标标的统计合计=9；当前招聘公开数=126960；近三月招聘公开数=126960；有效域名数=127；舆情统计总量=5131；负面舆情统计=156]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/1000)；operation:operation_insight_financing_info=data；operation:operation_insight_business_scale=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(10/76)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/109)；enterprise:enterprise_get_enterprise_main_person_info=data(6/6)]
- **pass** 中标能力与采购需求不混淆：通过：标讯记录总量=1000、中标标的统计合计=9；采购统计调用=empty、中标统计调用=data；报告章节=dict。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=比亚迪股份有限公司，resolved=True；metrics[标讯记录总量=1000；中标标的统计合计=9；当前招聘公开数=126960；近三月招聘公开数=126960；有效域名数=127；舆情统计总量=5131；负面舆情统计=156]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/1000)；operation:operation_insight_financing_info=data；operation:operation_insight_business_scale=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(10/76)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/109)；enterprise:enterprise_get_enterprise_main_person_info=data(6/6)]
- **pass** 异常空数据不转为零：通过：无对应指标；开庭当前展示0条，其中日期非空0条、案号非空0条；章节注=。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=比亚迪股份有限公司，resolved=True；metrics[标讯记录总量=1000；中标标的统计合计=9；当前招聘公开数=126960；近三月招聘公开数=126960；有效域名数=127；舆情统计总量=5131；负面舆情统计=156]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/1000)；operation:operation_insight_financing_info=data；operation:operation_insight_business_scale=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(10/76)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/109)；enterprise:enterprise_get_enterprise_main_person_info=data(6/6)]

## 离线浏览器检查

[Ego Lite 离线图表、页面溢出和脚本检查](browser-check.json)