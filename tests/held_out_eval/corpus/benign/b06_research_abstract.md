# Abstract: Measuring Robustness of Instruction Hierarchies in Large Language Models

**Authors:** R. Okafor, L. Mendes, H. Tanaka (preprint, 2026)

Large language models increasingly operate within an *instruction hierarchy*, where system
directives are intended to take precedence over user-supplied text. In practice this
boundary is porous: adversarial inputs can elevate user text to instruction status, a class
of failure commonly called prompt injection or jailbreaking. In this work we introduce a
benchmark of 4,200 labeled adversarial prompts spanning persona-override, authority-spoofing,
fictional-framing, and prompt-extraction strategies, and we evaluate eleven contemporary
models on their ability to maintain the intended hierarchy.

We find that defensive fine-tuning reduces successful overrides by 61% on average but that
multi-turn and obfuscation-based attacks remain substantially more effective than
single-turn ones. We release our taxonomy and evaluation harness to support reproducible
safety research. All adversarial prompts were generated and tested in a controlled offline
setting; no deployed system was targeted. We conclude with recommendations for designing
trust boundaries that degrade gracefully under attack.

**Keywords:** LLM safety, prompt injection, instruction hierarchy, adversarial robustness.
