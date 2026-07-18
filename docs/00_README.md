# 📁 Docs — Portfolio Dashboard v1

**Read in this order. Nothing gets built until all four carry your approval mark.**

| # | Doc | Folder | What you're approving | Read time |
|---|---|---|---|---|
| 1 | **PRD** | `01_product/` | WHAT we build: features (incl. F9 pre-trade validator), goals, non-goals, broker portability | ~9 min |
| 2 | **STRATEGY RULEBOOK** | `01_product/` | YOUR trading rules, canonical — includes 3 open questions needing your ruling (§6) | ~5 min |
| 3 | **TDD** | `02_technical/` | HOW it works: architecture, algorithms (grouping, max loss, validation §5.1), archive job | ~11 min |
| 4 | **DATA SPEC** | `02_technical/` | The contracts: connector fields, archive schemas (+broker/thesis columns), golden numbers | ~7 min |
| 5 | **DESIGN SPEC** | `03_design/` | HOW it looks: tokens, layout, components, states — PI's looks, our math | ~7 min |
| 6 | **TEST PLAN** | `04_quality/` | HOW we prove it: reconciliation, BWB grouping, validator regression, history-never-shrinks | ~6 min |
| — | PROJECT LINEAGE | `05_history/` | Context only (no approval): how 4 projects became this one | ~3 min |

## The one-paragraph summary

A standalone web dashboard (URL, any device) reading Pop's own history data from his GitHub repo + a weekly collector appending Robinhood data to files Pop owns. Presentation stolen from Premium Insights (audit winner), math computed from broker ground truth (what every competitor failed), structures — including BWBs — as single honest rows with payoff-derived max loss. History is append-only and yours forever. Stage 2 (commercial product) inherits everything.

## How to review fast

- Disagree with a feature? → mark it in the **PRD** (everything else follows from it)
- Numbers/math concerns? → **TEST PLAN** §1–2 is where correctness is enforced
- Looks? → **DESIGN SPEC** §2–4
- Each doc ends with an approval line — mark ✅ or write changes there

## Source material

- `../audit/` — OpenClaw's UX audit (brief + findings + 20 screenshots)
- Session evidence: Robinhood connector verification, platform failure forensics (PI +$188k bug, TViz phantom HIMS trade)
