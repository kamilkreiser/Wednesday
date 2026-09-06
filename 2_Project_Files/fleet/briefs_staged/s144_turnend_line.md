# SMALL ITEM while both your PRs are under gate — a Kam approval Wednesday has owed for 14 days

## BLUF
Both #884 and #876 round 2 are under tier-1 gates and you must push to neither, so here is a bounded
item in your OWN launcher that touches no gated branch. **Kam approved this on 2026-08-24 and
Wednesday never delivered its half.** That is Wednesday's lapse, not yours.

## THE APPROVAL, and why it matters to you specifically
Card `launcher-turn-end-line` => **approve**, 2026-08-24. Its option text names two halves:
*"I hand the exact line to each remaining project's agent"* — **Wednesday's, not done for 14 days** —
and *"the scaffold owner (Kam) pastes it into the shared template"* — his, also not done.

**Why it is not academic:** your seat stalled at turn end **twice this morning** (~06:51 and ~07:1x).
Both times you announced your next item and the turn simply ended; Wednesday tapped you and you
resumed immediately. Cost was two taps — but a stall at 02:00 with no coordinator awake costs hours.

## THE DIAGNOSIS — your launcher ALREADY carries a rule, and it is narrower than the approved one
Measured by Wednesday, read-only, before writing this:
- `Launch_Claude.command:555` carries a turn-end rule (one instance, `grep -c` = 1).
- **It genuinely reaches you**: the prompt opens at line 388, and counting unescaped `"` from 388
  through 555 gives exactly 1 (the opening quote), with zero unescaped quotes in 389-554 — so the
  string is unbroken. **Worth checking: that exact defect truncated Wednesday's own launcher on
  2026-09-02 and four seats booted without the prompt's tail, with `bash -n` clean.**

**Deployed (555):** *"…if you state you will **send, post, file or comment** something, do it in the
same turn before you stop…"*
**Approved (Kam's card, verbatim):** *"HARD RULE — a turn never ends on an unmailed report: before
ending any turn, **either continue working in-turn** or send a STATUS/wrap mail to
wednesday-agent@agentmail.to; an intention stated at turn end is not a trigger."*

**Both of your stalls were "next is item 3" and "next is #876 round 1" — an intention to WORK, not to
send/post/file/comment.** The deployed enumeration does not reach that case. **The approved wording's
"either continue working in-turn" does.** That is why it kept happening with the rule already present.

## THE ITEM
1. **Replace the line at 555 with Kam's approved wording**, verbatim as quoted above. It is your
   project's launcher — yours to edit, not Wednesday's.
2. **Escape every inner quote as `\"`** (or better, move the prose into a quoted heredoc assigned to
   the variable). The 2026-09-02 incident was one unescaped `"` closing the string early.
3. **Prove it survives into the prompt**, not just into the file: after the edit, re-run the same
   quote-parity check (unescaped `"` from the prompt's opening line through the new line must be odd),
   or source the block with dummy vars and assert the variable ends where it should. **`bash -n`
   cannot see a string boundary moving — it passed on the broken version.**
4. Commit it on its own branch or directly per your project's convention — **just not on #884 or #876.**

**Not urgent, not blocking, and it yields to any gate verdict that arrives.** If a verdict lands
mid-way, drop this and take the verdict.

PROVENANCE:
- Kam's approval and both its halves | card `launcher-turn-end-line` => approve, read via `decision_queue.sh show` in WEDNESDAY's tree | read 2026-09-07
- The deployed wording at line 555, the single instance, and the prompt-integrity check | Wednesday's own read-only greps and quote-parity count over your `Launch_Claude.command` | measured 2026-09-07
- That both of this morning's stalls were intentions to WORK rather than to send | Wednesday's pane captures at ~06:51 and ~07:1x, and the detector reporting an empty prompt both times | measured 2026-09-07
- Whether any OTHER project's launcher carries the narrow wording | NOT ESTABLISHED — Wednesday has read only yours | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 09:04
