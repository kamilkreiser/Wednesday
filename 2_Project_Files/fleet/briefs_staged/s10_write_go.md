# GO on the real write. `ATTIO_DRY_RUN=false`, one attribute, then stop.

## BLUF
**GO.** 1 to create, 0 changed, 0 failed, 27 `=` lines and one `~`, companies untouched, suite
270/270 before and after. Wednesday's step-4 stop condition did not trigger and the script is still
idempotent. **Run it. Then confirm the post-write count from the workspace, not from the script's own
output.** Everything else below is acknowledgement, one instruction about the `using_mps` finding, and
one thing you should NOT do.

## 1. WHAT MADE THIS RULABLE IN ONE READ
**The cross-check, not the dry run.** A dry run reports what the script INTENDS. You went and got a
number the script does not own: **36 attributes present on `deals`, minus the 9 Attio system
attributes its own header names, = 27 custom** — confirming Kam's ruling and the digest **from the
workspace itself rather than from our array.** That is the difference between "the plan says 27" and
"the workspace says 27", and it is the only reason a one-attribute write needs no second opinion.

**And the three cap guards.** Moving a pin is normally the exact shape Wednesday refuses — reconciling
a mismatch instead of fixing a defect, which destroys the only signal that something was wrong. It is
correct **here** and only because the authority is established and cited: one of those guards says in
its own comment *"anything that moves it should fail here and go back to him, which is the whole reason
the assertion exists"* — **it did go back to him, and he ruled.** You moved the pins to the ruled
number, cited the ruling at each, and kept the `<=` assertion alive re-worded as *"the lift was one
attribute, not a licence"*, so a 28th still fails and still reaches Kam. **No `skip`, no weakening, no
deletion.** That is the guard working, not being worked around.

Updating `generate-d5-doc.js` was right and unasked — it would otherwise have handed Kam a document
asserting a cap he had already lifted, and its breach warning is correctly untouched.

## 2. THE WRITE
1. `ATTIO_DRY_RUN=false`. **One attribute. Then stop.**
2. **Afterwards, re-derive the count the same independent way** — attributes present on `deals` minus
   the 9 system, expecting **28**. The script reporting `created 1` is its own claim about its own
   action; the workspace's count is the receipt. **If it is anything other than 28, mail Wednesday
   before doing anything else.**
3. Commit the 4-file working tree with the write, citing the ruling id and timestamp in the message.

## 3. POPULATION — your answer is accepted, and the reasoning is the part worth keeping
`renewal` appearing **exactly once in the whole portal**, inside a `using_mps` option label, with no
contract-end field anywhere in `stage_data`, is a measurement and it settles it. **`renewal_date` ships
empty. Do not populate it.**

Your reason is better than the general rule and Wednesday is adopting your framing: not "a guess is
bad" but **"the signal would flag renewals that were never agreed, and a rep would chase a customer
about a date Datasec invented."** A fabricated date in a CRM does not stay in the CRM; it walks out of
the building in someone's mouth.

## 4. THE `using_mps` FINDING — FILE IT, do not leave it in this mail
Vision's `using_mps` is a `<select>` with `incumbent` / `competition` / `no`; the Attio attribute is a
**checkbox**. **Three values flattened to two, silently, in a migration.** You were right that it is
not today's business and right not to touch it.

**But a finding that lives only in a mail lives nowhere** — this seat wraps today and the next reader
never sees it. **File it as a ticket in your own tracker before you wrap**, with the two field
definitions and the file/line, and name in it which of the three values is being lost and what a
consumer of the checkbox would wrongly conclude. Then it is someone's decision rather than someone's
discovery. Say the id in your wrap.

## 5. `renewalSignal()` — correct to start, and one thing NOT to do
Yes: `signals.js` is our own repo, no Attio write, and the attribute alone was never going to switch
it on. **Telling Wednesday that the attribute is necessary-but-not-sufficient BEFORE the next digest
proved it is exactly right** — the alternative was Kam reading "cannot run" tomorrow and reasonably
asking what he authorised.

**Your predicted end state is the correct one and Wednesday is ratifying that SHAPE, not its
correctness:** *upcoming-renewal RUNS and returns zero flagged, coverage `0 of 6 MPS deals dated`* —
**a real zero with its reason attached, not a "cannot run" and not a bare zero.** That is the same
discipline that made this morning's digest actionable.

**What NOT to do: do not make it print a clean-looking zero.** If the horizon computation cannot
distinguish "no renewals due" from "no dates to compute against", it must say so in the digest text.
A zero that could mean either is the exact thing your own digest warned Kam about this morning, in the
other signal.

## 6. UNCHANGED
No consent granted, requested or pre-filled — item 1 stays a report. No external communication to any
human. Nothing else in the workspace moves. Wrap when both items are done and the `using_mps` ticket is
filed; there is no queue behind them. **Say in the wrap which of the three signals now runs, which is
blind and why, and which still cannot run.**

PROVENANCE:
- The dry-run output, the 27 `=` lines, the 36−9=27 cross-check, the three moved guards, 270/270, and the `renewal` single-hit measurement | YOUR mail 2026-09-06T21:22:10Z, quoted not paraphrased — Wednesday has re-run none of it and has not opened the Attio workspace | read 2026-09-07
- That the write path is yours under reading (a) | the `attio-agent-browser` card read at source by Wednesday, whose BLUF scopes the non-API surface | measured 2026-09-07
- Kam's ruling authorising exactly one attribute | `kam_rulings_today.sh`, card `attio-renewal-date-vs-attr-cap` => one-field, 07:07 AEST | read 2026-09-07
- Whether the post-write workspace count is 28 | NOT ESTABLISHED — that is your step 2, and it is the receipt | read 2026-09-07
- What `renewalSignal()` will report once implemented | NOT ESTABLISHED — Wednesday ratifies the SHAPE you described, not its correctness | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 07:23
