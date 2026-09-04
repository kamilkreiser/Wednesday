## SCORE — RD-296 @ 7147a4a = **0.90**. QA PASSED (no Blocker, five Minors). ONE item is owed before Wednesday's GO: F-2. The deploy question is with Kam.

**QA report (read it whole, not this summary):** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-05-s33-rd296-through-code-and-browser/report.md` — probes, paired KPI payloads for six windows including both period edges, and both browser screenshots in `evidence/`.

**Wednesday's completion check — delivered vs commissioned, item by item:**
- Wire Sustainability through the configured-log-source selector like every other tab → **DELIVERED, confirmed by the gate at runtime** (log-line correlation with a control; `dataSource` on the payload).
- No new tile; `SECURE_RELEASE_AVOIDED` dark structurally and truthfully → **DELIVERED** (six lit / three dark; the QA's F-5 notes the tab is *silent* about that KPI rather than untruthful — pre-existing, for Kam's judgement, not this round's work).
- Figures unchanged on a SQLite deployment → **DELIVERED and MEASURED**: not a digit moved between b77feea and 7147a4a across six windows on byte-identical seeded data.
- Regression test drives the product's own path → **PARTIALLY DELIVERED — this is the deduction.** The 21 reader tests are real, but the WIRING guard is a source-text matcher: the QA reintroduced the exact defect and both reds read `server.js` as a string; a semantically identical correct refactor turned one of them red on correct code. A guard that false-reds on a tidy is the guard that gets loosened. **OWED before GO (F-2): one behavioural test that mounts the real router over a temp SQLite and asserts `dataSource === 'local-database'` — replacing, not adding to, the text matcher.** Small; put it on the branch with its own red-proof and say so in one line.
- No UI file touched / palette → **DELIVERED** (zero UI files in the diff, confirmed by the gate).
- Screenshots both modes, local-not-demo stated → **DELIVERED.**
- Sets-not-counts mail, four tickets filed rather than absorbed, adapter built-then-deleted with the reason → **DELIVERED, and the disclosure is why this is 0.90 and not lower** with F-2 open.

**Second, smaller deduction:** Claim 5's field derivation said 11; the set actually read is 12 — `created_at` was omitted, and it is the one with a hazard (all four parsers default it to *now* when `TimeGenerated` is absent, so a LAW row with no timestamp lands in "today" and vanishes from history). The conclusion "no adapter needed" survives; the derivation did not. One line on RD-296 correcting the count, and the `created_at` default hazard goes on **RD-306** as a sharpening (see below), not as a new ticket.

**Dispositions of the rest — yours to place on the board, no new build this round:**
- **F-1 → RD-306, sharpened:** RD-296 makes the LAW path LIVE, and on it the window is discarded (no `from`/`to` in `azureLogAnalytics.js`, no `TimeGenerated` clause), the KQL is `take 10000 | order by …` — `take` before the sort yields an ARBITRARY sample above the cap. Loud (truncated banner), so Minor on SQLite, Major on a large LAW workspace. **Cheapest half: reorder to `order by TimeGenerated desc | take N` so the cap bites on the newest rows** — that belongs to RD-306's round, not this one. Put the QA's sentence on RD-306.
- **F-3 → RD-306 too** (the `created_at`-defaults-to-now hazard is a LAW-path data-quality item).
- **F-4 → recorded as a curio on RD-296** (JS keeps a numeric-0 `Job_Start_Time_UTC`, SQL excludes it; no reachable path found).
- **RD-305 → SHARPENED by the QA, and it may shorten the ticket:** the same timespan string feeds `ago(${timespan})` (wants `30d`) AND `requestBody.timespan` (wants ISO-8601 per the file's own comment). Switching fixes one and breaks the other. **Existing callers already send `Nd` in the request body on every real deployment** — so either the API tolerates `Nd` (RD-305 is a doc fix) or those paths already fail in production. One probe decides; the QA wrote what it needs. Put that on RD-305 verbatim.
- **RD-304, RD-307:** confirmed as stated.

**Ports:** the QA left two local surfaces running — 3113 (7147a4a) and 3114 (b77feea) — in ITS worktrees, not yours; 3111 was held by a live NexusAI surface (pid 59826) that it did not touch. Wednesday retires the QA's two; nothing of yours is affected.

**The gated SHA is 7147a4a; the branch head is 2b3fe32 (RD-245, entirely untested).** The RD-245 batched gate covers the head later. **The deploy question — RD-296 alone at 7147a4a now, or the branch head once after the RD-245 gate — is carded for Kam; no deploy until he rules and F-2 lands.**

**Score: 0.90.** Held below higher by F-2 (a commissioned product-path guard delivered as text matching) and the 11-vs-12 derivation; earned by measured no-change across six windows, the honest SQLite-only limit, the deleted adapter, and four tickets filed rather than absorbed.

PROVENANCE:
- The QA verdict, F-1…F-5, the RD-305 sharpening, the NOT-TESTED list, the ports, the branch head at end of pass | `[QA -> Wednesday] RD-296 through-code + browser pass @ 7147a4a` at wednesday-agent@agentmail.to, 2026-09-04T23:19:46Z, and the report file at the path above (32,371 B, headings read) | read 2026-09-05
- 7147a4a gated; 2b3fe32 branch head at origin | `git ls-remote` on your repo (read-only), 09:3x AEST | read 2026-09-05
- The commissioned items | Wednesday's S33 brief 2026-09-04T22:17Z and Wednesday's RD-296 receipt 22:54Z — my project, not yours | read 2026-09-05
