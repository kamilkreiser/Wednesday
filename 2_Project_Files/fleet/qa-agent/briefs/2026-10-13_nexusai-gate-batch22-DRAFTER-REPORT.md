# DRAFTER REPORT — NexusAI gate 22 (batch 22: RD-838, RD-839, RD-840 + RD-841)

Drafter: read-only drafting agent (Opus 5.5) for the Tuesday seat, 2026-10-13 ~11:15–~11:55 AEDT.
Outputs:
- Brief: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-13_nexusai-gate-batch22.md`
- Launcher: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch22.sh`
- This report.

## 1. WRONG — what the READYs or the commission get wrong, or leave open (full list: brief § WRONG OR UNVERIFIED, items 1-22)
Each item gives the instrument that measured it.
1. **No builder verify ran on any committed head.** RD-838's ran on a dirty `5bfdc93` tree (`rd838-proof.out:23`). RD-839's ran on a dirty `cc42c42` tree (`rd839-proof.out:86`). RD-840 + RD-841's ran on `b2a9f19`, which differs from `88bba37` only in the counts file (`rd840-proof.log:20`; `git diff --name-only`). The gate's own verify of each head decides.
2. **Merging RD-838 lands all of RD-640 (rounds 1 and 2).** Measured with `git diff --numstat 944ca97...380bec3`: `dataErasure.js` +149/−22, plus the rd640 cells and the erasure-verdict cell. Gate 19 gave NO GO on round 2, and the round-1 and round-2 parts have never had a GO. The brief therefore re-runs gate 19's whole never-follow matrix at `380bec3` (ruling T3).
3. **RD-640's kept-chain error text puts the absolute canonical end path into `filesFailed`.** Source: `380bec3:backend/dataErasure.js:77-79`. RD-839 withholds that path, but only once RD-839 is also on main. If RD-838 lands first, the N-640-1 leak class gains one more shape in the meantime (read-only inference). That is why the proposed merge order is **B, A, C**.
4. **RD-839's backstop regex has blind spots** (read-only inference from `withholdOutsidePaths`). It misses a path that follows `[`, `<`, `{`, `,` or a backtick. A path containing a space loses only the part before the space, so its tail leaks. Values nested inside objects or arrays are never rewritten. A path written as `<DATA_DIR>/../x` counts as inside DATA_DIR. Row b3 checks every shape the product actually writes before any planted shape (ruling T4).
5. **RD-839 treats "first run complete but zero authorised users" as still inside the window.** Its predicate is `!(firstRunComplete && hasUsers)`, the same as `adminGateRefuses`. C-212 says "open mode after setup unchanged" (ruling T5).
6. **RD-841's own e2e glyph cell needs the font from the CDN** (`e2e spec:319`), and the gate's network belt blocks the CDN. RD-721's head `64ee309` has the exact vendored bytes: sha256 `0695565c…` and `eba82430…` (measured with `git cat-file -p | shasum`, and equal to RD-721's provenance file) (ruling T6).
7. **"brand-token-conformance stays green" does not cover the light theme's colour literals.** Its assertion 3 scans only `dark-mode.css`. Every hex value added by C is a token value. The two off-token hex values in `sustainability.css` are inside comments and were already there before C (measured).
8. **The jest-lock tool changed since gate 21.** The installed tool is now `3c33f5ae…` (RD-821 r3), so gate 21's guard 90 would refuse today (measured with `shasum`).
9. **Gate 21's launcher can misread a binary merge as clean.** Its merge-tree reader runs `awk` under a UTF-8 locale, and on rd-721's woff blobs `awk` died without printing anything (measured in my own run). The new launcher runs `awk` under `LC_ALL=C` and refuses if the pipe exits non-zero.
10. **Two READY statements are stale:** RD-839's numstat is +68/−1, not +66/−1. Its "onto main 08a81e2: clean" is out of date: main is now `944ca97`, where the merge conflicts in the counts file only (C-89). RD-840 + RD-841's partition does not name the old head `rd-437` (`54d8b4e`). That head conflicts with C exactly as it conflicts with main (three-argument merge-tree).

## 2. Decisions for Tuesday
Each T-slot in the brief reads `RULED:` followed by a stamp placeholder. Write "default" or your ruling in each.
- **D1 (T1) Merge order:** default is B → A → C, with clone-2 in reverse. This keeps N-640-1 from widening on main.
- **D2 (T2) Locks:** default is `19477a9` everywhere, plus `e9063d4` only for the red-control arm on `b214f6f`'s own tree. If that arm hits ENOTCACHED, the control runs on the head tree with only the `343348d` blob swapped in.
- **D3 (T3) RD-838's verdict covers RD-640's whole change:** default yes. Gate 19's 88-arm matrix and walk table are re-run at the head.
- **D4 (T4) RD-839 blind shapes:** default is Major if the leaking shape is one the product writes; a shape that only the gate planted is named, Minor at most.
- **D5 (T5) "First run complete, zero users":** default is to measure it and name it with no weight; Tuesday rules.
- **D6 (T6) Glyph under the belt:** default (a) serves RD-721's vendored bytes through `route.fulfill`, with no network and the page's own SRI check as the landing control. Alternative (b) leaves the glyph render NOT RUN.
- **D7 (T7) Screenshots:** default is that the gate's set is evidence only and Kam's set stays O's. The gate sends nothing to Kam.
- **D8 (T8) rd-427 / rd-437 conflicts:** default is that they are not C's stop, because each conflicts with C exactly as it conflicts with main.
- **D9 (T9) Slots:** default is both EMPTY.
- **D10 (T10):** nothing else by default.
- **Stamp:** the SELF-CHECK line and the Self-check note (12 placeholders in total, counting the T-slots).

## 3. What I verified, and how
- **Pins:** `git ls-remote origin` at 11:17:31 AEDT, rc 0, plus `git ls-remote https://github.com/datasecau/Reporting_Dashboard_Au.git refs/heads/main` (`944ca97`). The launcher re-read the same pins at 11:46:12. No `refs/pull/*/head` matches any member head.
- **Chains, merge-bases, numstats and blobs:** `rev-list`, `merge-base`, `log --format='%h %p'`, `diff --numstat/--raw`, `rev-parse`. Counts and the `__tests__` census at 12 shas: `show` piped to `python3`, and `ls-tree -r -z`.
- **Merge-trees:** three-argument `merge-tree` with no objects written: main × each member, each member pair, B × rd-721/761/794/819, C × rd-427/437/828/801/802. Partition: 64 open heads out of 217 `rd-*` refs, using `diff --name-only main...head`.
- **Code read:** RD-838's `_walkLinkChain` and `_linkTargetOrNull`; RD-839's route, `adminGateRefuses`, `getStatus`; RD-840 + RD-841's CSS/JS diff, `dark-mode.css`, `index.html` CDN lines and SRI, `bi-info-circle` in `index.js`. WCAG contrast ratios computed in python3 (11.986, 7.757, 4.449).
- **Rulings and context read in full:** Tuesday's 2026-10-13 N/O ANSWER/BRIEF/GO files, the gate-21 RELEASE, C-212, C-213, C-185 (with addenda) at source, gate 19's `body-0.md` and `body-1.md` §2, gate 19's RD-640 instruments (sha256 pinned in the brief and the launcher), gate 21's instrument list.
- **Lock and panes:** jest-lock sha256 via `shasum`; queue read with `ls` (empty); panes via `tmux list-panes`.
- **Launcher:** `bash -n` rc 0. `--check` refuses only at 32 (stamp) and 40 (route). A stamped copy in my scratchpad, with a scratch routing file, passed every guard (rc 0, 11:45:55).

## 4. What I could not verify
- None of the gate's runtime rows: the purge matrix, servers, browser, jest. The drafter makes no scratch clone and runs no `--write-tree`.
- Whether the product can actually reach "first run complete, zero users" (T5), or a signed-in admin inside the window (WRONG 9).
- Whether any product path writes RD-839's blind shapes.
- The Linux leg and CodeQL: there are no PRs.
- Whether the e9063d4 offline install would hit ENOTCACHED.

## 5. `--check` output, verbatim (2026-10-13 11:46:12 AEDT, unstamped)
```
bash -n rc=0
NOTE: no tmux pane named 'Datasec/NexusAI-R' — that builder seat is not a negative control this launch
guards pass (9 6 7 8 18 18b 90 22 93 95 96 98 23 35 70 80 31 83 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 89 38R 86); stamp and/or route NOT complete.
  ls-remote attempts this run: 1 (C-192); three-argument merge-trees checked: 10; origin main 944ca97
  member pins (origin, re-read now): RD-838 380bec32258337ef08eb7e8560077670b8c29264 · RD-839 057a69d960d12ba090fea160ba8dfee4c70a0aa6 · RD-840+841 88bba375d836e2d2edca0046ad8db84818d8e818 · red control rd-640-eloop-and-tree-cells-s87n b214f6f06395 · lock tool sha256 3c33f5ae58e1… · SLOTS: S1 EMPTY; S2 EMPTY;
  C-212 heads: rd-721-icons-vendor-s91p 64ee309 counts-only/clean; rd-761-law-endpoint-policy-s89r 7f1881e counts-only/clean; rd-794-ollama-runtime-slice-s89r cd171f9 counts-only/clean; rd-819-ai-config-empty-body-s89r fdd07af counts-only/clean;
  NEG seats (38R, derived live; coordinator pane 'tuesday'): `33350` (Datasec/NexusAI-M); `12326` (Datasec/NexusAI-N); `72238` (Datasec/NexusAI-O); `84103` (Datasec/NexusAI-P); `3983` (tuesday);
REFUSING (32): 12 stamp placeholder(s) remain in the brief (the SELF-CHECK line, the Self-check note and the RULED: slots T1-T10) — the coordinator re-reads end-to-end and stamps them before launch
REFUSING (40): no 'QA/NexusAI-batch22|tuesday-agent@agentmail.to|no' line in /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/inbox_routing.conf — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)
check rc=40
```
(After that run I changed only the drafting-time strings in both files. A re-run then returned rc 40 again.)

## 6. `inbox_routing.conf` line Tuesday must add
```
QA/NexusAI-batch22|tuesday-agent@agentmail.to|no
```

## 7. Drafter's own slips
- The gate-21-style `awk` merge-tree reader died silently on rd-721. I re-ran it under `LC_ALL=C`, and that fix is now in the launcher.
- My first hex census counted hex values inside comments. I corrected it by reading each hit's line.
- My first `--check` refused at guard 93, because my own over-broad `${st.dev}:${st.ino}` count also matched RD-685's `_inodeKey`. I fixed the guard to look for the loop-key line exactly.
- Guard 31's "round 3" check was case-sensitive; it is now case-insensitive.
- Two explanatory lines in the brief contained a literal stamp token that would have blocked launch after stamping. I reworded them.
- Nothing was written outside the three output files and my scratchpad. In `!CODING/` I used only git read verbs and the three-argument merge-tree.
