# Residue screen for the Spark — 2026-09-30 (written 13:22 AEST)

This screen was written by a Spark brief-writer sub-agent for Wednesday. Nothing was raised, pushed, posted or mailed. Linear was not read, because the pool did not need widening. GitHub was read only, with REST `GET` for the open PRs and their `/files`, using the token sourced for that one command. Nothing was written under `!CODING/`. Git write verbs ran only in the scratchpad clones `rs/{src,gold,ctl,round}`.

**Base:** develop `3e3a68260d0ef541b2410d323849d2639ddd6941`, read by `ls-remote` at 2026-09-30T03:09:42Z. It matches the expected base.
**Sources read:**
- gate47 report `…/reports/2026-09-30-batch1349-g47/report.md`. Its sha256 is `e0eb8ba1eb26…`, which matches.
- gate48a report `…-g48a/report.md` (`7710b5e399cc…`).
- gate48b report `…-g48b/report.md` (`5ae77e86d1ea…`).
- The B 46th, B 47th and B 48th handovers.
- The kit, the template and today's two example briefs.

**Counts:** 36 items screened (7 gate47 + 21 gate48a/b + 8 handover), 1 briefable pool item plus 1 twin that the writer found, 2 run, 2 PASS. Widening to KS Backlog/Todo (pool 4) was NOT triggered, because pools 1-3 yielded a briefable item.

## Verdict per pool item

### 1. gate47 polish
| Item | Verdict |
|---|---|
| N-1349-4 | **Peter's / EXCLUDED.** It is in `systemTest/akto/src/setup/aktoRateLimit.ts` and its test. Open #1351 touches 2 `aktoRateLimit` paths (REST `/files`, measured). B 47th's handover `:178` says to sequence it after #1351. |
| N-1349-5 | **Peter's / EXCLUDED.** Same file, and the same reason. |
| N-1350-3 | **EXCLUDED: not a code task.** It is a figure in #1350's PR body and READY ("19/14" vs "20/16"). #1350 is merged, and no repo file carries the claim. |
| N-1350-4 | **Owned by B 49th.** E1's message is in the ks1054 test file. |
| N-1350-5 | **Owned by B 49th.** The `trap … EXIT` is set twice in the ks1054 test file (`:94`, `:221`). |
| N-1350-6 | **Owned by B 49th.** The R-cells are in the ks1054 test file. It is also decision-shaped: whether to relabel the CONTROL cells or restructure them. |
| N-1350-7 | **BRIEFED and RUN: PASS.** The line is in `deploy.sh:857`. The ks1054 test is untouched, and the new test is its own file. |
| (N-1350-7b) | **BRIEFED and RUN: PASS.** This is the deploy-all.sh twin at `:312`, and gate47 did not name it. The writer found it and flags it for Wednesday's ruling. |

### 2. gate48a / gate48b findings
| Item | Verdict |
|---|---|
| N-1354-1 | **EXCLUDED: decision (Kam's).** It was ruled (c), and #1355 superseded it. |
| N-1354-2 | **EXCLUDED: not repo code.** It is a Wednesday/Kam card text. |
| N-1354-3 | **Owned by B 49th.** It is the row reason in `audit-baseline.json`. |
| N-1354-4 | **EXCLUDED: not a code task.** It is PR-body text, and B 47th already corrected it by API edit. |
| N-1354-5 | **EXCLUDED: already actioned.** It was filed as KS-1394 with the gate's text. KS-1394 itself is **decision-shaped**: its "suggested shape" is a per-lock command generator (a parent mount when a `file:` link escapes, `npm update <pkg>` for advisory moves). That is more than 3 edit points in `audit-locks.mjs`, and the design has not been ruled. A narrowed carve that changes only the `:352` pointer text would need a card first. |
| N-1354-6 | **EXCLUDED: void.** The override ticket is moot, because #1355 is that work. |
| N-1354-7 | **EXCLUDED: decision-shaped.** It would add `systemTest/` locks to the cleanroom corpus in `lockfile-cleanroom.sh:46`. Whether to add them, and which ones, is a design choice. It is also a lock/supply-chain gate, and a doubt about the security surface is resolved as excluded. |
| N-1354-8 | **EXCLUDED: Info.** It is about ruling citations. |
| N-1354-9 | **EXCLUDED: Info.** It is about ruling citations. |
| N-1354-10 | **EXCLUDED: Info.** It was about urgency, and it is resolved: pushes are unblocked. |
| N-1354-11 | **EXCLUDED: Info.** It was about mail delivery. |
| N-1355-1 | **Owned by B 49th.** It is the r53p row reason in `audit-baseline.json`, amended at the CLEANUP touch. |
| N-1355-2 | **EXCLUDED: not a code task.** It is a PR title or body. |
| N-1355-3 | **EXCLUDED: not a code task.** It is a PR title or body. |
| N-1355-4 | **EXCLUDED: not a code task.** It is a PR title or body. |
| N-1355-5 | **EXCLUDED: not a code task.** It is a PR title or body. |
| N-1355-6 | **EXCLUDED: record/instrument.** |
| N-1355-7 | **EXCLUDED: record/instrument.** |
| N-1355-10 | **EXCLUDED: record/instrument.** |
| N-1355-8 | **EXCLUDED: `package.json` is off limits.** It is the root `engines.node`. It is also a decision: which floor to set. |
| N-1355-9 | **EXCLUDED: out of scope.** It is mobile undici under KS 769, which expires 10-19. |

### 3. Handover residue (B 47th, B 48th)
| Item | Verdict |
|---|---|
| ITEM 1a KS-1054 rebase | **Owned by B 49th.** |
| ITEM 1b KS-1015 | **Owned by B 49th.** It is already a Spark READY. |
| 14/15-row baseline CLEANUP | **Owned by B 49th.** It is in `audit-baseline.json` and `baseline-contract.mjs`. |
| ITEM 2 KS-1380/1387 | **Owned by B 49th.** It covers lock and package files. KS-1380's creator is Peter and KS-1387's creator is Stuart, so it is excluded either way. |
| §5f live sweeps | **EXCLUDED: not briefable.** They need a live stack and are not a code change. |
| KS-1195 | **EXCLUDED: Kam's ruling, Stuart's thread.** |
| EMPTY/non-JSON divergence, deploy.sh vs deploy-all.sh | **EXCLUDED: decision.** It is kept and stated for Kam. |
| Fuse recompute | **EXCLUDED: not a code task.** |

## Rounds

| Brief | Tier | Rounds | Result | Wall | READY |
|---|---|---|---|---|---|
| `night/briefs/KS-1054-N-1350-7/`: deploy.sh `:857`, plus the new `ks1054_deploy_sh_rc1_message.test.sh` | bash_patch, rung 2 (spelled out, product + new test) | 1 of 2 | **PASS 7/7 + A2a**, BYTE-IDENTICAL to the golden | 59.6 s (prompt 31,344 / completion 1,574) | `2_Project_Files/local-model/night/READY_KS-1054-DEPLOYRC1-1_spark-dsv4flash_BRIEFED-BASHPATCH-DEPLOY-PASS-7of7_2026-09-30.diff.md` |
| `night/briefs/KS-1054-N-1350-7b/`: deploy-all.sh `:312`, plus the new `ks1054_deploy_all_rc1_message.test.sh` | bash_patch, rung 2 | 1 of 2 | **PASS 7/7 + A2a**, BYTE-IDENTICAL (cmp rc 0; cross-golden control rc 1) | 47.6 s (19,684 / 1,569) | `2_Project_Files/local-model/night/READY_KS-1054-DEPLOYALLRC1-1_spark-dsv4flash_BRIEFED-BASHPATCH-DEPLOY-ALL-PASS-7of7_2026-09-30.diff.md` |

No FAIL occurred, so no cause needed classifying. Both READYs had their heading and filename fixed by hand, and each fix is marked in the file. The reason is that `hold_ready.py` refuses `--model-tag` on bash_patch. It also doubles the ticket prefix on the ROWID and `BRIEFED-` on the title. That is recorded in `IMPROVEMENTS.md`. Ladder rows 48 and 49 have been added. The Spark served both calls immediately, with no queueing and no retry.

## Controls (each run before the round)
- **N-1350-7:**
  - Checker on the golden: PASS 7/7 strict, rc 0.
  - Product `+` line mutated: FAIL B3b, rc 1.
  - Test substring mutated: FAIL B5, rc 1.
  - A2a on the golden: rc 0. A2a with the header moved by -1: BAD, rc 1.
- **N-1350-7b:**
  - Checker on the golden: PASS 7/7 strict, rc 0.
  - Test substring mutated: FAIL B5, rc 1.
  - A2a on the golden: rc 0. A2a with the header moved by +1: BAD, rc 1.
- **Collision instrument:** 23 open PRs, 0 of which touch `deploy.sh`, `deploy-all.sh`, `check-startup-migrations.sh` or the new test paths. As a positive control, the same matcher found 2 `aktoRateLimit` paths in #1351.

## For Wednesday's ruling
- **The wording of both READYs is the brief-writer's.** The text is "FAILED or could not be verified — see above". gate47 named the defect, but not the replacement text.
- **N-1350-7b was not named by the gate.** Rule whether it rides with the N-1350-7 raise (a natural one-PR pair, two product files plus two tests) or is dropped.
- **Sequencing:** both belong under KS-1054, next to B 49th's ITEM 1a. They touch different files from ITEM 1a, so there is no textual conflict. The raise seat may want them after ITEM 1a's merge so that the wording covers all three rc-1 causes on develop.
- **KS-1394 is decision-shaped.** It would need a card: *"carve KS-1394 to the `audit-locks.mjs:352` pointer text only (name `npm update <pkg> --package-lock-only` and the parent mount for escaping `file:` links), or build the per-lock command generator the ticket suggests?"* No card was posted.
