// Types mirroring the backend JSON contract (docs/backend-plan.md "API contract").
// IDs are opaque strings — never parse them.

export type ScanStatusState = "queued" | "running" | "complete" | "failed";
export type FindingStatus = "failed" | "blocked";
export type Severity = "critical" | "high" | "medium" | "low";

export interface Option {
  id: string;
  label: string;
}

export interface Config {
  suites: Option[];
  frameworks: Option[];
}

export interface ScanTarget {
  name: string;
  endpoint: string;
}

export interface ScanProgress {
  completed: number;
  total: number;
}

export interface ScanSummary {
  risk_score: number; // 0-100, higher = worse
  attack_success_rate: number; // 0-1
  findings_count: number;
  regs_implicated: number;
}

export interface Scan {
  id: string;
  status: ScanStatusState;
  target: ScanTarget;
  suites: string[];
  frameworks: string[];
  progress: ScanProgress;
  summary: ScanSummary | null;
  error?: string | null; // set when status is "failed"
  created_at: string;
  completed_at: string | null;
}

export interface FindingSummary {
  id: string;
  title: string;
  severity: Severity;
  harm_category: string;
  status: FindingStatus;
  regulations: string[];
}

export interface AgentResponse {
  text: string;
  tool_calls: { name: string; arguments: Record<string, unknown> }[];
  trigger_matched: string | null;
}

export interface RegulationRef {
  code: string;
  name: string;
  rationale: string;
}

export interface FindingDetail extends Omit<FindingSummary, "regulations"> {
  probe: string;
  injected_document: {
    field: string;
    content: string;
    injection_span: [number, number];
  };
  agent_response: AgentResponse;
  detected_harm: string;
  regulations: RegulationRef[];
  remediation: string;
  retest_history: { timestamp: string; result: FindingStatus }[];
}

export interface RetestControlCase {
  label: string;
  result: "allowed" | "blocked";
  note: string;
}

export interface RetestResult {
  id: string;
  result: FindingStatus;
  previous_result: FindingStatus;
  timestamp: string;
  agent_response: AgentResponse;
  // Present when the fix also re-runs a legitimate control case (proves precision).
  control_case?: RetestControlCase;
  // Recomputed scan metrics so the dashboard cards can update after a fix.
  summary?: ScanSummary;
}
