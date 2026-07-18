# RedLayer — Backend (Python)

The garak-based red-teaming engine for the mock **SMB loan underwriting agent**:
attack suites (garak probes), harm→regulation mapping (ECOA/FCRA/GLBA/SR 11-7),
findings, per-finding re-test, and the JSON API the frontend consumes.

**Stack:** Python 3.12, FastAPI, [garak](https://github.com/NVIDIA/garak) (pinned to
`0.10.2` — see note below), managed with [uv](https://docs.astral.sh/uv/).

## Setup

```
uv sync
cp .env.example .env   # fill in ANTHROPIC_API_KEY
uv run uvicorn app.main:app --reload --port 8000
```

API served under `http://localhost:8000/api`. See [`FRONTEND_SPEC.md`](../FRONTEND_SPEC.md)
for the full contract.

## garak version pin

garak's latest release requires `torch>=2.6.0`, which has no macOS x86_64 (Intel)
wheels. This project pins `garak==0.10.2` (`torch>=2.1.3`, compatible with
`torch==2.2.2`, the last version with Intel Mac wheels) and adapts to that
version's actual API — see the docstrings in `app/plugins/` for specifics (plain
`str` prompts/outputs, not the newer Message/Conversation types; `bcp47` not
`lang`; the `Probe, LatentInjectionMixin` MRO hook-override gotcha). If you're on
Apple Silicon or Linux, garak's latest version should work fine and this pin can
be relaxed.

## Structure

```
app/
  main.py            # FastAPI app + all routes
  schemas.py         # pydantic response models (match FRONTEND_SPEC.md)
  config.py          # SUITES, FRAMEWORKS, target metadata, THRESHOLD
  store.py           # in-memory scans/findings dict + id helpers
  harness.py          # runs probes+detectors, assembles findings + summary
  compliance.py       # maps harm_category -> regulation citations
  target/agent.py     # the mock SMB underwriting agent (under test — ships vulnerable)
  plugins/
    generator.py       # UnderwritingAgentGenerator (garak Generator adapter)
    probes.py          # SMB latent-injection probes (data-poisoning style)
    detectors.py        # finance-specific detectors
```

No database, no auth, one target, three probes — see the build spec for scope.
