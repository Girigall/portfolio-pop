# 📁 Docs — Portfolio Dashboard v1

**Read in this order. Nothing gets built until all four carry your approval mark.**

| # | Doc | Folder | What you're approving | Read time |
|---|---|---|---|---|
| 1 | **PRD** | `01_product/` | WHAT we build: features, goals, non-goals, correctness rules | ~8 min |
| 2 | **TDD** | `02_technical/` | HOW it works: architecture, algorithms (grouping, max loss), archive job | ~10 min |
| 3 | **DATA SPEC** | `02_technical/` | The contracts: connector fields, archive file schemas, golden numbers | ~7 min |
| 4 | **DESIGN SPEC** | `03_design/` | HOW it looks: tokens, layout, components, states — PI's looks, our math | ~7 min |
| 5 | **TEST PLAN** | `04_quality/` | HOW we prove it: reconciliation to the cent, BWB grouping, history-never-shrinks | ~5 min |

## The one-paragraph summary

A Cowork dashboard reading live Robinhood data + a weekly archive job writing permanent history to your Drive. Presentation stolen from Premium Insights (audit winner), math computed from broker ground truth (what every competitor failed), structures — including BWBs — as single honest rows with payoff-derived max loss. History is append-only and yours forever. Stage 2 (commercial product) inherits everything.

## How to review fast

- Disagree with a feature? → mark it in the **PRD** (everything else follows from it)
- Numbers/math concerns? → **TEST PLAN** §1–2 is where correctness is enforced
- Looks? → **DESIGN SPEC** §2–4
- Each doc ends with an approval line — mark ✅ or write changes there

## Source material

- `../audit/` — OpenClaw's UX audit (brief + findings + 20 screenshots)
- Session evidence: Robinhood connector verification, platform failure forensics (PI +$188k bug, TViz phantom HIMS trade)
