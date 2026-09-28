#1319 KS-908: return connectorId in the key mint 201 body and the keys list row
head 07f42897e2afe381e5f91f54f04225077cf659d9

## What this changes

`POST /api/keys` accepted a `connectorId` and stored it, but **neither the 201 body nor the
`GET /api/keys` row echoed it back**, so a caller had no way to read what it had just set. Two lines,
one per response.

`Refs KS-908` — deliberately not a closing keyword. The gate decides the ticket move.

**Co-file note:** `services/security/src/index.ts` is also the file item 9 of my brief (KS 888 mint — de-hyphenated on purpose; a hyphenated key in a PR body ATTACHES that ticket)
touches, with **disjoint hunks**. That item is **NOT raised by this seat** — it is named UNRAISED in my
handover for a successor on Wednesday's budget ruling. Nothing here depends on it, and the brief-writer
measured that either order applies strictly.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/security/src/index.ts` (**+2/−0**)
- `Blockchain/Dev/services/security/src/__tests__/ks908-connector-id-read-back.test.ts` (new, **+98**)

**Ran — all by me, in this branch's own worktree at base `ec32c40e2b1e`, `npm ci` and `packages/shared` built**
- **RED-FIRST**, test applied alone with the product untouched: **2 failed / 2 passed / 4**. The two reds
  are `A1` (the 201 body returns the `connectorId` it was given) and `A2` (the list row carries it).
- **GREEN**, product hunk applied: **4 passed / 4**.
- **Whole `services/security` suite: 24 files / 251 tests / 0 failed** (`rc 0`). "No NEW red" rests on
  **0 failed**, not a delta.
- **The `keyHash` control is FALSIFIABLE, and I proved it rather than trusting it.** Control `C2`
  asserts neither response carries the key hash. With `keyHash: 'LEAKED-BY-TAMPER'` planted in the 201
  body, **`C2` — and only `C2` — reds** (1 failed / 3 passed). The anchor was asserted to occur exactly
  once before the tamper; the file was restored from a pre-tamper copy with the blob verified equal,
  tamper residue **0**, and the cell re-run green afterwards, so no figure here rests on the tamper run.
  A control that merely passes is not evidence; this one can fail on the thing it is about.
- **`tsc`, both ways:** the package's own `tsc --noEmit` **rc 0, 0 errors**; an **including** program
  (`exclude: []`, 441 files, `--listFilesOnly` confirming my cell once and `security/src/index.ts`
  once, bogus-filename control 0) reports **2 errors, neither in my files** — the same pre-existing
  pair this package carries in `ks952-rate-limit-scope*.test.ts`, which I measured as an identical set
  at base on the sibling PR for KS 747. **This PR adds none.**
- **No spec change is needed, and that is measured, not assumed.** `ApiKeyCreateResponseSchema` and the
  list schema are `.passthrough()` (`security.openapi.ts:345`), so the published contract tolerates the
  new field: **`npm run check:openapi` rc 0** and **the generator produces no yaml diff at all**
  (`git status` on `docs/openapi/secuura-api.yaml` is empty after `generate-openapi`). That is the
  difference from the KS 747 PR in this set, where a `parameters` declaration *does* change the spec and
  a regenerated yaml is a required third file.

**NOT run**
- ⚠ **`services/security` has no `lint` script**, so there is no package lint to report. Not implying one ran.
- No local stack: the ticket's demo-box measurement was not re-run, and the four platform suites
  (Schemathesis · Akto · Playwright · Performance/k6) did not run.
- The `services/security` integration path.

**Migrations + config**
- **None.** Two fields added to two existing JSON responses, plus a new test file.

## NOT COVERED (from the brief's own OPEN DOUBTS)

- **The published schemas are NOT updated.** `.passthrough()` means the contract *tolerates* the field
  rather than *declaring* it. Declaring it is a KS 794-shaped follow-up and is **not done here**.
- The list schema's `keys`-vs-`data` naming is a **separate pre-existing drift**, untouched.
- **No live stack**, so the ticket's demo-box measurement is not re-verified.
- The test signs JWTs with node crypto, as ks742 does; the product change touches **no auth code**.

⚠ The OPEN DOUBTS list also opens with *"No Spark round was run."* — **stale, and not carried**: the run
exists, `checker.out` records **9 PASS / 0 FAIL**, its A4/A5 figures (2/4 red, 4/4 green) are exactly
what I reproduced, and the run's `patch.diff` is byte-identical to the golden. Fourth README in this set
with that line; they were each written minutes before their round.

## Provenance

Patch produced by the local model (Spark) under a Wednesday brief, then re-verified here: the READY's
fenced diff block is **byte-identical** to the checker's canonical `patch.diff` (5969 bytes both; a
one-character mutation control differs), both `section_*.opts` name the plain `.diff`, and both sections
strict-apply clean at `ec32c40e2b1e`. Every figure above is one I measured.

## Push gate (in-hook preflight, from this push's own raw log)

`pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** ·
`run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** ·
`OK — 13 code guards passed.` · `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` ·
`^FIXTURE BUILD FAILED` **0**. `gatelines32`: **MATCHES the declared fleet STOP condition**. Push rc 0;
origin head re-read afterwards and equal to the commit (`07f42897e2af…`).

