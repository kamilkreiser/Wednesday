**Kam's ruling, option (a), verbatim** (card `secuura-ks1369-gateway-proxy-crash-guard-shape`, `ruled_ts` 2026-09-29T09:06:10.516709+10:00):

> **[a] Return early when the request was already sent (Recommended)** — One guard at the top of the hook: if the outgoing request's headers are already sent, skip the header writes. Smallest change; the ticket's first direction.

## TIER 1, and why

The hook writes `Authorization` at `routes/proxy.ts:296`. The ticket is Urgent, and the measured production symptom is a **13-restart, 11,362 × 502 outage**. One guard at the top of `onProxyReq`: if the outgoing request's headers are already sent, return before the header writes.

2 files, +65/−0 — the guard and a new cell file. No existing cell is re-pinned.

## Test Evidence

Re-measured on this rebased head against develop `2cb858335472`, not carried from the pre-merge base:

| | baseline at develop | this branch |
|---|---|---|
| `services/api-gateway` | 88 files / 795 tests, 0 failed | **89 files / 798 tests, 0 failed** |
| `tsc` api-gateway | 0 errors | 0 errors — **delta 0** |

**Red-first, test half applied ALONE with the product file asserted unchanged against develop** (measured: 0 differing product files): `services/api-gateway` **rc 1 — 1 file failed, 2 tests failed**, 88 files / 796 tests passing.

The previous seat reported this as "2 failed / 3 (H1, H2)" counting the new file's own three cells; **2 over the whole suite is the same measurement on a different denominator**. Both figures are correct.

⚠ **`packages/shared` is rebuilt (`npm run build -w @secuura/shared`) before every arm in this harness.** It does not affect this branch, which touches no shared source — but the same harness produced a **false red** on a sibling branch that does, because shared is consumed as built dist and both arms silently loaded develop's code. The tell was that the two arms returned *identical* counts, which cannot happen for a working red-then-green pair.

**Arms, carried as the previous seat's measurement at `8af6ab82` and named as such** — the diff is proved byte-identical across the rebase (`cmp` rc 0), so they still hold:
- **A1** guard removed → 2 failed / 3.
- **A2** guard **moved below the first `setHeader`** → 2 failed / 3. So its **position is load-bearing**, not merely its presence. That is the arm that distinguishes this fix from a guard that happens to sit in the file.

**A correction the previous seat made to its own correction, and it belongs here rather than as a criticism of the source README:** the README says "five header writes", and reading the source suggests seven. **Seven is a property of the source; five is a property of the fixture.** The control cell's expected list is the calls a *login* request actually triggers — `set X-Request-ID`, `set Authorization`, `set Content-Type`, `set Content-Length`, `write` — because the vouch and policy headers are conditional. The README was not wrong.

**Rebase evidence:** cut at `8af6ab82`, rebased onto `2cb858335472` after #1339 merged. `cmp` of the stored pre-rebase diff against the post-rebase diff is **rc 0, byte-identical**; patch-id equal as corroboration only. No conflict — #1339 and this branch share **zero** files.

**Push preflight: 12 of 15 legs ran, 3 skipped (legs 3, 4, 8 — local stack not up), nothing failed.** 12/15 is not a pass and is not quoted as one.

## Chain note for the gate

**This PR and the KS 1359 one both add a test file to `services/api-gateway`.** Each is measured against the new develop **alone**, so once either merges the other's suite count moves by the first's cells. The gate declares the chain; neither figure above anticipates the other merging.

## Not covered

- No load run; the k6 crash the ticket cites is not reproduced here.
- The client-visible result of an early return is not measured — the guard prevents the crash, and what the client receives on that path is unasserted.
- No built images and no local stack, so **a §5f live sweep is owed**. Nothing is deployed by this PR.

Refs KS-1369
