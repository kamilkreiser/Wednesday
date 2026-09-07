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

## 🔴 FIRST ACTION — the one thing with a pending trigger
**#890 has a MERGE GO from Wednesday, held ONLY on sequencing.** It waits for the **#889 re-gate**
(pane `QA/KS-597-889-r2`) to report. **The moment that verdict lands: tap s147 to merge #890 at
`4096bdd1a` — the gated head, unamended.** The seat was told the wake is a tap and to mail-and-ask if
nothing comes within the hour, so **an unanswered hour is a broken promise, not a quiet queue.**

## KAM'S DESK — three open cards, ALL default-safe, none blocking
1. **`secuura-889-issuer-org-caller-asserted`** (rec `hold-for-finding1`, default HOLD) — the issuing
   organisation on #889 is **caller-asserted and never bound to the actor**, and #889 is the first
   change that puts it on the **public verification surface**. Whether an org is a trust boundary
   inside a tenant is the open question **KS-621** holds. **A merge here decides a product question,
   so it is Kam's.** ⚠ **The head has MOVED since the card was written** (`af640e809` → `fc4480188`,
   test-only; `documentRepo.ts` byte-identical). The card's question is head-independent; the re-gate
   exists so his ruling is immediately actionable. **`decision_queue.sh` has no edit verb — he was
   told on the panel.**
2. **`secuura-891-workflow-scope-merge`** (rec `kam-merges`, default LEAVE OPEN) — GitHub refuses the
   PAT on a `.github/workflows/` file. **Widening the token is deliberately NOT an option and a
   successor must not re-propose it.** Matches his own 2026-09-05 `kam-merges` ruling.
3. **`secuura-ks968-demo-hash-probe`** (rec `probe`, default HOLD) — two read-only `SELECT count(*)`s
   would settle whether KS-968 fires on the demo. **s146 refused to run it and was right; do not run
   it on silence.**

## STATE — every SHA is an agent's `ls-remote`, NOT re-derived by Wednesday (no Secuura identity here)
    origin/develop   9e9a88709   (#888 merged 16:1x; NOT deployed)
    demo VM          632f16dfe   (unchanged all afternoon)
    #890  4096bdd1a  round 2 GATED GO-with-findings — MERGE GO given, awaiting the sequencing tap
    #889  fc4480188  Finding 2 closed; re-gate LIVE; merge HELD on Kam's card 1
    #891  3c07157a2  MERGE GO given, BLOCKED on PAT workflow scope, Kam's card 2
**KS-970 filed** (six items, one path — the scope encoder and its published contract; F-3 leads: a
whitespace-only `tenantId` on `/reset` silently retargets the caller's own bucket **and answers 200**).
**KS-969 filed** (systemTest actor/credential story, four items; **item 1 is the unlock** and is s147's
current work). **KS-968** = the seed's 23505 swallow. **KS-967** filed earlier.

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
**NEW — `chat_log.json` is written by BOTH Wednesday seats.** A rebase conflict there is NOT routine
churn: **merge by UNION on `(ts, text)`, never pick a side.** Equal message counts prove nothing —
today both sides read 1630 and each held one message the other lacked. **A VCS default there silently
deletes one of Kam's panel messages.**

## GIT
**PULL BEFORE EVERY WRITE** — the laptop seat is live on this vault. Use ONE chain:
`add -A dashboard/data && commit && -c rebase.autoStash=true pull --rebase && push`. **If the autostash
reapply conflicts, resolve dashboard/data to HEAD and re-union `chat_log.json` from a backup** — take
a copy of it BEFORE any multi-step git sequence. **Keep every autostash; drop nothing.**
