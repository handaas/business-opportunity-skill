# 上云服务商机识别

- 用户需求：分析海尔智家股份有限公司的云资产、经营与招聘信号，寻找数字化升级触点。
- 决策用途：判断云服务与数字化解决方案切入点。
- 本轮结果：**本轮检查通过**
- 实际工具调用：15；失败 0
- 章节覆盖率：100%（不代表证据质量）

## 预期业务检查（不自动宣称通过）

- 云资产数据与经营规模分开
- 数字化程度结论有返回字段支撑
- 招聘岗位不被直接解释为采购计划
- 商机建议标注推断性质

## 本轮自动检查发现


## 使用局限

- 云资产可见性受数据源限制
- 需要客户访谈确认真实预算与计划

## 证据与复现

- [审计结果](result.json)
- [工具调用、结果形态与响应摘要哈希](calls.json)
- [JSON](report.json) / [HTML](report.html) / [Markdown](report.md)

```bash
python3 business-opportunity-skill/scripts/compose_fusion_report.py --enterprise '海尔智家股份有限公司' --keyword-type name --output business-opportunity-skill/output/02-cloud-migration/report.json --report-output business-opportunity-skill/output/02-cloud-migration/report.html
```

## 逐场景业务复核

当前冻结产物逐项满足场景契约；结论仅限本轮公开数据和报告口径。

- **pass** 云资产数据与经营规模分开：通过：cloudmigration_cloud_assets=data，云资产字段数=10；有效域名数=35；HTML/MD均呈现当前口径限制=True。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=海尔智家股份有限公司，resolved=True；metrics[标讯记录总量=595；中标标的统计合计=24；当前招聘公开数=750；近三月招聘公开数=750；有效域名数=35；舆情统计总量=3174；负面舆情统计=46]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[news:news_bigdata_news_stats=data；cloudmigration:cloudmigration_cloud_assets=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/595)；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_business_scale=data；operation:operation_insight_enterprise_rankings=data(10/32)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/60)；enterprise:enterprise_get_enterprise_main_person_info=data(13/13)]
- **pass** 数字化程度结论有返回字段支撑：通过：cloudmigration_cloud_assets=data，云资产字段数=10；有效域名数=35；HTML/MD均呈现当前口径限制=True。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=海尔智家股份有限公司，resolved=True；metrics[标讯记录总量=595；中标标的统计合计=24；当前招聘公开数=750；近三月招聘公开数=750；有效域名数=35；舆情统计总量=3174；负面舆情统计=46]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[news:news_bigdata_news_stats=data；cloudmigration:cloudmigration_cloud_assets=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/595)；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_business_scale=data；operation:operation_insight_enterprise_rankings=data(10/32)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/60)；enterprise:enterprise_get_enterprise_main_person_info=data(13/13)]
- **pass** 招聘岗位不被直接解释为采购计划：通过：标讯记录总量=595、中标标的统计合计=24；采购统计调用=empty、中标统计调用=data；报告章节=dict。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=海尔智家股份有限公司，resolved=True；metrics[标讯记录总量=595；中标标的统计合计=24；当前招聘公开数=750；近三月招聘公开数=750；有效域名数=35；舆情统计总量=3174；负面舆情统计=46]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[news:news_bigdata_news_stats=data；cloudmigration:cloudmigration_cloud_assets=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/595)；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_business_scale=data；operation:operation_insight_enterprise_rankings=data(10/32)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/60)；enterprise:enterprise_get_enterprise_main_person_info=data(13/13)]
- **pass** 商机建议标注推断性质：通过：abstract=本报告对「海尔智家股份有限公司」进行商机事实整理。报告仅列示可核验的采购、中标、经营、招聘、云资产和舆情事实，不生成商机分或成交概率。；评分指标=无对应指标；coverage=100%，insights=[{"feature": "中标业绩边界", "evidence": "中标标的统计项 5、标讯记录总量 595。", "interpretation": "仅说明供应方历史市场活动；采购侧统计为空，不能据此宣称该企业存在采购需求。"}, {"feature": "扩张活动交叉线索", "evidence": "经营趋势命中 5 项；当前招聘 750、近三月招聘 750。", "interpretation": "经营与招聘两个独立域同时出现活动信号；仅构成扩张观察，不能推定采购预算。"}, {"feature": "云资产触点", "evidence": "有效域名 35，云服务器区间 500-1000台。", "interpretation": "说明存在可观测云资产触点；不能据此评价数字化成熟度、迁移意向或预算。"}, {"feature": "负面舆情提；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=海尔智家股份有限公司，resolved=True；metrics[标讯记录总量=595；中标标的统计合计=24；当前招聘公开数=750；近三月招聘公开数=750；有效域名数=35；舆情统计总量=3174；负面舆情统计=46]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[news:news_bigdata_news_stats=data；cloudmigration:cloudmigration_cloud_assets=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/595)；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_business_scale=data；operation:operation_insight_enterprise_rankings=data(10/32)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/60)；enterprise:enterprise_get_enterprise_main_person_info=data(13/13)]

## 离线浏览器检查

[Ego Lite 离线图表、页面溢出和脚本检查](browser-check.json)