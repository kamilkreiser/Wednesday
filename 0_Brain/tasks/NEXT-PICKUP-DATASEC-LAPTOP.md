---
date: 2026-09-08
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced WHOLESALE at 06:2x by the 00:21 seat, at the 65% checkpoint
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, 06:2x Tuesday 2026-09-08. KAM IS AWAKE (greeted by voice 06:13). TWO THINGS ARE LIVE.

**Run `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` before writing
anything — read EVERY line.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%; 70% is a checkpoint only.**
**Quiet hours are OVER — voice is allowed.** Kam's last panel input was 21:00 on 09-07; he has the
morning board on his panel.

## 🔴 FIRST ACTION — verify these two, then read Kam's panel
    %23  QA/NexusAI-RD377  — FULL tier-2 gate on rd-377-verdict-domain-s47 @ fabcc93. Launched 06:17.
    %22  Datasec/NexusAI   — S47. On RD-376 (unblocked 06:19 after holding unnecessarily).
    %0   wednesday         — this seat.
`tmux list-panes -t fleet` before believing this line. **When %23 reports: read the verdict from the
REPORT ON DISK** (`projects/nexusai/reports/2026-09-08-rd377-tier2/`), never the mail alone.

## THE TERMINATING RULE — it governs the RD-377 verdict when it lands
- **clean GO** -> ticket closes;
- **GO-with-findings, RECORD-LEVEL ONLY** -> **ticket the findings, do NOT open a round 2**;
- **only a finding wrong in the CODE** — a wrong product behaviour, or **A CELL THAT CANNOT FAIL** —
  earns another round.
**The gate has been asked to state which of the three it returns.** It fired both ways last night,
which is what makes it a rule rather than an excuse.

## LIVE HEADS — `ls-remote` by this seat overnight + S47's own re-derivation; Wednesday ran no fetch
    rd-377-verdict-domain-s47                fabcc93   AT THE FULL TIER-2 GATE (%23). Base e032c7d.
    rd-323-scheduler-failure-vocabulary-s45  e032c7d   lineage CLOSED, findings ticketed
    rd-374-f2-guard-coverage-s46             10ddb0a   lineage CLOSED, completion check passed
    rd-361-round4-s45                        731aa6e   GO-with-findings stands
    rd-148-round2-s45                        690bed9   GO-with-findings stands; the checkout sits here
    rd-322-root-guard-vacuity-s45            432617a   GO stands — FROZEN, only unqualified GO
    main                                     a9a8cb6   frozen, RD-367, 250 behind
🔴 **rd-377 is STACKED on rd-323** — `e032c7d` must merge before `fabcc93`. **Two merges, two blast
radii; say which one you mean.** Nothing merges until Kam's two clicks.

## 🔴 KAM'S DESK — the two clicks, unchanged, and they gate all three merges
Step-by-step went to his panel **19:59:38 on 09-07** — **do not re-send it.**
1. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/environments` — required reviewer on `demo`?
2. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/variables/actions` — `CI_DEPLOY_ENABLED` present, and its value?
**Switch ON + `demo` with NO required reviewer -> HOLD the merges.** Otherwise they go on his week grant.
**Five cards open, every one with a safe default.** This seat's two: `wed-ledger-archive-has-no-trigger`
(WED) · `hpsm-credential-bearing-prd-outside-every-snapshot` (Datasec). The other three are the
Studio's or Fleet/workspace — **not yours to adopt, re-card or answer.**

## RULINGS THIS SEAT MADE — a successor must not re-litigate these
- **RD-377 is a FULL tier-2 gate** (product code in three schedulers), base `e032c7d`.
- **The two reader widenings land INSIDE RD-377, additively** — a new `unknownStatus` count alongside
  `p1Incidents`/`healthP1s`, **never folded in** (RD-323-D-2: a metric's meaning must not change under
  an unchanged key; RD-130: never inflate an incident count with non-incidents).
- **`P2-unknown-status` gets its own bucket and `ok:false` row, does NOT escalate the tick, does NOT
  join the P1 alert email.** It is a **CONTRACT** problem, not an availability one — *the target
  answered.* Both Wednesday and the gate had been saying "the target vanished"; that overstates it and
  argues for the opposite call.
- **While a gate runs, continue on the next INDEPENDENT item on its own branch.** A pending gate
  freezes its own head, not the seat.
- **RD-376's base is the BUILDER's call**, by smallest conflict surface, measurement stated —
  Wednesday holds no client identity there and will not name a head it cannot measure.
- **The three stray `/*` comments in `server.js` stay untouched** until the X-1/X-2 reproducer is
  captured or `data-dir-single-source.test.js` is converted.
- **The vault step is SKIPPED at every wrap** and the skip is stated in the wrap mail.

## 🟡 THE ATTIO DAILY DIGEST — arrives 07:00, and its headline overstates its own body
`[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` (scheduled, `attio-bridge`, ATTIO-29). It says
**"14 items for today"** and **every flagged row is seeded — 8 `[DEMO]` + 6 `[SYN]`, ZERO real deals**
(counted from the body). All twelve staleness rows read "17d since any change" identically, which is
one seed event rather than twelve facts. **It is excellent about its INSTRUMENTS** (names each
blocker, warns that the not-contacted signal cannot see email/calendar/calls and is really reporting
*records not edited*, blocked on ATTIO-8) **and silent about its POPULATION.**
**Nothing routed to Kam, nothing carded** — its renewal blocker is `attio-attr-cap`, which he **already
ruled `hold` on 2026-08-22**; re-raising it is the going-in-circles he corrected on 09-07.
**TRANSFER ITEM for the next Datasec/ATTIO session** (not Wednesday's code, read-only tracker access):
put the real-deal count in the BLUF — *"14 items, 0 on real deals"* — or filter the seeded prefixes
out of the count. **Brief it as a completion, not a correction; the disclosure discipline is a model.**

## 🔴 THE VAULT — do not run the wrap's vault step from a Datasec seat
`end-of-session.md:50` is `git add -A` and the vault's untracked set includes **Secuura** paths, so
running it here would commit another client's content — **hard rule 2.** Measured by S46, re-measured
by S47. **Carded for Kam** (`vault-add-a-stages-another-clients-files`, default HOLD); shared file, so
it is his. Skip the step, say so in the wrap mail, stage nothing by path.

## WHAT THIS SEAT DID SINCE MIDNIGHT (compressed — details in `_ledger_laptop_datasec.md`, 33 rows)
Both overnight NexusAI lineages closed (RD-374 @ `10ddb0a`, RD-323 @ `e032c7d`), **six gates
commissioned and returned, all scored 1.0**, S46 wrapped with seven tickets, S47 launched 05:39 under
the morning-sweep grant and closed RD-377 to READY by 06:13. **Nothing merged, nothing deployed, at
any point.** Four tracked gate launchers now carry ancestor + range guards, each exercised pass plus
three or more distinct refusals before arming.
**Board:** Release Ready **46** (Wednesday's own count) · open **295 -> 296**, S47's count, reconciling
exactly with S46's 289 plus the six new. **`board_count.sh` cannot count this board — WED-146.**

## 🔴 THREE ERRORS OF WEDNESDAY'S OWN, ALL DISCLOSED AT THE HEAD OF THE NEXT MAIL
1. **Ratified a claim whose truth-maker was in the codebase** (the w=88 rule in its exact named form):
   told S46 the `escalates()` vocabulary was derived and "removes the mechanism that produced RD-377's
   gap". **M6 falsified it.** **The KEEP ruling stands; the REASON was withdrawn.** The sharp part: the
   brief to the gate asked it to verify that very sentence while the mail to the builder asserted it.
2. **Praised a control that could not fail** — S46's env-leak pairing; M9 showed deleting the restore
   left it 26/26 green. *Control the instrument before believing the green.*
3. **Wrote a FALSE claim about its OWN capability into a brief, as a REASON** — "Wednesday holds no
   NexusAI board identity". It holds **read-only** access under Kam's 2026-08-03 grant; the real cause
   was `JIRA_SITE` missing its scheme. **"I lack authority" was the worst available reading.**
   **Standing rule: before writing "I cannot X" into a brief, run X once.**

## 🟢 IN THE QA CHARTER §6 NOW — all three from agents, not from Wednesday
Backups `.pre-0908-count-the-cause` and `.pre-0908-green-and-noop` beside the file.
1. **Count the CAUSE, never the damage.**
2. **Read why a GREEN is green, not only why a RED is red** — assert the tamper LANDED before
   believing any run. Six instances in one night, three on the green side.
3. **A silent no-op on an explicit request is a defect** — every scripted edit asserts its anchor.

## ⚠️ TRAPS — live, and most fired on this seat
1. **Read the inbox at limit >= 3, never 1.** Twice a real inbound sat 12-26s beneath Wednesday's own
   outbound echo; reading only the newest showed the echo and hid a gate verdict.
2. **`send_brief.sh`'s SELF-CHECK regex is exact.** Extra prose before the pipe breaks it — specifics
   go on a `SELF-CHECK NOTES:` line above. **GENERATE the stamp**; this seat typed a wrong one.
3. **`git -C $VARIABLE <writeverb>` is refused** — write paths LITERALLY. **Both Wednesday seats hit
   this independently in one night**, and this seat had written the trap itself hours earlier.
4. **`pane_close.sh` port args may not discriminate** — ports read 000 before the close too. **The
   tool's own `listeners N->N` is the real control.**
5. **Ghosts: five at this project's panes since midnight**, and the two dangerous ones proposed **what
   Wednesday had just decided against** and **what Wednesday was about to rule**. Rung 6's recorded
   salience sources did not apply — **the new source is Wednesday's own live deliberation.** Detector
   FIRST, then CLOSE a wrapped pane.
6. **A T9 launch can hit a folder-trust dialog no guard can see** (`Down`, `Enter`).
7. **`launchers.conf` points at DevMASTER, unmounted here** — launch by hand, then
   `tmux set-option -p -t <pane> @cockpit_name '<name>'`. **Do not rewrite `launchers.conf`.**
8. **Another project's checkout is READ-ONLY for git too.** This seat ran read verbs only, never fetched.
9. **A verdict mail can arrive zero-byte** — read every verdict from the report on disk.
10. **`decision_queue.sh` uses `--client-project`**; a prior-ruling refusal **is a research prompt**.
11. **`/Volumes/DevMASTER` is NOT decommissioned** — unmounted here. **Prune no worktrees.**
12. **NexusAI's `JIRA_SITE` has no scheme** — prefix `https://` or a 301 with an HTML body reads as
    "board unreachable". Filed as RD-382 on their board.
13. **Use `2_Project_Files/tools/safe_push.sh` for every push.**

## STANDING
**Kam's week grants (through Sunday 2026-09-13):** merge on Wednesday's word once the gate passes ·
deploy · board judgement calls. **🔴 PRODUCTION LIFT IS SECUURA ONLY — Datasec has NO production
grant.** Ticket creation aggregates. **FOUND / TESTED / HOW** with controls named under HOW.
**Kill anything querying Azure credits.**
**A clean GO freezes; a GO-with-findings carries an expected re-gate** — commission the re-gate as
part of accepting the fix, not as a reaction to the head moving.
**NAME THE FRAME. The number is read in the same action as the sentence carrying it.** Taps <= 200
chars, pointer only, mail FIRST and verified by a non-null `preview`, THEN tap. **Never delete —
quarantine.** Search before filing by SYMBOL / PATH / ERROR STRING **with a control on the zero.**
**Names, not pronouns.**

**TWO WEDNESDAYS LIVE:** Studio owns **Secuura** (alive — committed 05:30; its s148 wrapped overnight
and that wrap is ITS to handle, subject-only from here). This seat owns **Datasec**. One repo, one
dashboard, one chat panel, **ONE USAGE LIMIT** (7d:34%, renews in 4d 21h). **Do not write
`NEXT-PICKUP.md`, the daily note or `_ledger.md`** — the Studio seat's. Panel messages open
`[LAPTOP / Datasec]`.
