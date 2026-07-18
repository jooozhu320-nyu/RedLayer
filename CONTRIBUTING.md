# Contributing to RedLayer

Thanks for your interest. RedLayer is a focused demo, so contributions should keep the
90-second story tight and the target's flaw honest.

## Ground rules

- **Keep it deterministic.** The target agent's success/failure must never depend on LLM
  sampling. An LLM may generate narration; it must not decide an attempt's outcome.
- **Prove exploits with real tool calls,** not assertions. Grading inspects tool-call logs.
- **Don't weaken the intentional vulnerability** without updating the plans in `docs/` to match.
- **This is not production software.** See [SECURITY.md](SECURITY.md).

## Workflow

1. Branch from `main` (`git switch -c your-change`).
2. Make your change. Update the relevant doc in `docs/` if behavior or contract changes.
3. Run typecheck, lint, and tests for the package you touched (`backend/` or `frontend/`).
4. Open a pull request using the template. Link any related issue.

## Commit style

Clear, imperative, professional messages (e.g. "Add deterministic grader for prepare_payment").
Keep the subject under ~72 characters; explain the "why" in the body when it isn't obvious.

## Project structure

- `backend/` — mock agent, scan orchestration, deterministic grader, REST API
- `frontend/` — single-page demo UI
- `docs/` — the source of truth for the contract and demo behavior
