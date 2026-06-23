"""
AEGIS security plugin for the Hermes agent harness.

Install: copy this file to ~/.hermes/plugins/aegis-security/plugin.py
         (or register it in ~/.hermes/config.yaml under plugins:)

Hook surface: pre_llm_call(messages) — called by Hermes before each LLM
request. Return the message list unchanged to allow, return None to block.
"""

import subprocess
import sys
import os
import json
import datetime
import pathlib

_AUDIT_LOG = pathlib.Path.home() / ".aegis" / "audit.jsonl"
_AEGIS_TIMEOUT = float(os.environ.get("AEGIS_TIMEOUT_SEC", "0.5"))


def _extract_text(messages: list) -> str:
    parts: list[str] = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block.get("text", ""))
    return "\n".join(parts)


def _audit(verdict: str, rule: str, preview: str) -> None:
    _AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "harness": "hermes",
        "hook": "pre_llm_call",
        "verdict": verdict,
        "rule": rule,
        "preview": preview[:120],
    }
    with _AUDIT_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def pre_llm_call(messages: list) -> list | None:
    """AEGIS pre-LLM hook for Hermes. Returns messages unchanged or None to block."""
    text = _extract_text(messages)
    if not text.strip():
        return messages

    try:
        proc = subprocess.run(
            ["aegis", "scan-pipe"],
            input=text,
            capture_output=True,
            text=True,
            timeout=_AEGIS_TIMEOUT,
        )
    except FileNotFoundError:
        # aegis not on PATH — warn once, then pass through
        print("[aegis] WARNING: aegis binary not found; install from https://github.com/pilot-protocol/aegis", file=sys.stderr)
        return messages
    except subprocess.TimeoutExpired:
        # scan timed out — fail open (don't block production on timeouts)
        print("[aegis] WARNING: scan-pipe timed out; passing through", file=sys.stderr)
        return messages

    if proc.returncode == 2:
        rule = proc.stdout.strip() or "unknown rule"
        _audit("BLOCK", rule, text[:120])
        print(f"[aegis] BLOCKED by Hermes hook — {rule}", file=sys.stderr)
        return None  # signals Hermes to abort this LLM call

    _audit("ALLOW", "", text[:120])
    return messages
