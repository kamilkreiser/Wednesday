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

## 🔴 THE LIVE THREAD — ATTIO MOVES OUT OF DATASEC (Kam, this morning)
**His rulings, verbatim:** 09:12 card `attio-repo-home` => **move**, *"i will set up under kamilkkreiser
but not in datasec"* · 09:18 *"use https://github.com/KamORG454/attic.git. please create deploy keys"* ·
09:28 *"that clears it up but i would still like it to live outside datasec. please instruct everyone."*

**New home `git@github.com:KamORG454/attic.git` — `attic`, NOT `attio`.** Checked, not assumed: attic
= HTTP 200, attio = 404. He pasted an https URL; **deploy keys are SSH**, so the `git@` form or the key
is never used. **Deploy keypair CREATED** at `!CODING/Datasec/ATTIO/3_Access_Keys/attic_deploy_rw`
(600/644; that folder is gitignored, verified). **The public key is with Kam to paste** at
github.com/KamORG454/attic → Deploy keys, **Allow write access ticked.** Nothing pushes until he has.
**Instruction mail SENT to Datasec/Vision (23:2xZ)** — the only seat that touches Attio. **Old
`datasecau/attio` is ARCHIVED NEVER DELETED, and that is Kam's hands (org op).**
**NOT RULED: whether the local folder leaves `!CODING/Datasec/ATTIO`. Default: leave it, move the
remote only. Do not invent this.**

**How it started, and it is Wednesday's failure:** he approved the renewal-date change on its merits
and only later saw the commits had gone to the **Datasec** org. *"Your role is to double-check and do
so."* **Every artefact said WHAT would change; none said WHERE it would land.** Standing line now in
`fleet/specs/brief-standing-lines.md`: **any card, brief or GO whose consequence is a commit NAMES the
remote and branch in its BLUF** (deploys name the environment; tickets name the board).
**Contamination scan at his challenge: ZERO Secuura refs in that push** (control: 48 `attio` hits).
Workspace-wide: Attio in **83 Datasec files, 3 Secuura** — all three session history, one of them a
Secuura agent recording it deliberately did NOT use an Attio finding. **Attio was never mixed with
Secuura; Kam accepted that and wants it out of Datasec anyway.**

## FLEET — one builder (s144, `%142`, standing down to wrap) + two QA panes reporting
| pane | state |
|---|---|
| `%142` Secuura/Blockchain (s144) | told to STAND DOWN and wrap — both its PRs are Kam's now |
| `%143` QA #884 r2 | **REPORTED: GO on the security question** |
| `%144` QA #876 r2 | **REPORTED: GO on the arm, but a REGRESSION survives** |

## PR STATE — heads read together at 09:0x
```
develop 306d0db923183f3b62b053f0242549e37bdf362c   UNMOVED ALL DAY — nothing merged
#884  64e457943  KS-858/F5  r2 GATED -> GO on security. F5 closed on BOTH request forms.
                            AWAITING KAM'S MERGE WORD — and it gates today's client disclosure.
#876  3047bcb1d  KS-930     r2 GATED -> arm CLOSED (7/8 shapes base-blocked -> r1-exempt -> head-blocked)
                            BUT `node-22` spelling still EXEMPT at head, BLOCKED at base = a REGRESSION.
                            Two NO GOs = Kam's cap reached -> CARDED to him.
#885  a98df6b11  KS-949     r1 pushed, NOT re-gated (queued)
#882  7e4603df   KS-698     r1 READY, NEVER GATED — needs a gate, nothing pending on it
#874 #879(stacked on #876) #880 #881 #883 — untouched today
```

## KAM'S DESK — 2 open
1. `secuura-ks930-cap-vs-regression` — **his cap says ship; Wednesday says a regression is not a
   known-gap.** Rec: ONE narrow round 3, regression only. **Wednesday deliberately did NOT apply the
   cap silently** — this is the edge his rule does not cover.
2. `attio-repo-home` => ruled **move** (above) — execution pending his key paste.

## WHAT WEDNESDAY OWES NEXT
1. **#884: put the merge to Kam WITH the disclosure draft** (`5_Project_History/2026-09-07_f5-disclosure-draft-for-kam.md`)
   — his `withfix` ruling ties them; F5 IS LIVE ON THE DEMO (300x, one route measured, GET only).
2. **Gate #882 `7e4603df`** — READY and never gated.
3. Re-gate #885. 4. Score s143, s144, s10 and five QA passes on the scoreboard.
5. **A gate-level finding worth more than any ticket: no pull_request workflow in that repo runs ANY of
   its 26 workspace suites** (from the #884 r2 verdict). Card it to Kam.

## DRIVES — DONE, verified, Kam told
T9 + KK_DEV_Local carry `WEDNESDAY` + `!CODING/Datasec`, one-way additive, `.git`/`qa-worktrees`
excluded. **Final T9 verify: Datasec = 0 items differing.** The last resume moved 1,151,037 files /
12.4 GB. Volume verified clean after an accidental mid-write unplug. **Kam's deletions on the travel
drive were deliberate — "gone on purpose, don't restore." NO bidirectional sync on KK_DEV_Local.**
His profile still has `confirmbigdel = false` — raised twice, his file, his call.

## WEDNESDAY'S ERRORS TODAY — SIX, all owned in the artefacts, all caught
1. #882 TIER-1 rating built on an unread mechanism (w=145). 2. "Re-price KS-946 to Blocker" — no such
field. 3. "Your address is gone from everywhere it is operative" — true of the code, false of the demo
(w=146). 4. "The Datasec copy did not finish" — evidence was a `.git` count the copy excludes (w=2).
5. **The retraction of 4 was ALSO wrong** — a `diff` of ATTIO alone, stated of the whole tree; the
resume then moved 1.15M files. 6. **An approval given without naming its DESTINATION** (Kam-caught).
**Families: 1-3 = a claim about a running thing composed from an artefact. 4-5 = an instrument whose
scope does not match the operation. 6 = the field nobody wrote down at all.**
**Three caught by agents, three by Kam or Wednesday. The catch rate is the system; the RATE is the
thing to watch.**

## STANDING NOTES
No `cd` (hook refuses). Tap ≤200 chars. **Verify a sent mail's BODY by `preview` being non-null.**
**`<<'EOF'` for every brief**, inject live values second. **An instrument carries the SAME exclusions as
the operation it measures.** **Name the destination in anything that causes a commit.** Never delete —
quarantine. Push nothing to a branch under gate.
