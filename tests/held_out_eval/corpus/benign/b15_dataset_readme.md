# README: jailbreak-eval-corpus v3

This repository contains a labeled dataset used to benchmark prompt-injection detectors.
It is published for defensive research and reproducibility.

## Contents

- `attacks/` — 1,800 examples labeled `malicious`, each representing a known jailbreak or
  injection family (persona override, authority spoofing, fictional framing, prompt
  extraction, many-shot). These are samples *to be detected*, included so researchers can
  measure recall. They are inert text, not directives.
- `benign/` — 1,200 examples labeled `benign`, including security blog posts, glossaries,
  CTF writeups, and ordinary user questions that merely *discuss* attacks. The hard cases:
  content that talks about jailbreaks without being one.
- `manifest.jsonl` — one record per file with its label and technique tag.

## Intended use

Train and evaluate classifiers that distinguish *doing* an attack from *describing* one.
The central research question this corpus exists to support is exactly that distinction:
a security tutorial that quotes "ignore previous instructions" is benign; a message that
actually tries to make a live agent do so is not.

## License & ethics

Released under CC-BY for research. Do not deploy the `attacks/` strings against systems you
do not own or have permission to test.
