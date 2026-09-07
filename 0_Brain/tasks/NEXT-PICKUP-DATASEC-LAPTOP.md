---
date: 2026-09-07
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced WHOLESALE at ~23:55 by the 19:51 seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, ~23:55 Monday 2026-09-07. KAM IS ASLEEP. NOTHING NEEDS HIM TONIGHT.

**Run `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` before writing
anything — read EVERY line.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%; 70% is a checkpoint only.**
**QUIET HOURS 23:00–06:00: no voice.** Chat mirror only, and only if something genuinely needs saying.

## 🔴 FIRST ACTION — one gate live, S46 holding with a DRY queue
    %18  QA/NexusAI-RD374 — tier 2 on rd-374-f2-guard-coverage-s46 @ 5e6077e. RUNNING, not yet reported.
    %17  Datasec/NexusAI  — S46. **Queue DRY. Told to HOLD, not wrap** — the RD-374 gate may return
         findings and they are better landing on a seat that holds the context.
**When RD-374 reports: findings → S46; clean GO → tell S46 it may wrap.**

**🔴 ONE DELTA IS OWED A GATE:** `rd-323-scheduler-failure-vocabulary-s45` moved **`99fb518` →
`1b6bedb`** (RD-323-F-1 landed WITH the change, on Wednesday's instruction, so the staleness is
Wednesday's to carry). **The GO-with-findings was on `99fb518`.** Queue a tier-2 pass on
`99fb518..1b6bedb`. **PASS 2173/2173** claimed; RD-323 evidence comment 37276.

**HEAD TABLE — three unmoved, and S46 said so explicitly rather than leaving it to be checked:**

    rd-374-f2-guard-coverage-s46             5e6077e   AT THE TIER-2 GATE NOW
    rd-323-scheduler-failure-vocabulary-s45  1b6bedb   GO was 99fb518 -> DELTA OWED A GATE
    rd-361-round4-s45                        731aa6e   GO-with-findings stands
    rd-148-round2-s45                        690bed9   GO-with-findings stands  (cleanest of the set)
    rd-322-root-guard-vacuity-s45            432617a   GO stands — merge-ready

## 🟢 A KEEPER FROM S46 — adopt it in every QA and builder brief
Told to *"rewrite the assertion against a shape `runOnce` actually emits"*, it did something stronger:
**it stopped writing a shape at all.** The certifying cell now drives the **real** `runOnce` against a
**real** local target and feeds whatever comes out into the **real** `_failed`. Its words:
> *"A hand-written shape cannot notice it is impossible; a driven one cannot be written for a state the
> product cannot reach."*
**Wednesday's instruction would have fixed the instance and left the next hand-written fixture free to
assert another unreachable state. This removes the category.** Same move as red-proofing against the
real `server.js` instead of an in-cell copy. **Standing line from now on.**

## 🔴 AND THE OTHER KEEPER — a red is not a detection until you have read WHY it is red
S46 got **two of its own red-proofs wrong** and self-caught both — **not the fixes, the EVIDENCE for
the fixes.** (1) payloads spliced at arbitrary line numbers landed mid-expression, the parser threw,
the cell reddened: **a parse error dressed as a detection**, including the arm proving the `https://`
case. (2) an hour later its Dockerfile arms failed on a **pre-existing** reason because `shipsTests()`
returns the first reason it finds. Both redone — at acorn-derived statement positions, and against a
minimal base. **Its framing:** *S45's §0 says the artefact you are fixing is the one you stop checking;
mine was the artefact I was PROVING WITH.* **The RD-374 gate has been pointed at those corrections
first, at S46's own request.**

**AND THE FINDING UNDER THE FINDING:** `stripComments()` existed **TWICE** — the named helper (3 call
sites) **and an unnamed inline copy of the identical regexes inside `serverCode()`** (5 more).
**A grep for the helper's name finds half of it.** Total damage re-measured: **33,106 characters over
1,073 lines.** The frame family again, one level down.

**✅ RD-322 @ `432617a` → GO** (merge-ready as it stands). **✅ RD-323 @ `99fb518` → GO-with-findings**
(1 Major, 2 Minor, 2 Polish). Report:
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd322-rd323-tier2/report.md`

**🔴 RD-323-F-1 (Major) — the THIRD check-that-cannot-fail tonight, inside the change built to stop
that family.** `healthSweeper.runOnce` sets `p1 = p1s.length` filtering `verdict.startsWith('P1')`,
**which includes `'P1-degraded'` — so `p1 >= degraded`, always** — and the override fails the tick on
it, **four lines below its own comment promising `degraded` is deliberately NOT failure.** Measured on
the shipped class with a real stub. **And the cell certifying the carve-out asserts
`f({degraded:1, p1:0}) === false` — a shape `runOnce` cannot produce.** Land the fix **WITH** the
change, not behind it: a few lines in one method plus one rewritten assertion.

**RD-322's judgement call is RATIFIED** — the gate verified both grounds itself across the **whole
`.github` tree** (5 workflows, 6 `runs-on` all `ubuntu-latest`, zero `container:`, zero matrix legs,
zero self-hosted, Dockerfile user `node`, no git hooks). **No workflow runs as root; RED-over-skip
stands.** It also added an arm the ticket lacked (delete the record so `blocked` goes true for the
WRONG reason — the cell still reddens): **narrow, not vacuous.**

S45 handed over at 23:03 and its pane is closed
(`HANDOVER-S45.md` at the NexusAI **project root**, outside the repo — its **§0** is the best thing in
it and sits above the branch table deliberately).

## 🔴 KAM'S DESK — FOUR open cards, all default-safe. The two clicks are the only thing that matters.
His last input was **21:00** (`deadlock`, actioned and delivered). **Nothing since.**

**THE TWO CLICKS, and they gate more than they look like they do:**
1. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/environments` — is there a
   **required reviewer** on the `demo` environment?
2. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/variables/actions` — does
   **`CI_DEPLOY_ENABLED`** exist, and what is its value?
**If the switch is ON and `demo` has NO required reviewer → HOLD the merges** (a merge to `main` then
deploys to the demo with nobody in the loop). Any other combination → the merges go on his existing
week-scoped authority. Repo confirmed from the git remote, not composed.
**The chain, measured link by link:** NexusAI releases through `main` → `main` frozen since 09-01 and
**251** behind → he ruled `mergeup` at 18:58 → blocked → **46 tickets in Release Ready** (counted via
`board_count.sh`, which certified it a real total, not a cap). Those are the *"tested but not
deployed"* items he pointed at on 13:40.

**Cards (2 Wednesday's, 2 the Studio's):** `vault-add-a-stages-another-clients-files` ·
`hpsm-credential-bearing-prd-outside-every-snapshot` · plus two Secuura ones that are **not yours**.

## FOUR BRANCHES — none merged, and TWO have GOs on commits that are no longer their heads
    rd-361-round4-s45   GO@f93730c   HEAD 731aa6e   GO-with-findings @731aa6e too (moved-heads gate)
    rd-148-round2-s45   GO@ea4d229   HEAD 690bed9   GO-with-findings @690bed9 — the cleaner of the two
    rd-322-root-guard-vacuity-s45            @ 432617a   -> %15 gating now
    rd-323-scheduler-failure-vocabulary-s45  @ 99fb518   -> %15 gating now
**`690bed9` would ship without reservation. `731aa6e` ships only with G-1 and G-2 ticketed** and this
sentence on the record (the gate's, Wednesday endorsed):
> *No future round may cite the WIRING cells as a completeness claim over `server.js` until
> `stripComments()` is gone.*

## S46'S QUEUE — G-1…G-5, one logical path: the F-2 guard's COVERAGE and its RECORD
Brief: `2_Project_Files/fleet/briefs_staged/2026-09-07_nexusai-s46-g-findings.md`
Gate report (**805 lines — read it, not a summary**):
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-moved-heads-tier2/report.md`

- **G-2 (Major), FIRST — the defect is in the RECORD, not the code.** `stripComments()` was kept for
  the WIRING cells on the reasoning a URL can't hide what they count. **False twice: a URL can, and
  the live damage needs no URL at all** — two prose comments contain `/*` (`server.js:638`, `:1097`),
  each opening a bogus block. **31,845 non-comment chars deleted across 116 ranges; lines 638–713 and
  1097–2062 gone (~1,040 lines).** Byte-identical payload, three placements: outside **RED**, inside
  **GREEN**, URL-on-line **GREEN**. `THE BUG` is a `not.toMatch`, so deleting text makes it **PASS —
  it fails OPEN.** **🔴 DO NOT OVERSTATE:** no deciding site is in a deleted span (all nine at 2349+),
  WIRING patterns count identically today, cells byte-unchanged — **no live defect, not a regression.**
- **G-1 (Major)** the AST census **misses what the regex caught**: `writeFileSync` with a template
  literal, with a string literal, and a spread carrying the key. **T-A8b passes the whole file 33/33;
  its pair T-MB2 (object literal) is RED — the only variable is SERIALISATION.**
- **G-3** `acorn-walk` declared **nowhere** in `package.json` — the guard rests on a transitive dev dep
  of `acorn-globals`. **G-5** "256 computed assignments" reproduces exactly but over a frame **121
  files wider** than the guard it qualifies (239 / 256 / 145) — sound limit, wrong frame, in a docblock
  whose whole purpose is that round 3 died of that. **G-4** the `__tests__` cell CAN fail but its title
  claims a property of the image while its assertion checks a spelling; **its green is luck — it never
  reads `.dockerignore`.**

**S46 reordered the queue by DEPENDENCY rather than severity (G-2 first) and it was right** — doing
G-2 first stops G-1's work landing on a stripper that deletes 1,040 lines. Wednesday took the
correction.

## ✅ DONE TONIGHT
**Security review COMPLETE and the queue is DRY.** Four delta reviews (CypherOneDrive · Teams ·
CommonValueLibraryCypher · Cyphercard-Enrolment) plus an HPSM **scope verdict**. Report:
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review/_Working/delta-review-2026-09/_BATCH2_REPORT.md`
**The June-baseline delta set is COMPLETE at 19/19** — and the agent **corrected Wednesday's census**:
only 19 of the 32 component summaries are June baselines; 13 were written today by this re-run, and
HPSM was scaffolded 2026-08-12, so no June state exists to diff. **What remains is decisions, not
work:** RD-18's Privacy Act package · whether to re-issue the June deliverables against the 219-finding
register · the live cloud pass, still blocked on the tenant question (`fc05dcdd` vs `0c57ab37`).

**RD-361's Blocker is CLOSED** after four rounds and three NO GOs. **RD-148's F-1/F-2/F-3 closed.**
RD-322, RD-323, RD-370, RD-371, RD-372, RD-373 filed or done. **Board 287** (S45 self-corrected its
own 289 double-count).

## ⚠️ TRAPS — the first two FIRED tonight, repeatedly
0. **🔴🔴 `C-u` DOES NOT CLEAR A RENDERED SUGGESTION — measured tonight.** A ghost line is DISPLAY
   text, not typed input, so `send-keys C-u` leaves it exactly where it was (the detector still read it
   afterwards). **What displaces it is real input: the pointer tap.** Order that works: mail → verify
   at destination → **tap** → re-run the detector to confirm `prompt empty`. **This is the concrete
   reason the standing rule says CLOSE a wrapped pane rather than clear it — on a wrapped pane there is
   no tap to send, so closing is the only thing that removes the line.**
0b. **🔴 THE NINTH GHOST WAS THE DANGEROUS ONE, because it was RIGHT-LOOKING.** At S46's prompt:
   *"land RD-375 on RD-322 before merge."* **RD-375 is REAL** (S46 filed it for the RD-322 polish),
   the findings are real, and landing polish before a merge is ordinarily sound. **It is wrong here for
   one reason visible only from the coordinator's seat: `rd-322 @ 432617a` is the ONLY head in the set
   with an unqualified GO, and moving it would cost that verdict for two Polish fixes that block
   nothing.** The other eight proposed work that was merely out of scope; this one proposed work that
   was in scope, sensible, and would have quietly spent the only thing ready to ship.
   **RULE, mailed to S46 and standing: a branch carrying a GO is FROZEN until it merges or Wednesday
   says otherwise. Polish and follow-ups go on a NEW branch cut from the GO'd head. The verdict is the
   asset; the branch is just where it lives.**
1. **🔴 GHOST TEXT NINE TIMES**, eight at wrapped panes, and `good night` **twice at the same NexusAI
   pane** (boot, and again at 23:2x). Others: *"check the Bearer scheme defect in SharePoint, MailFlow
   and UniversalPrint"* (already reviewed, outside the brief) · *"Send Kam a one-paragraph summary"* ·
   *"file a fix-backlog entry for F-B"* · *"file the N-1 ticket details for Wednesday"* · *"file G-1 and
   G-2 as tickets"*. **Run `2_Project_Files/fleet/cockpit/pane_prompt_check.sh <%ID>` FIRST, every
   time, then CLOSE the pane rather than clear the line.** A cleared prompt can be re-populated.
2. **A T9 launch hits a FOLDER-TRUST DIALOG no guard can see** — `No, exit` preselected. Only reading
   the pane catches it. Answer `Down` then `Enter`. (Fired on the Security Review launch tonight.)
3. **`launchers.conf` points at DevMASTER, unmounted here.** Launch by hand with `tmux split-window`,
   then **`tmux set-option -p -t <pane> @cockpit_name '<Client/Project>'`** or `cockpit.sh say` cannot
   find the pane. **Do not rewrite `launchers.conf`** — it is shared and correct for the Studio.
4. **`send_brief.sh` has three gates** and all three fired correctly tonight: a literal `PROVENANCE:`
   line (not `## PROVENANCE`); **absolute** paths or a named owner in every citation; and the heading
   `RULED BY KAM, NOT YET IN AN ARTEFACT` with bullets `- <card-id>: "<ruling>" -> must land in <x>`.
5. **No `cd` in a Bash call.** A wrapper needing `cd` is written with the **Write tool**.
   **`git -C $VARIABLE <writeverb>` is refused** — write git paths literally.
6. **Use `2_Project_Files/tools/safe_push.sh "<msg>" [paths…]` for every push.** It backs up the
   irreplaceable pair, discards the ten regenerated feeds, stages by name, and resolves conflicts by
   each file's own rule — **refusing (rc 22) on any file it has no rule for rather than guessing.**
7. **A verdict mail can arrive with a ZERO-BYTE body** — one did tonight. `send_brief.sh` refuses a
   body under 40 non-space chars, **but the QA agent does not send through it.** **Every gate brief
   must require a report path on disk, and a verdict is read from the report, never the mail alone.**

## STANDING
**Kam's week-scoped grants (through Sunday 2026-09-13):** merge on Wednesday's word once the gate
passes · deploy · board judgement calls. **🔴 THE PRODUCTION LIFT IS SECUURA ONLY** — 12:07 lifted,
**narrowed 12:10 to *"Only secure"*. Datasec has NO production grant.** Ticket creation aggregates
(one larger ticket per logical path, 13:23). Every analysis record carries **FOUND / TESTED / HOW**
with the controls named under HOW (18:56:36). **Kill anything querying Azure credits** (13:06).

**A GO NAMES A HEAD.** The moment a head moves, its GO stops describing what would ship. Two branches
proved it tonight. Say it in the same breath as any push.

**NAME THE FRAME** in any completeness claim. **Three separate findings tonight were frames narrower
than the sentence they supported, and two were Wednesday's own** — a component census widened once and
still wrong, and a Jira comment page sliced by a cap so it "found" three comments older than the one
it wanted. **The number is read in the same action as the sentence that carries it.**

Taps ≤200 chars, pointer only, mail FIRST and verified by non-null `preview`, THEN tap.
`<<'EOF'` or the Write tool for every body. **Never delete — quarantine.** Search before you file, by
SYMBOL / PATH / ERROR STRING.

**TWO WEDNESDAYS LIVE:** Studio owns **Secuura**, this seat owns **Datasec**. One repo, one dashboard,
one chat panel, **ONE USAGE LIMIT**. Do not write `NEXT-PICKUP.md`, the daily note or `_ledger.md` —
hers this session. Panel messages open `[LAPTOP / Datasec]`. Secuura mail in the shared inbox:
**read the subject, not the body, and leave it.**
**She fixed a real bug in `safe_push.sh` tonight** — Wednesday had hardcoded the T9 volume, dead on her
machine; it is self-locating now. **Any new tool gets a self-located root, never a volume.**
