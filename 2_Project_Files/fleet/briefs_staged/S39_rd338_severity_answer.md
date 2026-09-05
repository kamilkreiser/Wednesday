## BLUF
**RULED (v1.3 — ticket priority is Wednesday's): RD-338 → MEDIUM, on YOUR measurement (Wednesday has not re-derived it: "a logger that gains `.warn` loses the diagnostic ENTIRELY — zero logger calls, zero process warnings", falsifying `sustainability.js:212-213` in its own words; and item 3 — a spread refactor would silently NOOP every diagnostic in the file while every existing test stayed green). The Low was set at 16:17Z on the `reason` field's zero consumers; this is a different finding and it was unmeasured then. It stays NOT pre-deploy: the trigger is a logger that changes shape after construction or a refactor — an injection or a code change, not a production event. Move the ticket to Medium with a comment quoting the two measurements; your fix shape (resolve the method at CALL time inside the wrapper, items 1 and 3 in ONE commit because the wrong fix for 1 breaks 3 silently) is ADOPTED as the round's design line — run it as a hypothesis against the unfixed router first, as always. Queue order unchanged (RD-338 after RD-336 merges, before RD-339). Holding idle for the verdict is correct; nothing else to read.**

## Carried into the round's tests (your two instrument notes)
- `getRows` is called TWICE per request (`:447` and `:634`) and only the first sets `dataSource` — a per-call counter halves the apparent causes; the round's harness counts per REQUEST, and says so in a comment beside the counter.
- The cap notice fires on the THIRTY-THIRD distinct cause (the dedupe returns before the cap check at 32) — any assertion on the notice text drives a 33rd cause; the QA brief for RD-338 will carry both as cells.
- QA-F2's sentinel (`'(unlabelled)'` counted as a source — 31 real vs "32") — the fix changes the SENTENCE or excludes the sentinel from the count; say which in the READY and why.

## Nothing else changes
`3bdf20d` HELD; RD-336's verdict due ~05:15; RD-338 branches off the merged tip after; no deploy; never `--no-verify`; never delete; the detector on any prompt line.

PROVENANCE (answer — facts named):
- Your STATUS: the four items measured on the real router (QA-F1 lost entirely; QA-F2 31 vs "32" with the sentinel; the prototype property pinned by nothing; `emitWarning` both paths undriven); the double `getRows` call; the 33rd-cause note; the fix shape; the severity question; comment 37163 | `[Datasec/NexusAI -> Wednesday] STATUS: RD-338 prep done (37163) …` 2026-09-05T18:52:47Z (read whole) | read 2026-09-06 04:53
- RD-338's Low as set in Wednesday's 17:12Z GO (QA-F1/QA-F2 + the two untested paths, "ONE new Low residue ticket") — the priority's original basis | `briefs_staged/S38_rd337_go.md` | read 2026-09-06 04:53
- The code at `:207-213` / `:447` / `:634` / `:178-179` NOT re-read by Wednesday this action — every mechanism sentence above is YOUR measurement, labelled so; the RD-338 gate re-derives | stated | 2026-09-06 04:53
- scope: re-rank RD-338 on the builder's measurement; adopt the fix shape as a hypothesis; the queue and holds unchanged | this mail, written by Wednesday | read 2026-09-06 04:53

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 04:53
(checked against Kam's rulings for 09-06 — none — and the previous mail to this agent, the 18:46Z ACK (RD-338 read-only prep allowed; the hold): this mail changes RD-338's PRIORITY only and says so by name; queue order and holds identical; consistent.)
