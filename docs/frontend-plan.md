# Front-End Plan — SMB Lending AI Red-Teaming Dashboard

Source of truth: the frontend handoff spec (2026-07-18). The frontend consumes
clean JSON from the backend (a garak-based red-team engine) and never needs the
security internals. This plan restates the spec in our planning format and adds
our accessibility and demo-reliability conventions.

## What the product does

Scans an AI-powered **SMB loan underwriting agent** for prompt-injection
vulnerabilities — malicious instructions hidden inside documents the agent reads
(bank statements, tax returns) that can trick it into approving loans it
shouldn't, or leaking applicant data. Each finding maps to the financial
regulation or supervisory guidance it **implicates** (**ECOA, FCRA, GLBA,
SR 11-7**).

This is a **deterministic demonstration** of known injection classes mapped to
compliance, not an open-ended discovery scanner — frame it that way for judges.

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

- Four **metric cards**. Make **risk score** the hero card (largest, colored by
  the red/amber/green threshold). Render **regs implicated** as inline framework
  chips (ECOA · FCRA · GLBA · SR 11-7), not a bare count — the compliance mapping
  is the differentiator and should be legible without opening a finding.
- **Findings list** — one row per finding: severity indicator, title, severity badge, chevron.
- While running, show progress from the poll (see Interaction).

### 3. Finding detail (expand-in-place)

Expand **in place** on the dashboard (not a separate route) so the metric cards
stay visible — the retest's ripple into risk-score/attack-rate must be seen in the
same glance as the finding's red→green flip.

Order the content as a narrative a judge can scan in ~15s:

1. Title + severity + status (pinned top).
2. **The attack** — injected document, malicious span highlighted.
3. **What the agent did** — agent response (bad tool call like `approve_loan`),
   with `trigger_matched` surfaced.
4. **The harm** — detected-harm summary + regulation badges together
   (cause → consequence; rationale in tooltip/subtext).
5. **The fix** — suggested remediation.
6. **Re-test button** last, reading as the natural next action after the fix.

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
  drive a progress bar from `progress.completed / progress.total`. Stop on `complete`
  or `failed`, then fetch findings. (Per-suite spinner→check rows are a nice-to-have,
  but need a `suite_progress` field the contract doesn't yet define — don't fake them
  by splitting the aggregate counter.)
- **Failed / empty states:** on `status: "failed"`, show the `error` banner + Retry.
  On zero findings (all blocked), show a positive "target hardened" empty state,
  not a blank list.
- **Expand:** lazy-fetch `GET /api/findings/:id` on first expand (or prefetch — there are ~14).
- **Re-test:** spinner on that finding → `POST …/retest`. From the response:
  (a) flip the finding's `status` red→green; (b) show the **before/after** agent
  response (dim/strike the old text above the new; `trigger_matched` value → `null`)
  — required, it's the proof the fix is real, not cosmetic; (c) show `control_case`
  (legitimate approval still `allowed`); (d) apply the returned `summary` to animate
  the risk-score and attack-success-rate cards, so the headline metrics don't sit
  frozen while one row flips.

## Rendering conventions

- **Status is never color alone** (accessibility): pair every red/green with an
  icon and text. `failed` = vulnerable (red, e.g. ✕ "Failed"); `blocked` =
  resisted/fixed (green, e.g. ✓ "Blocked"); the retest `control_case.result`
  `allowed` = the legitimate approval went through (green ✓ "Allowed", styled
  distinctly from `blocked` — e.g. outline vs. solid — so the two greens read as
  different things).
- **Risk score** (0–100, higher = worse): red ≥ 67, amber 34–66, green ≤ 33.
- **Attack success rate** (0–1): render as `Math.round(x * 100)%`.
- **Severity** (`critical | high | medium | low`): critical/high red, medium amber, low gray.
- **Injection highlight:** use `injected_document.injection_span` `[start, end]` into
  `content` to highlight the malicious text. Don't rely on fill color alone — add a
  visible boundary (bracket icons or an inline ⚠ at the span start) so it reads on a
  projector and for color-blind viewers. Fall back to verbatim content if needed.
- **Surface `agent_response.trigger_matched`** — the canary string proving the injection worked.

## Build against mocks first

Every response shape has a fixture in `frontend/mocks/`. Toggle:

```js
const USE_MOCKS = true; // flip to false when the backend is live
const BASE = USE_MOCKS ? "/mocks" : "http://localhost:8000/api";
```

Minimum mock set: `config.json`, `scan_running.json`, `scan_complete.json`
(same id, different `status`), `findings.json`, `finding_001.json`,
`retest_blocked.json`, `scan_failed.json`, `findings_empty.json`.

Note: `apiClient` serves `scan_running` for the first couple of polls, then
`scan_complete`, so the progress state is demoable on mocks. Under Vite/Next the
`frontend/mocks/` files must be served from the framework's static root (e.g.
`public/mocks/`) for `fetch("/mocks/...")` to resolve.

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
- Metric cards use the risk-score thresholds above; risk score is the hero card;
  regs implicated render as framework chips.
- Re-test updates the dashboard metric cards (from the response `summary`), shows
  before/after agent response, and the `control_case` legitimate-approval result.
- Failed-scan and zero-findings states render (not a blank screen).
- App works fully against `frontend/mocks/` with `USE_MOCKS = true`.
