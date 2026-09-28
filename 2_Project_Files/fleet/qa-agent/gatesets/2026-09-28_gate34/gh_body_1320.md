#1320 KS-692: restrict vc-issuer status writes to the platform roles
head b9111f2bfad28f1bd63e787ae69a2de6b71a2d11

## What this changes

`STATUS_WRITE_ROLES` in `services/vc-issuer/src/routes/status.ts` included `ISSUER_ADMIN`. A status
list lives in a **process-local Map with no owning tenant**, so there is no tenant to compare a caller
against — which means an `ISSUER_ADMIN` in **any** tenant could revoke or un-revoke **any** tenant's
credential. Dropping `ISSUER_ADMIN` closes that until lists carry an owner, at which point it returns
together with a per-list ownership check.

**Kam's ruling, verbatim** — card `secuura-ks692-status-revoke-interim-posture`, option **a**
(2026-09-16 15:04 AEST): *"Narrow now, bind-creator later"*. Verified at source in the decision record,
where the card reads `ruled_choice: a`.

This is an **authorization change**, so it is deliberately narrow: one role removed from one
`as const` list, plus the header comment that documented the old posture.

`Refs KS-692` — deliberately not a closing keyword. The gate decides the ticket move.

## The rewritten comment makes a factual claim, so I checked it

The old header said tenant scoping was "tracked on KS 586". The new comment says that ticket is Done
and no longer tracks this. **Verified at source: KS 586 is `Done / completed`.** Had it not been, this
PR would have shipped a false pointer into the repo — so it is stated here as a measurement, not an
inherited assertion.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/vc-issuer/src/routes/status.ts` (**+8/−4** — one role removed, comment rewritten)
- `Blockchain/Dev/services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts` (new, **+81**)

**Ran — all by me, in this branch's own worktree at base `ec32c40e2b1e`, `npm ci` and `packages/shared` built**
- **RED-FIRST**, test applied alone with the product untouched: **2 failed / 3 passed / 5**. The reds are
  `A1` (the write gate holds the platform roles and nothing else) and `A2` (an `ISSUER_ADMIN` is refused
  403 on revoke **and** on unrevoke).
- **GREEN**, product hunk applied: **5 passed / 5**.
- **Whole `services/vc-issuer` suite: 15 files / 140 tests / 0 failed** (`rc 0`). "No NEW red" rests on
  **0 failed**, not a delta.
- **Lint (`eslint src`, which this package does have): rc 0** — 1 message, 0 errors, and **identical at
  base and at this head**, measured by putting the base blob in place with my test held aside. My two
  files contribute **0 messages**.
- **`tsc`, both ways:** the package's own `tsc --noEmit` **rc 0, 0 errors**; an **including** program
  (`exclude: []`, 455 files, `--listFilesOnly` confirming my cell once and `routes/status.ts` once,
  bogus-filename control 0) reports **4 errors, none in my files**, and the error set is **identical at
  base and at this head**. They are the `VCCredentialStatus` `TS2339` family in
  `credentialRepo.test.ts` (`revoked`, `revocationReason`, `revokedAt`) — **already filed as KS 1351**
  by the previous seat. **This PR adds none.**

**NOT run**
- No local stack: the four platform suites (Schemathesis · Akto · Playwright · Performance/k6) and the
  vc-issuer integration path did not run.
- **No live-tenant usage census** beyond the caller scan the decision card already records (see below).

**Migrations + config**
- **None.** One role removed from a literal list, a comment rewritten, one new test file.

## NOT COVERED — and one item here is a real cost, not a caveat

- 🔴 **Tenant admins lose status writes** until the owner column lands. **That is the ruled cost**, not
  an oversight: it follows directly from option **a**. Anyone holding only `ISSUER_ADMIN` can no longer
  revoke or un-revoke, including for their own tenant's credentials. **No live-tenant usage census was
  run** beyond the card's caller scan, so the number of callers actually affected is not measured here.
- Tenant scoping still **cannot** be enforced at this layer — the Map has no tenant linkage. This PR
  narrows *who* may write; it does not make the write tenant-aware. That is the "bind-creator later"
  half of the ruling and is **not** done here.
- The sibling file's own header comment still references the old ticket; this change does not edit that
  file.

⚠ The brief's OPEN DOUBTS list opens with *"No Spark round was run."* — **stale, and not carried**: the
run exists, `checker.out` records **9 PASS / 0 FAIL**, its A4/A5 figures (2/5 red, 5/5 green) are exactly
what I reproduced, and the run's `patch.diff` is byte-identical to the golden. Fifth README in this set
carrying that line; each was written minutes before its own round.

## Provenance

Patch produced by the local model (Spark) under a Wednesday brief, then re-verified here: the READY's
fenced diff block is **byte-identical** to the checker's canonical `patch.diff` (5476 bytes both; a
one-character mutation control differs), both `section_*.opts` name the plain `.diff`, and both sections
strict-apply clean at `ec32c40e2b1e`. Every figure above is one I measured.

## Push gate (in-hook preflight, from this push's own raw log)

`pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** ·
`run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** ·
`OK — 13 code guards passed.` · `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` ·
`^FIXTURE BUILD FAILED` **0**. `gatelines32`: **MATCHES the declared fleet STOP condition**. Push rc 0;
origin head re-read afterwards and equal to the commit (`b9111f2bfad2…`).

