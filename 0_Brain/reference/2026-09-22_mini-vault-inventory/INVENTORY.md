# Mini vault copy: read-only inventory (2026-09-22)

**Commission:** card `mini-vault-stale-skills` = a (Kam, 2026-09-22 15:24 AEST). This is the "inventory BEFORE touching anything" step only. **Nothing in the vault was changed.** The only git verbs used were ls-remote, rev-parse, rev-list, merge-base, log (including `-g`), show, diff (including `--no-index --numstat` for line counts), ls-tree, cat-file, status and for-each-ref, plus `hash-object` without `-w` to fingerprint files on disk. No file content was opened except where noted.
**Repo:** `/Volumes/KK_T9_External_HDD/Notes (MASTER)`. Seat: Tuesday (Datasec). Isolation: Secuura and Side Projects are reported as counts only.

## BLUF

- **Two premises in the commission are wrong.** (1) "Behind 527" is measured against a **stale** tracking ref. The live origin head is not in this clone at all. (2) The skills files **on disk are already byte-identical to `origin/main`** (the stale ref). What lags is git's HEAD and index, not the files.
- **The working tree is not mostly local work.** Of 125 dirty paths, **108 are byte-identical to `origin/main`**, and 2 are deletions that upstream also made. The files have moved forward, most likely by file sync, while `.git` stayed at the old HEAD. So the "dirty" state is largely git's view lagging behind the files.
- **The 7 local commits all touch `daily/` only** (shared). None touches Secuura, Side Projects or Datasec.
- **Secuura: 4 dirty paths, all untracked, all byte-identical to origin.** Side Projects: 0. No lines in any local commit touch another client.
- **Genuinely local or non-attributable content is limited to `daily/`, plus one skills conflict copy:** 4 daily files that differ from origin, 1 new daily file, 9 conflict copies (8 daily + 1 skills), and 1 daily file present at origin but missing on disk. Details in sections 3 and 5.

## 1. Origin head vs local tracking ref

| | sha | note |
|---|---|---|
| `git ls-remote origin refs/heads/main` (live) | `99eedb9994d70938f0abfe1dfacc3775dcc36cfc` | **not present locally** (`cat-file -t` fails) |
| local `refs/remotes/origin/main` | `f44fceb2d45a314fbcd7e91bc3566eac40de0933` | commit date 2026-09-21 17:17:17 +1000 |
| local `HEAD` (`refs/heads/main`) | `f295de4f2816e31bbda393f675c1f4cca97e9d46` | 2026-09-21 12:34:46 +1000 |
| merge-base(HEAD, origin/main) | `9fdc6ceb30584a74af06a27b95d5bb58e7828489` | 2026-06-10 23:16:27 +1000 |

- **The tracking ref is stale.** "Behind 527" counts `HEAD..f44fceb` only. The real distance to `99eedb9` is at least 527 and cannot be measured without a fetch, which is out of scope.
- The reflog for `origin/main` shows it last moved at 2026-09-21 17:17:20 by "update by push", after a "fetch -q: fast-forward" at 17:17:16. Something pushed from this `.git` without HEAD advancing. See section 6.

## 2. The 7 local commits (`origin/main..HEAD`, oldest first)

All are authored by `Kam Kreiser <kreiser.org@me.com>`. Each touches exactly one file, under `daily/`. **Class: shared-only (all 7).** No other client is touched, so the subjects are quoted.

| # | sha | date | folder: status | subject |
|---|---|---|---|---|
| 1 | f3bb9cdcd242 | 2026-09-07 18:01 | daily: A `daily/2026-09-07.md` | vault: 2026-09-07 Datasec/NexusAI S43 — security register filed, 4 fix branches to gates, RD-361 NO GO'd on a Blocker, RD-367 raised (2026-09-07) |
| 2 | 378d36cd8978 | 2026-09-08 02:03 | daily: M `daily/2026-09-07.md` | daily 2026-09-07: NexusAI S46 — RD-374 and RD-323 lineages closed, seven tickets filed |
| 3 | 87595bd38ad6 | 2026-09-16 23:31 | daily: A `daily/2026-09-16.md` | daily 2026-09-16: Datasec/HPSM S48 — CLARIFICATIONS, no-fail audit, VM recovery, rebuild plan for Kam (local commit; push blocked: vault behind 484 …) |
| 4 | cd73b21f603e | 2026-09-19 11:50 | daily: A `daily/2026-09-19.md` | daily 2026-09-19: Datasec/NexusAI S67 — round 4 gated (NO GO, RD-564), round 5 with Kam, RD-566/567 held (… push blocked, vault behind 509 …) |
| 5 | 9d8c7dafd2fa | 2026-09-20 20:26 | daily: A `daily/2026-09-20.md` | vault: S72 NexusAI — r3 merged to main, RD-518 built, three lessons (2026-09-20) |
| 6 | faa1358819e6 | 2026-09-21 10:22 | daily: A `daily/2026-09-21.md` | vault: NexusAI seat B session notes — RD-516 fix round, C-107/C-108, the C-54 mis-citation chain (2026-09-21) |
| 7 | f295de4f2816 | 2026-09-21 12:34 | daily: M `daily/2026-09-21.md` | daily 2026-09-21: NexusAI S74 — RD-574 READY FOR QA (31 cells); RD-591 filed (test runs not isolated across seats) |

Net local-only lines (`diff --numstat origin/main...HEAD`): 09-07 +91, 09-16 +40, 09-19 +65, 09-20 +87, 09-21 +78. There are no deletions.
**Every one of the 5 files is also changed upstream (A at origin).** No commit blob equals the origin blob, so every file is a two-sided divergence. See section 5.

## 3. Dirty paths (`status --porcelain=v1 -z --untracked-files=all`, parsed in python)

125 paths in total.

| top folder | counts | fingerprint vs `origin/main` |
|---|---|---|
| **Secuura** | `??` 4 | all 4 byte-identical to origin (counts only, per isolation) |
| **Side Projects** | 0 | none |
| **Datasec** | `??` 6 | all 6 byte-identical to origin |
| **(root)** | `??` 6 | all 6 byte-identical to origin |
| **intelligence** | `??` 4 | all 4 byte-identical to origin |
| **skills** | ` M` 2, `??` 3 | 4 identical to origin; 1 conflict copy not at origin |
| **daily** | ` D` 2, ` M` 5, `??` 93 | 84 identical; 2 deletions matching upstream; 14 local or divergent (below) |
| Access, .obsidian, others | 0 | none |

**Datasec (all `??`, all == origin):** `Datasec/CypherKey/OneTimePad — TokenOne Overview.md`, `Datasec/NexusAI/AI Automated Testing.md`, `Datasec/Sales Portal Tool/PRO-MODE-Plan.md`, `Datasec/Sales Portal Tool/W2-Migration-Plan.md`, `Datasec/Sales Portal Tool/Workmate-Feedback-Review-2026-04-21.md`, `Datasec/myPKI Commercial Strategy.md`.

**Root (all `??`, all == origin):** `AI Coding.md`, `Changes.md`, `Extranet.md`, `Pasted image 20260428094609.png`, `Shell Deloploy.md`, `my recording.md`.

**intelligence (all `??`, all == origin):** `intelligence/decisions/2026-06-12-mypki-native-clients.md`, `intelligence/decisions/2026-08-07-protocol-v1.3-scoped-delegation.md`, `intelligence/meetings/2026-06-26-tech-discussion-stuart.md`, `intelligence/meetings/2026-07-31-technical-weekly-catchup.md`.

**skills:** ` M` `skills/Current/end-of-session.md` and ` M` `skills/Current/extranet.md` are both == origin. `??` `skills/Current/no-skip-on-failure.md` and `??` `skills/Current/no-time-deferrals.md` are both == origin. `??` `skills/Current/extranet (conflict_on_2026-09-17).md` is **not at origin**: +3/−2 lines vs origin's `extranet.md`, and +11/−0 vs HEAD's.

**daily:**
- 84 `??` files are == origin. These are `daily/2026-05-29.md` and every dated note from 2026-06-11 to 2026-09-17, except those listed below. The full list was produced but is omitted here for length; all are the same class.
- ` M` `daily/2026-09-07.md` and ` M` `daily/2026-09-16.md` are == origin. The local-commit version is kept in git only.
- ` M` `daily/2026-09-19.md`: three-way divergence. HEAD→disk +6. HEAD→origin +321/−8. origin→disk +14/−321.
- ` M` `daily/2026-09-20.md`: three-way divergence. HEAD→disk +52. HEAD→origin +236/−52. origin→disk +104/−236.
- ` M` `daily/2026-09-21.md`: the disk copy is origin plus 15 lines, with no deletions (HEAD→disk +25, HEAD→origin +10).
- `??` `daily/2026-09-15.md`: **differs from origin** (+12/−68 vs origin). **Origin's version is the conflict copy** `daily/2026-09-15 (conflict_on_2026-09-17).md`: blob `197922e6…` equals `origin/main:daily/2026-09-15.md` exactly.
- `??` `daily/2026-09-22.md`: new today, not at origin (stale ref).
- `??` 9 conflict copies, none present at origin under that name. Line counts are relative to origin's base file:
  - `2026-09-08 (conflict_on_2026-09-17)`: +0/−989
  - `2026-09-09 (…09-17)`: +39/−1269
  - `2026-09-10 (…09-17)`: +31/−994
  - `2026-09-12 (…09-17)`: +15/−422
  - `2026-09-14 (…09-17)`: +9/−510
  - `2026-09-15 (…09-17)`: identical to origin's 09-15
  - `2026-09-16 (…09-17)`: +13/−76
  - `2026-09-17 (conflict_on_2026-09-18)`: +3/−306
  - `2026-09-17 (conflict_on_2026-09-19)`: +10/−306

  These are mostly older or shorter snapshots, but each except 09-08 carries a few lines that the origin base file lacks.
- **Not dirty but missing:** `daily/2026-09-18.md` exists at origin and is absent on disk.

**The two ` D` conflict files:** `daily/2026-04-29 (conflict_on_2026-05-04).md` and `daily/2026-05-01 (conflict_on_2026-05-04).md`. They exist in HEAD and are **not at origin**: upstream deleted them in `021e0cb` (2026-07-02). The local deletion agrees with upstream, so they need no action beyond git catching up.

## 4. skills/Current

Compared against **local `origin/main` = `f44fceb`, the stale ref**. The live head `99eedb9` cannot be read locally.

| file | HEAD blob | origin/main blob | on-disk hash | status | verdict |
|---|---|---|---|---|---|
| end-of-session.md | b4201bc3 | 00ec86f0 | **00ec86f0** | ` M` | disk == origin (+120 lines vs HEAD) |
| no-skip-on-failure.md | (absent) | 4ac582b6 | **4ac582b6** | `??` | disk == origin |
| no-time-deferrals.md | (absent) | cdb7e3a1 | **cdb7e3a1** | `??` | disk == origin |
| extranet.md | 776943b9 | e52fa00d | **e52fa00d** | ` M` | disk == origin (+13/−3 vs HEAD) |

**The skills are current on disk as of `f44fceb`.** Any agent loading them from this path reads the upstream text. They show as dirty only because HEAD is at a June merge-base plus the 7 daily commits. The last upstream commit touching `skills/Current/` before the stale ref is `ea1a7f0` (2026-09-10). Whether `99eedb9` changed any skill after 17:17 on 2026-09-21 is **unmeasured**.

There is a stash, `refs/stash` 16b86a2 (2026-04-25), which also holds older edits to `skills/Current/end-of-session.md`, `always-verify-and-check.md`, `README.md`, `skills/Meta/prompt-master.md` and `skills/README.md`. It predates all of this and should not be applied.

## 5. What a safe update would need (recommendation only; nothing done)

Upstream-changed paths (merge-base→origin/main): 115. By folder: daily 91, root 6, Datasec 6, skills 4, intelligence 4, Secuura 4. Intersections:
- **dirty ∩ upstream:** 114 (daily 90, root 6, Datasec 6, skills 4, intelligence 4, Secuura 4).
- **local commits ∩ upstream:** 5, all daily (09-07, 09-16, 09-19, 09-20, 09-21).
- **all three (dirty ∩ upstream ∩ local commits):** the same 5 daily files.

Classes and risks:

| class | count | risk | recommended handling |
|---|---|---|---|
| A. Untracked or modified, byte-identical to origin | 108 (Datasec 6, root 6, intelligence 4, skills 4, daily 86 incl. 09-07/09-16, **Secuura 4**) | Low. They only block a checkout ("untracked would be overwritten"). Content is already upstream. | Once the tree is at origin they become clean with no content change. Moving them aside to a scratch backup first is safer than deleting; the commission forbids deletions. Secuura's 4 are in this class, so no Secuura content judgement is needed. |
| B. Local deletions that match upstream deletions | 2 (daily conflict copies from May) | Nil. | Resolved automatically when git reaches origin. |
| C. Local commits whose file on disk already equals origin (09-07, 09-16) | 2 files / 3 commits | Medium. Origin's version drops 29 and 12 lines of the local commit's version, so a straight "take origin" could lose session notes. Their content survives in the local commit objects either way. | Rebase or merge the 7 commits onto origin and resolve per file, or have the owning NexusAI/HPSM agents reconcile their own notes. Do not reset HEAD away without preserving the shas (e.g. on a backup branch in a scratch clone). |
| D. Three-way divergent daily files (09-19, 09-20, 09-21 ` M`) | 3 | **High.** Local commit, local uncommitted edit and upstream all differ. Needs a real content merge. | Owning seats reconcile. 09-21 is the easy one: disk = origin + 15 lines. |
| E. Local-only untracked content | 09-15 (disk differs, origin copy saved as its conflict file), 09-22 (new) | Medium. 09-22 may collide with the live head. | Keep both. Rename-merge 09-15 by hand. Compare 09-22 against `99eedb9` after a fetch. |
| F. Conflict copies not at origin | 9 (8 daily + `skills/Current/extranet (conflict_on_2026-09-17).md`) | Medium. Most are shorter snapshots, but 8 of the 9 hold 3–39 lines absent from origin's base file. The skills one sits inside `skills/Current/`, where the loader may pick it up as a skill. | Diff each against its base, fold any unique lines in, then archive. The extranet conflict copy most urgently needs moving out of `skills/Current/`. |
| G. Missing on disk: `daily/2026-09-18.md` | 1 | Low. Something removed or never synced it. | Arrives with the update. Check why it is absent. |
| H. Old stash `16b86a2` (2026-04-25) | 1 entry: tracked (root 1, .obsidian 1, daily 1, intelligence 4, skills 5); untracked part (root 2, Datasec 8, daily 4) | Low if left alone. Applying it would revert skills to April text. | Leave it. Do not pop it. |

**Other-client impact: Secuura has 4 paths, all class A (identical to origin). Side Projects has 0.** The local commits touch no other client. So the whole clean-up can be attributed without opening any other client's content.

**Prerequisite for any action:** a `fetch` to get `99eedb9`. The fetch is a write, so it is outside this inventory. Every class above should be re-checked against the live head afterwards, because origin moved after the local ref was last updated.

## 6. UNMEASURED

- The true behind count, and every comparison against the live head `99eedb9`: that object is not local, and fetching is forbidden here.
- Whether any skill changed upstream after `f44fceb`.
- How the working tree came to match origin while HEAD did not. This is consistent with a file-level sync (the T9 as a sync copy per workspace notes), but it is inferred, not proven.
- What pushed `origin/main` to `f44fceb` from this `.git` at 2026-09-21 17:17 while HEAD stayed at `f295de4`. The reflog says "update by push"; the source ref was not established. (`worktree list` and `branch` were refused by the seat's hook as write-class verbs, so linked worktrees were not enumerated; `for-each-ref` shows only `refs/heads/main`, `origin/HEAD`, `origin/main` and `refs/stash`.)
- The `HEAD@{2026-09-19 11:50:27} reset: moving to HEAD` entry, i.e. a `stash` or `reset --hard HEAD` just before commit 4. No new stash entry resulted, so what it discarded, if anything, is unknown.
- Whether the local-commit lines that origin "dropped" in 09-07 (29), 09-16 (12), 09-19 (8) and 09-20 (52) were really removed or just reworded upstream. Establishing that needs a content read by the owning agents.
- Content of Secuura paths: deliberately not examined. They are fingerprint-identical to origin only.
