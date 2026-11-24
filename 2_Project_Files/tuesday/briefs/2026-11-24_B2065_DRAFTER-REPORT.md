STARTABLE: YES

# B2065 DRAFTER REPORT: OXPd 2 lane L3, the landing branch as ONE commit (build kit for seat X70)

Drafted 2026-11-24 22:39:10 to about 22:50 AEDT (first `date` 22:39:10; last `date` before this file 22:49:48) by a read-only Opus drafter for Tuesday s324. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2065_SEAT-X70_oxpd2-l3-one-commit-branch.md` (50455 bytes, ASCII only, 8 stamp slots, last line `READ-WHOLE-BY-TUESDAY: ____`). Sidecar: `...one-commit-branch.md.measured`; `stamp_check.py` rc 0, `160 claims, 160 measured`. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s324/d2065/` (below `<d>`). Seat tools: `<d>/seat-tools/`, 6 files.

## BLUF
- **The kit is small.** The seat runs `git commit-tree 03440d1d... -p 89a10a1b... -F commit-message-l3.txt` in its own seat-mode clone and asserts the tree id and `diff --quiet` against `51e91c26` (with a control). It then scans every object reachable from the new commit for the old id, scans it again with words.py, gitleaks and the workflow's own neutral scan, pushes by sha to the NEW `b2065/l3-onedrive-browse`, reads it back by `git/commits/<sha>`, and runs `hosted3.py --wait` at 2203 / 671 / 111 / 111. There is no source change, no `dotnet` and no heavy lock. Target READY is Step 0 + 45 minutes.
- **Proved in my scratch clone (prototype `f5906cf9b6a6bb4dffa87df6474cd6728e2c1e14`):**
  - The tree is `03440d1d15c679a0a9d071a7f12a01314210096e`.
  - `diff --quiet 51e91c26 <new>` returns rc 0. The control (`4b9814f1`) returns rc 1.
  - The commit has one parent, BASE. `rev-list --count` is 1, there are 671 files, and the diff against BASE has 13 rows (1 M, 12 A).
- **The old id is in no reachable object.** `literal_scan.py` reads every commit, tree and blob whole and case-insensitively:
  - New commit: `objects 1407 (commit 49, tree 487, blob 871)`, `holding the literal 0`, rc 0.
  - **Control `51e91c26`:** `holding the literal 1`, rc 1, `HIT blob f85ab776... tests/Datasec.Suite.OneDrive.Tests/BrowseTests.cs`.
  - `4b9814f1`: 1. `main` `84f088a2`: 0. BASE: 0.
  - `git grep` agrees: rc 1 at the new commit and rc 0 at `4b9814f1`.
- **The landing math is unchanged.** `merge-tree --write-tree 84f088a2 <new>` gives `0f34cebf88d2a520c14b6dad3ee3af660062474b`, the same squash tree gate B2064 tested. The gated head's hosted push run reads `HOSTED 51e91c26...: PASS` when I run it through `hosted3.py`. The new head has the same tree, so I predict the same numbers.

## FACTS RE-MEASURED (instrument, control)
| # | Fact | Instrument | Control |
|---|---|---|---|
| 1 | origin: `main` 84f088a2, `b2056/l3-onedrive-browse` 51e91c26 (tree 03440d1d, parent 4b9814f1), `heads/b2065` 0 rows, 0 open PRs, private/push `true true` | `gh api -X GET` 22:41:22, re-read 22:47:50 into `<d>/evidence/reads.txt` | `heads/b20` 10 rows |
| 2 | 51e91c26~2 = BASE 89a10a1b; ^{tree} = 03440d1d | `rev-parse` in the draft clone | n/a (two values) |
| 3 | the prototype's tree, parent, count, 671 files, 13 rows | `commit-tree`, `rev-parse`, `log`, `rev-list`, `ls-files`, `diff --name-status` | `diff --quiet` against 4b9814f1 rc 1 |
| 4 | the old id is absent from everything reachable from the new commit | `literal_scan.py` (new, this kit), `git grep -i -c -F` | 51e91c26 and 4b9814f1 each hold it once |
| 5 | the squash tree with main is 0f34cebf | `git merge-tree --write-tree` in MY scratch clone (never a project repo) | the same for 51e91c26 gives 0f34cebf |
| 6 | 51e91c26 hosted run PASS (run 45382346368; check runs 11:14:29Z to 11:18:00Z) | `hosted3.py` (no `--wait`), `<d>/logs/hosted-51e91c26.out` | the program's own `NOT-A-LINE-OF-ANY-LOG count 0` per job |
| 7 | message: `WORDS: clean (1 files)`, B-number count 0, 459 bytes, subject 401 characters; `commit-tree -F` stores it byte-equal | `words.py`, `grep -c -E`, in-process compare | `CONTROL FIRED: 13 of 13`; the commission counts 4 B-numbers |
| 8 | gitleaks `no leaks found` over the clone at the prototype and over the message and `literal_scan.py` under neutral names | gitleaks 8.30.1 | a planted program-built token: `leaks found: 1`, rc 1 (`<d>/logs/gitleaks-control.log`) |
| 9 | the workflow's neutral scan of every stored object on the prototype checked out: rc 0, `25 of 25`, `objects of this commit not among them 0`, `not among the stored objects 0` | `run_step.py` (form tool, unchanged) | its planted control (25 of 25) |
| 10 | `b[0-9]*/**` push trigger at `ci.yml:7`; `FLOOR=111` at `:211` (gated tree) | `grep -n` over `git show 51e91c26:.github/workflows/ci.yml` | `on:` at line 3 |
| 11 | X70 free: 1 `.md` file of 11-23/11-24 names it (the commission); no OXPd pane; `.tools/b2065` absent | word scan, `tmux list-panes`, `ls` | `X69`: 5 files; `.tools/b2062` present |

## D-DECISIONS (Tuesday's defaults as coordinator, in the kit)
D1 `commit-tree` with the tree id (no working-tree route). D2 no build or test (the tree id is equal). D3 the old id is scanned over every reachable object, the control runs FIRST, and a moved `main` is scanned too. D4 one folded subject.

## QUESTIONS FOR TUESDAY (defaults)
- **Q1 (STOP-CLASS, S4 answers in words): the commit message.** Default **a**: the folded subject in `commit-message-l3.txt` (round 1's subject plus "compared and sent without its fragment" and the drives/{id} limit; round 2's "folder-id row is an obviously synthetic id" is dropped because, in one commit, no earlier row exists). Alternatives: **b** round 1's subject verbatim, **c** round 2's subject verbatim.
- Q2: the commit form. Default: `commit-tree`. The alternative (checkout of files by path) is refused.
- Q3: the old branch. Default: left untouched. Removing it after the landing is yours. Until then the old id stays reachable on the origin by that ref. Whether GitHub then still serves `4b9814f1` by id is UNMEASURED.
- Q4: the scans. Default: all five (about 1 minute). Alternative: `literal_scan.py` and `words.py` only.
- Q5: level, windows, pane. Default: Opus (`CLAUDE.md:7`), READY at Step 0 + 45, push by Step 0 + 25, pane `Datasec/OXPd2-X70`.
- Q6: the check after. Default: your own check from the seat's STATUS and GitHub (`git/commits/<sha>` tree and parent), no gate. Alternative: a short G0 reader.
- **Why the gate's verdict carries, and where it would not:** the tree id is equal and the squash tree is the same. It stops carrying if (i) the seat's tree or parent differs (Step 2 STOPs), (ii) `main` moves before the landing (landing.txt's MAIN MOVES), or (iii) anything leans on the commit message (it is new text, clean). **Three things for you at the landing:**
  - `landing.txt` is pinned to `51e91c26` and the head branch `b2056/...`. Re-pin both to the new sha and branch.
  - `pr-body.md` names "the first commit's NO GO and the second commit's fix". That text needs a word changed, then a re-scan.
  - The old id stays reachable from `refs/heads/b2056/l3-onedrive-browse` until you remove it.

## CHAIN INPUTS
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit, Stamp S4 | Tuesday |
| 1 | `<src>` (6 files, exist); `<repo>` local values; origin refs | drafter scratch; `<repo>`; GitHub |
| 2 | the tree 03440d1d and BASE as objects; the message | Step 1's clone (`clone.py` fetches every origin branch); Step 1's tools copy |
| 3 | the commit checked out; `literal_scan.py`, `words.py`, `run_step.py`; gitleaks | Steps 2 and 1; `/opt/homebrew/bin/gitleaks` |
| 4 | the scanned commit; origin refs | Steps 2 and 3; GitHub |
| 5 | the pushed ref; `hosted3.py` | Steps 4 and 1 |

## UNMEASURED / NEVER RUN
- NEVER RUN: `clone.py` in seat mode for this lane, the commit with the seat's identity, the push and its object count, the GitHub read-back of the new sha (`git/commits`, `compare` 89a10a1b...new: DERIVED `ahead 1 behind 0 files 13`), and `hosted3.py --wait` on the new head.
- UNMEASURED: whether GitHub keeps an unreferenced commit after a branch removal, and whether the owner can remove a pull ref.
- Local CodeQL: not runnable (RELAYED, x86_64 extractor); no line of code changes.

## OUTSIDE THE FENCES (disclosure)
- **Scratch-only git identity.** In MY draft clone `<d>/clone` I set `git config --local user.name drafter-scratch` and `user.email drafter-scratch@invalid` so that `commit-tree` could run. The draft clone has no identity and its push URL is `invalid://no-push`. The commit `f5906cf9` exists only there.
- **Write verbs in that scratch clone only.** I ran `commit-tree`, `branch`, `switch` and `merge-tree --write-tree`, none of them in a project repo. A hook refused one `git -C "$C" switch` because the path was in a variable. I re-ran it with the literal `<d>/clone` path, which is under TUESDAY.
- **Reads outside the scratch.** I read the B2062 STATUS's last line only. I read `<project>/CLAUDE.md` lines 7, 55, 56, 82 and 83. GitHub calls were `gh api -X GET` only.
- **Sidecar skeleton moved.** `stamp_check.py --init` wrote a skeleton sidecar in `tuesday/briefs/`. I then edited the kit, so I moved that skeleton to `<d>/_quarantine/init-skeleton.measured` (moved, not deleted) and rewrote the sidecar.
- **Not done:** no push, no pull request, no write to any project, Jira, GitHub or card store, nothing to any human, nothing of another client.
