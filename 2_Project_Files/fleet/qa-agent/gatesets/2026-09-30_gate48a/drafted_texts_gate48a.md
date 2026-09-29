# gate48a DRAFTED TICKET TEXTS — VERBATIM from Seat B 47th's record folder (READ ONLY), DRAFTED, NOT FILED

Read 2026-09-29T22:02:19Z by drafts_gate48a.py from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-47th/ks470. The READY names these files but does not carry the texts (a finding for the gate: Wednesday's leg-7 ruling said "Put the ticket text in your READY"). The seat files them under the board identity only AFTER the merge, on the GO (its handover, 21:56Z). The gate returns each as POST AS-IS / POST AMENDED (with the amended text in full) / DO NOT POST, after checking every factual line as a ROW with evidence.

## override — the undici override follow-up (13 accepted advisories; the unscoped override; build + suites UNMEASURED)
- file: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-47th/ks470/TICKET-DRAFT-override.md
- SHA256 (file bytes): c8404eafca2790f6cec7eae24efe3e13b895feb73900b9aaaa97cab56b217c31
- 2308 chars, 30 lines | DRAFTED-NOT-FILED header: True | the READY names the file: True | the READY carries the title: False

```
<!-- DRAFTED, NOT FILED. Filed under the board identity only after the gate. -->
**Title:** undici under @connectrpc/connect-node: 13 accepted advisories close with one unscoped override

**Priority:** High — it retires 13 baseline rows, one of which now lapses 2026-10-09.

`undici` 5.29.0 is pinned via `frontend/issuer -> @meshsdk/core -> @meshsdk/provider -> @utxorpc/sdk ->
@connectrpc/connect-node`, which declares `undici ^5.28.3`. **13 advisories whose range includes 5.29.0
are accepted in the audit baseline** — 12 permanent (grandfathered, tickets KS 470 and KS 559) and
GHSA-r53p-7pc4-xj5r, added 2026-09-30 as a temporary exception **expiring 2026-10-09**.

**No lock bump can close them.** The newest 5.x on the npm registry is 5.29.0 itself (dist-tags latest is
8.x), and `npm update undici --package-lock-only` moves nothing — measured 2026-09-30 in a scratch copy:
MOVED=0. The advisory's first patched version for that line is 6.28.1.

**An unscoped `overrides` entry does close them, and the mechanism is already in that manifest.**
`frontend/issuer/package.json` carries `"overrides": { "ip-address": "^10.5.1", "jsdom": { "undici":
"^7.29.1" } }` — the existing undici override is **scoped to jsdom only**, which is exactly why the
top-level pin stays at 5.29.0. Adding an unscoped `"undici": "^7.29.1"` moves 5.29.0 -> 7.30.0. Sized
2026-09-30 by a dry lock-only regen in a scratch copy, the real lock untouched: **entries 723 -> 721**,
`@fastify/busboy` 2.1.1 removed (it was undici 5.x's dependency), the now-redundant nested
`jsdom/node_modules/undici` deduped into the top level, 1 moved. The workspace-root manifest carries the
same kind of block and would need the same entry.

**UNMEASURED, and it is the work of this ticket:** whether the issuer image still builds and its suites
still pass under that override. It forces a **major** version on a transitive dependency against its
declared `^5.28.3`. Note that undici ships nowhere — measured 2026-09-30 from the built artefact: the
issuer image serves 58 files from nginx with zero `node_modules` directories and zero occurrences of
`undici`, `connectrpc` or `connect-node`, with positive controls `react`=27 and `secuura`=8 firing in the
same grep — so the risk is to the build and the test suites, not to the served product.
```

## cleanroom — the cleanroom script's remediation command (per-dir mount EMISSINGTARGET; npm install inert)
- file: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-47th/ks470/TICKET-DRAFT-cleanroom.md
- SHA256 (file bytes): 9441b243a02700974c765259d2d67c616a4eb1552767a12d0062b3d4dc8fdffc
- 2126 chars, 32 lines | DRAFTED-NOT-FILED header: True | the READY names the file: True | the READY carries the title: False

```
<!-- DRAFTED, NOT FILED. Filed under the board identity only after the gate. -->
**Title:** lockfile-cleanroom.sh prints a remediation command that cannot regenerate one of the 43 locks it polices

**Priority:** Medium — it sends a reader to a command that fails.

`Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh:120` prints, for every lock that fails its
clean-room check:

    docker run --rm -v "$PWD/<dir>":/app -w /app node:24-alpine npm install --package-lock-only --ignore-scripts

**Two measured problems with that line, both hit on 2026-09-30 while regenerating
`systemTest/performance/package-lock.json`:**

1. **The per-directory mount cannot work for a lock with a `file:` link outside the directory.** That
   manifest carries `"secuura-observability": "file:../../observability"`, and the command fails:
   `npm error code EMISSINGTARGET — Missing target in lock file: "../observability" is referenced by
   "node_modules/secuura-observability" but does not exist`, rc 1, lock unchanged. Mounting the parent
   (`-v "$PWD/systemTest":/app -w /app/performance`) succeeds, rc 0.
2. **`npm install --package-lock-only` is inert for moving a pin off a vulnerable range.** Measured in a
   scratch copy of that directory: MOVED=0, ADDED=0, REMOVED=0, `js-yaml` still 5.2.3, because
   `npm install` keeps any pin that still satisfies the manifest range (`^5.2.1` here). The command that
   moves it is `npm update <package> --package-lock-only`, which produced MOVED=1, 5.2.3 -> 5.4.2, with
   nothing else changing.

So a reader following the printed line on an advisory-driven regen gets either a hard failure or a silent
no-op, and a silent no-op is the worse of the two: the lock is unchanged and the gate still refuses, with
nothing saying why. Suggested shape: make the mount the repository root or the lock's parent when the lock
contains a `file:` link that escapes the directory, and print `npm update <package>` when the reason for
the regen is an advisory rather than a clean-room failure.

**Measured on:** `develop` at `37205947ddd2775a72a417beb5b7ac8e3240fbf3`, npm 11.19.0 in `node:24-alpine`.
```

