# BLUF

**The tier-1 gate scored RD-516 at `f4264e5` with the security property CLOSED AND PROVED, and the
branch NOT CLEARED TO MERGE.** Those are two separate verdicts and neither one implies the other.
**No reader may record this round as clearing the merge.**

Your round is **five small, fully-specified corrections on `rd-516-ai-test-ssrf-s73`**. Every one is
already RULED by Tuesday, so do not re-derive any of them — but the rulings do not all rest on the
same strength of evidence, and you should know which is which. **F-1 was re-measured by Tuesday at
source rather than accepted from the report. F-2, F-3 and F-4 are the GATE's measurements, which
Tuesday ruled on without re-measuring.** If one of those three does not reproduce when you touch it,
**that is a finding — stop and mail me**, do not quietly correct it to match this brief.
**Do not re-run the gate's proved measurements** (§3 of the acceptance list names them). Round ends at **READY FOR QA**. No merge. No deploy.

**Why the merge still waits, so you do not chase it:** the branch's own §5 acceptance clause is
unsatisfied — the 28 seam-dependent cells are not on `main`. **That is a different seat's branch,
live right now (S74/RD-574), and it merges BEFORE you.** Nothing you do here closes it.

# YOUR FIVE ITEMS

## 1. F-1 (MAJOR) — CORRECT THE FALSE HEADER. This is what gates the merge.

`backend/services/aiEndpointPolicy.js`'s own header claims ai-config's Azure branch *"calls it too,
so (C-54) holds BY CONSTRUCTION"*. **Nothing calls it.** Measured by Tuesday at `f4264e5`:

- the **only** require in the whole backend is `server.js:16580`, inside ai-test
- `checkEndpointName` has **zero external callers** — its three hits are its definition `:180`, its
  own internal use `:222`, its export `:251`
- **ai-config still runs its inline regex** `^https://[a-zA-Z0-9-]+\.openai\.azure\.com/?$` at
  `server.js:~16414` — one suffix, https only, no port

**Fix: correct the header sentence. Nothing else.** A false claim stated as holding *by construction*,
in a tier-1 security module's own header, is what the next reviewer will rely on instead of reading
the code. Cheapest fix on the branch, highest value, and it is the one the gate named as gating merge.

🔴 **DO NOT WIDEN ai-config TO USE THE POLICY.** Wiring it changes what a **SAVE** path accepts
(1 suffix → 4, https-only → the policy's rule). That is a behaviour change on a different route,
needing its own cells and its own gate. **It is scope this ticket was not given, and it is the same
shape as the limiter collapse S73 correctly refused.** If you find yourself one line from doing it
because it is obviously right — that is the moment the rule is for.

## 2. F-1 part three — FILE THE DEFECT AS ITS OWN TICKET.

**There is a real, concrete customer defect behind that false header, and it must not die with the
header correction.** A Gov customer on `cognitiveservices.azure.us` — which IS on the policy's
sourced list — can **TEST successfully and can NEVER SAVE through the wizard.**

**It is not a security regression** (the dial-time policy runs on every ai-test call however the value
was stored) and saying otherwise overstates it. File a ticket carrying:
- the ai-config wiring **and** the Gov-customer save defect
- **C-41's "ONE PLACE" as still unachieved** — the rule is written twice and can drift; that is
  RD-462's shape, which this project has already paid for once
- **C-54 as now known-false in BOTH directions and untested**

⚠️ **C-54 also needs a CLARIFICATIONS correction — SUPERSEDE, NEVER DELETE — and that IS yours**, as
the project agent. It is not Tuesday's to write. **The relay is not done until the C-number comes
back to me.**

## 3. F-2 (MINOR, IPv6) — ONE REPLACE.

`http://[::1]/`, `[fc00::1]` and `[::ffff:192.168.8.37]` all audit as `HOST_NOT_ON_SOURCED_LIST`
instead of their true address class, because `new URL().hostname` **keeps the brackets** and
`net.isIP('[::1]')` is `0`.

**Refusal is still correct in every one of those cases — zero dials, identical body.** The loss is
purely the operator's audit log, which is *exactly the defect this branch just fixed for IPv4*.

**Fix, ruled:** `net.isIP(url.hostname.replace(/^\[|\]$/g,''))`

⚠️ **Note in your READY that this makes `unmap()` reachable on that path again**, and say whether you
checked that path. A one-line fix that re-enables a code path is two changes.

## 4. F-3 / F-4 (MINOR) — CORRECT THE §4 MUTATION TABLE IN THE IN-REPO BRIEF.

- **M-R12 reddens THREE cells**, not one: **R12, R12-provenance, R10ii.**
- **M-R8's direction is INVERTED today.** R8 is **already red** for RD-541, so deleting a mount takes
  it red → **GREEN**.

**Why this is not cosmetic:** a later reader applies M-R8, sees green, and records a *failed mutation*
— concluding the suite does not detect the thing it does detect. **That is a trap that produces a
confident wrong answer**, which is worse than a gap.

## 5. §8 — NEW-1 IS NO LONGER "UNCLASSIFIED". CORRECT THE LINE.

The gate brief's §8 still describes NEW-1 as unclassified. **S73 deliberately deferred this** because
committing would have moved the head the gate was measuring. **That condition is discharged — the
verdict has landed.** The correct text:

NEW-1 is **IN the set (making it 28)**, classified by READING: `ai-config-aoai-save.test.js:160-161`
drives ai-test anonymously at `http://127.0.0.1:${refusing}` and asserts `200`/`azure-openai`; a
caller-named loopback literal → `ADDRESS_LOOPBACK` → 400. **It needs `RD516_HOSTS` only — no
`RD516_INTERCEPT`, no listener, no seam** — and that suite **spawns the server itself**
(`spawn(process.execPath,[SERVER])` at `:62`), so its preload wires as `-r <preload>` in the spawn
args. **It will look different from the other four; that is not a mistake.**

# WHAT STAYS OWED — DO NOT CLOSE THESE, DO NOT BUILD THEM

- **F-5 (informational): the R16 mutant SURVIVES.** The Private Link relaxation can gain a fourth
  conjunct and the whole 31-cell suite is indistinguishable from baseline. §7 already owned R16 as
  unwritten; it now has a number on it. **Stays owed, with its three conjunct flips.**
- **R3 stays unwritten, and it must NEVER be built on the interception seam** (RD-584) — that would
  test the harness against itself.
- **R7, R8, R10(i)** stay visible and unfixed — RD-585, RD-541/C-106, RD-583.

# 🔴 THE UNDICI QUESTION IS RULED AND CLOSED. DO NOT REOPEN IT.

**Kam, panel, 2026-09-21 08:31:55, verbatim:** *"Decision
nexusai-rd516-undici-dependency-for-address-pinning: c — Ship WITHOUT pinning; ticket the rebinding
window (Recommended - already in force tonight)"*

So: **RD-516 ships layers 0-2 with NO address pinning.** RD-584 carries the rebinding window.
**Option (2) — reaching into undici internals — is REFUSED PERMANENTLY.** If a fix you are writing
starts to want a pinned address, stop and mail me; do not take the dependency.

# 🔴 DISJOINTNESS — THREE NEXUSAI SEATS ARE LIVE. THE FLOOR IS PARTITIONED BY FILE.

| seat | branch | owns |
|---|---|---|
| **you** | `rd-516-ai-test-ssrf-s73` | `backend/services/aiEndpointPolicy.js` + the in-repo gate brief |
| S74 / RD-574 | new, off `main @ 60c76d7` | `__tests__/` for rd464, rd486, rd523, rd545, ai-config-aoai-save + `__tests__/helpers/rd516-net-harness-preload.js` |
| RD-518 fix round 2 | its own | `backend/server.js` · `backend/encryptionService.js` · `docs/runbooks/local-run-for-qa.md` + its own cells |

**Stay inside your row.** You share an INBOX with the other two seats — mail addressed to them will
appear in it. **Read the addressee line before acting on anything; a commission that does not name
your branch is not yours.** If you want a file in another row, stop and mail me. It is never worth
one line.

⚠️ **S74's branch will add `__tests__/helpers/rd516-net-harness-preload.js`, which already exists on
YOUR branch byte-identical. That collision is intended and is a no-op. Do not "resolve" it by
changing the file.**

# HOW THIS ROUND IS ACCEPTED

1. **PRIOR WORK section, or the READY comes back (C-49).** Read what already exists before you write:
   the policy module's history, the gate brief, and CLARIFICATIONS for every C-number named above.
2. Every correction above, done. **Five items — name each one and what you did.**
3. **The measurements you must NOT re-run:** the 26 refusal classes, the absence clause, the
   105/105-on-main control. The gate proved all of them and said so explicitly.
4. **Say what you did NOT do and why** — particularly ai-config, which you are being told to leave.
5. READY FOR QA to Tuesday. **No merge, no deploy, no real Azure.**

# RULED BY KAM, NOT YET IN AN ARTEFACT

- **The undici dependency: ruled (c), ship without pinning** (08:31:55 today, quoted above). It was
  already in force, so nothing is redone — but it is ruled, and this brief is where it lands for you.

PROVENANCE:
- the tier-1 gate returned the security property CLOSED and the branch NOT CLEARED TO MERGE, its §5 acceptance clause unsatisfied | its verdict mail to tuesday-agent at 2026-09-20T15:02Z and the gate's own frame | read 2026-09-21 by Tuesday
- checkEndpointName has zero external callers and its only require is server.js:16580 inside ai-test | measured at f4264e5 by Tuesday at source, not accepted from the report | read 2026-09-21 by Tuesday
- ai-config still runs its own inline regex at server.js approximately 16414, one suffix, https only, no port | measured at f4264e5 by Tuesday at source | read 2026-09-21 by Tuesday
- the IPv6 fix is net.isIP on the hostname with brackets stripped, and refusal is already correct in every case | the gate's F-2 finding, ruled FIX IT by Tuesday | read 2026-09-21 by Tuesday
- M-R12 reddens three cells and M-R8's direction is inverted because R8 is already red for RD-541 | the gate's F-3 and F-4 findings, ruled CORRECT THE TABLE by Tuesday | read 2026-09-21 by Tuesday
- NEW-1 is in the set and needs RD516_HOSTS only, its suite spawning the server itself at line 62 | S73 classified it BY READING ai-config-aoai-save.test.js and Tuesday accepted it over the gate's inference | read 2026-09-21 by Tuesday
- Kam ruled the undici card option c, ship without pinning | his panel message on the Tuesday tab at 2026-09-21T08:31:55 | read 2026-09-21 by Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 09:10
