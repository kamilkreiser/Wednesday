---
date: 2026-09-07
type: pickup
source: replaced wholesale at the 50% checkpoint by the 06:0x morning seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 07:2x AEST, FOUR AGENTS LIVE, nine PRs open, nothing merged all morning

**Time:** ~07:2x AEST Monday. **Mail timestamps are UTC ≈ AEST−10.** Voice is allowed (06:00–23:00).
Kam is AWAKE and ruling actively — he ruled **seven cards** between 06:42 and 07:07. **Run
`kam_rulings_today.sh` before writing anything.**

## STANDING (unchanged)
Opus-5 boot pin through 2026-09-13 (doctor WARNs after). "Keep pushing Secuura to a ready state."
**NexusAI is PAUSED** on Kam's 09-06 17:01 ruling — do not launch it. Nothing merges, deploys or
reaches Peter/Stuart without Kam.

## FLEET — one builder seat (s144, `%142`), launched 08:0x
Everything else closed cleanly: the ATTIO seat wrapped and was scored 1.0; three QA gates reported and
their panes are closed. **Load was 10.5 at 07:5x on Kam's complaint; it is back down.**

## PR STATE — all heads read together by `ls-remote` at 08:0x
```
develop 306d0db923183f3b62b053f0242549e37bdf362c   (unmoved all morning)
#884  f3a037978  KS-858/F5  TIER-1 GATED -> GO on the security question, TWO MAJORS -> round 2 IN FLIGHT (P1)
#876  8d3e5208a  KS-930     TIER-1 GATED -> NO GO on ONE arm -> round 2 queued behind #884
#885  a98df6b11  KS-949     round 1 pushed, NOT re-gated (queued; shape ratified)
#882  7e4603df   KS-698     round 1 READY, NEVER GATED — needs a gate, no fix pending
#874  6f7885602 · #879 79f1fcb48 (stacked on #876) · #880 47b2b60f2 · #881 787771b97 · #883 bac58b93a — untouched today
```

## THE TIME-SENSITIVE THING — Kam ruled a client disclosure for TODAY
`secuura-f5-disclosure-timing` => **withfix**: Peter and Stuart are told today, **with the fix**.
Draft written and HELD at `5_Project_History/2026-09-07_f5-disclosure-draft-for-kam.md`.
**It waits on #884 round 2 being clean + Kam's merge word. Kam sends; nobody else.**

**F5 itself is CLOSED and proven** — fresh HEAD gateway 16/16 on both `//` spellings, fresh BASE
gateway 0/16 with all 8 firing canonically as the control. **F5 IS LIVE ON THE DEMO**, measured:
canonical `100;w=900` vs `//` `2000;w=60` = **300x** on one route. **Bounded: ONE of eight mounts
probed, GET only** — the limiter MISS is measured; whether the demo SERVES a POST through `//` is NOT.

**The two Majors blocking the merge** (both availability/conformance, NEITHER a security hole):
F-QA-1 the fix mangles absolute-form targets so every endpoint 404s where there is no nginx
(`index.ts` KS-245 names Dev/Demo Container Apps as exactly that); F-QA-2 nothing pins the mount or
its ordering — deleting the `app.use` line leaves 277/277 green.

## KAM'S DESK — EMPTY. All ten cards ruled today.
Ruled + delivered: demo-admin-password=b · f5-login-limiter-bypass=wait · f5-demo-exposure-probe=probe ·
f5-disclosure-timing=withfix · f5-demo-interim-mitigation=letitland · attio-renewal-date=one-field ·
attio-entra-consent-m365=scopes-first · attio-entra-consent-decision=open-and-look (**HIS action — open
the consent screen, look for "all mailboxes"**) · demo-admin-mfa=later · demo-admin-transcripts=redact.
**Still undelivered (older, none urgent):** `launcher-turn-end-line` => approve (2026-08-24, **14 days**
— Wednesday's half is to hand the exact wording to each project; owed to s144) · secuura-ci-billing ·
secuura-agent-github-identity · secuura-dependabot-triage · secuura-ks229-disclosure-mailbox ·
secuura-ps-759-760-merge-owner.

## DRIVES — done, verified at the destination
T9 and KK_DEV_Local both carry **WEDNESDAY + `!CODING/Datasec`**, one-way additive, `.git` excluded.
Verified by content (`diff -rq --exclude=.git` on ATTIO = zero lines), not by exit code.
**Kam deleted files on the travel drive deliberately — ruled "gone on purpose, don't restore".**
**NO bidirectional sync on that drive until he says otherwise.** 24 GB of NexusAI `qa-worktrees` scratch
excluded on Wednesday's call. His profile still has `confirmbigdel = false` — raised, his file, his call.

## WEDNESDAY'S ERRORS TODAY — four, all owned in the artefacts
1. **The #882 TIER-1 rating was Wednesday's and measurement broke it** (w=145) — KS-616 is a different
   limiter, already remediated, endpoint has zero consumers. Withdrawn to scope.
2. **"Re-price KS-946 to Blocker"** — no such field; already Urgent. A severity word relayed unchecked.
3. **"Your address is gone from everywhere it is operative"** told to Kam (w=146) — true of the CODE,
   false of the demo. An artefact property stated as a world property.
4. **"The Datasec copy did not finish"** told to Kam (w=2, scope-mismatch) — the gap was `.git`
   internals the copy deliberately excludes. **Second badly-scoped instrument of the morning.**
**Three of the four are one axis: a claim about a running thing composed from an artefact.**

## WHAT WEDNESDAY OWES
1. s144's #884 round 2 → then #876 round 2. **#884 is the critical path to Kam's disclosure.**
2. **Gate #882 `7e4603df`** — READY and never gated, and nothing is pending on it.
3. Re-gate #885 `a98df6b11` (queued for load).
4. Hand the exact approved turn-end wording to s144 (Kam's 14-day-old approval, Wednesday's half).
5. Score s143 and the three QA passes on the scoreboard.

## STANDING NOTES
Env does NOT persist across Bash calls — `set -a; . .env` in the SAME command. **No `cd`** (hook
refuses). **Tap ≤200 chars.** **Verify a sent mail's BODY by `preview` being non-null** — `text` is 0 in
a LIST response for every message. **Use `<<'EOF'` for every brief** and inject live values in a second
step. **An instrument must carry the SAME exclusions as the operation it measures.** Never delete —
quarantine. New work = new branch; push nothing to a branch under gate.
