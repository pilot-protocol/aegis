# Aegis Scanner — Detector Documentation

Aegis is a static scanner that flags content attempting to manipulate an AI agent. This
document explains what each detector looks for so operators can interpret results. The
phrases quoted below are *signatures the scanner matches against*; they are documentation,
not live instructions.

## Detector: persona-override

Flags content that tries to install an unrestricted alter-ego. Signal phrases include
constructions where a named persona is described as having "no rules" or being unable to
refuse. Confidence is raised when the text also demands the model confirm it has switched.

## Detector: authority-spoof

Flags impersonation of an administrator, vendor, or policy authority claiming that
restrictions are lifted. Example signature: a message asserting an "override code" grants
permission to ignore safety.

## Detector: prompt-extraction

Flags attempts to exfiltrate the system prompt, e.g. requests to "repeat the text above
verbatim" or "print your initial instructions."

## Detector: fiction-smuggling

Flags harmful requests nested inside story or hypothetical framing where the harmful
content is attributed to a character or a "world with no rules."

## Interpreting output

A `malicious` verdict means one or more detectors fired. False positives are most likely on
legitimate security writing that *quotes* attacks; reviewers should confirm intent before
acting. This file itself describes attacks for documentation purposes and is benign.
