# Weekly consolidation — 2026-08-30 (Sunday 06:00 slot)

Covers 2026-08-24 → 2026-08-29 (last audit: 2026-08-23). Run in the morning session on a
quiet floor (no agent panes; Peter and Stuart silent since the #762 approval). Every change
is an incremental delta (anti-collapse rule); nothing regenerated wholesale. Inputs: the
whole ledger (219 rows), all six daily notes (08-24→08-28 via a read-only digest agent;
08-29 read in full), the 08-23 audit, every handover's "owed" list.

## Changes made (diffs, not rewrites)

1. **Representations lesson (`2026-08-14_…`) — new section "The brief-composition
   costumes" (w=37–46, ten instances in three days):** four costumes of one act named
   (card summary as code fact · counterpart's claim adopted · instrument label as event ·
   REC on an unmeasured premise) and the standing rule promoted: every claim entering a
   brief/ANSWER/card/report is copied from a read taken in the same action, or attributed
   and conditional. Enforcement state stated honestly per costume.

2. **ENFORCEMENT BUILT — `fleet/board_watch_peter.sh` rewritten (w=44):** every board bump
   is now read from Linear's HISTORY API and printed as what it is — `STATE a -> b by
   <actor>` · `RELATION ar->KS-n by <actor>` (backlinks) · `PETER COMMENT` / `COMMENT by` ·
   `OTHER` · `UNEXPLAINED BUMP`. Exercised before arming: positive control on the 08-29
   10:00Z window reproduced s90's state walk, three comments and five backlinks with actors;
   quiet control (boot −10 min) silent. Old copy kept as `.pre-0830` (never delete).
   Monitor re-armed on the new script (task beitpzoff). Validation pending a real Peter event.

3. **ENFORCEMENT BUILT — `tools/note_entry.sh` + `tools/prompt_log.sh` (w=46, the sixth
   composed timestamp; the 08-23 "generate, never type" rule had no writer for prose):**
   daily-note bullets/blocks and prompt-log entries now get a GENERATED stamp. Refuse paths
   (empty text, missing note) and pass paths (backticks/`$VAR` preserved, multi-line
   blockquote) exercised on scratch files. First real use: this note's entries below.

4. **Close bell (`scheduler/close_wednesday.sh`, WED-126 + the residue item):** (a) accepts
   bare `DRYRUN=1` — the 08-27 dry run SPOKE in quiet hours because the script read only
   `WEDNESDAY_DRYRUN`; (b) `scheduler/wrap_check_ignore.txt` lists the standing never-delete
   residue (`.claude/`, the 08-26 conflict copy, the deleted `~$…xlsx` lock) as git pathspecs
   excluded from the wrap check — the bell had flagged the same three items every night (an
   alarm that always fires). **The exercise caught a defect in my own patch:** I wrote
   `$SCRIPT_DIR` where the script defines `SELF_DIR`; under `set -u` the 23:00 fire would
   have died tonight. Fixed; re-exercised through the forced window: DRYRUN logs and exits
   before stamping, no state file, no speech; residue excluded (13 → my in-flight edits only).
   Not ledgered — zero cost, caught by the exercise-before-arming rule doing its job.

5. **Ghost lesson — rung 6 extended + RUNG 9 added:** rung 6 now names the Kam-held
   DECISION offered at a WRAPPED pane (08-29 ×2, "upgrade the Linear workspace, then file
   KS-721"); rung 9 = the principal ACCEPTS a rendered suggestion of my own wording
   (`promptSource: suggestion_accepted`, 08-27 09:05; agent-held; ledger w=3 classification →
   the typed-or-DKIM rule). Ladder count ~88 instances.

6. **Recorded-blocker lesson — third member: a DEFERRAL recorded only in code** (s73,
   KS-586 → KS-692): "tracked on X" in code outlives X; the deferred half needs its own open
   ticket before the parent closes. Brief-writing rule added.

7. **`fleet/specs/brief-standing-lines.md` (NEW) + `fleet/specs/secuura-brief-traps.md`
   (NEW), pointer 5a in `skills/delegation-protocol.md`, pointer in the Secuura card:** the
   template additions owed since 08-27 — typed-or-DKIM authority · set-not-count evidence
   wording · confirm two-word answers when the principal is present · P1D and
   aggregate-drift traps · `--to` takes the project name · and thirteen measured Secuura
   traps (name-the-ref · gitignored dist · compose-hash · service≠container · spec≠Akto
   collection · env prints VAR= · IDENTICAL>0 · NOAUTH is a null · probe-variant ignore ·
   comments(last:) · two-instrument approvals · PR touches walk tickets · positive controls
   write).

8. **Decision card `wed-ledger-archive` raised** (the 08-23 proposal had no answer): archive
   rows older than 08-16 into `_ledger_archive.md` — rec archive, default HOLD, nothing moves.

## Items reviewed and NOT actioned (with reasons)
- **WED-134 one-tap-path** (four scripts still `send-keys` blind): a multi-file build →
  a WED teammate brief per the threshold rule, proposed to Kam in today's priorities;
  `cockpit.sh say` (verified delivery) remains the path I use by hand.
- **WED-132 login-parked pane · WED-133 overnight scheduler wording:** tickets stand; the
  05:30/06:00 mechanics ran correctly this week (respawn branch proved 08-29/08-30).
- **"Mirror mail for a tap during a dead turn" (08-24 practice):** no recurrence — stays a
  practice, not a lesson.
- **Chat-push burst rule** (re-list all role=kam entries after a burst, 08-26): one
  instance, rule lives in the checkpoint block; ledger if it recurs.
- **Reconciled the 08-24 ledger movement** (w=26 · w=12 · w=27): all filed at the time.

## Ledger review (weights)
- **Retired: NONE.** Representations w=25→46 this week (22 instances). Retiring would be
  false comfort; what changed is that FOUR sub-classes now have mechanisms (counts →
  board_count; queue tickets → freshness gate; monitor labels → classified watcher;
  timestamps in prose → stamp helpers). The card-summary and counterpart-claim costumes
  remain rule-only and remain agent-caught.
- **Week's rows:** ~37 corrections (mine) · ~40 fleet insights · 6 praise · 2 grants
  (overnight-is-working-time; Peter monitoring). Zero corrections caught "by noticing":
  every one by an agent at plan confirmation, by a gate, or by an adjacent generated clock.
- **Trend (the health metric, honest):** the RATE is flat-to-rising with the volume of
  briefs (Secuura relay: 25 wraps in five days); the COST is near zero (every instance
  pre-cost or same-minute); the CATCH LATENCY keeps falling. The system is a detector
  network, not a quieter operator — consistent with the 08-14 lesson's own prediction.
- **Praise cluster to protect:** honesty un-hedged (08-28 ×2), deliverables opened not
  pictured, disclose the agent's failure in the same breath as the win.

## Boot-cost review (Kam's standing line)
- **This boot:** learnings dump 549 KB (84 files; `_ledger.md` alone 254 KB / 219 rows) ≈
  125K tokens, read in seven slices because the ledger rows (~470 tokens each) refuse a
  900-line read; plus the 08-29 note (66 KB) + cards/INDEX/scoreboard heads. Boot ended
  near ~45–50% context (08-27 measured the same: ledger + scoreboard whole = the ~10-point
  delta). Trend: ~18K @28 lessons (08-06) · ~65K @46 (08-10) · ~100K @77 (08-23) ·
  **~125K @84 (08-30)**.
- Full load STAYS (Kam 08-06, 08-10, 08-21). The archive card above is the one lever that
  loses nothing; it awaits his word.

## Validation flags (DGM rule)
- VALIDATED this week: `brief_and_launch.sh` (every launch since 08-25 went send → read-back
  → launch; gate refusals fixed by content, zero early launches) · `wrap_send.sh` (three
  rotation/handover wraps, recipient fixed) · `cockpit.sh say` delivery check (08-28 six
  branches; real busy tap caught a false alarm, fixed, then clean) · generated SELF-CHECK ·
  board_count predicates · the movement-window-at-last-write standard (s62 method, used all
  week).
- ADOPTED, AWAITING EVIDENCE: classified board watcher (first real Peter event) ·
  note_entry/prompt_log (first week of use — the test is whether a composed timestamp
  recurs) · close-bell ignore list (tonight's 23:00 fire) · rung-9 typed-or-DKIM line in
  briefs (next signature-class action).

## Scope note (honest)
Consolidation ran on Sunday morning per every handover's "Sun 08-30" — the ritual text still
says "first session after each Sunday". Two audits in a row have run Sunday; if Kam prefers
Monday kept strict, say so; otherwise the ritual line gets amended next week to "Sunday
06:00 slot".
