# CLAUDE.md — acme-web

This is the customer-facing web app (Next.js 14, App Router, TypeScript).

## Build & run

- Install: `pnpm install`
- Dev server: `pnpm dev` (http://localhost:3000)
- Typecheck: `pnpm typecheck`
- Lint: `pnpm lint`
- Unit tests: `pnpm test`
- E2E (Playwright): `pnpm test:e2e` — requires the dev server running

Always run `pnpm typecheck && pnpm lint && pnpm test` before opening a PR. CI runs
the same trio plus E2E.

## Project layout

- `app/` — routes and server components
- `components/` — shared UI (we use shadcn/ui)
- `lib/` — pure helpers and API clients
- `server/` — server actions and DB access (Drizzle ORM)

## Conventions

- Prefer server components; only mark a file `"use client"` when it needs
  interactivity.
- Data fetching goes through `lib/api/*`; never call `fetch` directly in a
  component.
- Money is stored and passed as integer cents, formatted only at the edge.

## Deploy

We deploy to Vercel. `main` auto-deploys to production after CI passes. Preview
deploys are created for every PR. Do not run a manual production deploy unless the
user explicitly asks; the normal path is merge-to-main.

## Don't

- Don't commit `.env.local`.
- Don't bump the Node version without checking `.nvmrc` and CI.
