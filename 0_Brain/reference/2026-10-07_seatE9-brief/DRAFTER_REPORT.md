# DRAFTER REPORT: Seat E 9th raise brief (4 held Spark passes)

Drafted 2026-10-07 12:09-12:2x AEDT (01:03Z-01:2xZ) by Wednesday's brief drafter. Nothing was sent, launched, pushed, commented or written outside the brief, this file and the drafter's scratchpad (`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/01e35370-cae1-4af3-98f7-77582de84f4d/scratchpad/e9/`).

Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-07_seatE9_raise_spark4.md` (146 lines).

## What I measured, and how

| Fact | Value | Instrument |
|---|---|---|
| develop at origin | `69f2045af2a4f5f0b83b2f76c62514512abdc7b5` (#1404's squash; #1398 NOT yet landed) | `ls-remote` with the checkout's own `core.sshCommand`, `GIT_SSH_COMMAND` unset, 01:03:44Z-01:03:49Z rc 0, 2,104 lines |
| Shared store | `69f2045` present (R 7th's transfer); `deadbeef` absent; `rev-parse --all` 1,610 lines sha256/16 `45e4418378f83e7e`, `cmp` rc 0 before/after my clone + fetch; `.git/config` `4f624a213933d54b` both readings; local `develop` and `origin/develop` both `69f2045af2a4` | read verbs only |
| Strict apply at develop | E1 KS-1435 `e7f6d8d5c74f`; E2 KS-591 custody `7c72a4cdaf2e`; E3 KS-1432 `7fef637e0fb3`; E4 KS-591 tenant-id `7a8ed91afa2c`; create-status `d53612da0a7d`; KS-1364 share/system-errors `58157c9a2b45`. Check 0 / apply 0 for all six | temp `GIT_INDEX_FILE`, `read-tree` + `apply --cached --check` + `apply --cached` + `write-tree` in my `clone --shared` scratch clone after a by-SHA fetch from the GitHub URL |
| Tamper controls | all six: check rc 1, each at its first hunk (`index.ts:411`, `originate.openapi.ts:1629`, `verification.ts:259`, `tenant-provisioning.openapi.ts:454`, `:360`, `originate.openapi.ts:1601`) | one context line suffixed `X`, `cmp` rc 1 vs the original |
| Payload identity | each 10-07 payload `cmp` rc 0 vs its `-control` run (tenant-id vs `-control-r3`) | `cmp` |
| YAML companions | all four strict-apply at develop (yaml blob `2577a35fadab`), incl. the two cut at `52310cab` on 10-05 | same temp-index method |
| Sibling landings | 9 pairs (code + yaml) `merge-tree` rc 0 after the other lands; positive control (two flow-doc tail appends) rc 1 | `commit-tree` + `merge-tree --write-tree` in the scratch clone (`sim.py`, `simctl.py`) |
| Open PRs | 23 open; 0 touch any E-row file or `secuura-api.yaml`; `Projects Documents/` only #1383, #1398; 11 PRs carry a `package.json` (control, == R 5th's count) | GitHub REST GET, 01:05:00Z-01:05:30Z |
| Linear | KS-1435 Backlog board att `pull/1403`; KS-591 Backlog board 0 att; KS-1432 Backlog board att `pull/1403`; KS-1364 In Progress board; KS-565 Backlog board; **KS-529 Done + ARCHIVED**; KS-572 Done (Peter) | GraphQL read-only 01:07:08Z, HTTP 200 each |
| Docs at develop | flow `f9935e1cfe8c` 3,226 lines, `</body>` `:3224`, numbered `1-16, 18-24, 27`; cheat `191bb32270c5`, tail keys `KS-1305, KS-1436`; planted split `<h2>` HIT by the newline-tolerant reader, MISSED by the same-line one | `h2.py` over `git show <sha>:<doc>` |
| §4 applies? | yes: skill `b59b74a592e9` `:362`-`:363` "Every test change … backend unit, integration, *or* systemTest"; 13 of 13 service-test squashes from #1374 to `d75bfe2de` carry both docs (the 11 before, incl. #1365/#1368, carry 0) | `git diff-tree` over develop's last 60 first-parent commits |
| E lane tools | E 8th's matcher `MINE "e 8th"` with `e 9th` IN OTHER_SEATS (must be removed); OTHER_SEATS lacks `r 4th`-`r 8th`, `d 10th`-`d 16th`, `e 8th`, `g 3rd`; namecheck `MINE "e8"`, FOREIGN lacks `e8`, `seate8`, `ra2`-`ra7`, `d10`+; lock WAIT `-56 -f3 -g1 -d8` in both tools; `commite4.sh:26` stale `b57` knob | AST read without import, `grep -n`, `shasum` |

## Answers to what I was asked

- **Per-pass strict apply:** all four pass at `69f2045`, plus both other held passes; every tamper refuses.
- **The tenant stacking:** the "must stack AFTER create-status" premise holds only as "measured in that order". I measured both orders: **identical tree `625d0d4b6f1e`**, and after either lands the other merges clean (`merge-tree` rc 0, yaml included). So **no rebase is needed either way** (and Secuura never rebases a pushed branch anyway).
- **KS-1364 share/system-errors:** same file as the custody carve, disjoint lines (`:1601/:3763/:3911` vs `:1630`); both orders give tree `212d96a280f9`. It CAN go in this round, but as a different ticket it is a 5th PR. I made it optional row E5, default UNRAISED.
- **Doc blocks:** yes for every PR (§4 plus the measured precedent). Both docs are R 7th's until #1398 squashes, so RAISE_BASE has to be post-#1398. Next free numbers: `30.`-`34.` (`28.` = #1398, `29.` = KS-998, `25.`/`26.` = KS-1313/KS-1164 reserved, `27.` on develop).

## Open questions, each with a recommendation

1. **Q-BASE9: wait for #1398, or raise now on `69f2045`?** **Recommend waiting.** RAISE_BASE = develop after #1398's squash, accepted by name. Raising now means writing doc blocks into files R 7th is merging, or leaving them out against §4, and then re-composing them at merge-in time. The cost is idle time if #1398 stalls. If it has not landed within about an hour of E 9th's ITEM-0 ANSWER, Wednesday should re-rule rather than leave E 9th waiting.
2. **Q-STACK9: bundle create-status with tenant-id in one PR?** **Recommend (a): bundle.** It is the same ticket (one `Refs KS-591`), the same file, the same service, one test pass, one YAML regeneration and one doc-block pair, and it saves a PR build, a gate row and a later docs merge-in. Against it: create-status was held on 10-05 at `3ce8cd40`, so its proof is two days older (product blob unchanged, measured). E 9th re-proves it at RAISE_BASE either way. Its REVIEW measured it as security-adjacent but unable to change any auth decision. The fallback (b) is to raise it as its own PR ahead of tenant-id.
3. **Q-E5: raise KS-1364 share/system-errors in this round?** **Recommend leaving it UNRAISED by default.** E 8th hit 47% after one merge. Four rows is already more than one seat is likely to finish before the 45% line. Let it in only if the ctx read after E4 is under 45%.
4. **Q-KEY9: two cheat sections both keyed KS-591 (E2 and E4).** **Recommend distinct titles with the key at the end of each heading.** Wednesday should confirm whether the next gate's "keyed" check needs unique keys. If it does, add a carve suffix inside the heading text before the key.
5. **Q-N9: flow numbers.** **Recommend `30.` KS-1435, `31.` KS-591 custody, `32.` KS-1432, `33.` KS-591 tenants, `34.` KS-1364**, unique and keyed by ticket. If E 9th's base shows a collision, E 9th stops and mails.
6. **Q-XFER9: transfer RAISE_BASE into the shared store?** **Recommend yes, if needed.** Check `cat-file -t` first, because R 7th's Q-XFER7 may already have transferred it. Otherwise do one objects-only transfer under `.push-lock-e4`.
7. **KS-1435 "Closes as filed" (its brief) against our "Refs only" rule.** **Recommend `Refs KS-1435`.** No closing keyword ever goes in PR text, and §5f holds Done until a live sweep in any case.
8. **E 8th's ITEM 3 residue (N-1396-*) is not in this brief.** N-1396-4 names stale `verification.ts:1283` cites, which is E3's file. **Recommend keeping it out of this round and noting the overlap for whichever seat drafts it.**
9. **Colliding doc number on #1383 (F lane, `22.`).** This is not E 9th's problem, but it collides with develop's `22.`. **Recommend that Wednesday carries it to #1383's own merge-in.**

## UNMEASURED

- Every red/green/suite/tsc/`check:openapi`/push figure at the real RAISE_BASE. No `npm` was run by the drafter, so the YAML regenerated from source is unmeasured and the companions are expectations only.
- The E3 call-site-deletion arm: the brief says it is not unit-pinned; I did not run it.
- R 7th's and D 15th's live pane state (no tmux read). #1398's landing time.
- Whether `pushe7.sh`'s argv contract matches the invocation shape in the brief. The brief tells the seat to re-read it from the tool, which wins.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-07 12:24
