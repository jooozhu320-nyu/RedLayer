// Framework-neutral client for the SMB-lending red-teaming API
// (docs/backend-plan.md). Build against mocks first, then flip USE_MOCKS.

import type {
  Config,
  FindingDetail,
  FindingSummary,
  RetestResult,
  Scan,
} from "./types";

export const USE_MOCKS = true; // flip to false when the backend is live

const BASE = USE_MOCKS ? "/mocks" : "http://localhost:8000/api";

// Static fixtures for fixed (non-id) responses. Finding detail is routed by id
// below (`finding_001.json`, `finding_002.json`, ...).
const MOCK_FILES = {
  config: "config.json",
  scanRunning: "scan_running.json",
  scanComplete: "scan_complete.json",
  scanCompleteEmpty: "scan_complete_empty.json",
  scanFailed: "scan_failed.json",
  findings: "findings.json",
  findingsEmpty: "findings_empty.json",
  retest: "retest_blocked.json",
} as const;

// In mock mode, pick which end state a scan reaches so the failed/empty screens
// are demoable. Set from a dev control before starting a scan.
export type MockScenario = "happy" | "failed" | "empty";
let mockScenario: MockScenario = "happy";
export function setMockScenario(s: MockScenario) {
  mockScenario = s;
}

// Serve `scan_running` for the first few polls so the progress bar is demoable,
// then flip to the terminal state. Reset when a scan starts.
const MOCK_RUNNING_POLLS = 2;
let mockPollCount = 0;

async function getJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`GET ${url} failed: ${res.status}`);
  return res.json() as Promise<T>;
}

export interface StartScanRequest {
  target: string;
  suites: string[];
  frameworks: string[];
}

export function createApiClient() {
  return {
    getConfig(): Promise<Config> {
      return getJson<Config>(
        USE_MOCKS ? `${BASE}/${MOCK_FILES.config}` : `${BASE}/config`,
      );
    },

    async startScan(req: StartScanRequest): Promise<Scan> {
      if (USE_MOCKS) {
        mockPollCount = 0;
        return getJson<Scan>(`${BASE}/${MOCK_FILES.scanRunning}`);
      }
      const res = await fetch(`${BASE}/scans`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(req),
      });
      if (!res.ok) throw new Error(`POST /scans failed: ${res.status}`);
      return res.json() as Promise<Scan>;
    },

    getScan(scanId: string): Promise<Scan> {
      if (USE_MOCKS) {
        if (mockPollCount++ < MOCK_RUNNING_POLLS) {
          return getJson<Scan>(`${BASE}/${MOCK_FILES.scanRunning}`);
        }
        const terminal =
          mockScenario === "failed"
            ? MOCK_FILES.scanFailed
            : mockScenario === "empty"
              ? MOCK_FILES.scanCompleteEmpty
              : MOCK_FILES.scanComplete;
        return getJson<Scan>(`${BASE}/${terminal}`);
      }
      return getJson<Scan>(`${BASE}/scans/${scanId}`);
    },

    getFindings(scanId: string): Promise<{ findings: FindingSummary[] }> {
      if (USE_MOCKS) {
        const file =
          mockScenario === "empty"
            ? MOCK_FILES.findingsEmpty
            : MOCK_FILES.findings;
        return getJson(`${BASE}/${file}`);
      }
      return getJson(`${BASE}/scans/${scanId}/findings`);
    },

    getFinding(findingId: string): Promise<FindingDetail> {
      // Route by id so each finding shows its own detail (fail loud on a typo).
      return getJson<FindingDetail>(
        USE_MOCKS
          ? `${BASE}/${findingId}.json`
          : `${BASE}/findings/${findingId}`,
      );
    },

    async retest(findingId: string): Promise<RetestResult> {
      if (USE_MOCKS) {
        return getJson<RetestResult>(`${BASE}/${MOCK_FILES.retest}`);
      }
      const res = await fetch(`${BASE}/findings/${findingId}/retest`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(`POST retest failed: ${res.status}`);
      return res.json() as Promise<RetestResult>;
    },
  };
}

export type ApiClient = ReturnType<typeof createApiClient>;
