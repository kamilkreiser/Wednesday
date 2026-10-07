# DRAFTER REPORT: Seat R 13th launch brief (Secuura/Blockchain-R)

**Brief:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-08_seatR13_5d_raise_prs.md`. It is 203 lines, sha256/16 `d763967dee30794e`. It is staged only: not sent, not launched.
**Drafted:** 2026-10-07 13:2xZ to 13:36Z (2026-10-08 00:2x to 00:36 AEDT). The drafter wrote nothing under `!CODING/`, sent no mail, touched no ticket, PR or pane, and deleted nothing. Its network git verbs ran only in its own `clone --shared` scratch clone (`r13d_clone`). The shared `rev-parse --all` was byte-identical (`cmp`) before and after.
**Usage at drafting:** `usage_gate.sh --check` printed `ADVISORY — weekly usage 79% >= 70%` and `OK — weekly usage 79% < 90% (gauge age 6 min)`, rc 0.

## What changed since R 12th's brief
- **develop = `3d570510bdb3`**, R 12th's #1410 squash. It was unmoved from 13:23:51Z to 13:35:08Z (two `ls-remote` reads). gate73 is 4 of 4, so the brief has **no merge queue**.
- **New PRs:** #1418 and #1419. #1419 is KS-1361, Peter's lane. It touches 4 `systemTest/schemathesis/` paths, none of the payload paths, and neither doc.
- The doc tails at develop match the brief exactly. Flow ends `… 28 29 25 30 31` (29 numbers, 0 duplicates; `26` and `32`-`39` absent). Cheat ends `… KS-1136 KS-998 KS-1313 KS-1435 KS-591`. Both have planted controls.
- All three §5d sites were re-located by hunk: `:180`, `:412`, `:1630`. Both text-search controls reproduce (`:403`+`:412`; nine `.uuid()` lines).
- All five payloads plus the KS-1164 control variant re-hash equal to R 10th's table. Each strict-applies with rc 0 at develop in a temp index. The R3+R4 stack gives tree `deb5dd43edc5` in both orders. Applying R3 twice fails, as it should.

## Findings the brief acts on
1. **develop's objects are not in the shared store.** `cat-file -t 3d570510bdb3` reads "Not a valid object name"; the control `652cf5f6` reads commit. A raise worktree at RAISE_BASE needs one objects-only transfer first, or a boot pull. Covered by Q-OBJ13.
2. **The `r 13th` trap is live.** The parsed `OTHER_SEATS` (`inbox_matchra1.py:222`, entries at `:254`) contains `"r 13th"` and `"seat r 13th"` (`ast.literal_eval`, 171 members).
3. **The sweep class is wrong again.** R 12th's `(?:[1-9]|1[013-9])` matches 13 and not 12. The expected `(?:[1-9]|1[0-24-9])` was proven in python: it matches 1-12 and 14-19, not 13.
4. **KS-1139 carries 0 ticket references.** That is a SKILL §5d gap; KS-1274 and KS-1410 carry their keys (5 / 8 / 10 `+` lines). The brief holds R5's commit on Q-5D1139.
5. **§4 binds KS-1139** because it adds a test suite. #1383 is precedent for doc blocks on a `scripts/__tests__` bash suite. KS-1245's #1207 left 0 doc mentions (control `ks-591` = 2), which is a skipped duty, not a ruling.
6. **KS-1139 re-proved by the drafter** on bash 3.2.57:
   - The new suite fails at the tip: rc 1, 3 passed / 3 failed.
   - It passes with the fix: rc 0, 6/0.
   - The sibling suite is 5/0 both before and after; `bash -n` rc 0.
   - The new file lands 100644, the same as its sibling. The runner globs it (`run-shell-suites.sh:49`, `:65`).
   - KS-1250's canonical sections stack with KS-1139 in both orders, same tree `99a71729e33d`, so the two are disjoint.
7. **The `page_token` lesson is in R 12th's WRAP only** (`:89-94`). The handover has 0 mentions (control "provenance" = 4), although WRAP `:93-94` says it is there. The brief carries it from the WRAP.
8. **`_COPY_HASHES_ra12.txt` holds R 11th's pre-re-key hashes.** Seven of R 12th's re-keyed tools therefore will not match it. The brief gives R 12th's actual 20 hashes. `provenance_ra12.py` `16ce6b013eacfbd4` and `m7_squash.sh` `381c2a2188678a56` match the WRAP.
9. **`m7_squash.sh` is hard-wired to #1410** (worktree, GO v2, body and PR are literals). Handover `:131` says to re-key it. The brief holds it unrun because this seat has no squash.
10. **Instrument notes from this draft:**
    - zsh read `"$D:Projects Documents/…"` as the `:P` modifier. I caught it and used `${D}`.
    - My session scratchpad already held a stale `clone/`. One fetch went into it, objects only with no FETCH_HEAD write, before I moved to a fresh `r13d_clone`.
    - Eleven mail line citations were off by 2 because I took them from a `sed -n '3,$p' | cat -n` view. I re-read them against the files and fixed them before stamping.

## Open questions (each with the drafter's recommendation)
- **Q-N1139: flow number for KS-1139.** Recommend that §4 binds and the flow block is **`37.`** (next free after `36.`, unreserved), with a cheat section keyed KS-1139.
- **Q-5D1139: the payload has no §5d comments.** Recommend **(a)**: apply the payload byte-for-byte, then add one WHY + KS-1139 comment line above `pass()` and one `Refs` line in the suite header, in the same commit. Re-run red/green, the sibling suite and `bash -n` after. The body gives both the payload hash and the committed diff's hash. The alternative (b) is to raise byte-identical and name the gap.
- **Q-TIER1139.** Recommend **TIER 1**: three lines of one shape, red-first proved, not an auth surface. Choose TIER 2 if Wednesday wants a bash ≥ 4.1 (Linux) run before merge.
- **Q-KEY1139.** Recommend **KS-1139 as the PR's own key**, hyphenated once, with `KS 1148` de-hyphenated. Neither ticket closes.
- **Q-OBJ13: develop's objects are missing from the shared store.** Recommend **one objects-only transfer by SHA** from the seat's scratch clone, under the lock, with a `rev-parse --all` bracket and a `deadbeef` control. It is a recorded no-op if the boot pull brings the objects.
- **Q-SCOPE13: re-key scope.** Recommend: copy, hash and sweep all 20 tools, but **re-key only the tools the seat runs**. The merge-only tools (builder, mergein, mergera1, m7_squash) stay un-keyed and unrun, and are declared so. This saves boot budget.
- **Q-5D-MERGE13: who merges the §5d PR.** Recommend **it ends at READY FOR READ; this seat does not merge it**. The gate73 builder's GO literal is `on gate73` (`:103`) and its parsers expect a gate73 GO, which a tier-3 comment-only PR does not have. If a GO arrives anyway, the tool wins: mail the mismatch.

## Unmeasured by the drafter
- Linear: no access. Ticket states are relayed from R 12th's ITEM 0 (f). KS-1139 and KS-1148 are relayed from the Spark brief; KS-1148's state was read by nobody in this chain.
- Any bash ≥ 4.1 run.
- Whether a D successor or E 11th is live.
- What `run_shell_suites.test.sh` prints with one more suite.
- The pre-push hook's package selection.
