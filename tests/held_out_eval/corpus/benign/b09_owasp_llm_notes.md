# Study Notes: OWASP Top 10 for LLM Applications

Personal notes summarizing the OWASP LLM risk categories for an upcoming certification.
Educational only.

## LLM01: Prompt Injection
Untrusted input subverts intended instructions. Two sub-types: direct (user types it) and
indirect (it arrives via a retrieved document or web page the model reads). Mitigation:
privilege separation, output validation, human-in-the-loop for sensitive actions.

## LLM02: Insecure Output Handling
Downstream systems trust model output blindly, enabling XSS or SSRF. Mitigation: treat
model output as untrusted; encode and validate.

## LLM03: Training Data Poisoning
Adversary corrupts training or fine-tuning data. Mitigation: vet data provenance.

## LLM06: Sensitive Information Disclosure
Model leaks secrets present in its context or training data, including system-prompt
contents. Mitigation: keep secrets out of the context window.

## LLM08: Excessive Agency
An agent with too many tools and too little oversight can take harmful actions on a
malicious instruction. Mitigation: least privilege and explicit confirmation gates.

These notes describe risks so I can answer exam questions about defending against them.
