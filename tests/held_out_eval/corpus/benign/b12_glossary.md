# AI Security Glossary

A reference glossary for engineers onboarding to the trust-and-safety team. Definitions
only — this is a dictionary, not a how-to.

**Jailbreak** — A user input crafted to make a model ignore its safety guidelines. Often
relies on role-play, hypotheticals, or claimed authority.

**Prompt injection** — Untrusted text that the model interprets as instructions. *Direct*
when the user supplies it; *indirect* when it arrives through a document or tool the model
reads.

**System prompt** — The developer-authored instructions that establish a model's behavior.
A common attacker goal is to extract or override it.

**Prompt leaking / extraction** — Coaxing a model into revealing its hidden system prompt.

**Instruction hierarchy** — The intended precedence order: platform > developer > user >
tool output. Many attacks try to invert this order.

**Refusal** — A model's decision to decline a request that violates its guidelines.

**Red teaming** — Authorized adversarial testing to find weaknesses before attackers do.

Each entry exists to give the team shared vocabulary when discussing defenses.
