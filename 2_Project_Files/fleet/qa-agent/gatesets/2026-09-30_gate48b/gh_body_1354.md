## BLUF
Two advisories published 2026-09-29 refuse **every** push from `develop`. One is **fixed** (js-yaml moves
off the vulnerable range); one is **accepted as a temporary exception** on the date this baseline already
shares, with the working measured from the built artefact. Two files.

Refs KS-470

## Why both audit legs were refusing every push
`GHSA-r3ph-w7gj-g6xm` (js-yaml, moderate) and `GHSA-r53p-7pc4-xj5r` (undici, low) were **published on
2026-09-29** — 17:57:39Z and 18:22:07Z, from the GitHub advisory API. Neither is caused by any change in
flight: the commit that first hit the refusal touches two shell files and **zero lockfiles**, and the two
lockfiles the gate names are byte-identical between the base and that head. A push at 21:07Z failed
**leg 7** only; the same gate re-run at 21:15Z also failed **leg 6**, which reported 23 advisories at push
time and 24 eight minutes later — npm's quick-audit feed lagged the bulk endpoint leg 7 uses.

## 1. js-yaml — FIXED, not accepted
`systemTest/performance/package-lock.json`: `js-yaml` **5.2.3 → 5.4.2**. The advisory's first patched
version is 5.4.1 and the manifest already requests `^5.2.1`, so **no manifest change** is needed, and the
patched line is already in use in this repo (`systemTest/api-explorer` pins 5.4.1, `systemTest/akto` 5.4.2).

**Measured on the real lock, not a scratch copy:** entries **274 → 274**, **MOVED=1, ADDED=0, REMOVED=0**,
zero non-version field changes, `lockfileVersion` 3 both sides, and the `secuura-observability` link entry
byte-identical (`resolved: "../../observability"`, `link: true`).

⚠ **Two deviations from the documented remediation, both measured and both disclosed:**
1. **The verb.** `scripts/preflight/lockfile-cleanroom.sh:120` prints
   `docker run --rm -v "$PWD/<dir>":/app -w /app node:24-alpine npm install --package-lock-only
   --ignore-scripts`. **That command is inert here** — measured in a scratch copy: MOVED=0, ADDED=0,
   REMOVED=0, js-yaml still 5.2.3, because `npm install` keeps any pin that still satisfies the range. The
   container, `--package-lock-only` and `--ignore-scripts` are the script's; only the verb changed, to
   **`npm update js-yaml`**.
2. **The mount.** The script's per-directory mount **fails**: `npm error code EMISSINGTARGET — Missing
   target in lock file: "../observability" is referenced by "node_modules/secuura-observability" but does
   not exist`, rc 1, **lock unchanged**. That manifest carries `"secuura-observability":
   "file:../../observability"`, so a per-dir mount cannot see the target; mounting the parent
   (`-v "$PWD/systemTest":/app -w /app/performance`) gives rc 0. **So the command that leg 7's refusal points at
   cannot regenerate this lock** — and the cleanroom script itself checks 35 locks, none under `systemTest/`,
   so it never clean-rooms this one either — ticketed separately, not fixed here.
   A scratch dry run reported 273 entries because the copy lacked that link target; the real regen reports
   274, and 274 is the figure quoted above.

## 2. undici — ACCEPTED, temporary, on the date this file already shares
One row for `GHSA-r53p-7pc4-xj5r`: `package: undici`, `ticket: KS-470`, `decidedAt: 2026-09-30`,
**`expires: 2026-10-09`**. It joins the **2026-10-09 re-triage date this baseline already carries on four rows** — now five — rather than taking a fresh one. It is a **new acceptance on that shared
date, not a re-date** of any row dated by a signed instruction; those four are untouched.

**The working, measured FROM THE ARTEFACT rather than the manifest:**
- The pin is undici 5.29.0, reached only via
  `frontend/issuer → @meshsdk/core → @meshsdk/provider → @utxorpc/sdk → @connectrpc/connect-node`
  (which declares `undici ^5.28.3`).
- **The built issuer image serves 58 files from nginx with ZERO `node_modules` directories anywhere in the
  image**, and `undici`, `connectrpc` and `connect-node` each occur **0 times** in the served tree —
  **positive controls `react`=27 and `secuura`=8 fired in the same grep**, so the search is not blind. The
  Dockerfile is multi-stage and its final stage copies only `/app/dist/`.
- **undici is pinned in 0 of the 27 service standalone locks** (all 45 tracked locks parsed, 14,924
  package entries — the control that the parser sees anything).
- **No Dockerfile copies the workspace-root lock**: every image copies a per-directory manifest, so the
  root lock's own undici entry reaches no image either.
- **No patched version exists inside `^5.28.3`** — the newest 5.x on the registry is 5.29.0 itself — so
  this cannot be closed by a lock bump.

**Why temporary and not permanent:** the 12 sibling undici rows carry no `expires` **because they are
listed in `GRANDFATHERED_NO_EXPIRY`** in `scripts/audit/baseline-contract.mjs`, not because a new row may
omit it. Measured: that set holds 17 ids, 12 of the 13 undici rows among them; the contract test asserts
the no-expiry set equals it **exactly**, and refused a 13th that "arrived by omission". A permanent
acceptance is a gate change and a reviewer decision, so this row is temporary instead. **No gate file is
touched by this PR.**

## Test Evidence
All rc's read on their own line, never through a pipe.

| check | before this PR | with this PR |
|---|---|---|
| `npm run audit:contract` | **rc 0** at develop | **rc 0** |
| `npm run audit:gate` (leg 6) | **FAIL**, 24 reported / 25 baselined | **rc 0**, 24 reported / 26 baselined |
| `npm run audit:locks` (leg 7) | **FAIL**, 20 match / 18 baselined | **rc 0**, 19 match / 19 baselined |

🔴 **The two leg-7 numbers move for different reasons, which is what separates a fix from a suppression:**
*matches* fall **20 → 19** because the js-yaml pin moved **off** the vulnerable range, and *baselined*
rises **18 → 19** from the one accepted row. Had both been baselined, matches would have stayed at 20.
Rows with no `expires` stay at **17**, the base's figure, so the grandfather set still matches exactly.

## NOT COVERED — stated, not hidden
- **The real undici fix is not in this PR.** An unscoped `overrides` entry (the pattern
  `frontend/issuer/package.json` already uses for `jsdom`) moves undici 5.29.0 → 7.30.0 and would close
  this row **and all 12 siblings**; sized 2026-09-30 in a scratch regen at **723 → 721** entries
  (`@fastify/busboy` removed, the nested jsdom copy deduped). **Its build and suites are UNMEASURED**, and
  it forces a major version against a declared `^5.28.3`. Ticketed separately.
- **This PR adds one more entry lapsing at 2026-10-09**, taking that date from four rows to five.
- The two dead rows leg 6 reports as no longer reported (`GHSA-v2v4-37r5-5v8g`, `GHSA-mwp4-54f8-5fhr`) are
  **not removed here** — one of them is on the 2026-10-09 date, so removing it moves that count.
- `mobile/secuura-app` pins undici 6.28.0, which is also vulnerable to this advisory. That tree is the
  declared out-of-scope one and leg 7 excludes it by design. Untouched.
- No service image was built or run; nothing was deployed. The only image built was the issuer, for the
  artefact measurement above, and nothing was pruned or removed.
