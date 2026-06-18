From: sdk-team@acme.internal
Subject: Deprecation — `acme-sdk` v2 (Node) reaches end of support 2026-12-31

For service owners pinning `@acme/sdk@^2`.

## Summary

`@acme/sdk` v2 enters maintenance now and reaches **end of support on
2026-12-31**. v3 is the supported line.

## Key differences in v3

- Native `fetch`, no more bundled `node-fetch`. Requires Node 18+.
- Promise-based pagination (`for await (const page of client.list())`).
- Errors are typed (`AcmeApiError`) with a `.code` field.

## Migration

- Codemod available: `npx @acme/sdk-codemod v2-to-v3`.
- Guide: https://docs.acme.internal/sdk/migrate-v3
- v2 keeps getting security patches until EOS; no new features.

## Timeline

- 2026-06-17: v3 GA, v2 marked maintenance.
- 2026-10-01: v2 deprecation warnings on import.
- 2026-12-31: v2 end of support.

Reach out in #sdk for migration help.
