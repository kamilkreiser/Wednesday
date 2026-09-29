**Kam's ruling, option (a), verbatim** (card `secuura-ks1360-wallet-session-delete-reply-shape`, `ruled_ts` 2026-09-29T09:06:07.259189+10:00):

> **[a] Add success: true to the reply (Recommended)** — The code conforms to the published contract and to its own 404 shape. Additive, so existing callers that read message keep working.

`DELETE /api/wallets/session/{sessionId}` answered 200 with a body that omitted `success`, while the published contract and the route's own 404 shape both carry it. It now carries `success: true`.

**Additive by design:** nothing is removed or renamed, so a caller reading `message` is unaffected.

2 files, +76/−1 — the product change and a new cell file. No existing cell is re-pinned.

## Test Evidence

Measured at develop `0aa9b52c691b`:

| | baseline at develop | this branch |
|---|---|---|
| `services/wallet-connector` | 7 files / 45 tests, 0 failed | **8 files / 48 tests, 0 failed** |
| `tsc` wallet-connector | 0 errors | 0 errors — **delta 0** |

**Red-first, test half applied ALONE with the product file asserted unchanged against develop** (measured: 0 differing product files): **rc 1, 1 file failed, 1 test failed**.

**Arms, carried as the previous seat's measurement at the original base and named as such** — the branch's diff is proved byte-identical across **both** rebases (`cmp` rc 0 against the originally stored pre-rebase diff):
- **A1** remove `success: true` → 1 failed / 3.
- **A2** set `success: false`, key still present → **1 failed / 3**. So cell D1 pins the **value**, not merely the key's presence. Without A2, a change to `false` would pass.

## A declared risk in this branch's own fixture, and what it would mean

The new cell mocks `../db` with an `initDb` that **never settles** — the service boots at import, so the mock has to stand in for it. The source notes flag worker teardown as unmeasured.

**So a hang or a leaked handle on this suite is a finding, not a flake**, and it is stated here before anyone hits it rather than after. On this head the suite completed normally: 8 files / 48 tests, rc 0, with no hang, no timeout and no "did not exit" or open-handle warning in the run.

**eslint, run at this head: rc 0 with zero output on both changed files.** An empty result is ambiguous on its own — it reads the same whether the linter was clean or never ran — so it is established rather than inferred: both target files were asserted present first, and a control run of the same eslint against a file with a known warning does print `1 problem (0 errors, 1 warning)`. The silence is a clean result, not a silent command.

## Rebase evidence — this branch was rebased twice

Cut at the pre-bump develop, rebased onto `2cb858335472` when the advisory bump merged, then again onto `0aa9b52c691b` when the baseline re-date merged. **`cmp` against the originally stored pre-rebase diff is rc 0 — byte-identical across both moves** — with patch-id equal as corroboration only. The invariant checked is that the branch's own change never altered, not merely that the last rebase was clean. No conflict at either step: this branch shares zero files with both merges.

**Push preflight: 12 of 15 legs ran, 3 skipped (legs 3, 4, 8 — local stack not up), nothing failed.** 12/15 is not a pass and is not quoted as one.

## Not covered

- Worker teardown for this suite, as the source notes state.
- No built images and no local stack, so **a §5f live sweep is owed**. Nothing is deployed by this PR.
- Other wallet routes' reply shapes are unchanged and unasserted here.

Refs KS-1360
