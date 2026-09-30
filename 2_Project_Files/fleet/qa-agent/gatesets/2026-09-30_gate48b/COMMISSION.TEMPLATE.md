# gate48b COMMISSION — TWO Secuura PRs in order: #1354 KS-470 (T2, round 2) then #1355 KS-1378 (T1, round 1); merger {{MERGE_SEAT}}, round 48b

Filled by fill_gate48b.py at {{FILLED_AT}} from pins_gate48b.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-09-30 (the one-PR commission, then her scope change after Kam's card ruling), restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the {{N_KW}} keywords (each as a token).

## The PRs
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`) = #1350's squash. Both PRs sit on develop, 0 behind. {{CHAIN_LINE}} END_TREE `{{END_TREE}}` (`{{SHORTSTAT}}`); the reverse order gives the same tree.
- {{MODE_LINE}}
- {{HOOK_LINE}}
- Merger {{MERGE_SEAT}} (tmux %79; author of #1355; #1354's author is Seat B 47th). Pane `QA/Secuura-batch1355`. Report dir `{{REPORT}}`.

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
The GO string, as the GO mail's SUBJECT: `{{GO}}` — {{MERGE_SEAT}} merges #1354, then #1355. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate48b.py -> pin_1.out: {{CHAIN_LINE}} END_TREE `{{END_TREE}}`.
- lockdelta_gate48b.py -> lockdelta_1.out: {{LOCKDELTA}}
- baseline_gate48b.py -> baseline_1.out: {{BASELINE}}
- lockcensus_gate48b.py -> lockcensus_1.out: {{LOCKCENSUS}}
- overlaps_gate48b.py -> overlaps_1.out: {{OVERLAPS}}
- image_read_gate48b.sh -> image_read_1.out: {{IMAGE_READ}}
- keyscan_gate48b.py -> keyscan_1.out: {{KEYSCAN}}
- gh_read_gate48b.py -> gh_read_1.out: {{CENSUS_LINE}}
- capture_mail_gate48b.py -> capture_1.out: {{CAPTURE_LINE}}
