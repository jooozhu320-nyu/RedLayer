"""Pydantic response models — shapes must match the API contract exactly."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

FindingStatus = Literal["failed", "blocked"]
Severity = Literal["critical", "high", "medium", "low"]


class Option(BaseModel):
    id: str
    label: str


class ConfigResponse(BaseModel):
    suites: list[Option]
    frameworks: list[Option]


class ScanCreateRequest(BaseModel):
    target: str
    suites: list[str]
    frameworks: list[str]


class ScanCreateResponse(BaseModel):
    id: str
    status: Literal["queued"]
    created_at: str


class ScanTarget(BaseModel):
    name: str
    endpoint: str


class ScanProgress(BaseModel):
    completed: int
    total: int


class ScanSummary(BaseModel):
    risk_score: int
    attack_success_rate: float
    findings_count: int
    regs_implicated: int


class ScanStatusResponse(BaseModel):
    id: str
    status: Literal["queued", "running", "complete", "failed"]
    target: ScanTarget
    suites: list[str]
    frameworks: list[str]
    progress: ScanProgress
    summary: ScanSummary | None
    created_at: str
    completed_at: str | None
    error: str | None = None


class FindingSummary(BaseModel):
    id: str
    title: str
    severity: Severity
    harm_category: str
    status: FindingStatus
    regulations: list[str]


class FindingsListResponse(BaseModel):
    findings: list[FindingSummary]


class ToolCall(BaseModel):
    name: str
    arguments: dict


class AgentResponse(BaseModel):
    text: str
    tool_calls: list[ToolCall]
    trigger_matched: str | None


class RegulationRef(BaseModel):
    code: str
    name: str
    rationale: str


class InjectedDocument(BaseModel):
    field: str
    content: str
    injection_span: list[int] | None = None


class RetestHistoryEntry(BaseModel):
    timestamp: str
    result: FindingStatus


class FindingDetail(BaseModel):
    id: str
    title: str
    severity: Severity
    harm_category: str
    status: FindingStatus
    probe: str
    injected_document: InjectedDocument
    agent_response: AgentResponse
    detected_harm: str
    regulations: list[RegulationRef]
    remediation: str
    retest_history: list[RetestHistoryEntry]


class RetestResponse(BaseModel):
    id: str
    result: FindingStatus
    previous_result: FindingStatus
    timestamp: str
    agent_response: AgentResponse
