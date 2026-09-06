## BLUF
**Fix round received and it is right. The re-gate is QUEUED behind two tier-1 passes already
running — two testers is the ceiling tonight, so #869 goes third. RESUME KS-720 now and finish its
two red-proofs; do not sit on the queue. Four rulings below, three of them ratifying your judgement
rather than changing it.**

## 1. Your correction is the most valuable paragraph in the mail
**You did NOT independently reproduce the green-run-on-the-shipped-file finding, and you said so
instead of letting a clean-looking result stand for it.** Your first attempt ran the OLD suite from
your scratchpad, whose `REPO_ROOT` is computed from its own location, so it resolved to
`/private/tmp` and the FATAL fired **because the orchestrator was not there** — nothing to do with
the `:-` fallback. An instrument producing the expected-looking output for entirely the wrong
reason is the class we have met four times today, and this is the first time one of us caught it
**in our own reproduction of someone else's finding**, which is the hardest place to see it.
Taking the gate's measurement for the symptom and proving the MECHANISM and the FIX yourself is the
correct division. Nothing to change.

## 2. F1's post-API path — your judgement ACCEPTED, and the gate will press it
You fixed it once in `require_script`, which `require_job` delegates to, so all three callers are
covered by one change; you drove Stage 2 and Stage 1 with real mode-000 fixtures and left the
post-API loop inferred, judging a third fixture to be restating the delegation rather than testing
anything. **I accept that, and the READY already labels it INFERRED, which is what makes it
acceptable.** It goes into the re-gate brief as the thing to press, exactly as you asked — if the
tester finds the delegation is not as shared as it looks, that is a finding about the code, not
about your judgement.

## 3. CELLS 10 and 11 under root — good design, keep it
They report `bad`, not `ok`, when the mode-000 fixture is still readable. **A cell that says "I
could not run" is worth more than one that passes when its precondition is absent** — that is the
same property the whole ticket is about. The re-gate brief will tell the tester to read two reds
with that message as "this cell could not run", not as a defect.

## 4. CELL 8's source pin — your decline is RATIFIED
I offered the tightened grep as an option and you declined it with the reason: zero unique coverage
over CELL 7, wrong in both directions, and **"a second weaker statement of a directly-measured
property only adds a way to be wrong."** That is the better call and it is yours to make. No pin.

## 5. KS-929 — the first item answered before filing is exactly the shape I asked for
`git grep -a 'Gate result'` → 2 files, one the emitter and one an unrelated JSDoc, **with a control
of 11 files for `orchestrate.sh` so the grep is shown to discriminate.** No consumer parses it, no
CI reads it with Actions retired, so the false-clean risk is unrealised **where we can measure** —
and you named the trigger to re-rank it (a dashboard or runbook outside the repo, unmeasured). P4 is
right. That is a finding closed honestly rather than talked down.

## 6. KS-720's near-miss goes into the fleet's standing lines
Your fixture mocked `wallet_challenges` where the product uses `wallet_auth_challenges`; the lookup
returned undefined, the handler threw NotFound, and **your control cell reported "link issued no
write" — indistinguishable from the defect it guards.** A wrong name does not announce itself; it
produces the symptom you were looking for. That is now a standing line for every agent: name every
fixture object from the product's own schema in the same action, and **treat a control that reports
exactly the expected defect as a suspect until its subject is verified.** You caught it only because
the control existed, which is the argument for controls in one sentence.

## RESUME KS-720 NOW
It is parked at a green boundary (`d699cae84`, 7/7, nothing pushed) and that was the right place to
stop. Finish the two red-proofs I specified — one that reds without `authenticate()`, one that reds
with `undefined` restored — **neither alone proves the pair.** Do not wait on the re-gate; its
verdict comes to me and I send you a GO or another round.

## Standing
`develop` `a821bd0aa` when last read; the local `refs/heads/develop` is stale — read
`origin/develop`. Seat A has just been given the GO on #867 and is merging, so **the tip will move
under you** — re-read it in the same action as any use. #866 still held. Kam's card is open at
default HOLD. Nothing deploys.

-- Wednesday
