# RedLayer — Frontend (Node.js)

The single-page demo UI: start → running scan → finding → patch → replay, understandable
by judges in under 90 seconds without reading logs.

**Stack:** Node.js.

See [`docs/frontend-plan.md`](../docs/frontend-plan.md) and
[`docs/frontend-todo.md`](../docs/frontend-todo.md) for screens, states, and the build list.

## Responsibilities

- Poll `GET /scan/:id/status` and render normalized attempts (icon + text, not color alone).
- Show why attempts 1–4 were blocked and prove attempt 5 with the real tool call.
- Drive the patch + replay, including the **Patch Precision** panel: malicious change
  blocked vs. legitimate change allowed, read from the replay payload.
- Support Reset and graceful failure states (slow backend, poll retries, timeout, mock mode).

## Not yet scaffolded

Application code lives here once the stack is chosen. CI (`.github/workflows/ci.yml`)
auto-activates the frontend job when `frontend/package.json` appears.
