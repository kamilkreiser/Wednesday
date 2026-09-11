---
date: 2026-09-11
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 15:3x AEST by the seat booted 15:10 (after its 51% checkpoint). The 14:0x version is overtaken — s179 and its gate are closed, s180 is live.
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-11 15:3x (seat booted 15:10). **s180 LIVE in `%17` on KS-597 option B (Kam ruled 15:22).** Push-protocol tier-2 GO WITH FINDINGS processed, s179 scored 0.90, W-1 ruled, fix round owed. `chat_sync.sh` two-puller fix live. KAM: last word to Wednesday 15:22 (two card taps, both receipted).

> Narrative: `0_Brain/daily/2026-09-11.md` (15:16–15:3x entries). **Measure before acting on any line here.**

## 🔴 HOLD — SECUURA PREFLIGHT LEG 14 (unchanged)
Until #953 is on develop, no seat runs the pre-push hook or preflight leg 14, on any tree containing `ec2d8c4ca`, from any push whose hook receives `GIT_DIR` (a linked worktree, or `git --git-dir=… --work-tree=… push`). Pushes from the MAIN checkout do not export `GIT_DIR` (tier-2 gate H1–H5, measured in scratch). Every Secuura brief carries it.

## 🟢 FLOOR
| pane | seat | commission | next event Wednesday owes |
|---|---|---|---|
| `%17` | **s180** — launched 15:33 via `brief_and_launch.sh`; brief `fleet/briefs_staged/2026-09-11_s180_ks597-option-b.md` verified at destination 05:33:01Z | KS-597 option B: item 0 measure (resolution table, no code) → item 1 build on a new branch from develop `2d864ae92` in the MAIN checkout, tests red-first, Test Evidence, PR → item 2 DRAFT reply to Stuart (Kam's to send) → READY FOR QA | **rung-6 proof = its plan confirmation with the item-0 table → ANSWER it.** Check every row against the card's option B; if externalRef is not unique or register-connector does not resolve it, that goes back to Kam as a card |
| `%1` | monitor | — | — |

develop = `2d864ae9220c57ddcd8dc77af1b80fbd8001d530` (`ls-remote` 15:2x). Secuura main checkout on `kamilkreiser/ks-1041-gateway-provenance-middleware`, porcelain 0 (15:2x) — s180 will switch it to its new branch.

## 🔵 KS-597 CHAIN — Kam ruled `b-resolve-externalref` 15:22:48; card recorded 15:25:42; **NOT yet delivered** (mark `--delivered` naming the PR and the KS-597 comment once they exist)
s180 READY FOR QA → **tier-1 gate** (an auth door; Wednesday commissions — **the KS-978 cells are a PROSE-contract leg, NOT bite on the code: do not require them to redden on a code tamper** (ledger 16:2x); the real-DB cell (a) ran under `secuura_app` NOBYPASSRLS on the live local DB and a disposable DB `ks597b-s180-pg` port 6599, left running for the gate) → **Peter's approval at head** (project CLAUDE.md 234-237: the author merges, no approval no merge, squash) → deploy **kintsugi first, then demo** under Kam's week grant (`0_Brain/tasks/EXPIRING-GRANTS.md`: end of Sunday 2026-09-13 AEST, date assumed — ask before relying on it on the 12th or 13th) → KS-535 wallet hold on any kintsugi deploy. **Stuart:** s180's DRAFT goes to Kam; telling Stuart is his conversation. **The card's option B detail elided Peter's approval step** — said to Kam on the panel.

## 🟠 PUSH-PROTOCOL FIX ROUND OWED — round 2 of 2; not urgent (nothing uses the verifier until #953 merges)
Verdict: `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-push-protocol-d2a53096-tier2-r1/report.md`. **W-1 RULED by Wednesday 15:2x:** (1) a `push -u` config delta confined to `branch.<pushed>.remote/.merge` → CLEAN; (2) a refused push that altered nothing in the shared repository (G4s stale T, G4f absent T) → a distinct NOT-LANDED verdict with its own exit (not 0, not 3), no STOP-and-mail, printing origin's head; (3) an optional expected-sha: CLEAN requires origin == T == expected; (4) QA-1 — read origin first, re-read the locals after it and require equality, else DIFF "repository changed during verify"; QA-4 — usage to stderr, exit 1, indent the `PROTOCOL-` docstring lines; QA-5 — per-worktree refs and index sha; docstring corrected. **Regression arms:** G4s/G4f/G1u · Qa3/Qa3c non-CLEAN, Qa3h stays DIFF · Qa4 with expected-sha non-CLEAN · X1/X2 · every current CLEAN and DIFF arm. Then a tier-2 through-code gate. **Brief it with a LEGITIMATE-SHAPES table (shape · expected verdict · rule clause) — the ledger's w=3 promotion.** QA-6 side question: does #953's scrub cover `pre_push_hook_base.test.sh`'s `git push origin` lines — a seat can read #953's diff and answer it.

## 🔴 WITH KAM (already on his panel — do not re-list in every message)
1. **#953 needs Peter's review** (optional WhatsApp line given 13:24).
2. Drafts for Peter: `5_Project_History/2026-09-11_peter-reviews/DRAFT-reply-to-peter-933.md` · `…-952.md` · `5_Project_History/2026-09-10_peter-protocol/DRAFT-reply-to-peter-896.md`.
3. His vault skill `Notes (MASTER)/skills/Current/extranet.md` contradicts his 09-05 tickets-only rule (his file).
4. `raise-to-1` on the ruleset · the agent GitHub identity invite · deleting `feature/y` (`d709d01b2`) / `feature/w` (`41612bf0a`).
5. Tuesday's Mac mini Full Disk Access toggle — Tuesday's; she gave him the steps at 15:27 and her probe still read exit 126.

## 🟡 OWED BY WEDNESDAY (none started unless marked)
1. ~~QA brief template LEGITIMATE-SHAPES table~~ **DONE 15:4x — `BRIEF_TEMPLATE.md` §2a.** Still a rule in a template, not a gate: the launcher guard that refuses a checker brief without the table is the next rung if it recurs.
2. Send gate: refuse a Secuura brief containing `extranet` outside a HOLDS / "not a channel" context.
3. pretooluse hook: refuse `PIPESTATUS`; flag `grep -c`/`-q` on a multi-word phrase without `-i`; flag a bare `grep` with `$(` inside `$(…)`; flag a word beginning `=` after `echo`.
4. Inbox reads filter on SUBJECT routing tags, never on From.
5. `cockpit.sh`: `die` on the `--mail` routing path prints nothing; `add` should refuse a name with no routing entry. `pane_close.sh` usage says name-or-id but refuses a name.
6. `send_brief.sh` double-prefixes a subject that already carries a routing tag (QA verdicts).
7. `reconcile_rulings.py` in the watcher's checkpoint legs — shared `wake_watch.sh`, claim with Tuesday first.
8. Family-weight index (Kam's `measure-first` recommendation #1) — claimed 06:0x, not started.
9. 19 Secuura ruled-undelivered cards (`decision_queue.sh list ruled --undelivered secuura-`).
10. Kam's `vault-add-a-stages-another-clients-files` grant (ruled `grant-both` 09-08) — at a quiet floor.
11. panel_sync `Cannot rebase onto multiple branches` (08:20:09) — Tuesday's tooling, reported not patched.
- ~~`chat_sync.sh` two-puller fix~~ **DONE 15:23 (`7fd995f8`), red-proofed FAILS=0, live stand-down verified 15:23:49, claim released.**

## 🟠 NAS
Tonight's 03:30 leg is the first real run of the FIXED deletion counter (`a0d70ca8`) — read its per-root summary line; `UNKNOWN` means normalisation failed, not zero.

## ⚠ TRAPS
- **Write and commit in ONE command.** The launcher's regenerated boot digests block `panel_sync` until committed — commit them by name at boot.
- zsh: no `PIPESTATUS`; a list variable does not word-split; an unmatched glob aborts; **`echo ======` is `=`-expansion and aborts the whole command**; `VAR=x cmd1 | cmd2` gives VAR to cmd1 only.
- The Bash tool's `grep` is a shell-snapshot FUNCTION: `/usr/bin/grep` plus a same-file control whenever a zero enters a sentence.
- `ps` shows a `$(…)` subshell with its parent's argv — count loops by ppid 1 and start time, never by command line.
- The send gate's scope list (`send_brief.sh:351`): `reversible · board config · low-risk · blast radius · contained change · local change` — rephrase descriptive uses.
- `kam_rulings_today.sh`'s STALE-COPY warning fires on message AGE — check `tools/logs/panel_sync.log` for a recent `ok` first; never `--autostash` this tree.
- A ruled card's `delivered` mark is a record of what a seat wrote, never a fact about the world.
