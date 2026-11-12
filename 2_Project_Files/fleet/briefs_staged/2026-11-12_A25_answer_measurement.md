Seat A 25th

ANSWER: KS-1466 measurement (Seat A 25th)

BUILD. Your R1 settles Kam's stop rule on its own: both catalogues are EMPTY (KEYS secuura:gateway:doctype:* = 0 on kintsugi 00:36:54Z and on demo 00:37:34Z, AUTH OK), so after the fix an untyped create resolves to DOCUMENT, finds no catalogue, and passes at line 137 on both boxes. No current caller is refused, whoever they are; the rows could not change that answer, so they are not needed for this decision. Your log reading agrees (UNKNOWN_DOCUMENT_TYPE 0 and DOC_TYPE_DISABLED 0 on both). No credential grant is wanted and none is made.

Build as briefed: red test first, the fix at the untyped return (line 117 at develop), the operator note in the same PR, one tier-1 PR, READY FOR GATE (Opus gate). In the PR body and the READY, name as UNMEASURED: the row counts (psql refused without a password; no password was passed, correctly) and the absence of a positive control inside the allow-list for an empty KEYS reply (your basis: develop's compose and redis.ts, not the boxes' own files). The operator note says exactly your item 7: on a box whose catalogue is written by a current seed nothing changes (dt-seed-8 DOCUMENT is friction-free); a hand-built catalogue without DOCUMENT makes every untyped create a 400.

TWO FINDINGS go in your READY as CANDIDATE FILINGS (the board seat files them; you do not): (1) the catalogue is empty on both boxes, so KS-388's catalogue validation is OFF there today (any documentType passes); (2) the Outlook add-in sends documentType = the file's MIME type (frontend/outlook-addin/src/utils/api.ts:118), already a 400 UNKNOWN_DOCUMENT_TYPE on any box with a non-empty catalogue. Measured by you; Wednesday has not re-read either.

No further box call is granted or needed. Census first (your MEANWHILE), as briefed.

Wednesday
