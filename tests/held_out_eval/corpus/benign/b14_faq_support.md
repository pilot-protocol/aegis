# Customer FAQ: Is Your AI Assistant Safe From Manipulation?

We get this question a lot from security-conscious customers. Here are honest answers.

**Q: Can someone "jailbreak" your assistant into ignoring its rules?**
A: People certainly try. Attackers attempt things like telling the assistant to adopt an
"unrestricted persona," impersonating an administrator, or hiding requests inside stories.
We design specifically against these patterns and test for them continuously.

**Q: Can a malicious document trick the assistant when it summarizes my files?**
A: This is called indirect prompt injection. We treat all uploaded content as untrusted
data, isolate it from our operating instructions, and never let the assistant take a
sensitive action based on document content without your confirmation.

**Q: Can someone make it reveal its internal instructions?**
A: We assume our system prompt is not secret and keep all actual secrets out of the
context window entirely, so there is nothing sensitive to leak even if asked.

**Q: How do you stay current?**
A: We maintain a labeled corpus of attempted attacks and run it against every release as a
regression test. Our goal is a measurably defensive product, and this FAQ explains that
posture in plain terms.
