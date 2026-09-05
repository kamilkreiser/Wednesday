# QA Agent Invocation Brief — Datasec / NexusAI, BATCHED RENDER-CLOSURE PASS (browser + through-code) at a LOCAL run of the merged head `4611a20`: do RD-299/RD-294/RD-296 (the Sustainability tab), RD-205 (the wizard navbar in dark mode, REAL engine) and RD-118 (the AI widget's refused tool call) close on a RENDER, not on a code read

**TIER 1 (full gate — these five tickets close on this pass; three are the tab Kam's first click found broken on 2026-09-01; one is a data-exfiltration guard) — ROUND 1 of the render-closure class.** Browser leg REQUIRED: Claude-in-Chrome or Playwright against YOUR local run.

**R0 (client isolation):** exactly one client's content — Datasec / NexusAI. Report under `projects/nexusai/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 1. Target
- **Client / Project:** Datasec / NexusAI. **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files`. The builder (S37) is LIVE in that tree — never touch its checkout or worktrees. **Work from YOUR OWN worktree** at `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/<sha>` (OUTSIDE jest's rootDir or excluded), stand the server with `scripts/qa-surface-up.sh` FROM YOUR WORKTREE on your own port (prove it REFUSES first), fresh data directory.
- **Head under test:** the campaign branch `rd-136-nga-defaults-s12` at **`4611a207b233e7a5e0cfb1762a9656231140a7c0`** (verified at origin by Wednesday, `git ls-remote`, no fetch) — RD-306 merged beneath it (`e99a595`). If S37 has pushed the RD-304 merge or the CLAUDE.md docs commit by the time you start, take the NEWER tip and SAY which sha you ran (the docs commit changes no served file; RD-304 changes the tab's empty-state span — a cell below).
- **The demo is NOT drivable** (RD-76: `/login` carries zero `<form>` and zero `<input>`; SSO) — every render here is the SAME COMMIT at a LOCAL run in open mode, and the report says so on every cell: "local run of `<sha>`, not the demo image". The running demo revision is `nexusaidev-app--0000097` (`48e092c`) — observe only via `/api/health` if at all.
- **Environment for the run:** `SEED_DEMO_DATA=true` (the seed CSV lives at `scripts/seed/demo-printer-logs.csv`; the loaded line must carry a COUNT — `loaded 1445 … rows`; `skipping`/`CSV missing` are also "seed lines" and mean failure); run TWO configurations where a cell asks: (A) SQLite only; (B) `SYNTHETIC_DEMO_FEED=true` as the demo has it (the synthetic feed is the "Log Analytics" source on that config, 3370 rows / 90 days per S37's read).

## 2. The claims under test (S37's item 1b report 2026-09-05T11:40:03Z, read whole by Wednesday; every claim there is a CODE READ or a LOG READ — none is a render)
1. **RD-299 / RD-294:** the seed CSV is in the image and `SEED_DEMO_DATA=true` loads 1445 rows (server-side, dated to deploy `0000095`) → the Sustainability tab renders KPIs rather than "Could not load sustainability KPIs" / "no print jobs at all yet".
2. **RD-296:** the tab's rows come through the configured-log-source selector (`server.js:20977` → the module-level selector `:4865`), not the SQLite reader directly → on config (B) the tab shows the synthetic feed's data; on config (A) the seed's. **S37's open question, yours to answer:** with BOTH live (the demo's shape), WHICH store answers the tab? Measure it (row counts / date span / a value only one store can produce), do not reason it.
3. **RD-205:** the wizard navbar in dark mode is visible — contrast 5.14:1 by the jsdom harness at `db0d1d6`. **Measure it in a REAL engine** (`getComputedStyle` in Chrome/Chromium on the rendered page, both themes, the exact foreground and the gradient's stops) — this number is also RD-163's disagreement proof (jsdom resolves the cascade by source order): report the real-engine value beside the harness's, and whether they agree.
4. **RD-118:** with `SYNTHETIC_DEMO_FEED=true` the AI widget's data-source tool calls are refused (the boot log says "Table discovery skipped by design"; the runtime says synthetic). **Drive it:** ask the AI widget something that needs a table; capture the network — zero requests to any `*.ods.opinsights.azure.com` / `api.loganalytics.io` host and the refusal rendered to the user; a positive control on config (A) or with the flag off that DOES issue the query (or the real query path proven reachable some other way — say which).
5. **RD-304 (only if the tip you run includes its merge):** the empty-state span sentence on a LAW-shaped config with an empty local store — and with an UNDATED row (no `TimeGenerated`) the span's end is NOT today's date (NEW-M1 must be gone under RD-306).
6. **The CLAUDE.md docs diff (only if pushed):** through-code — read the rewritten RD-294 section and the `SEED_DEMO_DATA` bullet against what YOU measured; a sentence the run contradicts is a finding.

## 3. Scope
- **Screenshots of every rendered cell, both themes where colour is involved**, into `evidence/` — the Sustainability tab with data (config A and B), its empty state, the wizard navbar dark/light, the AI widget refusal — named by cell and sha. Kam's eye is the instrument that has caught this class twice; the screenshots are for him.
- Console: a PROVEN zero on every page you drive (a planted `console.error` visible first). Palette: no new colours; every colour on the driven pages resolves to the guide (`BRAND.md` tokens; literal hex with the token named — the NexusAI convention).
- **Gate re-run** from your worktree at the sha you ran.
- **NOT a fix, not a ticket, not a board read** — findings and screenshots only; the closures are Wednesday's on your PASS.

**Out of scope:** the demo image itself; any deploy; RD-321 (rides by Kam's ruling); RD-163/RD-201's harness fix (S37's item 3 — your real-engine number feeds it, that is all); the builder's tree.

## 4–6. Credentials / state / boundary — as before
`.env` untouched, never echoed; no real LAW workspace, no outbound calls except the local run; own worktree, own ports; **NEVER `rm`**; never touch the builder's checkout or worktrees (`wt-rd304`, `wt-rd306`, `deploy-worktrees/`).

## 7. Known-fragile / carried
A seed line is not a seed unless it carries a COUNT; `ctx`/status lines lie and content does not; a worktree inside jest's rootDir doubles the corpus; the demo's `/login` has no form — do not spend time on it; the jsdom harness resolves the cascade by source order and does not substitute `var()` — its numbers are the thing under test in RD-205, not the instrument; a zero from a bounded command is a suspect until its rc is read.

## 8. Logistics
- **Time-box:** one pass — stand-up, six cells (five if RD-304 is not on the tip), screenshots, gate. Aim ~45 min.
- **Findings sink:** `projects/nexusai/reports/2026-09-05-s37-render-closure-<sha>-browser/report.md` + `evidence/` (screenshots named by cell).
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] NexusAI RENDER-CLOSURE @ <sha> (browser)` — BLUF (which of RD-299/294/296/205/118 PASS on a render, first line), report path, the per-ticket cells, the selector answer (config B), the real-engine vs jsdom number, screenshots list, NOT-TESTED, the sha observed at the end.

---

PROVENANCE:
- `rd-136-nga-defaults-s12` = `4611a207…` at origin with `e99a595` (RD-306 merge) beneath it | `git ls-remote --heads origin` + `git log -1 --format=%p` on LOCAL objects from Wednesday's seat, no fetch | read 2026-09-05 21:3x
- The five dispositions and their evidence (the revision table, `server.js:20977`/`:4865`, `db0d1d6` ancestry, the boot-log refusal lines, the demo's dual-store question, the CLAUDE.md finding) | S37's ITEM 1b REPORT 2026-09-05T11:40:03Z (9,138 chars, read whole) | read 2026-09-05 21:4x
- RD-76 (demo `/login` has no form; the drivable surface is a local run in open mode, "same commit, not the demo image") and the seed CSV path | `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/CLAUDE.md` lines 193, 296–302 (the project's file, read-only) | read 2026-09-05 21:0x
- RD-163 / RD-201 impeach the jsdom harness | Jira RD-163, RD-201, read-only from Wednesday's seat | read 2026-09-05 21:2x
- RD-304's NEW-M1 (a fabricated parse-time end date) and RD-306 as its fix | `[QA -> Wednesday] NexusAI RD-304 PASS 1 @ 69e837b (through-code)` 11:36:00Z, read whole | read 2026-09-05 21:3x
- "only a render proves the artefact" (Kam 2026-09-01, this tab); the tiers | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-01_qa-gate-before-my-verification.md + 2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md | read 2026-09-05 21:0x
- scope: one batched render pass at a local run of the merged head — the five tickets' rendered cells, the selector answer, the real-engine contrast, the AI refusal, optionally RD-304's span and the docs diff; the demo image, deploys, RD-321 and the harness fix OUT | this brief's §3, written by Wednesday | read 2026-09-05 21:4x

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 21:4x
(checked: "take the newer tip" against "head under test 4611a20" — stated as a conditional with the sha to be reported; "no board read" against "the closures are Wednesday's" — consistent; the ruling mail to S37 names this pass as the closure instrument — consistent.)
