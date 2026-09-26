--- comment 5835435987 by linear[bot] at 2026-09-25T16:01:03Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1293/hermetic-unpinned-no-cell-in-the-originate-suite-pins-the-hermetic">KS-1293 HERMETIC-UNPINNED: no cell in the originate suite pins the hermetic property KS-1266 established — reverting ks1213's env line stays green</a></summary>
<p>

## BLUF

**KS-1266 stopped seven originate unit files reaching the network, and nothing in the suite would notice if that regressed.** The tier-2 gate on #1221 measured it: revert `ks1213`'s `ANCHORING_SERVICE_URL` line and the suite stays **green**. The property was proved by an **external probe**, not by a cell, so it is protected by nobody once the PR is merged.

## What #1221 established, and how

Seven files under `services/originate/src/__tests__/` now set `ANCHORING_SERVICE_URL` to `http://127.0.0.1:2` at import scope. Measured with a `--require` probe recording every `dns.lookup` and `net.connect`, bare vs patched, **157 tests green on both sides**:

|  | DNS `anchoring` | TCP `anchoring:4005` | TCP `127.0.0.1:2` |
| -- | -- | -- | -- |
| bare | **17** | **17** | 0 |
| patched | **0** | **0** | **26** |

The probe is not blind in either direction: 8 lookups of `127.0.0.1` on both sides. **But none of that lives in the suite** — it was an out-of-band measurement, and the suite's own 863 cells are indifferent to it.

## Why it matters more than it looks

The failure is **silent and slow**. A future edit that drops or overrides the env line puts the unit suite back on the host's resolver: it still passes, just non-deterministically and with a DNS lookup per anchoring call. That is precisely the state KS-1266 was filed to end, and it would return without any red.

It also erodes the port-1 half: `ks1228` and `ks520` were on `127.0.0.1:1`, which undici refuses **before opening a socket**, so their "closed port" never happened. Nothing pins that they must not drift back.

## Fix shape (the owner's call)

1. **A cell per file, or one shared helper cell**, asserting the module-scope base is a refused loopback port — cheap, but it pins the CONFIG rather than the PROPERTY.
2. **One probe-backed cell**: run the anchoring-touching files under a `dns.lookup` spy and assert **zero** lookups of a non-loopback host. That pins the actual property (hermeticity) and would red on any regression, however it arrives. It needs the probe to live in the repo rather than in a seat's scratch.
3. Keep it out of the suite deliberately and record that hermeticity is asserted only at the gate — honest, but then it must be written down somewhere a reader will find.

(2) is the one that matches what the ticket set out to guarantee.

## Done when

- ☐ a regression that removes or overrides `ANCHORING_SERVICE_URL` in any of the seven files **reds** the originate suite
- ☐ the port-1 shape is covered too: a change back to a Fetch-spec bad port is caught, not silently accepted

## SEARCHED BEFORE FILING

Literal census over **1,282** KS issues (archived included) and **3,625** comments: `127.0.0.1:2` → **1** hit (KS-1266 itself); `ANCHORING_SERVICE_URL` → 8, none owning this property; `hermetic` → 7, none this; `no cell pins` → 17, a generic phrase rather than this finding. Controls: `KS-1263` → 3 (so the instrument matches), a nonsense token → **0** (so it discriminates). **Unfiled.**

## PROVENANCE

Tier-2 gate `2026-09-25-batch1215-t2-r1` on #1221 (KS-1266), verdict GO with this as a disposition (`NEW: HERMETIC-UNPINNED (TICKET)`). Filed by Seat L1 on Wednesday's instruction of 2026-09-25 05:36:36Z, after the merge of #1221 as `9e744421ada2166c8944764017cad76d94737286`.

Refs KS-1266.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1293-pin-the-originate-unit-suites-hermeticity-in-the-suite-itself-abfe7c8a040e">Review in Linear</a></p>

--- comment 5841703762 by kksecura at 2026-09-26T00:53:01Z
## FIX ROUND 1 of 2 — B-1261-1 REVERT-SKIPS, new head `0b2fdbb1b8195d4f73467508f8eb6a4c3781b81a`

Fast-forward on this branch; the author has wrapped, so this round is another seat's work and the
history before this commit stays its author's. **No merge-in** — the base this worktree **contains**
is still `fa25c9b10fb4`.

### The circularity
The subject set was `if (!src.includes(ENV_KEY)) continue` — **which files mention the key**. Deleting
the env line the cell exists to catch therefore also deleted the file from its own subject set. Two of
the nine subjects (`ks1228`, `ks1264`) carry **no second mention** — measured, `grep -c` = 1 each — so
for them one deleted line is the whole of it.

### Two halves, and an arm proves each is necessary
1. **An explicit nine-file manifest.** A subject that stops pinning is an offender **named by file**,
   whether the line was deleted, the assignment nested, or the file renamed.
2. **The base must be an IMPORT-SCOPE assignment, read from the TypeScript AST.** `ks1213` assigns the
   key inside `finally` blocks at `:341` and `:356` as well as at `:30`, so deleting `:30` left a text
   reader still finding a base — but a nested assignment runs **during a test**, not at module load,
   and does not pin the phase this cell is about.

The AST is used rather than a column-0 regex because indentation is a formatting accident and prettier
is free to change it; `sf.statements` is the language's own answer to "is this top level".

**Neither half alone is sufficient, and that is measured rather than argued:**

| arm | tamper | reds (exact) |
|---|---|---|
| **circular** | restore ONLY the mention-derived subject rule | **RS1, RS2** |
| **anyassign** | restore ONLY the text reader | **RS3a, MECHANISM** |
| **base** | both = the rule exactly as at `eab8d7031b1b` | **RS1, RS2, RS3a, MECHANISM** |
| **emptymanifest** | hand the scan an empty manifest | **CONFIGPINNED** (the non-vacuity floor) |

### MANIFEST-DRIFT — the other direction
A new anchoring-touching file that nobody adds to the manifest is **also** an offender. Without it the
manifest could silently cover less of the suite than its name implies as the suite grows.

### The RS cells do not tamper the real files
RS1/RS2/RS3a drive the scan against **copies in a temp directory** with the import-scope line removed,
so they reproduce the gate's revert exactly without touching a tree another seat may be reading. Each
has a **paired CONTROL on the same untouched file**, because a cell that reds on a stripped fixture
also reds for a scan that calls everything an offender.

### N-1261-a NODNS-EGRESS, same round
The dns spy answered non-loopback names by **delegating to the real resolver**, so the pin itself sent
a live `getaddrinfo` off-host on every originate run — and inside the compose network, where the name
resolves, it made a real request to a live service and `rejects.toThrow()` failed: a red that is both
false and noisy. The spy now answers non-loopback names itself. **Loopback still reaches the real
resolver**, because the second arm's `ECONNREFUSED` must be a genuine socket-level refusal rather than
something the spy invented.

### Test Evidence
Base this worktree **CONTAINS**: `fa25c9b10fb4` (`merge-base --is-ancestor` YES), no merge-in.

| suite | result |
|---|---|
| the ks1293 cell | **10 / 10** (was 2) |
| originate **BARE** at `eab8d7031b1b` | **75 suites / 871 tests / 0 failed** |
| originate **PATCHED** | **75 suites / 879 tests / 0 failed** |
| `packages/shared` | **47 files / 930 tests / 0 failed** |
| `tsc --noEmit` | **rc 0, zero `error TS`** |

⚠ **On that `packages/shared` figure:** it is **930**, not the 941 seen on newer bases. That is the
BASE, not a regression — this branch contains `fa25c9b10fb4`, which carries **47** shared test files
against **48** at `4db87c3e4b98` (`walkTimeouts` landed between them), and this change touches **zero**
files under `packages/shared`. Measured, because a number that looks wrong is worth explaining before
someone else has to.

Push gate `28/0 · 6/0 · 49/0 · 60 of 60`; preflight **12/15 legs ran, 3 SKIPPED (3, 4, 8 — no local
stack), nothing failed** — not quoted as a pass.

### NOT covered
- **N-1261-b FINALLY-RESTORE-UNPINNED** is not built — the gate graded it non-blocking by reach.
- **N-1261-c** is a squash-body instruction, not a code change: the squash body must un-hyphenate the
  foreign keys. This commit's message hyphenates **only KS-1293**, audited before committing.
- `*.integration.test.ts` is still outside this config, as the file's own NOT-COVERED note states.
- Legs 3, 4, 8 NOT run. No database. No deploy.

