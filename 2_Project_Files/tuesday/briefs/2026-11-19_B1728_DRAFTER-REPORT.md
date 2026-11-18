STARTABLE: YES - the candidate shape is measured with the hosted CodeQL version: its five tracked fingerprints equal main's and the PR-diff post-filter (which reproduces the hosted PR's 5 results at cd019f38) keeps 0 results; the kit freezes that shape; stamp_check exits 0.

# B1728 DRAFTER REPORT - NexusAI lane B1726 round 2 (CodeQL "new alerts" on PR #229)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_B1728_SEAT-N156_nexusai-b1726-round2-codeql-rekey.md` (177 lines, ASCII, 5 four-underscore lines: 4 slots + last line). Sidecar `.measured`: 104 claims, 104 measured. Drafting window: `date` 08:49:18 to 09:04:14 AEDT, Thu 19 Nov 2026. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s291/d1728/` (work/, raw/, trees/, db/, packs/).

## BLUF
- **The brief's hypothesis was wrong in its premise, right in its fix.** The round-1 edit did NOT change any fingerprint. Hosted main and the hosted PR analysis carry identical `primaryLocationLineHash` values for all five findings, and the alerts API on `refs/pull/229/head` already maps them to main's alert numbers 229, 230, 231, 232 and 235.
- **What blocks the PR is the diff-informed PR analysis.** It keeps a result when the START line of its primary location, or of any related location, is a line the PR adds. The round-1 field read at `server.js:3618` is an added line, and it is the related "source" location of all five results.
- **The fix is to restore main's field read byte for byte and put the refusal in an early `if` above it** (shape A). With that change no related location lands on an added line, and the post-filter keeps 0 results. One attempt was made and it passed.
- The kit commissions A7b (server.js, +4 -1) and T7b (rd1007 C1 cell, +6 -6), with no counts change (6041/382). A required local CodeQL step comes before the waiter, then a jest chain of 11 steps in one lock acquisition, and one fast-forward push.

## Facts re-measured (instrument -> result)
1. `gh api -X GET .../pulls/229` (08:49:52) -> open, head cd019f38, base 37fb1bcb, mergeable_state blocked, merge_commit_sha da986da1.
2. `check-runs/135126646152` -> CodeQL, failure, "5 new alerts including 4 high severity security vulnerabilities". The summary heading is "New alerts in code changed by this pull request". Annotations: server.js 3620 x3, 3631, and jsonStorage.js 524.
3. `rules/branches/main` -> code_scanning `{alerts_threshold: errors, security_alerts_threshold: high_or_higher, tool: CodeQL}`, plus deletion, non_fast_forward and required_status_checks (empty list).
4. `code-scanning/default-setup` -> configured, query_suite `extended`, threat_model remote, CodeQL 2.27.4 in both SARIFs. `.github/workflows` has no CodeQL file (arm-ttk, build, deploy-demo, deploy, gitleaks, npm-audit).
5. Analyses: main 37fb1bcb js `2198430304` (29 results); PR head cd019f38 js `2199861480` (5 results). No analysis exists on `refs/pull/229/merge`.
6. `code-scanning/alerts?ref=refs/pull/229/head` -> 235, 232, 231, 230, 229, all open and created 2026-09-28. These are main's own alerts, not new numbers.
7. **Hosted SARIF fingerprints** (python over both SARIFs):

   | finding | main | PR head |
   |---|---|---|
   | bypass x3 | 3609:14/24/33 `fb6be83c60b60503:1` | 3620:14/24/33 `fb6be83c60b60503:1` |
   | bypass | 3620:13 `1957a54887b4c6f6:1` | 3631:13 `1957a54887b4c6f6:1` |
   | http-to-file-access | jsonStorage.js 524:34 `421941c6a9bc55b1:1` | jsonStorage.js 524:34 `421941c6a9bc55b1:1` |

   Each finding's fingerprint is EQUAL on main and on the PR head.
8. Related locations (python):
   - In the PR SARIF, every one of the five has server.js 3618, which is the round-1 changed line.
   - jsonStorage's only related location in the PR SARIF is 3618; on main it has 14 server.js lines. This is the signature of diff-informed restriction.
9. **Local CodeQL**: CLI 2.27.4, `javascript-security-extended.qls`, `--threads=4`, run on GitHub tarballs of 37fb1bcb and cd019f38 and on candidate copies. Each database took about 12 s and each analysis about 32 s.
   - full_main, full_head, full_candA and full_candB each give 29 results. Against hosted main, each reads new 0, gone 0 on (rule, file, fingerprint).
   - **Candidate (candB = shape A + T7b): the five tracked fingerprints EQUAL main's.** The bypass rows are at 3623 (x3) and 3634; jsonStorage stays at 524.
   - Post-filter `difffilter.py`, start-line rule, using ranges from `mkdiffpack.py` (main -> tree, added lines):
     - head keeps 5, which equals hosted PR #229 row for row. This is the control that can fail.
     - The span rule keeps 7 at head (two extra `js/missing-token-validation`, open on main as alerts 67 and 68, high). Hosted did not report those two, so hosted uses the start-line rule.
     - **candB keeps 0** with the start-line rule, and 2 with the span rule (the same two as at head).
   - The in-query diff-informed run (a `restrictAlertsTo` data-extension pack) gives 13 raw results at head and 12 at candB. After the post-filter, head keeps 5 and candB keeps 0.
10. Candidate artefacts:
    - server.js blob `0335a98ea26fc2d70965521cd8738d7f0fb06fce`; rd1007 blob `499d9675814b40377603e669bc3e8ad1ba894c45`; `node --check` rc 0 on both.
    - numstat against cd019f38: server.js 4/1, test 6/6.
    - The main-to-candidate hunk in the route is `@@ -3606,0 +3616,5 @@`.
    - Count of `Email, name, and password are required`: main 1, cd019f38 1, candidate 2.
    - Count of `if (!isPlainRequestObject(req.body)) {`: main 0, cd019f38 0, candidate 1.
11. Pins on the changed text:
    - rd1007 C1 (lines 119-126 at cd019f38) counts the round-1 line, so it must change: T7b.
    - `grep -r -i -F isPlainRequestObject` over `__tests__`, `tests` and `scripts` -> rd691:159 (the definition, unchanged), rd969:148 (a comment), rd1007:122 and 124.
    - The 400 text appears only in rd1007:25.
    - The round-1 reader list (39) and scanner list (71) name rd1007 0 times (control: `rd523|rd1005` reads 1 in the reader list).
12. Slot: the program prints 13 for `b1728-nodot/{old10,rone7,new21,mut27,chk1}` (controls: `b1726-nodot/old5` 13, `b1719-nodot/old15` 14). Band 28320-28959 `lsof` 0 rows (control: unbounded 12). Briefs of 18 and 19 Nov naming slot 13 or 28320: only the B1726 files and the B1727 gate commission.
13. Other reads:
    - `gh api user` login contains datasec: count 1.
    - `ls-remote` at 08:58:41: main 37fb1bcb, branch cd019f38.
    - `CLARIFICATIONS.md:2067` is the merge-path line.
    - `models_latest.json:23` is claude-sonnet-5-5.
    - `model-routing.md:92` is C2 and `:109` is G2.

### Chain inputs (rule 4: each produced earlier or existing at base)

| step | inputs | produced by |
|---|---|---|
| CQ | archives of 37fb1bcb, cd019f38, T7b; the hosted SARIFs; the cq tools | clone (Step 1); T7b (COMMITS); gh GET (CQ 2); copied at Tools |
| 0-2 | `new21` at A7b; `list-readers.txt`; `readers-base-counts.json` | A7b (COMMITS); round-1 raw (exists) |
| 3, 4 | `old10`, `rone7`; T7b's rd1007 file | trees (Setup); T7b (COMMITS) |
| 5, 6 | `new21` at T7b; reader and scanner lists | T7b; round-1 raw |
| 7 | `mut27` at T7b; `plants-predicted.json` | T7b; pre-lock generation (R2) |
| 9 | `chk1` at T7b (or M) | T7b; M only via HOLD 20 inside the chain |
| push | step 9 tree, step 10 fetch, step CQ PASS | earlier steps |

## D-decisions (the drafter's)
- **D-1: Shape A, unchanged from the brief's suggestion.** The RD-1007 two comment lines stay, the early `if` reuses the route's own 400 text, and main's destructure is restored byte for byte. No fallback shape was needed.
- **D-2: T7b edits rd1007 C1.** It now counts `refusal` = the early `if` line, `fields` = main's destructure, and the definition. The title and the two header lines are reworded to describe the new shape. Cell id `C1` is kept, and so is the cell count.
- **D-3: No K commit.** The counts stay 6041/382; a counts refusal at the verify is a STOP.
- **D-4: The round-2 seat makes its own clone `.tools/b1728/clone`.** It treats the round-1 seat's `.tools/b1726` and `b1726-nodot` as read-only. It reuses slot 13 (the lane's own; the round-1 seat is finished) with five new tree names.
- **D-5: The CodeQL comparison is a required pre-lock step.** It uses the drafter's verbatim tools (sha256-checked), with `CQ_BASE` exported to the seat's folder. A miss stops the seat before any jest run.
- **D-6: Chain steps 1 and 4 prove the change is position-only.** At A7b, only the old C1 goes red. The new rd1007 file run at cd019f38 has only C1 red.
- **D-7: Plants.** P7b removes the refusal, P8 (`return true;`) is as in round 1, and P11 restores the ternary read so C1 fails alone.

## Q-questions for Tuesday (each with a default)
- **Q-1:** Gate is a G2 round-2 delta review by Opus 5.5, covering A7b and T7b plus the step-CQ fingerprint table and the post-filter result. **Default: yes, Opus.** The mechanism sits on a G1 surface, and `model-routing.md:109` puts Opus first for that case.
- **Q-2:** Build seat level is Sonnet on row C2 (a pilot, as in round 1). **Default: Sonnet** (the edit is frozen and measured).
- **Q-3:** The residual is that the hosted filter might use line spans after all. Then the two `js/missing-token-validation` alerts (main 67 and 68, high, related location = the whole user add handler span) would be listed. The cd019f38 hosted result argues against this, because it did not list them. **Default: if the hosted check on the new head still fails, there is no dismissal and no bypass. Tuesday opens a round 3 with the hosted annotations as input.**
- **Q-4:** T7b rewords the C1 title and two header lines rather than only the count keys. **Default: yes** (the old wording would describe a shape the code no longer has).
- **Q-5:** The PR #229 body says nothing about round 2. **Default: Tuesday adds one plain-words line at landing** ("the refusal of an unparsed body sits above the unchanged field read"). The seat never edits the PR.

## UNMEASURED
- The hosted CodeQL result on the new head (only Tuesday's re-run measures it).
- The jest behaviour of shape A: every rd1007 colour at A7b, T7b, main and cd019f38 is PREDICTED from source plus the round-1 and gate measurements. The chain measures them.
- How the hosted fingerprint window works. It was not needed, because the fingerprints are equal in all four trees, so no line-window experiment was run.
- Whether GitHub's check logic labels alerts "new" by location-in-diff or by anything beyond the diff-informed result set. The drafter measured only that the set of results the PR analysis emits equals the start-line post-filter, at cd019f38.
- Load and lock FIFO at launch (STAMP slots).

## Outside-the-fences disclosure
- **Network reads:** `gh api -X GET` to api.github.com under the NexusAI GH_CONFIG_DIR. This covered the PR, the check run and its annotations, the ruleset, default-setup, analyses, two SARIF downloads (Accept sarif), alerts, `user`, and two tarballs of 37fb1bcb and cd019f38.
- **Git:** `git ls-remote origin` and `git log` were run read-only (`--no-optional-locks`) through the round-1 seat's clone `.tools/b1726/clone`, which uses its configured ssh command. Nothing was written there.
- **CodeQL:** the CLI ran on drafter copies under `fleet/state/s291/d1728/` only, and wrote 5 databases and SARIF there.
- **Untrusted data:** the GitHub tarballs were extracted into `trees/`. No script was run from inside them. Only `node --check` and CodeQL were run on files there, and the copies under `trees/candA` and `trees/candB` were edited by drafter scripts kept in `work/`.
- **Files read:** NexusAI files read: `CLARIFICATIONS.md` line 2067 only, the round-1 STATUS, the round-1 `.tools/b1726` listings and raw lists. TUESDAY files read: the B1727 verdict and the round-1 kit and sidecar. No Jira, no mail, no PR or alert writes, no project file edits, no decision-queue command.
- **Deletions:** none. `mv` was used inside the scratch folder to rename the extracted tarball directories (`trees/main`, `trees/head`), and `rmdir` removed their two then-empty parent folders, all within the drafter's scratch.
