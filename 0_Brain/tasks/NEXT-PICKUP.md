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

## 🔴 FIRST ACTION — s148 is on ROUND 3 (#892). Nothing else is running. Two things sit with Kam.
**All four gates have reported and all four panes are closed.** s148 is the only live agent.
**Do not start anything on the demo box** — the id-keyed decider is Kam's, **default STOP**.

## KAM'S DESK
- **`secuura-ks968-id-keyed-decider`** (rec `id-count`, **default STOP**) — `P=30` came back non-zero,
  **but that is NECESSARY, not SUFFICIENT** for the rotation story, and Wednesday's brief wrongly said
  otherwise. **One id-keyed count decides it, and it touches no hash so it is independent of the key.**
  **1 → rotation → incident (email login broken for those rows). 0 → benign, KS-968 moot.**
  **On silence: record CONSISTENT-WITH BUT UNESTABLISHED. Do not let it read either way.**
- `vault-ssh-pointer-heal` — **the LAPTOP's, not ours.** Do not adopt.

## STATE — every SHA is an agent's `ls-remote`, NOT re-derived here
    origin/develop   6c60cc09b   (#888, #890 merged today; NEITHER deployed)
    demo VM          632f16dfe   (untouched all day)
    #892  42e778203  ROUND 3 IN PROGRESS — F1 as a QUARANTINE (not a skip), F2 as a COMMAND SET.
                     Cap already spent: NO ROUND 4 WITHOUT KAM.
    #889  42d8cf5f5  Kam's BIND is CORRECT and gate-proved — but F1 MERGE-BLOCKS: the PR's own
                     integration suite is RED and its passing cells are VACUOUS. Needs a round 2.
    #893  0281b0faa  #894 merged into it. ** #893 -> develop HELD ** — it was waiting on #889, and
                     #889's answer is "not yet". THAT merge is the one that moves the trunk.
    #891  3c07157a2  KAM'S OWN CLICK — https://github.com/Secuura/Distributed_Secuura/pull/891
**Owed tickets:** the **F-1** from the #894 gate (`/api/rate-limit/check` publishes `maxLength: 256`
and still enforces code units, **on the route with NO role gate** — MAJOR, leads F-2…F-5); and the
gate's **F3 tooling finding**: `run-migrations.sh` reports `applied=N failed=0` **for migrations it
SKIPPED** — which is why three agents today insisted on confirming a migration BY NAME.

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
**AND THAT IS ONLY HALF THE FIX — learned 19:47.** Not staging them does not help, because
`rebase.autoStash` captures the whole dirty working tree and its REAPPLY conflicts on the same ten.
**So discard their local churn BEFORE pulling:**
`git -C <wed> checkout -- 0_Brain/dashboard/data/{agentmail,brain_state,datasec_calendar,linear_personal,linear_wed,news,parkinglot,personal_calendar,secuura_error,tickets}.json`
**then** pull. They are regenerated within seconds, so discarding costs nothing and the autostash
then has nothing to fight over. **Never discard `chat_log.json` or `decisions.json` this way.**
Equal counts prove nothing — both `chat_log` sides once read 1630 and each held a message the other
lacked.

## GIT
**PULL BEFORE EVERY WRITE** — the laptop seat is live on this vault. Use ONE chain:
`add -A dashboard/data && commit && -c rebase.autoStash=true pull --rebase && push`. **If the autostash
reapply conflicts, resolve dashboard/data to HEAD and re-union `chat_log.json` from a backup** — take
a copy of it BEFORE any multi-step git sequence. **Keep every autostash; drop nothing.**
