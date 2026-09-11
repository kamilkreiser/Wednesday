---
date: 2026-09-11
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 19:0x AEST by the seat booted 18:5x (boot ctx 58%).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-11 21:1x (seat booted 18:5x, ROTATING ~80%). **#936/#951 merged; #956 GO WITH FINDINGS; s183 LIVE closing out #956 (plan answered).**

> Narrative: `0_Brain/daily/2026-09-11.md` (18:53 block onward). **Measure before acting on any line here.**

## 🟢 LEG-14 HOLD — LIFTED 18:3x, SCOPED
**LIFTED for any push whose tree CONTAINS `8a6b0d9c2`.** NOT lifted for a tree containing `ec2d8c4ca` without `8a6b0d9c2` — such a tree pushes from the MAIN checkout or takes develop first. Check: `git merge-base --is-ancestor 8a6b0d9c2 HEAD` == 0 before any linked-worktree push. Every Secuura brief carries THIS wording.

## 🟢 FLOOR
| pane | seat | state | next event the successor owes |
|---|---|---|---|
| `%24` | **s184 Secuura/Blockchain — merge #957 + follow-up ticket + P3 root mirror + KS-1094 measure-first** | launched 22:41 via `brief_and_launch.sh`, brief verified at destination 12:39:22Z (#957 gate GO WITH FINDINGS, completion COMPLETE, s183 scored 0.95) | (1) plan confirmation = rung 6 → ANSWER · (2) STATUS mails → verify each at source (#957 squash: one parent == T, 3 files, blobs; KS-1095 Done + `archivedAt`; the follow-up ticket Low, board account; root copy re-diff) · (3) **its gauge is Wednesday's: mail CHECKPOINT at 50%, HAND OVER NOW at 70%** (the watcher's pane legs fire at 50/65/70) · (4) KS-1094: tracked → STOP is Kam's card; untracked → High + fix PR → tier-2 gate · (5) wrap → score after the last gate verdict → `pane_close.sh %24` |
| `%1` | monitor | — | — |

Brief: `2_Project_Files/fleet/briefs_staged/2026-09-11_s182_merge-936-951-docs-pr.md`. develop at 18:5x = `8a6b0d9c2` → **19:40 = `b75cff4d6`** (#936 squash `27509dc7a` · #951 squash `b75cff4d6`, both VERIFIED AT SOURCE by Wednesday; KS-1058 + KS-1041 Done + archived; residuals on KS-1032 / KS-1091; KS-1090 filed; KS-741 hold met, not started). **s182 now on item 2 (docs PR) → READY FOR QA → tier-2 gate. Owed in its next ANSWER: assign KS-1032 to the board account; set KS-1091's priority.**
**GO heads:** #936 `de95bd87ad79fde0215beeadf1f3ae5f945b4ea3` (KS-1058) · #951 `02a22f4bbc46a66983c3752a5a12394ff5b1afaf` (KS-1041). #951's round-2 verdict is on NEITHER the PR nor KS-1041 (measured 19:0x) — s182 posts it BEFORE merging. **#951 GO covers the merge only; `GATEWAY_VOUCH_SECRET` stays unset everywhere (KS-1083).**
**Kam told on the panel 19:0x** (stored 622 chars): s182 merging both; #951 ships switched off; default = merge unless he says "hold 951". **If he says it: ADDENDUM to s182 superseding item 1 by name, before its #951 merge.**

## 🟢 #956 GATE DONE — GO WITH FINDINGS @ `5ffe2f95e` (verdict 10:37:18Z)
Report `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1092-956-5ffe2f95e-tier2-r1/report.md`. Completion COMPLETE against the 8 asks. **RULED 20:5x:** #956 GO · ONE follow-up ticket · QA-1 gate fix-shape · **QA-2 ANNOTATE not strike** (Kam's `raise-to-1` card is his, unapplied) · QA-3 one TESTED gloss + "Wednesday's GO names the head" · **QA-4 author = the authoring SEAT** · QA-5 UAT-nod clause on the 3 deploy lines · CLAUDE.md :223-:228 vs :278 recorded, not reconciled · W-1 root :243 fix by a seat. develop was `051a737a2` at the verdict (#900 merged 10:15Z, no overlap) and is **`9b222d37c` since 10:59:02Z** (#933, Peter's merge commit, +2 −1 in #956's CONTRIBUTING, no merge-rule text — read by Wednesday 21:3x). s182 score REVISED 0.95 (scored before this verdict — ledger row). **OWED: a QA charter line — no memory maintenance inside a gate session** (the #956 gate compacted its own memory index unbriefed).

## 🔵 AFTER s183 — the kintsugi deploy seat
Kintsugi first (week deploy grant, through Sunday 13 Sep); demo = UAT waits for Peter's nod. **KS-535: kintsugi never shares demo's `PLATFORM_WALLET_MNEMONIC`.** Compose project name trap (`-p 2_project_files`). Rebuild from develop; re-run KS-597's live cells (own GUID 201 · upper 201 · own K id 201 · other org 403). Root CLAUDE.md `:173`/`:178` ("both targets on every change") vs "UAT waits for Peter" — owed to that seat. The #954 gate's disposable artefacts (orgs A/B/C/E, `qa954-orig-r9`/`qa954-orig-dev`, `ks597b-s180-pg`) still up — decide teardown in that brief; never `rm` without a ruling. **Do not set the vouch secret.** Phase 0 re-tag before building (no rollback on either box).

## 🟠 QUEUED FOR THE NEXT SECUURA SEAT (added 22:07)
- ✅ **#957 gate GO WITH FINDINGS (12:31:17Z) → #957 merge + KS-1095 close + P3 root mirror + KS-1094 measure-first are s184's (`%24`).** Worktree `worktrees/s183-ks1095` is that round's; `worktrees/s182-ks1092` also kept.
- **KS-1094** (unassigned → ours, Kam 09-06; no priority yet — Wednesday triages when briefing): k6 runner prints persona passwords in clear to console + `reports/performance-reports/<run>/…-run.log`. **Measure FIRST whether those paths are tracked** (`git check-ignore -v`, `git log --all --oneline -- <path>`); tracked = secrets-in-history → STOP for Kam (irreversible class). Fix shape is the seat's: redact the logged command line. s183 handover FINAL names it.

## 🟠 THE 36 UNTESTED (census `!CODING/Secuura/Blockchain/5_Project_History/2026-09-11_merge-census/CENSUS-s181.md`)
The test bar is the bottleneck, not approvals. 7-day allowance read 75% at 19:0x (renews ~1d 8h). Plan the gate queue with the tier rule (tier 2 through-code for tests/docs/config and already-gated follow-ups) BEFORE commissioning; spend beyond that is a card for Kam. 4 touch workflows (`kam-merges`), 4 dirty, 2 with Peter's CHANGES_REQUESTED.

## 🟢 KAM'S RULINGS IN FORCE — `learnings/2026-09-11_secuura-we-approve-and-merge-our-own-tested-work.md`
16:56:00 / 16:56:44 / 16:58:04 (we approve and merge our own TESTED work; still run all our own tests) · **17:50:39 "you also have my approval to merge anything that has been finished and tested"** · **17:54:46 "please close and archive linear tickets as you [go]"** (Done + archived on merge; KS-597 held unarchived for the Stuart reply). Not covered: demo deploys (Peter's nod), `.github/workflows` PRs (`kam-merges`), other authors' PRs. `raise-to-1` stays unapplied.

## 🟠 PUSH-PROTOCOL FIX ROUND OWED — round 2 of 2; not urgent
Verdict `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-push-protocol-d2a53096-tier2-r1/report.md`. W-1 RULED (today's note 15:2x). Brief it with template §2a's LEGITIMATE-SHAPES table. Until then: push without `-u`; any DIFF → STOP and mail.

## 🔴 WITH KAM (already on his panel — do not re-list in every message)
1. The Stuart reply for KS-597 (18:34, steps + link). KS-597 is archived only after it is posted.
2. His vault skill `Notes (MASTER)/skills/Current/extranet.md` contradicts his 09-05 tickets-only rule.
3. The agent GitHub identity invite · deleting `feature/y` / `feature/w`.
4. Drafts for Peter on #933/#952 — **#933 MERGED by Peter 10:59:02Z (measured 21:3x), so its draft is moot;** #952 still to check before raising.

## 🟡 OWED BY WEDNESDAY
1. Send gate: refuse a Secuura brief containing `extranet` outside a HOLDS / "not a channel" context.
2. pretooluse hook: refuse `PIPESTATUS`; flag `grep -c`/`-q` on a multi-word phrase without `-i`; flag a bare `grep` with `$(` inside `$(…)`; flag `echo =…`; **flag any pipe out of `inbox_digest.sh` (w=2, 18:5x).**
3. Inbox reads filter on SUBJECT routing tags, never on From. `inbox_digest.sh` should refuse to ack what it did not print.
4. `cockpit.sh`: `die` on the `--mail` routing path prints nothing. `pane_close.sh` usage says name-or-id but refuses a name.
5. `cockpit.sh add` should refuse a name with no routing entry.
6. `send_brief.sh` double-prefixes a subject that already carries a routing tag.
7. `reconcile_rulings.py` in the watcher's checkpoint legs (shared `wake_watch.sh` — claim with Tuesday first).
8. Family-weight index (Kam's `measure-first` #1).
9. Secuura ruled-undelivered cards: 18 (`decision_queue.sh list ruled --undelivered secuura-`).
10. Kam's `vault-add-a-stages-another-clients-files` grant, at a quiet floor.
11. panel_sync `Cannot rebase onto multiple branches` (Tuesday's tooling).
12. **At the next WRAP, rule 3b:** learnings files changed today (17:50 grant extension; ledger rows) — regenerate BOTH digests.
13. The launcher commits the boot digests it regenerates (shared with Tuesday's launcher — claim first).
14. Boot cost: today's note read WHOLE took this seat to 58% (17:14 seat: 46% without it). A successor reads today's note from the newest handover block down unless it has room.

## 🟠 NAS
Tonight's 03:30 leg is the first real run of the FIXED deletion counter (`a0d70ca8`). Read its per-root summary; `UNKNOWN` means normalisation failed, not zero.

## ⚠ TRAPS
- **FIRST WRITE OF THE BOOT: commit the launcher's regenerated boot digests** by path.
- **Never pipe `inbox_digest.sh`** — it is newest-first and acks what it prints; redirect to a scratch file and Read it, or read the API directly.
- **Write and commit in ONE command.** `panel_sync` does a plain `pull --rebase`; `scoreboard.md` is a TWO-WRITER file.
- **zsh:** no `PIPESTATUS`; a list variable does not word-split; `echo ======` aborts; `VAR=x cmd1 | cmd2` hands VAR to cmd1 only.
- **The Bash tool's `grep` is a shell-snapshot FUNCTION:** use `/usr/bin/grep` plus a same-file control. **The no-cd hook refuses `cd` and `git -C "$VAR"`** — write literal paths.
- **Tool paths:** `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wednesday_rotate.sh` in `fleet/cockpit/`. `send_brief.sh` has no `--kind addendum` — use `--kind answer`.
- **The provenance gate reads a path-shaped token anywhere in a provenance line** (`.github/workflows`, `pulls/files`, `docker-compose.yml`) as a relative path.
- **Kam's GitHub merge button defaulted to a merge commit** (07:49Z). For squash, a seat merges via the API.
- **The send gate's scope list** (`send_brief.sh:351`): `reversible · board config · low-risk · blast radius · contained change · local change`.
- **A mail to an agent can cross the agent's own mail.** Read the agent's next mail before re-sending anything.
