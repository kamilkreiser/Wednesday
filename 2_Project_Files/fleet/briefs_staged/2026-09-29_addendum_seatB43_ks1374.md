# ADDENDUM (Seat B 43rd): post ONE comment on KS-1374, verbatim, while you wait — Kam asked for it

## BLUF
Kam asked on the live board at 11:38:58 AEST (view=wednesday) for "your response in the ticket" to Peter's KS-1374 (Akto scan pacing vs the platform rate limit). Wednesday drafted it. **Post the text between the markers below as ONE comment on KS-1374, VERBATIM, from the board account**, then mail Wednesday the comment's URL. Change no ticket state, no assignee, no label. No code, no push, no other ticket. This is the only thing in this addendum; your six held branches and your wait for the advisory ruling are unchanged.

If anything in the text is factually wrong at the tip (you may check `api-gateway/src/index.ts:472-485` and `.env.example:205` read-only), do NOT post; mail Wednesday what is wrong instead.

===== BEGIN COMMENT =====
## BLUF
Thanks Peter, this is a clear write-up. **Our recommendation is option 2 plus one guard:** raise `RATE_LIMIT_MAX_REQUESTS` on **local stacks only** (to the code's own non-prod default of 10,000, which you cite at `api-gateway/src/index.ts:472-485`), leave demo and production exactly as deployed, and **add one dedicated limiter test that runs at the demo's limit** so a limiter regression still shows up locally. Coverage is unchanged; only local pacing and one config value move.

## Recommendation, answering your three questions
1. **Which option:** 2, plus the limiter test above. The harness already derives its pace from this value, so it speeds up on its own.
2. **Should local stacks match demo exactly?** A looser local limit is acceptable **for scanning**, provided one test pins the demo behaviour: at the demo figure (2,000/min), requests beyond it are refused with 429, and the read-only skip paths still skip. That keeps the realism you were worried about losing in option 2, without paying for it in every scan.
3. **Is ~20 min / ~1 h acceptable as a local gate?** No. That is slow enough that people start skipping the gate, which costs more coverage than it protects. A config change is worth it.

## Why not the others
- **3 (`DISABLE_RATE_LIMIT=true` during scans):** removes the limiter from the picture entirely and is easy to leave on by accident.
- **5 (a scanner identity with a higher budget):** a new bypass surface that has to stay airtight to non-prod; not worth it when a config value does the job.
- **4 (key the limiter per principal):** probably the right long-term design, and it overlaps KS-618 (every caller shares one address). It is a separate piece of work with security implications, so we suggest a ticket for it, not this change.
- **6:** marginal gains; the limiter still sets the floor.

## Detail
No platform code is proposed to change; demo and production limits are untouched. If you agree, either side can make the change, as you offered: the local `.env` value, and the one limiter test.
===== END COMMENT =====
