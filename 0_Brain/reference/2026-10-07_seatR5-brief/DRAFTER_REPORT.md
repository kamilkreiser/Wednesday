# Seat R 5th brief: drafter's report (2026-10-07 02:1x-02:3x AEDT, i.e. 2026-10-06 15:11Z-15:31Z)

**Brief:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-07_seatR5_raise_prs3to5_and_merge_gate71.md`. It is staged only: not sent, not launched. The `send_brief.sh` gates were run with `SEND_BRIEF_DRY_RUN=1` (rc 0, "all gates PASSED, nothing sent"; recipients resolved to `secuura-blockchain@agentmail.to`).

**Writes made:** the brief, this report, and scratch files under this session's scratchpad. In the Secuura project I ran READ verbs only (ls-remote, log, show, cat-file, ls-tree, rev-parse, diff). Every write verb (fetch, worktree, commit-tree, merge-tree, npm ci) ran in my own `clone --shared` scratch clone. Shared store `rev-parse --all`: `cmp` rc 0 before vs after the whole session (1,608 lines, sha256/16 `1d486de42c80b2bc`). `.git/config` `4f624a213933d54b` unchanged. `FETCH_HEAD` still at `2026-10-05T10:46:17Z`. The gate71 kit folder was read only, never edited.

---

## 1. Headline findings (Wednesday needs all four before sending)

1. **develop moved again, after R 4th's READY.** It is now `b39051390ff6` = #1405 (PeterObeden, merged 14:57:35Z, `5_Project_History/history.md` only, +36) on top of `40270d26`. The two doc blobs are the same as `40270d26`'s.
2. **#1402 renumbered the flow doc. Nobody has recorded this.** At `d75bfe2` the doc's tail was `22.` = KS-1305. At `40270d26` it is `22.` "Measured timings", `23.` "KS-571 refresh", `24.` KS-1305 (moved). So two of your rulings now collide with numbers develop already uses:
   - #1398's ruled `23.`
   - KS-998's ruled `24.` (Q-N)

   The widened gate asserts that numbers are UNIQUE, so it will fail #1398 as it stands. `25.`, `26.` and `27.` are still free. #1383 (F lane) carries a `22.` too.
3. **The shared store does not hold `40270d26` or `b3905139`.** I checked with `cat-file -t`, with `d75bfe2`/`c117`/`9414` present and a `deadbeef` control. The merge job needs develop's objects in that store whatever base you pick, so one objects-only transfer (STANDING_LINES `:404`) is needed. It is an ASK (Q-XFER5).
4. **The KS-1313 toolchain moved under the payload.** In `systemTest/performance`, vitest went 4.1.11 to 5.0.3 and @typescript-eslint 8.65 to 8.71.1. The payload's own comment says its fixtures were "captured from real vitest 4.1.9 JSON reports".

## 2. The base question: measured, with a recommendation (Wednesday decides)

| Measure | `d75bfe2` | `40270d26` / `b3905139` |
|---|---|---|
| Strict apply, 3 payloads (check / apply rc) | 0/0 ×3, trees `b5c790f8e7c9` `85eed054a3fe` `19e394344401` (= R 4th's handover) | 0/0 ×3. At `40270d26`: `e81c1e334577` `253a816ccada` `aafbb33a5101`. At `b3905139`: `5a60eebbee83` `475551ee035a` `8ffd3c2895d8` |
| Tamper control (KS-998 `Whose red` -> `RED`) | rc 1 at `:177` (R 3rd/R 4th) | rc 1 at `check-package-format.sh:177` (mine, at `b3905139`) |
| Product paths that differ (3 payload paths + `report.ts` + the 2 new test paths) | — | **0 of 6.** Blobs `cfae0cc6f48c` / `00103d946cc9` / `ac59af37cbc6`; new paths absent; 0 paths under `Blockchain/` |
| The PRs' package toolchain | vitest 4.1.11, ts-eslint 8.65 | vitest 5.0.3, ts-eslint 8.71.1 (+ eslint, prettier, tsx bumps) |
| The guard (`html_docs_matrix.test.sh`) | absent, so it runs first at merge-in | present (discovery 67 -> 68); runs in the pre-push hook at the raise |
| Old-format block (prose) on develop's docs | — | **fails**: #1404's fragment 3 + 4 findings; #1398's 8 + 2 |
| Matrix-format block on develop's docs | — | passes 0 / 0 |
| Doc work per PR | composed twice (old now, gated re-composition at merge) | composed once; later merge-ins are a mechanical keep-both (simulated sibling x sibling: rc 1, both docs only) |
| Objects transfer for the raises | none | one (needed for the merges anyway) |

**My recommendation: raise on develop at R 5th's ITEM-0 ANSWER (expected `b39051390ff6`).** Three reasons:
- The tests get proved on the toolchain that will run them after merge.
- The guard checks the block at the seat's own push, so the block is composed once.
- `systemTest/CLAUDE.md` MUST 1 says "create a branch off `develop`".

**The alternative and what it costs:** `d75bfe2` needs no transfer for the raises. But it proves PRs 4 and 5 on vitest 4.1.11, which will not ship, and it doubles the doc work. Every PR 3-5 block then needs a re-composition merge-in through the gate's text-conservation step, which is the same cost #1404 and #1398 now carry.

**A risk that comes with the recommended base:** vitest 5's JSON report might not carry a field the KS-1313 code reads. In my scratch the green half points to no:
- `40270d26` + PR 4 + PR 5 under vitest 5.0.3: **13 passed (13)**, rc 0, 5.62 s.
- Red-first was NOT driven.

The brief makes this a capture-and-compare item for the seat, with a STOP if any field differs.

## 3. What I measured: FOUND / TESTED / HOW, with controls

- **Refs.** FOUND develop `b39051390ff6`, #1404 `c117c0160684`, #1398 `9414aa54e92c`, highest pull 1405. TESTED twice, at 15:11:30Z and 15:23:32Z, same result. HOW: `env -u GIT_SSH_COMMAND git -C <checkout> -c core.sshCommand=<its own> ls-remote <GitHub URL>`. Token `ra5`: 0 raw / 0 bounded (control `ra4` 1/1).
- **What moved.** FOUND `d75bfe2..40270d26` = #1400/#1401/#1403/#1402, 189 paths (systemTest 170, observability 15, 2 docs, CLAUDE.md, .claude); `..b3905139` adds #1405, 1 path. HOW: `log --first-parent`, `diff --name-status` in the scratch clone after a by-SHA fetch (`deadbeef` control fails).
- **Strict applies.** As tabled. HOW: temp `GIT_INDEX_FILE`, `read-tree`, `apply --cached --check`, `apply --cached`, `write-tree`, `diff-tree --numstat`. CONTROL: a tampered patch fails.
- **The guard.** Read whole (99 + 129 lines). TESTED both ways with the project's own checker (node v24.7.0):
  - develop's docs: 0/0
  - `d75bfe2`'s docs: 169/90 (the positive control)
  - old fragments composed onto develop: 3+4 and 8+2
  - simulated matrix blocks: 0/0
  - `html_docs_matrix.test.sh` on a scratch worktree: 12 passed, 0 failed

  Fragments were extracted as the head minus the base (the removed bytes were 0, so the insert is boundary-free) and composed with `out.replace(frag,"",1) == develop` asserted.
- **Docs.** FOUND flow `49000270a211`, 23 blocks, order `1-16 18-24`, `</body>` `:3179` at column 0. Cheat `67fed69fa021`, 11 KS sections, tail KS-1305. HOW: a newline-tolerant reader; a planted split `<h2>` is HIT 1 by it and missed (0) by the same-line reader.
- **Toolchain.** FOUND from the lock files and the package.json diff. TESTED in a scratch worktree (`npm ci --ignore-scripts` rc 0; 25 EBADENGINE because host node 24.7.0 < `secuura-performance`'s own `>=24.11.0`, which holds at BOTH bases).
  - vitest 13/13.
  - eslint: rc 0; a planted `void` gives rc 1 (`no-meaningless-void-operator`).
  - 🔴 tsc: **`tsconfig.json` does not cover the test files** (a planted error still gives rc 0), while `tsconfig.node.json` does (planted error rc 2). A future "tsc rc 0" quoted on the wrong config proves nothing about these tests.
- **KS-998 on the new base.** The new test gives 8 passed, 0 failed (scratch).
- **Shell-suite counts.** `ls-tree` over both roots: `d75bfe2` 67, develop 68, R 4th's and R 3rd's heads 68 each (a different set), a PR-3 head would read 69.
- **Merge shapes.** `merge-tree --write-tree` against `b3905139`: #1404 rc 1 and #1398 rc 1, both docs only.
- **Lock tool census** (R 4th's `lockra1.sh` / `pushra1.sh` / `twolockra1.sh`, grep with counts): tabled in the brief. The live R 4th lines are at:
  - `lockra1.sh:224`, `:230`
  - `pushra1.sh:160`
  - `twolockra1.sh:41`

  The foreign-holder rc 12 is at `lockra1.sh:505`-`:508`. 0 locks are present.
- **Merge tools (R 2nd's).** FOUND that `mergeinra2_1395.sh` printed `VERDICT: FAIL` (5 failed of 43) on R 2nd's own #1395 merge, through stale #1394 gates (`:157`-`:176`); Wednesday overrode it for that commit only. Also: `build_addendumra2_1395.py` hardcodes R 2nd's REC, GO file and #1395 regexes, and `mergera1.py` reads `MERGE56_SCRATCH`. All of this must be re-keyed before R 5th merges anything (Q-TOOLS5).
- **Linear** (read-only, HTTP 200): as in the brief. KS-1313 is still UNASSIGNED (Q-A owed).
- **Open PRs** (GET only): 24. No overlap with PR 3-5 paths. Docs PRs open: #1383, #1398, #1404. Control: 11 PRs carry a `package.json`.
- **Rules.** The skill at `40270d26` = `b59b74a592e9`, and `head -642` is byte-equal (`cmp` rc 0) to `eaf43dfd4d98`. So §4/§5 are unchanged; only §6e (LTS-only) was added. The root CLAUDE.md added the same LTS rule. `systemTest/CLAUDE.md`'s MUST block is unchanged. This closes R 4th's UNMEASURED "whether §4 changed": it did not.
- **`send_brief.sh` gates.** Dry run rc 0. Separately, every hyphenated KS id in `## QUEUE` was checked against PROVENANCE: 8 of 8 present.

## 4. Where the handover (or another record) and the source disagree

1. **Handover `:13`-`:14`** says develop is at `40270d263ab0`. Source: `b39051390ff6` (#1405, merged after R 4th's 14:56Z READY read). This is a move, not an error.
2. **Handover `:40`/`:45` and `:110`-`:112`** say KS-1436 is Backlog with 0 attachments, "may lag". Source: In Progress, attachment `pull/1404`, updated 14:56:53Z. The lag has resolved and the bot moved the state at PR open.
3. **Handover `:90`** gives the 189 paths as "`systemTest/` 170, both docs, `CLAUDE.md` 1", which sums to 173. Source: plus `observability/` 15 and `.claude/` 1 = 189.
4. **Handover `:92`-`:93`** says "develop's shell-suite denominator has moved past my 68". Source: develop is 68 too (51 + 17); R 4th's head is 68 (52 + 16). It is the same count over a different set, and #1404 merged would read 69.
5. **Handover `:95`-`:98`** treats the skill's §4 as unknown at the new develop. Source: §1-§6d are byte-identical; only §6e was added.
6. **Not in the handover or any ruling:** #1402's flow renumbering (KS-1305 `22.` -> `24.`) and the resulting `23.`/`24.` collisions.
7. **Not in the handover:** the shared store lacks the new develop's objects. R 4th's merge-tree ran in a scratch clone.
8. **R 2nd's handover `:74`** cites `mergeinra2_1395.sh` `:87` (LOCK_SEAT) and `:101` (refs/seatra2). Source: `:92` and `:116`, because the file grew after those notes.
9. **R 4th's brief** says the seat was "launched with `WED_USAGE_STOP=100`". **R 4th's READY says `WED_USAGE_STOP=<unset>`.** One of the two is wrong about R 4th's launch. Please check the R 5th launch line.
10. **R 4th's brief P20** cites the grant as "row 10" of EXPIRING-GRANTS. Source today: it is the 2nd data row (the file was re-ordered), so the brief cites it by its title instead.
11. **gate71 `RULINGS_wednesday.md` P5** (TAIL, key-anchored, immediately before develop's `  </body>`, with two leading spaces) predates #1402. Develop's flow `</body>` is now at column 0, and the block format is a matrix. The widening drafter should know that P5's shape no longer describes develop.
12. **KS-1313 payload:** fixtures were "captured from real vitest 4.1.9", but even `d75bfe2`'s lock pins 4.1.11. The capture version never matched either base exactly.

## 5. Open questions for Wednesday (all also in the brief's QUESTIONS)

- **Q-BASE5:** the base for PRs 3-5. Recommendation: develop at the ANSWER (`b3905139`).
- **Q-N5:** flow numbers. Recommendation (minimum change): keep `25.` KS-1313, `26.` KS-1164, `27.` row 06; re-assign the collisions, #1398 `23. -> 28.` and KS-998 `24. -> 29.`. Rule this in ONE ruling shared with the gate71 widening. The in-flux `recompose_gate71.py` selftest already maps 23 -> 28, which suggests the widening drafter is heading the same way. Alternative: positional (25-29 in merge order), as Peter did in #1402.
- **Q-XFER5:** one objects-only transfer of the new develop into the shared store. This is a named exception to Q-F and needs your ANSWER.
- **Q-TOOLS5:** bring R 2nd's merge tools into R 5th's active set, with every PR-keyed constant made a required argument.
- **Q-GATE5:** PRs 3-5 go to gate72 rather than a second widening of gate71.
- **What the GO mail must carry** (the brief's M-track refuses an incomplete GO), for the widening drafter:
  - D (40-hex) and the PR head
  - the target tree T
  - T's two doc blob ids and the absolute paths of the kit's composed doc files
  - the declared squash subject (no `(#n)`) with its landed length
  - the squash-body file path and its sha256
  - the verdict line with its Actions classification
- **The `WED_USAGE_STOP` value** R 5th is launched with (see disagreement 9).
