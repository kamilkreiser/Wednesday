# NexusAI off-main gated heads: census and gate-26 proposal (Tuesday's drafter, 2026-10-18 12:13-12:22 AEDT, read-only)

## BLUF
- **Main has not moved.** It is still `c7ca0ed7113750b268028f12e8659bf1e3d34282`, read by `git ls-remote origin refs/heads/main` at 12:14 and again at 12:21 (MEASURED).
- **I checked 21 released, gated heads.** These are the nine 5a/5b merges released on 09-29 and the twelve turn-order items 12-17 and 20-25.
  - **One is DONE: RD-681.** Its released head `4209299` and its later CodeQL-fix head `faea66b` are both ancestors of main (rc 0), its test file is on main, and Jira says Release Ready.
  - **The other 20 are all off main** (`merge-base --is-ancestor` rc 1 for each).
  - **None of the 20 is already on main under another sha.** `git cherry` finds 0 patch-equivalent commits in each range, every new `__tests__` file is absent from main, and almost none of each head's added code lines appear verbatim on main. Most heads have 0 or 1 such line; C-170 has 7 of 314 and RD-761 has 3 of 230. RD-131's 9 of 25 are generic boilerplate that main already uses.
  - So I found **no superseded or abandon candidate**.
- **Every one of the 20 conflicts with main in exactly one file, `scripts/verify-expected-counts.json`.** That is `merge-tree --write-tree` rc 1 in my own scratch mirror, with zero code conflicts. I also merged them two at a time on main (380 ordered pairs) and got **zero non-counts conflicts**. A planted conflict in `backend/server.js` was detected, so the instrument can see one.
- **What decides re-gate versus TURN is which files changed on both sides since each head's merge base.** All 20 auto-merge cleanly; the split is about what main changed underneath them.
  - **9 heads have main changes under them** (one or more shared files besides the counts file): RD-627b, RD-682, RD-705, RD-695, RD-413, RD-761, RD-721, RD-794 and RD-819 share `backend/server.js`; RD-761 also shares `backend/azureLogAnalytics.js`; RD-413 also shares `static/js/first-run-setup.js`; RD-721 also shares `static/settings.html` and an rd385 test; RD-131 shares `static/js/index.js`.
  - **The other 10 have only the counts file in common with main.**
  - In every shared file, head->merged has the same `git patch-id --stable` as base->main. That is necessary but not sufficient (Tuesday's ANSWER-5, quoted in gate 25's kit).
- **Proposed gate 26 (TIER 1, re-gate as merged)** is one sequenced chain on the main that gate 25's landings produce: RD-819 (stacked on RD-794) -> RD-627b -> RD-682 -> RD-705 -> RD-695 -> RD-413 -> RD-831 -> RD-721. Beside the chain, and file-disjoint from it, go C-170 `be0fe37` (after S101O's re-check READY) and RD-594.
- **Proposed counts-only TURNs, no gate** (all of these are Tuesday's per-head decision):
  - **Tier 2:** RD-751, RD-817, RD-696, RD-807 (the fix head), and RD-131. RD-131 sits one step past the precedent, because `index.js` auto-merges.
  - **Tier 1:** RD-747, RD-777+776 and RD-775. It is your ruling whether the RD-801/802 precedent extends to tier 1.
- **RD-476 (S101O, local commit `3939290`, 12:18)** touches `model-config.js` and `__tests__/helpers/rd395-llm-mock-preload.js`. Both are gated RD-794 files.
  - It merges with no conflict onto main+RD-794 (MEASURED in scratch).
  - Even so, its tier-2 QA should run on the tree after RD-794 lands.

## How I measured (instruments, predicates, controls)
- **Scratch store.** `git clone --no-local --mirror` of the NexusAI repo into my scratchpad (`store.git`), with `gc.auto 0` and origin removed. All merge-tree, commit-tree, hash-object and write-tree work ran there.
  - In the NexusAI repo I used read verbs only: `ls-remote`, `for-each-ref`, `cat-file`, `config --get`, `count-objects`, and `worktree list`.
  - In S101O's live worktree I also ran `--no-optional-locks` `diff`, `log` and `ls-files`.
- **RD-807's gated head `ff5d725` is in NO local ref or object.** The local repo has only the gate-19 head `9b15a99` under `refs/remotes/t9-drive-2026-10-15/…`.
  - I fetched that one branch from GitHub into my scratch store only (`refs/scratch/rd-807`), using the project's deploy key read-only.
  - RD-476 `3939290` was fetched from the local NexusAI repo into scratch. That is an upload-pack read of NexusAI, and NexusAI itself was not written to.
- **Gate 25's T6 (side note).** On a `--mirror` clone, `git remote remove origin` deletes **every** `refs/remotes/*` ref, which is all of t9-drive-2026-10-15 and origin. My store went from 482 to 90 refs (MEASURED).
  - `7f1881e` and `cd171f9` are named only by remote refs, so in such a store they become unreferenced objects. They are still present (`cat-file -t` = commit, MEASURED), but only until a gc.
  - Gate 25's method creates its `g25/*` refs by sha, so it is safe as long as `gc.auto 0` holds.
- **Ancestry.** Predicate: `merge-base --is-ancestor <head> c7ca0ed` rc 0 means on main.
  - Positive controls, all rc 0: `4209299` and `faea66b` (RD-681), `6613113` (RD-801), `a103c8e` (RD-802), `2fab772` (RD-828), `c14be9d` (RD-795) and `2a3530f` (RD-823).
  - Negative control: `be0fe37` rc 1.
- **Content on main under another sha.** Three measures:
  - `git cherry c7ca0ed <head>`: count of "-" lines (patch-equivalent commits on main).
  - The presence on main of every `__tests__` file the range adds. A positive control is RD-681's test file, ON-MAIN; a negative control is a made-up path, rc 128.
  - Added non-test code lines longer than 25 characters, compared verbatim against main's copy of the same file. Positive control: RD-681's 7 server.js lines give 7/7. RD-131's 9/25 are generic table-loop boilerplate that main's toner CSV already uses (read).
- **Merge prediction.** Predicate: `merge-tree --write-tree --name-only c7ca0ed <head>`, recording rc and the conflicted paths.
  - Control: main's own merge parents `2965ed7` + `55047f4` give rc 1 with the counts file only. That is the same shape, because c7ca0ed regenerated its counts.
  - **The pairwise matrix.** For each head A, I built a scratch commit of main+A with main's counts blob, then ran `merge-tree` with each other head B. Predicate: conflicted paths other than the counts file.
  - Pairwise positive control: two planted commits that edit `backend/server.js` line 1 differently give rc 1, `backend/server.js`.
- **Patch-id.** For each shared file I compared `git diff <head> <merged> -- f | git patch-id --stable` against `git diff <mb> c7ca0ed -- f | git patch-id --stable`.
  - Cross-check against gate 25's WRONG 3, measured independently: RD-761 `4c79e73f` / `fe11d3bc` and RD-794 `c7688917` match.
  - Negative control: RD-627b's head->merged id (`e3c40841`) differs from RD-413's base->main id (`ec65bedc`).
- **Jira.** `GET /rest/api/3/issue/<key>?fields=status,…` with NexusAI's `JIRA_SITE`/`JIRA_EMAIL`/`JIRA_API_TOKEN` (names read, values never printed). HTTP 200 on all 28 keys.
  - Positive controls: RD-681, RD-801 and RD-802 are Release Ready, which matches the landed heads.

## Per-head table
All MEASURED unless marked RELAYED.
- "Remote" is `git ls-remote origin` at 12:14. "Local" is `for-each-ref` in NexusAI.
- **mb** is the merge base, **behind** is the number of commits main has that the head lacks, and **ahead** is the number the head has that main lacks.
- **Both-sides** lists the files changed on both sides since mb, apart from the counts file. "≡" means the shared file's patch-ids are equal.
- **Merge** is the merge-tree result onto c7ca0ed. It is rc 1 with the counts file only for every off-main row.
- **Gate 25 overlap** is against `backend/server.js`, `backend/azureLogAnalytics.js`, the counts file and `backend/llm/*`. Every head overlaps on the counts file, so that is not repeated.

| Head | Branch @ sha (remote = gated?) | Local ref carrying the sha | mb / behind / ahead | Both-sides (≡) | Gated files byte-equal in merged tree | Gate 25 overlap | RD-476 overlap | Jira |
|---|---|---|---|---|---|---|---|---|
| RD-681 (5a #1) | `rd-681-clear-undecryptable-s84m` now `faea66b` (gated `4209299`; both on main) | t9 ref only for `4209299` | **ON MAIN** | — | — | — | — | Release Ready |
| RD-627b | `rd-627b-sigterm-flush-s84m` `c82aa92` = gated | t9 only | 1904765 / 304 / 1 | server.js ≡ | 1/2 | server.js | none | RD-627 Testing |
| RD-682 | `rd-682-clear-partial-audited-s84m` `f15fed6` = gated | t9 only | 4209299 / 303 / 1 | server.js ≡ | 2/3 | server.js | none | Testing |
| RD-705 | `rd-705-no-store-authenticated-pages-s86m` `e164d1a` = gated | t9 only | 1904765 / 304 / 1 | server.js ≡ (nearest main hunk 87 base lines away) | 1/2 | server.js | none | Testing |
| RD-695 | `rd-695-stats-trend-undated-s84m` `ad97d12` = gated | t9 only | 748cece / 307 / 1 | server.js ≡ | 1/2 | server.js | none | Testing |
| RD-413 | `rd-413-truthful-mail-secret-storage-s84m` `f70594a` = gated | t9 only | 11666d3 / 328 / 1 | server.js ≡ (70 lines away), first-run-setup.js ≡ | 4/6 | server.js | none | Testing (RD-636 To Do, closes with it) |
| C-170 / RD-460 | `rd-460-pkg-into-main-s84m` `be0fe37` = gated | t9 only | 1904765 / 304 / 1 | none. **But main changed `Dockerfile`, `.dockerignore`, `package.json` and the lock since mb**, and C-170's tests read `backend/server.js` | 33/33 | none | none | RD-460 Testing; RD-505/506 To Do |
| RD-696 | `rd-696-listen-remedy-cells-s84m` `2c221fa` = gated | t9 only | 1904765 / 304 / 1 | none | 1/1 | none | none | Testing |
| RD-594 | `rd-594-kv-identity-open-window-s86m` `c7fbf33` = gated | t9 only | 1904765 / 304 / 1 | none. **But the code its cells guard moved on main:** RD-603 `eb90f92` moved `healthDetailsForCaller` to `services/healthProjection.js`, and `7983c9d` changed a non-admin's keyVaultEncryption to null | 1/1 | none | none | Testing |
| RD-751 (item 12) | `rd-751-rd693-cells-s91p` `7a6d6bd` = gated | t9 only | d5b6d31 / 106 / 2 | none (target `static/js/entra-provisioning-ui.js` unchanged on main since mb) | 1/1 | none | none | Testing |
| RD-817 (13) | `rd-817-trim-and-firstat-cells-s86m` `e504339` = gated | t9 only | 7d11359 / 99 / 2 | none (target `services/cspReport.js` unchanged since mb) | 1/1 | none | none | Testing |
| RD-747 (14) | `rd-747-clear-generation-s87n` `968ee14` = S3 JOINS head | t9 only | 8b7ae54 / 130 / 2 | none (`jsonStorage.js` unchanged since mb; 2 added main lines name `jsonStorage` as a caller, `hasAnyAuthorizedUsers`, not `backupFile`) | 2/2 | none | none | Testing |
| RD-831 (15) | `rd-831-legal-loader-s91p` `e9eeceb` = gated | t9 only | 8b7ae54 / 130 / 3 | none (main's 18 CSP-mentioning lines since mb are the report-intake budget, not the policy header; read) | 3/3 | none | none | Testing |
| RD-777+776 (16) | `rd-777-776-validators-s92r` `94b288c` = gated = `refs/pull/67/head` | t9 only | 4526575 / 114 / 4 | none (0 main lines name `validateInput` or `validators`) | 2/2 | none | none | RD-777 Testing, RD-776 Testing |
| RD-761 (17) | `rd-761-law-endpoint-policy-s89r` `7f1881e` = gated = `refs/pull/58/head` | `refs/remotes/origin/…` (t9 holds the older `141d7ea`) | 8853e36 / 138 / 17 | server.js ≡, azureLogAnalytics.js ≡ | 7/9 | **gate 25 member A** | none | Testing (updated 10:29) |
| RD-721 (20) | `rd-721-icons-vendor-s91p` `64ee309` = gated | t9 only | 8853e36 / 138 / 6 | server.js ≡, settings.html ≡, rd385 test ≡ | 18/21 | server.js | none | Testing |
| RD-794 (21) | `rd-794-ollama-runtime-slice-s89r` `cd171f9` = gated (no PR ref) | t9 only | 3e6d02d / 174 / 7 | server.js ≡ | 13/14 | **gate 25 member B** | **`model-config.js`, rd395 mock preload** | Testing (updated 11:35) |
| RD-819 (22) | `rd-819-ai-config-empty-body-s89r` `fdd07af` = gated; **`cd171f9` is its ancestor (stacked, rc 0)** | t9 only | 3e6d02d / 174 / 16 | server.js ≡ | 13/14 | server.js + all of RD-794's files (stack) | **same as RD-794 (inherited)** | Testing |
| RD-807 (23) | `rd-807-incidents-prototype-key-s89r` `ff5d725` = gate-21 fix head | **NONE locally** (t9 has `9b15a99`); fetched to scratch | 4332fb0 / 147 / 6 | none (0 main lines name incident callers) | 4/4 | none | none | Testing |
| RD-131 (24) | `rd-131-fleet-health-drum-csv-s87n` `e7d2cd1` = gated | t9 only | 7d11359 / 99 / 2 | `static/js/index.js` ≡ (main RD-614 `f515f6e`; nearest hunk 4,741 lines away) | 1/2 | none | none | Testing |
| RD-775 (25) | `rd-775-readiness-key-s92r` `537741c` = gated = `refs/pull/70/head` | t9 only | 41c5a47 / 96 / 3 | none (0 main lines name `readiness`) | 2/2 | none | none | Testing |

- **Every one of the 20 off-main remote heads equals its gated sha.** The only remote branch that moved is RD-681's, and it is on main.
- **File collisions between heads** (pairwise shared files, counts file excluded, MEASURED). None of them conflicts:
  - `backend/server.js` is shared among RD-627b, 682, 705, 695, 413, 761, 721, 794 and 819.
  - RD-413 and RD-721 also share `static/first-run-setup.html`.
  - RD-721 and RD-831 share `static/legal.html`.
  - RD-794 and RD-819 share the whole stack (13 files).
  - All other pairs are file-disjoint.
- **Content check (cherry "-" commits / added test files on main / added code lines on main).** For all 20 heads: 0 "-" commits and 0 test files on main. The largest verbatim-line ratios are C-170 7/314 and RD-761 3/230; the RD-131 9/25 lines are boilerplate, as explained above.

## The gate that covered each head (quoted, with path:line; all RELAYED from Tuesday's records)
- **5a (all TIER 1):** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-28_nexusai_M_batch5a_verdict.md:1`: *"BATCH 5a PASSED — all six lane-1 changes are GO WITH FINDINGS (verdict 15:48Z …)"*.
  - `:5` gives the heads: *"RD-681 4209299 · RD-682 f15fed6 · RD-627b c82aa92 · RD-695 ad97d12 · RD-705 e164d1a · RD-413 f70594a"*.
  - `:4` gives the order rule: *"RD-627b goes BEFORE RD-682 …"*.
  - The tier comes from `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-gate-batch5a-rd681-rd682-rd627b-rd695-rd705-rd413.md:1` *"(all TIER 1)"*.
- **5b:** `/Volumes/Laptop-DEV/TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:1239`: *"All 3 GO WITH FINDINGS (C-170/RD-460 be0fe37 t1, RD-696 2c221fa, RD-594 c7fbf33 t1); order C-170 → RD-696 → RD-594"*.
  - Tiers come from `…/qa-agent/briefs/2026-09-27_nexusai-gate-batch5b-c170pkg-rd696-rd594.md`: `:1` *"RD-696 (TIER 2, tests only)"* and `:29` *"RD-594's tier (WRONG 14): TIER 1"*.
- **The 09-29 RELEASE of all nine:** `NEXT-PICKUP-TUESDAY.md:1213`: *"Nine merges: RD-681 → 627b → 682 → 705 → 695 (fwd) → 413 (fwd; RD-428 id accounted) → C-170 → RD-696 → RD-594."*
  - The successor drafter cited this as `:1159`. The file has grown since, so the line moved.
  - The release mail itself is `fleet/briefs_staged/2026-09-29_nexusai_M_release_5a_5b.md:3-5`.
- **Gate 20 (RD-761 T1, RD-831 T1+browser, RD-777/776 T1, RD-747 T1, RD-751 and RD-817 T2):**
  - `NEXT-PICKUP-TUESDAY.md:642`: *"GATE 20 DELIVERED, ALL TEN GO; RELEASED … 12 P RD-751 · 13 M RD-817 · 14 N RD-747 · 15 P RD-831 · 16 R RD-777/776 (#83/#84/#43 must read fixed on main post-merge) · 17 R RD-761"*.
  - Tiers: `…/qa-agent/briefs/2026-10-08_nexusai-gate-batch20.md:58`, plus the JOINS lines `:467` (RD-777 TIER 1) and `:469` (RD-747 `968ee14` TIER 1).
  - The RD-751 and RD-817 tiers come from the READYs, `/Volumes/Laptop-DEV/TUESDAY/0_Brain/daily_tuesday/2026-10-08.md:100` (*"RD-751 @ 7a6d6bd (tier 2, test-only …)"*) and `:112` (*"RD-817 @ e504339 (… test-only, tier 2 …)"*).
- **Gate 19 (RD-794 T1, RD-819 T1 stacked, RD-721 T1+browser):** `fleet/briefs_staged/2026-10-12_nexusai_gate19_RELEASE.md`:
  - `:5` *"RD-794 @ cd171f9: GO WITH FINDINGS (F-794-1, F-794-2 Minor; MG-vc-fn survivor, RD-820)."*
  - `:6` *"RD-819 @ fdd07af: GO WITH FINDINGS (F-819-1 Polish). Merge only after RD-794."*
  - `:10` *"RD-721 Icons @ 64ee309: GO WITH FINDINGS (own survivor M-prefixLoose, named)."*
  - `:14` gives the turn items 20-22.
  - Tiers are in `…/qa-agent/briefs/2026-10-07_nexusai-gate-batch19.md:59`.
  - The stack rule is NexusAI `1_Project_Definition/CLARIFICATIONS.md:2164` (C-199 ADDENDUM): *"the same pattern is applied to RD-819 STACKED on RD-794"*, and `:2165` *"RD-794 first, RD-819 on top in a LATER turn, never in the same push."*
- **Gate 21 (RD-775 T1, RD-131 T2+browser, RD-807 fix T2):** `fleet/briefs_staged/2026-10-12_nexusai_gate21_RELEASE.md`:
  - `:4` *"RD-775 @ 537741c: GO WITH FINDINGS … #69's closure is a POST-MERGE landing condition (C-209)."*
  - `:5` *"RD-131 @ e7d2cd1: GO."*
  - `:6` *"RD-807 F-807-1 fix @ ff5d725: GO WITH FINDINGS."*
  - `:11` gives items 23-25.
  - Tiers are in `…/qa-agent/briefs/2026-10-12_nexusai-gate-batch21.md:57`.
- **Gate 25 (in flight, TIER 1, AS MERGED: RD-761 on c7ca0ed, RD-794 in both orders):** `…/qa-agent/briefs/2026-10-18_nexusai-gate25-rd761-rd794-merged.md:1-8`.
- **NexusAI's own records:**
  - CLARIFICATIONS `:1801` (C-170, Kam's option (b)).
  - `:1913` (RD-594): *"DELIVERED AS GUARD CELLS 2026-09-27; the property PRE-EXISTED via RD-518 round 3"*.
  - `:2270` (C-209, post-merge alert closure).
  - **Main's `HISTORY.md` (8,383 lines) mentions none of RD-627b, 682, 705, 413, be0fe37 or RD-681.** The grep found no history record of why the 5a/5b sequence stopped. `5_Project_History/` holds no history.md.

## PROPOSAL (Tuesday rules; nothing here is a ruling)
**(i) DONE, superseded or abandon candidates**
- **DONE: RD-681.** `4209299` and `faea66b` are ancestors of main (rc 0), `__tests__/rd681-clear-undecryptable-key.test.js` is on main, and Jira is Release Ready. It needs only a "landed" line in the record.
- **Superseded: none, by the three content instruments.**
- **Watch item: RD-594.** It adds cells only. Its property pre-existed (CLARIFICATIONS:1913), and main has since added direct projection cells: `__tests__/rd603-health-projection.test.js` and `rd518-r3-health-detail-decision.test.js` both name `keyVaultEncryption`.
  - Its K1/K2 open-window route census is not on main (its test file is absent). So it is NOT an abandon candidate on this evidence.
  - It is a candidate for Tuesday to compare against rd603's cells before spending gate time.

**(ii) Turn order, batched for ONE next gate (gate 26)**
- **0. Nothing lands while gate 25 runs.** Gate 25's kit pins main `c7ca0ed` and treats a moved head as a reason to stop (§1). Next come gate 25's verdict and its landings (RD-761, then RD-794 in the ruled order), each through C-190's PR path.
- **1. Gate 26, chain A: TIER 1, one sequenced chain of merged trees.** Every member shares `backend/server.js` with main, and with each other where noted. The chain is built on the main that results after RD-794 lands:
  - **RD-819** first. It is stacked, so it gates on main+RD-794, never alone (C-199 ADDENDUM).
  - Then the 5a order, as released: **RD-627b -> RD-682 -> RD-705 -> RD-695 -> RD-413**. The B-2 rule puts 627b before 682.
  - Then **RD-831**, which shares `static/legal.html` with RD-721, so it is sequenced rather than batched.
  - Then **RD-721**, the auth gate's static prefixes, with its browser leg. Screenshots go to Kam before any demo deploy (gate-19 RELEASE `:14`).
  - RD-831 has no main changes under it, but it must sit somewhere relative to RD-721. Placing it in the chain costs one tree; it is not a full re-gate of its own.
- **1b. Gate 26, file-disjoint TIER 1 members beside chain A:**
  - **C-170 `be0fe37`**, only after S101O's re-check READY (its queue item 3). It keeps its image legs and the arm-ttk.yml workflow-scope question.
  - **RD-594**, a cells-only row: its cells and K2 population by name on the merged tree, with C-F1's plants re-derived against the moved `healthProjection.js`. Or drop it under (i).
  - Measured, all members are file-disjoint from chain A and from each other.
  - The 09-29 RELEASE put C-170 after RD-413. That is a sequencing convention, not a file dependency (MEASURED: disjoint). Keep it only if it costs nothing.
- **2. Counts-only TURNs, one at a time, in the old relative order.** These can run while gate 26 runs, because they are file-disjoint from every gate-26 member (pairwise MEASURED).
  - **Order:** RD-751 -> RD-817 -> RD-747 -> RD-777+776 -> RD-807 -> RD-131 -> RD-775 -> RD-696.
  - **Each landing re-forwards the counts file only.** The gate-26 merged trees then land later as counts-only forwards of their gated trees, as RD-801/802 did.
  - **CodeQL conditions to read after each land (C-209):** RD-777/776 #83/#84/#43; RD-775 #69; RD-807's own alerts (#73/#74 per gate 19's kit line 8).
- **3. RD-476 (S101O) goes after RD-794 lands.** Its QA (tier 2, then Kam's look) runs on that tree.
  - It merges cleanly on main+RD-794 and on main+RD-794+RD-819 (rc 0, MEASURED). The hunks are apart: RD-476 at model-config.js 49-110, and RD-794 at 37-38 and 167-361, which takes in `systemPrompt: SYSTEM_PROMPT` at ~266.
  - But RD-794 restructures the provider config the prompt rides in, and both touch the rd395 mock.

**(iii) Re-gate as merged versus counts-only TURN, per head, and the instrument that decided it**
- **Re-gate AS MERGED (gate 26):**
  - **RD-627b, RD-682, RD-705, RD-695, RD-413 and RD-721.** Instrument: the both-sides set includes code (`server.js`, plus first-run-setup.js and settings.html). They are 303-328 commits behind for 5a and 138 for RD-721. They are tier-1 security surfaces (credential store and audit, mail secret storage, no-store on credential pages, the auth gate's static prefixes). Patch-ids are equal, but per ANSWER-5 that does not prove coverage.
  - **RD-819.** Instrument: the stack (`cd171f9` is its ancestor) plus server.js on both sides. Same tier-1 reasoning as RD-794 in gate 25.
  - **C-170.** Instrument: the main-changed set since `1904765` includes `Dockerfile`, `.dockerignore`, `package.json` and `package-lock.json`. These are exactly what its package build and image guards consume. It is tier 1 (the package door).
  - **RD-594, cells only.** Instrument: main's log since `1904765` shows RD-603 moving, and changing, the projection its cells guard (`eb90f92`, `7983c9d`).
  - **RD-831, in the chain for sequencing.** Instrument: the pairwise file overlap with RD-721. Its own both-sides set is counts-only.
- **Counts-only TURN candidates (RD-801/802 precedent).** For each one the conflict is the counts file only, every gated file is byte-identical in the merged tree, and main made 0 changes to the module the head changes or tests since its base (census above):
  - **Tier 2:** RD-751, RD-817, RD-696 and RD-807 (the fix head is tier 2).
  - **Tier 1:** RD-747, RD-777+776 and RD-775. The precedent was set at tier 2 (gate 19's kit `:59`: *"RD-801 and RD-822 are TIER 2"*), so **extending it to tier 1 is Tuesday's ruling**. The alternative is cells-by-name rows for these in gate 26, which is cheap because they share no files.
  - **RD-131 (tier 2 + browser)** is one step outside the precedent, because `static/js/index.js` auto-merges (patch-id equal, 4,741 lines from main's only hunk). My lean is a TURN, with its browser leg named NOT RE-RUN. That is Tuesday's call.

## UNMEASURED
- **Why the 5a/5b sequence stopped after RD-681.** I found no record of it in main's HISTORY.md, NEXT-PICKUP or the daily notes.
  - NEXT-PICKUP:1158 shows that on 09-29 "ALL MAIN PUSHES PAUSED", with RD-681 piloting PR #32 under the new CodeQL ruleset. That is a plausible cause, but it is inferred, not read.
- **Gate reports 5a, 5b, 19, 20 and 21.** They are on the unmounted T9. Every verdict above is RELAYED from Tuesday's RELEASE files and pickup, not read in a report.
- **No semantic interaction was probed.** Every "no interaction" above is a text census (file sets, hunk distance, keyword lines). As gate 25's WRONG 5 says, a census cannot see a call through a helper or a library. No jest, npm, docker or HTTP was run.
- **C-57 / C-133 id accounting for any head on today's main.** Not run. It is needed per TURN, at the merge hold.
- **CodeQL state of each PR.** Not read (no gh calls made). PR refs exist for #58 (RD-761), #67 (RD-777/776) and #70 (RD-775); RD-794 has no PR ref (`ls-remote`).
- **Whether RD-807's seat has `ff5d725` locally.** The NexusAI repo does not have it, so a seat must fetch it before its merge.
- **The NexusAI `.git/objects` loose-file count went from 56 to 74 during my window.** I attribute this to the live S101O seat, but only partly:
  - 9 files are stamped 12:18:02, including S101O's commit `3939290` (`find -newermt` + `cat-file`).
  - 9 trees and blobs stamped 12:19:33 and 12:19:49 have no commit. I attribute them to S101O's activity, not to me. The only NexusAI verbs I ran then were read-only (`--no-optional-locks diff/log/ls-files`), but the attribution is INFERRED.
- **Every test-to-module mapping is grep-based.** Tests that boot `server.js` through helpers are counted by a pattern, not traced.

PROVENANCE: scratch store `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/1c3b60d3-2efd-41a2-8d45-bc3872ebb4c7/scratchpad/store.git`. Raw outputs are in that scratchpad: `lsremote.txt`, `localrefs.txt`, `census2.out`, `mcommits.txt` (the scratch main+head commits), `fs/` (per-head file sets) and `jira_*.json`. Scripts are in `scratchpad/tools/`. Ran 12:13-12:22 AEDT 2026-10-18.
-- drafter for Tuesday (read-only; nothing pushed, mailed, commented or deleted)
