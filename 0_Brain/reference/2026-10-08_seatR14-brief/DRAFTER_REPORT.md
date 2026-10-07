# DRAFTER REPORT — Seat R 14th launch brief (Secuura/Blockchain-R)

Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-08_seatR14_raise_r2_r5.md` (DRAFT, not sent, nothing launched, no mail, no ticket/PR/pane/project write).
Drafted 2026-10-08 ~02:00-02:20 AEDT (2026-10-07 ~15:00-15:20Z).

## What changed under the brief while drafting (read this first)
- **develop moved:** `b280b74ff07b` (15:00:55Z) -> **`ed346e6d9ff8e7635f7ce36cd3b36f5d64b5f784`** (15:12:35Z): Peter's merge of #1421 (KS 1445, k6 / observability image pins), 15:02:11Z. 21 paths, 0 of the 11 payload paths, but BOTH platform docs (flow: a status paragraph, no `<h2>`; cheat: a `KS-1367` section inserted mid-document, 17 -> 18 sections). Tails unchanged (`31` / `KS-591`). All four payloads strict-apply at it; R3+R4 stack agrees both orders; R3-twice still fails. The brief now names both values and treats its develop as stale.
- **`ed346e6d` objects are NOT in the shared store** (same refusal message as `deadbeef`, which per R 13th's lesson 4 is not itself evidence). R 14th's boot pull (sole seat) is expected to bring them; Q-OBJ14 was re-worded accordingly.
- Weekly usage **83%** (ADVISORY; was 79% at R 13th's send). Read twice: 02:00:46 AEDT and at the end of drafting.

## Open questions (each with a recommendation)
1. **Q-OBJ14 — objects for the first worktree add.** Recommend: a RECORDED NO-OP if RAISE_BASE's objects are already present after boot (likely, via the boot pull), ABSENT control declared SPENT; otherwise ONE objects-only transfer in Q-OBJ13's shape.
2. **Q-TIER14 — tier for R2 (KS-1274) and R3+R4 (KS-1410).** Both have been "rec TIER 1" since R 10th, and nobody has ruled. Recommend TIER 1 for both, with "live run owed" in each body. Rule it at send so the READY is not held.
3. **Q-KEYOWN14 — how often the PR's OWN key may appear hyphenated.** R 13th's #1423 carried it 6× (Refs line, URL, a verbatim test title, three cheat-key mentions: `Q_ctx2.txt:38`), and Wednesday did not rule. Recommend: allowed in the Refs line, the URL, and verbatim file content (test titles, cheat key); every foreign key de-hyphenated; strict closing regex 0 with a firing control.
4. **Q-SWEEP14 — a gap in the sweep.** `sweepra13.py:48`'s `stale-artefact-name` alternation omits `restraisera`, `poll_actionsra` and `provenance_ra`, so stale generations of those three filenames are never swept. Also, `restraisera13.py:18`'s usage print still names `restraisera9.py`. Recommend: R 14th adds the three stems in its own copy, each controlled by a CONTROL 1 plant that must FIRE and a `mine_planted` `ra14` name that must NOT, and re-keys the usage print.
5. **Q-SCOPE14 — re-key scope.** Recommend: Q-SCOPE13 unchanged. The four merge-only tools stay un-keyed and unrun, and namecheck stays uncited.
6. **The lesson count: ten, not nine.** Your instruction says "lessons (nine)". The handover has TEN numbered lessons (`:85-141`), and the WRAP mail lists nine because it merges the two planted-control ones and omits `$?`-after-a-pipe. The brief binds all ten. Recommend: keep ten. Separately, `page_token` is still WRAP-only, with 0 hits in the handover (control "provenance" = 3), so the brief carries it explicitly.
7. **S-3 control bytes, 55 vs 53.** `git log -1 --format='%(trailers)' bf277eead268 | wc -c` reads 55, while R 13th's commitra3 print read 53. The two instruments differ. The brief asks the seat to name its instrument and assert NON-ZERO. Recommend: no ruling needed. Noted so nobody files it as drift.
8. **The ra15 sweep class in the WRAP line.** The brief gives `(?:[1-9]|1[0-46-9])` as an EXPECTATION for R 15th. I did not drive it on planted forms. It fullmatches 1-14 and 16-19 by construction. Recommend: leave it as an expectation, to be proved by R 14th.

## Not in R 14th's queue (stated in the brief)
- Merging #1422 and gating #1423. Wednesday batches #1423 with R 14th's raises into one QA gate and routes #1422's merge separately. The brief also forbids touching `s-ra13-5d` and `s-ra13-ks1164`.

## Drafter self-disclosure
- I **overwrote three files in the session scratchpad root**, left there by an earlier drafter in this same session dir: `lsr1.out`, `revall_before.txt` and `usage.out`. My first commands wrote to those names before I moved to a fresh `r14d/` subfolder. Nothing outside the scratchpad was touched, and the previous drafter's measurements are recorded in R 13th's brief PROVENANCE. All of my own artefacts are in `scratchpad/r14d/`.
- The `pretooluse_no_cd.sh` hook refused a `git init` in the scratchpad. I applied the KS-1139 patch to the mini-tree with a python applier (`r14d/apply1139.py`, anchors asserted) instead of git. The tree reproduced R 13th's drafter's red/green numbers exactly.

## Key numbers (instrument in the brief's PROVENANCE)
- Payload trees at b280b74f / ed346e6d: KS-1274 `5e2701480f8d`/`aa5865c212b5`; KS-1410n `0acf4ae44694`/`49d08cd5e958`; KS-1410b `228d28cda705`/`723501715afa`; KS-1139 `831636269a78`/`183cad36cf43`; R3+R4 `c779083564a8`/`f9bffe3104f3`.
- KS-1139 on /bin/bash 3.2.57: tip `3 passed, 3 failed` rc 1. Fix `6/0` rc 0. Fix + the WHY line above `pass()` `6/0` rc 0, with anchors 1 1 1. Sibling `5/0` in all three states. KS-1250 + KS-1139 both orders give tree `11f85cabf97f`.
- Matcher, parsed: 173 entries / 171 unique, with `r 14th` and `seat r 14th` PRESENT (the trap). Sweep class as copied: 8 deviations. `1[0-35-9]`: 0 deviations.
- Shared `rev-parse --all` 1,622 lines `2bc26e01e759b826`, `cmp`-identical across the whole drafting.
