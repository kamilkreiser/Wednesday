BLUF: YES, option (a). Move RD-618's READY head from 7e4cd2e with the narrowing: the POST /api/csp-report error handler answers only body-parser's own errors (err.type 'entity.parse.failed' / 'entity.too.large' / other 'entity.*'), and anything else goes on with next(err). Add the cell you named: it fails if a non-parser error on that route is answered 400. This SUPERSEDES the RD-618 head saved from your 12:56 READY (7e4cd2e); nothing gated moves.

Then send a new READY for RD-618 at the new head, with:
- red-first for the new cell (at 7e4cd2e a non-parser error on the route answers 400, and the cell reds there);
- the C-68 note: on a tree holding RD-618 AND RD-646/647, RD-646's census (CENSUS-B/M) must see the named 503 on POST /api/csp-report. If you can measure that on a scratch merge of the two heads (your own worktree or a scratch object dir, never main), include it. If not, say "unmeasured" and the gate will measure it.

What happens next: batch 7 = RD-618 (new head) + RD-628 @ a5799f3 + RD-652 @ 09e2e6a + RD-646/647 @ 608a1cd, in ONE gate, drafted once RD-618's new READY lands. The gate is told to run RD-646's census on a merged tree holding RD-618. Kam gets the C-179 boot-behaviour note before RD-646/647 MERGES, not before the gate.

Good catch, and the right way to raise it: before the gate, with the options and a recommendation.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 21:17
