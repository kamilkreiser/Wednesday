# gate50b COMMISSION — ONE Secuura PR: #1364 KS-729 (T2, round 1) + two client-visible texts; author and merger Seat B 51st, round 50b

Filled by fill_gate50b.py at 2026-09-30T23:58:28Z from pins_gate50b.json (measured 2026-09-30T23:51:31Z). Wednesday's commission to the drafter, 2026-10-01, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the 29 keywords (each as a token).

## The PR
| PR | ticket | tier | head | parent | merge-base | ahead / behind | files (+/-) | subject declared -> lands |
|---|---|---|---|---|---|---|---|---|
| #1364 | KS-729 | T2 | `f7466281acf18fd7ea47be19bfa88ececdb3dbb8` | `723dc0722b68` | `723dc0722b68` | 1 / 0 | 2 (+2/-9) | 78 -> 86 |

- develop `723dc0722b68482a03de8577fdb5eb5b3359e725` (tree `2a874956406ca974f3090b24392f6dbfdc8bc4d6`) = #1363's merge. 0 behind. END_TREE `90fe6bbb79eb487023eda4ab8cb237a29f924f8b` (`2 files changed, 2 insertions(+), 9 deletions(-)`). Three instruments agree on it (end_tree_crosscheck_1.out): merge-tree + commit-tree over develop, the head's own tree (parent == develop), and GitHub's `refs/pull/1364/merge` tree; develop's own tree 2a874956406c is the control that differs.
- MODES (git ls-tree): both PR paths 100644 at head / alone / END; control `Blockchain/Dev/scripts/run-migrations.sh` 100755 at develop / head / END.
- IDENTICAL at develop / head / END: `pre-push` ffc25ebc37d4, `preflight.sh` 270b8913c009, `audit-gate.mjs` 8e236ee70ce1, `audit-locks.mjs` aff23b0420ce, `lock-discovery.mjs` 3dd903b527f2, `advisory-fetch-stub.mjs` 29c9fc48f328, `baseline-contract.test.mjs` 2379c0aeee6e, `expected-case-count` 04f9fe46068b.
- Merger Seat B 51st (tmux %86; the author). Pane `QA/Secuura-batch1364`. Report dir `2026-10-01-batch1364-g50b`.

## The ruling
- Wednesday's brief ITEM 1 (removable set predicted `{mwp4}`; leg 7 by its reported map; nothing re-dated; no GRANDFATHERED line; no third file; floor not lowered) + route (a) for base 723dc0722b68; her ANSWER: "the gate50b GO, which covers #1364 and this text" (ITEM 4).
- **The claim** (the READY): 2 files +2/−9; rows 26 → 25; removed `{mwp4}`; r53p `reason` == B 49th's extracted file (1948 B); nothing re-dated; GRANDFATHERED 18 byte-equal; contract `:44` 17 → 18; test file blob-identical; legs 6 / 7 / contract rc 0 at head with a refusal control each; fuse 4 → 3.

## What the gate must rule (by name)
1. **#1364's diff re-derived** by parsing both blobs. (DIFF-REDERIVED, TWO-FILES-ONLY, ROWS-26-25, REASON-CMP, NOTHING-REDATED, GRANDFATHERED-BYTE-EQUAL, CONTRACT-ONE-LINE, FLOOR-NOT-LOWERED)
2. **mwp4 dead to BOTH legs at develop** (leg 6 CLEANUP lists it; leg 7's reported map lacks it, read by a throwaway probe, never its CLEANUP block); legs 6 / 7 / contract rc 0 at head with a refusal control each. (MWP4-DEAD-BOTH-LEGS, LEG7-PROBE, LEGS-RC-HEAD, GATE-STILL-REFUSES)
3. **The fuse cohort at END**: 3 rows dated 2026-10-09 (frvp, wrjc, 337j). (FUSE-COHORT)
4. **The ITEM 4 NEW-TICKET text**: POST AS-IS / POST AMENDED (full text) / DO NOT POST, sentence by sentence against B 50th's recorded readings, the migration files at develop and KS-1376 / KS-1054 on Linear (read-only). (ITEM4-TICKET-TEXT)
5. **The KS-1397 acceptance comment**: same scale, against nginx.conf :24 / :142 at develop and KS-1397's own description. (KS1397-COMMENT)
6. **The PR text**: subject, body, Test Evidence, de-hyphenated foreign keys. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, DEHYPHENATED-KEYS, PR-BODY-CLAIMS)
7. CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS; TIERING, DISK-ENOSPC, **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` LAST. The change is SMALL: a proportionate pass (usage 82%).
- NOT in scope: any deploy, any database read on kintsugi or demo, any SSH, any image build.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 51st): merge 1364 on gate50b` — Seat B 51st merges #1364. Verdict mail subject: `[QA -> Wednesday] GATE50B #1364 (Seat B51 author and merger, round 50b; T2 baseline cleanup: the dead mwp4 row removed 26->25, r53p reason, contract count line; ITEM 4 ticket text and KS-1397 comment ruled)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate50b.py -> pin_1.out: END_TREE `90fe6bbb79eb487023eda4ab8cb237a29f924f8b`. The measured numstat is +2/-9 over 2 files; the seat claimed +2/-9.
- baseline_gate50b.py -> baseline_1.out: BASELINE PASS: 0 FAIL of 14 checks | base 723dc0722b68 head f7466281acf1 | rows 26 -> 25 | removed ['GHSA-mwp4-54f8-5fhr'] | fuse 4 -> 3
- sources_gate50b.py -> sources_1.out: SOURCES READ: 0 FAIL of 12 reads | develop 723dc0722b68 | cited commit 91a8f6b721bc
- keyscan_gate50b.py -> keyscan_1.out: KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL, 0 FLAG line(s) (live surfaces; the gate rules them)
- gh_read_gate50b.py -> gh_read_1.out: CENSUS 22 other open PR(s) read | 0 touch a kit path or carry a census key ['KS-729'] | client-human PRs named: ['1360', '1362'] (the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)
- linear_read_gate50b.py -> linear_read_1.out: LINEAR READ OK: 4 of 4 tickets read
