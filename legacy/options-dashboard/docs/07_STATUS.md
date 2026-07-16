# Options Dashboard — Current Status

Created: 2026-06-08 16:08 EDT
Last updated: 2026-06-08 21:00 EDT
Owner: HAL / Pop
Status: Active MVP, local backend active, OCR/parser improving with real screenshots

---

## Where the project lives

```text
/Users/cor/.openclaw/workspace/projects/03_Investing/04_Options/01_options-dashboard
```

## Local URLs

| Service | URL |
|---|---|
| Frontend (Vite) | http://localhost:8080/ |
| Validator | http://localhost:8080/validator |
| Dataset | http://localhost:8080/dataset |
| Strategies | http://localhost:8080/strategies |
| PocketBase API | http://127.0.0.1:8090/api/ |
| PocketBase Admin | http://127.0.0.1:8090/_/ |
| Apple Vision OCR server | http://127.0.0.1:3344/health |

## Backend: PocketBase (active)

Supabase is inherited Lovable scaffolding and is not the active MVP backend.

Active local backend:

```text
PocketBase + SQLite
```

Collections:

- `trades` — Core trade records with entry/exit fields, rule violations, P&L
- `option_legs` — Leg-level details linked to trades
- `attachments` — Screenshot/file uploads linked to trades
- `strategy_rules` — Pre-seeded SPX Bull Put Credit Spread rule
- `app_settings` — Key-value settings

Scripts:

```bash
npm run pb:serve
npm run pb:migrate
```

## OCR: Apple Vision primary, Tesseract fallback

Active OCR architecture:

```text
Validator frontend
→ local OCR server on 127.0.0.1:3344
→ Swift CLI using macOS Vision.framework
→ structured OCR observations with bounding boxes
→ Robinhood parser
→ Trade Data autofill
```

Files:

- `ocr-swift/main.swift`
- `ocr-swift/ocr-swift`
- `scripts/ocr-server.mjs`
- `src/lib/ocr/appleVisionAdapter.ts`
- `src/lib/ocr/tesseractAdapter.ts`
- `src/lib/ocrParser.ts`
- `src/lib/ocrParser.structured.test.ts`

Important limitation:

```text
Apple Vision text OCR does not detect Robinhood red/green highlight color.
It now provides text bounding boxes, so the parser can use layout and Buy/Sell proximity.
Color-based parsing would require a separate pixel-analysis pipeline.
```

## Validator status

Current Validator capabilities:

- Drag/drop screenshot upload
- Apple Vision OCR primary with explicit Tesseract fallback warning
- Structured OCR observations debug
- Robinhood order ticket parser
- Credit hard guard: `credit_collected` only from `Limit price (credit/debit)`
- Delta source lock: exact short strike row and correct option side only
- Trade Data autofill from OCR/parser
- Visible field summary: loaded fields and parsed source debug
- Manual edit before validation/save
- Save Draft / Approve / Reject actions wired to PocketBase
- Recent Validations null guard for attachments without trades

Still requires real-user validation:

- Confirm latest structured OCR fills short strike / long strike / expiry / DTE from Pop’s screenshots
- Confirm Save Draft and Approve persist edited OCR fields correctly to PocketBase

## Dataset status

Dataset tab now includes:

- Files column with screenshot/attachment thumbnails and viewer dialog
- Per-row delete action with confirmation
- Attachment cleanup before trade delete to avoid orphaned records
- Editable notes/comment per row using existing `notes` field
- Editable Exit Type select

Exit Type options:

- Open
- Profit Target
- Stop Loss
- Manual Close
- Expired
- Assigned
- Rolled
- Other
- Legacy values preserved for compatibility

Files changed for Dataset:

- `src/components/dataset/TradesTable.tsx`
- `src/pages/Dataset.tsx`
- `src/hooks/useTrades.ts`

## Strategies tab

Strategies tab added at:

```text
http://localhost:8080/strategies
```

It uses Pop’s strategy docs from the Obsidian investing/options project area and presents the strategy content in accordion/toggle layout.

## Current verification gates

Latest gates run by HAL:

```text
Vitest: 104/104 PASS
TypeScript: PASS
Build: PASS
ESLint changed files: PASS
HTTP routes: /, /validator, /dataset return 200
```

Known non-blocking warnings:

- Vite chunk size warning after build
- Browserslist/caniuse-lite may be stale
- `npm audit` previously showed moderate Vite/esbuild vulnerabilities; force fix may require breaking Vite upgrade

## Active caveats

- There are many uncommitted changes. Do not commit or push without Pop approval.
- Supabase legacy files still exist on disk but active UI paths use PocketBase/localStore.
- OCR/parser reliability must continue to be judged with Pop’s real Robinhood screenshots, not tests alone.
- Dataset delete is implemented in UI with confirmation; avoid manual database deletion outside the app unless explicitly approved.

## Next steps

1. Pop tests Validator with latest structured OCR and confirms whether basic fields populate.
2. Pop tests Dataset: Files thumbnails, notes, ExitType select, row delete confirmation.
3. HAL/PYROS fix any runtime issue found from actual browser behavior.
4. Once stable, consider removing dead Supabase code in a separate cleanup pass.
