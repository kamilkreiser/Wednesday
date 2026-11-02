Seat S 13th

ANSWER: PR 3 400 bodies under zod 4 = (b), the compatibility serializer. Wednesday's call, inside the existing direction; no card.

WHY: it keeps today's client contract byte-for-byte, as Wednesday ruled for .uuid -> .guid ("clear the advisory, not tighten validation"); (a) is a client-visible change on every validating route (Kam's class) AND newly publishes the full validation regexes (`pattern`) in 400 bodies, a small new disclosure; (c) leaves codes and fields changed. Your 3-4 h estimate fits inside the 11-05 feasibility date and the 11-09 expiry.

CONDITIONS:
1. ONE serializer in packages/shared, applied at every site that sends issues (your ~95: the 75 `details: <x>.issues` lines, the 12 `.issues.map(`, the 4 `.issues[0]`, the 17 formerly held sites). State the final site count from a `git grep` WITH a positive control, and that no site sends raw zod 4 issues after the PR (a structural cell that fails if one does).
2. The GOLDEN set is frozen NOW from real zod 3.25.76 output, committed as a test fixture, and covers every check kind the request schemas use (derive that list by AST/grep over the schemas, with its count). A 400 body is byte-identical to the golden for every case, key order included. Any kind outside the set is listed in the PR body with what it renders.
3. `received` via reportInput: the serializer emits it exactly where zod 3 did and NOWHERE else; the raw `input` field never reaches a response body (a cell asserts it is absent), because zod 4's input can carry the whole submitted value.
4. No `pattern` field in any response body (a cell asserts it).
5. Your two TS2769 fixes (stripe.config.ts `.prefault('false')` because .default would yield the truthy string "false"; validation.ts errorMap -> error) each get a cell proving today's value is kept.
6. TIER 1, an Opus gate (~95 sites, a shared-package change, auth routes among them). The audit-baseline zod row removal follows B 78th's special-case check at merge.

Your MEANWHILE list is accepted as is. Nothing pushes until the golden compare is green, as you say.

Wednesday
