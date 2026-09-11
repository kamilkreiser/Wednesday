---
date: 2026-09-11
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 17:55 AEST by the seat booted 17:14, at its 65% checkpoint.
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-11 17:55 (seat booted 17:14, checkpoint 65%). **s181 MERGE LANE LIVE in `%19`. #954 IS ON DEVELOP (Kam merged it). KAM 17:50: approval to merge ANYTHING finished and tested.**

> Narrative: `0_Brain/daily/2026-09-11.md` (17:18–17:55 entries). **Measure before acting on any line here.**

## 🔴 HOLD — SECUURA PREFLIGHT LEG 14 (unchanged)
Until #953 is on develop **and Wednesday has verified it and lifted the hold BY NAME** (mail to the seat + this file), no seat runs the pre-push hook or preflight leg 14, on any tree containing `ec2d8c4ca`, from any push whose hook receives `GIT_DIR` (a linked worktree, or `git --git-dir=… --work-tree=… push`). Main-checkout pushes do not export `GIT_DIR`.

## 🟢 FLOOR
| pane | seat | state | next event Wednesday owes |
|---|---|---|---|
| `%19` | **s181 Secuura/Blockchain — merge lane** | launched 17:50; brief `2_Project_Files/fleet/briefs_staged/2026-09-11_s181_merge-lane-953-954.md` verified 07:50:39Z; ADDENDUM `…/2026-09-11_s181_addendum_954-merged-by-kam.md` verified 07:53:56Z; rung 5 at 17:52 | **plan confirmation → ANSWER it** (rung 6). In the answer add: update the Stuart draft's Status line — #954 is MERGED (`2600229ef`, merge commit), NOT deployed. |
| `%1` | monitor | — | — |

develop = **`2600229efedae9682339064d8127ccf035b90afc`** (`ls-remote` 17:5x): Peter's #896 (07:38:25Z) → Peter's #899 (07:46:46Z) → Kam's #954 (07:49:56Z, merge commit; second parent = gated head `355d82c8b`; diff vs first parent = the PR's 9 files). #953 open at `8987b8a0e`, gate-clean (tier-2 GO WITH FINDINGS, KS-1089).

## 🔵 s181's round, and what Wednesday does at each event
1. **Item 0 mail** (project CLAUDE.md root copy lines 234/237 amended to Kam's words; quarantine copy + sha256s) → read the edited lines back yourself (read-only) before accepting.
1b. **Item 0 VERIFIED 18:2x** (root CLAUDE.md `:232-:241` + `:266` note, sha `a4cd7d58…`; Stuart draft line 11; KS-1085 comment `96f6350a`). **Owed in the next ANSWER:** s181 posts one correction on KS-925 (its 09-10 comment says step 7 no longer marks seen; `Launch_Claude.command:537` still does).
2. **#953 merged** → verify at source: `merged`, merge commit has ONE parent (squash), parent == develop tip before it, develop tip == it → **LIFT THE LEG-14 HOLD BY NAME** (mail s181 + this file + the Secuura brief standing lines) → KS-1086 comment + board move verified.
3. **#954 verify receipt** → KS-597 comment + Tested Not Deployed verified.
4. **Census mailed** (`!CODING/Secuura/Blockchain/5_Project_History/2026-09-11_merge-census/CENSUS-s181.md`) → sample each TESTED row at source (gate verdict at CURRENT head, Test Evidence, base, mergeable, no workflows) → **GO by PR number + head SHA, one at a time, citing Kam's 17:50 extension.** Other authors' PRs: they merge their own.

## 🔵 AFTER s181 — the KS-597 deploy seat
Kintsugi first (week deploy grant; demo = UAT waits for Peter's nod under the 16:56 flow). **KS-535: kintsugi never shares demo's `PLATFORM_WALLET_MNEMONIC`.** Compose project-name trap (`-p 2_project_files`). Rebuild from develop at the merge; re-run the live cells (own GUID 201 · upper-case 201 · own K id 201 · other org 403). The #954 gate's disposable artefacts (orgs A/B/C/E, `qa954-orig-r9`/`qa954-orig-dev`, `ks597b-s180-pg`) are still up — decide their teardown in that brief, never `rm` without a ruling.
**Stuart draft** `!CODING/Secuura/Blockchain/5_Project_History/2026-09-11_ks597/DRAFT-reply-to-stuart-ks597.md` (read whole 17:4x): to Kam once its Status line is true — merged now; deployed after kintsugi.

## 🟢 KAM'S GRANTS IN FORCE — `learnings/2026-09-11_secuura-we-approve-and-merge-our-own-tested-work.md`
16:56:00 / 16:56:44 / 16:58:04 (we approve and merge our own tested work; still run all our own tests) + **17:50:39 EXTENSION: "you also have my approval to merge anything that has been finished and tested."** Tested = QA gate at the CURRENT head + Test Evidence + our suites. Not covered: deploys to demo (Peter's nod), `.github/workflows` PRs (`kam-merges` card), other authors' PRs. `raise-to-1` stays unapplied.

## 🟠 PUSH-PROTOCOL FIX ROUND OWED — round 2 of 2; not urgent
Verdict `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-push-protocol-d2a53096-tier2-r1/report.md`. W-1 RULED (today's note 15:2x): `-u` config delta on `branch.<pushed>.remote/.merge` → CLEAN · refused push that altered nothing → NOT-LANDED with its own exit · optional expected-sha · QA-1 origin-first re-read · QA-4/QA-5 ride along. Brief it with template §2a's LEGITIMATE-SHAPES table.

## 🔴 WITH KAM (already on his panel — do not re-list in every message)
1. The Stuart reply — when its Status line is true.
2. Drafts for Peter (#933 / #952 / #896): #896 has now MERGED (Peter, 07:38Z) — that draft is likely moot; check before raising.
3. His vault skill `Notes (MASTER)/skills/Current/extranet.md` contradicts his 09-05 tickets-only rule.
4. The agent GitHub identity invite · deleting `feature/y` / `feature/w`.
5. Tuesday's Mac mini Full Disk Access toggle (Tuesday's).

## 🟡 OWED BY WEDNESDAY
1. Send gate: refuse a Secuura brief containing `extranet` outside a HOLDS / "not a channel" context.
2. pretooluse hook: refuse `PIPESTATUS`; flag `grep -c`/`-q` on a multi-word phrase without `-i`; flag a bare `grep` with `$(` inside `$(…)`; flag `echo =…`.
3. Inbox reads filter on SUBJECT routing tags, never on From.
4. `cockpit.sh`: `die` on the `--mail` routing path prints nothing. `pane_close.sh` usage says name-or-id but refuses a name.
5. `cockpit.sh add` should refuse a name with no routing entry — blocks parallel Secuura seats.
6. `send_brief.sh` double-prefixes a subject that already carries a routing tag (the QA verdict subjects).
7. `reconcile_rulings.py` in the watcher's checkpoint legs (shared `wake_watch.sh` — claim with Tuesday first).
8. Family-weight index (Kam's `measure-first` #1).
9. 18 Secuura ruled-undelivered cards (`decision_queue.sh list ruled --undelivered secuura-`).
10. Kam's `vault-add-a-stages-another-clients-files` grant, at a quiet floor.
11. panel_sync `Cannot rebase onto multiple branches` (Tuesday's tooling).
12. **Wrap rule 3b:** a learnings file was edited this seat (17:50 grant extension) — regenerate BOTH digests at wrap.
13. **Launcher commits the boot digests it regenerates** (shared with Tuesday's launcher — claim with her first).

## 🟠 NAS
Tonight's 03:30 leg is the first real run of the FIXED deletion counter (`a0d70ca8`). Read its per-root summary; `UNKNOWN` means normalisation failed, not zero.

## ⚠ TRAPS
- **Write and commit in ONE command.** **Commit the launcher's regenerated boot digests as the FIRST write of every boot** — at 17:14 they sat uncommitted 45 min and blocked `panel_sync` (ledger 18:03).
- **`panel_sync` does a plain `git pull --rebase`:** a local MERGE must be pushed in the same action, or the daemon re-linearises it into the same conflict. `scoreboard.md` is a TWO-WRITER file (both seats insert top rows).
- **zsh:** no `PIPESTATUS`; a list variable does not word-split; `echo ======` aborts; `VAR=x cmd1 | cmd2` hands VAR to cmd1 only; `sleep N; cmd` is blocked.
- **The Bash tool's `grep` is a shell-snapshot FUNCTION:** use `/usr/bin/grep` plus a same-file control.
- **Tool paths:** `brief_and_launch.sh`, `send_brief.sh` and `self_check_view.sh` live in `2_Project_Files/fleet/` (NOT `fleet/cockpit/`); `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh` live in `fleet/cockpit/`. `send_brief.sh` has no `--kind addendum` — corrections go as `--kind answer`.
- **The provenance gate reads a path-shaped token ANYWHERE in a provenance line** (`.github/workflows`, `pulls/files`) as a relative path — write "the GitHub workflows directory", "pull-files endpoint".
- **Kam's GitHub merge button defaulted to a merge commit** (07:49Z). For squash, the seat merges via the API.
- **The send gate's scope list** (`send_brief.sh:351`): `reversible · board config · low-risk · blast radius · contained change · local change`.
- **A mail to an agent can cross the agent's own mail.** Read the agent's next mail before re-sending anything.
- **A ruled card's `delivered` mark** is a record of what a seat wrote, never a fact about the world.
