#1261 KS-1293: pin the originate unit suite's hermeticity, in the suite itself
head 0b2fdbb1b8195d4f73467508f8eb6a4c3781b81a

## BLUF
KS-1266 stopped the anchoring-touching unit files reaching the network, and **nothing in the suite would have noticed if that regressed** — the property was proved by an out-of-band probe, so once #1221 merged it was protected by nobody. The tier-2 gate measured exactly that: revert one file's env line and the suite stays green. Pinned here, in the suite, with two cells and five red arms.

## Why TWO cells, measured rather than assumed
The ticket has two acceptance criteria and one instrument cannot serve both. Measured on node 24 while writing the cells:

| base | `cause.code` | what actually happened |
|---|---|---|
| `http://127.0.0.1:2` | `ECONNREFUSED` | a socket **was** attempted and refused — the closed port happened |
| `http://127.0.0.1:1` | *undefined* | a **Fetch bad port**: refused *before* any socket, so the closed port never happened |
| a loopback literal | — | **0** `dns.lookup` calls |
| the product default | — | **1** lookup for its non-loopback host — the regression shape |

So a DNS spy **cannot** tell `:1` from `:2`: both are loopback and both produce zero lookups. That is precisely the erosion the ticket's second criterion names.

| cell | carries | how |
|---|---|---|
| `CONFIGPINNED` (static) | **criterion 2** — a drift back to a bad port | every anchoring-touching file in this config sets a loopback host on a port not in the Fetch bad-port list |
| `NODNS` (probe-backed — the ticket's preferred shape) | **criterion 1** — hermeticity itself | with a `dns.lookup` spy installed: zero non-loopback lookups **and** a socket-level `ECONNREFUSED` |

Both assert non-vacuity **before** the property: `CONFIGPINNED` refuses a scan finding fewer than 8 bases, and `NODNS` proves its own spy can fire by first showing the product default *does* produce a lookup.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (new). 1 file, +157. Test-only.

**Ran (all on this head, base `fa25c9b10fb4`):**
- `npx jest --runInBand` (originate): **bare 869 / 869, 74 suites** with the file moved aside, **patched 871 / 871, 75 suites** with it in place — both rc 0, same commit. +2 cells, +1 suite, fully accounted.
- **Five red arms.** Every restore verified by `sha256`; untampered re-run clean afterwards:

  | arm | cell(s) red |
  |---|---|
  | C1 a subject file points at a non-loopback host | `CONFIGPINNED` only |
  | C2 a subject file drifts to a Fetch bad port (`:1`) | `CONFIGPINNED` only |
  | C3 non-vacuity: a subject file stops setting it at all | `CONFIGPINNED` only |
  | N1 the configured base becomes a non-loopback host | `CONFIGPINNED` + `NODNS` |
  | N2 the configured base becomes a Fetch bad port (`:1`) | `CONFIGPINNED` + `NODNS` |

  **The two N arms necessarily redden both cells**, because this file is itself one of `CONFIGPINNED`'s subjects — stated rather than presented as single-cell arms. The three C arms tamper a **different** file and redden only `CONFIGPINNED`, so both cells are shown independently reachable.
- `npm run lint` (= `eslint src`): rc 0.
- `npx tsc --noEmit`: rc 0. Re-run with `exclude: []` and this file asserted present in the program (706 files, `--listFilesOnly`): rc 0.
- `npm test -w packages/shared`: 47 files / **930 tests**, rc 0 — rebuilt first, since `packages/shared` moved in this base.
- Push: rc 0. `pre_push_hook_base` 28/0, `pre_push_hook_base_fixture_guard` 6/0, shell suites 60/0/0 of 60. No `FIXTURE BUILD FAILED`.

**Three errors of mine that only running caught**, recorded because each would have shipped a cell that proved less than it claimed:
1. The static cell first counted **7** bases where the suite has 8 — `ks1213` assigns a **constant**, not a literal, so a literal-only reader would have reported the one file that is *more* readable than its siblings as an offender. It now resolves the constant's own declaration.
2. The probe cell had **no configured base**, because this file did not set one — so it was measuring the regression shape rather than the pinned one. Fixed by making this file hermetic like the other eight, which is also correct in its own right: it runs in the same config.
3. `import * as dns` yields a namespace object whose `lookup` is **getter-only**; assigning it throws `Cannot set property lookup ... which has only a getter`. The mutable exports come from `require('dns')`. A standalone probe of mine had used `require` and worked, which is exactly why the import form's failure was surprising.

**NOT covered:**
- **`*.integration.test.ts` is not scanned.** It runs only under `jest.integration.config.js`, and `ks1263-multi-write-rolls-back.integration.test.ts` currently sets the base to `127.0.0.1:1` — **a bad port, the very shape criterion 2 names.** Correcting it was ruled into the KS-1310/KS-1311 PR, where that file is already open; widening this scan to the integration config belongs with that change, not ahead of it. Both facts are written into the file's own footer so the next reader finds them.
- These cells pin the suite's **configuration** and the configured base's **behaviour**. They do not prove that every anchoring call site in the product routes through that base.
- **Preflight INCOMPLETE — 12/15 legs, 3 SKIPPED** (legs 3, 4, 8 — local stack down). A skip is not a pass.

**Migrations + config:** none.

Refs KS-1293

🤖 Generated with [Claude Code](https://claude.com/claude-code)

