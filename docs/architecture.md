# Architecture: Pluggable Verticals

RedLayer separates a **domain-agnostic engine** from **pluggable verticals**.
The engine runs scans, grades from observable output, and serves the API without
knowing what domain it is attacking. Each vertical is a self-contained package
that teaches the engine one domain. **Finance** is the first; new domains
(healthcare, legal, HR, support, …) drop in without engine changes.

> **Direction update (2026-07-18).** The active product is an **SMB
> loan-underwriting** red-teaming dashboard built on NVIDIA **garak**
> (see [backend-plan.md](backend-plan.md), [frontend-plan.md](frontend-plan.md)).
> The pattern below still holds, with this mapping:
>
> - A **vertical** is still a domain (finance). A **scenario** is the SMB
>   underwriting target + a garak probe suite, surfaced as **findings** rather
>   than a scripted attempt sequence.
> - Grading is done by **garak detectors** on observable output (tool calls,
>   canary strings) — the "deterministic, no-LLM-judge" rule is unchanged.
> - The **frontend is config-driven**: suites and frameworks come from
>   `GET /api/config`, so there is no frontend vertical registry (removed).
> - **Migration status:** the code under `backend/src/redlayer/` is the pattern
>   scaffold from the first direction (Accounts Payable scenario). This is a
>   **rewrite, not an incremental migration** — `core/models.py`, `scanner.py`,
>   `registry.py`, and `verticals/finance/*` use a different vocabulary
>   (`AttackAttempt`/`AttemptStatus` vs. `Finding`/`queued|running|complete|failed`)
>   and will be replaced. Note the two existing tests exercise the archived
>   scenario, so **CI is currently false-green** — the garak engine has no coverage
>   yet. Replace those tests as the engine lands.

## Concepts

- **Vertical** — a domain being red-teamed (e.g. `finance`). Contributes one or
  more scenarios.
- **Scenario** — a target agent + a forbidden objective, plus everything needed
  to run the demo: the attack sequence, a deterministic grader, evidence, and a
  mitigation. Identified by `target_id` + `objective_id`, which is exactly what
  the API's `POST /scan/start` selects.
- **Engine (`core`)** — scan orchestration, the in-memory store, the shared
  data model, evidence, and the registry. Depends only on the abstract contract,
  never on a concrete vertical.

```
core  ──uses──▶  verticals/base (ABCs)  ◀──implements──  verticals/finance
  ▲                                                            │
  └──────────────── registry resolves target+objective ───────┘
```

The one hard rule: **`core` must never import from a concrete vertical.** That
inversion is what keeps verticals pluggable.

## Backend layout (`backend/src/redlayer/`)

```
core/
  models.py      # AttackAttempt, ToolCall, Evidence, ScanSummary, enums
  registry.py    # register / resolve verticals and scenarios
  scanner.py     # in-memory ScanStore + run_scan / run_replay (loop = TODO)
  evidence.py    # (future) shared evidence helpers
verticals/
  base.py        # RedTeamVertical + Scenario abstract contract
  __init__.py    # load_verticals(): registers every built-in vertical
  finance/
    fixtures.py     # simulated vendor, invoices, accounts, approval ledger
    target.py       # mock Accounts Payable Agent tools (rule-based decision)
    attempts.py     # the 5 attacks + the legitimate control case
    grading.py      # deterministic grader (prepare_payment → 9017)
    mitigations.py  # out-of-band approval patch (precise, not blanket)
    vertical.py     # AccountsPayableScenario + FinanceVertical wiring
api/
  app.py         # create_app() — framework TBD (FastAPI vs Flask)
```

## Frontend layout (`frontend/src/`)

```
core/
  types.ts       # mirror of the backend JSON contract (Config, Scan, Finding, Retest)
  apiClient.ts   # client for the 6 endpoints, with USE_MOCKS toggle
  polling.ts     # poll /scans/:id until complete/failed
components/       # shared UI (framework TBD)
mocks/            # (frontend/mocks/) static fixtures for USE_MOCKS mode
```

The UI is config-driven: suites and frameworks come from `GET /api/config`, and
findings render generically from the API. There is no frontend vertical registry.

## How to add a vertical

**Backend**

1. Create `backend/src/redlayer/verticals/<name>/`.
2. Implement `Scenario` (subclass `verticals.base.Scenario`): set `target_id`,
   `objective_id`, `forbidden_outcome`; implement `build_attempts`, `grade`
   (deterministic, from tool calls), `build_evidence`, and `apply_mitigation`.
3. Implement `RedTeamVertical` returning your scenario(s), plus a
   `build_vertical()` factory.
4. Register it in `verticals/__init__.py` `load_verticals()`.
5. Add tests mirroring `tests/test_vertical_registry.py`.

**Frontend**

The frontend is config-driven — suites and frameworks come from `GET /api/config`,
so a new domain needs no frontend registry entry. At most, add display copy where
the UI labels new suites/frameworks. (There is no `frontend/src/verticals/` — it was
removed.)

No `core` files change in either half. That is the point.

## Invariants every vertical must uphold

- **Deterministic outcomes.** The target's decision is rule-based; an LLM may
  narrate but must never gate an attempt's status.
- **Grade from real tool calls,** never from an LLM judgment.
- **Precise mitigations.** Prove the patch blocks the exploit _and_ still allows
  a legitimate, properly authorized action (the control case).
