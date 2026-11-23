"""Opaq: private AI inference on Solana.

200+ models through one OpenAI-compatible endpoint, paid from a sealed balance
in Solana Privacy Rings. Zero prompt logs. https://opaq.computer
"""
from __future__ import annotations

import json
import os
import urllib.request
from typing import Any, Mapping

from openai import AsyncOpenAI, OpenAI

__all__ = ["Opaq", "AsyncOpaq", "list_models", "estimate_cost", "claude_code_env", "OPAQ_ORIGIN", "OPAQ_BASE_URL"]
__version__ = "0.1.0"

OPAQ_ORIGIN = "https://opaq.computer"
OPAQ_BASE_URL = f"{OPAQ_ORIGIN}/v1"

_MISSING = "Missing Opaq API key. Pass api_key= or set OPAQ_API_KEY. Create one at https://opaq.computer/console"


def _key(api_key: str | None) -> str:
    key = api_key or os.environ.get("OPAQ_API_KEY")
    if not key:
        raise ValueError(_MISSING)
    return key


class Opaq(OpenAI):
    """An OpenAI client pointed at Opaq. Every method of the official `openai` package works."""

    def __init__(self, *, api_key: str | None = None, base_url: str = OPAQ_BASE_URL, **kwargs: Any) -> None:
        super().__init__(api_key=_key(api_key), base_url=base_url, **kwargs)


class AsyncOpaq(AsyncOpenAI):
    """The async OpenAI client pointed at Opaq."""

    def __init__(self, *, api_key: str | None = None, base_url: str = OPAQ_BASE_URL, **kwargs: Any) -> None:
        super().__init__(api_key=_key(api_key), base_url=base_url, **kwargs)


def list_models(*, private_only: bool = False, base_url: str = OPAQ_BASE_URL, timeout: float = 20) -> list[dict]:
    """The live catalog with prices per 1M tokens (margin included). No key needed."""
    req = urllib.request.Request(f"{base_url}/models", headers={"user-agent": f"opaq-python/{__version__}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)["data"]
    return [m for m in data if m.get("private")] if private_only else data


def estimate_cost(model: Mapping[str, Any], usage: Any) -> float:
    """Cost in USD of a response, from a catalog model and OpenAI or Anthropic usage (object or dict)."""
    pricing = model.get("pricing") if isinstance(model, Mapping) else None
    if not pricing:
        raise ValueError("estimate_cost needs a model from list_models()")

    def read(*names: str) -> int:
        for n in names:
            v = usage.get(n) if isinstance(usage, Mapping) else getattr(usage, n, None)
            if v is not None:
                return int(v)
        return 0

    tokens_in = read("prompt_tokens", "input_tokens")
    tokens_out = read("completion_tokens", "output_tokens")
    return (tokens_in * pricing["prompt_per_mtok"] + tokens_out * pricing["completion_per_mtok"]) / 1e6


def claude_code_env(api_key: str | None = None) -> dict[str, str]:
    """The two environment variables that run Claude Code (or any Anthropic SDK) on Opaq."""
    return {"ANTHROPIC_BASE_URL": OPAQ_ORIGIN, "ANTHROPIC_API_KEY": _key(api_key)}
