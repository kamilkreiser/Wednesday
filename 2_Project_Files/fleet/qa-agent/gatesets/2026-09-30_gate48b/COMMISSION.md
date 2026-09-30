# gate48b COMMISSION — TWO Secuura PRs in order: #1354 KS-470 (T2, round 2) then #1355 KS-1378 (T1, round 1); merger Seat B 48th, round 48b

Filled by fill_gate48b.py at 2026-09-30T01:48:58Z from pins_gate48b.json (measured 2026-09-30T01:22:41Z). Wednesday's commission to the drafter, 2026-09-30 (the one-PR commission, then her scope change after Kam's card ruling), restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the 26 keywords (each as a token).

## The PRs
| PR | ticket | tier | head | parent | merge-base | ahead / behind develop | files | declared subject -> lands |
|---|---|---|---|---|---|---|---|---|
| #1354 | KS-470 | T2 | `88802586cebe35855983f7639b5e18069fe11e13` | `4370be410bbf` | `37205947ddd2` | 2 / 0 | 3 (6 0 Blockchain/Dev/scripts/audit/audit-baseline.json; 1 0 Blockchain/Dev/scripts/audit/baseline-contract.mjs; 3 3 systemTest/performance/package-lock.json) | 81 -> 89 |
| #1355 | KS-1378 | T1 | `6fab9c0936d4790b15f9b95d59e2f70f00d29d08` | `37205947ddd2` | `37205947ddd2` | 1 / 0 | 5 (4 26 Blockchain/Dev/frontend/issuer/package-lock.json; 1 0 Blockchain/Dev/frontend/issuer/package.json; 5 34 Blockchain/Dev/package-lock.json; 1 0 Blockchain/Dev/package.json; 3 3 systemTest/performance/package-lock.json) | 77 -> 85 |

- develop `37205947ddd2775a72a417beb5b7ac8e3240fbf3` (tree `6930599560c93f3a6cd929cc634b537a2eeb2eaf`) = #1350's squash. Both PRs sit on develop, 0 behind. in order #1354 on develop clean (squash 8fc495aabb3e, tree 08de1e4e5910) -> #1355 on #1354's squash clean (squash ba4b2857349a, tree 0693c2b391b6, NO-OP: systemTest/performance/package-lock.json); END_TREE `0693c2b391b6e0086524c18461c22d72f89a84f1` (`7 files changed, 21 insertions(+), 63 deletions(-)`); the reverse order gives the same tree.
- Recorded modes (pin (H), `git ls-tree`): 8 PR path(s) all 100644 and OK at head / alone / chain step / END; CONTROL `.githooks/pre-push` 100755 at develop / both heads / END (not a PR path: the instrument reads a second value in the same run).
- THE HOOK, THE PREFLIGHT, THE CLEANROOM SCRIPT, THE CONTRACT, THE AUDIT LEGS, THE ISSUER DOCKERFILE (pin (I), (K)): pre-push 100755 ffc25ebc37d4 (IDENTICAL in every tree); preflight.sh 100644 270b8913c009 (IDENTICAL in every tree); lockfile-cleanroom.sh 100644 518bffeeaf4a (IDENTICAL in every tree); baseline-contract.mjs 100644 2504d9a28dc0 (DIFFERS between trees — the contract, by #1354); audit-gate.mjs 100644 8e236ee70ce1 (IDENTICAL in every tree); audit-locks.mjs 100644 aff23b0420ce (IDENTICAL in every tree); Dockerfile 100644 67d5abc68560 (IDENTICAL in every tree).
- Merger Seat B 48th (tmux %79; author of #1355; #1354's author is Seat B 47th). Pane `QA/Secuura-batch1355`. Report dir `2026-09-30-batch1355-g48b`.

## The rulings
- **#1354: Kam's card ruling** (secuura-undici-ghsa-r53p-exception-1354, choice (c), 2026-09-30; decisions.json `ruled_ts` 11:04:41 AEST, Wednesday's quote 11:03:17): "c — Accept permanently, like the twelve siblings | note: And fix now". The row loses `expires`; its reason becomes gate48a's amended text made permanent plus a sentence citing the ruling; `GRANDFATHERED_NO_EXPIRY` +1. **Authority: Kam's ruling, not the advisory-baseline grant.** gate48a's exception question is closed by his word.
- **#1355: Kam's KS-1378 ruling (a)** ("bump … undici") and the card's "And fix now"; Wednesday's route-1 and raise ANSWERs (2026-09-30 10:14 / 10:22 AEST). No baseline row.
- **Merge order: #1354, then #1355.** Both carry the js-yaml blob `80c6752aab86`; #1355's hunk on that file is a NO-OP after #1354.
- **TIERS: #1354 T2, #1355 T1** (a dependency change in a shipped image's build). A tier-1 GO needs UNDICI-MAJOR-RUNTIME MEASURED.

## What the gate must check (by name)
0. **#1354's row and contract line**: no `expires`, only this row changed, every factual sentence of the permanent reason TRUE (none presents "build-tree only" as sufficient); the contract +1/−0, alphabetical, the no-expiry set == GRANDFATHERED exactly; audit 0/0/0 at #1354's head. (ROW-PERMANENT-FIELDS, CONTRACT-LINE-ONLY)
1. **Both lock deltas** against a pristine regen of develop; the 12 lightningcss/magicast dev-flag entries set-equal and attributed to npm; undici 7.30.0 registry-true with a False control; the js-yaml blob byte-equal to #1354's. (LOCK-DELTA-BOTH)
2. **Contract / leg 6 / leg 7** at develop (0/1/1), #1354's head, #1355's head and END (0/0/0); each rc on its own line; leg 6's CLEANUP verbatim (14 rows at #1355-alone, 15 at END with the new permanent r53p row); none removed; #1355 adds no row. (AUDIT-LEGS-HEAD-END, NO-BASELINE-ROW)
3. **The issuer image** built at END (build only); content compared by layer list, not ID; the install difference shown; served-file search with firing controls; the vacuity of a served diff said plainly if the content is identical. (ISSUER-IMAGE)
4. **The suites**: issuer vitest at develop and END with the installed undici; the seat's NOT-RUN list ruled, its resolver claim verified, a named sample run. (SUITES)
5. **The forced major**: is connect-node code reachable in any shipped artefact — measured with controls; a blocker candidate if it ships. (UNDICI-MAJOR-RUNTIME)
6. **Who consumes the root lock**, and the blast radius. (ROOT-LOCK-CONSUMERS)
7. **The preflight at END**, offline legs. (PUSH-PREFLIGHT)
8. **The merge in order**, END, modes, the census of the 11 overlapping PRs and whether each still applies; Peter's #1351-#1353 reported only. (CLEAN-MERGE, END-TREE, MODES, OUT-OF-KIT-CENSUS)
9. **Subjects and bodies**, both PRs. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS)
10. **Follow-ons, reported**: the CLEANUP (two files; ip-address KS 729 on the fuse); the fuse count at END. (FOLLOW-ONS, FUSE-COUNT)
11. TIERING, DISK-ENOSPC, and **REPORT-HASH-LAST**.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 48th): merge 1354 1355 on gate48b` — Seat B 48th merges #1354, then #1355. Verdict mail subject: `[QA -> Wednesday] GATE48B #1354 #1355 (Seat B48 merger, round 48b; T2 KS-470 r53p permanent on Kam ruling (c), then T1 KS-1378 undici 7.30.0 override + js-yaml 5.4.2)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate48b.py -> pin_1.out: in order #1354 on develop clean (squash 8fc495aabb3e, tree 08de1e4e5910) -> #1355 on #1354's squash clean (squash ba4b2857349a, tree 0693c2b391b6, NO-OP: systemTest/performance/package-lock.json); END_TREE `0693c2b391b6e0086524c18461c22d72f89a84f1`.
- lockdelta_gate48b.py -> lockdelta_1.out: LOCKDELTA PASS: 0 FAIL | base 37205947ddd2 head 6fab9c0936d4 | root 1970 -> 1968 | issuer 723 -> 721
- baseline_gate48b.py -> baseline_1.out: BASELINE PASS: 0 FAIL | #1354 row PERMANENT (no expires), contract +1 | #1355 NO ROW | FUSE-COUNT 4 on 2026-10-09 at END, 214.6 h | CLEANUP(pred.) 15, 14 GRANDFATHERED, 1 on the fuse
- lockcensus_gate48b.py -> lockcensus_1.out: CENSUS DONE: 45 lock(s), 17 undici/js-yaml/connect-node entr(y/ies), 1 vulnerable | root-lock copies 0 | connect-node imported in 0 tracked source file(s); VULNERABLE entries: 1 in 1 lock(s): ['Blockchain/Dev/mobile/secuura-app/package-lock.json undici 6.28.0 (PRODUCTION entry)']
- overlaps_gate48b.py -> overlaps_1.out: OVERLAPS READ: 11 PR(s) | conflict today 1 | conflict after #1354 then #1355 1 | empty residue (superseded) 0 | touching undici/busboy 0
- image_read_gate48b.sh -> image_read_1.out: IMAGE READ OK: 4 issuer probe images share one content (layer list e268850c681c0c91); their ids differ only where the compose project label differs
- keyscan_gate48b.py -> keyscan_1.out: KEYSCAN PASS: 12 checks over 2 PR(s), 0 FAIL, 2 FLAG line(s) (live surfaces; the gate rules them)
- gh_read_gate48b.py -> gh_read_1.out: CENSUS 23 other open PR(s) read | 11 touch a kit path or carry a census key ['KS-1378', 'KS-1380', 'KS-470'] | client-human PRs named: ['1351', '1352', '1353'] (at 2026-09-30T01:22:51Z; the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)
- capture_mail_gate48b.py -> capture_1.out: the READY and the seat's thread read by id, verbatim, with TEXT_SHA256; Kam's card ruling from decisions.json; any LATE mail on #1354's new head; Wednesday's four ANSWER files (READY as captured == the seat's record /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-48th/mail/READY-1355.txt (stripped, header block removed): True | READY as captured == Wednesday's scratch copy /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ffc4a192-4894-4f1e-abfb-22149b1bd26c/scratchpad/b48_ready48b.md (stripped, header block removed): True | KAM RULING card secuura-undici-ghsa-r53p-exception-1354: status ruled, ruled_choice c, ruled_ts 2026-09-30T11:04:41.047347+10:00 (Wednesday quoted 2026-09-30 11:03:17 AEST) | LATE mails from the seat naming 1354 after 00:56Z, beyond the ids captured above: 0; CAPTURE OK: 16 mails + the brief by id, 11 check(s), 0 problem(s) -> mail_gate48b_ready.md).
