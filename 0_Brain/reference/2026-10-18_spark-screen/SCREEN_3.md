# Spark screen, part 3 (2026-10-19 ~01:0x-01:35 AEDT): KS-1623 N3 and KS-1624 F1

By a Spark brief-writing sub-agent for Wednesday. Secuura only. Tip pinned: `8a9970511f22661d92f634058fae8c08c656124f` (ls-remote at 01:06; the cache lacked it until Wednesday ran the cache fetch; `cat-file -t` = commit afterwards). Nothing held, raised, pushed, merged, committed or deleted. Ticket text of KS-1623/1624 was NOT read (no Linear reader in the README); briefs rest on Wednesday's commission text.

## Result

| item | brief dir (`local-model/night/briefs/`) | mode / rung | control | round | golden | model s / tokens | run dir (`local-model/runs/`) |
|---|---|---|---|---|---|---|---|
| KS-1623 N3 (summary comment :1445 names deleted + expired) | `ks_1623_p1` (r1 text kept as `KS-1623.md.pre-r2`) | code_patch, rung 1 (1 comment line + NEW source-text jest test) | CONTROL-PASS 7/7 BYTE-IDENTICAL (`..._ks_1623_p1-control-r3`; r1/r2 earlier controls also PASS, r2 after adding `ctx=131072`) | R1 **FAIL**; R2 (the one rebrief) **PASS** | R1 TREE-IDENTICAL; R2 TREE-IDENTICAL | R1 50.7 / 32261+885; R2 44.0 / 32601+856 | `spark_secuura_2026-10-19_ks_1623_p1`, `..._ks_1623_p1-r2` |
| KS-1624 F1 p1 (verify.ts `export`) | `ks_1624_p1` | bash_patch2, rung 1 (2 edit points: 1 product line, 1 suite hunk) | CONTROL-PASS 10/10 BYTE-IDENTICAL (`..._ks_1624_p1-control-r2`) | **PASS** | TREE-IDENTICAL | 23.3 / 9565+831 | `spark_secuura_2026-10-19_ks_1624_p1` |
| KS-1624 F1 p2 (index.ts import + banner; suite banner cell) | `ks_1624_p2` | bash_patch2, rung 2 (3 edit points: 2 index.ts hunks, 1 suite hunk) | CONTROL-PASS 10/10 BYTE-IDENTICAL (`..._ks_1624_p2-control-r2`) | **PASS** | TREE-IDENTICAL | 19.6 / 9284+651 | `spark_secuura_2026-10-19_ks_1624_p2` |

Dry-run rc 0 and brief_lint rc 0 for all three briefs before any round.

## Checker verdict lines
- KS-1623 R1: `RESULT: PASS (7/7)` (A4 "fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)", A5 "5 passed / 5 run", A6, A7 tsc rc 0) then `FAIL A2a ANCHOR ... BAD section 2 ...ks1623-...test.ts: not at the tip` -> `SPARK RESULT: FAIL (checker rc=0; A2a rc=1)`.
- KS-1623 R2: `RESULT: PASS (7/7)`; `PASS A2a ANCHOR ... hunks=1 ok=1 bad=0 skipped_newfile=1`; `SPARK RESULT: PASS`.
- KS-1624 p1: `RESULT: PASS (10/10)`; B4 "RED(rc 1, 2 FAIL)", B5 "(10 pass)", B6 "no NEW failure after (6 suite(s)...)"; A2a hunks=2 ok=2; `SPARK RESULT: PASS`.
- KS-1624 p2: `RESULT: PASS (10/10)`; B4 "RED(rc 1, 1 FAIL)", B5 "(8 pass)", B6 "no NEW failure after (16 suite(s)...)"; A2a hunks=3 ok=3; `SPARK RESULT: PASS`.

## FAIL classification
- KS-1623 R1: **model**. The code was right (7/7, tree-identical) but the NEW file's section was headed `--- a/<path>` instead of `--- /dev/null`, which the brief's Output section said. Same class as the 10-18 KS-1545 A2a miss (header geometry). One rebrief spent (a ROUND 2 section naming the miss and giving the four header lines); R2 PASS. Counter for KS-1623: original + 1 rebrief used.
- Brief defects fixed BEFORE any model run (control failures, not rounds): KS-1624 p1/p2 control r1 FAILED B3c "a line the brief says STAYS was removed" because I wrote the must-change Where bullets without bold; the builder reads bold as must_change (the SCREEN_2 finding in reverse: unchanged bullets must not be bold, changing ones must be). Fixed in both, control r2 PASS. KS-1623 has no must-change parse (A3b skipped), so it was unaffected.

## What was decided
- **KS-1624 F1 is two briefs, two rounds** (the commission said one round each but also at most 3 edit points per brief, split if needed). Count: verify.ts `export` (1) + index.ts import (1) + index.ts banner (1) + suite (the old banner cell replaced and new cells added, 2 hunks) = 5. p1 = export + 3 new suite cells (2 RED reading the export: stripped value, and the default when unset; 1 CONTROL). p2 = import + banner + the old banner cell replaced by a source-text cell (RED) and a CONTROL. The two goldens apply together and the suite gives 11 passed, 0 failed (measured); alone p1 gives 10/0 and p2 8/0.
- Ruling (a) honoured: the value is exported, not recomputed. The banner cell cannot run index.ts (express, app.listen), so p2's cell is a source-text check of the import and the template `API target: ${SECUURA_API_URL}`; "a base with trailing slashes prints without them" is pinned by p1's behavioural export cell (`https://example.test/base//` -> `https://example.test/base`).
- KS-1623 test: reads verification.ts with readFileSync, finds the summary line by text, and compares it with the status list parsed out of the SQL (`lower(btrim(d.status)) NOT IN (...)`). Red cells: `RED KS-1623 the summary comment names deleted`, `RED KS-1623 the summary comment names expired`. 3 CONTROL cells green both ways.
- The ks812 suite is `Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh` (found by `ls-tree -r --name-only` at the tip). Product paths are `Blockchain/Dev/connectors/whatsapp-bot/src/{verify,index}.ts` (the commission wrote them without `Blockchain/Dev/`).
- I did not run jest in a scratch clone for KS-1623 (no config resolved from there); the red/green proof is the control's A4/A5. The ks812 suite was run by hand against tip and edited sources (p1: 8/2 then 10/0; p2: 7/1 then 8/0).

## NOT tested / unmeasured
- Not held or read line by line: I did not read the three model patches beyond the checker (TREE-IDENTICAL to my golden). Wednesday reads at source.
- `tsc` on the whatsapp-bot connector (own package): not run. p2 alone leaves `index.ts` importing a name not yet exported until p1 lands; land p1 first or together.
- Open-PR overlap and live seats' unpushed work: not checked. The stale list in other comments/OpenAPI text for KS-1623: not searched.
- KS-1623 audit surface: a comment and a test only. KS-1624: connector code, deployed nowhere.
- queue.md: two provenance comment lines appended; no runnable queue line (rounds were run by hand with round.sh). `done.md` not touched.

## Files written
Briefs: `night/briefs/ks_1623_p1/` (`KS-1623.md`, `KS-1623.md.pre-r2`, `golden.diff`, `spark.pins`), `ks_1624_p1/`, `ks_1624_p2/` (each `KS-1624.md`, `golden.diff`, `spark.pins`). `spark/queue.md` (2 comment lines). Run dirs and `spark/state/dry/` are round.sh's own. Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/spark_drafter2/` (clone, golden generators, `mkbrief1623.py`, `mkbrief1624.py`, `prove.sh`, logs).
