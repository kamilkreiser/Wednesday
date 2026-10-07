---
date: 2026-10-07
type: reference
source: Wednesday's brief-drafter subagent (session 0e6aaa67), 2026-10-06 22:11Z-22:2xZ UTC
status: draft-report
---

# Seat R 6th brief: drafter's report

**Brief:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-07_seatR6_merge1404_1398_raise3to5.md` (151 lines, ~48 KB; NOT sent, NOT launched).

## Headline
- develop is **`fa24bddedf3b9af0cc198ea72848902971f16639`**. I read it at 22:12:16Z and again at 22:17:34Z (`ls-remote`, rc 0), unmoved since your 22:10:32Z read. It is #1406's squash: one parent `b39051390ff6`, tree `85820a21f80c`, and five `package-lock.json` paths only. None of the five is a path of #1404, #1398 or PRs 3-5. The doc blobs are unchanged.
- **I re-predicted #1404's target with the gate71 kit itself: T' = `a4a219b872710c6cc1cbf1eee193b9e192cf090d`** (PASS, guard 12/0). My own hand build matches it. `merge-tree M x fa24bdd` (rc 0) produces the same tree. T..T' is exactly the five locks, so the GO's doc blobs and the kit's composed files still apply verbatim.
- **Rebuilding M: you need to rule on this (Q-REBUILD6).** A merge of fa24bdd INTO the retained M is clean, but its parents are `[M, fa24bdd]`. The kit's `qm` Q1 requires `[head, D]` (`c4_docs_gate71.py:290`), so that merge fails Q1 by construction. My recommendation is a FRESH merge-in M' of fa24bdd into `c117`, made on a detached HEAD. `pushra1_ff.sh:112` pushes `HEAD:refs/heads/<branch>` pinned at origin's `c117`, which is a fast-forward. The local branch ref keeps pointing at M, so nothing is deleted or rewound.
- #1398's SIM target on the new chain is `ce7f6c7bbda2` (it was `960e71800ea1`). It is still a SIM; per W-Q8 the GO must name the real post-#1404 develop.

## Changes vs R 5th's brief
1. Seat, token and lock: R 6th / `ra6` / `LOCK_SEAT='Secuura/Blockchain-R ra6'`. The re-key halves swap: add r 5th, remove r 6th, forward-add r 7th, d 15th and g 4th. The F-2 warning about MY_FORMS vs FOREIGN_FORMS is carried.
2. B (merge) now runs FIRST and A (raise) comes after. The raise base is re-proposed as develop at the START of A (Q-BASE6), not develop at the ITEM-0 ANSWER, because B moves develop twice.
3. The merge-in tool's required-arg values are re-measured: `--expect-ours-paths` 195 (was 190), `--expect-dev-paths` 4, `--dev-parent-count` **1** (was 2: develop is now a squash, not Peter's merge). Stale-value arms must refuse.
4. GO strings are `GO (Seat R 6th): merge 1404|1398 on gate71`. The declared subjects carry NO `(#n)`, and their landed length is stated as equal to the declared length (66 and 83).
5. New open questions: Q-REBUILD6, Q-COVER6 (a proposed five-condition "no new gate" rule), Q-XFER6, Q-BASE6, Q-GATE6 and Q-LAUNCH6.
6. The live-seat partition is now D 14th (live, demo) and G 3rd (wrapped). D 13th is gone.
7. The launch no longer cites `WED_USAGE_STOP=100`, because that grant row is EXPIRED.
8. For legs 6/7: re-install in `s-ra4-ks1436` before the dry read. The locks changed under R 5th's install.
9. Kit tools are to be run with `python3 -B` (see the incident below).

## Every fact re-verified (command)
- R 5th's handover sha256 = `1492bb1a44ed13d4d11b…`, matching the expected prefix. 224 lines, 18,847 B. Checked with `shasum -a 256`. R 4th's handover is `6f2af1b5e8fe91c0` and R 3rd's is `35ad164280e587d5`, both unchanged.
- develop and PR heads: `env -u GIT_SSH_COMMAND git -C "<checkout>" -c core.sshCommand=<own> ls-remote git@github.com:Secuura/Distributed_Secuura.git` at 22:12:11-16Z, then `git -C "<checkout>" ls-remote origin refs/heads/develop refs/pull/{1383,1398,1404}/head` at 22:17:29-34Z.
- What moved and the PR path sets: in the scratch clone (`clone --shared --no-checkout`, by-SHA fetch from the GitHub URL), I ran `git log -1 --format=%H%n%T%n%P%n%s`, `git diff --name-status b3905 fa24bdd` and `git diff --name-only b3905...<head>`. The shared `rev-parse --all` and `.git/config` read identical before and after (`cmp` rc 0).
- T': `python3 -I c4_docs_gate71.py predict|targets --repo <scratch clone> --pr 1404 --head c117… --develop-after fa24bdd…`. I also hand-built it in `scratchpad/predict.sh`, with old-T and negative controls. Cross-checked with `git merge-tree --write-tree`.
- Merge-in tool counts: `git diff --name-only|--name-status c117 a4a219b8`, `fa24bdd a4a219b8`, with the old-T control (190/188/4 matches the handover).
- PRs 3-5 payloads: STRICT apply into a temp index at both bases, plus the tamper control (`scratchpad/payloads.sh`). vitest in the fa24bdd lock is 5.0.3.
- Shared store, read verbs only: `cat-file -t`, `rev-parse --all | wc | shasum`, `rev-parse refs/heads/…`, the worktree's `rev-parse HEAD` / `status --porcelain`, `ls -A worktrees`, and `TZ=UTC stat FETCH_HEAD`.
- PR state: GET `/pulls/{1404,1398,1383,1406}` and `pulls?state=open`. Linear: GraphQL `issue(id)` for KS-998, 1313, 1326, 1164, 1436, 1136 and 1437. Tokens were read by name and never printed.
- GO inputs: `git hash-object` of the kit's composed docs, plus `shasum` of `1404_squash_body.txt` and the gate71 report.
- Tool facts: `shasum` of R 5th's `raise/` files, plus `sed -n` of `pushra1_ff.sh:78-140`, `mergera1.py` MG-11 at `:393-:409` and `c4_docs_gate71.py:1-45,280-300,425-459`.
- gate71 ruling line numbers: grep over `RULINGS_wednesday.md` (`:88`-`:100`, `:140`-`:146`).

## Contradictions in the sources
1. **The R 5th GO and the gate71 verdict use the dead suffix arithmetic.** #1404 is given as "66 chars, lands 74 with (#1404)" and #1398 as "83, lands 91" (gate71 Q5 even ruled on 91). But `mergera1.py` appends nothing (`:393`), so they land at 66 and 83. MG-11 still passes because there is no `(#` in the subject. This is the same root cause as the 10-05 #1376 and 10-07 #1406 GOs.
2. **STANDING_LINES `:318` is stale.** It still says GitHub's squash appends ` (#n)` and that MG-11 is measured as `len + len(" (#n)") <= 92`. The tools' hand-fix 3 removed the append. That line now teaches the wrong arithmetic and is the likely source of the repeat.
3. **Gate number collision.** R 5th's brief (Q-GATE5) reserved **gate72** for PRs 3-5, and NEXT-PICKUP's 07:2x state also said "next number gate72" for the advisory PR. gate72 was spent on #1406, so PRs 3-5 need a new number.
4. **Usage launch.** R 5th's brief ruled the `WED_USAGE_STOP=100` launch under the SPEND-TO-100% row. EXPIRING-GRANTS now marks that row EXPIRED (Kam's /login ~08:4x).
5. **"M stays valid while develop == b3905" vs reality.** NEXT-PICKUP's "STATE AT THE WRAP" section still describes M as RETAINED and the GO as valid. The newer LIVE STATE section in the same file says VOID. That is an internal inconsistency in the pickup file.
6. **`rev-parse --all` is 1,610 lines, not R 5th's 1,608.** I did not attribute the +2; the likely sources are G 3rd's branch/worktree and D 14th. This is not a contradiction, but nobody has measured it.

## Open questions for Wednesday
1. **Q-REBUILD6**: (a) a fresh M' from `c117` on a detached HEAD (recommended), or (b) merge into M with qm Q1 waived by name?
2. **Q-COVER6**: does my five-condition rule stand, so that gate71 still covers #1404 and #1398 with no re-gate?
3. **Q-XFER6**: may the seat do objects-only transfers of fa24bdd and of each later GO's D?
4. **Q-BASE6**: should the raise base be develop at the start of A (expected post-#1398) or develop at the ITEM-0 ANSWER?
5. **Q-GATE6**: what gate number do PRs 3-5 get (gate73)?
6. **#1398's squash body**: it is not in the kit (`recomposed_2026-10-07/` has no `1398_squash_body`). Who writes it under Q4, the merge seat or Wednesday with the GO?
7. Should STANDING_LINES `:318` be corrected now, before the next GO is written? Not in my write scope.

## Incident (mine, disclosed)
My first `c4_docs_gate71.py predict` run (python without `-B`) created `__pycache__/` (two `.pyc` files) **inside the gate71 kit folder**, which is outside my write scope. I confirmed it was new: the dir mtime was the run time and it was absent from the earlier listing. I moved it to my scratchpad (`scratchpad/quarantine_kit_pycache/`), and the kit folder is back to 0 `pycache` entries. Every later kit run used `-B`, and the brief tells the seat to do the same. Nothing else was written outside the two named files and my scratchpad. `!CODING/` was touched by read verbs only. No mail, no tmux and no launch.
