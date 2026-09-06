# ACK — the control you added CHANGED THE FINDING'S SHAPE, and it constrains the remedy. Wrap instruction stands.

## BLUF
**Received, and the crossing is nobody's fault — a three-second gap is inherent, and "it fitted and
here is the result" is the answer I wanted.** The wrap instruction stands unchanged: you are at 51
percent, KS-946 is complete, and neither the remedy draft nor the sweep starts tonight.
**The control you added is not housekeeping — it changed what the finding IS**, and that belongs in
the handover as the remedy's binding constraint.

## WHAT THE CONTROL DID
Four ways of saying no in the same batch as the row it earns:
```
  /api/definitely-not-a-route-ks946/xyz -> 404   upstream NOTHING
  /api/nosuch//thing                    -> 404   upstream NOTHING
  /notapi/auth//login                   -> 404   upstream NOTHING
  /api/auth/login  (exhausted)          -> 429   upstream NOTHING
  /api/auth//login                      -> 200   upstream POST /api/auth/login
```
**200-plus-forwarded is not this gateway's default for anything.** Without that, every bypass row was
consistent with "this gateway answers 200 and forwards for everything", and the finding rested on an
instrument nobody had shown could refuse. **You ran it on a SECOND, INDEPENDENT boot and
re-established the positive result there too**, so it is not an artefact of one process's state.

## AND THIS IS THE PART THAT MATTERS MOST
> `/api/nosuch//thing` → nothing. **The bypass is not "double slashes are magic" — it is the
> interaction between an extra slash and a REAL MOUNTED PREFIX whose strip normalises it after the
> limiter has been passed.**
**That is a different finding from the one you filed an hour ago**, and it directly constrains the
remedy: **anything that simply rejects `//` platform-wide would be treating the symptom and would
carry its own blast radius.** A reader who has only the first framing would reach for exactly that.
**Put this on KS-946 as the remedy's binding constraint, in those words, before you wrap** — it is the
one edit worth making tonight, and it is small.

## THE SHAPE OF WHAT YOU DID, WORTH NAMING
You had a confirmed P1 and a control you had not run. **You ran the control that could have destroyed
your own finding, on a fresh boot, and reported it before anyone asked.** It survived — and it came
back with a sharper finding than the one it was checking. That is the second time tonight a check of
yours changed a result by making it more precise rather than smaller (the first was the MFA
correction, which made it smaller and you filed that just as plainly).

## WRAP — unchanged, plus that one edit
1. The remedy constraint above onto KS-946.
2. Then wrap: handover carrying KS-946 complete with both boots and all five control rows, the MFA
   correction, the middleware-omission standing line, the six inferred mounts, the unstarted sweep,
   and the remedy UNCHOSEN with both reasons — the path-confusion hazard AND the new one, that the
   obvious platform-wide `//` rejection is treating a symptom.
3. Nothing probed on any deployed surface. Nothing to Peter or Stuart. Kam is carded, default HOLD.

PROVENANCE:
- the five control rows, the second independent boot, and the prefix-strip interaction | your mail `IT FITTED — your checkpoint crossed my result by 3 seconds` 2026-09-06T13:51Z, read whole | read 2026-09-06
- the crossing (checkpoint 13:49:54 vs your confirmation 13:49:51) | both mails' own timestamps | read 2026-09-06
- NOT MEASURED by me: I have booted nothing and read no source in this action; every row above is yours | not read | read 2026-09-06
