---
date: 2026-09-11
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at the 65% checkpoint (14:0x AEST) by the seat booted 13:26. The 13:2x version is overtaken: s179 is live.
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-11 14:0x (seat booted 13:26, 65% checkpoint, NOT rotating — band 80-90). **s179 WRAPPED (pane closed). TIER-2 GATE on `push_protocol.py` @ `d2a53096` LIVE in `%16`.** #953 gate-clean at `8987b8a0e`, 0 reviews, waits on Peter. KAM: last word to Wednesday 08:06.

> Narrative: `0_Brain/daily/2026-09-11.md` (13:3x–14:0x entries). **Measure before acting on any line here.**

## 🔴 HOLD — SECUURA PREFLIGHT LEG 14 (unchanged; reworded 11:50 on the #953 tier-1 gate's QA-4)
Until #953 is on develop, no seat runs the pre-push hook or preflight leg 14, on any tree containing `ec2d8c4ca`, from any push whose hook receives `GIT_DIR` (a linked worktree, or any `git --git-dir=… --work-tree=… push`). Property protected: the shared `.git` config, refs and HEADs. Every Secuura brief carries it in HOLDS.

## 🟢 FLOOR
| pane | seat | commission | next event Wednesday owes |
|---|---|---|---|
| ~~`%15`~~ | **s179 WRAPPED 04:33:28Z** — handover `HANDOVER-s179-tier2-predicate.md` sha256 `a9ae6cd8…` verified on disk; history entry on top; pane closed via `pane_close.sh %15`, listeners 24 → 24 | item 0 delivered + verified (KS-1089 · KS-1086 `efb52344` · #953 `5629351067`); item 1 READY FOR REVIEW ruled COMPLETE | **score owed at the `%16` gate verdict** |
| `%1` | monitor | — | — |

**develop = `2d864ae9220c57ddcd8dc77af1b80fbd8001d530`** (unmoved since the 12 squash merges this morning; `ls-remote` 13:3x).

**After #953 merges** (Peter approves at head; author squash-merges): HOLD lifts → #879 (approved at `79f1fcb48`) and #813 (Peter's approval WITHDRAWN) per `!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s176-merge-lane-2.md` Item 2, under the FIXED protocol, reviews read at head before each push.
**Deferred on purpose:** the #899/#900 review seat — launch only when #896 has merged AND #933's B-1 is fixed (`HANDOVER-s175.md`).

## 🔵 GATE LAUNCHED 14:39 — `push_protocol.py` @ `d2a53096` (tier 2 through-code, round 1), pane `%16` `QA/Secuura-push-protocol`
- **Brief** `2_Project_Files/fleet/qa-agent/briefs/2026-09-11_secuura-push-protocol-d2a53096-tier2.md` · **prompt** `…tier2.prompt.txt` · **launcher** `2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_push_protocol_d2a53096.sh` (`--check` rc 0; red-proof 12 cells FAILS=0: green · NEVER 11 · MAIL 12 · ROUND 15 · TIER 7 · handover 17 · no-write 13 · directive 8 · sha 6 · override-launch 16 · green). Report dir `Testing Agent MAIN/projects/secuura/reports/2026-09-11-push-protocol-d2a53096-tier2-r1/`.
- **Verdict arrives FROM Wednesday's send path — route on `[QA -> Wednesday] TIER 2 GATE push_protocol.py d2a53096 ROUND 1`.** Then: verify the subject sha unchanged → completion check → score s179 → `pane_close.sh %16`. A NO GO → fix round from s179's handover, under the two-round cap.
- (Original asks, kept for the record:)
- **Why tier 2:** tooling, not product. It guards Secuura's SHARED `.git`, its old failure path was a destructive restore, and every arm and aim so far is the author's. **Not urgent:** those pushes wait on Peter's #953 review; pipelining is the point.
- **Asks:** (1) re-run `push-protocol/redproof/redproof_driver.py` AND write at least two arms of the gate's OWN design — a fetch by another process between snapshot and verify (must not read CLEAN), and a tag or multi-ref push; (2) the REAL `.githooks/pre-push` on a no-op push with empty stdin, in a scratch clone (s179 saw a SCRATCH hook fire on that shape); (3) trace the sub-scripts `.githooks/pre-push` and `preflight.sh` call for any fetch / ls-remote / pull that moves another ref (s179 read the top level only); (4) show that no legitimate shape (first push · fast-forward · no-op · refused) can read DIFF, and that no output says restore.
- **Template:** `2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1086_953_round2.sh` + its brief (guards: NEVER-line, MAIL line, ROUND, TIER). **The prompt must forbid a push, the real hook or preflight inside the Secuura checkout.** Read s179's handover (its gate asks + NOT TESTED) before writing the brief.

## 🟠 SYNC INCIDENT 15:06 — RESOLVED, one question open with Tuesday
- `panel_sync` sat in a stopped rebase 14:40:48 → 15:03:54 (no PULL FAILED / RECOVER line for that rebase); repaired with `rebase --quit` + `branch -f main` + `switch main`; the 15:03:54 cycle recovered normally. Nothing lost (ledger row 15:05).
- **ROOT CAUSE FOUND 15:09 (Tuesday's discriminators ruled out autostash and a loop restart):** the puller was **`com.wednesday.chatsync` → `2_Project_Files/tools/chat_sync.sh:41`** (`pull --rebase`, no autostash, every 60 s). Its own log `2_Project_Files/fleet/state/chat_sync.log` at 14:40:48: `SKIP: pull rc=1 … Rebasing (1/3)…(3/3)` — it left the conflicted rebase and never aborted. **Two pullers in one tree.**
- 🔴 **OWED, Wednesday's file (claimed with Tuesday by mail 15:09):** `chat_sync.sh` must `git rebase --abort` when its pull fails mid-rebase, or not pull at all while the `panel_sync.sh loop` process is live. Red-proof it on a scratch two-clone repo with an induced derived-file conflict (the 09-10 panel_sync harness shape): a failed pull must leave NO `.git/rebase-merge`. **Until then the stuck rebase can recur on any concurrent derived conflict.**
- **If `SKIP rebase/merge in progress` repeats in `tools/logs/panel_sync.log`:** copy the non-derived stores out first, check `git ls-files -u` and `.git/rebase-merge/` (stopped-sha, done, todo), and if every conflict is derived data, `rebase --quit` + `branch -f main HEAD` + `switch main`. **Never commit while a rebase is stopped.**

## 🔴 WITH KAM (all already on his panel — do not re-list in every message)
1. **`secuura-ks597-bind-compares-two-id-spaces-now-deployed`** (card, rec B) — ALL DEPLOYS HELD; Stuart's two 09-10 comments unanswered; Stuart not told (Kam's conversation).
2. **#953 needs Peter's review** — optional WhatsApp line given on the panel 13:24.
3. Drafts for Peter: `5_Project_History/2026-09-11_peter-reviews/DRAFT-reply-to-peter-933.md` (one blocker) · `…-952.md` (no blockers; merge after #896) · `5_Project_History/2026-09-10_peter-protocol/DRAFT-reply-to-peter-896.md`.
4. His vault skill `Notes (MASTER)/skills/Current/extranet.md` contradicts his 09-05 tickets-only rule (his file).
5. `raise-to-1` on the ruleset · the agent GitHub identity invite · deleting `feature/y` (`d709d01b2`) / `feature/w` (`41612bf0a`).

## 🟡 OWED BY WEDNESDAY (none started this seat unless marked)
1. Send gate: refuse a Secuura brief containing `extranet` outside a HOLDS / "not a channel" context.
2. pretooluse hook: refuse `PIPESTATUS`; flag `grep -c`/`-q` on a multi-word phrase without `-i`; flag a bare `grep` pattern with `$(` inside `$(…)`.
3. Inbox reads filter on SUBJECT routing tags, never on From.
4. `cockpit.sh`: `die` on the `--mail` routing path prints nothing; `add` should refuse a name with no routing entry. `pane_close.sh` usage says name-or-id but refuses a name.
5. `send_brief.sh` double-prefixes a subject that already carries a routing tag (QA agent verdicts).
6. **NEW 13:3x:** `reconcile_rulings.py` at every checkpoint (lesson `2026-09-11_a-boot-time-reconciler-cannot-catch-a-mid-session-tap`) — done by hand this seat at 13:26 and 14:00; the mechanism (watcher checkpoint legs) is in shared `wake_watch.sh` → claim with Tuesday first.
7. Family-weight index (Kam's `measure-first` recommendation #1) — claimed 06:0x, not started.
8. 18 Secuura ruled-undelivered cards (`decision_queue.sh list ruled --undelivered secuura-`).
9. Kam's `vault-add-a-stages-another-clients-files` grant (ruled `grant-both` 09-08) still unexecuted — at a quiet floor.
10. panel_sync `Cannot rebase onto multiple branches` (08:20:09) — Tuesday's tooling, reported not patched.

## 🟠 NAS
Tonight's 03:30 leg is the first real run of the FIXED deletion counter (`a0d70ca8`) — read its per-root summary line; `UNKNOWN` means normalisation failed, not zero.

## ⚠ TRAPS
- **Three Write calls then a later commit = uncommitted non-derived files = panel_sync skips = the 14:40 stuck rebase.** Write and commit in ONE command (python + `git add` + `git commit` in the same Bash call).
- zsh: no `PIPESTATUS`; no word-split of a variable holding a list or a command; an unmatched glob aborts the command. Capture output to a file, read `$?` on its own line.
- The Bash tool's `grep` is a shell-snapshot FUNCTION: a `$(` pattern inside `$(…)` read 0. Use `/usr/bin/grep` + a same-file control when a zero enters a sentence.
- `git rev-parse` takes ONE ref per call in this form ("Needed a single revision").
- Commit every non-derived write in the same command; while `panel_sync` is live, commit and let it push.
- `kam_rulings_today.sh`'s STALE-COPY warning fires on message AGE — check `tools/logs/panel_sync.log` for a recent `ok` before pulling; never `--autostash` this tree.
- A ruled card's `delivered` mark is a record of what a seat wrote, never a fact about the world.
