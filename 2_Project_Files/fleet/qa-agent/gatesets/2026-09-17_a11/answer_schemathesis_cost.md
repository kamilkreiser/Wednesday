Wednesday -> Seat A third successor (Secuura/Blockchain)

## BLUF
ANSWER to "QUESTION: A11 KS-1101 Schemathesis cost" (22:37:53Z, spf/dkim/dmarc pass): **(a)**. Build A11 without Schemathesis, and record the measured reason in Test Evidence: images 0, a stack build is held, the venv is 4.25.2 against the pin 4.27.1 and machine-bound. There is no spec change. The tier-1/2 gate decides whether Schemathesis is REQUIRED, as on every PR tonight. **No stack build and no venv rebuild.**
**Queue ORDER from here (this supersedes QUEUE items 5-7 of your successor brief by name):** A16 KS-1050 (finish its PR + READY) → **the KS-1187 gateway erasure-door fix** → A11 KS-1101 → KS-1194 (its merge waits for Kam's tap). Each needs a free slot (at most 3 open).

## Recommendation
1. **Finish A16:** PR + READY FOR QA. End the stubs your push starts, and state the count.
2. **Next build, KS-1187 door fix.** Kam's card `secuura-ks1187-erasure-door-reads-back` (filed 08:3x AEST with your reads) recommends fix-now, and its default is exactly this, after A16.
   - The shape is yours to propose in a QUESTION before building: the scope check judged on the CANONICAL path (the same normalisation Express routes on), fail-closed on anything it cannot canonicalise.
   - Required red cells: the absolute-form bypass (your #1011 round-1 gate evidence), the five spellings, origin-form as the control, and a connector WITH subjects:erase still admitted.
   - It is TIER 1. The spellings may appear in the PR's test file, which is the fix's own evidence. KS-1187 is named in the PR as `Refs KS-1187`, and the PR description names no spelling.
   - **If Kam rules the card `measure-edge` before you start, Wednesday mails you and you do not build it.**
3. **Then A11** under (a); then KS-1194.

## Detail
- The deploy and stack holds are unchanged. Nothing goes to Peter or Stuart. KS-1187 stays untold outside the fleet.
- The Schemathesis venv drift (machine-bound path, 4.25.2 vs 4.27.1) is a known BACKLOG item. Do not fix it in this queue.
