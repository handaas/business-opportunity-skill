# 科技企业增长商机

- 用户需求：分析小米科技有限责任公司的经营、招聘、云资产和招投标信号，评估企业服务商机。
- 决策用途：识别成长型科技企业的服务需求线索。
- 本轮结果：**本轮检查通过**
- 实际工具调用：15；失败 0
- 章节覆盖率：100%（不代表证据质量）

## 预期业务检查（不自动宣称通过）

- 主体解析无歧义
- 增长动能引用经营和招聘证据
- 云资产条目不被当作预算证明
- 商机等级和证据强度匹配

## 本轮自动检查发现


## 使用局限

- 公开信号只用于线索排序
- 实际需求、预算和决策链需销售核实

## 证据与复现

- [审计结果](result.json)
- [工具调用、结果形态与响应摘要哈希](calls.json)
- [JSON](report.json) / [HTML](report.html) / [Markdown](report.md)

```bash
python3 business-opportunity-skill/scripts/compose_fusion_report.py --enterprise '小米科技有限责任公司' --keyword-type name --output business-opportunity-skill/output/07-technology-growth/report.json --report-output business-opportunity-skill/output/07-technology-growth/report.html
```

## 逐场景业务复核

当前冻结产物逐项满足场景契约；结论仅限本轮公开数据和报告口径。

- **pass** 主体解析无歧义：通过：subject.enterprise=小米科技有限责任公司、resolved=True、resolve_reason=工商基础信息中的企业名称和统一社会信用代码已返回；工商章节字段数=11。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=小米科技有限责任公司，resolved=True；metrics[标讯记录总量=50；中标标的统计合计=9；当前招聘公开数=3726；近三月招聘公开数=3726；有效域名数=1427；舆情统计总量=5904；负面舆情统计=874]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/50)；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(9/9)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/53)；enterprise:enterprise_get_enterprise_main_person_info=data(5/5)]
- **pass** 增长动能引用经营和招聘证据：通过：招聘工具状态=data/data，招聘章节={"current": 3753, "last_3m": 3753, "avg_salary": 10073.5575539269, "welfare": []}；当前招聘公开数=3753、近三月招聘公开数=3753。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=小米科技有限责任公司，resolved=True；metrics[标讯记录总量=50；中标标的统计合计=9；当前招聘公开数=3726；近三月招聘公开数=3726；有效域名数=1427；舆情统计总量=5904；负面舆情统计=874]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/50)；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(9/9)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/53)；enterprise:enterprise_get_enterprise_main_person_info=data(5/5)]
- **pass** 云资产条目不被当作预算证明：通过：cloudmigration_cloud_assets=data，云资产字段数=10；有效域名数=1427；HTML/MD均呈现当前口径限制=True。；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=小米科技有限责任公司，resolved=True；metrics[标讯记录总量=50；中标标的统计合计=9；当前招聘公开数=3726；近三月招聘公开数=3726；有效域名数=1427；舆情统计总量=5904；负面舆情统计=874]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/50)；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(9/9)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/53)；enterprise:enterprise_get_enterprise_main_person_info=data(5/5)]
- **pass** 商机等级和证据强度匹配：通过：abstract=本报告对「小米科技有限责任公司」进行商机事实整理。报告仅列示可核验的采购、中标、经营、招聘、云资产和舆情事实，不生成商机分或成交概率。；评分指标=无对应指标；coverage=100%，insights=[{"feature": "中标业绩边界", "evidence": "中标标的统计项 5、标讯记录总量 50。", "interpretation": "仅说明供应方历史市场活动；采购侧统计为空，不能据此宣称该企业存在采购需求。"}, {"feature": "扩张活动交叉线索", "evidence": "经营趋势命中 6 项；当前招聘 3753、近三月招聘 3753。", "interpretation": "经营与招聘两个独立域同时出现活动信号；仅构成扩张观察，不能推定采购预算。"}, {"feature": "云资产触点", "evidence": "有效域名 1427，云服务器区间 1000台以上。", "interpretation": "说明存在可观测云资产触点；不能据此评价数字化成熟度、迁移意向或预算。"}, {"feature": "负面舆情；本轮当前产物：technical=passed，successful_data_calls=14；subject.enterprise=小米科技有限责任公司，resolved=True；metrics[标讯记录总量=50；中标标的统计合计=9；当前招聘公开数=3726；近三月招聘公开数=3726；有效域名数=1427；舆情统计总量=5904；负面舆情统计=874]；quality={'total_sections': 6, 'populated_sections': 6, 'empty_sections': 0, 'coverage_pct': 100}；非空章节=['主体与工商基础', '经营公开线索', '采购与中标事实（分列）', '舆情情感统计', '云资产与数字触点', '招聘公开线索']；代表记录=7；calls[cloudmigration:cloudmigration_cloud_assets=data；news:news_bigdata_news_stats=data；recruitment:recruitment_trend=data；recruitment:recruitment_employer_profile=data；bidding:bid_bigdata_procurement_stats=empty；bidding:bid_bigdata_bid_win_stats=data；bidding:bid_bigdata_bidding_info=data(20/50)；operation:operation_insight_business_scale=data；operation:operation_insight_financing_info=data；operation:operation_insight_company_trends=data；operation:operation_insight_enterprise_rankings=data(9/9)；enterprise:enterprise_get_enterprise_base_info=data；enterprise:enterprise_get_enterprise_holder_info=data；enterprise:enterprise_get_enterprise_invest_info=data(50/53)；enterprise:enterprise_get_enterprise_main_person_info=data(5/5)]

## 离线浏览器检查

[Ego Lite 离线图表、页面溢出和脚本检查](browser-check.json)