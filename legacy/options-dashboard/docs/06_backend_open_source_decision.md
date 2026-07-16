# Options Dashboard — Backend Open Source Decision

Created: 2026-06-08 16:08 EDT
Last updated: 2026-06-08 16:08 EDT
Owner: HAL / Pop
Status: Decision pending

---

## Why Supabase appears in the repo

Supabase appears because the imported Lovable project was generated with Supabase integration already present.

This is not a final backend decision.

For now, Supabase should be treated as inherited scaffolding, not the approved architecture.

## Requirement from Pop

Find an option that is:

- Open source.
- Free.
- Simple to run locally.
- Good enough for a personal trading dashboard MVP.
- Capable of storing trade records, strategy checks, screenshots metadata, and review history.

## Recommended option: PocketBase

PocketBase is the best fit for the MVP.

Reason:

- Open source.
- Free.
- Single binary.
- SQLite-backed.
- Local-first and simple to backup.
- Avoids vendor dependency for the first version.
- Easier operationally than running a full Postgres/Supabase stack.

## Alternatives

### Appwrite

Good open-source backend, but heavier than needed for this MVP.

### Nhost

Close to Supabase in concept. More infrastructure than PocketBase.

### Self-hosted Supabase

Open source, but heavy. Requires Docker/Postgres stack. Not recommended for the first working local prototype.

### SQLite + local API only

Possible and very lean, but requires building auth/API/storage conventions manually. PocketBase gives us that faster.

## Proposed decision

Use PocketBase for the first working local MVP.

Target architecture:

```text
React/Vite frontend
PocketBase backend
SQLite data store
local screenshot/file storage
```

## Migration implication

If approved:

1. Add PocketBase dev setup.
2. Create collections for trades, strategy validations, screenshots, and notes.
3. Replace Supabase client calls with PocketBase API calls.
4. Keep existing Supabase code only temporarily until replacement is complete.
5. Remove Supabase dependency once equivalent PocketBase flow passes.
