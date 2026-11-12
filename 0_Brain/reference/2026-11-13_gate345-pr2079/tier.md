PR 2079: TIER 1 (stopped before testing; at head 0fffdfba0f9578f23d48112068d1451ea947cd29, base develop 410feda1a85e54b82a65464607f4761c2da3bb1b)

Gate 345, 2026-11-13 ~06:05-06:12 AEDT. Findings only; no testing done after the tier call.

Pins: re-read 06:05:04 AEDT by git ls-remote (develop 410feda1a85e..., refs/pull/2079/head 0fffdfba0f95...); both equal the commission's pins. Scratch blobless clone at scratch/clone (push URL disabled) resolves pr/2079 = 0fffdfba..., origin/develop = 410feda1...

Why tier 1:
- Deleted file `Blockchain/Dev/services/shared/src/security/redis-security-store.ts` (417 lines). At develop it exports RedisRateLimitStore, RedisBruteForceStore (keys `security:bruteforce:`) and a CSRF token store (CSRFTokenRecord). These are access-control / auth-abuse-protection surfaces (brute-force lockout, CSRF tokens, rate limiting). The commission's rule: tier 1 = auth, tokens, access control.
- The same PR deletes `src/security/index.ts` export lines (3 added / 13 removed) that re-export those stores, and the cache/ section (redis-client, connection-pool, cache-middleware, compression, index) that the stores depend on.
- The PR body itself records that Wednesday drew this file list as "option A ... tier 1" (ANSWER 2026-11-06 05:40:48Z). The gate-344 style "tier 2" does not fit: this is not tests/docs/config; 12 of 18 files are product source deletions on a security surface.
- The drop is a behaviour question, not only config: whether any runtime consumer (any service importing the package, Dockerfile COPY, the zod census walker, builds) still reads or constructs these stores. The PR asserts "nothing imports it" from a develop-c5c26b2835df search; that claim is unverified by me, and it is exactly what a tier-1 pass must re-measure (a full repo grep with a positive control, at the head). My own full-repo grep over a blobless clone was started and stopped (too slow over promisor fetches); it produced no result and nothing is claimed from it.
- Secondary: the floor `toBeGreaterThan(500)` -> `(494)` in packages/shared/src/__tests__/ks1725-zod3-compat.test.ts is the only non-services/shared edit; the body's own arithmetic (506 files at develop, 500 after, floor 494) is stated, not re-measured here.

Not done (for the Opus relaunch): the KS-657 ticket read, floor red-proof, consumer enumeration, suites before/after, merge-tree vs develop 410feda1a85e, the "develop's lines survive" control, body checks. The PR body notes its pre-push preflight as PREFLIGHT INCOMPLETE (13/16 legs, 3 skipped, stack not up) and the Schemathesis/Akto acknowledgement boxes are unticked; neither is a pass.

Notes for the relauncher: in the scratch clone, set `core.sshCommand` from the project's `2_Project_Files` repo config (deploy key) or promisor fetches of blobs fail; the plain https `gh repo clone` returns Repository not found under the project's gh account.
