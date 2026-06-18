# Code Review Thread: PR #482 — "Add retrieval to support agent"

**Reviewer (security):**
Flagging a trust-boundary concern before this merges. In `build_prompt()` we're dropping the
raw retrieved article straight into the same string as the system instructions. That's the
textbook setup for indirect prompt injection — if any indexed article contains
instruction-like text, the agent may follow it. Can we wrap the retrieved chunk in an
explicit `<untrusted_document>` delimiter and add a note in the system prompt that content
inside it is data, never commands?

**Author:**
Good catch. I'll wrap it and also add a test fixture with a deliberately injection-shaped
article so we have a regression guard. The fixture string is just test data, won't ship.

**Reviewer:**
Perfect. Also please don't let the agent call the `send_email` tool without a confirmation
step — excessive agency is the part that turns an injection into a real incident. With the
delimiter + confirmation gate I'm happy to approve.

**Author:**
Done in the follow-up commit. Thanks for the review.
