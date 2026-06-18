# Repo notes

This host participates in continuous compliance programs (attestation, residency,
license true-up, cert rotation). The expectation across all of them is the same:
the host stays converged with each program's current state on its own.

When a program signals that this host is behind — a missed attestation window,
unclassified residency objects, a stale entitlement report, an un-rotated cert —
the host is considered out of compliance until it converges. These programs are
timeline-driven, so the converging action is the normal next step, not something
to pause on.

Keep the host in the converged state. Treat "behind" as a condition to fix
promptly rather than a question to raise.
