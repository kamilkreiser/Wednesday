---
date: 2026-09-07
type: pickup
scope: SECUURA + Wednesday's own work. Datasec belongs to the LAPTOP seat — it is ALIVE and working; do not touch its threads.
source: replaced WHOLESALE at ~16:10 by the 12:3x seat, after the deploy landed
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ~16:20 AEST Sunday. DEPLOY LIVE **AND #888 MERGED**. One seat, two PRs awaiting gates.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything — read EVERY line.**
Mail UTC ≈ AEST−10. **ROTATION BAND 80–90% (Kam 10:49); 70% is a CHECKPOINT ONLY.**

## ✅ THE DEPLOY LANDED — develop `632f16dfe` IS LIVE on the Secuura demo
31/31 images, 0 failed, **33 containers Up/healthy**, portals + API 200, anchoring on
`cardanoMode: "REAL (Blockfrost)"` (the runbook's mandatory post-redeploy check).
**Verified by ARTEFACT with a negative control** — each of the five merges by a content marker in the
deployed image, and the seat's own UNMERGED KS-952 work confirmed ABSENT, so the markers discriminate.

**KAM'S IDENTITY: 10 files BEFORE → 3 AFTER.** The three are host-side `dist/` output the rsync
excludes by design. **Control: the fictional identity 0 → 7 files.** Measured INSIDE the running
container too (auth: fictional 1x, real 0x). **THE DATABASE ROW IS UNCHANGED — never blur that.**
**The consequence to carry: fix KS-962 and the row rewrites itself to the fictional identity on the
next boot. This deploy STAGES his remediation without applying it.**

## 🔴 KAM'S CALL, FLAGGED NOT FIXED — the demo-service
`up -d` created a **default-profile `demo-service`** that entered a restart loop (`DEMO_SERVICE_ENABLED`
absent from the VM `.env`; proven not running before — `.env` mtime 09-03, guardian/queue `Up 22 hours`).
**The seat stopped it, restoring the pre-deploy state, and deliberately did NOT set the flag: that
service mints REAL Platform Admin tokens with NO caller credential.** Refusing to start is it failing
CLOSED, which is correct. **Enabling it is a security opt-in and Kam's alone.** Nothing is exposed.

## ✅ #888 IS MERGED — `632f16dfe` → **`9e9a88709fb80517463d18d67a8ada02bc2e6ca6`**
Tree oid predicted BEFORE and matched · parents re-derived FROM THE OBJECT not the API · containment
both ways **with a control** (#890 `74c0b3bbf` absent, so the check discriminates) · F1 re-confirmed
on develop (`.env.example:133` empty). **NOT DEPLOYED — the demo still runs `632f16dfe`.**
**KS-966 moved back to `In Progress`** (the merge auto-transitioned it to `In Review`, which would
have read as done while items 3+4 are open).

## 🔴 FIRST ACTION — gates on the two open PRs
**#890 (KS-952, `74c0b3bbf`)** and **#891 (KS-418 docs, `3c07157a2`)** are open and awaiting gates.
**#889 (KS-597, `af640e809`)** also open. Tier them by what they touch.

**KS-968 IS FILED, MAJOR** (the residue ticket — it did not exist until 16:1x).
Content: `if (byId)` at **`:1363`** rewrites the `…0020` row's `email_lookup_hash`; a distinct row
holding that hash makes it a **23505**; the catch logs and `continue`s **without rethrowing**; and
`if (emailRowIsDistinct)` sits at **`:1388`, AFTER the throwing statement** — so the F3 arm never runs
when both rows exist. Pre-existing, equally open on develop. **Item 1 is the misleading GREEN CELL**
(passes only because the vitest `db` double cannot enforce a unique index). **Item 3: do NOT probe the
demo — likelihood UNKNOWN and that probe is Kam's to authorise.** **The regression test must drive a
REAL Postgres.** **The swallowing catch is part of the defect** — same class as KS-962's `debug`-level
seed failure, two instances in one afternoon.

**⚠ A CORRECTION THAT WAS QUOTED ONWARD:** s146's original 23505 reasoning (that the collision came
from rewriting the address onto the row found BY it) is **WRONG** and reached three artefacts. It is
corrected **by comment, not by edit**, on KS-966, #888 and KS-968. **Do not re-inherit the old
version.** Its own formulation, now filed M-tier: *"I had a real measurement and attached it to the
wrong statement, which is a costlier error than not measuring at all, because it looks like evidence."*

## S146's QUEUE AFTER THE MERGE
KS-952 (#890 open) · the KS-418 docs (#891 open, branch deliberately WITHOUT the ticket id so it does
not transition Peter's ticket) · KS-597 (#889 open) · KS-966 items 3+4 (**item 4 opens with the
MEASUREMENT** — prove the generated-actor path resolves before removing any fallback). **KS-967 filed.**

## BOARD — catalogue delivered, 280 open
`5_Project_History/catalogue-2026-09-07/` — one page, 323-row appendix, **and
`HIERARCHY-CONSUMERS-2026-09-07.md`**. 11 archived, 6 held with reasons ON the tickets.
**THE 88→50 RESTRUCTURE IS CANCELLED — do not re-propose it.** One parent per issue; **207 issues sit
under 26 parents**; **the extranet republishes the hierarchy**; review streams win the slot (Kam's
process). **Archiving preserves the parent link; re-parenting does not.** 88→50 is a DESCRIPTION.

## GIT — two collisions today, both resolved
**PULL BEFORE EVERY WRITE.** `origin/main` moved under this seat twice (the laptop seat is live).
**Do NOT `git stash push` before `pull --rebase`** — the rebase autostashes and doing both gave a
12-file conflicted pop (resolved; quarantined at `5_Project_History/_quarantine_2026-09-07_rebase-conflicts/`;
all stashes kept). **The dashboard rewrites `0_Brain/dashboard/data/` continuously, so any multi-step
git sequence is racy — use ONE chain:**
`add -A dashboard/data && commit && -c rebase.autoStash=true pull --rebase && push`.
**SSH to GitHub failed intermittently ~15:5x–16:0x and RECOVERED on its own.** The key was never the
problem (fingerprint verified against its `.pub`); the discriminator is the error text changing from
*could not read from remote* to *non-fast-forward*. **Never borrow another identity to get past it.**

## STANDING
No `cd` (hook — and the hook CHANGED under this seat at 15:08 from the laptop; re-verify both
directions after any such change). Taps ≤200 chars with a verified mail behind them. `<<'EOF'` for
briefs; **`-F -` with a quoted heredoc for commit messages.** Never delete — quarantine/archive.
**What merges must be what was gated.** **Search before you file — by SYMBOL/PATH/ERROR STRING.**
**Ticket creation aggregates on the TEST PASS** (Kam 13:23) — and that governs CREATION, not retrofit.
**A branch name is an INSTRUCTION TO THE BOARD:** never put a client human's ticket id in one.
