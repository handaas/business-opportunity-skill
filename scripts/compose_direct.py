#!/usr/bin/env python3
"""Evidence-first business opportunity composition without synthetic scores."""

from __future__ import annotations
import datetime as dt
from typing import Any, Dict, List, Mapping, Optional
import mcp_orchestration as orch

REPORT_TYPE = "business_opportunity_direct"
BANNER = "企业商机事实与线索报告"
SERVERS = [
    "enterprise-mcp-server",
    "enterprise-operation-mcp-server",
    "bidding-mcp-server",
    "news-mcp-server",
    "cloudmigration-mcp-server",
    "recruitment-mcp-server",
]
PRODUCTS = [
    "企业基础信息",
    "经营动态",
    "采购与中标统计",
    "舆情统计",
    "云资产线索",
    "招聘公开线索",
]
DOMAINS = [
    ("enterprise", "主体与工商基础"),
    ("operation", "经营公开线索"),
    ("bidding", "采购与中标事实"),
    ("news", "舆情统计"),
    ("cloudmigration", "云资产触点"),
    ("recruitment", "招聘公开线索"),
]


def _effective(v: Any) -> bool:
    if v in (None, "", "-", [], {}):
        return False
    if isinstance(v, dict):
        return any(_effective(x) for x in v.values())
    if isinstance(v, list):
        return any(_effective(x) for x in v)
    return True


def _int(v: Any):
    try:
        return int(float(str(v).replace(",", "")))
    except (TypeError, ValueError):
        return None


def _base(data: Mapping[str, Any]) -> Dict[str, Any]:
    ent = data.get("enterprise") or {}
    return dict(ent.get("base") or data.get("base") or {})


def _identity(data: Mapping[str, Any], requested: str) -> tuple[str, bool, str]:
    meta = data.get("_meta") or {}
    resolved = meta.get("resolved") or {}
    canon = str(resolved.get("enterprise") or requested).strip()
    base = _base(data)
    name = str(base.get("企业名称") or base.get("name") or "").strip()
    code = str(
        base.get("统一社会信用代码") or base.get("socialCreditCode") or ""
    ).strip()
    confirmed = (
        name not in ("", "-")
        and (name == canon or name == requested)
        and code not in ("", "-")
    )
    reason = (
        "工商基础信息中的企业名称和统一社会信用代码已返回"
        if confirmed
        else "工商基础信息未返回可核验企业名称及统一社会信用代码"
    )
    return (name if confirmed else canon), confirmed, reason


def _section(
    sections: List[Dict[str, Any]],
    core: Dict[str, Any],
    key: str,
    title: str,
    body: Any,
) -> None:
    if _effective(body):
        sections.append({"key": key, "title": title, "kind": "kv"})
        core[key] = body


def build_direct_payload(
    enterprise: str, keyword_type: str, *, dry_run: bool, skills_root: str,
    max_pages: Optional[int] = None,
) -> Dict[str, Any]:
    data = orch.collect_direct(
        enterprise, keyword_type, dry_run=dry_run, skills_root=skills_root,
        detail_max_pages=max_pages,
    )
    meta = data.get("_meta") or {}
    errors = meta.get("errors") or {}
    canon, confirmed, reason = _identity(data, enterprise)
    sections: List[Dict[str, Any]] = []
    core: Dict[str, Any] = {}
    for key, title in (
        ("enterprise", "主体与工商基础"),
        ("operation", "经营公开线索"),
        ("bidding", "采购与中标事实（分列）"),
        ("news", "舆情情感统计"),
        ("cloudmigration", "云资产与数字触点"),
        ("recruitment", "招聘公开线索"),
    ):
        _section(
            sections,
            core,
            key,
            title,
            _base(data) if key == "enterprise" else data.get(key),
        )
    bidding = data.get("bidding") or {}
    news = data.get("news") or {}
    cloud = data.get("cloudmigration") or {}
    rec = data.get("recruitment") or {}
    op = data.get("operation") or {}
    metrics = []
    records = []
    insights = []
    procurement = list(bidding.get("procurement_products") or [])
    procurement_areas = list(bidding.get("procurement_areas") or [])
    wins = list(bidding.get("win_subjects") or [])
    bid_total = _int(bidding.get("bidding_total"))
    if procurement:
        metrics.append(
            {
                "label": "采购品类统计项",
                "value": str(len(procurement)),
                "hint": "采购侧统计项；不代表当前采购意向",
            }
        )
    if procurement_areas:
        metrics.append(
            {
                "label": "采购区域统计项",
                "value": str(len(procurement_areas)),
                "hint": "采购侧区域统计项",
            }
        )
    if bid_total is not None:
        metrics.append(
            {
                "label": "标讯记录总量",
                "value": str(bid_total),
                "hint": "含投标/中标公开记录，不等同采购需求",
            }
        )
    if wins:
        win_count = sum(_int(x.get("count")) or 0 for x in wins if isinstance(x, dict))
        metrics.append(
            {
                "label": "中标标的统计合计",
                "value": str(win_count),
                "hint": "供应方历史中标分布，不能替代买方采购意向",
            }
        )
    current = _int(rec.get("current"))
    last3 = _int(rec.get("last_3m"))
    if current is not None:
        metrics.append(
            {
                "label": "当前招聘公开数",
                "value": str(current),
                "hint": "招聘活跃线索，不代表采购计划",
            }
        )
    if last3 is not None:
        metrics.append(
            {
                "label": "近三月招聘公开数",
                "value": str(last3),
                "hint": "招聘接口口径，需结合采集时点",
            }
        )
    domains = _int(cloud.get("effective_domain_num"))
    if domains is not None:
        metrics.append(
            {
                "label": "有效域名数",
                "value": str(domains),
                "hint": "云资产触点，不代表数字化成熟度或预算",
            }
        )
    sentiment = news.get("sentiment") or {}
    negative = _int(sentiment.get("negative"))
    total = sum(
        _int(sentiment.get(k)) or 0
        for k in ("negative", "neutral", "positive", "unknown")
    )
    if total:
        metrics.append(
            {"label": "舆情统计总量", "value": str(total), "hint": "接口情感分类合计"}
        )
    if negative is not None:
        metrics.append(
            {
                "label": "负面舆情统计",
                "value": str(negative),
                "hint": "舆情风险线索，不作法律定性",
            }
        )
    if procurement or procurement_areas:
        insights.append(
            {
                "feature": "采购侧公开线索",
                "evidence": f"采购品类统计项 {len(procurement)}、区域统计项 {len(procurement_areas)}。",
                "interpretation": "可作为采购研究入口；统计未提供当前预算、采购计划或截至日，必须人工核验。",
            }
        )
    elif wins or bid_total:
        insights.append(
            {
                "feature": "中标业绩边界",
                "evidence": f"中标标的统计项 {len(wins)}、标讯记录总量 {bid_total if bid_total is not None else '未知'}。",
                "interpretation": "仅说明供应方历史市场活动；采购侧统计为空，不能据此宣称该企业存在采购需求。",
            }
        )
    trends = op.get("trends") or {}
    trend_names = (
        [k for k, v in trends.items() if str(k).startswith("is") and str(v) == "1"]
        if isinstance(trends, dict)
        else []
    )
    if trend_names and (current is not None or last3 is not None):
        insights.append(
            {
                "feature": "扩张活动交叉线索",
                "evidence": f"经营趋势命中 {len(trend_names)} 项；当前招聘 {current if current is not None else '未知'}、近三月招聘 {last3 if last3 is not None else '未知'}。",
                "interpretation": "经营与招聘两个独立域同时出现活动信号；仅构成扩张观察，不能推定采购预算。",
            }
        )
    if _effective(cloud):
        insights.append(
            {
                "feature": "云资产触点",
                "evidence": f"有效域名 {domains if domains is not None else '未知'}，云服务器区间 {cloud.get('cloud_server_num') or '未知'}。",
                "interpretation": "说明存在可观测云资产触点；不能据此评价数字化成熟度、迁移意向或预算。",
            }
        )
    if negative is not None and negative > 0:
        insights.append(
            {
                "feature": "负面舆情提示",
                "evidence": f"情感统计中负面 {negative} 条，总量 {total} 条。",
                "interpretation": "应人工复核负面样本、时间和相关性；本报告未查询司法/合规风险，不作信用或法律结论。",
            }
        )
    for m in metrics[:8]:
        records.append({"维度": m["label"], "关键记录": f"{m['value']}（{m['hint']}）"})
    missing = [
        title
        for key, title in DOMAINS
        if not _effective(_base(data) if key == "enterprise" else data.get(key))
    ]
    if not confirmed:
        missing.insert(0, "主体工商确认")
    missing.append("司法与合规风险（本 skill 未查询）")
    verdict = {
        "level": "线索观察" if confirmed else "数据不足",
        "recommendation": "进入人工核验" if confirmed else "先确认主体",
        "summary": (
            "报告仅列示可核验的采购、中标、经营、招聘、云资产和舆情事实，不生成商机分或成交概率。"
            if confirmed
            else "主体未通过工商名称和统一社会信用代码确认，不形成商机判断。"
        ),
        "blockers": [],
        "key_concerns": ([f"负面舆情统计 {negative} 条"] if negative else [])
        + [f"缺口：{x}" for x in missing],
        "specialty_average": None,
    }
    total_sections = len(DOMAINS)
    populated = len(sections)
    abstract = f"本报告对「{canon}」进行商机事实整理。" + str(verdict["summary"])
    report = {
        "report_type": REPORT_TYPE,
        "title": f"{canon} 企业商机线索报告",
        "banner": BANNER,
        "subject": {
            "enterprise": canon,
            "match_raw": enterprise,
            "keywordType": keyword_type,
            "resolved": confirmed,
            "resolve_reason": reason,
        },
        "abstract": abstract,
        "summary": abstract,
        "executive_summary": [verdict["summary"]]
        + [x["interpretation"] for x in insights[:4]],
        "verdict": verdict,
        "specialty_scores": {"items": [], "average": None, "rating_eligible": False},
        "metrics": metrics,
        "caliber": {
            "match_target": canon,
            "match_type": "单企业商机事实观察（不评分）",
            "data_scope": f"有效覆盖 {populated}/{total_sections} 个主题域；生成时间 {dt.datetime.now().astimezone().isoformat(timespec='seconds')}",
            "products": PRODUCTS,
            "limit": "缺口："
            + "；".join(missing)
            + "。中标业绩不等同采购需求，招聘和云资产不等同预算；司法与合规风险未评估。",
        },
        "core_analysis": {**core, "sections": sections},
        "representative_records": records,
        "insights": insights,
        "data_source": {
            "mcp_server": f"{len(SERVERS)} MCP",
            "mcp_servers": SERVERS,
            "mode": "live_mcp" if meta.get("source") == "live" else "cached_reports",
            "dry_run": dry_run,
            "generated_at": dt.datetime.now()
            .astimezone()
            .isoformat(timespec="seconds"),
            "quality_report": {
                "total_sections": total_sections,
                "populated_sections": populated,
                "empty_sections": total_sections - populated,
                "coverage_pct": round(populated / total_sections * 100),
            },
            "tool_errors": list(errors),
            "products": [{"name": p} for p in PRODUCTS],
        },
    }
    if meta.get("source") == "live":
        from common import attach_pagination

        report = attach_pagination(report, meta.get("pagination_payloads") or {})
        call_usage = meta.get("call_usage")
        if isinstance(call_usage, dict) and call_usage:
            report["data_source"]["call_usage"] = call_usage
        if max_pages is None:
            budget_note = (
                "明细接口默认按单页预算采集（每接口仅请求第 1 页，该页同时用于分析与上游 total 发现，不重复计费）；"
                "如需更多明细页，请先规划所需结论与数据维度，再用 --max-pages N 明确页数预算；"
                "若预算不足以支撑关键结论，必须说明证据缺口与预计所需额外页数，不得悄悄降级结论或扩大计费范围。"
            )
            report["abstract"] += budget_note
            report["summary"] += budget_note
            report["caliber"]["limit"] += budget_note
        for note in (meta.get("schema_limited") or {}).values():
            report["abstract"] += note
            report["summary"] += note
            report["caliber"]["limit"] += note
    return report
