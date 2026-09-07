---
date: 2026-09-07
type: pickup
scope: SECUURA + Wednesday's own work. Datasec belongs to the LAPTOP seat — do not touch its threads.
source: replaced WHOLESALE at 20:40 by the 20:12 seat, at its 50% checkpoint
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 20:40 AEST Monday. TWO GATES IN FLIGHT. ONE CARD ON KAM'S DESK. Nothing merged, nothing deployed.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything — read EVERY line.**
Mail UTC ≈ AEST−10. **ROTATION BAND 80–90% (Kam 10:49); 70% is a CHECKPOINT ONLY.**

## 🔴 FIRST ACTION — read the two gate panes, then the inbox. Nothing else is owed to anyone.
**`%166` QA-889-r2 (tier 1) and `%167` QA-892-r3 (tier 2) are both LIVE and progressing.**
**`%162` Secuura/Blockchain is DORMANT BY DESIGN at 47%** — it named its wake as the two verdicts,
Wednesday told it in writing to stay on them, and **WEDNESDAY IS ITS WAKE PATH.** Its idle is correct;
do not read the watcher's repeating idle alert as a stall (see STANDING, below).

## KAM'S DESK — one card, and one click
- **`secuura-ks968-id-keyed-decider`** (rec `id-count`, **default STOP**). P=30 is NECESSARY, not
  SUFFICIENT, for the rotation story. One id-keyed count decides it and **touches no hash, so it is
  independent of the key in question.** 1 → rotation → incident (email login broken for those rows).
  0 → benign, KS-968 moot. **On silence: CONSISTENT-WITH BUT UNESTABLISHED. Nothing further runs on
  that box.**
- **PR #891 is KAM'S OWN CLICK** — GitHub refuses the agent's token on a `.github/workflows` file.
  **https://github.com/Secuura/Distributed_Secuura/pull/891** — every reminder carries the link.

## STATE — every SHA is an agent's read, NOT re-derived at this seat
    origin/develop   6c60cc09b   (#888, #890 merged today; NEITHER deployed)
    demo VM          632f16dfe   (untouched all day)
    #892  34a48abc6  ROUND 3, UNDER GATE at %167. Kam authorised this round himself
                     (round3-narrow, F1+F2 ONLY). ** NO ROUND 4 WITHOUT KAM ** — a NO GO here
                     goes back to him, it does NOT ship under the two-NO-GO cap.
    #889  48ad0354e  ROUND 2, UNDER GATE at %166. Round 1 was NO GO on F1.
    #893  0281b0faa  ** #893 -> develop still HOLDS ** behind #889. That merge moves the trunk.
    #891  3c07157a2  Kam's click (link above).
**Filed this evening by s148:** KS-974 (F-1+F-5) · KS-975 (F-2+F-4) · KS-976 (F-3).
**KS-808 already covered the `run-migrations.sh` finding** — evidence added there, hold reason
written ON the ticket. **No owed tickets remain.**

## WHAT THE GATES MUST COME BACK WITH — do not accept a green run for either
- **#889:** the proof is **the TAMPER, not the green integration suite** — a green suite is exactly
  what the BROKEN state produced (three cells were vacuous; only the positive control caught it).
  Delete the `AND tenant_id` predicate from BOTH organizations subqueries → the two cross-tenant
  cells must go RED. **Plus a green baseline**: a red-proof shows a check CAN fail; only a baseline
  shows it passes for the right reason.
- **#892:** F1 is a POSTCONDITION claim — *"a non-write is not a removal"*. A stale drifted manifest
  outlives a non-write. **`generated/` is gitignored, so a clean `git status` is NOT evidence.**

## WHAT WEDNESDAY GOT WRONG THIS SEAT — both agent-caught, neither reached a cost
- **A SEVERITY WORD WITH NOTHING BEHIND IT:** called F-2 *"an unpinned arm rather than a live
  defect"*. **It changed a live 200 → 403 on `/check`, the route with NO role gate.** Unpinned is
  true; not-a-live-defect is false, and only that half decides how hard a thing gets pushed.
  Classification-is-the-field, **w=11**, hours after the same family was gate-refused.
- **A TOOL PATH COMPOSED FROM ITS NAME:** reached for `fleet/pane_prompt_check.sh`, got "No such
  file", and was one sentence from telling Kam the ghost-text detector was missing. **It lives at
  `fleet/cockpit/pane_prompt_check.sh`.** Prove an absence with `find`/`grep` + a positive control —
  a failed `bash <path>` is `ls`'s costume.

## STANDING — and two that are NEW this seat
No `cd` (hook; it also refuses `git -C $VAR` — use literal paths). Taps ≤200 chars with a verified
mail behind them (`--mail`). `<<'EOF'` for briefs; **`-F -` for commits, never `-m`**. Never delete —
quarantine. **Search before you file, by SYMBOL/PATH/ERROR STRING — and run the FUZZY search too:
the noise is what found KS-808** (`fleet/specs/brief-standing-lines.md`).
**`0_Brain/dashboard/data/` holds TWO irreplaceable files** — `chat_log.json` and `decisions.json`.
**Never `git add -A` it and never `git checkout <sha> --` it.** Discard the ten regenerated feeds by
name BEFORE pulling, then stage only those two. Copy both to the scratchpad first.

**🟡 NEW — THE WATCHER'S IDLE LEG HAS NO FIRE-ONCE, and it is firing on a correctly-dormant seat.**
`wake_watch.sh:151-160` increments `cnt` and fires on EVERY subsequent sample — **the same defect as
the frozen leg (w=2). The diagnosis is that it is in NEITHER leg but in the shared pattern**: both
count consecutive qualifying samples and fire on `>=`, and neither resets. **MEASURED AND SAFE: leg
(a), new mail, runs FIRST and `exit 0`s before the pane leg (`:60-61`) — a repeating idle wake CANNOT
mask a verdict.** **NOT FIXED, deliberately: two gates are live on this watcher.** Fix shape, one
line for both legs: reset the counter on fire, or a `fired_$key` marker cleared when the hash changes.
**CHEAP TRIAGE, one call:** inbox since baseline · `grep` both gate panes for their commissioned
nouns · detector on the idle pane.

**🟡 NEW — QA LAUNCHERS ARE MOVING OUT OF THE GITIGNORED DRAWER.** `fleet/state/` is gitignored and
holds **128 wrappers + 128 prompt files** — invisible to every git search a successor can run, which
is how a seat nearly rebuilt a launch command by hand and bypassed its own guards. **New wrappers now
go to the TRACKED `fleet/qa-agent/launchers/`** (the two live ones are there). **The bulk move of the
128 is QUEUED — a `mv`, never a gitignore change, and never while gates are live.**

## GIT
**PULL BEFORE EVERY WRITE** — the laptop seat is live on this vault. Discard the ten regenerated
dashboard feeds by name, stage `chat_log.json` + `decisions.json` + your real changes, then
`-c rebase.autoStash=true pull --rebase && push`. **Keep every autostash; drop nothing.**
HEAD at this checkpoint: `0b3c4e66`, clean, == origin/main.
