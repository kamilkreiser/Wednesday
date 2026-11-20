STARTABLE: YES - the kit is whole, `stamp_check.py` exits 0 (154 claims, 154 measured), the READ list is 213 kB, and every fact it freezes was re-measured at GitHub, in the records or over the three tarballs; two conditions sit in Tuesday's slots (launch only after the C104 pane is up; the CI image's `npm ci` layer must be cached or Tuesday must grant the registry for that one step).

# B1803 drafter report: SEAT-C106, the refresh of held pull request 85 (Security Composer)

Drafter: Sonnet, read-only, 2026-11-20 from 20:11 AEDT (`date` prints 20:11:01 to 20:30:16 in the work). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1803_SEAT-C106_composer-pr85-refresh.md` (78,223 bytes), sidecar `.measured` beside it, this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s301/d1803/`.

## BLUF
1. **No file-level conflict is predicted, and a stronger statement is frozen.** The pull request changes 57 paths, main changed 87 since the base, **0 in common** (no removals, no renames on either side). The merged tree is therefore the union; a program of mine reproduces main's tree `7e6e405b...` and the head's tree `7d766102...` exactly as GitHub prints them, then predicts the merge's tree as **`e9ded89d6e2137a126525b0304f2a71d8c7d456a`** (988 files = main's 974 + the 14 the pull request adds). The seat re-derives it and compares: a tree that differs is a STOP, which catches every clean-merge surprise.
2. **The release stays byte-equal:** 10 paths under `content/` (7 release files, `SOURCES.json` and two derived sources); main changed 0 paths under `content/`, so a merge cannot touch them. Their blob shas and the four hash values (demo and draft, head and main) are frozen in the kit.
3. **The test totals B423 recorded cannot be matched, by design.** B423's 318 files / 3,213 passed / 0 failed ran with the withheld SOW text mounted; the commission forbids mounting it. Measured on main by B1581: 2 rows of `packages/content/src/citations.test.ts` stay red without it. So the kit freezes the red set as exactly those two rows at the main base AND at the merge, and a count claim as a delta (merged passed = main passed + 133, 133 = 3,213 - 3,080, relayed).
4. **The new E8-citation check on the new release is UNMEASURED by this lane** (it needs the text); that is the one thing Tuesday must decide for the review (Q-3).
5. The lock file moved on main (45 package entries, vitest 5.0.0 to 5.0.5) and not on the branch, so every earlier green was proved on the old toolchain: the kit makes that the third non-conflict hazard.

## Facts re-measured, with instruments (all in the kit's FACTS; the controls are named there)
| fact | value | instrument |
|---|---|---|
| PR 85 | open, draft, head `851057291ffb019baee6c3c51a50d7b8833f5b3a`, 14 commits, 57 files, +38887 -3186, `mergeable_state` clean | `gh api -X GET pulls/85` (account `kamilDatasec` read first; `pulls/9999` 404) |
| main | `b4681297d974ac3d8e74a4a12baeb9ea41962c52`, tree `7e6e405b...`; ahead 43 behind 0 of the base `308b7aa6...`, every commit one parent | `commits/main`, `compare` both ways |
| file lists | 57 (14 added, 43 modified) and 87 (39 added, 48 modified), common 0, `content/` 10 vs 0, `bridge/` 0 vs 0 | python over `pulls/85/files` and `compare ... files` (control: `policy-summary.ts` in main's list only) |
| release blobs | the 10 head blob shas and main's counterparts (kit FACT 4); API `sha` equals the tarball's blob for 57 of 57 | python git-blob sha1 over the head tarball |
| hashes | demo head `5db37614...`, main `05070f1d...`; draft head `5679855b...`, main `62cf4932...`; demo item counts equal at both (55 items, 123 controls) while sources 5 to 7 | `cat` of the CONTENT_HASH files, python over the bundles |
| predicted tree | `e9ded89d6e2137a126525b0304f2a71d8c7d456a` (988 files) | `treesha.py` (a claim; its main and head trees equal the API's; control: one blob replaced gives `b99a5667...`) |
| test files by the vitest project globs | head 318 (equals B423's 318: the control), main 316, merged 323 | python over the tarballs |
| hosted checks | last merged PR #130 head `632ca83c...` and PR 85's head each show 3 runs, all success (`CodeQL`, `Analyze (javascript-typescript)`, `Analyze (csharp)`); main shows 2; open alerts on main 0; ruleset has `required_status_checks: []` | `commits/<sha>/check-runs`, `rulesets`, `code-scanning/alerts` |
| lock file | base = head `f3e4197f...` (B423's value), main `e8b4094e...`; 45 `packages` entries differ base to main | python over the three tarballs |
| prior work | 200 branches compared with the old head: 68 behind, 131 diverged, 1 identical (the branch itself), 0 contain it; 130 PRs, only #85 open; no C-154 or later entry | 200 `compare` GETs, `pulls?state=all`, `grep -c` over `CLARIFICATIONS.md` (control C-153 prints 1) |
| open findings | B358-2 = BACKLOG #367 = Jira PCOMP-66; B424-1 = BACKLOG #368 = Jira PCOMP-67; both Backlog | Jira GET by `project = PCOMP AND ( labels in (...) )` (control `PCOMP-9999` 404), `grep -n` over `BACKLOG.md` |
| Composer panes | none live at 20:17 (the C104 pane was not up; its launch window ran to 20:27) | `tmux list-panes -a` (control: 12 lines printed) |
| ports | 9960-9969 free; 0 of 42 kits name a 996x port (control: `7330` is named by 2) | `lsof`, python scan |
| pointers | 111 `file:line` pointers in the kit re-printed with `awk NR` after the last edit: 110 matched; the one miss was my checker's own substring (the line is right) | python pointer checker |

## D-decisions (the drafter's choices, each open to Tuesday)
- **D1 own clone, not a worktree** (`.tools/b1803/clone`, as B1581; B423 used a worktree of the shared checkout). Reason measured: the shared checkout is stale (HEAD `0b2fca43...`, no `b4681297` object), its `core.sshCommand` names a `/Volumes/Laptop-DEV/` key path that does not exist here, and the project `CLAUDE.md` has no rule on merging or branches (3 lines match `merge|push|rebase|deploy|branch|land`, none a merge rule). The landing rule quoted is C-101's squash line (`CLARIFICATIONS.md:1799`), so the merge commit is branch history only.
- **D2 Sonnet** (row C5, `model-routing.md:95`, with C2 `:92`); I do not argue for Opus: no conflict is predicted and every risk is a printed check that STOPs. The G1 review after it is Opus (Tuesday's slot).
- **D3 the merge is `git merge --no-ff -F <message file> <BASE>`**, parents in the order (old head, main), message frozen (no ticket key, brief number, card id or name), identity the repo's own; the seat first runs `git merge-tree --write-tree` as the trial and merges only if it exits 0 with the predicted tree.
- **D4 any conflict, any trial rc other than 0, any moved main or moved head is a STOP.** The six conflict shapes are listed in the kit and each shown impossible by program; there is no shape the seat may resolve by hand.
- **D5 the chain is B1581's** (lint, format:check, typecheck, build, the two vitest projects, secret scan, `test-db.sh`) **plus B423's content checks and a base run at main** (E7 is a delta claim and needs main's own counts). Not run, with reasons: the bridge job (0 bridge paths on either side; 0 bridge files name the release), the compose-stack steps (`ci.sh:125`-`:133`, they start a stack), the fake-docker script tests (they read only main's own scripts, which the merge leaves byte-equal to main).
- **D6 READY needs the three hosted check runs `completed` and `success`;** pending after 45 minutes ends `PARTIAL B1803: <sha> | done steps 0-6 | not done step 7`.
- **D7 the seat drafts the PR-body text** (`evidence/PR85-BODY-PROPOSED.md`, four sections kept, the stale "Known red" paragraph replaced from its own measurements, no names or ids) and applies nothing.

## Questions for Tuesday (each with the default the kit uses)
- **Q-1 clone or worktree.** Default: own clone (D1).
- **Q-2 the registry for `npm ci`.** Default `cached-only` (STOP if a layer needs the network). The lock is the same on main since 2026-11-15 (B1581's PR touched 4 files, none the lock), and B1581 built an image from it, so the layer is likely in the build cache, but I could not run docker: UNMEASURED. If it is not cached the seat STOPs at Step 2 with the layer named; granting `registry-for-npm-ci-only` avoids that.
- **Q-3 the SOW text.** Default: never mounted, as the commission says; expected reds at both main and the merge are exactly the two citations rows; the new release's E8 citations are unproved by this lane. Tuesday decides whether the review mounts it.
- **Q-4 a guard in the repository** (the card's deploy refusal). Default: "not in this lane"; the kit measures how a deploy seat tells a release changed (`git diff --quiet <last deployed sha> <target> -- content/release-demo content/release-draft`, the two CONTENT_HASH texts, three controls) and names the paths a guard would touch (`scripts/`, `DEPLOY.md`), nothing built.
- **Q-5 C104.** Default: launch C106 only after the C104 pane is up and its REFUSE table passed (C104 refuses at Step 0 if any other `Composer` pane is live); and tell C104's owner that its BASE (the old head) will not read after C106 pushes.
- **Q-6 bridge job.** Default: not run (D5).
- **Q-7 main moves during the run.** Default: STOP, never merge a newer main (the predictions rest on this tip).

## THE REQUIRED QUESTION (item 2): three things that are not a file-level conflict and can still break the property
1. **A main test that reads the real release and was written for the old one.** Of 11 files pinning `05070f1d` or `62cf4932` on main, 9 are edited by the pull request; the other 2 (`b103-policy-target.db.test.ts:33`, `b113-name-target-counts.db.test.ts:32`) name it in comments only (cleared by reading). The live exposure is main's two new real-render tests, `packages/renderers/test/change-report.test.ts` (796 lines added; `realRenderInput` at `:17`, `:31`, `:32`) and `b1581-cover-date-time-zone.test.ts` (`:7`); `performance.test.ts` asserts 123 controls but reads a generated fixture (cleared). Detected by a by-program census over the merged tree (old-pin files; main-changed files naming `real-resolution|real-content|release-demo|release-draft|CONTENT_HASH`), the red set equal to the two citations rows, and those tests named by their pass lines. UNMEASURED (needs the stack): 3 browser specs naming the release.
2. **A caller main added to the scanner the branch rewrote.** `secrets.ts` is untouched by main (blob `18d98e30...` at base and main) and rewritten by the branch (`88b77292...`); main changed 6 files naming `credentialShapes`, among them `change-report.ts` (+278, strict call at `:98`). The rendered-text variant has 0 non-test callers at main. The old "strict equals main's" proof was for the file, at the old base; the callers moved. Detected by the same census at the merged tree (the rendered variant keeps 0 non-test callers beyond its export lines), the builder's differential probe (`.tools/b423/probe/cells_vs_main.ts`, with a control that must differ), the renderers project, and the secret scan.
3. **The lock file and the toolchain.** Only main touched it: 45 entries (vitest 5.0.0 to 5.0.5, vite, rolldown, ajv's fast-uri, fastify, undici) plus new eslint overrides; the branch's tests and the 17,000-line bundle were proved on the old versions. Detected by an `npm ci` image from the merged lock with versions printed, lint/format/typecheck, and `content:check` plus the demo check printing "is current" with the head's two hashes (the generator reproducing the head's bytes on the new dependencies), timing tests named and re-run once alone if red.
4. (DB half) main's migrations 0023-0027 name no content table (0 lines in each; control 0020 prints 6) and the 20 DB test files main added read the new hash through `migrate`; detected by `scripts/test-db.sh` counts equal main's.

## Step inputs (rule 4: each input is produced by an earlier step or exists at BASE)
| step | inputs | produced by / exists at |
|---|---|---|
| 0 | the kit, the key, `heavy.sh` (b1569), the slots | exist at BASE (Tuesday's stamp) |
| 0b | `branches`, `pulls`, Jira PCOMP-66/67, `CLARIFICATIONS.md` | exist (GET) |
| 1 | clone with `origin/main` and `origin/b330/...` fetched, E1-E10 | Step 0 (clone, fetch) |
| 2 | `origin/main` tree, `.tools/b1803/scripts/heavy.sh`, image base layers | Step 0 |
| 3 | trial tree (Step 1), message file, identity | Step 1, Step 0 |
| 4 | the merge commit | Step 3 |
| 5 | merged tree, Step 2's counts and red set, `probe/cells_vs_main.ts` (exists at the project) | Steps 2 and 3 |
| 6 | Step 4 and 5 passes, `ls-remote` reads | Steps 4 and 5 |
| 7 | the pushed sha | Step 6 |
| 8 | all counts, the image id, the pins | Steps 1-7 |

## Corrections to the commission and to the plan
- The commission says another Composer seat "is live beside you": at 20:17 no pane named Composer was listed (C104's window ran to 20:27); C104 refuses to start if another Composer pane is live, so the kit adds a LAUNCH-ORDER slot.
- The commission's "test totals B423 recorded" are with the SOW text mounted; they are claims to compare, not numbers the unmounted chain can reach (BLUF 3).
- "The content bundle files and both CONTENT_HASH files" are 10 paths under `content/` (7 release files, `SOURCES.json`, two derived sources); the kit guards the whole `content/` tree.
- The plan (section 5) says the pull request's builders' STATUS files were not read; I read B423, B424 and B358 (the parts named). Its facts agree with mine: ahead 14, behind 43, 57 files, 0 in common with 87, last merged PR #130 with 3 runs, 0 workflows, rulesets as read. One addition: the PR body has four sections, not the "Known red" paragraph alone being stale.
- The drafter rules file names `/Volumes/Laptop-DEV/` paths; the commission's `/Volumes/Datasec_DEV/` paths were used.
- The gate kits `.tools/b358` and `.tools/b424` are not on this drive (`ls` rc 2); only the builder's `2_Project_Files/.tools/b423/` is. The review index therefore points at the STATUS tables and evidence folders (54 and 23 run files) and cannot hand over the old scripts.
- Open findings B358-2 and B424-1 carry tickets PCOMP-66 and PCOMP-67 (the commission asked for the ticket of each); the strict-scanner gap (ruling 3) has no BACKLOG row (`grep` prints 0; control `:363` prints).

## Recommended slots
CARD: Tuesday prints the card's state (the kit refuses unless it reads `ruled a`, 20:06 AEDT, with the word "refresh"). BASE `b4681297d974ac3d8e74a4a12baeb9ea41962c52`. HEAD `851057291ffb019baee6c3c51a50d7b8833f5b3a`; open PRs: #85 only. CHECK SET: `CodeQL`, `Analyze (javascript-typescript)`, `Analyze (csharp)`. LOCK: free at drafting (`.tools/composer-heavy.lock` absent); no Composer pane live. DOCKER: Tuesday reads `docker version`. NPM-NETWORK: `cached-only` unless Tuesday grants the registry for `npm ci` (Q-2). PORTS: `none`. IDENTITY: `kamilDatasec` / `88359143+kamilDatasec@users.noreply.github.com` (main's author; the clone has none). REVIEW: G1, Opus, separate kit, Tuesday's. LAUNCH-ORDER: after C104's REFUSE table passed. HARD STOP: Tuesday sets it from the launch clock (two image builds, two full chains and up to 45 minutes of hosted wait: allow about four hours).

## The READ list and its load (by program)
The kit 77,263 bytes (before this report's last edit: 78,223 now) + 135,965 bytes of files and slices = about **213 kB**: B423 STATUS whole 34,419; B424 STATUS lines 1-14, 54-66, 102-131, 154-181 (18,393); B358 lines 162-174, 380-407, 408-447 (11,191); CLARIFICATIONS slices 1286-1297, 1682-1691, 1736-1748, 1777-1795, 1797-1799, 2853-2857 (21,351); project `CLAUDE.md` 2,719; `heavy.sh` 1,726; the two B423 probe files 24,732; `ci.sh` 7,685, `test-db.sh` 2,608, `secret-scan.sh` header 2,095, `vitest.config.ts` 2,134, `package.json` 1,481, the two content CLIs 4,276, `content.ts` slice 1,155. Under about 400 kB.

## UNMEASURED
Docker, the build cache and every image (no docker run); whether the `npm ci` layer is cached; the cost of `secret-scan.sh --history` in a clone with 167+ refs; what the live demo runs (no request to any site; the records say `05070f1d...`); the browser specs; the E8 citation rows on the new release (SOW text unmounted); whether the old scripts of the gates exist elsewhere; the text of PCOMP-66 and PCOMP-67 beyond summaries and labels (read by JQL, not whole); that CodeQL runs on a push to a draft pull request's branch (B423 saw its Analyze runs queue after its push, relayed); when C104's pane started.

## Outside-the-fences disclosure
Writes: the kit, its `.measured`, this report, and scratch under `d1803/` (three tarballs `dl/*.tgz` and their extractions `main/`, `head/`, `base/`; `a.txt`, `b.txt`, `pr85_files.tsv`, `pr85_blobs.tsv`, `main_since_base_files.tsv`, `pulls_all.tsv`, `branches.txt`, `branch_desc.tsv`, `pr85_body.txt`, `jget.py`, `treesha.py`, `measured.bak0`). Network: `gh api -X GET` only (including three tarball GETs and 200 `compare` GETs) and Jira GET (7 JQL reads and 3 control reads, credentials in-process, none printed). Slips, said plainly: one stdout redirect to `/tmp/dummy_unused` (an empty file, left in place, never deleted: it is outside my scratch folder); `sed -i.bak0` on my own sidecar created `...measured.bak0` in the briefs folder, which I moved into scratch (`measured.bak0`); one first `ls` listing ran against `2_Project_Files/.tools` (read-only). I read the same-day kit `2026-11-20_B1801_SEAT-C104_...md` (form and partition) and the commission; I did not read the decision-card store, `briefs_staged`, the scoreboard, any ledger, any WEDNESDAY or FRIDAY tree or any other project; I ran no docker, build, test, install or git write; nothing of HPSM-POC was opened; no hosted site was requested.
