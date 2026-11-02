Seat S 13th

ANSWER: PR 3 serializer: how received is obtained = (a), the GLOBAL ERROR MAP. It SUPERSEDES the words "received via reportInput" in condition 3 of my 21:2x ANSWER; the rest of condition 3 stands (received exactly where zod 3 had it; no `input` in any body).

WHY: per-call reportInput puts the raw input on every issue object, including boot-time `Schema.parse(process.env)` errors that get logged (a secret-to-log path); the map sets `received` once and zod's finaliser drops `input`, so no issue anywhere carries raw input. It is a mechanism inside the ruling, so Wednesday's call.

CONDITIONS (add to the matrix):
1. The GUARD CELL you propose: fails if a zod release stops the map seeing the raw issue or stops keeping `received` (plus the golden compare).
2. INSTALL ORDER: prove the map is installed before ANY zod parse in EVERY service process (a structural cell: each of the service entry files you swapped for boundedJson imports the module that installs it, or the install sits at packages/shared's root import that each entry loads first; name which, with the file count and a positive control). A service that parses before the install would emit zod 4 shapes: that is the failure to rule out.
3. NO `input` key on any issue ANYWHERE: a cell parses a failing schema carrying a sentinel secret and asserts the sentinel is absent from the issue object, its JSON, and the 400 body; and a boot-config parse failure's logged error carries no sentinel.
4. validation.ts:187 (the one schema with its own errorMap) uses an error function from the same helper; a cell pins its output against the golden.
5. Process-wide effect stated in the PR body: z.config applies to every zod 4 copy in the process (any library using zod 4 now gets zod 3-style messages); say whether any non-request zod use in the repo depends on zod 4's default texts (git grep with a control).

Wednesday
