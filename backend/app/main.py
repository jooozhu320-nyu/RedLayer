"""FastAPI app exposing the red-teaming engine's REST API. See §7 of the build spec."""

from __future__ import annotations

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import harness, store
from app.config import FRAMEWORKS, SUITES, TARGET_ENDPOINT, TARGET_NAME
from app.schemas import (
    ConfigResponse,
    FindingDetail,
    FindingsListResponse,
    FindingSummary,
    RetestResponse,
    ScanCreateRequest,
    ScanCreateResponse,
    ScanStatusResponse,
)

load_dotenv()

app = FastAPI(title="RedLayer SMB Underwriting Red-Team API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/config", response_model=ConfigResponse)
def get_config() -> ConfigResponse:
    return ConfigResponse(suites=SUITES, frameworks=FRAMEWORKS)


@app.post("/api/scans", response_model=ScanCreateResponse, status_code=201)
def create_scan(req: ScanCreateRequest, background_tasks: BackgroundTasks) -> ScanCreateResponse:
    scan_id = store.new_scan_id()
    created_at = harness.now_iso()
    scan = {
        "id": scan_id,
        "status": "queued",
        "target": {"name": TARGET_NAME, "endpoint": TARGET_ENDPOINT},
        "suites": req.suites,
        "frameworks": req.frameworks,
        "progress": {"completed": 0, "total": 0},
        "summary": None,
        "created_at": created_at,
        "completed_at": None,
        "error": None,
    }
    store.save_scan(scan)
    background_tasks.add_task(harness.run_scan, scan_id)
    return ScanCreateResponse(id=scan_id, status="queued", created_at=created_at)


@app.get("/api/scans/{scan_id}", response_model=ScanStatusResponse)
def get_scan(scan_id: str) -> ScanStatusResponse:
    scan = store.get_scan(scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="scan not found")
    return ScanStatusResponse(**scan)


@app.get("/api/scans/{scan_id}/findings", response_model=FindingsListResponse)
def list_findings(scan_id: str) -> FindingsListResponse:
    scan = store.get_scan(scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="scan not found")
    findings = store.findings_for_scan(scan_id)
    summaries = [
        FindingSummary(
            id=f["id"],
            title=f["title"],
            severity=f["severity"],
            harm_category=f["harm_category"],
            status=f["status"],
            regulations=[r["code"] for r in f["regulations"]],
        )
        for f in findings
    ]
    return FindingsListResponse(findings=summaries)


@app.get("/api/findings/{finding_id}", response_model=FindingDetail)
def get_finding(finding_id: str) -> FindingDetail:
    finding = store.get_finding(finding_id)
    if finding is None:
        raise HTTPException(status_code=404, detail="finding not found")
    return FindingDetail(**finding)


@app.post("/api/findings/{finding_id}/retest", response_model=RetestResponse)
def retest_finding(finding_id: str) -> RetestResponse:
    if store.get_finding(finding_id) is None:
        raise HTTPException(status_code=404, detail="finding not found")
    result = harness.retest_finding(finding_id)
    return RetestResponse(**result)
