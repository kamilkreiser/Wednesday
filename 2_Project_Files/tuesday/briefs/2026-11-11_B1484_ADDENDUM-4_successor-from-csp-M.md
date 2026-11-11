# B1484 ADDENDUM-4 (SEAT-N122, fourth seat): you resume the landing chain at row 6 `csp`, step M, now that the rd407-r2 test fix has landed

From Tuesday (s266), 2026-11-11, written just after PR #191 landed (read at source 15:1x AEDT).

**Your commission is the B1484 kit** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1484_SEAT-N122_nexusai-landing-counts.md` (read it WHOLE first) **as amended by** ADDENDUM-1, ADDENDUM-2, ADDENDUM-3, ANSWER-1, ANSWER-2, ANSWER-3, ANSWER-4, ANSWER-5 and **this file**: all `2026-11-11_B1484_*` in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`, read each WHOLE. Where they differ, the later file wins; **this file wins over all of them.** Your pane name is `Datasec/NexusAI-N122` (the previous pane is closed). HARD STOP 18:00 AEDT 2026-11-11 is unchanged.

**Then read, whole:** the STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-11_B1484_STATUS.md`, above all its newest HANDOVER section (the csp values, the recipe, the watch-outs) and the `## READY 5 ci` section as your model.

**What changed since the third seat stopped (MEASURED by Tuesday at source):**
- **PR #191 (RD-407, the rd407-r2 test fix: cells M2, R1 and R3 count the retry waits instead of timing them; test only, one file) LANDED** as merge commit `0364b252b826576bde6dad43ca5000df436c97b7` (parents `0ab365b1` + `e290417a`; tree `c02d5811` = the gated head's tree; Deploy demo skipped). It did not change the counts file: main counts stay **5536 tests / 331 suites**. Its gate ran the new cells 12/12 plain and 10/10 under a 3x slow-sleep shim on this machine, and a full plain verify 5536/5536.
- So the reason the chain paused (rd407-r2 red on this machine) is fixed on main. **ANSWER-3's exact-sleep shim is RETIRED: run every verify plain, with no shim of any kind** (ANSWER-5 already showed the NODE_OPTIONS form never reached jest's realm). ANSWER-4 (re-file once, then hold on rd407) is SUPERSEDED: if rd407-r2 fails now, that is a real failure: STOP and name it.

**What changes for you:**
1. **REFUSE 3 is replaced:** the STATUS, `.tools/b1484/` and `b1484-nodot/` exist by design. Before you write anything, the STATUS last line must read exactly `HANDOVER B1484: next csp M after rd407 fix`; otherwise STOP naming what it reads.
2. **STATUS is append-only:** append `## SUCCESSOR 3 (ADDENDUM-4)` with your Step 0 (date, pane, model, files read with line counts and sha256 prefixes) and continue the chain log under it. Name ADDENDUM-4 in ADDENDA READ.
3. **No new clone, no new npm ci** unless the predecessor's go.sh package check fails. Reuse `.tools/b1484/` tools after reading each one you run.
4. **REFUSE 4/5 values become:** origin main = `0364b252b826576bde6dad43ca5000df436c97b7` (any other value: STOP and name it); main counts 5536/331; rows 6 to 10 at their gated sha40s (csp `e6addceb...`, smtp `857843e4...`, archive `52df6468...`, revoke `5fbad1ba...`, l1 `70709c61...`; read the full sha40s from THE QUEUE).
5. **Start at row 6 `csp`, step M:** re-merge the NEW main `0364b252` into the csp gated head `e6addceb` exactly as the kit's M step does (the merge brings in #191's one test file and nothing else of yours; check `git diff --name-only 0ab365b1 0364b252` is exactly `__tests__/rd407-r2-missing-mid-swap.test.js` and say so). PREDICTED for csp: 5563/333 (unchanged by #191). Then the chain as written: each row's READY handshake to Tuesday through STATUS, Tuesday opens the PR and merges.
6. **Context band:** at about 65% start no new row; at about 75% hand over exactly as the predecessors did (a `## HANDOVER` section with state, values for the next row and the recipe, then `HANDOVER B1484: next <key> <step>`).
