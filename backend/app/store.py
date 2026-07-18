"""In-memory scan/finding store + id helpers. No database — resets on restart."""

from __future__ import annotations

import itertools
import uuid

_scans: dict[str, dict] = {}
_findings: dict[str, dict] = {}
_finding_counter = itertools.count(1)


def new_scan_id() -> str:
    return f"scan_{uuid.uuid4().hex[:6]}"


def new_finding_id() -> str:
    return f"finding_{next(_finding_counter):03d}"


def save_scan(scan: dict) -> None:
    _scans[scan["id"]] = scan


def get_scan(scan_id: str) -> dict | None:
    return _scans.get(scan_id)


def save_finding(finding: dict) -> None:
    _findings[finding["id"]] = finding


def get_finding(finding_id: str) -> dict | None:
    return _findings.get(finding_id)


def findings_for_scan(scan_id: str) -> list[dict]:
    return [f for f in _findings.values() if f["scan_id"] == scan_id]
