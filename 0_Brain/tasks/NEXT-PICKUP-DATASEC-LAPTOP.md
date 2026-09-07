---
date: 2026-09-08
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced WHOLESALE at 01:0x by the 00:21 seat (a partial patch at 01:05 left the head table contradicting the first-action block; this is the wholesale replacement that rule demands)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, 01:0x Tuesday 2026-09-08. KAM IS ASLEEP. NOTHING NEEDS HIM TONIGHT.

**Run `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` before writing
anything — read EVERY line.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%; 70% is a checkpoint only.**
**QUIET HOURS 23:00–06:00: no voice.** Chat mirror only, and only if something genuinely needs saying.
**His last panel input was 21:00 on 09-07.** Nothing since.

## 🔴 FIRST ACTION — one re-gate live, S46 working a five-item queue
    %20  QA/NexusAI-RD374-r2  — TIER 2 RE-GATE on 5e6077e..7c10437. Launched ~01:03. RUNNING.
    %17  Datasec/NexusAI      — S46. **Queue is NOT dry**: four RD-323 delta findings + one ticket,
                                mailed 01:00. Wednesday is its waker.
    (%18 RD-374 r1 and %19 RD-323 delta both REPORTED; both panes CLOSED, listeners 13→13 each.)

**When %20 reports: findings → S46; clean GO → S46 may wrap once its RD-323 queue is also done.**
Read every verdict from the **REPORT ON DISK**, never the mail alone (a verdict mail arrived
zero-byte on 09-07). Report dirs are named in each brief.

## HEAD TABLE — `ls-remote` by this seat at ~01:02, a read verb; Wednesday ran no fetch
    rd-374-f2-guard-coverage-s46             7c10437   AT THE TIER-2 RE-GATE (%20). GO was on 5e6077e.
    rd-323-scheduler-failure-vocabulary-s45  1b6bedb   GO-with-findings (delta gated); 4 items with S46
    rd-361-round4-s45                        731aa6e   GO-with-findings stands — unmoved, verified
    rd-148-round2-s45                        690bed9   GO-with-findings stands (cleanest of the set)
    rd-322-root-guard-vacuity-s45            432617a   GO stands — merge-ready, FROZEN, verified unmoved
    main                                     a9a8cb6   frozen, RD-367, ~251 behind
**A GO NAMES A HEAD.** RD-374's moved twice in one night, which is why two gates ran. Say it in the
same breath as any push. **`rd-322` @ `432617a` stays FROZEN** — the only unqualified GO in the set;
RD-375's polish goes on a NEW branch cut from it, never onto it. S46 holds this rule independently.

## ✅ WHAT THIS SEAT DID
**Three gates commissioned, two returned, one running. Nothing merged, nothing deployed.**

1. **RD-323 delta gate** (the item the 23:55 handover flagged as owed) — `99fb518..1b6bedb`.
   **GO-with-findings: 1 Major, 1 Minor, 2 Polish.** Brief/prompt/launcher:
   `2_Project_Files/fleet/{qa-agent/briefs/2026-09-08_nexusai-rd323-delta-tier2.md,…prompt.txt,launch_qa_nexusai_rd323_delta.sh}`
2. **RD-374 round-1 gate** — `5e6077e`. **GO-with-findings: 1 Major, 3 Minor, 3 Polish.** Routed to S46.
3. **RD-374 round-2 re-gate** — `5e6077e..7c10437`, RUNNING at `%20`. Launcher
   `2_Project_Files/fleet/launch_qa_nexusai_rd374_r2.sh` (TRACKED, not the gitignored `state/` drawer).

**Both new launchers carry ancestor + range guards**, so "the delta is the subject" is a property of
the tree, not a sentence in a brief. **Exercised before arming, five branches each:** rc 0 pass ·
rc 9 head not on origin · rc 10 base not an ancestor · rc 11 range wider than one commit · rc 6
prompt missing the thinking directive.

## 🔴 S46'S CURRENT QUEUE — mailed 01:00, four items + one ticket
Subject: `RD-374 round 2 ACCEPTED … + RD-323 delta GO-with-findings`.
1. **RD-323-D-1 (MAJOR)** — no cell anywhere in the repo asserts the health-sweeper alert email, for
   any verdict. Proved twice: structurally (`emailService → null`, `liveMode → false` in the cell that
   documents it) and mutationally (M3 disabled the degraded alert; **2173/2173 passed**). Major on
   PROXIMITY: `const escalated` sits 28 lines below the guard, so a tidy silently kills a P1 alert.
2. **RD-323-D-2 (Minor)** — `p1` changed meaning under an unchanged key on `/api/admin/health` and the
   persisted audit JSONL. Operators now see `p1: 0` on a sweep that raised a P1.
3. **RD-323-D-3 / D-4 (Polish)** — the sibling arm unreachable by the same criterion; and
   `p1 === unreachable` always now, so **neither new cell can distinguish a correct `escalated` filter
   from one that just returned `unreachable`.**
4. **Second ticket** — `P2-unknown-status` is counted by nothing (probed 4 vs sum 3; no bucket, no
   audit row, no escalation). **Deliberately NOT merged with RD-376** — different logical paths.

## 🔴 TWO RULINGS THIS SEAT MADE — do not re-open without reading them
- **The three stray prose comments: NOT overruled. Leave them.** S46 invited the overrule and gave the
  reason to refuse it: they are product code serving the nine guards in G-2c, and cleaning them here
  proves the change against one file instead of nine. **The cleanup belongs with RD-376.** S46 was told
  to put that on the ticket, not leave it in a mail.
- **S46's refusal of Wednesday's G-1a remedy was ACCEPTED as correct.** Wednesday specified a name
  heuristic (`/^AUTH_ENFORCED/`); S46 implemented binding resolution. **Wednesday's remedy had two
  holes S46 found while proving it** (Q-2 a local `const`, Q-3 a renamed destructure). The `%20`
  re-gate exists partly to confirm which is actually in the file — **S46 said its own control cannot
  discriminate, and asked for the gate.**

## 🔴 KAM'S DESK — the two clicks still gate everything, plus one new card
**THE TWO CLICKS.** Step-by-step was delivered to his panel at **19:59:38 on 09-07**, one minute after
he asked — **do not re-send it, he has it.**
1. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/environments` — required reviewer on `demo`?
2. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/variables/actions` — does `CI_DEPLOY_ENABLED` exist, and its value?
**Switch ON + `demo` with NO required reviewer → HOLD the merges.** Any other combination → merges go
on his existing week-scoped authority.

**NEW CARD — `wed-ledger-archive-has-no-trigger` (WED), rec `trigger`, default = nothing moves.**
Not a re-raise of his 09-04 cadence ruling; the prior-ruling gate refused it and the override reason is
a measurement in the BLUF. His 09-04 card set a CADENCE and a PLACE (CLAUDE.md 3c, under "Session end")
and is **silent about what fires it**. Measured three ways: `wednesday_rotate.sh` has no
ledger/archive/wrap step, `doctor.sh` has no ledger check, the launcher only tells seats to READ it.
**A rotating seat never runs the session-end ritual, so 3c fires approximately never.** The trigger is
the defect; the cadence stays his.

## 🔴 THE LEDGER, AND WHY THIS SEAT READ LESS THAN THE BOOT PROMPT SAYS
**Measured in the boot action:** `_ledger.md` **398,606 B / 206 rows**; the by-tier digest **293,380 B**.
Both whole is ~167 K against the window. **Digest WHOLE (118 lessons), ledger as row HEADLINES only** —
same trade the 09-07 seat made, disclosed the same way. Rows dated **2026-09-05 (38 rows, 58,508 B) are
archive-eligible under 3c as written, right now** — **NOT moved by this seat**: `_ledger.md` is the
Studio seat's this session, and two seats racing a shared file nearly deleted four of Kam's rulings on
09-07. **This seat's ledger rows go to `_ledger_laptop_datasec.md`** (29 rows).

## 🟡 THE IDLE-ACK DECAYS, AND THE CAUSE IS NOW MEASURED — one-line fix, SUPERVISED, morning only
`wake_ack.sh %17` was set and the idle wake **re-fired within ~3 minutes, twice**, on a pane whose
substantive output was byte-identical. **Cause, measured not guessed:** the ack hashes
`capture-pane | grep -v '^$' | tail -20`, and on a quiet pane that window **includes the statusline** —
`… ctx:28% | 7d:32% renews:5d 3h`. **The `renews:` field ticks, so the ack cannot outlive it**; the
quieter the pane, the more of the hashed window is chrome. **A check that cannot SUCCEED.**
**NOT fixed tonight, deliberately:** the 22:26 predecessor recorded at 23:28 that it refused a third
unsupervised watcher iteration — same watcher, same night, and nothing new bears on the risk. The fix
is already specified in the 09-07 note: **hash a chrome-stripped tail, and do NOT touch `wake_watch`'s
own `h`, which the frozen-busy leg needs to change to detect liveness.** Supervised, in daylight.

## 🟢 ADOPTED FLEET-WIDE TONIGHT — S46's formulation, now in the QA charter §6
> **A census taken with the broken instrument is silent about precisely what the breakage hides.
> Count the CAUSE, never the damage.**
Written client-neutrally into `2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` §6 (backup
`.pre-0908-count-the-cause` beside it) so it reaches every future QA invocation rather than living in
one mail. Credited to the Datasec/NexusAI builder on the scoreboard.

## ⚠️ TRAPS — carried forward, all still live
0. **`C-u` DOES NOT CLEAR A RENDERED SUGGESTION.** A ghost line is DISPLAY text. What displaces it is
   real input: the pointer tap. On a WRAPPED pane there is no tap to send — **close the pane.**
0b. **A ghost fired at `%18` tonight and it was the right-looking kind** — *"ticket G-1a and hand the
   fourth-shape repro to the builder"*, i.e. roughly what Wednesday intended to do anyway. Detector
   said SUGGESTION; the decision was taken from the report instead, then the pane was closed. **Run
   `2_Project_Files/fleet/cockpit/pane_prompt_check.sh <%ID>` FIRST, every time.**
1. **A T9 launch can hit a FOLDER-TRUST DIALOG no guard can see** — `No, exit` preselected. Answer
   `Down` then `Enter`. Neither `%19` nor `%20` hit it (both checked).
2. **`launchers.conf` points at DevMASTER, unmounted here.** Launch by hand:
   `tmux split-window -t %17 -v -P -F '#{pane_id}' "bash '<launcher>'"` then
   `tmux set-option -p -t <newpane> @cockpit_name '<name>'`, or `cockpit.sh say` cannot find it.
   **Do not rewrite `launchers.conf`** — shared, and correct for the Studio.
3. **`send_brief.sh` has three gates and ALL THREE fired on this seat tonight, correctly:** a relative
   path in PROVENANCE (w=8 family), then the SELF-CHECK twice. **The SELF-CHECK line must be EXACTLY
   `SELF-CHECK: re-read end-to-end for contradictions | YYYY-MM-DD HH:MM`** — extra prose between the
   phrase and the `|` breaks the regex. Put your specifics on a `SELF-CHECK NOTES:` line above it.
4. **`cockpit.sh say` refuses a tap over 200 chars.** Pointer only, and pass `--mail '<subject>'`.
5. **No `cd` in a Bash call.** A wrapper needing `cd` is written with the **Write tool**.
   **`git -C $VARIABLE <writeverb>` is refused** — write git paths literally.
6. **Another project's checkout is READ-ONLY for git too.** `rev-parse`, `diff`, `log`, `ls-remote`,
   `merge-base`, `rev-list`, `show` are READ. `fetch`, `pull`, `merge-tree --write-tree`,
   `worktree add` WRITE. **This seat ran read verbs only and did not fetch.**
7. **Use `2_Project_Files/tools/safe_push.sh "<msg>" [paths…]` for every push.**
8. **A verdict mail can arrive with a ZERO-BYTE body** — the QA agent does not send through
   `send_brief.sh`, so its 40-char floor does not protect it. **Read the verdict from the report.**
9. **`decision_queue.sh add` has `--client-project`, NOT `--project`**, and its prior-ruling gate will
   refuse a subject Kam has written on. **A refusal is a research prompt** — open the artefact his
   ruling shipped into and read what the fix CHANGED before overriding.
10. **`pane_close.sh` port arguments do not necessarily discriminate.** This seat passed 3000/3001/8080
   and all three read 000 *before* the close too — proving nothing. **The tool's own `listeners N→N`
   count is the real control.** Do not quote the ports as evidence.
11. **The gate called `/Volumes/DevMASTER` "decommissioned" — it is NOT.** It is the master drive and
   the other Wednesday's home, merely unmounted here. **Prune no worktrees**; ~119 stale entries are
   stale *on this machine* only. Corrected to S46 before the phrase could reach a ticket.

## STANDING
**Kam's week-scoped grants (through Sunday 2026-09-13):** merge on Wednesday's word once the gate
passes · deploy · board judgement calls. **🔴 THE PRODUCTION LIFT IS SECUURA ONLY** — lifted 12:07,
**narrowed 12:10 to "Only secure". Datasec has NO production grant.** Ticket creation aggregates (one
larger ticket per logical path, 13:23). Every analysis record carries **FOUND / TESTED / HOW** with the
controls named under HOW (18:56:36). **Kill anything querying Azure credits** (13:06).

**NAME THE FRAME** in any completeness claim. **The number is read in the same action as the sentence
that carries it — and GENERATE timestamps, never type them** (this seat typed `01:1x` into a
SELF-CHECK when `date` said `00:41`). Taps ≤200 chars, pointer only, mail FIRST and verified by a
non-null `preview`, THEN tap. `<<'EOF'` or the Write tool for every body. **Never delete —
quarantine.** Search before you file, by SYMBOL / PATH / ERROR STRING, **with a control on the zero.**
**Names, not pronouns.**

**TWO WEDNESDAYS LIVE:** Studio owns **Secuura**, this seat owns **Datasec**. One repo, one dashboard,
one chat panel, **ONE USAGE LIMIT** (7d:32% at this boot, renews in 5d 3h). **Do not write
`NEXT-PICKUP.md`, the daily note or `_ledger.md`** — the Studio seat's this session. Panel messages
open `[LAPTOP / Datasec]`. **Secuura mail in the shared inbox: read the SUBJECT, not the body, leave it.**
