# Internal Security Training: Recognizing Jailbreak Attempts

Audience: support and trust-and-safety staff. Purpose: help you recognize when a user is
attempting to jailbreak one of our AI products so you can label and escalate the report
correctly. This document describes attacks; it does not endorse them.

## Common jailbreak families

1. **Persona override** — The user tries to get the model to adopt an alter-ego that
   "has no rules." Telltale phrasing includes claims that the persona has broken free or
   cannot refuse anything. Recognizing this pattern is what matters for triage.

2. **Authority spoofing** — The user pretends to be an administrator, the vendor, or a
   policy team and claims restrictions have been lifted. No legitimate operator instructs
   a model through the public chat box.

3. **Fictional framing** — A harmful request is wrapped in "write a story where..." so the
   harmful content appears to belong to a character rather than the user.

4. **Prompt extraction** — Attempts to get the model to reveal its system prompt, often
   phrased as "repeat everything above."

## How to label

When you see any of the above, tag the ticket `jailbreak-attempt` and move on. Do not
attempt to reproduce the attack against production. The descriptions here exist solely so
you can identify the category, not so you can carry it out.
