"""Harm category -> regulation citations. Plain lookup, no LLM involved."""

from __future__ import annotations

COMPLIANCE_MAP = {
    "unauthorized_action": [
        {
            "code": "ECOA",
            "name": "Equal Credit Opportunity Act / Reg B",
            "rationale": (
                "Manipulable, inconsistent credit decisions create disparate-treatment risk."
            ),
        },
        {
            "code": "SR_11-7",
            "name": "Model Risk Management (SR 11-7)",
            "rationale": "Model can be steered to override its own risk controls.",
        },
    ],
    "pii_exfiltration": [
        {
            "code": "GLBA",
            "name": "Gramm-Leach-Bliley Act",
            "rationale": "Failure to safeguard nonpublic personal financial information.",
        },
    ],
    "disclosure_bypass": [
        {
            "code": "FCRA",
            "name": "Fair Credit Reporting Act",
            "rationale": "Adverse-action notice requirement not met on denial.",
        },
    ],
}


def regulations_for(harm_category: str, frameworks: list[str]) -> list[dict]:
    """Regulations implicated by a harm, filtered to the scan's selected frameworks."""
    return [reg for reg in COMPLIANCE_MAP.get(harm_category, []) if reg["code"] in frameworks]
