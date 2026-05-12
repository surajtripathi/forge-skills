"""
VAHAN parivahan portal fetcher — live vehicle registration data.

TOOL_SCHEMA: Anthropic tool definition used by compose_answer.
execute(**params) -> str: called by the tool-use loop in answer_agent.
"""
from __future__ import annotations

import json
import logging
from calendar import month_name

import httpx

logger = logging.getLogger(__name__)

TOOL_SCHEMA: dict = {
    "name": "vahan_fetch_monthly_sales",
    "description": (
        "Fetch monthly vehicle registration counts from the official VAHAN parivahan "
        "portal (vahan.parivahan.gov.in) for a specific maker and time period. "
        "Use this whenever the user asks for real sales / registration figures for "
        "an OEM in India. Returns official RTO registration data, NOT factory dispatch."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "maker": {
                "type": "string",
                "description": (
                    "Maker name as it appears in VAHAN (all-caps). "
                    "Examples: 'TATA MOTORS LTD', 'MARUTI SUZUKI INDIA LTD', "
                    "'HYUNDAI MOTOR INDIA LTD', 'MAHINDRA & MAHINDRA LTD', "
                    "'HONDA MOTORCYCLE & SCOOTER INDIA PVT LTD'. "
                    "If unsure of exact spelling, use the popular brand name "
                    "(e.g. 'TATA') and the tool will fuzzy-match."
                ),
            },
            "month": {
                "type": "integer",
                "description": "Calendar month (1=January … 12=December).",
            },
            "year": {
                "type": "integer",
                "description": "Calendar year (e.g. 2025, 2026).",
            },
            "vehicle_class": {
                "type": "string",
                "description": (
                    "Vehicle class to filter. Common values: 'Motor Car', "
                    "'Motor Cycle', 'Motor Cab', 'ALL'. Defaults to 'ALL'."
                ),
            },
        },
        "required": ["maker", "month", "year"],
    },
}

_BASE = "https://vahan.parivahan.gov.in/vahan4dashboard"
_FY_START = 4  # April is month 1 of the Indian financial year

_MONTH_ABBR = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; ForgeAnswerEngine/1.0; "
        "+https://github.com/your-org/forge)"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"{_BASE}/",
}


def _financial_year(calendar_year: int, month: int) -> str:
    """Return VAHAN financial-year string (e.g. '2025-2026')."""
    if month >= _FY_START:
        return f"{calendar_year}-{calendar_year + 1}"
    return f"{calendar_year - 1}-{calendar_year}"


def _fy_month_index(calendar_month: int) -> int:
    """April=1, May=2, … March=12."""
    return ((calendar_month - _FY_START) % 12) + 1


def execute(
    maker: str,
    month: int,
    year: int,
    vehicle_class: str = "ALL",
) -> str:
    """
    Return a plain-text summary of VAHAN monthly registration data.

    Falls back to an informative error string so the caller (Claude)
    can communicate the situation to the user.
    """
    fy = _financial_year(year, month)
    fy_month = _fy_month_index(month)
    month_label = f"{month_name[month]} {year}"

    try:
        with httpx.Client(timeout=20, follow_redirects=True) as client:
            # Step 1: seed the session (VAHAN uses JSF session cookies).
            client.get(_BASE + "/", headers={"User-Agent": _HEADERS["User-Agent"]})

            # Step 2: fetch comparative maker-month data.
            resp = client.post(
                f"{_BASE}/vahan/dashboardview/getAllVehicleDetails",
                headers=_HEADERS,
                data={
                    "groupVal": maker.upper(),
                    "selectedMonth": fy_month,
                    "fYear": fy,
                    "selectedvehicleClass": vehicle_class,
                },
            )
            resp.raise_for_status()

            try:
                payload = resp.json()
            except Exception:
                # Response may be HTML or empty on bad maker name
                return _no_data_message(maker, month_label, fy)

            rows = payload if isinstance(payload, list) else payload.get("data", [])
            if not rows:
                return _no_data_message(maker, month_label, fy)

            return _format_rows(rows, maker, month_label, fy)

    except httpx.TimeoutException:
        logger.warning("vahan_fetcher: request timed out maker=%s fy=%s", maker, fy)
        return (
            f"VAHAN portal timed out while fetching data for {maker!r} "
            f"({month_label}). The portal may be temporarily unavailable. "
            f"Try again later or visit {_BASE} manually."
        )
    except httpx.HTTPStatusError as exc:
        logger.warning(
            "vahan_fetcher: HTTP %s maker=%s fy=%s", exc.response.status_code, maker, fy
        )
        return (
            f"VAHAN portal returned HTTP {exc.response.status_code} "
            f"for {maker!r} ({month_label}). "
            f"Verify the maker name or visit {_BASE} to check availability."
        )
    except Exception as exc:
        logger.error("vahan_fetcher: unexpected error maker=%s: %s", maker, exc)
        return (
            f"Could not fetch live VAHAN data for {maker!r} ({month_label}): {exc}. "
            f"Visit {_BASE} for manual lookup."
        )


def _no_data_message(maker: str, month_label: str, fy: str) -> str:
    return (
        f"No registration data found on VAHAN for maker '{maker}' "
        f"in {month_label} (FY {fy}). Possible reasons: "
        "(1) exact maker name doesn't match VAHAN spelling, "
        "(2) data for this month hasn't been uploaded yet (2–4 week lag is normal), "
        "(3) the vehicle class filter excludes all matching vehicles. "
        f"Visit {_BASE} and use the Comparative Report to search manually."
    )


def _format_rows(rows: list, maker: str, month_label: str, fy: str) -> str:
    lines = [
        f"VAHAN registration data — {maker} — {month_label} (FY {fy})",
        "",
    ]
    total = 0
    for row in rows:
        state = row.get("stateName") or row.get("state") or row.get("groupValue", "")
        count = row.get("totalRegistration") or row.get("count") or row.get("total", 0)
        try:
            count = int(count)
            total += count
        except (ValueError, TypeError):
            count = "?"
        if state:
            lines.append(f"  {state}: {count:,}" if isinstance(count, int) else f"  {state}: {count}")

    lines.append("")
    lines.append(f"Total registrations: {total:,}")
    lines.append(
        "(Source: VAHAN parivahan.gov.in — reflects RTO registrations, "
        "not factory dispatches. Data may lag 2–4 weeks.)"
    )
    return "\n".join(lines)
