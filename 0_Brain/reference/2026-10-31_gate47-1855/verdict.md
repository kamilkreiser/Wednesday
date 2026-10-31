# QA GATE 47: Secuura/Blockchain PR #1855 (KS-1850, Seat E 22nd), Tier 1, Round 1
**Head gated: 9fc7fb14afd65b34d98ae4874795f66cabe1cc99**. This is the head origin holds: `refs/pull/1855/head` was fetched and matches E's ls-remote. Merge-base is develop 85cd24d81cb9. Develop tip is cb2320368 and none of its newer commits touch billing, nft-certificate or packages/shared.

## VERDICT: GO WITH NOTES. No finding needs fixing before merge. F3 and F4 are older problems in these files and need their own tickets.

| File | Change | Gated |
|---|---|---|
| services/billing/src/routes/billing.ts | +7 -2: POST /admin/credits now uses `isPlatformRole` from @secuura/shared | yes |
| services/nft-certificate/src/routes/nft.routes.ts | +7 -2: PUT /admin/platform-fee, same change | yes |
| billing/src/__tests__/ks1850-admin-credits-requires-a-platform-admin.test.ts | new, **14 tests** | yes |
| nft-certificate/src/__tests__/ks1850-platform-fee-requires-a-platform-admin.test.ts | new, **14 tests** | yes |
| Projects Documents/*.html (2 files) | +41 / +19 | conflict noted only (F6) |

**(1) Role check.** E reuses the shared helper (packages/shared/src/security/keyRevokePolicy.ts:140, `PLATFORM_ROLES` at :60) and does not write a new list, so there is no reuse defect. It is the same predicate that security/index.ts, originate certifications.ts:169 and adminConfig.ts:999 use.
- The helper refuses anything that is not a string. It folds case for ASCII letters only, then looks the result up with `Set.has`, which cannot match a prototype key.
- Probe `g47-{billing,nft}-shapes.test.ts` runs the real routers over HTTP with 56 role shapes and 7 shapes of the user object itself. It checks each answer against an oracle written separately (`/^(SYSTEM_ADMIN|SUPER_ADMIN)$/i`, no u flag, so non-ASCII letters never fold to ASCII).
- At head, billing ran 64/64 and nft 63/63 (the oracle self-check is billing-only).
- Admitted are exactly the ASCII case variants of SYSTEM_ADMIN and SUPER_ADMIN.
- Refused with 403, the body unchanged, and the mock never called:
  - leading or trailing space, tab, LF, NUL, ZWSP, BOM, a hyphen in place of `_`, no separator, PLATFORM_ADMIN, ADMIN, OWNER, ORG_ADMIN in any case, empty string;
  - look-alikes: long-s, dotless ı, dotted İ, fullwidth, Cyrillic Е, Greek Α, an NFD combining mark;
  - `__proto__`, `constructor`, `hasOwnProperty`, `toString`;
  - arrays (flat, nested, two elements), null, undefined, 0, 1, NaN, true, false, `{}`, an object with toString, an object with toPrimitive, a String object, a Symbol, a function, a BigInt, a Set, a nested `{role}`;
  - req.user that is a string, null, an array, a number, or a null-prototype object with OWNER.
- A role getter that throws answers 500 with the generic body. That fails closed.
- Shapes are recorded in `rows_{billing,nft}_head.json`.
- One shape is admitted: `role` inherited through the prototype chain. JSON-decoded JWT claims are always own properties, so I consider it unreachable. I did not check the JWT library itself.
- **Positive control.** The same probe against the base product files gives 12 FAIL per service. Base admitted OWNER, ORG_ADMIN, `['SYSTEM_ADMIN']`, a toString object, a String object and a null-prototype OWNER (`rows_*_base.json`). So base also failed open on arrays and objects, and this PR closes that as well. Files restored and sha256 asserted (head_sha256.txt).

**(2) Other routes in the two files** (instrument: every route listed, then a grep for `req.user`).
- billing.ts: :626 is the only role check. The only other reads of `req.user` are :144 and :186, where checkout takes the customer from the principal.
- nft.routes.ts: :709 is the only role check. :232 reads the reader identity.
- Neither file has another route that admits OWNER or ORG_ADMIN through a role list. No other route in either file carries a role check, though some should (F3, F4).
- Same service, other file: webhooks.ts:243 `requireRole('SYSTEM_ADMIN','SUPER_ADMIN')` already excludes OWNER.
- The gateway (api-gateway proxy.ts:1184, :1233) only authenticates. It applies no role gate of its own.

**(3) Effect on legitimate platform admins.**
- SYSTEM_ADMIN is still admitted. SUPER_ADMIN and lowercase spellings are newly admitted.
- Callers that lose access are OWNER, ORG_ADMIN, and array/object role shapes. ORG_ADMIN's removal is decision D2.
- No frontend calls either route: a grep of frontend/** for `admin/credits` and `platform-fee` returns 0 hits; the same grep finds both in the services and the spec.
- The spec already says 403 "Admin role required" for both routes. The 403 body is unchanged: base-passing cells assert it, and mutant M12 is killed.

**(4) Red-first, suites and mutants**
- Red-first (Spark deterministic run): base 8 pass / 6 fail, head 14/14, in each service. The 6 that fail on base are OWNER, ORG_ADMIN, array, system_admin, SUPER_ADMIN, and B8 (400 instead of 403).
- Suites at head, `--maxWorkers=2`, one at a time: billing 11 files / 113/113, nft-certificate 14 files / 121/121. Both match E.
- `tsc -p` (built-in tsc, no emit): billing 0 errors, nft 0 errors. Positive control: an injected TS2322 is caught in both (F2).
- Mutants: 12 per route, 24 in total (`probes/mut1855/`, unique anchor, sha256 restored after each: billing 2d291b2a…, nft ad7582ee…). **E's tests kill 24 of 24.**
  - The set: truthy-role, list+OWNER, +ORG_ADMIN, String() coercion, full toUpperCase, exact case, SYSTEM_ADMIN only, trim+toString, validate-before-auth, dropped `return`, negated check, changed body.
  - My probe kills 22. It passes "validate first" because it sends only valid bodies. E's B8 kills that one.

## FINDINGS
- **F1 Note (y/n: n; correct the PR text and docs). Cell counts are wrong; the totals are right.** E says "16 cells each" and "existing billing 97 / nft 105". `vitest list` gives 14 tests in each new file and 99 / 107 existing (113 / 121 listed, which matches the suite runs). Red-first is 6 of **14**.
- **F2 Note (n). E's "billing tsc 10 pre-existing errors" does not reproduce.** I get 0 at head under the service tsconfig, and the positive control shows tsc is reporting. The likely cause is a different program: E says "with the test files in the program", or a stale shared build. This does not affect the change.
- **F3 Major, pre-existing, outside KS-1850 (n; open a ticket under KS-486).** Many billing routes take a caller-supplied customer or object id and check neither ownership nor role, so any authenticated user (OWNER) can act on another customer's data. Instrument: static read only, nothing exercised.
  - :658 POST /credits/use spends credits from **any** customerId.
  - :265 / :286 / :309 / :335: read, update, and look up a customer by email.
  - :464 / :488 / :592: purchases and invoices.
  - :515 / :531 / :548 / :572: setup-intent, list payment methods, set the default, detach.
- **F4 Minor, pre-existing (n).** nft.routes.ts :532 and :557: any authenticated caller can pin or unpin any CID.
- **F5 Info (n). The meaning of "platform admin" differs between components.**
  - auth users.ts:193 and oauth.ts:1166 count `admin` and `super_admin` as platform roles.
  - The admin UI types the role as `'admin'|'super_admin'` (authStore.ts:17).
  - webhooks.ts:243 compares case-sensitively.
  - `isPlatformRole` refuses `admin`. Base also refused it, so this is not a regression; only the definitions are out of step.
- **F6 Note (DOCS HOLD).** `git merge-tree --write-tree` against develop cb2320368 conflicts in both Projects Documents html files. The code files merge clean.

**NOT TESTED:** a real JWT (RS256/HS256) through `jwtAuthenticate`, where the stand-in middleware sets req.user; the gateway in front of the services; a running stack; real Stripe or the cost estimator (mocks only); F3/F4 by probe (static read only); E's tsc run with tests in the program; the Akto, Schemathesis, Playwright and k6 suites; the html docs content; deploy.

## HOW
- Clone: `git clone --shared --no-checkout` from gate 46's clone into the non-existent `repo/`, toplevel asserted, then remote set to Secuura/Distributed_Secuura with the Blockchain deploy key as core.sshCommand and push URL `no_push_qa_gate`.
- Fetched refs/pull/1855/head and develop, then a detached checkout of 9fc7fb14.
- Setup: `npm ci` (1806 packages) and a build of @secuura/shared only.
- Tools: vitest via `npx --prefix <svc> vitest run --root <svc> --maxWorkers=2`.
- Probes were copied into `src/__tests__` only for their runs, then moved to `probes/_quarantine_2026-10-31/` (not deleted). `git status` is clean afterwards.
- Base controls swapped in the base product files and restored them, with the sha256 asserted.
- No git write verb was run in /Volumes/DevMASTER/!CODING/**. Every process I started has exited.
- Instrument faults: the first rows dump went to console (vitest swallowed it), so it now writes a file; the first prototype-row assertion was rewritten so that row is recorded rather than failing the run; a hook refused a `$R` variable form, so I re-ran with literal paths.

## Spark shadow (`spark_gate.sh` once per service, work dirs in the session scratchpad, `--node-modules` set; `spark_review.py`; copies in `probes/spark/`)
- Its deterministic facts match mine exactly: 8/6 to 14/14 in both services.
- Its review gave GO WITH NOTES for both, with 8 Notes each and no Major.
- What it got wrong:
  - It fetched the ticket as "fetch failed: IndexError" (the same fault as in gate 46).
  - It flagged E's suite, mutant and tsc claims as "unmeasured in facts". That is true of its own instruments, and I measured all three here.
  - It said B8 does not prove auth runs before validation. That is false: mutant M9 is killed by B8 in both services.
  - It said the 403 body is not compared with the old code. That is weak: the cells that pass on base assert the same body, and M12 is killed.
- What it missed: the cell miscount (F1), F3, F4, F5, and the base fail-open on array and object roles.
