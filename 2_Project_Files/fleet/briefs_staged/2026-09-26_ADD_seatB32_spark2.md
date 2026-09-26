# ADDENDUM (Seat B 32nd): two more held Spark PASSes for your raise stream — raise after items 1-2, same gate if they are READY in time

## BLUF
Two more READYs from the Spark, both PASS 7/7 on one round, **both source-read by Wednesday: the model's diff is byte-identical to the brief's golden** (KS-1334-A sha1 b51a5614; KS-1337 akto sha1 27033ab4). Raise ONE PR each, **after** your items 1-2 (part C, KS-1344), before or alongside item 3 (the closes). If all four PRs are READY before the gate kit is drafted, they share ONE gate; otherwise these two go to the next gate. Nothing here changes items 0-5 of your brief.

## The two READYs (paths are Wednesday's tree; copy the diff block, do not retype)
1. **KS-1334-A — `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` :113 and :1859 → `fail500` + in-place edits to `ks730c-adminconfig-500-never-answers-err-message.test.ts`** (the ks730c count/KNOWN-list lines MUST change with the fix — by design, see the READY). READY: `2_Project_Files/local-model/night/READY_KS-1334-ADMINCONFIG500-A_spark-dsv4flash_BRIEFED-CODEPATCH-ADMINCONFIG-500-NEVER-ANSWERS-ERR-MESSAGE-PASS-7of7_2026-09-26.diff.md`. **TIER 1** (production error handling on a security surface). Refs KS-1334 — sites 2 of 4; KS-1334 stays In Progress (brief B for :2031/:2158 comes after this merges, because both edit the same ks730c lines).
2. **KS-1337 site 2 — `systemTest/akto/tests/preSuiteSetup.ts:36` URL.pathname → fileURLToPath + one test cell.** READY: `2_Project_Files/local-model/night/READY_KS-1337-AKTOPRESUITE_spark-dsv4flash_RUNG4-CODEPATCH-AKTO-PRESUITE-FILEURLTOPATH-PASS-7of7_2026-09-26.diff.md` (held by hand — the hold tool cannot yet hold a rung-4 run; the READY says why and carries the verdict lines verbatim). **TIER 2** (tooling). Refs KS-1337; it stays In Progress (the playwright site remains).

## Rules (unchanged from your brief, repeated because they bit today)
- Lint each touched file with ITS package's own lint (+ format:check where the package has it) before pushing; if lint fails, STOP and ask, as B 31st did on KS-1337.
- Quote only the gate lines your push actually printed (`fleet/STANDING_LINES.md`, the 2026-09-26 B 31st section). An akto-only push runs the format gate only: fleet STOP = NOT APPLICABLE.
- Foreign keys un-hyphenated in PR titles, bodies and commit messages.
- No file of these two overlaps part C (webhooks.ts, ks1341c) or KS-1344 (ks1341a) — Wednesday checked the paths; re-check against open PRs as your brief says.
