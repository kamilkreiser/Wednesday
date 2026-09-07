---
date: 2026-09-07
type: pickup
scope: SECUURA + Wednesday's own work. Datasec belongs to the LAPTOP seat — it is ALIVE and working (it rotated 17:07 and its successor is running). Do not touch its threads.
source: replaced WHOLESALE at ~17:55 by the 16:2x seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ~17:55 AEST Sunday. THREE CARDS ON KAM'S DESK. #890 has a GO awaiting one tap.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything — read EVERY line.**
Mail UTC ≈ AEST−10. **ROTATION BAND 80–90% (Kam 10:49); 70% is a CHECKPOINT ONLY.**

## 🔴 FIRST ACTION — nothing has a pending trigger; two gates report to you
**Both live gates mail their verdicts to WEDNESDAY, not to the seat.** When one lands, rule it, then
tap s148. **s148 must not poll them.**

## KAM'S DESK — ALL SECUURA CARDS RULED. Nothing of mine is open.
He ruled six today. **The two that became work are `bind` and `strong-control` (19:00), both now in
s148's brief.** `#891` remains **his own click** — link given, not ours:
`https://github.com/Secuura/Distributed_Secuura/pull/891`.
**Still open and NOT MINE:** `vault-ssh-pointer-heal` (Fleet/workspace — the LAPTOP seat's card; it
edits the shared workspace `CLAUDE.md`, which is outside this seat's writable scope; Kam has ruled it
three times, so his panel is re-presenting it) and two `nexusai-*` cards (the laptop's).
**Do not act on any of those three.**

## STATE — every SHA is an agent's `ls-remote`, NOT re-derived here (no Secuura identity on this seat)
    origin/develop   6c60cc09b   (#888 and #890 both merged today; NEITHER deployed)
    demo VM          632f16dfe   (untouched all day)
    #892  42e778203  round 2 GATE LIVE — NO GO 1 of 2 already spent, a NO GO here SPENDS THE CAP
    #893  ab1053141  queued for ONE tier-1 gate on #894's head (contains #893)
    #894  e02d0fecc  stacked on #893 so #893's gated head cannot move; not re-targeted at develop yet
    #889  9898ae724  Kam ruled BIND — the change is s148's work, then a TIER 1 gate, then merge
    #891  3c07157a2  KAM'S OWN CLICK
**KS-973** = the #892 residue (F4, F5 + the F6–F9 minors). **KS-970** complete. **KS-969** items 1–3
done, item 4 still blocked on #892 landing. **KS-968 status: UNMEASURED, not clear** — the probe
returned zeros from an instrument nobody had shown could return non-zero; **Kam authorised the strong
control at 19:00 and s148 runs it, pre-registered and hashed first.** The earlier pre-registration is
durable at `5_Project_History/KS-968-probe-preregistration-2026-09-07.txt`.

## WHAT WEDNESDAY GOT WRONG TODAY — all agent- or gate-caught, none reaching a cost
- **The #890 fix instruction was wrong THREE ways** (base64url renames the `-` sentinel rather than
  removing it; a total encoder alone creates a fresh surrogate collision class — Wednesday's own
  objection to a try/catch applied to Wednesday's own fix; and the wire cell specified could not pass
  under the fix specified in the same mail). **The SELF-CHECK attestation PASSED on that mail** —
  `self_check_view.sh` compares ids and numbers and has **no view for mechanism-versus-cell.**
- **A GO naming a gated head, plus an instruction to edit that head, in one mail.** s147 refused and
  was right. **Rule: a GO that names a head must say whether any edit precedes or follows the merge.**
- **An absence claim made twice with blind instruments** (`ls` on the repo root; `head` on
  `history.md`) **about an agent's honesty** — both artefacts existed. **Use `find`/`grep` to prove an
  absence, never `ls`/`head`.**
- **"Current develop head" written as "the PR's base"** — four different facts (head, base,
  merge-base, the PR's recorded base). The tester caught it; a two-dot diff would have been poisoned.
- **`cockpit.sh rotate` used on an ALREADY-WRAPPED seat** → false "work may be lost" alarm. Its window
  opens at the tap; it cannot see a wrap that already happened. **Use a plain relaunch instead.**

## STANDING — and two that are NEW today
No `cd` (hook; it also refuses `git -C $VAR` because it cannot resolve the variable — use literal
paths). Taps ≤200 chars with a verified mail behind them (`--mail`). `<<'EOF'` for briefs; `-F -` for
commits. **Never delete — quarantine.** **Search before you file, by SYMBOL/PATH/ERROR STRING.**
**NEW — the shared local dev stack is STALE BY DESIGN** (121 commits behind at 17:19): a gate that
drives it tests an old build. **Every gate brief now says: build your own from the repo's provisioning
path, or state what a stack built on <date> cannot prove.** **The local seeded stack on :6882 also
took unparameterised writes** from a QA pass (disclosed) — **treat its DATA as untrusted until
re-seeded.**
**🔴 NEW AND LEARNED THE HARD WAY — `0_Brain/dashboard/data/` HOLDS TWO IRREPLACEABLE FILES, NOT ZERO.**
`chat_log.json` (Kam's conversation) **and `decisions.json` (the decision queue's durable state — his
RULINGS).** Everything else in that directory is a regenerated feed. **NEVER
`git checkout <sha> -- 0_Brain/dashboard/data` as a blanket conflict resolution.** Wednesday did that
twice on 2026-09-07 and **destroyed four of Kam's rulings and three whole cards** — he re-ruled them
fifty minutes later because the panel showed them open again. Nothing was ACTED on wrongly (the
operational effects were already mailed to the agent) but the RECORD was gone and unrecoverable:
the cards had never been committed, so git had nothing, and the autostashes predated them.
**The rule: resolve dashboard/data file-by-file. `chat_log.json` merges by UNION on `(ts, text)`;
`decisions.json` merges by UNION on card `id`, keeping the RULED version of any card present in both;
the other ten may take upstream.** **Copy BOTH to the scratchpad before any multi-step git sequence.**
**🔴 AND THE CAUSE-LEVEL FIX, adopted 19:1x after this broke FOUR times in one hour: NEVER
`git add -A 0_Brain/dashboard/data`. Stage ONLY `chat_log.json` and `decisions.json`, by name.**
The other ten are rewritten continuously by the dashboard server, so they change between the `add` and
the `pull`, and the autostash reapply then conflicts on all ten **every single time** — leaving
conflict markers in files the dashboard reads. **Leaving them uncommitted costs nothing: they are
regenerated.** Staging them by directory is what turned a routine sync into a repeated repair.
Equal counts prove nothing — both `chat_log` sides once read 1630 and each held a message the other
lacked.

## GIT
**PULL BEFORE EVERY WRITE** — the laptop seat is live on this vault. Use ONE chain:
`add -A dashboard/data && commit && -c rebase.autoStash=true pull --rebase && push`. **If the autostash
reapply conflicts, resolve dashboard/data to HEAD and re-union `chat_log.json` from a backup** — take
a copy of it BEFORE any multi-step git sequence. **Keep every autostash; drop nothing.**
