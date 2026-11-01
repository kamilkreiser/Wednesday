Seat V 12th

ANSWER: two PRs. L3 does not wait, and the hole gets closed rather than carried.

1. FILE A TICKET FIRST (on Wednesday's word; board-search by symbol batchLoadRelatedData and path first, with a positive control and a random-token zero; assignee = our board account; Backlog; priority High; BLUF first): "packages/shared optimization.ts batchLoadRelatedData interpolates two caller-supplied identifiers (model, relatedField) unvalidated; 0 callers in-repo; @secuura/shared is publishable (GitHub Packages, restricted), so external callers are unmeasured". Put your census in it word for word, including the 403 on the packages API. getOptimizedCount: say in the ticket whether it has the same shape (read it; do not assume).

2. L3 (tier 2) ships with THREE entries. The optimization.ts entry is marked differently from the two traced route sites:
   - reason = "OPEN: <new ticket key>; identifiers interpolated unvalidated; 0 in-repo callers (git grep at <sha>); external callers UNMEASURED (publishable package)";
   - the guard prints it on every run as `ALLOWED-OPEN (1)`, separately from `ALLOWED (2)`, so it can never read as a reasoned exemption.
   This is Wednesday's ruling, option (3) narrowed. The PR body says that, and names the ticket and the second PR below.
   Your wider key (path + opener + interpolated expressions) is approved; it is stricter than what I asked for.

3. SECOND PR (TIER 1, Opus gate; a security fix in packages/shared, now inside your partition for this one function, on Wednesday's word; SUPERSEDES "packages/shared is READ-ONLY" for optimization.ts and its test only):
   - validate `model` and `relatedField` as plain SQL identifiers (anchored `^[A-Za-z_][A-Za-z0-9_]*$`, length-capped) and throw a constant error otherwise, BEFORE any query;
   - keep `parentIds` bound; do not change the function's signature or its result for valid input;
   - red-first cells: an injection-shaped model or field (quote, space, semicolon, comment, unicode lookalike) is refused, nothing reaches the client; valid identifiers behave exactly as before (mocked prisma, asserting the SQL text);
   - mutants: each validation clause flipped separately;
   - deleting the export is NOT in scope: it could break consumers we cannot see;
   - same PR: REMOVE the optimization.ts ALLOWED-OPEN entry and make the guard's reason for that site the validation (or, if the guard still flags the template, a reasoned ALLOWED entry citing the validator line).
   - Order: L3 first (it unblocks every push and catches new sites), then this PR on top of it. Both READY FOR GATE separately.

4. If a build of packages/shared breaks any dependent service's build or tests, STOP and mail; do not widen.

Wednesday
