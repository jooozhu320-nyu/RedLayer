"""Wraps UnderwritingAgent behind garak's Generator interface.

Verified against the installed garak==0.10.2 source
(site-packages/garak/generators/base.py): ``_call_model`` takes a plain ``str``
prompt and must return a list of exactly one ``str | None`` — this version of
garak predates the Message/Conversation prompt types.
"""

from __future__ import annotations

import garak._config as _config
from garak.generators.base import Generator

from app.target.agent import UnderwritingAgent


class UnderwritingAgentGenerator(Generator):
    """Adapts the SMB underwriting agent under test to garak's generator interface."""

    generator_family_name = "smb-underwriting"

    def __init__(
        self,
        agent: UnderwritingAgent,
        name: str = "underwriting_agent",
        config_root=_config,
    ) -> None:
        self.agent = agent
        super().__init__(name, config_root=config_root)

    def _call_model(
        self, prompt: str, generations_this_call: int = 1
    ) -> list[str | None]:
        # The agent's response_text already contains the TOOL: line(s) that
        # tool_calls was parsed from (see target/agent.py) — nothing to append.
        result = self.agent.review(prompt)
        return [result["response_text"]]
