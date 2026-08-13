#!/usr/bin/env python3
"""Business-opportunity MCP orchestration: tool plan + multi-source collection + normalization.

Selects high-value tools across 6 MCP servers, tuned for sales lead evaluation:

  enterprise     : base_info / holders / investments / key persons
  operation      : business-scale / financing / company-trends / rankings
  bidding        : procurement_stats / bid_win_stats / bidding_info
  news           : news_stats (sentiment distribution / trend)
  cloudmigration : cloud_assets (cloud assets / domains / spending)
  recruitment    : trend / employer-profile (expansion signals)

Two collection modes:
  * live  — connect to the 6 MCP servers via MultiMcpClient (richest data)
  * cache — read pre-existing atomic report JSONs (reports_探迹/) for dry-run

Both normalize into the SAME unified structure consumed by cross_analysis.
"""
from __future__ import annotations

import asyncio
import json
import pathlib
from typing import Any, Dict, List, Mapping, Optional

from multi_mcp_client import MultiMcpClient, MultiMcpError

# --------------------------------------------------------------------------- #
# Generic extractors
# --------------------------------------------------------------------------- #

def _is_api_error(value: Any) -> bool:
    """Detect MCP API error responses (not empty data, but actual failures like 405)."""
    if value is None:
        return False
    if isinstance(value, str):
        return any(s in value for s in ("接口调用失败", "查询失败", "状态码：4", "状态码：5"))
    if isinstance(value, dict):
        # Check all string values for error indicators
        for v in value.values():
            if isinstance(v, str) and any(s in v for s in ("接口调用失败", "查询失败", "状态码：4", "状态码：5")):
                return True
    return False

def _first_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        if _is_api_error(value):
            return []
        for key in ("resultList", "list", "items", "data", "holderList", "stockHolderList", "fpFinancingList",
                    "purchasingProductStatList", "winbidStatList", "tenderStatList", "winbidAreaStat",
                    "purchasingAreaStatList", "tenderAreaStatList", "winbidAmountStatList", "tenderAmountStatList",
                    "sentimentLabelList", "effectiveSubDomainList", "subDomainList", "cloudServerList",
                    "cdnServerList", "recruitingWelfareList", "welfareList"):
            if isinstance(value.get(key), list):
                return value[key]
    if value in (None, "", {}):
        return []
    return [value]


def _safe_total(value: Any) -> Optional[int]:
    if isinstance(value, dict):
        if _is_api_error(value):
            return None
        t = value.get("total")
        try:
            return int(t) if t is not None else None
        except (TypeError, ValueError):
            return None
    return None


def _text(value: Any, limit: int = 0) -> str:
    if value is None:
        return ""
    t = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
    t = " ".join(t.split())
    return (t[: limit - 1].rstrip() + "…") if (limit and len(t) > limit) else t


def _int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _float(value: Any) -> Optional[float]:
    try:
        return float(str(value).replace(",", "").replace("万", "").replace("亿", ""))
    except (TypeError, ValueError):
        return None


def _amount(value: Any) -> str:
    """Parse a HandaaS amount field into readable text.

    Accepts: {"coinType":"人民币","value":2e9} | 20000 | "100万" | "人民币 100万"
    """
    if value in (None, "", "-"):
        return "-"
    if isinstance(value, dict):
        val = value.get("value")
        coin = value.get("coinType") or value.get("currency") or ""
        if val is None:
            return "-"
        try:
            fv = float(val)
        except (TypeError, ValueError):
            return f"{coin} {val}".strip()
        if fv >= 1e8:
            return f"{coin} {fv / 1e8:.2f}亿".strip()
        if fv >= 1e4:
            return f"{coin} {fv / 1e4:.0f}万".strip()
        return f"{coin} {fv:.0f}".strip()
    return str(value)


def _industry_text(value: Any) -> str:
    """Flatten a nested industry dict into '一级/二级/三级' text."""
    if not isinstance(value, dict):
        return str(value) if value else "-"
    parts = []
    for k in ("firstIndustry", "secondIndustry", "thirdIndustry", "fourthIndustry"):
        v = value.get(k)
        if v and str(v) not in parts:
            parts.append(str(v))
    return " / ".join(parts) if parts else "-"


def _amount_num(value: Any) -> Optional[float]:
    """Extract the numeric value from a HandaaS amount field."""
    if isinstance(value, dict):
        return _float(value.get("value"))
    return _float(value)


def _kv_addr(value: Any) -> str:
    """Extract address string from a nested addressValue dict."""
    if isinstance(value, dict):
        return str(value.get("value") or value.get("address") or "-")
    return str(value) if value else ""


# --------------------------------------------------------------------------- #
# Live collection: MCP tool plan
# --------------------------------------------------------------------------- #
def build_mcp_calls(enterprise: str, keyword_type: str) -> List[tuple[str, str, str, Dict[str, Any]]]:
    """Return [(key, domain, tool, args), ...] for all business-opportunity tools."""
    ent_kw: Dict[str, Any] = {"keyword": enterprise}
    mk_kw: Dict[str, Any] = {"matchKeyword": enterprise, "keywordType": keyword_type}
    return [
        # --- enterprise (工商) ---
        ("ent_base", "enterprise", "enterprise_get_enterprise_base_info", ent_kw),
        ("ent_holder", "enterprise", "enterprise_get_enterprise_holder_info", ent_kw),
        ("ent_invest", "enterprise", "enterprise_get_enterprise_invest_info", ent_kw),
        ("ent_person", "enterprise", "enterprise_get_enterprise_main_person_info", ent_kw),
        # --- operation (经营) ---
        ("op_scale", "operation", "operation_insight_business_scale", mk_kw),
        ("op_financing", "operation", "operation_insight_financing_info", mk_kw),
        ("op_trends", "operation", "operation_insight_company_trends", mk_kw),
        ("op_rankings", "operation", "operation_insight_enterprise_rankings", {**mk_kw, "pageSize": 10}),
        # --- bidding (招投标) ---
        ("bid_procurement", "bidding", "bid_bigdata_procurement_stats", mk_kw),
        ("bid_win_stats", "bidding", "bid_bigdata_bid_win_stats", mk_kw),
        ("bid_info", "bidding", "bid_bigdata_bidding_info", {**mk_kw, "pageSize": 20}),
        # --- news (舆情) ---
        ("news_stats", "news", "news_bigdata_news_stats", mk_kw),
        # --- cloudmigration (上云) ---
        ("cloud_assets", "cloudmigration", "cloudmigration_cloud_assets", mk_kw),
        # --- recruitment (招聘) ---
        ("rec_trend", "recruitment", "recruitment_trend", mk_kw),
        ("rec_profile", "recruitment", "recruitment_employer_profile", mk_kw),
    ]


_ENTERPRISE_SUFFIXES = ("公司", "集团", "有限", "院", "厂", "中心", "事务所", "合作社", "合伙")


def is_full_name(raw: str) -> bool:
    return any(s in (raw or "") for s in _ENTERPRISE_SUFFIXES)


async def resolve_enterprise(client: MultiMcpClient, keyword: str) -> Dict[str, Any]:
    """Resolve a keyword to a canonical enterprise name via enterprise MCP fuzzy search."""
    keyword = (keyword or "").strip()
    if not keyword:
        return {"keyword": "", "enterprise": "", "resolved": False}
    if is_full_name(keyword):
        return {"keyword": keyword, "enterprise": keyword, "resolved": True, "reason": "视为企业全称"}
    fuzzy = await client.call(
        "enterprise", "enterprise_get_keyword_search", {"matchKeyword": keyword, "pageSize": 1}
    )
    for rec in _first_list(fuzzy):
        if isinstance(rec, dict):
            name = str(rec.get("name") or "").strip()
            if name:
                return {"keyword": keyword, "enterprise": name, "resolved": True, "reason": "关键词模糊查询补全"}
    return {"keyword": keyword, "enterprise": keyword, "resolved": False, "reason": "模糊查询未命中，按关键词直查"}


async def _collect_live(enterprise: str, keyword_type: str) -> Dict[str, Any]:
    """Connect to 6 MCP servers, resolve name, fan out all tool calls."""
    async with MultiMcpClient() as client:
        resolved = await resolve_enterprise(client, enterprise)
        canon = resolved["enterprise"] or enterprise
        calls = build_mcp_calls(canon, keyword_type)
        raw = await client.call_many(calls)
    raw["_resolved"] = resolved
    return normalize_mcp(raw)


# --------------------------------------------------------------------------- #
# Cache collection: read pre-existing atomic report JSONs (dry-run)
# --------------------------------------------------------------------------- #
def _metric_value(report: Mapping[str, Any], label: str) -> Optional[str]:
    for m in report.get("metrics", []):
        if isinstance(m, dict) and label in str(m.get("label", "")):
            return str(m.get("value", ""))
    return None


def _metric_int(report: Mapping[str, Any], label: str) -> Optional[int]:
    v = _metric_value(report, label)
    return _int(v.replace(",", "").replace("万", "").replace("%", "")) if v else None


def _collect_cache(skills_root: str, enterprise: str) -> Dict[str, Any]:
    """Load atomic report JSONs from reports_探迹/ and normalize."""
    root = pathlib.Path(skills_root)
    reports_dir = root / "reports_探迹"
    if not reports_dir.exists():
        # fall back to each atomic skill's output/ sample
        return normalize_reports({}, enterprise, resolved=False)
    reports: Dict[str, Any] = {}
    for p in sorted(reports_dir.glob("*.json")):
        try:
            reports[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return normalize_reports(reports, enterprise)


# --------------------------------------------------------------------------- #
# Normalization — both modes produce THIS structure
# --------------------------------------------------------------------------- #
def normalize_mcp(raw: Mapping[str, Any]) -> Dict[str, Any]:
    """Normalize live MCP results into the unified cross-analysis structure."""
    resolved = raw.get("_resolved") or {}
    errors = {k: v["_error"] for k, v in raw.items() if isinstance(v, dict) and "_error" in v}

    # --- enterprise ---
    base_raw = raw.get("ent_base") or {}
    bi = base_raw.get("base_info") if isinstance(base_raw, dict) else {}
    if not isinstance(bi, dict):
        bi = {}
    base = {
        "企业名称": bi.get("name") or "-",
        "统一社会信用代码": bi.get("socialCreditCode") or bi.get("orgCode") or "-",
        "法定代表人": bi.get("legalRepresentative") or "-",
        "企业类型": bi.get("enterpriseType") or "-",
        "行业": _industry_text(bi.get("industry")),
        "注册资本": _amount(bi.get("regCapital")),
        "实缴资本": _amount(bi.get("realCapital") or bi.get("payAmountCount")),
        "成立日期": str(bi.get("foundTime") or "-"),
        "经营状态": bi.get("operStatus") or "-",
        "注册地址": bi.get("address") or _kv_addr(bi.get("addressValue")) or "-",
        "经营范围": _text(bi.get("business") or bi.get("businessScope"), limit=400) or "-",
    }
    # 实缴率：若实缴与注册资本都可量化则计算
    reg_v = _amount_num(bi.get("regCapital"))
    paid_v = _amount_num(bi.get("realCapital") or bi.get("payAmountCount"))
    if reg_v and paid_v is not None and reg_v > 0:
        base["资本实缴率"] = f"{paid_v / reg_v * 100:.1f}%"
    holders = _first_list(raw.get("ent_holder"))
    investments = _first_list(raw.get("ent_invest"))
    investments_total = _safe_total(raw.get("ent_invest")) or len(investments)
    persons = _first_list(raw.get("ent_person"))

    # --- operation ---
    os_ = raw.get("op_scale") or {}
    of = raw.get("op_financing") or {}
    ot = raw.get("op_trends") or {}
    operation = {
        "scale": {
            "staff": os_.get("enterpriseScale") if isinstance(os_, dict) else None,
            "turnover": os_.get("annualTurnover") if isinstance(os_, dict) else None,
        },
        "financing_count": _int(of.get("fpFinancingCount")) if isinstance(of, dict) else None,
        "financing_list": _first_list(of.get("fpFinancingList")) if isinstance(of, dict) else [],
        "trends": ot if isinstance(ot, dict) else {},
        "rankings": _first_list(raw.get("op_rankings")),
    }

    # --- bidding (招投标) ---
    bp = raw.get("bid_procurement") or {}
    bw = raw.get("bid_win_stats") or {}
    bi_list = _first_list(raw.get("bid_info"))
    # filter "查询数据为空"
    if isinstance(bp, dict) and bp.get("text") == "查询数据为空":
        procurement = {}
        bidding_list = []
    else:
        procurement = bp if isinstance(bp, dict) else {}
        bidding_list = [b for b in bi_list if isinstance(b, dict) and b.get("text") != "查询数据为空"]
    # 中标统计
    win_stats = bw if isinstance(bw, dict) else {}

    bidding = {
        "procurement_products": _first_list(procurement.get("purchasingProductStatList")),
        "procurement_areas": _first_list(procurement.get("purchasingAreaStatList")),
        "win_subjects": _first_list(win_stats.get("winbidStatList")),
        "win_areas": _first_list(win_stats.get("winbidAreaStat")),
        "win_amounts": _first_list(win_stats.get("winbidAmountStatList")),
        "win_trends": _first_list(win_stats.get("winbidTrend")),
        "bidding_list": bidding_list,
        "bidding_total": _safe_total(raw.get("bid_info")) or len(bidding_list),
    }

    # --- news (舆情) ---
    ns = raw.get("news_stats") or {}
    if isinstance(ns, dict) and ns.get("text") == "查询数据为空":
        sentiment = {}
        sentiment_trend = []
    else:
        sentiment = ns.get("newsSentimentStats") if isinstance(ns, dict) else {}
        sentiment_trend = _first_list(ns.get("newsSentimentTrend")) if isinstance(ns, dict) else []

    news = {
        "sentiment": sentiment if isinstance(sentiment, dict) else {},
        "sentiment_trend": sentiment_trend,
    }

    # --- cloudmigration (上云) ---
    ca = raw.get("cloud_assets") or {}
    if isinstance(ca, dict) and ca.get("text") == "查询数据为空":
        cloud_assets = {}
    else:
        cloud_assets = ca if isinstance(ca, dict) else {}

    cloudmigration = {
        "effective_domain_num": _int(cloud_assets.get("effectiveSubDomainNum")),
        "sub_domain_num": _int(cloud_assets.get("subDomainNum")),
        "cloud_server_num": cloud_assets.get("cloudServerNumInterval"),
        "cloud_level": cloud_assets.get("cloudConsumptionScale"),
        "cloud_servers": _first_list(cloud_assets.get("cloudServerList")),
        "has_cdn": cloud_assets.get("hasCdn"),
        "has_idc": cloud_assets.get("hasIDC"),
        "has_cloud_storage": cloud_assets.get("hasCloudStorage"),
        "has_overseas": cloud_assets.get("hasOverseasCloudService"),
        "cdn_servers": _first_list(cloud_assets.get("cdnServerList")),
    }

    # --- recruitment ---
    rt = raw.get("rec_trend") or {}
    rp = raw.get("rec_profile") or {}
    recruitment = {
        "current": _int(rt.get("recruitingCurrentCount")) if isinstance(rt, dict) else None,
        "last_3m": _int(rt.get("recruitingLastThreeMonthCount")) if isinstance(rt, dict) else None,
        "avg_salary": rt.get("recruitingAvgWorkingSalary") if isinstance(rt, dict) else None,
        "welfare": _first_list(rp.get("recruitingWelfareList") or rp.get("welfareList")) if isinstance(rp, dict) else [],
    }

    return _wrap(resolved, errors, "live", enterprise=resolved.get("enterprise", ""),
                 base=base, holders=holders, investments=investments, persons=persons,
                 operation=operation, bidding=bidding, news=news, cloudmigration=cloudmigration,
                 recruitment=recruitment)


def normalize_reports(reports: Mapping[str, Any], enterprise: str, *, resolved: bool = True) -> Dict[str, Any]:
    """Normalize cached atomic report JSONs into the unified structure (dry-run)."""
    er = reports.get("enterprise-report", {}) if isinstance(reports, dict) else {}
    opr = reports.get("enterprise-operation-report", {}) if isinstance(reports, dict) else {}
    br = reports.get("bidding-report", {}) if isinstance(reports, dict) else {}
    nr = reports.get("news-report", {}) if isinstance(reports, dict) else {}
    cr = reports.get("cloudmigration-report", {}) if isinstance(reports, dict) else {}
    recr = reports.get("recruitment-report", {}) if isinstance(reports, dict) else {}

    def _ca(report: Mapping[str, Any]) -> Mapping[str, Any]:
        return report.get("core_analysis", {}) if isinstance(report, dict) else {}

    # enterprise
    ec = _ca(er)
    base = _kv_to_dict(ec.get("enterprise_base")) if isinstance(ec.get("enterprise_base"), list) else (ec.get("enterprise_base") or {})
    # 补充 metrics 里的资本充实性字段
    for mlabel, bkey in [("资本实缴率", "资本实缴率"), ("注册资本", "注册资本"), ("实缴资本", "实缴资本")]:
        mv = _metric_value(er, mlabel)
        if mv and not base.get(bkey):
            base[bkey] = mv
    holders = ec.get("holders") or []
    investments = ec.get("investments") or []
    persons = ec.get("key_persons") or []

    # operation
    opc = _ca(opr)
    operation = {
        "scale": _kv_to_dict(opc.get("business_scale")),
        "financing_count": _metric_int(opr, "融资次数"),
        "financing_list": opc.get("financing_info") or [],
        "trends": _kv_to_dict(opc.get("company_trends")),
        "rankings": opc.get("enterprise_rankings") or [],
    }

    # bidding (缓存模式尝试从 bidding-report 读取)
    bc = _ca(br)
    bidding = {
        "procurement_products": bc.get("procurement_products") or [],
        "procurement_areas": bc.get("procurement_areas") or [],
        "win_subjects": bc.get("win_subjects") or [],
        "win_areas": bc.get("win_areas") or [],
        "win_amounts": bc.get("win_amounts") or [],
        "win_trends": bc.get("win_trends") or [],
        "bidding_list": bc.get("bidding_list") or [],
        "bidding_total": _metric_int(br, "招投标参与数"),
    }

    # news (缓存模式尝试从 news-report 读取)
    nc = _ca(nr)
    news = {
        "sentiment": _kv_to_dict(nc.get("sentiment_stats")),
        "sentiment_trend": nc.get("sentiment_trend") or [],
    }

    # cloudmigration (缓存模式尝试从 cloudmigration-report 读取)
    cc = _ca(cr)
    cloudmigration = {
        "effective_domain_num": _metric_int(cr, "有效域名数"),
        "sub_domain_num": _metric_int(cr, "子域名数"),
        "cloud_server_num": _pick(cc, "云用量", "cloudServerNumInterval"),
        "cloud_level": _pick(cc, "上云资产等级", "cloudConsumptionScale"),
        "cloud_servers": cc.get("cloud_servers") or [],
        "has_cdn": _pick(cc, "是否有CDN", "hasCdn"),
        "has_idc": _pick(cc, "是否有IDC", "hasIDC"),
        "has_cloud_storage": _pick(cc, "是否有云存储", "hasCloudStorage"),
        "has_overseas": _pick(cc, "是否有海外云服务", "hasOverseasCloudService"),
        "cdn_servers": cc.get("cdn_servers") or [],
    }

    # recruitment
    recc = _ca(recr)
    recruitment = {
        "current": _metric_int(recr, "当前招聘人数"),
        "last_3m": _metric_int(recr, "近三月招聘人数"),
        "avg_salary": _metric_value(recr, "平均薪酬"),
        "welfare": recc.get("benefit_tags") or [],
    }

    resolved_meta = {"keyword": enterprise, "enterprise": enterprise, "resolved": resolved,
                     "reason": "缓存报告（dry-run）" if not resolved else "已有报告"}
    return _wrap(resolved_meta, {}, "cache", enterprise=enterprise,
                 base=base, holders=holders, investments=investments, persons=persons,
                 operation=operation, bidding=bidding, news=news, cloudmigration=cloudmigration,
                 recruitment=recruitment)


def _kv_to_dict(value: Any) -> Dict[str, Any]:
    """Convert a [{字段/名称, 内容/值}] KV list (report style) to a plain dict."""
    out: Dict[str, Any] = {}
    if isinstance(value, list):
        for row in value:
            if isinstance(row, dict):
                k = row.get("字段") or row.get("名称") or row.get("指标") or row.get("维度") or ""
                v = row.get("内容") or row.get("值") or row.get("数量") or row.get("占比") or row.get("值/说明") or ""
                if k:
                    out[str(k)] = v
    elif isinstance(value, dict):
        out = dict(value)
    return out


def _pick(d: Any, *keys: str) -> Any:
    """Tolerant field extractor."""
    if not isinstance(d, dict):
        return None
    for k in keys:
        v = d.get(k)
        if v not in (None, "", "-", []):
            return v
    return None


def _wrap(resolved: Mapping[str, Any], errors: Mapping[str, Any], source: str, **domain: Any) -> Dict[str, Any]:
    enterprise = domain.pop("enterprise", resolved.get("enterprise", ""))
    return {
        "_meta": {
            "enterprise": enterprise,
            "resolved": dict(resolved),
            "source": source,  # "live" | "cache"
            "errors": dict(errors),
        },
        "enterprise": {
            "base": domain.get("base", {}),
            "holders": domain.get("holders", []),
            "investments": domain.get("investments", []),
            "persons": domain.get("persons", []),
        },
        "operation": domain.get("operation", {}),
        "bidding": domain.get("bidding", {}),
        "news": domain.get("news", {}),
        "cloudmigration": domain.get("cloudmigration", {}),
        "recruitment": domain.get("recruitment", {}),
    }


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #
def collect_direct(enterprise: str, keyword_type: str, *, dry_run: bool, skills_root: str) -> Dict[str, Any]:
    """Collect multi-source data: live MCP (default) or cached reports (dry-run)."""
    if dry_run:
        return _collect_cache(skills_root, enterprise)
    try:
        return asyncio.run(_collect_live(enterprise, keyword_type))
    except MultiMcpError as exc:
        # No MCP connection available — gracefully degrade to cached reports.
        print(f"⚠️  MCP 连接不可用 ({exc})，回退到缓存报告模式", file=__import__("sys").stderr)
        return _collect_cache(skills_root, enterprise)
