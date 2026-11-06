#!/usr/bin/env python3
"""Evidence-first business opportunity composition without synthetic scores."""

from __future__ import annotations
import datetime as dt
import json
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


_TREND_LABELS = {
    "isStaffExpandIn3Month": "近3月人员扩张",
    "isStaffExpandIn6Month": "近6月人员扩张",
    "isExpandNewCityIn3Month": "近3月新增城市",
    "isExpandNewCityIn6Month": "近6月新增城市",
    "isExpandNewCityIn12Month": "近12月新增城市",
    "isFoundSubsidiaryIn3Month": "近3月新增子公司",
    "isDiffAreaWinBidIn6Month": "近6月跨区域中标",
    "isDiffAreaWinBidIn12Month": "近12月跨区域中标",
}
_FIELD_LABELS = {
    "staff": "人员规模",
    "turnover": "年营业额",
    "financingAmount": "金额",
    "financingSeries": "轮次",
    "financingTime": "时间",
    "investorList": "投资方",
    "subjectMatter": "标的",
    "count": "数量",
    "percent": "占比",
    "area": "区域",
    "range": "金额区间",
    "year": "年份",
    "month": "月份",
    "negative": "负面",
    "neutral": "中立",
    "positive": "正面",
    "unknown": "未知",
    "rankingListName": "榜单",
    "rankingListYear": "年份",
    "rankingListInstitution": "发布机构",
    "rank": "排名",
}


_ORGANIZED_KEYS = {
    "operation": ("人员规模", "年营业额", "融资轮次", "融资记录", "经营趋势命中", "上榜记录"),
    "bidding": (
        "采购品类统计",
        "采购区域统计",
        "中标标的分布",
        "中标区域分布",
        "中标金额分布",
        "中标年度趋势",
        "招投标明细",
        "招投标记录总量",
    ),
    "news": ("情感分布", "月度情感趋势"),
    "cloudmigration": (
        "有效域名数",
        "子域名数",
        "云服务器区间",
        "云消费规模",
        "云服务商",
        "CDN服务商",
        "是否使用CDN",
        "是否使用IDC",
        "是否使用云存储",
        "是否有海外云",
    ),
    "recruitment": (
        "当前招聘公开数",
        "近三月招聘公开数",
        "平均薪酬（元/月）",
        "福利标签",
        "窗口口径",
    ),
}


def _num_text(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.2f}".rstrip("0").rstrip(".")
    return str(v)


def _one_line(value: Any) -> str:
    """Render upstream nested values as readable Chinese text.

    Every returned item is preserved; only JSON punctuation and English field
    keys are removed. Unknown keys stay verbatim so upstream fields remain
    traceable instead of being silently merged.
    """
    if isinstance(value, dict):
        if {"subjectMatter", "count"} <= set(value):
            pct = value.get("percent")
            pct_text = f"，占比 {_num_text(pct)}%" if pct is not None else ""
            return f"{value.get('subjectMatter')} {value.get('count')} 条{pct_text}"
        if {"area", "count"} <= set(value):
            return f"{value.get('area')} {value.get('count')} 条"
        if {"range", "count"} <= set(value):
            pct = value.get("percent")
            pct_text = f"，占比 {_num_text(pct)}%" if pct is not None else ""
            return f"{value.get('range')} {value.get('count')} 条{pct_text}"
        if {"year", "count"} <= set(value):
            return f"{value.get('year')} 年 {value.get('count')} 条"
        if {"month", "stats"} <= set(value):
            stats = value.get("stats") if isinstance(value.get("stats"), dict) else {}
            return (
                f"{value.get('month')} 负面 {stats.get('negative', 0)} / "
                f"正面 {stats.get('positive', 0)}"
            )
        if "financingTime" in value:
            investors = value.get("investorList") or []
            inv = f"（{'、'.join(str(x) for x in investors)}）" if investors else ""
            return (
                f"{value.get('financingTime')} {value.get('financingSeries') or '轮次未知'} "
                f"{value.get('financingAmount') or '金额未知'}{inv}"
            )
        if "rankingListName" in value:
            rank = value.get("rank")
            rank_text = (
                f"第 {rank} 位"
                if rank not in (None, "", "-")
                else "排名未返回"
            )
            return (
                f"{value.get('rankingListName')} {rank_text}"
                f"（{value.get('rankingListInstitution') or '机构未知'}，"
                f"{value.get('rankingListYear') or '年份未知'}）"
            )
        parts = []
        for key, item in value.items():
            if item in (None, "", "-", [], {}):
                continue
            parts.append(f"{_FIELD_LABELS.get(str(key), key)} {_one_line(item)}")
        return "；".join(parts)
    if isinstance(value, (list, tuple)):
        if all(not isinstance(x, (dict, list, tuple)) for x in value):
            return "、".join(_num_text(x) for x in value if x not in (None, "", "-"))
        return "；".join(_one_line(x) for x in value if x not in (None, "", "-"))
    return _num_text(value)


def _salary_text(value: Any) -> Optional[str]:
    try:
        return f"{float(str(value).replace(',', '')):.2f} 元/月"
    except (TypeError, ValueError):
        return None


def _clean_lines(lines: list[str]) -> str:
    return "；".join(line for line in lines if line)


def _trend_hits(trends: Any) -> List[str]:
    """Every upstream ``is*`` flag observed as 1, with its source field name.

    Known flags get their Chinese label plus the raw field/value evidence;
    unknown flags stay verbatim so they are neither dropped nor given an
    invented meaning.
    """
    if not isinstance(trends, dict):
        return []
    hits = []
    for key, value in trends.items():
        if not str(key).startswith("is") or str(value) != "1":
            continue
        label = _TREND_LABELS.get(str(key))
        if label:
            hits.append(f"{label}（{key}=1）")
        else:
            hits.append(f"{key}（上游趋势字段=1，未收录标准标签）")
    return hits


def _organized_core(core: Mapping[str, Any]) -> Dict[str, Any]:
    """Turn nested MCP payloads into reader-facing text, preserving every item."""
    out = dict(core)
    op = core.get("operation")
    if isinstance(op, dict) and not any(k in op for k in _ORGANIZED_KEYS["operation"]):
        scale = op.get("scale") if isinstance(op.get("scale"), dict) else {}
        trends = op.get("trends") if isinstance(op.get("trends"), dict) else {}
        organized = {
            "人员规模": scale.get("staff"),
            "年营业额": scale.get("turnover"),
            "融资轮次": op.get("financing_count"),
            "融资记录": _one_line(op.get("financing_list")),
            "经营趋势命中": "、".join(_trend_hits(trends)),
            "上榜记录": _one_line(op.get("rankings")),
        }
        out["operation"] = {k: v for k, v in organized.items() if v not in (None, "", "-", [], {})}
    bid = core.get("bidding")
    if isinstance(bid, dict) and not any(k in bid for k in _ORGANIZED_KEYS["bidding"]):
        organized = {
            "采购品类统计": _one_line(bid.get("procurement_products")),
            "采购区域统计": _one_line(bid.get("procurement_areas")),
            "中标标的分布": _one_line(bid.get("win_subjects")),
            "中标区域分布": _one_line(bid.get("win_areas")),
            "中标金额分布": _one_line(bid.get("win_amounts")),
            "中标年度趋势": _one_line(bid.get("win_trends")),
            "招投标明细": _one_line(bid.get("bidding_list")),
            "招投标记录总量": bid.get("bidding_total"),
        }
        out["bidding"] = {k: v for k, v in organized.items() if v not in (None, "", "-", [], {})}
    news = core.get("news")
    if isinstance(news, dict) and not any(k in news for k in _ORGANIZED_KEYS["news"]):
        organized = {
            "情感分布": _one_line(news.get("sentiment")),
            "月度情感趋势": _one_line(news.get("sentiment_trend")),
        }
        out["news"] = {k: v for k, v in organized.items() if v not in (None, "", "-", [], {})}
    cloud = core.get("cloudmigration")
    if isinstance(cloud, dict) and not any(
        k in cloud for k in _ORGANIZED_KEYS["cloudmigration"]
    ):
        def yes_no(value):
            if value in (None, "", "-"):
                return "未知"
            return "是" if str(value) == "1" else "否"
        organized = {
            "有效域名数": cloud.get("effective_domain_num"),
            "子域名数": cloud.get("sub_domain_num"),
            "云服务器区间": cloud.get("cloud_server_num"),
            "云消费规模": cloud.get("cloud_level"),
            "云服务商": _one_line(cloud.get("cloud_servers")),
            "CDN服务商": _one_line(cloud.get("cdn_servers")),
            "是否使用CDN": yes_no(cloud.get("has_cdn")),
            "是否使用IDC": yes_no(cloud.get("has_idc")),
            "是否使用云存储": yes_no(cloud.get("has_cloud_storage")),
            "是否有海外云": yes_no(cloud.get("has_overseas")),
        }
        out["cloudmigration"] = {
            k: v for k, v in organized.items() if v not in (None, "", "-", [], {})
        }
    rec = core.get("recruitment")
    if isinstance(rec, dict) and not any(
        k in rec for k in _ORGANIZED_KEYS["recruitment"]
    ):
        current = _int(rec.get("current"))
        last3 = _int(rec.get("last_3m"))
        welfare = rec.get("welfare") or []
        organized = {
            "当前招聘公开数": current,
            "近三月招聘公开数": last3,
            "平均薪酬（元/月）": _salary_text(rec.get("avg_salary")),
            "福利标签": _one_line(welfare) if welfare else None,
        }
        if current is not None and last3 is not None and current == last3:
            organized["窗口口径"] = (
                "上游当前值与近三月值相同，两个时间窗口不可区分；"
                "不能视为两次独立扩张信号"
            )
        out["recruitment"] = {
            k: v for k, v in organized.items() if v not in (None, "", "-", [], {})
        }
    return out


def _dedupe_recruitment_metrics(metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_label = {m.get("label"): m for m in metrics}
    cur = by_label.get("当前招聘公开数")
    last3 = by_label.get("近三月招聘公开数")
    if not (cur and last3 and cur.get("value") == last3.get("value")):
        return metrics
    cur["hint"] = (
        "当前在招公开数；上游近三月字段返回同值，两个窗口不可区分，"
        "不作为独立扩张证据"
    )
    return [m for m in metrics if m is not last3]


def _quality_nonempty(value: Any) -> bool:
    """0/False are real values; only None/''/[]/{} count as empty."""
    if value is None or value == "":
        return False
    if isinstance(value, dict):
        return any(_quality_nonempty(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(_quality_nonempty(v) for v in value)
    return True


def _refresh_quality_report(report: Dict[str, Any]) -> None:
    data_source = report.get("data_source")
    core = report.get("core_analysis")
    if not isinstance(data_source, dict) or not isinstance(core, dict):
        return
    sections = core.get("sections")
    if not isinstance(sections, list):
        return
    declared = [s for s in sections if isinstance(s, dict)]
    populated = sum(
        1 for section in declared if _quality_nonempty(core.get(section.get("key")))
    )
    quality = data_source.get("quality_report")
    if not isinstance(quality, dict):
        quality = {}
    # The composer declares every section it attempted before empty bodies are
    # dropped. Keep that declared total so a review pass cannot turn missing
    # dimensions into a false 100% coverage; grow it only when a section was
    # added, and fall back to the current count for foreign payloads.
    try:
        previous_total = int(quality.get("total_sections") or 0)
    except (TypeError, ValueError):
        previous_total = 0
    total = max(len(declared), populated, previous_total)
    quality["total_sections"] = total
    quality["populated_sections"] = populated
    quality["empty_sections"] = max(0, total - populated)
    quality["coverage_pct"] = round(populated / total * 100) if total else 0
    data_source["quality_report"] = quality


def apply_content_review(
    report: Mapping[str, Any], calls: Any = None
) -> Dict[str, Any]:
    """Offline content normalization for an existing business-opportunity report.

    Only rewrites values already present in the frozen report; it never calls
    MCP or adds new facts.
    """
    reviewed = json.loads(json.dumps(report, ensure_ascii=False))
    core = reviewed.get("core_analysis")
    if isinstance(core, dict):
        sections = core.get("sections")
        organized = _organized_core({k: v for k, v in core.items() if k != "sections"})
        if isinstance(sections, list):
            organized["sections"] = sections
        reviewed["core_analysis"] = organized
    if isinstance(reviewed.get("metrics"), list):
        reviewed["metrics"] = _dedupe_recruitment_metrics(reviewed["metrics"])
        if isinstance(reviewed.get("representative_records"), list):
            reviewed["representative_records"] = [
                row
                for row in reviewed["representative_records"]
                if row.get("维度") != "近三月招聘公开数"
            ]
    cur = next(
        (m for m in reviewed.get("metrics") or [] if m.get("label") == "当前招聘公开数"),
        None,
    )
    if cur:
        value = str(cur.get("value"))
        for insight in reviewed.get("insights") or []:
            evidence = str(insight.get("evidence") or "")
            duplicate = f"当前招聘 {value}、近三月招聘 {value}"
            if duplicate in evidence:
                insight["evidence"] = evidence.replace(
                    duplicate,
                    f"当前招聘 {value}（近三月字段同值，窗口不可区分）",
                )
                old_interp = str(insight.get("interpretation") or "")
                insight["interpretation"] = (
                    "经营趋势与招聘两个独立来源均有公开活动；"
                    "招聘当前值与近三月值相同，不能视为两次独立信号；"
                    "仅构成扩张观察，不能推定采购预算。"
                )
                if isinstance(reviewed.get("executive_summary"), list):
                    reviewed["executive_summary"] = [
                        str(item).replace(old_interp, insight["interpretation"])
                        for item in reviewed["executive_summary"]
                    ]
    caliber = reviewed.get("caliber")
    if isinstance(caliber, dict):
        note = "字段已整理为中文可读文本，数值逐项保留，未新增推断。"
        if note not in str(caliber.get("limit") or ""):
            caliber["limit"] = str(caliber.get("limit") or "") + note
    _refresh_quality_report(reviewed)
    return reviewed


def build_direct_payload(
    enterprise: str, keyword_type: str, *, dry_run: bool, skills_root: str,
    max_pages: Optional[int] = None, calls: Any = None,
) -> Dict[str, Any]:
    data = orch.collect_direct(
        enterprise, keyword_type, dry_run=dry_run, skills_root=skills_root,
        detail_max_pages=max_pages,
    )
    meta = data.get("_meta") or {}
    evidence = calls
    if evidence is None:
        evidence = data.get("calls")
    if evidence is None:
        evidence = meta.get("calls")
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
    return apply_content_review(report, evidence)
