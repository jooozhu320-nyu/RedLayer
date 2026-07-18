# RedLayer

**A deterministic, autonomous red-team demo that exposes a layered prompt-injection vulnerability in a mock finance AI agent — then patches it and proves the fix.**

RedLayer attacks a mock **Accounts Payable Agent**, escalates through increasingly layered prompt-injection techniques across chat, documents, email, and tool output, lands one exploit through a real tool call, applies a backend mitigation, and replays the same exploit to show it blocked — all in under 90 seconds.

> ⚠️ **This project contains intentional vulnerabilities for demonstration.** The target agent is deliberately insecure. Nothing here is production-ready or safe to deploy against real systems. See [SECURITY.md](SECURITY.md).

## The story it tells

1. Define a forbidden financial outcome — paying an attacker-controlled account.
2. Run an autonomous scan of five escalating attacks.
3. Attacks 1–4 are **blocked**, each for a specific, explained reason.
4. Attack 5 **succeeds**: layered poisoning (invoice + fake CFO email + poisoned bank-verification result) tricks the agent into calling `prepare_payment` for the wrong account.
5. Inspect proof: the exact tool call and the ordered attack chain.
6. Apply a mitigation and replay.
7. Confirm the malicious change is now blocked **and** a legitimate, out-of-band-approved change still goes through — proving the patch is precise, not a blanket block.

## The vulnerability under test

The mock agent will honor a beneficiary (destination-account) change **if and only if `verify_bank_account` returns `verified`** — trusting a single tool's output as authorization, with no independent cross-check. Attack 5 poisons that tool. The fix: require an independently verified out-of-band approval, sourced from a trusted channel the attacker cannot influence.

## Demo scenario

| Field            | Value                                                   |
| ---------------- | ------------------------------------------------------- |
| Vendor           | CloudGrid Infrastructure                                |
| Invoice          | CG-2026-1842                                            |
| Amount           | $42,850 (simulated)                                     |
| Approved account | ending 3381                                             |
| Attacker account | ending 9017                                             |
| Control case     | invoice CG-2026-1901 → account 7742, genuinely approved |

## Design principles

- **Deterministic.** The target agent's decision is rule-based, not model-sampled. An LLM may generate flavor text, but it never decides whether an attempt succeeds. Grading inspects real tool-call logs.
- **Polling, not streaming.** A simple REST API with an in-memory scan store; the frontend polls status.
- **Evidence-driven.** Success is proven by an actual `prepare_payment` tool call, not an assertion.

## Repository layout

```
.
├── backend/     # Mock agent, scan orchestration, deterministic grader, REST API
├── frontend/    # Single-page demo UI (start → scan → finding → patch → replay)
└── docs/        # Plans and to-dos for both halves
```

## Documentation

- [Backend plan](docs/backend-plan.md) · [Backend to-do](docs/backend-todo.md)
- [Frontend plan](docs/frontend-plan.md) · [Frontend to-do](docs/frontend-todo.md)

## Status

**Planning.** The plans and to-dos are complete; application code has not yet been scaffolded.

## License

[MIT](LICENSE)
