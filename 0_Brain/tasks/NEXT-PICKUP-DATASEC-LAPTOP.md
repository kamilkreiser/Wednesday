---
date: 2026-09-08
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced WHOLESALE at ~02:00 by the 00:21 seat, at the 50% checkpoint
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, ~02:00 Tuesday 2026-09-08. KAM IS ASLEEP. NOTHING NEEDS HIM TONIGHT. THE QUEUE IS EMPTY.

**Run `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` before writing
anything — read EVERY line.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%; 70% is a checkpoint only.**
**QUIET HOURS 23:00–06:00: no voice.** **His last panel input was 21:00 on 09-07.** Nothing since.

## 🔴 FIRST ACTION — there is nothing in flight. Verify that, then decide what the morning needs.
    %17  Datasec/NexusAI — S46. Filing four tickets, then WRAPPING (permission given explicitly).
                            At 50% ctx with a bounded task — it should NOT rotate; wrap is the boundary.
    All gate panes CLOSED: %18, %19, %20, %21. Each `listeners 13 → 13` on close.
**If S46 has wrapped: the Datasec queue is genuinely empty and everything left is Kam's or filed.**
Do not invent work. Do not launch a builder to fill the silence.

## ✅ WHAT THIS SEAT DID — both NexusAI lineages closed, nothing merged, nothing deployed
    rd-374-f2-guard-coverage-s46   10ddb0a   ACCEPTED. Completion check PASSED on all five. Closed.
    rd-323-scheduler-failure-...   e032c7d   GO-with-findings, RECORD-LEVEL ONLY. Closed.
    rd-361-round4-s45              731aa6e   GO-with-findings stands, unmoved
    rd-148-round2-s45              690bed9   GO-with-findings stands, unmoved (cleanest)
    rd-322-root-guard-vacuity-s45  432617a   GO stands — FROZEN, only unqualified GO in the set
    main                           a9a8cb6   frozen, RD-367, **250 behind** (the gate measured it; "~251" was wrong)

**Five QA gates commissioned tonight, all returned, all scored 1.0.** Three new tracked launchers
with ancestor + range guards (`launch_qa_nexusai_rd323_delta.sh`, `..._rd374_r2.sh`, `..._rd323_r2.sh`),
each exercised pass + ≥3 distinct refusals before arming.

**Board residue, all filed, none of it tonight's work:** RD-376 (stripper across nine guards) ·
RD-377 (`P2-unknown-status`, **R2-1 folded in with its caveat leading**) · RD-378 (three alias shapes)
· R2-2/R2-3/R2-4.

## 🔴 THE TERMINATING RULE — it is the reason tonight ended instead of continuing. Keep it.
Three gate rounds per lineage is where this was heading. The rule, set BEFORE each verdict:
- **a clean GO ends the lineage;**
- **a GO-with-findings that is RECORD-LEVEL ONLY also ends it — ticket, do not fix;**
- **only a finding wrong in the CODE — a wrong product behaviour, or A CELL THAT CANNOT FAIL — earns another round.**
**It fired in BOTH directions tonight**, which is what makes it a rule rather than an excuse: RD-374's
F-3 earned a round (three deletions each left 37/37 green — a cell that could not fail); RD-323's R2-1
earned a ticket (every new cell reddens under a mutation aimed at it).
**Why it is necessary and not fastidious:** *a docblock promise with no cell behind it* is
**self-similar** — closing it at layer N creates an instance at layer N+1, inside the test written to
close it. Both lineages did exactly that. **Without a terminating rule this class never ends and every
night looks like progress.**

## 🔴 TWO OF WEDNESDAY'S OWN ENDORSEMENTS WERE FALSIFIED BY THE GATE — read this before ratifying anything
1. **The w=88 rule, broken in its exact named form.** Ruling `escalates()` KEPT, Wednesday told s46
   the deciding reason was *"the vocabulary is enumerated by driving `_classify`… it removes the
   mechanism that produced RD-377's gap."* **M6 added a real fifth verdict: 2175/2175 GREEN, test
   unedited, and the verdict silently joined the escalation set.** The strings are derived (drift
   caught, real); the four probe **inputs** are hand-listed. **The KEEP ruling STANDS** — its
   load-bearing half is the RD-347 design argument, which is ratifiable, and the refactor measured
   behaviourally identical (0 disagreements). **What was wrong was Wednesday's reason, stated as
   settled.** The sharp part: **the brief sent to the gate asked it to "verify that is what the code
   does, not what the comment says", while the ruling mail to the builder asserted it as fact.** Two
   artefacts, one claim, one hour, two epistemic statuses — and the agent reads the mail as authority.
2. **Wednesday praised an env-leak proof that was vacuous.** M9: deleting the `process.env` restore
   leaves the pairing 26/26 green; jest isolates env per test file. *Control the instrument before
   believing the green* — **the rule Wednesday had put in the QA charter one hour earlier.**
**Both retracted to s46 at the HEAD of the closing mail, scoped to exactly what M6 and M9 tested.**
**Candidate standing rule (ledger, OPEN):** when a claim is going to a gate, the mail to the builder
says so **in the same breath** — *"I ratify the DESIGN; whether the vocabulary is really derived is the
gate's question, not mine."* Enforcement candidate at w=4 in the ledger row.

## 🟢 ADOPTED INTO THE QA CHARTER §6 TONIGHT — client-neutral, so every future gate carries them
Backups `.pre-0908-count-the-cause` and `.pre-0908-green-and-noop` beside the file.
1. **"Count the CAUSE, never the damage"** — a census taken with a broken instrument is silent about
   precisely what the breakage hides.
2. **"Read why a GREEN is green, not only why a RED is red"** — a mutation script with a syntax error
   printed 37/37; that green was the *unmutated* file. Assert the tamper landed before believing a run.
3. **"A silent no-op on an explicit request is a defect"** — an edit script used `if old in s:` where
   its siblings used `assert old in s`; the replacement silently did nothing and **two independent
   readers then reported the omission as a deliberate choice.** Every scripted edit asserts its anchor.
All three came from the builder, not from Wednesday. **Credit them on the scoreboard, keep rewarding it.**

## 🔴 KAM'S DESK — five open cards, every one with a safe default
**THE TWO CLICKS still gate all three merges.** Step-by-step was delivered to his panel at
**19:59:38 on 09-07** — **do not re-send it, he has it.**
1. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/environments` — required reviewer on `demo`?
2. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/variables/actions` — `CI_DEPLOY_ENABLED` present, and its value?
**Switch ON + `demo` with NO required reviewer → HOLD the merges.** Otherwise they go on his existing
week-scoped authority.
Cards: `wed-ledger-archive-has-no-trigger` (WED, **this seat's**, rec `trigger`) ·
`hpsm-credential-bearing-prd-outside-every-snapshot` (Datasec, **this seat's**) ·
`vault-add-a-stages-another-clients-files` (Fleet/workspace) · two Secuura ones that are **not yours**.

## 🔴 THE LEDGER — read less than the boot prompt says, and say so
`_ledger.md` **398,606 B / 206 rows** vs the by-tier digest **293,380 B**; both whole is ~167 K.
**Digest WHOLE, ledger as row HEADLINES only.** 09-05's 38 rows are archive-eligible under rule 3c
right now and were **NOT moved** — `_ledger.md` is the Studio seat's this session, and two seats
racing a shared file nearly deleted four of Kam's rulings on 09-07.
**This seat's rows go to `_ledger_laptop_datasec.md` — 32 rows now.**

## 🟡 THE IDLE-ACK DECAYS — cause measured, fix is a supervised one-liner for daylight
The ack hashes `capture-pane | grep -v '^$' | tail -20`, which on a quiet pane **includes the
statusline**; `renews:5d Nh` ticks, so **the ack cannot outlive it** and the quieter the pane the more
of the window is chrome. **A check that cannot SUCCEED.** Fix specified in the 09-07 note: hash a
chrome-stripped tail, and **do NOT touch `wake_watch`'s own `h`**, which the frozen-busy leg needs.
**Not done tonight, deliberately** — the 22:26 predecessor refused a third unsupervised watcher
iteration and nothing new bears on that risk.

## ⚠️ TRAPS — all live, and three of them fired on this seat tonight
0. **`C-u` does not clear a rendered suggestion.** Close a wrapped pane; never clear the line.
0b. **Three ghosts tonight, and the third is a NEW salience source.** One proposed what Wednesday
   intended anyway; one proposed **the option Wednesday had just explicitly REJECTED** (file F-3 as a
   ticket, minutes after ruling FIX). **Rung 6's recorded sources are a Kam-held decision or a decision
   routed UPWARD. Neither applied.** The new source: **weighing two named alternatives makes the LOSER
   maximally salient.** Deliberation is a generator prompt, not only escalation. Detector FIRST, always.
1. **Read the inbox at limit ≥3, never 1.** Twice tonight a real inbound sat **12–26 seconds beneath
   Wednesday's own outbound echo** — listing only the newest showed the echo and hid the gate's verdict.
   **The builder caught the same overlap independently and flagged it.**
2. **`send_brief.sh`'s SELF-CHECK regex is exact:** `SELF-CHECK: re-read end-to-end for contradictions | YYYY-MM-DD HH:MM`.
   Extra prose between the phrase and the `|` breaks it. Specifics go on a `SELF-CHECK NOTES:` line above.
   **And GENERATE the stamp** — this seat typed `01:1x` when `date` said `00:41`.
3. **`pane_close.sh` port args may not discriminate** — this seat passed three ports that read 000
   *before* the close too. **The tool's own `listeners N→N` count is the real control.**
4. **A T9 launch can hit a folder-trust dialog no guard can see** (`Down`, `Enter`). None hit it tonight.
5. **`launchers.conf` points at DevMASTER, unmounted here.** Launch by hand with `tmux split-window`
   then `tmux set-option -p -t <pane> @cockpit_name '<name>'`. **Do not rewrite `launchers.conf`.**
6. **No `cd` in a Bash call**; `git -C $VARIABLE <writeverb>` is refused. Write paths literally.
7. **Another project's checkout is READ-ONLY for git too.** This seat ran read verbs only and never fetched.
8. **A verdict mail can arrive zero-byte** — read the verdict from the report on disk, always.
9. **`decision_queue.sh` uses `--client-project`**, and its prior-ruling gate refusal **is a research
   prompt**: open the artefact the ruling shipped into and read what the fix CHANGED before overriding.
10. **`/Volumes/DevMASTER` is NOT decommissioned** — master drive, other Wednesday's home, merely
   unmounted here. **Prune no worktrees.** A gate called it decommissioned; corrected before it travelled.
11. **Use `2_Project_Files/tools/safe_push.sh` for every push.**

## STANDING
**Kam's week-scoped grants (through Sunday 2026-09-13):** merge on Wednesday's word once the gate
passes · deploy · board judgement calls. **🔴 PRODUCTION LIFT IS SECUURA ONLY — Datasec has NO
production grant.** Ticket creation aggregates (one larger ticket per logical path). Every analysis
record carries **FOUND / TESTED / HOW** with controls named under HOW. **Kill anything querying Azure credits.**

**A GO NAMES A HEAD**, and tonight's two-rule refinement: **a CLEAN GO freezes** (follow-ups on a new
branch cut from it); **a GO-WITH-FINDINGS carries an EXPECTED re-gate** — say so when issuing it and
commission the re-gate as part of accepting the fix, not as a reaction to the head moving.

**NAME THE FRAME.** **The number is read in the same action as the sentence carrying it.** Taps ≤200
chars, pointer only, mail FIRST and verified by a non-null `preview`, THEN tap. **Never delete —
quarantine.** Search before filing, by SYMBOL / PATH / ERROR STRING, **with a control on the zero.**
**Names, not pronouns.**

**TWO WEDNESDAYS LIVE:** Studio owns **Secuura**, this seat owns **Datasec**. One repo, one dashboard,
one chat panel, **ONE USAGE LIMIT** (7d:34% at ~02:00, renews in 5d 2h). **Do not write
`NEXT-PICKUP.md`, the daily note or `_ledger.md`** — the Studio seat's this session. Panel messages
open `[LAPTOP / Datasec]`. **Secuura mail: read the SUBJECT, not the body, and leave it.**
