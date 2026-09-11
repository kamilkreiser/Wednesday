---
date: 2026-09-12
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — read her mail by SUBJECT only, never brief or answer for a Datasec project.
source: replaced WHOLESALE at 04:42 AEST by the seat booted 2026-09-11 21:17 (boot ctx 41%; this pickup written at ctx 76%).
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-12 04:42. **#956, #957 merged; #958 (KS-1094 credential mask) GO WITH FINDINGS; s186 LIVE to merge it onto the tested tree only.**

> Narrative: `0_Brain/daily/2026-09-12.md` (overnight), then `0_Brain/daily/2026-09-11.md` from the 21:17 boot block. **Measure before acting on any line here.**

## 🟢 FLOOR
| pane | seat | state | next event the successor owes |
|---|---|---|---|
| — | **No Secuura seat live** (s186 wrapped 19:17:34Z, verified, `%27` closed after `end_turn`; scored 1.00) | — | **Commission the kintsugi deploy seat for develop `4554b25e2`** (QUEUE item 1) · rule on `worktrees/s184-ks1094` teardown (quarantine, never delete) |
| `%1` | monitor | — | — |

**develop = `8515d1db7`** (Peter merged his own #952 at 14:07:17Z). Merged tonight by our seats, all verified at source: #956 → `cc7927ffc` · #957 → `8394cee6a`. **#958 head `ffb28575223dbd611a91242e3cd711aaeb3085b7`**, merge-base `8394cee6a`, gate report `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-12-ks1094-958-ffb285752-tier2-r1/report.md`.
**Scored tonight:** s183 0.95 · s184 0.90 · s185 0.95 (scoreboard rows).

## 🟢 KAM'S RULINGS AND GRANTS IN FORCE (check expiry by `date`, not by memory)
- **We approve and merge our own TESTED Secuura work** (Kam 2026-09-11 16:56 / 16:58 / **17:50:39 "merge anything that has been finished and tested"** / 17:54:46 close and archive tickets as we go) — `learnings/2026-09-11_secuura-we-approve-and-merge-our-own-tested-work.md`. TESTED = QA gate verdict at the CURRENT head + Test Evidence + our suites; Wednesday's GO names the head. Not covered: demo (UAT) deploys (Peter's nod), `.github/workflows` PRs (`kam-merges`), other authors' PRs. `raise-to-1` stays unapplied.
- **Deploy freely to kintsugi AND demo until end of Sunday 13 Sep** (email 2026-09-10 15:24) — kintsugi first; demo waits for Peter's nod under the 09-11 flow. **Merge + production grants of 09-07 also expire end of Sunday 13 Sep** (EXPIRING-GRANTS).
- **Overnight is working time** (08-28) — agents continue while their queue is live.

## 🔵 QUEUE AFTER s186 (in order)
1. **The kintsugi deploy seat** — rebuild from develop; KS-535: kintsugi NEVER shares demo's `PLATFORM_WALLET_MNEMONIC`; no `GATEWAY_VOUCH_SECRET` (KS-1083); migration 048 first; Phase 0 re-tag before building (no rollback on either box); compose project name trap (`-p 2_project_files`); root `CLAUDE.md` :173/:178 ("both targets on every change") vs "demo waits for Peter's nod"; re-run KS-597's live cells; the #954 gate's disposable artefacts (orgs A/B/C/E, `qa954-orig-r9` / `qa954-orig-dev`, `ks597b-s180-pg`) — decide teardown in that brief, never `rm` without a ruling. **Deadline: the deploy grant ends Sun 13 Sep.**
2. **KS-1098 (mask spellings + name set for Peter + PASSWD cell) and KS-1099 (YAML error prints secrets-file lines) fix rounds** → tier-2 gates. **Also owed to the next Secuura seat: the merge script's TREF gate reads an ABSENT path as its own argv echo under `2>/dev/null` (s186's finding) — fix to `cat-file -e` with an explicit ABSENT verdict.** **KS-1097** (Low; QA-957-1..5 + W-2 doc polish) after.
3. **THE 36 UNTESTED PRs** (census `!CODING/Secuura/Blockchain/5_Project_History/2026-09-11_merge-census/CENSUS-s181.md`, now older than several merges — re-census first). The test bar is the bottleneck: **7-day allowance read 80% at 04:38, renews ~23h**. Plan the gate queue by tier before commissioning; spend beyond the allowance is a card for Kam.

## 🔴 WITH KAM (already on his panel — do not re-list in every message)
1. The Stuart reply for KS-597 (steps + link). KS-597 is archived only after it is posted.
2. His vault skill `Notes (MASTER)/skills/Current/extranet.md` contradicts his 09-05 tickets-only rule.
3. The agent GitHub identity invite · deleting `feature/y` / `feature/w`.
4. Drafts for Peter: #933 and #952 both MERGED by Peter — moot; confirm before raising anything.
6. **Measure first, then raise if still true (from s186's sweep):** KS-775's title names a decision window that lapsed 2026-09-10 ("before the qs fuse lapses") · the vault's `daily/2026-09-11.md` holds 605 uncommitted lines from Secuura seats s172-s185 (the vault is read-only to Wednesday).
5. **For the morning report (no action from him):** develop's CI security-gate step red since Peter's #900 (recorded on KS-1075, cause not established) — already told on the panel 23:22.

## 🟡 OWED BY WEDNESDAY
1. **`wake_watch.sh` fix (SHARED with Tuesday — claim first):** QA-tag subjects (`[QA -> Wednesday]`) count as inbound for the mail leg; the runner never arms `stable_n=9999` while any cockpit pane is live. Measured 2026-09-12: a GO verdict sat unread 01:00 → 04:32 (ledger row).
2. **QA charter line** into `fleet/qa-agent/QA_AGENT_CHARTER.md` (shared with Tuesday — claim first): no memory maintenance inside a gate session (applied per-invocation in the #957/#958 prompts + launcher guard exit 14).
3. **The QA agent's own memory notes** (asked in the #957 and #958 CLOSINGs; do them in a NON-gate QA session): fence-skipping paragraph joiners; strip blockquote prefixes before calling a quote absent; a local clone copies branches only; never anchor `$` on a two-column ref listing; the performance `tsconfig.json` lists neither runner nor tests (use `tsconfig.node.json`); `git grep --no-index` refuses paths outside the repo.
4. Send gate: refuse a Secuura brief containing `extranet` outside a HOLDS / "not a channel" context.
5. pretooluse hook: refuse `PIPESTATUS`; flag `grep -c`/`-q` on a multi-word phrase without `-i`; flag a bare `grep` with `$(` inside `$(…)`; flag `echo =…`; flag any pipe out of `inbox_digest.sh`; flag `2>/dev/null` on a composed script path.
6. `inbox_digest.sh` should refuse to ack what it did not print. `send_brief.sh` double-prefixes a subject already carrying a routing tag. `cockpit.sh add` should refuse a name with no routing entry; `add` prints success on a skip.
7. `reconcile_rulings.py` in the watcher's checkpoint legs (shared `wake_watch.sh` — with item 1).
8. The launcher commits the boot digests it regenerates (shared with Tuesday's launcher — claim first).
9. Secuura ruled-undelivered cards: 18 (`decision_queue.sh list ruled --undelivered secuura-`).
10. Kam's `vault-add-a-stages-another-clients-files` grant, at a quiet floor. Family-weight index (Kam's `measure-first` #1).
11. **At the next WRAP, rule 3b:** `learnings/` files changed on 2026-09-11 and 2026-09-12 (ledger rows) — regenerate BOTH digests.

## 🟠 NAS
The 03:30 leg on 2026-09-12 was the first real run of the FIXED deletion counter (`a0d70ca8`). Read its per-root summary (`nas_sync_last_wednesday.txt`); `UNKNOWN` means normalisation failed, not zero.

## ⚠ TRAPS
- **FIRST WRITE OF THE BOOT: commit the launcher's regenerated boot digests** by path.
- **A QA verdict never wakes the mail leg** (it arrives From `wednesday-agent@`; `wake_watch.sh` :103-:116), and **a QA pane launched after a `stable_n=9999 agents=0` arm is not idle-watched until the 4h backstop.** After launching a gate with no builder live, arm a session-side wait on the verdict subject.
- **Peter merges his own PRs at night.** Every Secuura merge brief STOPs on a moved develop unless the brief rules the exact base/tree (the s186 shape: T == tested base AND predicted tree == the gate's tree).
- **Builder seats cannot see their own gauge and climb fast** (s184: 51 → 66% in ten minutes). Read their statusline at every wake; mail CHECKPOINT 50%, HAND OVER NOW 70%.
- **Before a pane close, read the transcript's last assistant row for `end_turn`** (`~/.claude/projects/<project>/<session>.jsonl`), not a spinner word.
- **The 23:00 close ritual appends to the daily note** and stalls `panel_sync` until committed.
- **Never pipe `inbox_digest.sh`** — read the API directly into a scratch file.
- **Write and commit in ONE command.** `scoreboard.md` is a TWO-WRITER file.
- **zsh:** no `PIPESTATUS`; a list variable does not word-split; `echo ======` aborts; a `grep -F` pattern splits on inner single quotes; `VAR=x cmd1 | cmd2` hands VAR to cmd1 only.
- **The Bash tool's `grep` is a shell-snapshot FUNCTION:** `/usr/bin/grep` plus a same-file control. **The no-cd hook refuses `cd` and `git -C "$VAR"`** — write literal paths.
- **The send gate's SELF-CHECK line must be exactly** `SELF-CHECK: re-read end-to-end for contradictions | YYYY-MM-DD HH:MM`.
- **The provenance gate reads a path-shaped token anywhere in a provenance line as a relative path** — absolute paths only there. Scope-gate words: `reversible · board config · low-risk · blast radius · contained change · local change`.
- **Linear relations read [] once a related issue is archived** — a known blindness, not an absence.
- **A PR-body discriminator can miss content** (a tree id absent while the run is present) — re-check with a second token.
- **Tool paths:** `brief_and_launch.sh`, `send_brief.sh`, `self_check_view.sh` in `2_Project_Files/fleet/`; `cockpit.sh`, `pane_close.sh`, `pane_prompt_check.sh`, `wednesday_rotate.sh`, `wake_watch.sh` in `fleet/cockpit/`; QA launchers in `fleet/qa-agent/launchers/` (latest template: `launch_qa_secuura_ks1094_958.sh`, red-proof 13 cells). `send_brief.sh` has no `--kind addendum` — use `--kind answer`.
