# Front-End To-Do — SMB Lending Dashboard

## Setup and API layer

- [ ] Pick framework (Vite+React or Next.js) and scaffold the SPA with routing
- [ ] Add `USE_MOCKS` toggle and `BASE` switch (mocks vs `http://localhost:8000/api`)
- [ ] Create the six mock fixtures in `frontend/mocks/`
- [ ] Add TypeScript types for config, scan, finding-summary, finding-detail, retest
- [ ] API client for all six endpoints
- [ ] Polling utility: poll `/scans/:id` every ~1.5s, stop on `complete`/`failed`

## Scan configuration (`/`)

- [ ] Prefilled read-only target endpoint field
- [ ] Multi-select of attack suites from `GET /api/config`
- [ ] Multi-select of compliance frameworks from `GET /api/config`
- [ ] Run scan button → `POST /api/scans` → route to `/scans/:id`
- [ ] Disable/spinner state while the scan is being created

## Results dashboard (`/scans/:id`)

- [ ] Progress bar from `progress.completed / progress.total` while running
- [ ] Metric card: risk score with red/amber/green thresholds (≥67 / 34–66 / ≤33)
- [ ] Metric card: attack success rate as `Math.round(x*100)%`
- [ ] Metric card: findings count
- [ ] Metric card: regs implicated
- [ ] Findings list rows: severity indicator, title, severity badge, chevron
- [ ] Fetch findings once scan is `complete`

## Finding detail

- [ ] One shared detail component (expand-in-place or `/findings/:id`)
- [ ] Lazy-fetch `GET /api/findings/:id` on first expand
- [ ] Injected document with malicious span highlighted via `injection_span`
- [ ] Agent response with tool calls; surface `trigger_matched` canary
- [ ] Detected harm summary
- [ ] Regulation badges with `rationale` as tooltip/subtext
- [ ] Suggested remediation line
- [ ] Status line showing current pass/fail

## Re-test flow (top priority)

- [ ] Re-test button per finding
- [ ] Spinner on the finding during `POST /api/findings/:id/retest`
- [ ] Update finding `status` from the response `result`
- [ ] Animate red→green transition
- [ ] Show before/after: `previous_result` → `result` (optionally diff agent_response)

## Accessibility and presentation

- [ ] Status uses icon + text, never color alone
- [ ] Severity/risk colors match the documented thresholds
- [ ] Readable on a projector-sized window
- [ ] Record a backup demo video

## Manual review checklist

- [ ] Whole app runs against `frontend/mocks/` with `USE_MOCKS = true`
- [ ] Switching to live backend is a one-line change
- [ ] Re-test updates from the response and animates red→green
- [ ] Injection highlight and `trigger_matched` visible on a failed finding
- [ ] Metric cards apply the risk-score thresholds
- [ ] No status conveyed by color alone

## Council review follow-ups (2026-07-18)

- [ ] Finding detail expands in place (dashboard cards stay visible)
- [ ] Progress bar from `progress.completed/total`; per-suite rows only if the backend adds a `suite_progress` field
- [ ] Risk score is the hero card; regs implicated render as framework chips
- [ ] Retest applies the returned `summary` to animate the metric cards
- [ ] Retest shows before/after agent response (required) + `trigger_matched`→null
- [ ] Retest shows the `control_case` (legitimate approval still allowed)
- [ ] Failed-scan state (error banner + Retry) using `scan_failed.json`
- [ ] Zero-findings "target hardened" state using `findings_empty.json`
- [ ] Injection highlight has a boundary marker/icon, not fill color alone
- [ ] Serve `frontend/mocks/` from the framework static root (`public/mocks/`)
- [ ] Finding-detail content follows the attack→did→harm→fix→retest order
