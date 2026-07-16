# Options Dashboard — Change Review

Created: 2026-06-08 21:03 EDT
Last updated: 2026-06-08 21:03 EDT
Owner: HAL
Status: Reviewed, pending Pop runtime confirmation

---

## Scope reviewed

This review covers the current Options Dashboard changes after the PocketBase migration, Apple Vision OCR implementation, Validator parser improvements, Strategies tab, and Dataset usability updates.

Project path:

```text
/Users/cor/.openclaw/workspace/projects/03_Investing/04_Options/01_options-dashboard
```

## Technical gates run

```text
npx vitest run: 104/104 PASS
npx tsc --noEmit: PASS
npm run build: PASS
npx eslint changed files: PASS
HTTP /: 200
HTTP /validator: 200
HTTP /dataset: 200
```

Build warnings are non-blocking:

- Vite chunk size warning
- Browserslist/caniuse-lite stale warning

## Backend review

PocketBase is now the active MVP backend. Active hooks route through PocketBase/localStore helpers rather than direct Supabase calls.

Reviewed areas:

- `src/hooks/useTrades.ts`
- `src/hooks/useSettings.ts`
- `src/integrations/pocketbase/client.ts`
- `src/lib/localStore.ts`
- `pocketbase/pb_migrations/1780951833_init_options_schema.js`

Assessment:

```text
PASS_WITH_CAVEATS
```

Caveats:

- Supabase legacy scaffolding remains on disk.
- There are many uncommitted changes.
- No commit/push should happen without Pop approval.

## Validator review

Validator now uses Apple Vision OCR as primary with Tesseract fallback. It supports structured OCR observations with bounding boxes, field-source locking, Trade Data autofill, and manual correction before saving.

Reviewed areas:

- `src/pages/Validator.tsx`
- `src/lib/ocrParser.ts`
- `src/lib/ocrParser.structured.test.ts`
- `src/lib/ocr/appleVisionAdapter.ts`
- `scripts/ocr-server.mjs`
- `ocr-swift/main.swift`

Assessment:

```text
PASS_WITH_RUNTIME_CAVEATS
```

Caveats:

- Tests pass, but OCR/parser correctness must still be judged against Pop’s real Robinhood screenshots.
- Apple Vision OCR does not detect red/green highlight color. It now uses text bounding boxes and layout proximity instead.
- Delta extraction remains intentionally conservative: exact short-strike row and correct option side only.

## Dataset review

Dataset tab now includes:

- Files column with attachment thumbnails and viewer dialog
- Per-row delete with confirmation
- Related attachment cleanup before trade delete
- Editable notes/comments
- Editable ExitType select with expanded options

Reviewed areas:

- `src/components/dataset/TradesTable.tsx`
- `src/pages/Dataset.tsx`
- `src/hooks/useTrades.ts`

Assessment:

```text
PASS_WITH_RUNTIME_CAVEATS
```

Caveats:

- Delete action is implemented with confirmation, but Pop should test with non-critical local rows first.
- Attachment cleanup deletes attachment records before trade delete to avoid orphan records.
- No schema migration was needed because `notes` and `exit_type` already exist.

## Strategies tab review

Strategies tab is added and route is active.

Reviewed areas:

- `src/pages/Strategies.tsx`
- `src/components/layout/Sidebar.tsx`
- `src/App.tsx`

Assessment:

```text
PASS
```

## Main risks

1. OCR/parser reliability still depends on the quality/layout of Robinhood screenshots.
2. Dataset delete is destructive at app-data level, although protected by confirmation.
3. Large uncommitted diff makes rollback harder unless a clean checkpoint is created later.
4. Legacy Supabase files may confuse future maintenance if not cleaned in a separate pass.

## Recommended next actions

1. Pop tests Validator again with the same screenshots and checks:
   - Trade Data loaded fields
   - Structured OCR observations
   - short/long strikes
   - expiry/DTE
   - credit from `Limit price (credit)` only
2. Pop tests Dataset using a non-critical trade:
   - Files column thumbnails
   - Notes edit/save
   - ExitType select/save
   - Delete confirmation
3. If runtime behavior passes, create a clean checkpoint commit only after Pop approval.
4. Schedule a separate cleanup pass for dead Supabase scaffolding.
