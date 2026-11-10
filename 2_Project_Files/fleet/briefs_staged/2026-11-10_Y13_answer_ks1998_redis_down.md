Seat Y 13th

ANSWER: (A), the PUT's shape, no pre-check. While Redis is down: settings GET answers the stored record, policy GET answers the stored verification values (through readPlatformSettings, refill TRUE). This is Wednesday's design ruling inside KS-1998 (D3 left the state open), not Kam's: write it so.

Reason: (B) leaves the loss path open (a page loaded during an outage shows defaults and the next save writes them over the record), and the PUT already reads the record with no pre-check, so (A) makes the three doors agree.

IN THE PR BODY AND THE READY, plainly, for the tier-1 gate: (1) readPlatformSettings's own doc says it is 'for a reader that has ALREADY confirmed Redis is available'; (A) calls it without that check, as the PUT does today: name both lines; (2) your claim that the refill writes the in-process Map so the PUBLIC policy GET reads the database once per process during an outage, not once per hit: state it as yours, with the cell that pins it (one DB read across N GETs with Redis down) or as UNMEASURED; (3) the connector readers (verification.ts 840) keep their pre-check and are not touched. Add the Redis-down cells to your declared list (prediction before the run) and one mutant that adds the pre-check back.

Wednesday
