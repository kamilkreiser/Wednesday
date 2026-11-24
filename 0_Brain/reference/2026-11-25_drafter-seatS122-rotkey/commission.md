# DRAFTER COMMISSION — brief for Seat S 122nd (Secuura/Blockchain-S, READ-ONLY code read)

Written by Wednesday 2026-11-25 (morning). You are a DRAFTER: write ONE brief file and nothing else. You do not launch, mail, or touch any project file outside the output path.

## Output
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-25_seatS122_rotkey_read.md`

## Template
Copy the SHAPE (sections, STAMP block, provenance table, plan-QUESTION-first rule, wrap section, the launcher first-action warning, never-cd/never-rm/MOVE rules, mail tooling) from
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-24_seatS121_board.md`. Read it WHOLE first. Keep everything that is about seat discipline; replace the work items.

## Authority (quote verbatim in the brief)
- Kam, live board 2026-11-25 06:56:40, card `secuura-rotated-key-erase-scope-1125` = a: "Have a seat read the code first and tell me what it does today". The card's option detail: "one board seat reads register-connector's rotate path read-only and puts the measured answer on this card's ticket for you; nothing is posted to Stuart until you rule again".
- Kam, live board 2026-11-25 06:57:19 (usage grant): "keep working.  I will log in with a new account after usage runs out".

## The question (Stuart, KS-843 comment 2026-11-24T06:05:42Z, addressed to Kamil; item 6 on KS-772)
"does a rotated key carry `subjects:erase` and the 3,000-an-hour limit? S does nothing until that is answered."
Context from the same comment: a platform admin calls `register-connector` with `rotate: true`; keys minted 20-21 Aug predate KS-869 (6 Sep) and likely carry no connector id; related tickets KS-1152, KS-2114, KS-577, PS-740, PS-1751.

## The work (ALL read-only)
1. Clone develop at the live tip into the seat's own scratchpad (never the shared checkout; never write in 2_Project_Files). Record the sha.
2. Find the register-connector rotate path (api-gateway and/or originate; search, do not assume). Answer, each with file:line at the sha:
   a. On rotate, are the OLD key's scopes copied to the NEW key? Specifically `subjects:erase`. If not copied, what scopes does the new key get, and from where (defaults, request body, organisation)?
   b. Is the 3,000-an-hour rate limit a property of the key (copied or not), of the organisation, of the scope, or global? Where is 3,000 defined?
   c. Does the answer differ for keys minted before KS-869 (no connector id)?
   d. Any test that pins (a)-(c) today; name it, run it if it is cheap and in the seat's own clone.
3. NO write anywhere: no Linear comment, no ticket, no PR, no push, no mail to any human, no request to any running stack (Kintsugi, demo).
4. Deliver: a QUESTION/plan mail first (read-only plan), then a FINDINGS mail to Wednesday with the answer in plain words at the top (two sentences Kam can read), then the evidence, then what was NOT measured. Wednesday relays it to Kam; Kam rules what goes to Stuart.
5. WRAP per the template.

## Routing
Model: Sonnet (newest; Wednesday fills the id from models_latest.json at launch). Lane -S. Seat name exactly `Seat S 122nd`.

## Return
When the file is written, reply with its path, byte count, and any fact in this commission you could not validate against the source (say UNVALIDATED next to it in the brief too).
