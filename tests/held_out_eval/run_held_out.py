#!/usr/bin/env python3
"""
AEGIS held-out adversarial evaluation.

Usage:
    python3 tests/held_out_eval/run_held_out.py [--l1-only]

Scans all files in corpus/malicious/ and corpus/benign/, reports
precision, recall, F1, and false-positive rate vs. the LABEL header.
Exits non-zero if precision < 0.90 or recall < 0.80.
"""
import subprocess, sys, os, pathlib, re

REPO = pathlib.Path(__file__).parent.parent.parent
BIN = REPO / "target/release/aegis"
CORPUS = pathlib.Path(__file__).parent / "corpus"
L1_ONLY = "--l1-only" in sys.argv

def label_from_file(path: pathlib.Path) -> str:
    """Read the LABEL comment from the first few lines of a file."""
    try:
        text = path.read_text(errors="replace")
        for line in text.splitlines()[:5]:
            m = re.search(r'LABEL:\s*(MALICIOUS|BENIGN)', line, re.I)
            if m:
                return m.group(1).upper()
    except Exception:
        pass
    # Infer from directory
    return "MALICIOUS" if "malicious" in str(path) else "BENIGN"

def scan_file(path: pathlib.Path) -> str:
    """Return QUARANTINE, WARN, or ALLOW."""
    cmd = [str(BIN), "scan", str(path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        combined = result.stdout + result.stderr
        if "QUARANTINE" in combined or "BLOCK" in combined:
            return "QUARANTINE"
        if "WARN" in combined and "pattern fired" in combined:
            return "WARN"
        return "ALLOW"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

if not BIN.exists():
    print(f"ERROR: binary not found at {BIN} — run: cargo build --release")
    sys.exit(1)

files = list(CORPUS.glob("**/*"))
files = [f for f in files if f.is_file() and not f.name.startswith(".")]

if not files:
    print(f"No files found in {CORPUS}")
    sys.exit(1)

tp = fp = tn = fn = warn_tp = warn_fp = 0
results = []

for path in sorted(files):
    truth = label_from_file(path)
    verdict = scan_file(path)
    predicted_attack = verdict in ("QUARANTINE",)
    actual_attack = truth == "MALICIOUS"

    if actual_attack and predicted_attack:      tp += 1
    elif not actual_attack and predicted_attack: fp += 1
    elif not actual_attack and not predicted_attack: tn += 1
    else:                                        fn += 1

    if verdict == "WARN":
        if actual_attack: warn_tp += 1
        else:             warn_fp += 1

    status = "✓" if (actual_attack == predicted_attack) else "✗"
    results.append((status, verdict, truth, path.name))

print(f"\nAEGIS Held-out Evaluation  ({len(files)} files)\n{'─'*60}")
for status, verdict, truth, name in results:
    print(f"  {status}  {verdict:<12} [{truth:<9}]  {name}")

print(f"\n{'─'*60}")
precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
fp_rate   = fp / (fp + tn) if (fp + tn) > 0 else 0.0

print(f"  Recall    : {recall:.0%}   ({tp} TP, {fn} FN)")
print(f"  Precision : {precision:.0%}   ({tp} TP, {fp} FP)")
print(f"  FP rate   : {fp_rate:.0%}   ({fp} FP, {tn} TN)")
print(f"  F1        : {f1:.0%}")
if warn_tp + warn_fp > 0:
    print(f"  WARN      : {warn_tp} true positives surfaced, {warn_fp} false positives surfaced")
print()

ok = precision >= 0.90 and recall >= 0.80
if ok:
    print("PASS — meets minimum thresholds (precision ≥ 90%, recall ≥ 80%)")
else:
    print("FAIL — below minimum thresholds:")
    if precision < 0.90: print(f"  precision {precision:.0%} < 90%")
    if recall    < 0.80: print(f"  recall    {recall:.0%} < 80%")
    sys.exit(1)
