# RedLayer — Backend

The mock **Accounts Payable Agent**, scan orchestration, deterministic grader, and REST API.

See [`docs/backend-plan.md`](../docs/backend-plan.md) and
[`docs/backend-todo.md`](../docs/backend-todo.md) for the full contract and build list.

## Responsibilities

- Expose the mock agent's tools: `read_invoice`, `search_finance_email`,
  `lookup_vendor_record`, `verify_bank_account`, `prepare_payment` — logging every call.
- Run the five-attempt scan deterministically and grade success from real tool-call logs.
- Serve the polling API: `POST /scan/start`, `GET /scan/:id/status`, `POST /scan/:id/replay`.
- Apply the mitigation and replay both the malicious and the legitimate control change.

## Not yet scaffolded

Application code lives here once the stack is chosen. CI (`.github/workflows/ci.yml`)
auto-activates the backend job when `backend/package.json` appears.
