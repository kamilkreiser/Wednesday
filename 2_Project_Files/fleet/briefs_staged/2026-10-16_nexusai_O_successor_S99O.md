# BLUF — SUCCESSOR SEAT Datasec/NexusAI-O (lane 3), first seat on a NEW MACHINE. YOUR FIRST WORK IS RD-846: NexusAI main 3907c57 does not build into an image in ACR, which blocks the owed demo deploy and every future release image. Reproduce, bisect, make the smallest Dockerfile fix on a branch, and end at READY FOR GATE (tier 1). No merge and no deploy until Tuesday's mail. Send a PLAN CONFIRMATION first.

**Addressed to the cockpit seat `Datasec/NexusAI-O` ONLY.** No other NexusAI seat is live (floor read 2026-10-16 10:0x: Tuesday + the fleet monitor only). Establish your seat from your own pane's cockpit name (`tmux display -p '#{@cockpit_name}'`). The highest HANDOVER-S* file is S98P, so you are **S99O**.

## ⚠ THE MACHINE CHANGED — measure these before any git or build step
You run on Kam's Mac mini from the volume `/Volumes/Laptop-DEV`, not the T9. Measured by Tuesday 2026-10-16 10:1x:
- The project is at `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/`. It was synced from the T9 on 2026-10-15 by Friday, verified by count (Friday's mail, unread by you; Tuesday relays it).
- The root checkout `2_Project_Files` is on `main` at **cd2b543** (S47-era), far behind origin. Fetch before trusting anything local.
- Before your launcher ran, the repo-local `core.sshCommand` pointed at the T9 path (`ls-remote` failed: "Identity file /Volumes/KK_T9_External_HDD/… not accessible"). Your launcher rewrites it at boot. **Confirm with `git ls-remote origin refs/heads/main` as your first git command.**
- **All 222 folders under `worktrees/` hold `.git` links to the T9 path** (e.g. `worktrees/s96o-deploy-3907c57/.git` → `gitdir: /Volumes/KK_T9_External_HDD/…`). Run `git worktree repair` from `2_Project_Files` (or make a fresh worktree) before using one. Say which in your plan.
- **Docker is installed but its daemon is NOT running** (`docker info`: cannot connect to `~/.docker/run/docker.sock`). If you want local builds (plan step 1), start Docker Desktop (`open -a Docker`) and wait for `docker info` to answer. If that fails, say so and use ACR only.
- Your `4_Credentials/` (`.env`, `.azure`, `.gh-config`) is the drive's copy. Verify identities at point of use: `gh auth status` (Tuesday read `kamilDatasec`, keyring), `az account show` (unread by Tuesday).
- Disk: 977 GiB free on the volume (`df -h`, 10:08).

## READ FIRST, in this order (all in the NexusAI folder)
1. `HANDOVER-S96O.md` WHOLE (51 lines). Section 0 is your work: the symptom, the logs (`session-tools/s96o/deploy/acr-build-3907c57.log`, `-run2.log`), the five build-context commits since 0677388 (1fd5d0f, 8de8e5c, 4016ba5, 3f7e263, e224ab9), and what is already ruled out.
2. Jira RD-846, including comment 39425 (Tuesday's plan; Tuesday has NOT re-read it today).
3. Tuesday's mails on this inbox since 2026-10-13T11:00Z naming O, read WHOLE. They include the DEMO DEPLOY brief (12:04Z), the step-2 ANSWER (12:10Z) and the WRAP NOW (12:18Z).
4. CLARIFICATIONS: C-57, C-127, C-149, C-186, C-190 + addendum, C-197, C-199, C-214.

## MEASURED BY TUESDAY (2026-10-16 ~10:1x AEDT)
- origin main = **3907c5789a** (gh api repos/datasecau/Reporting_Dashboard_Au/commits/main), committed 2026-10-13T11:03:17Z. **Unchanged since S96O wrapped.**
- GitHub Code Security on Reporting_Dashboard_Au = **enabled** (gh api …/security_and_analysis). On 10-14 it was OFF, so CodeQL could not run. It can now.
- Weekly usage: 0% (statusline, renews in 6 d 22 h). No usage hold.

## YOUR QUEUE
1. **RD-846.** Unmeasured, so treat it as a hypothesis and settle it first: a THIRD state besides "a commit broke it" is a transient ACR fault. The tag `nexusai:2.2.1-s96o-3907c57` was not created, so a single retry of the IDENTICAL `az acr build` at 3907c57 is cheap. Run it ONCE, and record the run id and result, before bisecting. Then the plan from HANDOVER-S96O §0: local build at 3907c57 (classic AND BuildKit) → bisect the five commits → the smallest Dockerfile/.dockerignore fix on a branch from main → your own build proving the image builds AND the image-content guards stay green → **READY FOR GATE: <branch> @ <sha>** (tier 1: the shipped build). Tuesday commissions the gate.
2. **Then WAIT** for Tuesday's TURN mail. The merge and the demo deploy (steps 0-2 of the 2026-10-13 DEMO DEPLOY brief, RE-DONE FRESH) each need their own mail. If the retry in item 1 builds cleanly, STOP and mail Tuesday before anything else: the demo deploy may then go ahead without a code change, on Tuesday's word.

## AUTHORITY
- Build and diagnosis: card `nexusai-rd846-build-broken-demo-deploy-1013`, open, default (a) *"Tuesday's morning seat launches the RD-846 fix first, then the demo deploy."* This launch IS that default. (decision_queue.sh list open, read 2026-10-16 10:1x.)
- The demo deploy of main: Kam, Tuesday's terminal 2026-10-13 ~12:1x, verbatim *"once agents finish up, deploy everything and wrap up"* (EXPIRING-GRANTS row, an EVENT, not yet spent: the demo deploy is the part still owed). Not on this mail's authority: it waits for Tuesday's DEPLOY mail.
- Merges: the open-ended grant *"work through the tickets and merge once tested"* (Kam 2026-09-25, re-affirmed 09-27) is tied to the account it was given on, and this machine's gauge reset suggests the account has changed. **Tuesday re-confirms it with Kam before any TURN mail.** That does not hold up your build work.
- No CodeQL alert is ever dismissed. Never push an unscanned commit to main; never bypass.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- None for NexusAI (`decision_queue.sh list ruled --undelivered`, read 2026-10-16 10:1x). **Limit, stated:** Tuesday cannot read Kam's live board from this machine yet (the seat certificate is missing), so any board tap since 2026-10-14 06:4x is UNMEASURED. If one reaches you, mail it to Tuesday verbatim.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- C-186: turns only by Tuesday's TURN/RELEASE mail.
- 2026-10-13 12:10:10Z ANSWER: GO on the Entra pre-check evidence for the demo deploy, with these additions: after the swap, watch the new revision's logs for group-read failures and roll back on any hit; name the rollback anchor; say the demo then runs ahead of the 2.2.0 package. All of it is re-measured fresh at the next attempt.
- Rollback anchor for that attempt, unless it has changed: revision `nexusaidev-app--s81j-220-fdda330` on the 2.2.0 release digest `nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda3309…7f66` (HANDOVER-S96O §1). Re-read before relying on it.

## STANDING LINES
- PRIOR-WORK CHECK before rebuilding, replacing or removing anything. Every READY carries PRIOR WORK + NOT TESTED.
- Never delete (move aside). Never edit a running script. Never kill by pattern (C-174).
- Every factual sentence in a mail names its instrument, or says "unmeasured".
- zsh does not word-split unquoted lists; build file lists in bash and check for a real "Tests:" line (your own S96O lesson).
- Write the handover when your pane first shows less than 10% before auto-compact.

PROVENANCE:
- origin main 3907c5789a, committed 2026-10-13T11:03:17Z | gh api repos/datasecau/Reporting_Dashboard_Au/commits/main, GH_CONFIG_DIR=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config | read 2026-10-16
- code_security enabled | GitHub API read by Tuesday (gh api, field security_and_analysis.code_security.status) - Tuesday's measurement, not a file | read 2026-10-16
- local main cd2b543; core.sshCommand → T9; worktree .git → T9; 222 worktrees | git -C 2_Project_Files log -1 / ls-remote stderr / cat worktrees/s96o-deploy-3907c57/.git / ls worktrees | wc -l | read 2026-10-16
- docker daemon down | docker info | read 2026-10-16
- RD-846 symptom, plan and rollback anchor | /Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/HANDOVER-S96O.md | read 2026-10-16
- card default (a) | /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh list open - Tuesday's tree, not yours | read 2026-10-16

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 10:12

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-O -> Tuesday] QUESTION: plan confirmation` with your seat identity facts (pane id, cockpit name, claude pid), what you read, the result of your first `git ls-remote`, your worktree-repair choice, whether Docker came up, your launcher preflight warnings VERBATIM, and your order for item 1. Then start item 1 unless Tuesday says otherwise within 15 minutes. Your wake is Tuesday's mail plus a tap.
-- Tuesday
