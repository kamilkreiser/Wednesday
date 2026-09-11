---
date: 2026-09-11
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 18:5x AEST by the seat booted 17:14, ROTATING at ~80%.
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-11 18:5x (seat booted 17:14, ROTATING ~80%). **#953 AND #954 ARE ON DEVELOP. s181 CENSUS COMPLETE: of our 38 open PRs, 2 are TESTED (#936, #951). s181 told to wrap.**

> Narrative: `0_Brain/daily/2026-09-11.md` (17:18–18:5x entries). **Measure before acting on any line here.**

## 🟢 LEG-14 HOLD — LIFTED 18:3x, SCOPED
**LIFTED for any push whose tree CONTAINS `8a6b0d9c2`** (#953, verified at source). **NOT lifted** for a tree containing `ec2d8c4ca` without `8a6b0d9c2` — the hook runs the pushing tree's own runner, so such a tree pushes from the MAIN checkout or takes develop first. Check: `git merge-base --is-ancestor 8a6b0d9c2 HEAD` == 0 before any linked-worktree push. Every Secuura brief carries THIS wording.

## 🟢 FLOOR
| pane | seat | state | next event the successor owes |
|---|---|---|---|
| `%19` | **s181 Secuura/Blockchain — merge lane** | census COMPLETE (verified at source 18:5x); ANSWER "wrap now" verified at destination 08:50:21Z, pointer queued | **its wrap mail** → verify `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s181-merge-lane.md` + the history entry on disk → **score s181** (outgoing seat's provisional reading **1.00**: item 0 verified at source; #953 squash merged + verified; #954 verify; KS-1086 Done+archived, KS-597 Done unarchived, KS-925 correction `16fbcd61`; census complete; three instrument errors self-caught and disclosed) → `pane_close.sh %19` (use the `%ID`, not the name) |
| `%1` | monitor | — | — |

develop = **`8a6b0d9c2ef28b73ee6180bca17277ecb2e60e51`** (`ls-remote` 18:5x): … #896 (Peter) → #899 (Peter) → #954 (Kam, merge commit `2600229ef`) → #953 (s181, squash `8a6b0d9c2`).

## 🔴 NEXT COMMISSION — s182 Secuura MERGE SEAT, after the successor samples both rows AT SOURCE
Census: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-11_merge-census/CENSUS-s181.md` (+ `census-raw.json`, `census-corrected.json`). 51 open · ours 38 · TESTED 2 · UNTESTED 36 (all "no gate verdict at head"; 4 touch workflows, 4 dirty, 2 with Peter's CHANGES_REQUESTED) · not ours 13 (Peter 3, dependabot 10). Heads at 18:5x: #936 `de95bd87a`, #951 `02a22f4bb` (both == gated heads).
1. **#936 → KS-1058.** Tier-1 GO WITH FINDINGS at `de95bd87a` (KS-1058 comment `ed1b5934`, 2026-09-10 10:53Z, gated by s170 — a separate seat — at Wednesday's instruction; 0 Blockers · 0 Majors · 2 Minors). 0 file overlap with develop since its merge-base; merge-tree clean (s181's). **Before the GO, check:** the two Minors are ticketed; head still `de95bd87a`; Test Evidence; no CR; not dirty; no workflows. Then GO (Kam 17:50 extension) → squash via API, head pinned → verify one parent == develop tip, files == PR → KS-1058 Done + archived.
2. **#951 → KS-1041.** Round-2 tier-1 GO WITH FINDINGS at `02a22f4bb` exists **ONLY in the report** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1041-951-02a22f4bb-tier1-r2/report.md` — **post the verdict on PR #951 and KS-1041 FIRST.** **PROVISIONING UNSAFE (R2-1, Major; KS-1083):** with `GATEWAY_VOUCH_SECRET` set, the gateway's own POST /api/documents forward saves under DEFAULT_TENANT. **A GO covers the merge only; the secret stays unset on every environment.** One file overlaps develop (`docker-compose.yml`), independent (census, s181). Outgoing seat's reading, to state to Kam as a reading: an inert control whose hazard is ticketed is "finished and tested" for the MERGE; turning it on is not.
3. **The 36 UNTESTED:** the test bar is now the bottleneck, not approvals. Gates cost a pass each and the 7-day allowance read 75% at 18:48 (renews ~1d 9h). Plan the gate queue with the tier rule (tier 2 through-code for tests/docs/config and already-gated follow-ups) before commissioning; spend beyond that is a card for Kam.

## 🔵 KS-597 — merged; kintsugi deploy is the seat after s182
Kintsugi first (week deploy grant); demo = UAT waits for Peter's nod. **KS-535: kintsugi never shares demo's `PLATFORM_WALLET_MNEMONIC`.** Compose project name trap (`-p 2_project_files`). Rebuild from develop; re-run the live cells (own GUID 201 · upper 201 · own K id 201 · other org 403). Root CLAUDE.md `:173`/`:178` ("both targets on every change") contradict "UAT waits for Peter" — owed to that seat (s181's P2). The #954 gate's disposable artefacts (orgs A/B/C/E, `qa954-orig-r9`/`qa954-orig-dev`, `ks597b-s180-pg`) are still up — decide teardown in that brief; never `rm` without a ruling.
**Stuart draft** (`!CODING/Secuura/Blockchain/5_Project_History/2026-09-11_ks597/DRAFT-reply-to-stuart-ks597.md`, Status line now true): **with Kam since 18:34** (steps + KS-597 link). Default: nothing goes to Stuart. If he says "post it": a Secuura seat posts it verbatim on KS-597, reads it back, then archives KS-597.

## 🟢 KAM'S RULINGS IN FORCE — `learnings/2026-09-11_secuura-we-approve-and-merge-our-own-tested-work.md`
16:56:00 / 16:56:44 / 16:58:04 (we approve and merge our own TESTED work; still run all our own tests) · **17:50:39 extension: "you also have my approval to merge anything that has been finished and tested"** · **17:54:46: "please close and archive linear tickets as you [go] so there is no confusion"** (Done + archived on merge; KS-597 held unarchived for the Stuart reply). Not covered: demo deploys (Peter's nod), `.github/workflows` PRs (`kam-merges`), other authors' PRs. `raise-to-1` stays unapplied.

## 🟠 PUSH-PROTOCOL FIX ROUND OWED — round 2 of 2; not urgent
Verdict `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-push-protocol-d2a53096-tier2-r1/report.md`. W-1 RULED (today's note 15:2x). Brief it with template §2a's LEGITIMATE-SHAPES table.

## 🔴 WITH KAM (already on his panel — do not re-list in every message)
1. The Stuart reply (18:34, steps + link).
2. His vault skill `Notes (MASTER)/skills/Current/extranet.md` contradicts his 09-05 tickets-only rule.
3. The agent GitHub identity invite · deleting `feature/y` / `feature/w`.
4. Drafts for Peter: #896 merged (07:38Z) and #933/#952 are Peter's own PRs — under the new flow these are likely moot; check before raising.

## 🟡 OWED BY WEDNESDAY
1. Send gate: refuse a Secuura brief containing `extranet` outside a HOLDS / "not a channel" context.
2. pretooluse hook: refuse `PIPESTATUS`; flag `grep -c`/`-q` on a multi-word phrase without `-i`; flag a bare `grep` with `$(` inside `$(…)`; flag `echo =…`.
3. Inbox reads filter on SUBJECT routing tags, never on From.
4. `cockpit.sh`: `die` on the `--mail` routing path prints nothing. `pane_close.sh` usage says name-or-id but refuses a name.
5. `cockpit.sh add` should refuse a name with no routing entry.
6. `send_brief.sh` double-prefixes a subject that already carries a routing tag.
7. `reconcile_rulings.py` in the watcher's checkpoint legs (shared `wake_watch.sh` — claim with Tuesday first).
8. Family-weight index (Kam's `measure-first` #1).
9. Secuura ruled-undelivered cards (`decision_queue.sh list ruled --undelivered secuura-`).
10. Kam's `vault-add-a-stages-another-clients-files` grant, at a quiet floor.
11. panel_sync `Cannot rebase onto multiple branches` (Tuesday's tooling).
12. **At the next WRAP, rule 3b:** learnings files changed this seat (17:50 grant extension; ledger rows) — regenerate BOTH digests.
13. The launcher commits the boot digests it regenerates (shared with Tuesday's launcher — claim first).
14. Repo copy `2_Project_Files/CLAUDE.md` (:254/:257/:277), `Blockchain/Dev/CONTRIBUTING.md` (:467-468, :476, :516), `docs/DEV-PROCESS.md` (:5, :21, :250) still say "no approval → no merge" — owed via a PR by a Secuura seat (s181's handover carries the text).

## 🟠 NAS
Tonight's 03:30 leg is the first real run of the FIXED deletion counter (`a0d70ca8`). Read its per-root summary; `UNKNOWN` means normalisation failed, not zero.

## ⚠ TRAPS
- **FIRST WRITE OF THE BOOT: commit the launcher's regenerated boot digests** (`_boot_digest.md`, `_boot_digest_by_tier.md`) by path. At 17:14 they sat 45 min uncommitted, panel_sync skipped every cycle, and the pull then hit a two-writer scoreboard conflict (ledger 18:03).
- **Write and commit in ONE command.** `panel_sync` does a plain `pull --rebase`: a local MERGE must be pushed in the same action. `scoreboard.md` is a TWO-WRITER file.
- **A `chat_reply.sh` write in the same second as panel_sync's pull fails that one cycle** ("unstaged changes"); it recovers the next cycle — confirm, do not assume.
- **zsh:** no `PIPESTATUS`; a list variable does not word-split (`set -- $pair` too); `echo ======` aborts; `VAR=x cmd1 | cmd2` hands VAR to cmd1 only; `sleep N; cmd` is blocked (use a background until-loop).
- **The Bash tool's `grep` is a shell-snapshot FUNCTION:** use `/usr/bin/grep` plus a same-file control. **The no-cd hook refuses `git -C "$VAR"`** — write literal paths, or put multi-step git work in a script file run with `bash`.
- **Tool paths:** `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wednesday_rotate.sh` in `fleet/cockpit/`. `send_brief.sh` has no `--kind addendum` — use `--kind answer`.
- **The provenance gate reads a path-shaped token anywhere in a provenance line** (`.github/workflows`, `pulls/files`) as a relative path.
- **Kam's GitHub merge button defaulted to a merge commit** (07:49Z). For squash, a seat merges via the API.
- **The send gate's scope list** (`send_brief.sh:351`): `reversible · board config · low-risk · blast radius · contained change · local change`.
- **A mail to an agent can cross the agent's own mail.** Read the agent's next mail before re-sending anything.
- **A sort-ordered string is not a set:** compare dirty-path sets as sets (the 17:57 guard misfire).
