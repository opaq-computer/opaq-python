<p align="center"><img src="https://raw.githubusercontent.com/opaq-computer/brand/main/logo/opaq-logo-512.png" width="96" alt="Opaq" /></p>

<h1 align="center">opaq-python</h1>

<p align="center">The Python client for <a href="https://opaq.computer">Opaq</a>: private AI inference on Solana.<br/>200+ models through one OpenAI-compatible endpoint, paid from a sealed balance in Solana Privacy Rings. Zero prompt logs.</p>

<p align="center">
  <a href="https://github.com/opaq-computer/opaq-python/actions/workflows/test.yml"><img src="https://github.com/opaq-computer/opaq-python/actions/workflows/test.yml/badge.svg" alt="tests" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-f7c600" alt="MIT" /></a>
  <a href="https://opaq.computer/docs"><img src="https://img.shields.io/badge/docs-opaq.computer-16161a" alt="docs" /></a>
</p>

## Install

```bash
pip install git+https://github.com/opaq-computer/opaq-python
```

Opaq speaks the OpenAI API, so `Opaq` is the official [`openai`](https://pypi.org/project/openai/) client pointed at Opaq: streaming, tools, vision and async all work unchanged.

## Quickstart

Get a key in the [console](https://opaq.computer/console) (sign in with a Solana wallet, seal a top-up, create a key).

```python
from opaq import Opaq

client = Opaq()  # reads OPAQ_API_KEY

r = client.chat.completions.create(
    model="anthropic/claude-sonnet-5.5",
    messages=[{"role": "user", "content": "Hello"}],
)
print(r.choices[0].message.content)
```

### Streaming

```python
stream = client.chat.completions.create(
    model="deepseek/deepseek-v4.1-flash",
    stream=True,
    messages=[{"role": "user", "content": "Write a haiku about privacy."}],
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

### Async

```python
from opaq import AsyncOpaq

client = AsyncOpaq()
r = await client.chat.completions.create(model="openai/gpt-6.2-sol", messages=[{"role": "user", "content": "hi"}])
```

### Models and prices

```python
from opaq import list_models, estimate_cost

models = list_models()                     # live catalog, no key needed
enclave = list_models(private_only=True)   # models served inside a hardware enclave (TEE)

model = next(m for m in models if m["id"] == "anthropic/claude-sonnet-5.5")
print(estimate_cost(model, r.usage))       # USD, from the usage a response returned
```

### Claude Code

```python
import os, subprocess
from opaq import claude_code_env

subprocess.run(["claude", "--model", "claude-sonnet-5.5"], env={**os.environ, **claude_code_env()})
```

## API

| Name | What it does |
|---|---|
| `Opaq(api_key=None)` / `AsyncOpaq` | `OpenAI` / `AsyncOpenAI` with `base_url` set to `https://opaq.computer/v1`. Raises if no key. |
| `list_models(private_only=False)` | The live catalog from `GET /v1/models`, with prices per 1M tokens. |
| `estimate_cost(model, usage)` | Cost in USD of a response, from OpenAI or Anthropic usage. |
| `claude_code_env(api_key=None)` | The two environment variables that run Claude Code on Opaq. |

## Privacy

Opaq never stores prompts or completions and strips end-user identifiers before routing. What is stored and what stays public is listed at [opaq.computer/security](https://opaq.computer/security).

## Links

[Docs](https://opaq.computer/docs) · [OpenAPI spec](https://opaq.computer/openapi.json) · [Examples](https://github.com/opaq-computer/examples) · [X](https://x.com/OpaqPrivacy) · Security reports: team@opaq.computer

## License

MIT
