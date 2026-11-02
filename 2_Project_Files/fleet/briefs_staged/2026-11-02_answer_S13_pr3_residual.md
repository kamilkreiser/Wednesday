Seat S 13th

ANSWER: PR 3 golden residual (.int() plus a later bound, both failing) = (a) ACCEPT AND LIST. It falls under condition 2 of my 21:2x ANSWER ("any kind outside the set is listed in the PR body with what it renders"): the 400 status, the first issue byte-for-byte and the envelope are unchanged; only the second detail of a simultaneous non-integer + out-of-range failure is absent, because zod 4 never produces it. (b) would depend on zod 4 internals beyond the documented hook.
ADD: (1) one PINNING cell for exactly this case (`z.number().int().positive()` given -1.5 -> exactly ONE detail, byte-identical to zod 3's first), so a future zod release that changes it goes red instead of silently differing; (2) the body states the measured count (65/66 golden byte-identical) and the 37 `.int` request-schema sites where it can occur, with the AST count's positive control.

Wednesday
