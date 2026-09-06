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

## FLEET — four agent panes, all productive
| pane | who | on |
|---|---|---|
| `%137` | Secuura/Blockchain (s143, seat A) | **#876 round 1** (the F-6 regression) + the breadth question |
| `%138` | QA | **#884 @ `f3a037978` tier 1** — the F5 fix |
| `%139` | QA | **#885 @ `9be9a8380` tier 1** — the demo admin identity |
| `%140` | Datasec/Vision (s10) | ATTIO: scopes REPORT, then one attribute (dry-run → mail → write) |

**Two seats stalled at turn end this morning (%137, twice).** Detector first (`pane_prompt_check.sh`),
then a ≤200-char pointer tap. Cause diagnosed — see the daily note: the deployed launcher line is a
narrower paraphrase than Kam approved and misses "next I will do Y".

## PR STATE — all heads read by `ls-remote` at 07:2x, verified in this action
```
develop 306d0db923183f3b62b053f0242549e37bdf362c   (unmoved all morning)
#874  6f7885602  KS-926   tier-2 round 2 of 2 — NOT GATED TODAY
#876  a0ad0a084  KS-930   NO GO round 1 — regression, fix round in flight
#879  79f1fcb48  KS-945   STACKED on #876, blocked behind it
#880  47b2b60f2  KS-577   Stuart cutover — Kam's, not gated
#881  787771b97  OAuth cluster — NOT GATED TODAY
#882  bd2b761a0  KS-698   NO GO round 1 — queued behind #876
#883  bac58b93a  KS-729 leg 1 — NOT GATED TODAY
#884  f3a037978  KS-858/F5 — GO ruled on the criterion; TIER-1 GATE RUNNING
#885  9be9a8380  KS-949   demo admin — TIER-1 GATE RUNNING
```
**#876 and #882 both had a tier-1 NO GO. Round 1 of 2 under Kam's cap — a second NO GO on either
class ships the closed instances and tickets the residue.**

## THE ONE THING THAT IS TIME-SENSITIVE
**Kam ruled `secuura-f5-disclosure-timing` => withfix: Peter and Stuart are told TODAY, with the fix.**
The draft is written and HELD at
`5_Project_History/2026-09-07_f5-disclosure-draft-for-kam.md`. **It waits on the #884 gate reporting
and Kam's merge word.** Kam drafts nothing and Wednesday sends nothing — **Kam sends.**

**F5 IS LIVE ON THE DEMO**, measured (2 read-only GETs): canonical `100;w=900` vs `//` `2000;w=60`,
**300x** on `/api/auth/verify-email`. **Bounded: ONE of eight mounts probed; GET only, so the limiter
MISS is measured and whether the demo SERVES a POST through `//` is NOT.** Kam ruled
`secuura-f5-demo-interim-mitigation` => **letitland** — nothing touches the demo, the fix lands.

## KAM'S DESK — 2 open cards, both default HOLD, neither urgent
1. `secuura-demo-admin-transcripts` — his name is in 10 dated session transcripts. Rec: redact WITH a
   dated note. The agent refused to rewrite them (*"falsifies a record rather than fixing a defect"*).
2. `secuura-demo-admin-mfa` — MFA still off on the demo admin. Rec: leave until the platform suites run.

**Ruled and DELIVERED today (do not re-raise):** demo-admin-password=b · f5-login-limiter-bypass=wait ·
f5-demo-exposure-probe=probe · f5-disclosure-timing=withfix · f5-demo-interim-mitigation=letitland ·
attio-renewal-date-vs-attr-cap=one-field · attio-entra-consent-m365=scopes-first.

**Ruled and STILL UNDELIVERED (older):** `launcher-turn-end-line` => approve (2026-08-24, **14 days**;
Wednesday's half = hand the exact line to each project, queued to ride the next %137 mail; Kam's half =
paste it into the shared scaffold) · `secuura-ci-billing` · `secuura-agent-github-identity` ·
`secuura-dependabot-triage` · `secuura-ks229-disclosure-mailbox` · `secuura-ps-759-760-merge-owner`.

## WHAT WEDNESDAY OWES, IN ORDER
1. **Both tier-1 verdicts** (#884, #885) → rule, score, then #884's merge goes to Kam WITH the
   disclosure draft, since his ruling ties them together.
2. **s143's #876 round 1** + its answer to the breadth question (should the F-6 exemption exist at all
   — Wednesday's lean is an allow-list or a fail-closed inversion over a fourth narrowing).
3. **s10's scopes report** → becomes the body of a card to Kam. **And its ATTIO dry-run diff — do not
   let it write until Wednesday has read it.**
4. Hand the exact approved turn-end wording to %137 and %140.

## TWO WEDNESDAY ERRORS TODAY, both owned in the artefacts
- **The #882 TIER-1 rating was Wednesday's and measurement broke it** (ledger w=145). KS-616 is a
  different limiter, already remediated, and the endpoint has zero consumers. Withdrawn to the
  measurement's scope; the defect, the fix and the pass all stand.
- **"Re-price KS-946 to Blocker" was unexecutable** — no such field; it is already Urgent. A severity
  word relayed without checking the board had somewhere to put it. Withdrawn.
Both are the same axis: **a rating is a claim about the product and goes to the gate like any other.**

## STANDING NOTES
Env does NOT persist across Bash calls — `set -a; . .env` in the SAME command. **No `cd`** (hook
refuses). Tap ≤200 chars or it is refused. **Verify a sent mail's BODY by the `preview` field being
non-null** — `text` is 0 in a LIST response for every message, and a subject-only mail passed both
delivery checks this morning (`send_brief` now refuses a body under 40 non-space chars). Never delete
— quarantine. New work = new branch; **push nothing to a branch under gate.**
