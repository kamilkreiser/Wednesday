# B1484 ADDENDUM-3 (SEAT-N122, third seat): you continue the landing chain at row 6 `csp`, step G

From Tuesday, 2026-11-11, written just after the predecessor's handover line read at 12:05:20 AEDT.

**Your commission is the B1484 kit** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1484_SEAT-N122_nexusai-landing-counts.md` (read it WHOLE first) **as amended by** ADDENDUM-1 (`..._B1484_ADDENDUM-1_learning-row-4b.md`), ADDENDUM-2 (`..._ADDENDUM-2_successor-after-reboot.md`), ANSWER-1 (`..._ANSWER-1_learning-timing-rerun.md`), ANSWER-2 (`..._ANSWER-2_rd407-red-on-main-tree.md`), ANSWER-3 (`..._ANSWER-3_exact-sleep-update-run.md`) and **this file**: all in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`, read each WHOLE. Where they differ, the later file wins. Your pane name is `Datasec/NexusAI-N122` (the previous pane is closed). HARD STOP 18:00 AEDT 2026-11-11 is unchanged.

**Then read, whole:** the STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-11_B1484_STATUS.md`, above all its last section `## HANDOVER (successor, 12:05 AEDT)` (state, the csp values, the six-step recipe, the watch-outs) and the `## READY 5 ci` section as your model.

**What changes for you (as ADDENDUM-2 did for the second seat):**
1. **REFUSE 3 is replaced:** the STATUS, `.tools/b1484/` and `b1484-nodot/` exist by design. Instead, before you write anything, the STATUS last line must read exactly `HANDOVER B1484: next csp G`; otherwise STOP naming what it reads.
2. **STATUS is append-only:** append `## SUCCESSOR 2 (ADDENDUM-3)` with your Step 0 (date, pane, model, files read with line counts and sha256 prefixes) and continue the chain log under it. Name ADDENDUM-3 in ADDENDA READ.
3. **No new clone, no new npm ci** unless the predecessor's go.sh package check fails. Reuse `.tools/b1484/` tools after reading each one you run.
4. **REFUSE 4/5 values become:** origin main = `0ab365b1db62c2b60cb63de9deb1ceccb0b1c4c9` (row 5's landing; any other value: STOP and name it); main counts 5536/331; rows 6 to 10 at their gated sha40s (csp `e6addceb...`, smtp `857843e4...`, archive `52df6468...`, revoke `5fbad1ba...`, l1 `70709c61...`; read full sha40s from THE QUEUE).
5. **Start at row 6 `csp`, step G** (W was done and logged by the predecessor). PREDICTED 5563/333.
6. **Context band:** at about 65% start no new row; at about 75% hand over exactly as the predecessor did (a `## HANDOVER` section with state, values for the next row and the recipe, then `HANDOVER B1484: next <key> <step>`).
