# Back-End To-Do — SMB Lending Red-Teaming Engine

## garak integration

- [ ] Add garak as a dependency and confirm a minimal scan runs
- [ ] Wire a mock SMB underwriting target (`POST /agents/underwriting/run`)
- [ ] Make the target's approve/deny + disclosure behavior rule-based (deterministic)
- [ ] Define canary triggers (e.g. `OVR-7734-APPROVE`) and detectors for them

## Attack suites and probes

- [ ] Suite `latent_injection`: instructions hidden in document fields
- [ ] Suite `unauthorized_action`: `smb.SMBLoanApprovalInjection` → bad `approve_loan`
- [ ] Suite `pii_exfiltration`: cross-applicant leak via RAG store
- [ ] Suite `disclosure_bypass`: missing adverse-action notice on denial
- [ ] Map each suite id to its garak probe group

## Injected document fixtures

- [ ] Author bank-statement and tax-return documents with malicious spans
- [ ] Record `injection_span` [start, end] for each
- [ ] Keep documents plausible-but-synthetic (no real PII)

## Compliance mapping

- [ ] harm_category → regulations mapping (ECOA, FCRA, GLBA, SR 11-7)
- [ ] One-line `rationale` per regulation
- [ ] Report only frameworks selected for the scan
- [ ] Compute `regs_implicated` for the summary

## Findings

- [ ] Build finding objects from probe/detector results
- [ ] severity, harm_category, status (failed|blocked)
- [ ] injected_document (field, content, injection_span)
- [ ] agent_response (text, tool_calls, trigger_matched)
- [ ] detected_harm, remediation, retest_history

## Fix and re-test

- [ ] Implement the backend fix (document/instruction isolation; human sign-off on approve_loan)
- [ ] Enable the fix so retest returns `blocked`
- [ ] Re-test re-runs a single probe and returns result + previous_result + agent_response
- [ ] Precision: fix blocks injection but still allows a legitimate approval

## API

- [ ] `GET /api/config` (suites + frameworks)
- [ ] `POST /api/scans` → 201, async, returns `queued`
- [ ] `GET /api/scans/:id` with progress, summary when complete
- [ ] `GET /api/scans/:id/findings`
- [ ] `GET /api/findings/:id`
- [ ] `POST /api/findings/:id/retest`
- [ ] Open CORS for localhost; JSON everywhere
- [ ] Async scan worker (queued → running → complete/failed)

## Metrics

- [ ] risk_score 0–100
- [ ] attack_success_rate 0–1
- [ ] findings_count
- [ ] regs_implicated

## Determinism and errors

- [ ] Pin target/model config + seed so scans reproduce
- [ ] 404 on unknown scan/finding id
- [ ] 400 on malformed request
- [ ] Scan failure → status "failed" with a short error
- [ ] Repeating a scan yields the same findings; re-test reproducible

## Document enrichment (Tavily, authoring-side)

- [ ] Isolated `authoring` package with the Tavily client (not on the runtime path)
- [ ] `regenerate_content` script: query Tavily, compose, write fixtures, record provenance
- [ ] `tavily` as an optional dependency, not installed for demo/CI runtime
- [ ] Test: scan path never imports the Tavily client (import-graph firewall)

## Manual review checklist

- [ ] Config shape matches the frontend exactly
- [ ] Failed findings carry real tool calls + trigger_matched
- [ ] injection_span bounds the malicious text
- [ ] Mapping only reports selected frameworks
- [ ] Re-test flips failed → blocked via real behavior change
- [ ] Scans are reproducible

## Council review follow-ups (2026-07-18)

- [ ] Build the garak `report.jsonl` → Finding adapter (the core, currently unowned)
- [ ] Custom garak generator so the target's structured tool call survives into the report
- [ ] Run garak as a subprocess per scan; derive progress from completed probes
- [ ] Retest invokes a single probe+detector directly (bypass the batch run)
- [ ] Restrict grading to deterministic string/trigger detectors; exclude ML detectors
- [ ] Register custom probes/detectors in garak's plugin namespace
- [ ] Add a distinct PII canary + detector and a second-applicant record for a real cross-applicant leak
- [ ] Retest returns malicious + legitimate control results and a recomputed summary
- [ ] Define risk_score / attack_success_rate formulas; label metrics as authored-suite, not measured exposure
- [ ] Correct harm→regulation mapping (disclosure→ECOA+FCRA; re-scope unauthorized_action; SR 11-7 = guidance); "implicates" not "violates"
- [ ] Tavily fixture scrub/validation pass + CI test that fails on PII patterns
- [ ] Add garak + web framework to dependencies; declare `authoring` extra (done in pyproject)
- [ ] Replace the stale Accounts-Payable scaffold tests with garak-engine tests (current CI is false-green)
