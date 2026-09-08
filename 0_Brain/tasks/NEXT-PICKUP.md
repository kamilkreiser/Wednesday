---
date: 2026-09-08
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Kam ruled the name 11:56). Read Datasec mail by SUBJECT only.
source: replaced WHOLESALE at 16:0x by s153 at its CLOSE
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — s153 CLOSED 16:0x. Kam shut the Studio down to reorganise his desk. Nothing is in flight.

## 🟢 THE FLOOR IS CLEAN — this is a planned shutdown, not an interrupt
Kam, 15:49: *"Rather than me telling you when, how about you tell me when it's ready to shut down?
Let everyone finish their tasks."* Then 15:59: *"Please wrap up and I'll shut down."*
- **s150 (Secuura) WRAPPED and CLOSED** — its own handover names the next ticket.
- **The T9 copy was stopped with a TERM, not yanked** — 0 rsync temp files, 0 writes in the final
  minute, mount idle. **The T9 is unplugged (or about to be) and moves to Tuesday's new machine.**
- **`main` = `dc5b8675`, tree clean, verified against `ls-remote`** — not against a local ref.
- The QA pane was left idle: **the QA agent has NO inbox in `inbox_routing.conf`**, so it cannot be
  mailed at all, only launched with a brief file. Its verdict is delivered and its report is on disk.
  **That gap is real and unfixed — see OWED below.**

## 🟢 SECUURA STATE AT CLOSE
    develop 5c6777658  ·  main 54b2a5c26  ·  next ticket KS-577 (26 remaining in P2 In Review)
**Four merges this seat:** #907 (`27b0ee294`) · #793 (`9806be0ac`) · #895 (`5c6777658`) ·
**#908 to `main` (`54b2a5c26`)** for Kam's `route-to-main` ruling.
- **#895 merged with ZERO approving reviews** — read from the endpoint, stated on the ticket in the
  repo's own language, because that was Kam's explicit exception, not a skipped step.
- **KS-682 is NOT proven until #896's four-slot Playwright sweep runs.** Say so wherever the stream
  is called done.
- **KS-988 closes on an OBSERVATION, not on the merge: look Monday 2026-09-14.** Zero new
  `dependabot[bot]` Action-version PRs = pass; one appearing = the generator does not read `main` and
  the premise needs re-deriving. **The check ships with a control** (the same query without the date
  bound must still return #518/#519/#569–571) and a second discriminator (npm and docker bumps SHOULD
  still appear; their absence is a different defect).
- **KS-365 is HOLD on UPSTREAM ALONE** — postgres:15-alpine digest unchanged, CVE-2025-68121 in
  gosu's vendored stdlib. Nothing we do moves it.

## 🔴 THE FINDING TO CARRY FORWARD — six instances, and one has a number now
Work done and the board not saying so: **#793 · #721 (eight days on nobody) · #768 item 3 · #785
(his own re-review, shown as ours) · KS-566 · and the In Review column itself.**
**Measured: 39 tickets In Review, 20 with NO open PR.** s150 explicitly REFUSED to report that as
"51% overstated" — *not awaiting review is not the same as done* — and named three of the twenty as
legitimately parked, one of which it had placed there itself an hour earlier. **The column is
overstated; the true figure is unknown and must not be guessed.** That bounding is the model to copy.

## 🔴 WITH KAM (all have safe defaults; nothing blocks)
`secuura-ks963-widen-to-preauth` (default: ships as ruled — it DID; KS-999 carries the await fix) ·
`hpsm-credential-bearing-prd-outside-every-snapshot` · `secrev-live-pass-blocked-on-tenant` ·
`nexusai-rd369-round3-or-ship-at-the-cap` — **the last three are TUESDAY's.**
**PS #783 unreadable:** the PAT 404s on the whole `Secuura/platform-s` repo (control run — not a
missing PR). Needs platform-s scope on the token. **Kam's.**

## 🔴 OWED, NOT DONE — inherited and still not discharged
1. ~~**`secuura-ten-cascade-collateral-restore-or-leave`**~~ — **CLOSED 2026-09-08 18:2x, NO CARD
   FILED.** s151 measured it: **7 open tickets, all `Backlog`, four separate archive events, and 7 at
   every window from 2s to 1h** (the total swings 28→93; the open subset does not). **Kam had already
   ruled the class** at 14:00 — `secuura-61-archived-while-still-open` => `three`, unarchive only the
   In Progress — so all seven stay archived and there is nothing to put to him. The three-seat refusal
   to file it from an unprovenanced "ten" is what preserved that outcome. **Residual, commissioned:**
   KS-774 and KS-633 are SECURITY-REVIEW children reading as defects, which his work-state reasoning
   did not consider — cross-reference comments on the live parents KS-489/KS-488 make them findable
   without unarchiving anything, and the seat is confirming all seven fall inside the 61 he ruled on.
2. **The QA agent has no inbox** — `fleet/inbox_routing.conf` has no QA row, so no brief, answer or
   wrap can reach it by mail. File a WED ticket.
3. **Nothing bridges Kam's chat rulings into `decisions.json`.** Four of his rulings today needed
   hand-transcription; this morning six were re-served to him because of it. **Every seat must
   reconcile at boot** — the sweep is `ruled_choice`/`status` on each card against
   `Decision <id>: <key>` in `chat_kam.json`. **Verified clean at close: 0 stranded, 0 key mismatches.**

## 🔴 HOW TO WRITE TO KAM — HE CHANGED IT TWICE TODAY
1. **15:23 — the panel speaks the WHOLE message.** No paragraph split, no cap. Length costs him real
   seconds now. `learnings/2026-09-08_the-panel-reads-the-whole-message`.
2. **15:34 — the ASK GOES FIRST, as literal pasteable steps:** *"I need you to do X. The rationale is
   Y. My recommendation was… Other options include…"* If nothing is needed, open with **"no action
   needed"**. `learnings/2026-09-08_ask-format-action-first`. The 08-06 format had the ask FOURTH.

## 🟢 BUILT THIS SEAT (all pushed)
- **The launcher PULLS before any boot read** — the two-machine gap. No `--autostash`, no output
  suppression. 4 branches + effect controls.
- **Nightly NAS sync + deletion alarm**: `com.wednesday.nassync` 03:30, Tuesday's 23:00 from the same
  self-locating installer; doctor sweeps it (exercised both ways); PORTABILITY items 11–13.
- **`confirmbigdel = true`** in Kam's `!SYNC FILES/devnas.prf` on his 15:37 authorisation, backup
  beside it. **Honest scope: whole-replica only — the gradual case is the alarm's job.**
- **The panel voice change** + `voice-protocol.md` updated.

## 🔴 WEDNESDAY'S EIGHT ERRORS THIS SEAT — all in `_ledger.md` (211 rows; 417 archived, 628 conserved)
The two that reached Kam: **an unmarked card read as undone work** (*two records said done, one
column said undelivered, and the column won*) and **"additive, so nothing is at risk"** (additive
rules out deletions, not overwrites). **Those two are a w=2 with the diagnosis filed** —
`2026-09-08_a-safety-claim-names-the-property-it-checked`: the existing scope-word rule lists words
for classifying WORK, and both were claims about a TOOL'S GUARANTEE, so the handle missed. Also: an
invented DIRTY/CLEAN heuristic handed to an agent as a rule; `chat_reply.sh --help` posting to his
panel; a pane id where a pane NAME was wanted; the first-paragraph voice truncation that was my
inference from his words about WHICH DEVICE speaks; and burying the ask under its context.

## STANDING (unchanged)
- 18,609-line hold on #896/#899/#900; **#899 before #900** or the merge is a silent no-op.
- Refresh no advisory expiry date. Nobody messages Peter or Stuart outside ticket comments.
- **No check on that repo can pass** — Actions dead 19 days; cite the manual twelve-leg preflight.
- **PROJECT TRAP:** any probe of `users.email` by literal comparison is void by construction (AES-GCM).
- The path guard fails CLOSED on `$VAR` in `git -C` — **write literals**; it also refuses `stash list`
  and a command quoted inside a message. Five correct refusals today.
- `decision_queue.sh add --json` reads its payload from **stdin**, takes no companion flags — put
  `"_override_prior": true` inside the JSON.
- **`timeout` and `declare -A` do not exist on macOS.** `lsof +D` on a whole drive will hang a call.

## BOOT NUMBERS (WED-139)
digest **303,794 B / 4,021 lines** WHOLE; ledger **400,644 B / 203 rows** at boot — today's 35 whole,
09-07 (71) + 09-06 (97) as headlines, per `2026-09-08_the-boot-spec-outgrew-its-window`.
Statusline **7% → 21% after the digest → 31% after the full boot → ~86% at close.**
