# QA GATE — Datasec/NexusAI RD-361 **ROUND 3**, `rd-361-round3-s44` @ `2f4896d`. **TIER 1.**

**Charter first, in full:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/CLAUDE.md`
(T9 seat — DevMASTER is not mounted; every path here is a T9 path.)

## Why this round exists, and what that means for your bar
Round 2 was **NO GO on a Blocker**: an interrupted first run **permanently bricked a fresh
deployment**. **Kam bent his own two-round cap to authorise this round**, narrowly — the Blocker plus
one line of test plumbing, nothing wider. So: **a finding that the fix is incomplete or wrong is
exactly what this gate is for. A finding that the change is narrower than you would have made it is
not** — narrowness is the commission.

## 1. Target — four SHAs, four different facts
- **Branch:** `rd-361-round3-s44` · **Head:** `2f4896d`
- **Cut from `1149d1c`** (round 2's head), **not** the campaign tip — verify that ancestry yourself.
- **Round 2 head `1149d1c`** is the before-state for the Blocker repro.
- 🔴 **Do NOT diff against `main`** (248 commits behind — RD-367).
- **Diff:** 3 files — `backend/services/authEnforcement.js`, `__tests__/auth-gate-fail-closed.test.js`,
  `scripts/verify-expected-counts.json`. Builder reports **2177/2177 across 113 suites, jest exit 0.**
- **Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files` — **read-only to
  you**; work in your own clone.
- **NON-PROD. NO DEPLOY. NO `az`. Do not contact `nexusai-staging` or the demo.** Kam's production
  lift is **Secuura only**.

## 2. 🔴 THE CENTRAL QUESTION — reproduce the Blocker at `1149d1c`, then prove it gone at `2f4896d`
The builder handed you the exact repro. **Run it on BOTH heads — the before-state is the control:**

    DATA_DIR=$(mktemp -d); export DATA_DIR
    npm start            # open /first-run-setup — it serves. Do NOT complete setup.
    ^C ; npm start       # restart against the SAME directory = the interrupted first run

**At `1149d1c` boot 2 must FAIL** — 503 on `/api/setup/status`, `/api/admin/health` and
`POST /api/auth/enforce`, and `/first-run-setup` 302 to `/login`. **At `2f4896d` boot 2 must SERVE.**
**If the before-state does not fail, your instrument is wrong, not the world — stop and say so.**

**🔴 The builder pre-empted a false control and it is right:** `/api/health` returns **200 on both
heads**, so it cannot discriminate. **Do not use it as the instrument.**

## 3. THE DISCRIMINATOR — audit the reasoning, and audit the REJECTED candidate too
**Chosen:** `authEnforced` is written at exactly one site (`server.js:3349`) and the very next
statement (`:3350`) writes `firstRunComplete: true`; the disable path writes both (`:15426`/`:15427`).
So **`authEnforced` present ⇒ `firstRunComplete` present**, and the contrapositive is the fix.

**Verify the premise, because the whole fix rests on it:**
1. **Is `authEnforced` really written at exactly ONE site?** Sweep the whole tree, not the two files —
   and say what your sweep covered, including the extension list.
2. **Can the two ever be written apart?** A crash, an early return, or a partial write between `:3349`
   and `:3350`. If they can diverge, the implication fails and the gate reopens.
3. **Does it fail CLOSED?** The builder says it relaxes only on positive evidence — a readable,
   plain-object settings file with no `firstRunComplete`. **Test unreadable, unparseable, non-object,
   null, array, and a file that reads as `{}` on a volume that has stored things before.**

**The REJECTED candidate is part of the evidence and worth checking:** the builder considered *"no
authorized users means auth was never enforced"* and **rejected it after reading the route** —
`POST /api/auth/enforce` validates the four Entra settings and **not** the user list, so
`authEnforced: true` is reachable with zero users. **It says it had written that fix in its head
before reading the route, and that it would have been wrong in the product's favour and green in the
suite.** Confirm the rejection is correct: had it shipped, would the suite have caught it?

## 4. THE F-B HALF — cell D must drive the REAL fallback
Round 2's cell D hand-set `store.dataDirFallbackActive = true`, so it proved a reader reads a property
of that name and **could not prove `jsonStorage` ever sets it** — red-proof M10 flipped the sole
producer and the suite stayed **20/20 green, blind**. **Re-run that exact mutation against round 3:
flip `jsonStorage.js:847` and the cell must now go RED.** If it stays green, F-B is not closed.

## 5. THE SHAPE THAT PRODUCED THE BLOCKER — hold the new cells to it
Round 2's negative control asserted *"a genuine first run still OPENS, or setup is bricked"* by
constructing **one** `JsonStorage` on a fresh directory — **true at boot 1, false at boot 2.**
**A cell that constructs its subject ONCE cannot see a property that only appears on the second
construction.** Check that round 3's cells construct the subject **twice** where the property is a
second-boot property. **A round-3 cell with a single-boot fixture reproduces the exact defect this
round exists to fix.**

## 6. Evidence rules — mandatory
1. Every cell: **what it MOCKS and therefore cannot prove.**
2. **Both controls on every negative claim** — positive (your instrument fires) **and** negative (an
   impossible pattern), so a zero is vouched-for. **A positive control on the INSTRUMENT ITSELF where
   the instrument might not reach the subject** — 404/blank/timeout means BLIND, never "absent".
3. **Assert each tamper LANDED before asserting its effect.** **A uniform non-zero across variants is
   as suspect as a uniform zero** — establish the command RAN before reading its exit code.
4. **Counts:** confirm 2177/113 and that the delta matches cells that actually ran; report skips.
5. **No screenshots are expected** — the builder changed no screen and **refused to manufacture any**,
   which is correct. What renders differently is *whether the first-run pages serve at all on boot 2*.
6. **Never delete.** Cleanup means quarantine. **Findings-only — you never fix.**

## 7. Verdict
**GO** · **GO-with-findings** · **NO GO**. Severity yours, priority Wednesday's. **This is a
Kam-authorised extra round on a capped class**, so if you find the Blocker still open, say so plainly
and name precisely which case survives — that goes straight back to him, not into another round.

Report to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Datasec RD-361 round 3 (@ 2f4896d, tier 1)`.

PROVENANCE:
- branch `rd-361-round3-s44` @ `2f4896d`, cut from `1149d1c`, 3 files, 2177/2177 across 113 suites, the repro, the `/api/health` caveat, the chosen discriminator and the rejected candidate | the builder's mail `STATUS: READY FOR QA — RD-361 round 3`, 2026-09-07T09:25:34Z, re-read from the inbox in this action | read 2026-09-07. **The SHAs are the builder's read; re-derive them yourself.**
- round 2's Blocker, F-B and M10 | the round-2 gate verdict mail, 2026-09-07T07:41:43Z | read 2026-09-07
- Kam's authorisation of a third round | his panel ruling `nexusai-rd361-blocker-vs-nogo-cap => round3`, 18:58:10 | read 2026-09-07
- production lift is Secuura-only | Kam, panel 12:07 + 12:10 | read 2026-09-07
- **UNMEASURED by Wednesday:** every claim above about the round-3 code. Wednesday has read none of the changed lines.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 19:29
