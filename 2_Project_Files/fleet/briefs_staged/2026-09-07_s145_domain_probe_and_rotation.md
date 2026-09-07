## BLUF — Kam ruled TWICE at 11:43. (1) The domain probe is authorised — and Wednesday is changing what it is FOR. (2) The 183-file credential is a ROTATION, done properly, as its own round AFTER #885 merges.
**Destination: no commit at all for item 1. Item 2 lands on `origin`, a NEW branch, and only after
#885 is merged.**

## 1. THE DOMAIN PROBE — authorised, but use it as the DEPLOY'S OWN PROOF, not as a footnote
**Kam, card `secuura-demo-row-060-remediation` => `domain-probe-then-decide` (11:43:27).** You
identified this check yourself and correctly refused to run it on one probe's authority. **He has now
granted the second.**

**Wednesday is re-purposing it, and this is the operative instruction.** You closed the
*does-the-fix-reach-the-row* question from source, so that gap is gone. **What remains open is
whether the row currently holds a NON-FICTIONAL domain** — your boolean only proved "not the
placeholder". **So run the domain check as a BEFORE/AFTER PAIR around the deploy:**
- **BEFORE (now):** compare the domain only against the fictional `secuura-test.invalid`. A
  non-fictional domain establishes the exposure as measured rather than inferred.
- **AFTER (post-deploy):** the identical statement. It must read fictional.
**That turns the deploy from "we believe it remediated" into a measurement at the destination**, which
is the only kind of completion claim worth making about a running system.

**BOUNDS, unchanged and absolute:** ONE statement per side, **read-only**, **the address is never
selected** — compare the domain, return a boolean, exactly as you built the first probe. **No writes,
no login, no restart.** **Write the success/failure/cannot-discriminate conditions down BEFORE each
run**, as you did at 01:05, and report which you got. **If the check cannot discriminate, say so and
STOP.**

## 2. THE ROTATION — Kam ruled `rotate-properly` (11:43:32). Its own round, AFTER #885 merges.
**Do not start the code until #885 is merged.** You may do the MEASUREMENT half now, because it is
read-only and it decides the shape.

**Kam's option, as he chose it:** *"A new credential, set by environment variable everywhere it is
needed, the CI workflows updated to use a secret rather than a literal, and `.env.example` carrying a
placeholder rather than a working password."*

**MEASURE FIRST — and one of your own findings changes this materially.** You established that
**Actions is retired for that repo: 20 of 20 recent runs are `startup_failure` with zero jobs.**
**So the CI workflow files are an EXPOSURE, not a working dependency** — nothing is executing them.
That means removing the literal from those three workflow files **cannot break a run that does not
happen**, and it decouples the risky-sounding half from the real one.

**So establish, before proposing a shape:**
1. **Which consumers actually READ these values today** — the local/manual suites per `DEV-PROCESS.md`,
   `docker-compose`, developer `.env` files. `.env.example` is a template; is anything reading it
   directly, or is it copied by hand?
2. **Which of the 183 occurrences are EXECUTABLE** (something reads them) versus **DOCUMENTARY** (a
   human reads them). Those are two different jobs with two different risks, and the numbers should be
   reported separately rather than as one total.
3. **Whether a new credential needs to be SHARED at all.** Prefer **no default and no shared secret**:
   an env var each runner sets for itself. A shared value that must be distributed is a rotation we
   will have to do again.
**Then propose the shape to Wednesday BEFORE writing it.** Kam ruled the direction, not the design.

**Never in any artefact: the old plaintext, the old hash, or a new working credential.** A rotation
that publishes its replacement has rotated nothing.

## 3. TWO CORRECTIONS WEDNESDAY OWES YOU
**(a) You were right about the CI lane and Wednesday was wrong, in the direction that matters.**
Wednesday told Kam *"PRs are not unchecked"* on the strength of a `pull_request` trigger block. **Your
20-run `startup_failure` census refutes it.** Wednesday read the field that DECLARES a thing instead
of the record that EVIDENCES it — **and your framing is the one that went into the record**: the same
shape as the three filed today. **Worse than a repeat: it was a CORRECTION, which carries more
authority than the claim it replaced.** Corrected to Kam leading with it. **Your baseline then
justified his ruling better than Wednesday's reasoning had** — the lane is RED on develop, two
pre-existing failures, so blocking would have stopped every PR including Peter's and Stuart's.

**(b) Wednesday put KS-645/KS-952 in your queue when you had finished it 40 minutes earlier.** You
did not redo it, you said so, and you showed the `updatedAt` timestamps. **Wednesday wrote a queue
item without reading its state** — the same root cause as this morning's, pointed the other way.
Filed.

## 4. STATE — Wednesday's reading, correct it if wrong
#885 `6dbe63cae` under gate (%150) · PR #887 `bb0502c80` (advisory lane + the DEV-PROCESS row) ·
KS-597 `af640e809` pushed, **no PR yet — say if you want one opened** · KS-960 filed (schema
divergence, do-not-reconcile) · KS-961 filed (the lane, with the two failing suites named as the
blockers for making it blocking) · KS-61 quarantine `d6922d8ec` local-only, pending Kam.

## HOLDS
**Push nothing to #885.** Nothing merges without the gate and Wednesday's GO. **The deploy is
authorised and happens after the gate — and now carries the BEFORE/AFTER domain check as its proof.**
No human contacted. No history rewrite. No `rm`. Do not touch the demo beyond the two authorised
read-only statements.

## PROVENANCE
- Both rulings | Kam's panel 2026-09-07 11:43:27 and 11:43:32, cards
  `secuura-demo-row-060-remediation` => `domain-probe-then-decide` and
  `secuura-admin-credential-rotation-183-files` => `rotate-properly` | read by Wednesday this action.
- The Actions census, the RED baseline, the 183/128 counts, KS-645/952 timestamps | **your
  measurements, quoted.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **11:43:27 `domain-probe-then-decide`** — lands in: your before/after probe report.
- **11:43:32 `rotate-properly`** — lands in: the rotation ticket and its round's PR.
