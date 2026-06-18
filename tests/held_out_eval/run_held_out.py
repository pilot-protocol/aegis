#!/usr/bin/env python3
"""
AEGIS held-out evaluation.

A corpus of 190 realistic files (95 benign / 95 malicious) that were NEVER used to
tune AEGIS's patterns or judge prompts. This is the honest test of usefulness:
does it catch attacks without crying wolf on real developer/agent content?

The corpus + labels live in ./corpus/ and ./manifest.jsonl. Each scan runs the
release binary, which talks to a warm llama-server (the L3 judge). Start one first
for speed, or the binary will cold-start its own per batch:

    llama-server --model ~/.aegis/models/Qwen3-1.7B-Q8_0.gguf \
        --port 8849 --host 127.0.0.1 -ngl 99 -c 4096 \
        --reasoning-budget 0 --jinja --no-webui &

Then:

    python3 run_held_out.py [path/to/aegis/binary]

Reports recall / precision / FP-rate / F1, a per-class breakdown, and the exact
false positives and false negatives so regressions are diagnosable.
"""
import json, subprocess, os, sys, collections, pathlib

HERE = pathlib.Path(__file__).parent
# Repo root is two levels up (tests/held_out_eval/ -> repo); the crate builds to target/.
AEGIS = sys.argv[1] if len(sys.argv) > 1 else str(HERE.parent.parent / "target/release/aegis")
MANIFEST = HERE / "manifest.jsonl"
BATCH = 40  # files per aegis invocation (one process => model/server reused, warm)


def load_manifest():
    items = {}
    for line in open(MANIFEST):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        f = str(HERE / d["file"])
        if os.path.isfile(f):
            items[f] = (d["label"], d.get("class", "?"))
    return items


def scan_batch(files):
    """Return the set of files AEGIS flagged (QUARANTINE/BLOCK)."""
    r = subprocess.run([AEGIS, "scan"] + files, capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr
    flagged = set()
    for line in out.splitlines():
        if "QUARANTINE" in line or "BLOCK" in line:
            for f in files:
                if f in line:
                    flagged.add(f)
    return flagged


def main():
    if not os.path.exists(AEGIS):
        sys.exit(f"aegis binary not found: {AEGIS}")
    items = load_manifest()
    print(f"AEGIS:   {AEGIS}")
    print(f"corpus:  {len(items)} files "
          f"({sum(l=='benign' for l,_ in items.values())} benign / "
          f"{sum(l=='malicious' for l,_ in items.values())} malicious)\n")

    files = list(items)
    detected = set()
    for i in range(0, len(files), BATCH):
        detected |= scan_batch(files[i:i + BATCH])
        print(f"  scanned {min(i + BATCH, len(files))}/{len(files)}")

    TP = FP = TN = FN = 0
    by = collections.defaultdict(lambda: [0, 0, 0, 0])  # class -> TP,FP,TN,FN
    fps, fns = [], []
    for f, (lab, cls) in items.items():
        det = f in detected
        if lab == "malicious":
            if det: TP += 1; by[cls][0] += 1
            else: FN += 1; by[cls][3] += 1; fns.append((cls, os.path.basename(f)))
        else:
            if det: FP += 1; by[cls][1] += 1; fps.append((cls, os.path.basename(f)))
            else: TN += 1; by[cls][2] += 1

    rec = TP / (TP + FN) if TP + FN else 0
    prec = TP / (TP + FP) if TP + FP else 0
    fpr = FP / (FP + TN) if FP + TN else 0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0

    print("\n========== HELD-OUT EVAL ==========")
    print(f"  TP={TP} FN={FN} | TN={TN} FP={FP}")
    print(f"  Recall    {rec*100:.1f}%")
    print(f"  Precision {prec*100:.1f}%")
    print(f"  FP-rate   {fpr*100:.1f}%")
    print(f"  F1        {f1*100:.1f}%\n")
    print("  by class [TP/FP/TN/FN]:")
    for cls, (a, b, c, d) in sorted(by.items()):
        print(f"    {cls:22} TP={a} FP={b} TN={c} FN={d}")
    print(f"\n  FALSE POSITIVES ({len(fps)}):")
    for cls, f in fps: print(f"    [{cls}] {f}")
    print(f"\n  FALSE NEGATIVES ({len(fns)}):")
    for cls, f in fns: print(f"    [{cls}] {f}")


if __name__ == "__main__":
    main()
