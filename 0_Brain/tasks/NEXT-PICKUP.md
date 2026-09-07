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

## 🔴 FIRST ACTION — three cards are on Kam's desk and ONE of them gates a Blocker
**Nothing runs until he rules `secuura-892-cap-spent-blocker-open`.** #892 took its SECOND NO GO, so
**the cap is spent** — and F1, the Blocker, is still open. **Do NOT merge #892 under the cap:** the cap
says closed instances ship and the residue is ticketed, **but #892 IS the instance**, so merging it
ships the exact defect KS-969 exists to remove with a ticket attached. Recommendation on the card is
one narrow round 3 (both fixes are one-liners, per the gate). **Default HOLD.**

## KAM'S DESK — three open, all default-safe, all mine
1. **`secuura-892-cap-spent-blocker-open`** (rec `round3-narrow`, default HOLD) — above.
2. **`secuura-ks968-hash-population-count`** (rec `count-populated`, default STOP) — **the KS-968
   control returned C=0, the pre-registered "instrument NOT validated" arm, so NOTHING was concluded.**
   Two explanations survive and **one is not about KS-968 at all**: either that address has no row, or
   **the rows were hashed under a rotated key — which breaks email login on that box, because login
   resolves users by that hash.** One integer separates them. **On silence, record KS-968 as
   UNMEASURED and the key-rotation possibility as UNINVESTIGATED — do not let either read as clear.**
3. **`secuura-org-trust-boundary-within-tenant`** — **ALREADY RULED `bind`**; the change is pushed.
**NOT MINE and not to be adopted:** `vault-ssh-pointer-heal` (Fleet/workspace — the LAPTOP's card, and
it edits the shared workspace `CLAUDE.md`, outside this seat's writable scope) and any `nexusai-*`.

## STATE — every SHA is an agent's `ls-remote`, NOT re-derived here (no Secuura identity on this seat)
    origin/develop   6c60cc09b   (#888 and #890 merged today; NEITHER deployed)
    demo VM          632f16dfe   (untouched all day)
    #889  42d8cf5f5  Kam's BIND is PUSHED — needs a TIER 1 gate, then merge. NOT gated yet.
    #892  42e778203  NO GO x2, CAP SPENT, F1 Blocker + F2 open — carded, do not merge
    #893  ab1053141  contained inside #894
    #894  e02d0fecc  ONE tier-1 gate LIVE over the stack (gating #894 gates #893)
    #891  3c07157a2  KAM'S OWN CLICK — https://github.com/Secuura/Distributed_Secuura/pull/891
**Live panes:** `Secuura/Blockchain` (s148, on KS-973) · `QA/KS-970-894` (the stack gate).
**Both gates report to WEDNESDAY, not to the seat.** **#889's tier-1 gate is OWED and not yet
launched** — launch it when a pane frees; it is the last thing standing between Kam's `bind` ruling
and a merge.

## WHAT THE #892 GATE FOUND THAT MUST NOT BE LOST
**F1: withholding a manifest is a NON-WRITE, not a REMOVAL** — a stale drifted manifest already on
disk survives the fix and the suites still read it. **There is a live instance on the builder's own
worktree.** **F2: `run.py quality` is EXEMPT from the pre-step and runs 389 live-API cells.**
**F3 (new): the cell pinning "a refusal is not a warning" CANNOT FAIL.**

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
