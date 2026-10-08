# Drafter report: Seat R 19th launch brief (2026-10-08)

**Brief:** `2_Project_Files/fleet/briefs_staged/2026-10-08_seatR19_raise_r3r5_ks1410_ks1139.md` (188 lines). Staged, NOT sent. SEND AMENDMENT left as one `@@FILL@@` line; SELF-CHECK as `@FILL@`. A grep for `@`-tokens finds only those two.

## commitra3.sh lock-release finding (R 18th's copy, sha256/16 `f1357d1a956984fb`, 224 lines)
| defect (G 4th / EF addendum) | verdict | where |
|---|---|---|
| `LOCK_SEAT` override | ABSENT | `:61` requires it from the env; no assignment or export anywhere |
| release rc read through `echo "$?"` | **PRESENT, different shape** | `:172-173` `echo "$(now) release rc=$? : …"`: `$(now)` resets `$?` before it expands. Replica on `/bin/bash` 3.2.57 with the release forced to rc 3 printed `release rc=0` |
| release check in the EXIT trap after the status is set | **PRESENT** | `:174` `trap release EXIT`; `release()` checks nothing and never exits; same replica exited 0. No post-release "lock gone" assertion exists |
| release test on the wrong lock dir | ABSENT (there is no release test) | lock dir parsed from `lockra1.sh:217` (`.push-lock-d8`); holder pid read from it at `:168` |
| (extra, found here) | PRESENT | `:171` exits 2 after a successful take and before the trap is armed, so the lock stays HELD |
| (adjacent) `pushra1.sh` | same class | `:267` bare release with `$$` and no rc read; exit is the push rc; `:229`/`:238` `|| true` |
The brief tells R 19th to fix these before its first commit (Q-COMMITFIX19), with the EF addendum's red-proof.

## Measured (all 2026-10-08, instruments are in the brief's PROVENANCE P1-P13)
- `ls-remote` 07:13:07Z: develop `0a6177ea5482` unmoved, #1427 head `2b6da5f561b0`, highest pull 1427, lane-token counts with controls.
- Shared store: develop objects PRESENT (`cat-file -e`, positive + negative controls), so Q-OBJ19 expects a no-op. `rev-parse --all` reads 1,636 (R 18th's wrap read 1,635; the extra ref is G 4th's quarantine ref). `cmp`-identical across my scratch clone.
- Doc tails at develop and on #1427's blobs (newline-tolerant reader, document-shaped controls).
- Payload bytes/hashes, strict apply forward/reverse, trees, R3+R4 stack both orders, R3-twice control rc 1, R3+R4+R5 stack `ff435e3b58bb`. All of R 18th's figures reproduce.
- All 14 inherited tool hashes match the handover table.
- Matcher membership by `ast` (`r 19th` trap is live; `g 5th` is absent). Sweep class: 9 occurrences.
- Locks (1 held: G 4th's `g1`, holder `g4`), worktrees, tmux panes, `df -m`, usage gauge.
- The parallel-seat standing block is `cmp`-identical to the learning's `:86-91`.

## Not measured
- Linear (no access): every ticket's PROVENANCE line is left for Wednesday at send.
- GitHub API (no token): open-PR state, #1427's `mergeable_state`/Actions.
- G 5th's pane, lane token and lock (not launched).
- SKILL / repo `CLAUDE.md` line numbers: carried from R 18th's brief. develop has not moved, so they should still hold. Flagged in UNMEASURED.

## Departures from the predecessor brief, and why
1. **No QUEUE B / board write.** KS-1450 is Done (R 18th). The HOLDS say this seat writes nothing on the board.
2. **Queue is R3+R4 then R5 only.** R2 is #1427. R 18th's trivy paths are removed from R's payload row, and #1427 and its worktree are added to never-touch.
3. **New COMMIT TOOL FIX section**, from the task and the EF/G 4th findings.
4. **Partition rewritten as it is now:** actual pane ids `%96`/`%97`/`%98`, a G 5th row for KS-1171 (token/lock UNMEASURED), the held `g1` lock with its holder, and the "Now" column.
5. **Sweep line numbers:** the handover says `:19 :31 :43 :49 :50`. Two instruments read `:18 :32 :44 :50 :51`. The brief states both and says the file wins.
6. **New arm: add `g 5th`** to `OTHER_SEATS` (absent by `ast`). Q-G5-19 was added.
7. **Q-OBJ19 recommends a no-op.** R 18th's Q-OBJ18 flipped to a transfer, but the objects are now present.
8. **Stack figure:** the four-row `2bb2e5d9bd01` is replaced by the three-row `ff435e3b58bb`, and the brief says why.
9. **Usage:** the gauge is now **90%**. The bare gate REFUSES (rc 3). With `WED_USAGE_STOP=100` it is OK (rc 0). **Wednesday must launch with the grant's stop set, or the launch tools will refuse.**
10. **Q-LOCK56-19 recommends reconciling, which differs from R 18th's "leave it".** STANDING_LINES `:415` requires the two tools' WAIT sets to be identical, and I measured that `lockra1.sh`'s loop already skips an empty slot. The default is to reconcile.
11. Q-LOCK18/Q-NUM18/Q-R2WT18 are moved to RULED. Q-SCOPE becomes Q-SCOPE19.
12. Added calibration from R 18th's push (legs, leg 14 green, ~8 min, the hook log's location), the `lockra1.sh:230` stale `ra16` prose, and the engines gap widened to three packages.
