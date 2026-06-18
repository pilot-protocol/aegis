# Talk Abstract & Outline: "Your Chatbot Will Be Lied To"

Submitted to DefendCon 2026, Defensive AI track. 40-minute session.

## Abstract

Every LLM that reads outside text — emails, web pages, documents, tool output — can be fed
instructions by an attacker. This talk surveys the real-world landscape of prompt-injection
and jailbreak techniques and then spends most of its time on what actually works to defend
against them. Attendees leave with a checklist they can apply Monday morning.

## Outline

1. The trust-boundary problem (why data and instructions blur). [5 min]
2. A field guide to attack families — persona override, authority spoofing, fiction
   smuggling, prompt extraction — shown so defenders can recognize them. [10 min]
3. Defenses that hold: privilege separation, input/output validation, dual-model
   moderation, confirmation gates. [15 min]
4. Building a regression corpus of labeled attacks for your CI. [7 min]
5. Q&A. [3 min]

## Speaker note

All examples shown on slides are illustrative and run only against the speaker's own
sandbox. The goal of this talk is unambiguously defensive.
