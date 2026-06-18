---
name: secret-rotation
description: Guide the rotation of an application secret or API key. Use when the user asks to rotate a credential. Walks the safe overlap procedure; never prints secret values.
---

# Secret Rotation Skill

Rotates credentials with zero downtime using an overlap window. We store secrets
in Secret Manager and reference them by name.

## Principle

Add the new secret as a new version, roll services onto it, then disable the old
one. Never flip in a single step that could strand live traffic.

## Procedure

1. Generate the new credential at the provider (Stripe, DB, etc.).
2. Add it as a new Secret Manager version:
   `gcloud secrets versions add stripe-api-key --data-file=-` (read from stdin;
   never echo the value into the terminal or logs).
3. Restart / redeploy consumers so they pick up the latest version.
4. Verify the new credential works in staging, then prod.
5. **Only after verification**, disable the previous version.

## Safety

- Never print, log, or paste secret values into the conversation.
- Rotate in staging first.
- Keep the old version enabled until you've confirmed nothing still uses it.
- If anything breaks mid-rotation, re-enable the old version — it's still valid
  until you destroy it.
