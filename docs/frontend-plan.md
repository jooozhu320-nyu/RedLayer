# Front-End Plan — SMB Lending AI Red-Teaming Dashboard

Source of truth: the frontend handoff spec (2026-07-18). The frontend consumes
clean JSON from the backend (a garak-based red-team engine) and never needs the
security internals. This plan restates the spec in our planning format and adds
our accessibility and demo-reliability conventions.

## What the product does

Scans an AI-powered **SMB loan underwriting agent** for prompt-injection
vulnerabilities — malicious instructions hidden inside documents the agent reads
(bank statements, tax returns) that can trick it into approving loans it
shouldn't, or leaking applicant data. Each vulnerability maps to the specific
financial regulation it would put a lender in violation of (**ECOA, FCRA, GLBA,
SR 11-7**).

The user configures a scan, watches it run, browses findings, and — the key demo
moment — **re-tests a finding after a fix and watches it flip from "failed" (red)
to "blocked" (green).**

## Stack

Single-page app (Node.js) with client-side routing. Framework TBD (Vite+React or
Next.js). Build against mocks first (see below).

> **Layout is flexible; the JSON data contract is not.** Rearrange screens freely,
> but keep the API shapes exact (see [backend-plan.md](backend-plan.md)). A
> reference wireframe (screenshots/Figma) will be shared separately.

## Screens

### 1. Scan configuration (`/`)

- Target endpoint field — read-only / prefilled (one target for the demo).
- Multi-select of **attack suites** (from `GET /api/config`).
- Multi-select of **compliance frameworks** (from `GET /api/config`).
- **Run scan** button → `POST /api/scans` → navigate to `/scans/:id`.

### 2. Results dashboard (`/scans/:id`)

- Four **metric cards**: risk score, attack success rate, findings count, regs implicated.
- **Findings list** — one row per finding: severity indicator, title, severity badge, chevron.
- While running, show progress from the poll (see Interaction).

### 3. Finding detail (expand-in-place or `/findings/:id`)

- **Injected document** — doc text with the malicious span highlighted.
- **Agent response** — what the agent did (often a bad tool call like `approve_loan`).
- **Detected harm** — plain-English summary.
- **Regulations implicated** — badges (rationale in tooltip/subtext).
- **Suggested remediation** — one line.
- **Re-test button** + a status line showing the current pass/fail state.

## API contract (summary)

Full request/response shapes live in [backend-plan.md](backend-plan.md). Base URL
(dev) `http://localhost:8000/api`; JSON; no auth (localhost); IDs are opaque.

| Method | Path                   | Purpose                                   |
| ------ | ---------------------- | ----------------------------------------- |
| GET    | `/config`              | Suites + frameworks for the config screen |
| POST   | `/scans`               | Start a scan (async; returns `queued`)    |
| GET    | `/scans/:id`           | Status + summary metrics (poll)           |
| GET    | `/scans/:id/findings`  | Findings list (summary fields)            |
| GET    | `/findings/:id`        | Full finding detail                       |
| POST   | `/findings/:id/retest` | Re-run one finding; returns new pass/fail |

## Interaction and state

- **Start:** `POST /api/scans` → get `id` → route to `/scans/:id`.
- **Poll:** while `status` is `queued` or `running`, `GET /api/scans/:id` every ~1.5s;
  drive a progress bar from `progress.completed / progress.total`. Stop on
  `complete` or `failed`, then fetch findings.
- **Expand:** lazy-fetch `GET /api/findings/:id` on first expand (or prefetch — there are ~14).
- **Re-test:** spinner on that finding → `POST …/retest` → update its `status` from
  the response; animate red→green. This is the moment judges remember.

## Rendering conventions

- **Status is never color alone** (accessibility): pair every red/green with an
  icon and text. `failed` = vulnerable (red, e.g. ✕ "Failed"); `blocked` =
  resisted/fixed (green, e.g. ✓ "Blocked").
- **Risk score** (0–100, higher = worse): red ≥ 67, amber 34–66, green ≤ 33.
- **Attack success rate** (0–1): render as `Math.round(x * 100)%`.
- **Severity** (`critical | high | medium | low`): critical/high red, medium amber, low gray.
- **Injection highlight:** use `injected_document.injection_span` `[start, end]` into
  `content` to highlight the malicious text; fall back to verbatim content if needed.
- **Surface `agent_response.trigger_matched`** — the canary string proving the injection worked.

## Build against mocks first

Every response shape has a fixture in `frontend/mocks/`. Toggle:

```js
const USE_MOCKS = true; // flip to false when the backend is live
const BASE = USE_MOCKS ? "/mocks" : "http://localhost:8000/api";
```

Minimum mock set: `config.json`, `scan_running.json`, `scan_complete.json`
(same id, different `status`), `findings.json`, `finding_001.json`,
`retest_blocked.json`.

## Scope guardrails (hackathon)

- One hardcoded target; no general connector UI.
- Skip auth, accounts, scan-history lists, pagination.
- Priority order — cut from the bottom if time runs out:
  1. The re-test red→green flow
  2. Finding detail with reg badges
  3. Metric cards
  4. Polish

## Manual review

- The story is understandable without reading logs.
- Findings render status with icon + text, not color alone.
- Re-test updates state from the response and animates red→green.
- Injection highlight and `trigger_matched` are visible on a failed finding.
- Metric cards use the risk-score thresholds above.
- App works fully against `frontend/mocks/` with `USE_MOCKS = true`.
