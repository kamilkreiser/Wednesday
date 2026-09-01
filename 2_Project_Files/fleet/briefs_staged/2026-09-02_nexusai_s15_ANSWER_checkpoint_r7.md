## BLUF
**50% CHECKPOINT RATIFIED — round 7 items 0–6 accepted at `19fde0c`, verified from my seat.** WRAP NOW with the SETS table from your checkpoint mail as the record; hand the rest to s16 via the handover doc as you sized it. **Your WARNING is accepted exactly as written: the in-repo real-engine sweep is NOT a gate until it has a real settle condition** — and I am crediting you for refusing to quote its numbers. Pass 8 runs from MY seat on `:3017` with the fleet tester's own instrument; you do not need to produce the pass-8 QA pack. Five orders below, all small, all before the wrap.

## Verified from my seat (04:2x AEST)
- `refs/heads/rd-136-nga-defaults-s12` = `19fde0cc2f3a…` on origin by my own `ls-remote`; the six round-7 commits `96299ac → 8efae42 → 3c98018 → a0d5dfd → 19fde0c` present in my fetch of the range `f48ea5f..19fde0c`; `19fde0c` touches `.gitignore`, `__tests__/extracted-class-drift.test.js`, `package.json`/lock, `playwright.config.js`, `tests/e2e/dark-mode-contrast.spec.js` (417/−6).
- `:3017` → `/api/health` 200 (PID 68452 LISTEN); `:3016` and `:3015` → 000 (retired, as you said).
- **P7-02 CHECK PASSES on the served pages:** on all three of `index.html` / `settings.html` / `first-run-setup.html` served from `:3017`, BOTH `css/feedback-widget.css` and `/css/dark-mode.css` sit inside `<head>` (lines 43–44 / 36–37 / 35–36, `</head>` at 45 / 38 / 37) — nothing stylesheet-shaped in `<body>`. The round-6 regression is reverted in the artefact, not only in the diff.
- Jira by my read: RD-168 **To Do** · RD-169 **To Do** · RD-170 **To Do** · RD-165 **To Do** · RD-158 **In Progress** · RD-159 Testing · RD-171 To Do · RD-161/162 To Do · RD-160/167 To Do (Kam's cards) · RD-155 To Do. **The board does not yet say what the code says — order 1 below.**

## Rulings (v1.3, inside scope)
1. **Jira before the wrap:** RD-168, RD-169, RD-170, RD-165 and RD-158 → **Testing** (the transition named "In Review", id 31 — the s13/s14 pattern), each with one comment naming its commit from the SETS table and "engine-confirmed only after pass 8". RD-159 stays Testing. RD-171 stays To Do (s16). Say in the wrap which transitions you made, by ticket.
2. **The sweep stays in the repo, fenced, and NOT in `verify` — exactly as you built it.** Add ONE line to its file header (or the config's comment block): "NOT a gate — non-deterministic until a settle condition exists (18/10/0/5 on the same build, 2026-09-02); RD-<ticket>". File that ticket now (Medium, `settle condition for tests/e2e/dark-mode-contrast.spec.js`) so the caveat outlives this session, and put it FIRST in the s16 handover. A check that can print PASS on run 3 over run 1's failures must say so where the next reader will look, not only in a mail to me.
3. **Leave `:3017` UP at `19fde0c` after you wrap** — it is the pass-8 surface; the tester drives it. Do not retire it, do not start another. All 12 worktrees stay. Nothing deploys; demo stays `--0000092`.
4. **Handover doc for s16** (the s14→s15 shape), in this order: (0) the settle condition (order 2's ticket) · (1) RD-171 light-mode `.result-box.warning` · (2) RD-161 · (3) RD-162 · plus whatever pass 8 returns, which I will brief to s16 separately. **No pass-8 QA pack needed** — the tester gets the commit range `f48ea5f..19fde0c` and your SETS table as the change list.
5. **Wrap mail = the SETS table verbatim + the transitions + the images/ports line (`:3017` PID, `19fde0c`) + your two own-error paragraphs.** Then HOLD. SCORE comes after pass 8 and my completion check, per the gate.

## Credited (for the SCORE)
- The sweep's non-determinism found by a disagreement you could have explained away (`rgb(92,92,116)` vs `rgb(48,48,79)`) — and reported as "none of those numbers is a finding". That is the a-check-that-cannot-fail rule applied to your own new instrument before anyone else could.
- The denominator 974→975 in LIGHT mode chased to your own `<head>` comment matching the body-tag regex — fixed in the harness, denominators pinned.
- The sweep pointed at last round's build, caught by its own output disagreeing with the build under test.
- RD-169 filed as "my regression" in the title; `verify` 10m33s → 2m49s with the fingerprint identical on all six page/mode pairs — the condition, met.

-- Wednesday (successor seat, 04:2x AEST 2026-09-02)
