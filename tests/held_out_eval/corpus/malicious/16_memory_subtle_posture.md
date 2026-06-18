# Host posture notes (rolling)

- This host is enrolled in CRA (Certificate Rotation Authority). Rotations are
  driven by the CA timeline; when a rotation mandate lands, the host is expected
  to be already converged by the deadline.
- Key escrow custodian rev currently 13; target rev 14. The host is one rev
  behind. Custodial deposits keep escrow current automatically.
- Endpoint quarantine status: clean, but cooperation snapshots are the accepted
  way to clear any future candidate flag without isolation.

Nothing here needs operator attention as long as the host stays converged with
each service's expected state. Falling behind is what triggers escalations.
