# Spark screen, part 13 (2026-10-19 ~16:35-17:15 AEDT): four briefs from four tickets, four rounds, FOUR PASS (KS-1642 x2, KS-1645 item 3, KS-1641 finding 2); ceiling rung 2 (twice), rung 2 test-only 0, rung 1 test-only once

By a Spark screen-and-brief sub-agent for Wednesday (receipt: claude-sonnet-5-5, row C8, P1-P4 no, gauge 34%). Secuura only. Nothing held, raised, pushed, merged, committed or deleted; no GitHub or Linear write; no `hold_ready`; no override of the lane guard. Nothing under `!CODING` was written (only `git ls-remote`; the cache clone is in Wednesday's tree). `LINEAR_API_KEY` was sourced inside script files, never printed.

## Pinned sha
`git ls-remote origin refs/heads/develop` read 16:43 = `722e07f19cee683ea037930e601e380a9491f7b5` (the commission said 846ae27; develop is "Refs KS-1634: label a simulated anchor on chain-first verify", i.e. #1597's v2 work has merged). Fetched into the cache clone (`cat-file -t` = commit). Re-read after the rounds (17:1x): unchanged. All four briefs say `Tip: 722e07f19cee`.

## Census (Linear, read-only)
- Query: team KS, `updatedAt >= 2026-10-19T00:00:00Z`, `first:50`, 1 page, `hasNextPage=False`: **34 tickets** (In Progress 16, Backlog 10, In Review 6, Todo 2). Backlog/Todo among them: **12** (KS-1645, 1644, 1643, 1642, 1641, 1640, 1639, 1629, 1483, 1384, 772, 485).
- Positive control: the named recent candidates KS-1643, 1644, 1645, 1640 are in the page; KS-1625 and KS-1628 are NOT (not updated since the cutoff), so I read them by number: KS-1625 Backlog (updated 10-18 15:27Z), KS-1628 In Progress with PRs #1587-1590 attached. Their descriptions were read whole.
- Descriptions read whole: KS-1645, 1644, 1643, 1642, 1641, 1640, 1639, 1628, 1625, 1483.
- Prior art: none of KS-1639..1645 is in SCREEN_10/11/12 or queue.md; KS-1639 was a named exclusion in SCREEN_12 and is not one now.

## SKIPs (reason, measured)
- KS-1640: originate `verification.ts` and `verificationV2.ts` (Seat R); also the ticket says fold v2 in with KS-1634 and re-cut ks563.
- KS-1644: anchoring `index.ts` and `anchorOverwriteGuard.ts` (Seat J).
- KS-1643: `scripts/preflight/preflight.sh` and a bash test, outside `services/*` (the builder refuses a product there); Minor 1 is also a "move it or reword the message" choice.
- KS-1639: a decision stated by the ticket ("decide whether the text form should be accepted at all ... a product call") on a credential-flag mapper (`rowToApiKey`, `isActive`).
- KS-1628 (what is left): item 1 (the originate verify route) was retired (KS-1637 is about its removal pin); item 2 is originate `routes/anchors.ts` (Seat J); item 3 is already done on develop (`anchorReadback.ts:28` imports `FABRICATED_TX_PREFIX`, `:115` uses it).
- KS-1625: a decision by its own title and text (four options, "options, not a recommendation").
- KS-1645 items 1, 2, 4: item 2 is "decide the `to` boundary"; item 1 (page the upstream or declare the cap) is a choice; item 4 reconciles an OpenAPI block four ways (spec text and a generated yaml). Only item 3 is briefed.
- KS-1641 finding 1: needs `Settings.tsx` to open a tab from the URL (frontend, outside `services/*`). KS-1641 `:515`: needs the Microsoft token endpoint stubbed.
- KS-1642 option 2 for (b) (reword only) not taken; KS-1483 (pre-push hook: bash, outside `services/*`, changes what the hook refuses); KS-1384 (Kamil's, anchoring, a decision); KS-1629 (named exclusion); KS-772, KS-485 (review streams, not tasks).

## Briefs and rounds (brief dirs under `local-model/night/briefs/`, run dirs under `local-model/runs/`)
All four: `brief_lint` rc 0 with an empty stderr (control: the same linter on a copy of ks_1645_p1 with the `File:` line under `## The test` removed printed `WARNING TEST PATH`, rc 0), dry-run rc 0 with no WARNING, ctx=65536 pinned, no blank context line in any edit block, no tip line re-added as `+`, ONE real round each, no rebrief. Each test was run by hand before its brief was written (red at the tip, green with the edit). Develop did not move during the work.

| # | ticket / piece | dir | tier / rung | control | round verdict (verbatim) | golden |
|---|---|---|---|---|---|---|
| 1 | KS-1645 item 3: `audit-export.ts` validates `type` (derives `AuditType` from a runtime list, 400 BAD_REQUEST for unknown or repeated) + NEW vitest file | `ks_1645_p1` | code_patch, rung 2 | CONTROL-PASS 7/7 BYTE-IDENTICAL, 75 s | `SPARK ROUND ks_1645_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 722e07f19cee · 118s round, 45.32s model, 13941+1969 tok` | BYTE-IDENTICAL |
| 2 | KS-1642 (b)+(c)+H10: `idNamespaceCollision.ts` up-front read probe so the helper never throws on a throwing getter/Proxy; reason comment on the child catch + NEW jest file | `ks_1642_p1` | code_patch, rung 2 | control r1 FAILED A3b (my brief defect, below), **r2 CONTROL-PASS 7/7 BYTE-IDENTICAL**, 75 s | `SPARK ROUND ks_1642_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 722e07f19cee · 113s round, 33.067s model, 13943+1214 tok` | BYTE-IDENTICAL |
| 3 | KS-1641 finding 2 (`:465`): cap the reflected `error_description` at 200 chars in the m365 OAuth callback + NEW vitest file booting the real app | `ks_1641_p1` | code_patch, rung 2 | CONTROL-PASS 7/7 BYTE-IDENTICAL, 48 s | `SPARK ROUND ks_1641_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 722e07f19cee · 101s round, 55.827s model, 33447+1452 tok` | BYTE-IDENTICAL |
| 4 | KS-1642 (a), H9 half: RED + CONTROL cell in the existing ks1612 jest file; tamper `idNamespaceCollision.ts:84` (`r.constraint === null &&` dropped) | `ks_1642_p2` | test_only, rung 1 | CONTROL-PASS 7/7 BYTE-IDENTICAL, 69 s | `SPARK ROUND ks_1642_p2: PASS — PASS (checker rc 0 + A2a anchor OK) · golden TREE-IDENTICAL · tip 722e07f19cee · 96s round, 19.61s model, 14774+472 tok` | TREE-IDENTICAL |

Checker lines (each `checker.out`): ks_1645_p1 `A4 ... (3 failed / 5 run; controls green; assertion reds)`, `A5 (5 passed / 5)`, `baseline: total=1132 failed=0 | after: total=1137 failed=0`, `A7 rc 0`; ks_1642_p1 `A4 (3 failed / 5)`, `A5 (5/5)`, `total=1481 | after 1486`; ks_1641_p1 `A4 (2 failed / 4)`, `A5 (4/4)`, `total=64 | after 68`; ks_1642_p2 `A4 (1 failed / 15 run)`, `A5 (15/15)`, `total=1481 | after 1483`. All `NEW reds: []`, A7 rc 0.

## Things Wednesday should read before holding
1. **Tier-1 routing.** KS-1645 edits the admin audit-export route (only refuses more: unknown or repeated `type`); KS-1641 edits an unauthenticated OAuth callback (only shortens the reflected text, same `.slice(0, 200)` as `services/auth`); KS-1642 p1 and p2 are the 409-mapping helper (an unreadable error shape now answers `false`, i.e. the existing 500 path; no recognised error changes). No token or credential is read, issued or compared.
2. **Partials, none closes its ticket.** KS-1645: item 3 validation only. KS-1641: `:465` only (finding 1 and `:515` open). KS-1642: p1 = (b)+(c)+the H10 control, p2 = H9; together they cover all of (a)-(c). The ticket's option for (b) was chosen: make the comment true (the alternative, reword, would leave G1/G3/G4 unpinned) - flag it if the owner prefers the reword.
3. **KS-1642 p1 design note.** The product change is a one-line probe (`try { void [o.originalCode, ...Object.keys(o)]; } catch { return; }`) after `const o = ...`, not a re-nesting of the reads: a re-nested hunk was refused by the builder (every re-indented line equals a removed line stripped of indentation, so it counts as context). A getter that throws only on its second read would still escape (stated in the brief's UNMEASURED).
4. **KS-1642 sequencing.** p2's tamper is `idNamespaceCollision.ts:84`; if p1 merges first that line becomes `:87` and p2's pin must be re-read (round.sh's stale-brief check will say so). The two briefs touch different files otherwise.
5. **Brief defect found (mine, fixed before the model round):** KS-1642 p1 control r1 `FAIL A3b PARTIAL FIX - the product hunk leaves 2 of 2 named site(s) untouched: :67 ... :74`: I had labelled the two lines a pure insertion sits next to as "must change" in `## Where`. For an insertion the neighbours are `(correct)`; A3b counts a must-change site as changed only if the hunk edits that very line. Worth a line in the template next to SCREEN_12's `(correct)` rule. Also: a `test_file=` pin may not equal `ref=` (the builder refused ks_1642_p2's first dry-run); pin a different neighbouring test as `ref=`.
6. **Blank context lines** (builder gate): hunks next to blank lines were written with the blank folded into the change as a `-`/`+` pair (ks_1645_p1 hunk 1 and 2), by `nb_diff.py` in scratch; each golden was checked with `git apply --check` and by applying it to the scratch clone and running the new test (5/5, 5/5, 4/4).
7. **Open-PR overlap NOT checked** on any of the four product or test files (Linear attachments only: none of KS-1641..1645 has one; GitHub not queried).
8. Housekeeping: `spark/cache/work/` gained about 10 per-round clones (not pruned); the cache clone fetched develop `9b90f8ac7..722e07f19`.

## NOT done
- No rebrief used; nothing held or raised. No GitHub or Linear read of PR state.
- Not measured: the whole-suite runs beyond the checker's A6; real security service / real Postgres / real browser for any piece; KS-1645 items 1, 2, 4 and "the filter actually filters"; the production behaviour of the m365 redirect target; a stateful (second-read) throwing getter for KS-1642; the Windows-style / UTF-16 boundary of the 200-char cap.
- Not briefable from this pool (decisions or outside tier): see SKIPs. With seats R/E/C/J/G still holding the verification/documents/anchors/certifications/platform files, most of the rest of the pool is "a decision first" (as SCREEN_12 found).

## Files written
Briefs: `local-model/night/briefs/ks_1645_p1/`, `ks_1642_p1/`, `ks_1641_p1/` (each `KS-<n>.md`, `golden.diff`, `spark.pins` tier=code_patch, ref=, line=, ctx=65536), `ks_1642_p2/` (tier=test_only, test_file=, ref=, line=84, ctx=65536). Run dirs (round.sh's own): `spark_secuura_2026-10-19_ks_1645_p1`, `_ks_1642_p1` (+ `-control`, `-control-r2`), `_ks_1641_p1`, `_ks_1642_p2` (+ `-control` each). Scratch (not durable): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fab5379f-182f-40a2-8bd3-ff9052525009/scratchpad/spark_screen13/`.
