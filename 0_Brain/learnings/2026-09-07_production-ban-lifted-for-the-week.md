---
date: 2026-09-07
type: grant
source: Kam, panel 2026-09-07 12:07:38
status: live
tier: W
expires: 2026-09-13 (Wednesday's reading of "this week", stated to Kam; doctor.sh warns after)
scope: SECUURA ONLY — CONFIRMED by Kam 2026-09-07 12:10:40 ("Only secure" = Secuura, his Whisperflow rendering, which he corrected himself at 09:50:58 earlier the same day)
---

# The production ban is lifted for the week — read narrowly, flag every use

**His words, verbatim:** *"Lift the production ban. This week we are allowed to make production
changes, but flag these when relevant or when making changes. Make the change directly."*

**This is the largest boundary Kam has moved.** "Never touch prod" is one of the seven hard rules and
carries its own skill (`never-update-prod`). It is his to lift and he has lifted it. **It is not
Wednesday's to widen.**

## The three things Wednesday did with it, in order
**1. It told him the grant does not unblock what he thinks it unblocks.** The demo deploy was never
held by the production ban — it is held because **the fix is wrong** (it would write twelve plaintext
addresses into an encrypted column, eleven of them public demo personas). **Lifting the ban changes
nothing about that.** Saying so cost one paragraph and prevented him believing the road was clear.
**A grant given against a misdiagnosed blocker is worth correcting even though the grant is welcome**
— [[2026-08-21_challenge-me-when-you-think-im-wrong]].

**2. It read the scope NARROWLY and said so with a default.** Taken as covering **Secuura**, the
project under discussion. **NOT** taken as covering Datasec production — which includes Vision's live
site and database in `datasec-sales-portal-rg` — because that belongs to the laptop seat and because
the asymmetry is absolute: **reading it narrowly costs one more question; reading it broadly and
being wrong costs a production system at another client.** Stated to him as a default he can correct
in one word.

**3. It recorded the expiry as a CHECK, not a note.** "This week" → through **Sunday 2026-09-13**,
stated as Wednesday's reading. `doctor.sh` now warns after that date across **all three** of the
week-scoped grants he gave today (merge 09:40, deploy 11:09, production 12:07). Both branches
exercised with the clock moved.

## What remains OUTSIDE the grant, because he did not name it
- **A credential that live systems authenticate with is a ROTATION, and it still comes to Kam.** The
  published admin password in 128 files is the live example; he ruled `rotate-properly` on it, and
  that ruling governs — the production grant does not silently absorb it.
- **External communication to any human.** Untouched.
- **Anything irreversible that a production grant does not itself imply** — history rewrites,
  credential deletion, destructive tenant operations.
- **Other clients**, pending his answer.

## How to apply
1. **Flag every production change** — his condition, taken as a standing obligation rather than a
   courtesy: named to Kam **before** where there is time, **immediately after** where there is not,
   with what changed and where. **It goes into every agent's standing HOLDS**, not just Wednesday's
   memory ([[2026-08-09_an-enforcement-you-must-arm-is-not-one]]).
2. **Name the destination** — a production change states the environment and subscription in its BLUF,
   exactly as a commit states its remote and branch
   ([[2026-09-07_name-the-field-that-says-whose-it-is]]).
3. **The grant removes the pause, not the receipt** ([[2026-08-07_autonomy-grant-ship-decisions]]).
4. **Never argue an action into scope.** If it needs a clever reading of "production changes", it is
   outside it — and this grant in particular will be read by successors who were not in the room.

**Family:** [[2026-08-07_protocol-v1.3-signed-delegation]] (production was his signature class; this
suspends that one line for a week) · [[2026-09-07_merge-authority-was-already-mine]] and
[[2026-09-07_deploy-grant-and-fix-the-visible-data]] (the day's other two week-scoped grants — check
the register before asking for any of the three) · [[2026-09-06_a-scoped-override-carries-its-own-expiry]] ·
[[2026-08-03_go-slow-earn-autonomy]] (rule 5) · [[2026-08-21_challenge-me-when-you-think-im-wrong]].
