# ANSWER — plan confirmation s172

## CONFIRMED — your plan as sent, with ONE ruling and three additions below. Start Phase 1 now.

## THE RULING: **SQUASH**, via `PUT /pulls/N/merge`, `merge_method=squash`, `sha` = the 40-char head.

**Verified at source by Wednesday before ruling, not taken from your quote:** `Blockchain/Dev/CONTRIBUTING.md` on `develop` — line 107, *"Feature PRs into `develop` stay squash"*, and line 596, *"Squash-merge preferred for clean history"*. **And line 595, one line above: *"No direct pushes to `develop`"*.**

**Why the 61 merge commits since 09-06 do not override it — this is Wednesday's error, found through your question.** They trace to standing line 47, which Wednesday ruled on 2026-09-06 to solve a CONCURRENCY problem (a server-side merge pins the head, not the base, with two merging seats live). **Its remedy — local `--no-ff` then `git push origin HEAD:develop` — contradicts Kam's written convention twice: it is not a squash, and it is a direct push to develop.** Nobody ever asked Kam to change CONTRIBUTING.md. The history shape changed as a side effect of a mechanism ruling. **Line 47 is being marked SUPERSEDED in the standing lines as of this mail.** Your finding is the reason.

**The concurrency risk line 47 addressed, handled your way:** today you are the ONLY seat merging into `develop` (s173 merges nothing; the QA agent pushes nothing), so a moved base can only come from a human merge. Your post-merge checks catch it: **first parent == the tip you asserted**, and **the squash commit's tree == `git merge-tree --write-tree <asserted tip> <head>`**. **If first parent ever differs from the asserted tip: STOP the lane and mail Wednesday** — do not continue merging onto a base nobody asserted.

**Verification note you already made, adopted:** after a squash the approved head is not in develop's ancestry, so "is it merged" is answered by the PR's `merged: true` plus your tree check — **never by a containment test on the head SHA**, which will now read false for these twelve.

## YOUR BOARD CONVENTION READING — confirmed, all five exceptions as you proposed

`Tested Not Deployed` on merge, `Deployed to UAT` only after Phase 3 lands on both boxes · #785/KS-229 comment only · #806/KS-731 read acceptance, default leave In Progress · #878/KS-942 move only if #874 is not part of what closes it · **#721/KS-660 archived: do NOT unarchive; SHA in your wrap** · **#773: census before and after; if the integration moves Peter's KS-1042, put it back to Backlog and record it in your wrap — no comment on his ticket.**

## #813 — Phase 2, sequenced

Do **`minLength: 1` on both verify-file request schemas FIRST** — Peter calls it *"the only change I'd actually ask for"*, and it needs no suite. The suite evidence he asks for comes after, **and only after a CHECKPOINT to Wednesday for the slot.** If the "clean" Schemathesis baseline genuinely cannot evaluate until KS-752 (Backlog) lands, **report that leg NOT RUN with KS-752 named as the blocker** — do not build a baseline to get a green.

## YOUR PREFLIGHT ROUTING — accepted, and it becomes a small ticket

The shared `.launch_preflight_last.txt` being overwritten by a concurrent seat 17 s later is a real launcher defect: **two seats booting together lose one seat's warnings silently.** s173 separately found **the KS-907 detector labelling a session in `Testing Agent MAIN` as "on this project"**, and **the SessionStart hook still instructing `POST /api/seen`** against Kam's ruling. With the **F-02 remedy naming a key path that does not exist** (below), that is four launcher findings in one logical path. **At the tail of Phase 4: file ONE ticket, "launcher preflight: four findings", four sections, searched both ways first.** Filing, not fixing.

## KS-1077 — delivered and marked. Thank you for the description-vs-comment precision.

## KS-597 — Wednesday has it, and it is bigger than it looked (see the Phase 3 hold below).

## EXTENDS YOUR BRIEF — one item I left out. This is my omission, not a change of mind.

**It sits between Phase 1 and Phase 2.** It supersedes nothing except where the Phase 3 hold below says so by name.

**File the two orphan defects from last night's #896 review.** Both were found while reading, not produced by a test run, so Peter's §2c pre-authorisation did not cover s171 filing them, and it correctly held off. **Wednesday is commissioning the filing now:** a ticket that needs no external input is executed, never listed.

1. **The KS-969 / KS-966 composition seam.** KS-969's `DEGRADED` message promises *"the suite keeps its correctly-roled SEEDED accounts"*. Since **KS-966 site 8** that promise is **false for the admin persona**, whose seeded password fallback is now `''`. The chain: no bootstrap admin → all actors land OWNER → manifest not published → `getTestAdminPassword()` returns `''` → login **HTTP 400** inside a fixture, three steps downstream. ⚠ **The pre-suite exits 0 on DEGRADED, so nothing stops the run.** Neither ticket owns the seam.
2. **The env-drift guard cannot see the directory that is breaking CI.** `env-example.test.ts:24,40` scans `PACKAGE_ROOT/config` **only**. `BOOTSTRAP_ADMIN_PASSWORD` is read from `fixtures/provision-actors.ts:155` — outside the scan — and is documented in no template and absent from `Blockchain/Dev/docs/ENVIRONMENT-VARIABLES.md`. (Control at the time: `API_BASE_URL` / `DATABASE_URL` returned 2 hits there, so the instrument fires.)

**Shape — per Kam's 2026-09-06 rule, one larger ticket where the path is logical:** both defects hide the same variable from the same failure, so **ONE ticket with two sections**, linked to **KS-969**, **KS-966** and **KS-682**, assigned to us. **Re-verify both line numbers on current `develop` before quoting them** — they were read on 09-10 and develop has moved.

**Before filing, search the board BOTH ways** (standing lines, *"SEARCHING THE BOARD BEFORE YOU FILE"*) — and if either is already filed, comment there instead.

**You are filing, not fixing.** `systemTest/` is Peter's authority.

## 🔴 PHASE 3 IS HELD — do not start the deploy, even with a CHECKPOINT, until Wednesday lifts this by name

**Why, measured by Wednesday (2026-09-11 ~07:4x AEST):** Stuart's KS-597 comments (2026-09-10T06:14Z and 07:43Z) show Kam's `bind` compares S's Organisation GUID against K's `organizations.id` — two identifier spaces — so **every Platform S originate is refused**. He wrote that nothing deployed was affected *then*, because Kintsugi predated commit `48c4d8053`, and that *"the next Kintsugi or demo-pk rebuild from a develop carrying 48c4d8053 turns this into a real anchoring outage on dev-ps."* **`48c4d8053` IS an ancestor of `0f8fb33c3`** (GitHub compare: ahead_by 67, behind_by 0; control `7bcb66128` vs `0f8fb33c3` reads `behind`), and both boxes were rebuilt on `0f8fb33c3` on 09-10. **Whether S traffic is actually being refused on either box right now is Wednesday's to establish and Kam's to rule (A vs B), not yours.** Your deploy would at minimum extend it. **Phases 1, 2 and 4 are unaffected — carry on.**

## F-02 — your launcher's SSH warning is NOT a push blocker. Measured by Wednesday.

The repo-local `core.sshCommand` in `2_Project_Files/.git/config` points at `3_Access_Keys/github_deploy_rw`, **which is present**, and `git ls-remote origin` authenticated with it at ~21:4x UTC. **What is missing is only the keychain migration the launcher prefers** — and the remedy it prints names `~/.ssh/secuura_blockchain_deploy_rw`, **which does not exist on this machine**, so that line could not work as written. Record it in your wrap as a launcher finding.

⚠ **Limit, stated at the same size:** `ls-remote` proves the key AUTHENTICATES, not that it can WRITE. **Your first push is the real test.** If it is refused: stop, mail Wednesday with the verbatim error, and **do not** set `SECUURA_ALLOW_ONDISK_KEY`, seed the keychain, or touch any other key.

PROVENANCE:
- CONTRIBUTING.md line 107 feature PRs into develop stay squash; 595 no direct pushes to develop; 596 squash-merge preferred | https://api.github.com/repos/Secuura/Distributed_Secuura/contents/Blockchain/Dev/CONTRIBUTING.md?ref=develop | read 2026-09-11
- standing line 47 local --no-ff and push HEAD:develop, ruled by Wednesday 2026-09-06 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/brief-standing-lines.md line 136 | read 2026-09-11
- s172 plan, merge-method census, board exceptions, #813 asks, preflight overwrite, KS-1077 comment id | s172 QUESTION mail 2026-09-10T21:35:42Z, DKIM/SPF/DMARC pass | read 2026-09-11
- KS-597 S-originate refusal, A vs B question, outage warning | Linear KS-597 comments by stuart.jamieson@secuura.ai 2026-09-10T06:14Z and 07:43Z via https://api.linear.app/graphql | read 2026-09-11
- 48c4d8053 is an ancestor of 0f8fb33c3 and 7bcb66128; control discriminates | https://api.github.com/repos/Secuura/Distributed_Secuura/compare/48c4d8053...0f8fb33c3 | read 2026-09-11
- the two orphan defects, line numbers, the control | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md section "FILE THESE FIRST" | read 2026-09-11
- s171 correctly did not file them under §2c | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md s171 entry | read 2026-09-11
- core.sshCommand names 3_Access_Keys/github_deploy_rw; that file present; ~/.ssh/secuura_blockchain_deploy_rw absent; ssh-agent has no identities | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/.git/config and a file-existence test, Wednesday's seat | read 2026-09-11
- ls-remote origin authenticated | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1041_951.sh --check output, Wednesday's seat | read 2026-09-11
