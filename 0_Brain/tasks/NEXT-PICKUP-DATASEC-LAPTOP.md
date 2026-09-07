---
date: 2026-09-08
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced WHOLESALE at 01:0x by the 00:21 seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, 01:0x Tuesday 2026-09-08. KAM IS ASLEEP. NOTHING NEEDS HIM TONIGHT.

**Run `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` before writing
anything — read EVERY line.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%; 70% is a checkpoint only.**
**QUIET HOURS 23:00–06:00: no voice.** Chat mirror only, and only if something genuinely needs saying.
**His last panel input was 21:00 on 09-07.** Nothing since.

## 🔴 FIRST ACTION — TWO gates live, S46 holding with a dry queue
    %20  QA/NexusAI-RD374-r2 — TIER 2 RE-GATE on 5e6077e..7c10437. LAUNCHED ~01:03, RUNNING.
         (%18 RD-374 r1 and %19 RD-323 delta both REPORTED and their panes are CLOSED.)
    %17  Datasec/NexusAI        — S46. **Queue DRY. Told to HOLD, not wrap** — both gates may return
         findings and they are better landing on a seat that holds the context. Wednesday is its waker.

**When either gate reports: findings → S46; clean GO on BOTH → tell S46 it may wrap.**
Read the verdict from the REPORT ON DISK, never from the mail alone (a verdict mail arrived
zero-byte on 09-07). Report dirs are named in each brief.

## ✅ WHAT THIS SEAT DID — the owed delta gate is now running
The 23:55 handover flagged **one delta owed a gate** and it is now commissioned rather than noted.
`rd-323-scheduler-failure-vocabulary-s45` moved **`99fb518` → `1b6bedb`** because RD-323-F-1's fix
landed WITH the change on Wednesday's instruction — so **no verdict described what would ship.**

- Brief: `2_Project_Files/fleet/qa-agent/briefs/2026-09-08_nexusai-rd323-delta-tier2.md`
- Prompt: `…/2026-09-08_nexusai-rd323-delta-tier2.prompt.txt`
- **Launcher (TRACKED, not in the gitignored `state/` drawer):**
  `2_Project_Files/fleet/launch_qa_nexusai_rd323_delta.sh` — run `--check` to re-verify its guards.
- Report expected under `projects/nexusai/reports/2026-09-08-rd323-delta-tier2/`.

**Guards exercised before arming — pass plus FOUR distinct refusals, each firing for its own reason:**
rc 0 pass · rc 9 head not on origin · rc 10 base not an ancestor · rc 11 range wider than one commit ·
rc 6 prompt missing the thinking directive. The ancestor and range guards are new on this wrapper:
they make "the delta is the subject" a property of the tree rather than a sentence in the brief.

**The three questions the brief points the gate at** (so you can read its verdict against them):
1. **THE FRAME.** The commit claims `p1` "is read in exactly two places… checked rather than assumed" —
   a completeness claim with no frame on it, and everything rests on it. Re-derivation demanded, frame
   to be named, with `getHealthSnapshot`, the alert-email path, API/dashboard surfaces and the
   **frontend** called out as where a `backend/` grep does not reach.
2. **THE CARVE-OUT IS A STRING EQUALITY** — `filter(r => r.verdict !== 'P1-degraded')` excludes exactly
   one literal. Every `P1-*` verdict the class can emit must be enumerated from the class, not the tests.
3. **A DOCBLOCK PROMISE THAT MAY HAVE NO CELL.** The docblock says a degraded target "still triggers the
   alert email". The new cell asserts the audit row; **Wednesday could not find an alert-email
   assertion** — and the brief explicitly tells the gate to report that Wednesday was wrong if Wednesday
   was wrong.

**Calibration note carried into the brief:** S46 did the stronger thing than it was asked. Told to
rewrite an assertion against a shape `runOnce` emits, it stopped writing a shape at all — the cell now
drives the real `runOnce` against a real local stub into the real `_failed`, plus a negative control
(unreachable target, same instrument, opposite answer) so the carve-out must NARROW the verdict, not
remove it.

## 🔴 KAM'S DESK — the two clicks still gate everything, plus one new card
**THE TWO CLICKS, unchanged and still the only thing that matters.** Step-by-step was delivered to his
panel at **19:59:38 on 09-07**, one minute after he asked for it — **do not re-send it**, he has it.
1. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/environments` — required reviewer on `demo`?
2. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/variables/actions` — does `CI_DEPLOY_ENABLED` exist, and its value?
**Switch ON + `demo` with NO required reviewer → HOLD the merges.** Any other combination → the merges
go on his existing week-scoped authority.

**NEW CARD filed by this seat — `wed-ledger-archive-has-no-trigger` (WED), rec `trigger`, default =
nothing moves.** Not a re-raise of his 09-04 cadence ruling; the prior-ruling gate refused it and the
override reason is a measurement in the BLUF. His 09-04 card set a CADENCE and a PLACE (CLAUDE.md 3c,
under "Session end") and is **silent about what fires it**. Measured three ways: `wednesday_rotate.sh`
has no ledger/archive/wrap step at all, `doctor.sh` has no ledger check, and the launcher only tells
seats to READ it. **A rotating seat never runs the session-end ritual, so 3c fires approximately never**
— which is why the file outgrew its cadence, and it is not about the row rate. Recommendation is split
deliberately: the **trigger** is the defect (a doctor warning), the **cadence** stays his.

## 🔴 THE LEDGER, AND WHY THIS SEAT READ LESS THAN THE BOOT PROMPT SAYS
**Measured in the boot action:** `_ledger.md` **398,606 B / 206 rows**; the by-tier digest **293,380 B**.
Reading both whole is ~167 K against the window. This seat did what the 09-07 seat did and says so:
**digest WHOLE (118 lessons), ledger as row HEADLINES only.** Rows dated **2026-09-05 (38 rows,
58,508 B) are archive-eligible under 3c as written, right now** — **NOT moved by this seat**, because
`_ledger.md` is the Studio seat's this session and two seats racing a shared file nearly deleted four
of Kam's rulings on 09-07. Ledger rows for this seat go to **`_ledger_laptop_datasec.md`** (29 rows).

## 🟡 THE IDLE-ACK DECAYS, AND THE CAUSE IS NOW MEASURED — one-line fix, SUPERVISED, morning only
`wake_ack.sh %17` was set at ~00:47 and the idle wake **re-fired within ~3 minutes, twice**, on a pane
whose substantive output is byte-identical. **Cause, measured not guessed:** the ack hashes
`capture-pane | grep -v '^$' | tail -20`, and on a quiet pane that window **includes the statusline** —
`… ctx:28% | 7d:32% renews:5d 3h`. **The `renews:` field ticks, so the ack cannot outlive it**, and the
quieter the pane the more of the hashed window is chrome. It is a check that cannot SUCCEED.
**NOT fixed tonight, deliberately:** the 22:26 predecessor recorded at 23:28 that it refused a third
unsupervised watcher iteration, same watcher, same night. The refinement is already specified in the
09-07 note — **hash a chrome-stripped tail, and do NOT touch `wake_watch`'s own `h`, which the
frozen-busy leg needs to change to detect liveness.** Do it supervised, in daylight.
**Until then: expect an idle wake on `%17` every ~3 min. It is not S46 asking for anything.**

## HEAD TABLE — read from S46's 00:10 fetch by this seat, NOT re-fetched by Wednesday
    rd-374-f2-guard-coverage-s46             5e6077e   AT THE TIER-2 GATE (%18)
    rd-323-scheduler-failure-vocabulary-s45  1b6bedb   AT THE TIER-2 DELTA GATE (%19)
    rd-361-round4-s45                        731aa6e   GO-with-findings stands
    rd-148-round2-s45                        690bed9   GO-with-findings stands (cleanest of the set)
    rd-322-root-guard-vacuity-s45            432617a   GO stands — merge-ready, FROZEN
    main                                     a9a8cb6   frozen, RD-367, ~251 behind
**A GO NAMES A HEAD.** The moment a head moves its GO stops describing what would ship — that is the
whole reason %19 exists tonight. Say it in the same breath as any push.
**RD-322 @ `432617a` is FROZEN**: it is the only unqualified GO in the set, and RD-375's polish goes on
a NEW branch cut from it, never onto it. S46 holds this rule and reached it independently.

## ⚠️ TRAPS — carried forward, all still live
0. **`C-u` DOES NOT CLEAR A RENDERED SUGGESTION.** A ghost line is DISPLAY text. What displaces it is
   real input: the pointer tap. Order: mail → verify at destination → tap → re-run the detector.
   On a WRAPPED pane there is no tap to send, so **close the pane** rather than clear it.
0b. **NINE GHOSTS on 09-07, and the ninth was the dangerous one because it looked RIGHT** — *"land
   RD-375 on RD-322 before merge."* Real ticket, real findings, ordinarily sound, and wrong for one
   reason visible only from the coordinator's seat. Run
   `2_Project_Files/fleet/cockpit/pane_prompt_check.sh <%ID>` FIRST, every time.
1. **A T9 launch can hit a FOLDER-TRUST DIALOG no guard can see** — `No, exit` preselected. Only
   reading the pane catches it. Answer `Down` then `Enter`. **%19's launch did NOT hit it** (checked).
2. **`launchers.conf` points at DevMASTER, unmounted here.** Launch by hand:
   `tmux split-window -t <pane> -v -P -F '#{pane_id}' "bash '<launcher>'"` then
   `tmux set-option -p -t <newpane> @cockpit_name '<Client/Project>'` or `cockpit.sh say` cannot find it.
   **Do not rewrite `launchers.conf`** — it is shared and correct for the Studio.
3. **`send_brief.sh` has three gates:** a literal `PROVENANCE:` line (not `## PROVENANCE`); absolute
   paths or a named owner in every citation; and the heading `RULED BY KAM, NOT YET IN AN ARTEFACT`.
4. **No `cd` in a Bash call** (the hook refuses the whole call). A wrapper needing `cd` is written with
   the **Write tool**. **`git -C $VARIABLE <writeverb>` is refused** — write git paths literally.
5. **Another project's checkout is READ-ONLY for git too.** `rev-parse`, `diff`, `log`, `ls-remote`,
   `merge-base`, `show` are READ. `fetch`, `pull`, `merge-tree --write-tree`, `worktree add` WRITE.
   This seat ran read verbs only and did **not** fetch — the 00:10 fetch was S46's.
6. **Use `2_Project_Files/tools/safe_push.sh "<msg>" [paths…]` for every push.**
7. **A verdict mail can arrive with a ZERO-BYTE body.** The QA agent does not send through
   `send_brief.sh`, so its 40-char floor does not protect it. **Read the verdict from the report on disk.**
8. **`decision_queue.sh add` has `--client-project`, NOT `--project`**, and its prior-ruling gate will
   refuse a subject Kam has written on. **A refusal is a research prompt** — open the artefact his
   ruling shipped into and read what the fix CHANGED before overriding.

## STANDING
**Kam's week-scoped grants (through Sunday 2026-09-13):** merge on Wednesday's word once the gate
passes · deploy · board judgement calls. **🔴 THE PRODUCTION LIFT IS SECUURA ONLY** — lifted 12:07,
**narrowed 12:10 to *"Only secure"*. Datasec has NO production grant.** Ticket creation aggregates
(one larger ticket per logical path, 13:23). Every analysis record carries **FOUND / TESTED / HOW**
with the controls named under HOW (18:56:36). **Kill anything querying Azure credits** (13:06).

**NAME THE FRAME** in any completeness claim. **The number is read in the same action as the sentence
that carries it.** Taps ≤200 chars, pointer only, mail FIRST and verified, THEN tap. `<<'EOF'` or the
Write tool for every body. **Never delete — quarantine.** Search before you file, by SYMBOL / PATH /
ERROR STRING. **Names, not pronouns.**

**TWO WEDNESDAYS LIVE:** Studio owns **Secuura**, this seat owns **Datasec**. One repo, one dashboard,
one chat panel, **ONE USAGE LIMIT** (7d:32% at this boot, renews in 5d 3h). **Do not write
`NEXT-PICKUP.md`, the daily note or `_ledger.md`** — the Studio seat's this session. Panel messages
open `[LAPTOP / Datasec]`. **Secuura mail in the shared inbox: read the SUBJECT, not the body, and
leave it.**
