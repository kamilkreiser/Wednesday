#1227 KS-1252 + KS-1253 E7PREFIX: bound the ULID-ish prefix, refuse fourteen credential names, and pin both patterns from the scripts side
head 69a72726e8eee0711a56b782d04936bf647e9160

## What and why

Two defects in E7 — the spec-example guard's only **name-blind** secret rule — plus the first cells that
pin it from the scripts side. One PR: one file changed plus one new suite, and one run of that suite
covers both tickets. KS-1253's own description says *"The same family as KS-1252."*

**KS-1252** (`582ab9e5e`) — `BENIGN_SHAPES`'s "prefixed ULID-ish fixture id" entry was
`/^(?:[a-z]+_)?[0-9A-Z]{20,32}$/`: an **unbounded, name-blind** prefix, so `session_` + 32 upper-case
alphanumerics (40 chars, past E7's floor), `password_` + 32, `accesstoken_` + 32 and a 60-letter prefix
were all silent. Bounded to `{2,12}`, with the same two name guards as `PREFIXED_UUID_RE`.

**KS-1253** (`69a72726e`) — `PREFIXED_UUID_RE`'s deny list admitted **14** credential names, because none
*contains* one of the listed substrings (`sess` is not `session`; `tok` is not `token`). All 14 are now
refused as **exact** prefixes.

**New: `Blockchain/Dev/scripts/__tests__/ks1252_1253_e7_prefix_guard.test.sh`.** Until now the only cells
pinning these two patterns lived in `packages/shared`, so a change to this guard could only be proved
from another workspace — and that workspace is another seat's lane this round. These 8 cells drive the
guard's own exports from beside it and run through `scripts/run-shell-suites.sh`, i.e. **preflight leg
14**, so the boundaries are pinned by a gate that actually runs rather than by a PR body.

## A declared NARROWING — ruled by Wednesday 2026-09-25T02:42:57Z

KS-1253 recommends replacing the deny list with an **ALLOW list of the 13 minted prefixes**. **That is
not available from this lane**, measured before writing anything rather than discovered at leg 14.
`packages/shared/src/__tests__/ks256-spec-example-contract.test.ts` imports this file directly:

| candidate | `ks256` rows | prefix table | `refused===['key']` | the 14 probed names | spec's `anchor_…` |
| --- | --- | --- | --- | --- | --- |
| **current — the control** | 0 mismatches | 0 | OK | **14/14 admitted** | benign |
| **A — the ALLOW list the ticket asks for** | **2 mismatches** | 0 | OK | 0/14 | benign |
| **B — this PR** | **0 mismatches** | 0 | OK | **0/14** | benign |

The **current** row is the harness's positive control: it reproduces `ks256`'s expectations exactly while
showing the defect fully open, so the instrument can both pass and fail. The two rows A would redden are
`['len12','abcdefghijkl_<v4>',false]` and `['credit','credit_<v4>',false]` — each asserting that a
*non-secret-named* prefix stays benign. **KS-1253 stays OPEN** for the allow list, with those two rows
named on the ticket. `credit_` survives here because this file's own comment already records that `cred`
is refused as an **exact** prefix only, and `creds_` is not `credit_`.

## RED-PROOF — of the suite as well as of the fix

The new suite run against three trees:

| tree | result | which cells |
| --- | --- | --- |
| base `6ab9d5021e96` | **6 passed, 2 failed** (rc 1) | both defect cells red, all 6 controls green |
| `582ab9e5e` — KS-1252 only | **7 passed, 1 failed** (rc 1) | cell 1 green, **KS-1253's cell still red** |
| this head `69a72726e` | **8 passed, 0 failed** (rc 0) | — |

The middle row is the independence check: each cell is bound to its own ticket, and neither fix masks the
other.

**What each cell holds, and why the controls are not decoration**

| cell | pins |
| --- | --- |
| 0 | the probe **ran** and produced all **41** rows — a cell list computed from an empty file would pass vacuously |
| 1 | KS-1252: 4/4 of the named shapes FIRE |
| 2 | KS-1253: 14/14 of the probed prefixes FIRE |
| 3 | **the 13 minted prefixes stay silent** — without this, cell 2 is satisfied by a guard that refuses *everything*, which would red the published spec |
| 4 | the three prefixed values the published spec actually carries stay silent |
| 5 | **ks256's `len12` and `credit` rows stay silent** — a future edit here cannot quietly red `packages/shared` |
| 6 | the probe prints **both** verdicts (21 FIRES / 20 silent at head); `key_`, `sk_live_` and a lower-case body still fire; a digest and a bech32 stay benign |
| 7 | an unlisted name yields **no** verdict, so an empty read cannot pass for agreement |

**Published spec, measured at this head** (`docs/openapi/secuura-api.yaml`, 1,345,320 bytes, **1,242**
distinct tokens of 20+ chars): E7 fires on **6** tokens at base and the **same 6** at this head —
**0 new, 0 lost**. Controls: the tokeniser finds a known spec value and does not invent an absent one.

Why that census is here rather than an assertion that "tightening reddens nothing": the ULID-ish entry
matches exactly **2** spec values, both under E7's 40-char floor, and **0** tokens reach E7 exempted only
by it. `PREFIXED_UUID_RE` matches exactly **1** — `anchor_00000000-0000-4000-8000-000000000032`, 43 chars
— and it **does** reach E7 and is exempted **only** by that pattern. **So any allow-list replacement must
admit `anchor` or the guard reds the published spec.** That is the constraint the census exists to find.

## Two defects in the new suite, fixed before it was committed

Disclosed because either would have failed inside the push hook rather than here:

1. The probe used `import { … } from process.argv[2]` — **not valid ESM**. An import declaration takes a
   string literal, so it would have failed to *parse* before it could run. Now a dynamic
   `await import(pathToFileURL(…).href)`.
2. Cell 0 asserted **44** rows where the probe produces **41**. The cell failed rather than accepting the
   miscount, and the count was corrected.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/spec-examples/check/contract.mjs` (the two patterns) and a new
`Blockchain/Dev/scripts/__tests__/ks1252_1253_e7_prefix_guard.test.sh`. No service, no route, no spec
regeneration, no runtime config, no migration, no `package.json`, no lockfile, nothing under
`scripts/audit/` or `scripts/preflight/`, nothing in `packages/shared`.

**Ran:** the three-tree suite matrix above; the spec census base-vs-head; the guard itself
(`node scripts/spec-examples/check-spec-examples.mjs`); `scripts/run-shell-suites.sh`;
`scripts/check-script-portability.sh`; `scripts/preflight/deps-present.sh`. Ratios in the READY.

**NOT run:** preflight **legs 3, 4 and 8** — they need the local platform stack on `:6882`, which by
Wednesday's coordination of 02:44:51Z comes up once at the batch QA gate and is not started mid-round.
**This PR changes a check's regexes and adds a shell suite — no route, no served spec, no runtime
config** — so those legs have no subject here and nothing is owed at the gate. Not "gate green": 12 of 15
legs run, three with nothing to test.

**Effect on leg 14's tally:** this PR **adds one suite** to `run-shell-suites.sh`, so its reached count
rises by exactly one. `ks949_main_seed_idempotence.test.sh` is untouched and its verdict is unchanged.

**Migrations + config:** none.

Refs KS-1252
Refs KS-1253

🤖 Generated with [Claude Code](https://claude.com/claude-code)

