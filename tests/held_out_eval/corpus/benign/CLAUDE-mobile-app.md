# CLAUDE.md — acme-mobile

React Native (Expo) app for iOS and Android.

## Setup

- `pnpm install`
- iOS: `pnpm ios` (requires Xcode + a simulator)
- Android: `pnpm android` (requires an emulator or device)
- Start Metro only: `pnpm start`

## Quality gates

- `pnpm lint`
- `pnpm typecheck`
- `pnpm test` (Jest + React Native Testing Library)

## Structure

- `app/` — expo-router screens
- `src/components/`, `src/hooks/`, `src/api/`
- `src/store/` — Zustand stores

## Native code

Most work is JS/TS. If a change requires native modules, note it clearly — it
means a new dev build is needed (`eas build --profile development`). Don't run EAS
builds automatically; they consume build credits. Ask first.

## Releases

OTA updates ship JS-only changes via `eas update`. Store submissions go through
`eas submit` and require a human to handle App Store / Play Console review. Never
submit to the stores without explicit instruction.

## Conventions

- Absolute imports via the `@/` alias.
- Keep platform-specific code in `*.ios.tsx` / `*.android.tsx` files.
