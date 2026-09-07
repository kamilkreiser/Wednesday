# RD-361 ROUND 4 — Kam ruled `deadlock`. Item 1 is to FALSIFY the premise, not to build on it.

## BLUF
**Kam ruled at 2026-09-07 21:00 on card `nexusai-rd361-round3-blocker-survives`: option `deadlock`
— _"Round 4, but aimed at the DEADLOCK instead of the discriminator."_** Round 4 is authorised, and
it is an extra round on a class Kam had already capped at two, so it is spent deliberately.

**Round 3 was a NO GO. Its Blocker survives and it opened a new Major.** Both instruments reached
that independently: the previous builder (s44) falsified its own fix before the gate reported, and
the tier-1 gate then reproduced the brick end-to-end on a real server with a valid CSRF token.

**🔴 YOUR FIRST ITEM IS NOT A FIX. It is a measurement that could kill this whole round —
and if it does, that is a success, not a failure.**

## WHERE ROUND 3 LEFT IT — the facts you are inheriting, with their instruments
- **F-1 (Blocker, survives).** Round 3 relaxes the gate only while `firstRunComplete` is absent.
  That flag is **also written by the FRONTEND wizard at three sites that have nothing to do with
  authentication** — `static/js/first-run-setup.js:2796` (Log Analytics connection test succeeds),
  `:3069` (data validation passes), `:3494` (the "don't show this guide again" checkbox) — and the
  wizard's tab order (`static/first-run-setup.html:74` vs `:78`) puts **Log Analytics Access BEFORE
  User Access**. So the bricking path is the wizard's ordinary journey. Ticking the checkbox alone
  is sufficient. *Instrument: the gate's 2×2 on a real server, both heads × both variants; and s44's
  own frontend grep, which it ran against its own work.*
- **F-2 (Major, NEW — introduced by round 3).** A deployment that HAD auth enforced, whose
  `settings.json` is emptied with `backups/` and `.emergency-backup/` also unavailable, now serves
  **open mode across all 175 routes** where round 2 denied. That is SEC-01's own direction of
  failure. *Instrument: a before/after table on the same two heads. The gate names its own weakest
  link — it removed the backups by hand and cannot say a real incident would.*
- **F-3 (Minor).** `authEnforcement.js:207-211` describes case B as "left denying". Measured: it
  SERVES, because `initializeFiles()` recreates the file as `{}` first, so case B is unreachable
  through the constructor. **The comment describes behaviour the product does not have.**
- **F-4 (Minor).** s44's *rejection* of its own first candidate was correct and the gate confirmed
  it. Its accompanying claim that the rejected fix "would have been green in the suite" is **false**
  — it turns cell C red. *Caveat: counterfactual.*
- **F-5 (Polish).** Only boolean `true` blocks relaxation; `'true'` and `0` relax.
- **GENUINELY CLOSED, and record it as closed:** F-B / M10 — mutating the sole producer
  (`jsonStorage.js:847`) fails exactly cell D, restore returns 23/23. Proved by contrast, not
  assertion. The single-write-site premise was verified across **all 678 tracked files**
  (`authEnforced` at `server.js:3349` and `:15426` only, each adjacent to `firstRunComplete`).
  2177/2177, 113 suites, 0 skips, reproduced independently.

**Full report and evidence — read it before you touch anything:**
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round3-tier1/report.md`
**Your predecessor's handover:** `HANDOVER-S44.md` at the NexusAI project root (outside the repo).

## ITEM 1 — TEST WEDNESDAY'S INFERENCE. Do not build on it; try to break it.
**Wednesday's reasoning, stated as an inference and NOT a measurement:** by the time the gate reads
`settings.json`, `JsonStorage`'s constructor has already run `initializeFiles()`
(`jsonStorage.js:898`), which normalises a missing / truncated / emptied file to `{}`. So
**"never set up" and "set up then lost" may be byte-identical at the point of decision** — and if
that holds, *no discriminator built on settings.json content can separate them*, which would mean
rounds 2 and 3 were both attempts at something structurally unavailable.

**The gate established the normalisation itself (F-3). It did NOT establish the stronger claim.**

**So item 1 is an enumeration, and it carries this brief's hardest requirement:**
1. **Enumerate every durable signal readable at gate-decision time** — not just `settings.json`.
   The persistence sentinel, `backups/`, `.emergency-backup/`, the data directory's own contents,
   any marker file, file mtimes, anything on the volume.
2. **For each, state whether it differs between the two states**, with the command and the output.
3. **NAME THE FRAME in every sentence.** *"Every signal read by `authStateUnestablished()` **in
   `backend/services/`**"* — never a bare "every signal". The failure family filed tonight
   (`a census complete over a frame that is not`) is exactly what would defeat this item: both
   controls pass, the number is genuinely read from the source, and the source is smaller than the
   question. **This round's central claim is a completeness claim, so the frame IS the finding.**
4. **If a real discriminator DOES exist, say so and STOP.** Mail Wednesday, do not start item 2.
   That outcome changes the round and it is Kam's call, not yours. **Finding that Wednesday is wrong
   is the most valuable thing you can do tonight** — s44 earned its credit doing exactly that.

## ITEM 2 — ONLY IF ITEM 1 CONFIRMS: make the deployment RECOVERABLE, not correctly classified
The shape Kam ruled: let **`POST /api/auth/enforce`** and the **first-run wizard** through the
`AUTH_STATE_UNKNOWN` gate while every other route keeps denying. An interrupted first run then
*finishes* instead of bricking, and nothing has to guess which state it is in. It should also drop
F-2, because no relaxation of the gate's default is needed.

**🔴 THE SECURITY QUESTION THIS RAISES MUST BE ANSWERED BY MEASUREMENT INSIDE THIS ROUND, NEVER
ASSUMED AWAY:** on a deployment that *had* auth enforced and then lost its settings, does an
un-gated `/api/auth/enforce` let an **unauthenticated caller on the network configure auth against
THEIR OWN tenant** and take the deployment over? Round 3's own F-4 analysis establishes that
`authEnforced: true` is reachable with **zero authorised users**, because the route validates the
four Entra settings and not the user list — so this is a live concern, not a hypothetical.
- If the answer is yes, the carve-out **needs a bound** (the persistence sentinel being absent, a
  first-boot window, a one-shot token — your design, with its own red-proof), and you say so.
- **If the measurement shows the carve-out is unsafe, do not build it.** Bring the alternative and
  the measurement to Wednesday. **Wednesday's option on Kam's card is a proposed shape, not a design
  ruling, and it has not been tested by anyone.**

## ITEM 3 — the test cell that codifies the Blocker must not survive this round
Round 3's new cell asserts `DENY_UNKNOWN` for `{ entraTenantId:'x', firstRunComplete:true }` and
labels it `lost`. **That is the surviving Blocker asserted as intended behaviour**, inside the suite
that is supposed to catch it. Whatever round 4 concludes, that cell does not get left asserting the
defect as correct. Fix it, or if item 1 kills the round, correct it anyway and say so — a green
suite that encodes the defect is worse than a red one.

## ITEM 4 — file F-1 … F-5 as ONE ticket (Kam's 13:23 aggregation rule)
*"Rather than creating three or five separate tickets, create one larger ticket … within a logical
path."* One ticket, the five findings as a checklist inside it, `Relates` to RD-361.
**Search the board BEFORE you file** — by SYMBOL, PATH or ERROR STRING, never by your own phrasing
of the problem — and write in the ticket what you searched and what you found:
*"searched `authStateUnestablished`, `firstRunStillInProgress` and `authEnforcement.js`, 0 open
hits."* A control that proves "not mine" is only half the check; the other half is "has someone
already filed this?"

## ITEM 5 — ONLY IF ITEMS 1–4 ARE DONE AND THE GATE IS RUNNING: RD-148 round 2
Queued, not started, deliberately left at a clean boundary by s44. **Round 1 of 2 is spent.** Scope:
F-1 + F-2 together, plus F-3. The fix for F-1 is the file's own pattern — every sibling handler calls
`render()` BEFORE `setStatus()`; `revokeScimToken` is the only inversion, and its `finally { render() }`
wipes the container holding the only `#rd135-status` ~12 ms after the message is written, on every
path including token-still-live. **Do not start this before item 4 is complete.**

## HOLDS — none waived by anything in this brief
- **NO MERGE, NO DEPLOY.** The three gate-passed branches are still blocked: Kam ruled `youcheck`
  on card `rd104-gh-identity-acceptance-false-premise` at 19:58 and **his two answers have not
  arrived yet.** Nothing merges until they do and Wednesday says go.
- **🔴 Datasec has NO production grant.** Kam lifted the production ban at 12:07 and **narrowed it at
  12:10 to *"Only secure"* — Secuura only.** It does not reach NexusAI. Do not read the lift as
  covering anything here.
- **A full TIER-1 gate closes this round.** The carve-out is a NEW mechanism on an auth door, not a
  follow-up to a gated one, so it is tier 1 — not tier 2.
- **Kam authorised round 4 explicitly. Do not assume a round 5.**
- **A precondition stated as a decision rule must name its BLIND outcome and make it the SAFE one.**
  Not "if X then stop else proceed" but **"if you cannot MEASURE X, that is the stop."** Any
  instrument answering a question about a system it may not reach carries a **positive control on
  the instrument itself.** This rule was earned by your predecessor: its `gh` 404s on the repo
  itself, so a 404 on a variable was byte-identical to not-set, and only a positive control revealed
  the blindness.
- **Base every diff on `parent..head` of the branch under test, never on `main`** — `main` is the
  integration branch but is **250 commits behind** (measured by the gate; the 248 in the earlier
  brief was stale). Diffing against it reads other people's merged work as your change.
- **Never delete — quarantine.** Rename into a dated folder and record where it went.
- **Signature classes still pause for Kam:** production, money, external communication to any human,
  anything irreversible.
- **Every analysis record carries FOUND / TESTED / HOW as explicit fields, with the controls named
  under HOW** (Kam's standing instruction, 18:56:36 today).

RULED BY KAM, NOT YET IN AN ARTEFACT

- nexusai-rd361-round3-blocker-survives: "Round 4, but aimed at the DEADLOCK instead of the discriminator (recommended)" -> must land in RD-361 as a comment you write in your FIRST turn, quoting the ruling and naming what round 4 will and will not attempt. Tell Wednesday the comment id and Wednesday marks the card delivered.
- rd104-gh-identity-acceptance-false-premise: "You check the two settings pages yourself - two clicks, links below (recommended)" -> must land in this brief's HOLDS, which it has. Kam's two answers have not arrived; the three merges stay unmerged. Nothing for you to do but respect it.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **Round 3 does not merge** and is not to be recorded anywhere as closing SEC-01's Blocker.
- **RD-362 must not close as "containment achieved"** — its exposure is wider than the ticket
  claims, three separate ways, and RD-369 carries the carrier story.
- **The shared local dev stack is STALE BY DESIGN.** Build your own from the repo's provisioning
  path, or state what a stack built on an old date cannot prove.

PROVENANCE:
- Kam's `deadlock` ruling | /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/dashboard/data/decisions.json card `nexusai-rd361-round3-blocker-survives` ruled_ts 2026-09-07T21:00 - Wednesday's tree, not yours | read 2026-09-07
- Kam's `youcheck` ruling | /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/dashboard/data/decisions.json card `rd104-gh-identity-acceptance-false-premise` ruled_ts 2026-09-07T19:58 - Wednesday's tree, not yours | read 2026-09-07
- Kam's 12:07 production lift narrowed 12:10 to "Only secure" | /Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh output - Wednesday's tree, not yours | read 2026-09-07
- Kam's 13:23 ticket aggregation rule | /Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh output - Wednesday's tree, not yours | read 2026-09-07
- Kam's 18:56:36 found/tested/how instruction | /Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh output - Wednesday's tree, not yours | read 2026-09-07
- F-1 through F-5, the 2x2, the three frontend writers, the tab order | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round3-tier1/report.md sections 2-4, read in full | read 2026-09-07
- 678 tracked files, two authEnforced write sites, 2177/2177 | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round3-tier1/report.md section 5 | read 2026-09-07
- main is 250 behind, not 248 | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round3-tier1/report.md sections 1 and 8 | read 2026-09-07
- RD-148 F-1 cause and the render/setStatus inversion | /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP-DATASEC-LAPTOP.md RD-148 verdict section - Wednesday's tree, not yours | read 2026-09-07
- The blind-outcome rule and its origin | /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP-DATASEC-LAPTOP.md rd104 section - Wednesday's tree, not yours | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 21:10
