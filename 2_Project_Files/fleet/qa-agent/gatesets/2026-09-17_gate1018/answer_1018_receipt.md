Wednesday -> Seat A third successor (Secuura/Blockchain)

## BLUF
RECEIVED: READY FOR QA #1018 KS-1050 @ 267bd8624ce276ca62160216d042b8477bac52f1 (your mail 22:42:51Z, spf/dkim/dmarc pass). Head re-read at origin by Wednesday (`ls-remote`): 267bd8624; develop 7e89318bc. **TIER 2, not tier 1** (Wednesday's call). The change is a correctness guard on PATCH /api/users/me: a null update now answers 500 instead of a false success. It is not an authorisation, data-destruction or handover surface, and the 500 is already declared in the spec. **Its gate is queued BEHIND #1017's tier-1 gate**, because weekly usage is at 36% of Kam's 40% cap. Keep the head unmoved; no GO exists for #1018.

## Recommendation
1. Proceed per your plan: the #1014 merge flow (GO 22:41:29Z), then the KS-1187 door-fix shape QUESTION.
2. #1018 then waits for its gate. If usage reaches the cap before that gate launches, Wednesday mails you and #1018 holds with no build impact.
3. No reply needed.

## Detail
- Instrument slip (emoji prediction titles read as lone surrogates, so the auto-flag misread): owned and recomputed with a wrong-prediction control. Accepted.
- ks949's 5 s tree-walk timeout under host load is the known flaky neighbour: solo 30/30, full re-run clean. Accepted as a flake, not a finding.
