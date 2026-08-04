# Delegation monitoring — attending a live delegation (WED-42 v1, cockpit v2)

**v2 cockpit layer (2026-08-04, WED-50 — Kam-approved design):** when
delegations run, prefer launching project sessions as PANES of the tmux
`fleet` session (`2_Project_Files/fleet/cockpit/cockpit.sh add "<Client>/<Project>"
'bash "<launcher>"'`) instead of `open`-ing separate Terminal windows — Kam
watches everything in one iTerm2 window (`tmux -CC attach -t fleet`), and
`monitor.sh` watches every pane (DEATH/STALL/INPUT → alerts.log + spoken tap
on death). Mail remains the durable record; the cockpit is the live layer.
Delegation itself remains PAUSED until the WED-54 pilot review (Kam's
standing constraint).

The ritual for the window between "project session launched" and "wrap email
received". Companion to [[delegation-protocol]] (which governs the brief and
scoring); this file governs *presence*. Design + rejected alternatives:
`1_Project_Definition/Architecture/2026-08-04_seamless-integration-v1.md`.

**The goal in one line:** Kam sees one surface (me). Agents' questions come to
me; only approval/ambiguity/reserved-decision items reach him.

## The loop

1. **Launch** the project's own launcher (`open …/Launch_Claude.command`) after
   the instruction email is at the top of their inbox. Never spawn project
   execution under my own session identity (structural anti-leak — see design
   note, approach b rejected).
2. **Monitor**: run `2_Project_Files/fleet/inbox_digest.sh` on a sleep+check
   cadence — every **3–5 min** while a delegation is live, at natural
   checkpoints otherwise. Anti-eager-polling: never tighter than 2 min; the
   digest is the summaries firewall — do NOT fetch full bodies unless acting
   on that mail (`full <inbox> <message_id>` on demand).
   **NEVER run `mark-seen` mid-monitoring** — it blanket-marks everything new
   at call time and races concurrent arrivals (it swallowed a live QUESTION
   on 08-04, see [[../learnings/2026-08-04_never-blanket-markseen-mid-monitoring]]).
   Baseline use at session start only. Outbound sender-copies are absorbed by
   the loop's own digest cycle; the fire condition ignores `[OUTBOUND]`.
   Any wrap saying "no ANSWER by fallback" → audit the seen-state immediately.
3. **Triage every [QUESTION]** into exactly one of:
   - **ANSWER** — I can resolve it. Compose from: the brief + the target
     project's own tree (read-only) + that client's entry card. **Validate
     before sending** (mental-model rule): any fact naming a file/flag/tenant/
     ticket gets checked against the live source, and the ANSWER cites what was
     checked. Send within one poll cycle where possible.
     **Plan-confirmations are ANSWER-class** (v1.1): check the proposed plan
     line-by-line against the Kam-approved brief — faithful (small additions
     within their own conventions are fine) → confirm, noting any tweaks;
     deviating in scope or containing approval-class actions → ESCALATE that
     part, confirm the rest.
   - **ESCALATE** — approval-class (prod/demo-affecting, money, external comms
     to humans, irreversible), genuine Kam-intent ambiguity, or a decision he
     has reserved. Speak (one-line tap) + text with a recommendation. ONE
     question per turn; queue the rest. Send the agent a holding ANSWER:
     "with Kam; meanwhile do X."
   - **REDIRECT** — belongs to another agent/system: forward with the right
     subject tag, tell the asker who has it.
4. **Cross-client guard, per answer** (checklist, not vibes):
   - Subject client == the client whose materials I used to compose. No other
     client's paths, names, code, or context appear in the body.
   - A mail whose body references a different client than its subject is
     flagged to Kam, never actioned.
5. **Completion oracle**: the Step-2d wrap email ends the loop. On [WRAP]:
   score the delegation (scoreboard), update INDEX.md + entry card, close the
   loop my instruction email opened, log answered-question count + escalation
   count in the daily note (feeds the WED-30 KPI line later).
6. **Silence handling**: if the agent reported BLOCKED and my ANSWER gets no
   wrap or follow-up within ~30 min, check whether their session is alive
   before assuming success — a dead session looks identical to a quiet one.

## Answer mail format

Subject: `[Wednesday -> <Client>/<Project>] ANSWER: <topic>` — topic string
mirrors the question EXACTLY (it is the correlation key).
Body: the answer → the validation line ("checked: <path/board>") → what to do
next ("continue with…" / "pause only if…").

## What this skill is not

- Not a license to do their work: answers guide; edits stay theirs
  (manage-don't-do).
- Not a reason to interrupt my own deep work every 3 minutes when nothing is
  delegated — the tight cadence applies only while a briefed session runs.
- Escalation is not failure. Approval-class traffic SHOULD reach Kam; the test
  of v1 is that *only* that class does.
