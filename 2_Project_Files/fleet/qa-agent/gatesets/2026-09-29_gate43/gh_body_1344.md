**Kam's ruling, option (a)** (card `secuura-ks1359-platform-audit-log-bounds`, `ruled_ts` 2026-09-29T09:06:03.955357+10:00):

> **[a] Refuse wrong-type and below-minimum values with 400; keep the KS 5 cap for too-large ones (Recommended)** — Garbage and negative inputs get a clear 400; very large values still clamp quietly as KS 5 chose. One product file.

⚠ **One deliberate alteration to that quote, disclosed:** Kam wrote that ticket key in its hyphenated form. A hyphenated key in a PR body **attaches that ticket in Linear**, so it appears above un-hyphenated, as `KS 5`. The words are otherwise verbatim.

(That sentence was itself rewritten: the first draft quoted the hyphenated spelling in order to explain avoiding it, which would have attached the ticket anyway — the explanation reintroducing the very thing it describes. The key scan refused the post and named it.)

`GET /api/platform/audit-log` accepted wrong-type and out-of-range `limit` / `offset` values. It now refuses them with 400. **The KS 5 clamp for too-large values is unchanged** — that behaviour was ruled deliberately and this PR does not touch it.

2 files, +89/−0 — the product guard and a new cell file. No existing cell is re-pinned.

## Test Evidence

Re-measured on this head against develop `0aa9b52c691b`, not carried from either earlier base:

| | baseline at develop | this branch |
|---|---|---|
| `services/api-gateway` | 88 files / 795 tests, 0 failed | **89 files / 802 tests, 0 failed** |
| `tsc` api-gateway | 0 errors | 0 errors — **delta 0** |

**Red-first, test half applied ALONE with the product file asserted unchanged against develop** (measured: 0 differing product files): `services/api-gateway` **rc 1 — 1 file failed, 4 tests failed**.

The previous seat reported "4 failed / 7 (B1–B4)" counting the new file's own seven cells; over the whole suite it is the same four.

**Arms, carried as the previous seat's measurement at the original base and named as such** — the branch's diff is proved byte-identical across **both** rebases (`cmp` rc 0 against the originally stored pre-rebase diff), so they still hold:
- **A1** neuter `badInt` → 4 failed / 7.
- **A2** raise the offset minimum from 0 to 1 → **the offset-0 control reds**. So the *minimum itself* is load-bearing, not merely the presence of a guard. That is the arm that distinguishes this from a check that happens to reject something.

**eslint: 1 warning, pre-existing.** Proved by **line shift**, not asserted: the same rule and the same message move from `:983` to `:989`, which is exactly the number of lines this patch inserts above them. The new test file reports zero.

## Carried from the source notes, unresolved

The refusal uses `VALIDATION_ERROR` where some neighbouring routes use `BAD_REQUEST`. That inconsistency is carried as stated rather than settled here — picking one would change responses on routes this ticket did not rule on.

## Chain note for the gate

**This PR and the KS 1369 one both add a test file to `services/api-gateway`.** Each is measured against develop **alone**, so once either merges the other's suite count moves by the first's cells. Neither figure above anticipates the other. The gate declares the chain.

## Rebase evidence — this branch was rebased twice

Cut at the pre-bump develop, rebased onto `2cb858335472` when the advisory bump merged, then rebased again onto `0aa9b52c691b` when the baseline re-date merged. **`cmp` against the originally stored pre-rebase diff is rc 0 — byte-identical across both moves** — with patch-id equal as corroboration only. The invariant checked is that the branch's own change never altered, not merely that the last rebase was clean. No conflict at either step: this branch shares zero files with both merges.

**Push preflight: 12 of 15 legs ran, 3 skipped (legs 3, 4, 8 — local stack not up), nothing failed.** 12/15 is not a pass and is not quoted as one.

## Not covered

- No built images and no local stack, so **a §5f live sweep is owed**. Nothing is deployed by this PR.
- Bounds on other platform routes are unchanged and unasserted here.

Also cross-referenced, deliberately un-hyphenated so they are not attached: KS 5 (the clamp this preserves) and KS 662 (the declared-bounds ruling).

Refs KS-1359
