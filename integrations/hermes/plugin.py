"""
AEGIS security plugin for the Hermes agent harness.

Install: copy this file to ~/.hermes/plugins/aegis-security/plugin.py
         (or register it in ~/.hermes/config.yaml under plugins:)

Hook surface: pre_llm_call(messages) — called by Hermes before each LLM
request. Returns messages unchanged (allow) or raises AegisBlockedError (block).
Callers must NOT catch AegisBlockedError unless they intend to suppress it.
"""

import subprocess
import sys
import os
import json
import datetime
import pathlib

_AUDIT_LOG = pathlib.Path.home() / ".aegis" / "audit.jsonl"
_AEGIS_TIMEOUT = float(os.environ.get("AEGIS_TIMEOUT_SEC", "0.5"))


class AegisBlockedError(RuntimeError):
    """Raised when AEGIS blocks a pre-LLM message. Do not catch and silently ignore."""
    def __init__(self, rule: str) -> None:
        self.rule = rule
        super().__init__(f"AEGIS blocked LLM call: {rule}")


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


def _audit(verdict: str, rule: str, preview_hash: str) -> None:
    _AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "harness": "hermes",
        "hook": "pre_llm_call",
        "verdict": verdict,
        "rule": rule,
        # Hash instead of plaintext to avoid leaking system-prompt secrets into
        # the audit log (which is mode 0644 by default).
        "preview_sha256": preview_hash,
    }
    with _AUDIT_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def _sha256_hex(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def pre_llm_call(messages: list) -> list:
    """AEGIS pre-LLM hook for Hermes. Returns messages or raises AegisBlockedError."""
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
        print("[aegis] WARNING: aegis binary not found; install from https://github.com/pilot-protocol/aegis", file=sys.stderr)
        return messages
    except subprocess.TimeoutExpired:
        print("[aegis] WARNING: scan-pipe timed out; passing through", file=sys.stderr)
        return messages

    if proc.returncode == 2:
        rule = proc.stdout.strip() or "unknown rule"
        _audit("BLOCK", rule, _sha256_hex(text))
        raise AegisBlockedError(rule)

    if proc.returncode != 0:
        # Crash / OOM / signal — treat as block (fail closed on unexpected exits)
        rule = f"AEGIS_ERROR:exit{proc.returncode}"
        _audit("BLOCK", rule, _sha256_hex(text))
        raise AegisBlockedError(rule)

    _audit("ALLOW", "", _sha256_hex(text))
    return messages
