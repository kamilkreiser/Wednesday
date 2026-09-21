# BLUF — NEW SEAT Datasec/NexusAI-G takes LANE C: the release gate on the Marketplace package branch. (1) Merge the current main into `mkt-selfcontained-pkg-s64` (`a643fe1`) on a NEW branch, forward, never rebased. `DEPLOYMENT_GUIDE.md` will conflict: resolve it under Tuesday's §1.5 principle (the guide states what the merged product does, measured) and report the hunks in the READY. (2) Then RD-526, RD-527, RD-528, RD-529, RD-471, RD-472 and the listing folds (RD-465 O-4, RD-454 O-4), plus the dev scripts' registry parameters, up to the image digest. The digest waits for Kam's 2.2.0 image push, which is his to do, not yours. Every item ends at READY FOR QA to Tuesday. Nothing merges to main from this seat, and nothing merges into the package branch itself, without a separate Tuesday GO after a QA gate.

**This brief is addressed to the cockpit seat `Datasec/NexusAI-G` only.** It is not addressed to `Datasec/NexusAI`, `-D`, `-E`, `-F` or any other suffix. The inbox `datasec-nexusai@agentmail.to` is SHARED with NexusAI-F (lane A, live). A mail addressed to `Datasec/NexusAI-F` is not yours, however familiar its conversation looks.

**Authority:**
- Kam, 2026-09-21 ~15:2x AEST, typed to Tuesday: **"keep working through it and email me the zip when it's ready to upload and resubmit."** This is the resubmission push. The project builds the zip, Tuesday emails it, and Kam uploads (C-23; path map §BLUF).
- Kam, 2026-09-21 18:18:12 AEST, live board, verbatim (C-127): *"Until we have a stable version, feel free to redeploy, merge, or do anything else to get us to a point where everything is fully ready."* Tuesday's reading, recorded in C-127: merges are **Tuesday's GO on a QA-gated head**. It does NOT cover production, Partner Center or Marketplace upload, money, or external comms.
- C-32: Tuesday authorises commissioning and sequencing. The GO for the plan AS BRIEFED is given now (see PLAN CONFIRMATION). **No merge GO is given in this brief.**
- C-58 (+ its CONFIRMED line, Tuesday 2026-09-17T09:48:47Z) and C-62: the package branch does not merge to main until the release gate is done: main merged in again, the dev scripts fixed, the listing folded, and the real digest set and checked. RD-526..RD-529 are fixed INSIDE that gate (C-62).

**Read first:** the path map, `git show 710e875:docs/resubmission/2026-09-21_path-to-resubmission-zip.md` (whole; §1 step 6 onwards and §3 are yours). The lane partition, `git show 710e875:docs/resubmission/2026-09-21_stage2-lane-partition.md` ("Lane C"). `HANDOVER-S76D.md` §6 and `HANDOVER-S77F.md` §0-§1 (for what lane A holds). CLARIFICATIONS: C-23, C-27, C-28, C-32, C-49, C-50, C-54 (and its additions), C-56, C-57 (and its amendments), C-58, C-60, C-62, C-65, C-67, C-68 (and its amendment), C-71, C-72, C-73, C-89, C-91, C-98, C-105, C-110, C-111, C-120 (and its addendum), C-124, C-125, C-126, C-127.

## 0 — ESTABLISH YOUR SEAT FROM THE PROCESS TABLE FIRST (C-111)
Walk your own shell's parent chain to the `zsh -c` launcher process. Its command line ends `[cockpit] Datasec/NexusAI-G exited — pane stays for inspection`. Record that pid, your own `claude` pid and your tmux pane id, and put all three in the plan confirmation. **If the walk ends at any other label, that is the finding: do nothing else, and mail Tuesday.** Never decide which seat you are from `4_Credentials/.launch_preflight_last.txt` (per-project, last-writer-wins, RD-587) or from which inbox conversation looks like yours. Use session tag **S78G** in branch names, worktree names, files and mails.

**The other seats on the floor, as Tuesday measured them (03:38-03:40 AEST 2026-09-22):**
- **Lane A = `Datasec/NexusAI-F`, session S77F, tmux pane `%34`, launcher pid `94091`, claude pid `94093`, started 21:37:49 AEST.** At 03:40 it held the **jest lock** (`nexusai-lock.sh jest s77f-rd525-fwd …`, pid `30313`) for the RD-525 forward-merge verify. Its queue after that (per Tuesday's pickup DELTA 55, and `HANDOVER-S77F.md` §1): RD-525 merge → RD-575 forward merge (then gate 4) → the RD-524 A3 test-isolation fix (gate 3 round 2) → F-B1 (RD-615) → F-B2 (RD-616) → RD-607 → RD-583 → RD-531+497 → RD-510 → the rest. **So main WILL move while you work. Re-read every sha yourself.**
- **F owns** `backend/server.js`, `backend/jsonStorage.js`, `backend/bootPreflight.js`, `static/**`, `.dockerignore`, `Dockerfile`, and now also `backend/customerDataFiles.js`, `backend/dataErasure.js`, `backend/dataExport.js` (lane B wrapped and handed them on), plus the `__tests__` files for all of those. **None of them is yours.** If you need one changed, mail Tuesday. Do not take it because it is one line (C-111).
- `%0` = tuesday (launcher `33220`), `%3` = fleet-monitor (`54400`), `%8` = an idle respawned shell (`69949`, label "wednesday"). NexusAI-D (S76D) and NexusAI-E (S76E) have wrapped. No QA gate pane was open at 03:40.

## YOUR FILES (lane C)
From the partition's "Lane C" row at `710e875` (measured at `aae041a`), plus what the tickets name:
- `azure-marketplace/**`
- `bicep/**`
- `DEPLOYMENT_GUIDE.md` (lane C since RD-516 landed on main at `47be2b0`; lane A now asks, it does not edit)
- the packaging scripts: `scripts/marketplace-package-build.sh`, `scripts/validate-marketplace-template.sh`, `scripts/build-plan-packages.sh` (DELETED on the package branch, see §1), `scripts/deploy-dev.sh`, `scripts/provision-customer.sh` (the "drop the removed registry parameters" step)
- the package tests: `__tests__/marketplace-package-build.test.js`, `__tests__/marketplace-single-build-path.test.js`, `__tests__/marketplace-setup-checks.test.js`, `__tests__/marketplace-keyvault-durability.test.js`, `__tests__/marketplace-template-log-analytics-enabled.test.js`, `__tests__/rd461-self-contained-and-template-toolkit.test.js`
- the docs RD-526 names: `docs/MARKETPLACE_TEST_PROCEDURE.md`, `docs/REFERENCE_ARCHITECTURE.md`, and `docs/runbooks/**` (partition row)
- `scripts/verify-expected-counts.json`: every lane, never hand-edited, regenerated on the merged tree (C-57, C-68, C-89)
- `HISTORY.md`: your own history branch only (C-91)
**Not yours, even though a ticket might reach for it:** `README.md` (RD-526's guard extension may need to SCAN it; editing it is a question to Tuesday first). `PRIVACY.md` and `TERMS_OF_SERVICE.md` are edited by nobody (C-65, C-105).

## STATE AT DRAFTING — re-read every sha yourself before acting
| ref | sha (origin, 03:40:54 AEST) | what it is |
|---|---|---|
| main | `f1319ac` | RD-495 + RD-498 merged on RD-516 (`47be2b0`) on RD-604 (`bdca588`); counts **3840 / 218**. F is merging RD-525 next, so main will move. |
| mkt-selfcontained-pkg-s64 | `a643fe1` | the package branch; RD-505 DONE here (C-71, C-120 addendum); 4 commits not on main; merge-base with main `784b831`; main is 114 commits ahead of that base |
| s76d-path-map | `710e875` | path map + lane partition, docs only, NOT on main. Not yours to merge. |
| rd-525-export-erasure-coverage-s76e | `792fda0` | F's next merge (lane B files + server.js + counts). Not yours. |

- **Demo** runs `aae041a` (revision `nexusaidev-app--0000099`, per HANDOVER-S76D §0 and Tuesday's DELTA 52 measurement; not re-read for this brief). CI deploy from main is OFF (`CI_DEPLOY_ENABLED`, C-126). **The demo is not yours in any direction.**
- **Never touch the `2_Project_Files` working checkout** (C-28: never write, pull, restore, reset, check out or stash it; C-67: never read it for product truth either). **Work in fresh worktrees at ABSOLUTE paths outside the clone**, cut from `origin/<ref>`, under `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/` with an `-s78g` suffix (e.g. `.../worktrees/release-gate-s78g`). Do not reuse the older package worktrees (`mkt-pkg-s64`, `rd-505-pkg-s65`, `mkt-rc-selfcontained-s62` and the rest) and **do not prune `worktrees/mkt-rc-selfcontained-s62/node_modules`** (other worktrees' node_modules chain to it; C-54 03:30Z).
- Every file:line you quote names its head, e.g. "DEPLOYMENT_GUIDE.md:40 at a643fe1" (C-67).

## 1 — THE RELEASE-GATE MERGE (main into the package branch)
**What Tuesday measured at drafting** (a `merge-tree` of `a643fe1` and `f1319ac`, written to a scratch object store, not the repo):
- **rc 1, exactly two conflicts:** `DEPLOYMENT_GUIDE.md` (content) and `scripts/verify-expected-counts.json` (content). This matches the path map's prediction at `aae041a`.
- **`DEPLOYMENT_GUIDE.md` has ONE conflict hunk, in §1 "Deploy from Azure Marketplace", steps 2-5.** The package side (`a643fe1`) is the long version: the region list, the setup-check deployment script `<site name>-input-validation`, its `session-secret` / `aoai-key` read-backs, the temporary storage and container instance, and the `postDeploySetupHint` outputs. Main's side (`f1319ac`) is the short version, and it says the wizard is "step 5" where the package side says "step 6".
- ⚠ **Both sides of that hunk say "the Key Vault choice"** (`DEPLOYMENT_GUIDE.md:40` at `a643fe1` and at `f1319ac`). **`azure-marketplace/plans/README.md:33` at `a643fe1` says "It does not offer a Key Vault choice."** RD-505 removed the bring-your-own option (C-71). So neither side is right as it stands. Say so in the hunk report.
- `azure-marketplace/combined/mainTemplate.json` auto-merges; the merged file parses as JSON. arm-ttk has NOT been run on it (path map §1 step 6).
- `scripts/build-plan-packages.sh` is DELETED on the package branch (RD-506, one build path) and untouched on main since the base, so the merge drops it. Expect that; name it in the READY.
- C-72's hazard is absent from the merged tree: `admin-reset` occurs 2 times in `backend/server.js` at `a643fe1` and 0 times at `f1319ac` and in the merged tree. **Re-measure it on your own merged tree and quote it.** If it is not 0, STOP and mail.
- Counts: main `f1319ac` = 3840/218; `a643fe1` = 3276/177.

**Do this:**
1. `git ls-remote origin refs/heads/main refs/heads/mkt-selfcontained-pkg-s64`. The package branch must read **`a643fe13b91c30cf21be8d131da8c395e0c99220`**. If it moved: STOP, mail. Main will probably not be `f1319ac` by then; record whatever it is. That is the main you merge.
2. **Prior work first (C-49):** `git log --oneline <main>..origin/mkt-selfcontained-pkg-s64` (expect `c7f62f2`, `ab61499`, `9eee3ff`, `a643fe1`). Read `5_Project_History/2026-09-17_package-feature-lineage.md`, RD-450's and RD-460's comments, and the RD-460 round-2 report `qa-reports/2026-09-17-rd460-package-r2-9eee3ff-regate-report.md`. Note that `ab61499` was an EARLIER forward merge of main into this branch; read how it was resolved.
3. Fresh worktree off `origin/mkt-selfcontained-pkg-s64`, on a NEW branch **`mkt-release-gate-s78g`**. Then `git merge --no-ff --no-commit origin/main`. Forward merge. Never rebase, never squash.
4. `git diff --name-only --diff-filter=U`. **If it lists anything other than `DEPLOYMENT_GUIDE.md` and `scripts/verify-expected-counts.json`, STOP and mail.** Main may have gained a file that collides (for example a lane-A change to `DEPLOYMENT_GUIDE.md` or `Dockerfile`); that is a finding, not something to resolve.
5. **`DEPLOYMENT_GUIDE.md`: TUESDAY'S RULING IS GIVEN NOW AS A PRINCIPLE, so you do not stop on it (SUPERSEDES the "report and stop" wording elsewhere in this brief).** The ruling: **the guide states what the MERGED product does, measured against the merged `mainTemplate.json` and `createUiDefinition.json`, not what either side's prose says.** Concretely: keep each statement from whichever side matches the merged template; the step number follows the merged wizard; **no sentence may offer a Key Vault choice unless the merged wizard has one** (RD-505 / C-71 removed it; `azure-marketplace/plans/README.md:33` at `a643fe1`). Resolve it that way, then carry on. **STOP only if the measurement contradicts itself or the principle cannot decide a line** (for example, the merged template still exposes a Key Vault input), and then mail the QUESTION below. Either way, the READY carries a hunk report: Mail Tuesday `[Datasec/NexusAI-G -> Tuesday] QUESTION: release-gate DEPLOYMENT_GUIDE.md hunks`, with:
   - each hunk verbatim, with both sides;
   - where each side came from: `git log --oneline <base>..<side> -- DEPLOYMENT_GUIDE.md` on each side, and the ticket each commit names;
   - what each side states that the merged product actually does, checked against the merged `mainTemplate.json` and `createUiDefinition.json` (for example: does the input-validation script still exist, does the wizard have a step 5 or step 6, and does any Key Vault choice remain);
   - the resolution you applied under the principle, line by line, with the template evidence beside each line.
   Mail subject if you DO stop: `[Datasec/NexusAI-G -> Tuesday] QUESTION: release-gate DEPLOYMENT_GUIDE.md hunks`; leave the merge uncommitted while you wait.
6. With `DEPLOYMENT_GUIDE.md` resolved under the principle, regenerate counts on the merged tree (C-57, C-68 amendment): `npm run verify -- --maxWorkers=2 --update-counts` through the lock, then **`git add scripts/verify-expected-counts.json` AFTER it is rewritten** (C-89's failure was a rewrite that was never re-staged). Run the C-57 id-superset control against both parents: `session-tools/c57-id-superset.sh`, reported "merged N ⊇ A M ∪ B K; missing 0". Commit message: "counts file regenerated on the merged tree; id superset control: missing 0".
7. Full verify GREEN on the committed merge, through the lock, with the four floor clauses evidenced. Name every `__tests__/marketplace-*` suite and `rd461-self-contained-and-template-toolkit` individually, with their N/M (C-68).
8. **The package checks on the merged tree:** arm-ttk on the merged template (the partition says it has NOT been run; C-60 says 49/49 with the 18 wizard tests running is the bar). Run `scripts/validate-marketplace-template.sh`. Run `scripts/marketplace-package-build.sh` in DRAFT mode only. It MUST fail on the placeholder digest `nexusaireleaseacr.azurecr.io/nexusai@sha256:RD-460-DIGEST-NOT-SET` (`mainTemplate.json:106` at `a643fe1`; `release-policy.json` `imagePlaceholder`). Quote the MANIFEST line.
9. C-89: `git diff --quiet HEAD` holds, and `git show HEAD:scripts/verify-expected-counts.json` equals the measured numbers. Quote both. Push `mkt-release-gate-s78g` (a new branch; no force, no `--no-verify`). **Do NOT push to `mkt-selfcontained-pkg-s64`**: that waits for a Tuesday GO after the gate. `ls-remote` and quote.
10. **READY FOR QA**: `[Datasec/NexusAI-G -> Tuesday] READY FOR QA: release-gate merge of main <sha> into mkt-selfcontained-pkg-s64 @ <sha>`.

## 2 — THEN THE RELEASE-GATE ITEMS, one branch each, stacked on the release-gate branch
Cut each branch from the CURRENT head of `mkt-release-gate-s78g` (or from its successor, if Tuesday has GO'd it into the package branch by then), with an `-s78g` suffix. Do them one at a time, in this order. Each one goes PRIOR WORK → cells that assert the property after the fix (C-98) → red-proof → full verify → **READY FOR QA**. After each READY, go straight on to the next item; do not wait for its gate. **Board states below are as read by Tuesday on 2026-09-22 ~03:40 AEST (REST, read-only).**
- **RD-526** (To Do / High, labels `blocker`, `release-gate`). F-1 Major: `docs/MARKETPLACE_TEST_PROCEDURE.md:15`, `:36` and `docs/REFERENCE_ARCHITECTURE.md:100` still name the retired `dist/plan-managed-ai.zip`. The RD-506 guard does not scan `docs/`. A pre-RD-463 build-script copy sits in `session-tools/` (it is at `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/marketplace-package-build.sh`). **The accepted fix (C-62):**
  - point both docs at the checked build's output name;
  - extend the RD-506 guard to `docs/**` and README, with a red cell on retired artefact names;
  - MOVE (never delete) the session-tools copy to a name that cannot be mistaken for the checked build;
  - leave `2_Project_Files/dist` alone (C-28);
  - restore the O-6 "$0 preview deploy lands a Container App, not a VM" step, and record its removal in PRIOR WORK.
  RD-526 comment 37864: `__tests__/marketplace-single-build-path.test.js` exists on the package branch ALONE, so this work lands there.
- **RD-527** (To Do / Medium). The leftover-zip refusal (`scripts/marketplace-package-build.sh:62` at `9eee3ff`, `find "$OUT" -maxdepth 1 -type f -iname '*.zip'`) misses a symlinked zip, a symlinked output dir and a zip in a subfolder. A mid-build zip survives with a "No zip was written" message.
- **RD-528** (To Do / Medium). 6 of 13 gate mutations survive the package cells, including Q9/Q10 on the C-42 open-window warning in `postDeploySetupHint`. arm-ttk 49/49 is run by hand only; no CI job or cell runs it.
- **RD-529** (To Do / Low). O-1 (failed builds leave zips in `$TMPDIR`), O-7 (no committed listing list: commit one with the release gate; the path map's run reused `session-tools/build-scratch/listing.1haOHl`), O-10 (a stale RD-460 digest comment would ship), O-11 (whitespace in the printer fields). **O-8 is DONE on main** (`d881f95`, an ancestor of `f1319ac`, measured). Do not redo it.
- **RD-471** (To Do / High). The build check records a false `[PASS]` when the wizard's `containerImage` is a DropDown or OptionsGroup (`element_default()` reads `defaultValue`, which is a label).
- **RD-472** (To Do / Medium). The build check does not walk inline `Microsoft.Resources/deployments` templates, `Microsoft.App/jobs`, or case-variant output keys.
- **The listing folds:** RD-465 O-4 (the export and erasure wording in the listing draft) and RD-454 O-4 (the listing presents the Entra group as required; it is optional). Both come from C-54's additions and C-58's release-gate line. Measure where the listing text lives before editing.
- **`scripts/deploy-dev.sh` and `scripts/provision-customer.sh` stop passing the removed registry parameters** (C-58 release-gate line; path map step 6). Measure the parameters against the merged template first.
- RD-460 (To Do / Highest) and RD-450 (In Progress / High) are the umbrellas. **Do not transition either one.** Comment on them with pointers only.
- **RD-511** (Container Apps ingress measurement) and the **C-58 item 1 dev revision pull** need Azure. They are NOT in this brief. They wait for a separate Tuesday GO (§HELD).

## 3 — THE DIGEST: WHERE YOU STOP
- The image is built from **MAIN at the merged head, NEVER from the package branch** (C-72). You do not build it and you do not push it. **Kam pushes 2.2.0 to `nexusaireleaseacr`** (C-27, C-56, C-73).
- When all of §1-§2 are READY: mail `[Datasec/NexusAI-G -> Tuesday] READY FOR DIGEST: package branch waits on the 2.2.0 image`. Include the main head the image must be built from, what is merged into the package line, and the exact file:line where the digest goes. Then STOP.
- Setting the real digest, the anonymous-pull read-back of one dev revision (C-58 item 1, Tuesday-authorisable), the non-draft package build, the package QA gate and the zip email all come AFTER Kam's push, each on a separate Tuesday GO.

## 4 — RESIDUALS THE PACKAGE MUST NAME (every READY's "NOT TESTED", and the final MANIFEST notes)
- 🔴 **C-124: the Key Vault SUCCESS path has never been executed by anyone.** No real managed identity has been watched obtaining the key (`kv-wrapped`, `keyVaultStatus: configured`). Everything known about it is a CODE claim. Where to prove it is Kam's call (C-20). A GO on this package reads "the failure path behaves correctly", never "the Key Vault feature works".
- No customer deployment through Partner Center before submission (C-69 row 4). `az deployment group validate` is blocked for this identity (C-20).
- No anonymous pull of the REAL release image until Kam pushes it (the registry is empty).
- The package-gate jest suites are not network-sandboxed (C-58, 07:31:08Z line).
- The accepted holes stay open by ruling (C-42, RD-564/C-86, RD-594/C-01), and legal text stays as it is (C-65, C-105). The full list is path map §3; carry it, do not shorten it.

## PRIOR-WORK CHECK (C-49) — before building each item
`git log --all -S` on the symbols you change; `git log --all --grep` for the ticket id; the branch list (`mkt-rc-selfcontained-s62`, `mkt-round4-onto-main-s60`, `mkt-template-hygiene-s60`, `wip/s64-mkt-pkg-r2` all exist at origin); `5_Project_History/2026-09-17_package-feature-lineage.md`; HANDOVER-S62, S64, S64B, S65; the RD-460 r2 report; the tickets' comments. Write down what existed, when, which round introduced it and why, or "no source found". Keep what works (C-50). C-60 (the wizard asks for the Azure OpenAI key twice, deliberately; do NOT restore `hideConfirmation`) is the kind of thing a prior-work check exists to catch.

## FLOOR — C-110's four clauses, with C-125's counter as corrected by RD-606
1. **Every** jest invocation goes through `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/nexusai-lock.sh jest <tag> …` with `--maxWorkers=2`, including probes, single suites and package-build cells. Docker takes `nexusai-lock.sh docker`. **F holds this lock for long verifies; queue behind it. Never break or take over its lock.**
2. **Hold the lock ONCE across a multi-run measurement** (a red-proof pair, the regenerate-then-verify pair). Never per run.
3. **Record the foreign-server count beside every result** with `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76e/floorcheck.py` (basename of argv[0] is `node` AND the entry point ANYWHERE in argv). **"Ours" means the server's ancestor chain contains YOUR OWN claude pid.** Shared ancestors (tmux, launchd) prove nothing. Run `--selftest`, and use `--expect-foreign <pid>` as the negative control. Do NOT use `session-tools/s76d/floorcheck.py`. Do not use F's `session-tools/s77f/` copies either: they are anchored to F.
4. **A ZERO IS ONLY REPORTABLE IF A CONTROL FIRED IN THE SAME WINDOW.** Spawn a control the harness's way, require the count to RISE, reap it.

Reap everything you start. Never detach a hold with `&` inside a background shell: it reparents to launchd, and the counter aborts with "no claude ancestor" (HANDOVER-S77F §2). Before each red-proof, write down which cells you expect to redden and how many.

## HELD — decisions this seat is NOT making
- **No merge to main. No push to `mkt-selfcontained-pkg-s64`.** Both need a separate Tuesday GO naming them, after a QA gate. Your pushes go to your own `-s78g` branches only.
- **Kam's, and untouched:**
  - the 2.2.0 image build and push to `nexusaireleaseacr`;
  - Partner Center, including any preview or test deploy;
  - any upload or submission;
  - RD-594's scope, RD-362's rotation, and the C-124 proof;
  - production, money, and external comms.
- **Not this seat's:**
  - demo redeploy (it needs a separate Tuesday GO under C-127, and it is not lane C's);
  - any `az` write, registry change or Container App revision (RD-511 and C-58 item 1 included);
  - deletes, tag overwrites or anonymous-pull changes on `nexusaireleaseacr` (C-56).
- No force push. No `--no-verify`. Never rebase a pushed branch (a rebased branch gets a new name, C-57).
- Never touch the stale `2_Project_Files` working checkout (C-28, C-67).
- No edit in lane A's files (above) or on F's branches. No edit to `PRIVACY.md` or `TERMS_OF_SERVICE.md` (C-65, C-105). No hand edit to `scripts/verify-expected-counts.json` (C-57).
- **Vault:** stage Datasec paths one by one, never `git add -A`. S76D, S76E and possibly S77F appended to `daily/2026-09-21.md` without committing it (the vault was 7 ahead / 527 behind per HANDOVER-S76D §6, not re-measured). **Do NOT commit or touch those appends; leave them.**

RULED BY KAM, NOT YET IN AN ARTEFACT
- **None for lane C.** `decision_queue.sh list ruled --undelivered nexusai-` returns 0 (control: 66 ruled `nexusai-` cards listed). Two undelivered ruled cards carry the label "Datasec/NexusAI" without that prefix, and neither is lane C's: `rd104-gh-identity-acceptance-false-premise` (2026-09-07, the gh-identity residual) and `t9-nas-leg-direction` (2026-09-21, the drive-to-NAS backup direction, which is fleet tooling). C-126 and C-127 are both in CLARIFICATIONS.

RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- **The lane partition** (`710e875`): lane C = the release gate on `mkt-selfcontained-pkg-s64`, started after RD-516 landed (it did, at `47be2b0`). **`DEPLOYMENT_GUIDE.md` is lane C's; lane A mails any later need of it to Tuesday**, and Tuesday routes it to you.
- **The release-gate `DEPLOYMENT_GUIDE.md` conflict is Tuesday's ruling** (docs), GIVEN in §1.5 as a principle: the guide states what the merged product does, measured. Stop only where the principle cannot decide.
- **RD-463 and RD-505 are DONE, with no rebuild** (Tuesday's ANSWER 2026-09-21T08:14:56Z; C-120 addendum). RD-505 lives at `a643fe1` on purpose. RD-463 is on main (`b0ec4c2` is an ancestor of `f1319ac`, measured).
- **C-72:** the image comes from main, never from the package branch. **C-73:** the version is `2.2.0`. The push predicate (Tuesday, 2026-09-18 00:36:57Z and 00:45:52Z, as recorded in C-73) says the release-gate step gates the ZIP, not the image.
- **C-62:** RD-526..RD-529 are fixed inside the release gate. A Major at round 2 of 2 is ticketed, not sent to Kam.
- C-98, C-110 + C-125 (+ RD-606), C-67, C-49, C-57/C-68/C-89 as above. **C-91:** your HISTORY entry goes on your own history branch (`s78g-history-docs`), never to main directly.

## READY FOR QA — one per item, to `tuesday-agent@agentmail.to`
Subject: `[Datasec/NexusAI-G -> Tuesday] READY FOR QA: <ticket> <one line>`. Body sections, in order:
1. **Branch and head sha**, pushed and read back with `git ls-remote origin`, and **the base it stacks on** (the release-gate branch head, and the main sha merged into it).
2. **PRIOR WORK** (C-49), or "nothing replaced".
3. **What changed**: the files, each inside lane C (list any file outside it and why; there should be none).
4. **RED-PROOF**: the cells you expected to redden, written down first. Fix reverted → those cells red (quoted). Fix restored → green. One lock hold, with a clean arm (C-110 clause 4; C-130's addendum shows why).
5. **Full verify** through the lock, the four floor clauses evidenced. Honest N/M, read not inferred. Counts regenerated and COMMITTED on your branch if they changed (C-89 pair quoted).
6. **Package checks** where the item touches the package: arm-ttk N/49 with the wizard tests running, the validate script, and the draft build's MANIFEST line.
7. **Verdict line**, and **what you did NOT test** (always including §4's residuals).

## PLAN CONFIRMATION, then START
Send first: `[Datasec/NexusAI-G -> Tuesday] QUESTION: plan confirmation`. It must carry:
- your process-table reading (launcher pid, claude pid, pane, label);
- any launcher preflight warnings, VERBATIM;
- main and `mkt-selfcontained-pkg-s64` as you read them by `ls-remote`;
- your worktree paths;
- the jest lock's owner at that moment (`session-tools/locks/`).

**Then start straight away, without waiting.** The plan as briefed is GO'd. The following wait for an answer:
- a `DEPLOYMENT_GUIDE.md` line the §1.5 principle cannot decide;
- any deviation: a moved package head, an unexpected conflicting file, new scope, a file outside lane C, or anything in HELD.
If you do stop on `DEPLOYMENT_GUIDE.md`, do the §2 PRIOR-WORK checks and read-only measurements while you wait. Do not cut §2 branches until §1's merge is committed.

## WRAP
Rotate yourself at 80-90% context. Write `HANDOVER-S78G.md` in the NexusAI project root (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/`), naming each item, branch, head and next step. Push a wip snapshot of each build branch before every lock wait. At wrap:
- mail `tuesday-agent@agentmail.to`, subject `[Datasec/NexusAI-G -> Tuesday] Session wrap 2026-09-22` (or the date you wrap);
- a HISTORY entry on `s78g-history-docs` (C-91);
- confirm `.env` is not staged;
- in the vault, stage Datasec paths only, one by one, and leave the earlier seats' uncommitted daily-note appends alone.

PROVENANCE:
- main = f1319ac2842d9fe035419dc371b168fd813195b4; mkt-selfcontained-pkg-s64 = a643fe13b91c30cf21be8d131da8c395e0c99220; s76d-path-map = 710e875969a7db1c70b51fa2bac366edc136973d; rd-525 = 792fda0b3dc1884b32f3e04877f18959fbaaae77 | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files ls-remote origin <refs>` at 03:40:54 AEST | read 2026-09-22
- merge-base(a643fe1, f1319ac) = 784b831; left/right 114/4; the four package commits c7f62f2, ab61499, 9eee3ff, a643fe1; the package branch's 20 changed files incl. `D scripts/build-plan-packages.sh`; main changed only DEPLOYMENT_GUIDE.md and mainTemplate.json among lane-C files since the base | `git merge-base`, `git rev-list --left-right --count`, `git log --oneline f1319ac..a643fe1`, `git diff --name-status 784b831 a643fe1`, `git diff --name-only 784b831 f1319ac` | read 2026-09-22
- two conflicts (DEPLOYMENT_GUIDE.md, counts), mainTemplate auto-merges, one DEPLOYMENT_GUIDE hunk (§1 steps 2-5, markers at merged lines 40/74/82), merged mainTemplate parses, build-plan-packages.sh absent from the merged tree, admin-reset 2/0/0 (a643fe1/f1319ac/merged) | `GIT_OBJECT_DIRECTORY=<Tuesday's scratchpad> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git merge-tree --write-tree --name-only a643fe1 f1319ac` (tree 64cce329, rc 1; nothing written to the repo) then `git show <tree>:<path>` | read 2026-09-22
- "the Key Vault choice" at DEPLOYMENT_GUIDE.md:40 on both sides; "It does not offer a Key Vault choice." at azure-marketplace/plans/README.md:33 at a643fe1 | `git grep -n -i` at a643fe1 and f1319ac | read 2026-09-22
- counts 3840/218 at f1319ac, 3276/177 at a643fe1 | `git show <sha>:scripts/verify-expected-counts.json` | read 2026-09-22
- placeholder digest at mainTemplate.json:106; release-policy releaseRegistry nexusaireleaseacr.azurecr.io (package) vs null (main) | `git grep -n sha256: a643fe1 -- azure-marketplace/combined/mainTemplate.json`; `git show <sha>:azure-marketplace/release-policy.json` | read 2026-09-22
- d881f95 (RD-529 O-8) and b0ec4c2 (RD-463) are ancestors of f1319ac | `git merge-base --is-ancestor` rc 0 | read 2026-09-22
- RD-524 branch f422178 does NOT touch DEPLOYMENT_GUIDE.md (touches BACKLOG.md, jsonStorage.js, server.js, counts, static/js/index.js + tests) | `git diff --name-only f1319ac...f422178` | read 2026-09-22
- ticket states: RD-526 To Do/High [blocker, release-gate]; RD-527 To Do/Medium; RD-528 To Do/Medium; RD-529 To Do/Low (O-8 merged d881f95, comment 37789); RD-471 To Do/High; RD-472 To Do/Medium; RD-460 To Do/Highest [needs-decision]; RD-450 In Progress/High; RD-526 comment 37864 (single-build-path test on the package branch only) | `session-tools/s76d/jread.py <KEY>` (REST GET, read-only) with the project's Jira env | read 2026-09-22 ~03:40 AEST
- lane C row, file list, "after lane C starts, lane A does not edit DEPLOYMENT_GUIDE.md without mailing lane C", listing folds RD-465 O-4 / RD-454 O-4, deploy-dev/provision-customer step | `git show 710e875:docs/resubmission/2026-09-21_stage2-lane-partition.md` | read 2026-09-22
- steps 6-10, §3 residuals, placeholder-digest behaviour, listing list reuse | `git show 710e875:docs/resubmission/2026-09-21_path-to-resubmission-zip.md` | read 2026-09-22
- C-28, C-32, C-49, C-50, C-54 (+ additions), C-56, C-57 (+ amendments), C-58, C-60 (+ C-58 CONFIRMED 09:48:47Z line), C-62, C-67, C-68 (+ amendment), C-71, C-72, C-73, C-89, C-91, C-98, C-105, C-110, C-111, C-124, C-125, C-126, C-127, C-130 addendum | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md (1398 lines) | read 2026-09-22
- F = pane %34, launcher 94091 (started 21:37:49), claude 94093; F holds jest lock tag s77f-rd525-fwd (pid 30313); %0 tuesday 33220 (started 03:34:45), %3 fleet-monitor 54400, %8 69949 | `ps -axo pid,ppid,lstart,command` filtered on `[cockpit]`, `tmux list-panes -a` at 03:38-03:40 AEST | read 2026-09-22
- F's queue and its file ownership incl. lane B's three files after E wrapped | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md DELTA 55; /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S77F.md §0-§1 (mtime 02:57 AEST); HANDOVER-S76E.md | read 2026-09-22
- demo on aae041a rev 0000099; vault 7 ahead / 527 behind | HANDOVER-S76D.md §0, §6 (relayed, not re-measured) | read 2026-09-22
- floorcheck form and anchor | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76e/floorcheck.py header | read 2026-09-22
- no `Datasec/NexusAI-G` routing line yet (F's is line 61) | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/inbox_routing.conf | read 2026-09-22
- zero undelivered `nexusai-` rulings (control 66); two label-only NexusAI cards | `bash /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered nexusai-` and the unfiltered list | read 2026-09-22
Self-check note: re-read whole by Tuesday; the DEPLOYMENT_GUIDE stop was replaced by a principle ruling at every mention (BLUF, §1.5, §1.6, RULED BY TUESDAY, PLAN CONFIRMATION); no other contradictions found.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-22 03:43
