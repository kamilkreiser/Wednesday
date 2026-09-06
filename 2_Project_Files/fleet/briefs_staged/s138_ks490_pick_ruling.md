## BLUF
**KS-490 pick RATIFIED; RULED: build (1) — the FIVE runtime-stage Dockerfiles — as ONE PR on a NEW branch off develop re-read (`e08472c6ef44ccede29001a64fdba5f4b5a20c0b` at 11:5x, verified by Wednesday); then (2) the governance dev tree as its OWN PR; then (3) the stale Azure pointer as its OWN small PR with the live values read from the client CLAUDE.md, no deploy. The two register corrections are the right kind of finding and are scored. KS-856 received — seat B builds it. #845 stays HELD under its tier-1 gate (verdict ~12:20).**

## 1. (1) — the five Dockerfiles (auth, nft-certificate, referral, staking, vc-issuer)
- **Measure before removing:** for EACH of the five, prove argon2 (and anything else the runtime `apk add` served) is built in the builder stage and copied — a runtime `apk add` that the builder stage does NOT cover is the thing that breaks a service at boot. State per service what the toolchain was there for.
- **The change:** drop `python3|make|g++` (and whatever else the sweep names) from every stage after the last `FROM`. One mechanical change × 5, one commit or five — your call, one PR.
- **Red-proof, predicted first:** a guard asserting no `apk add` of a compiler after the last `FROM` in every service Dockerfile — RED at the parent (5 hits; control 24 Dockerfiles enumerated) and GREEN at the head. **PLACEMENT (the partition rule):** `scripts/` is seat B's family — if the repo's existing Dockerfile checks live under `scripts/`, the guard is NAMED on the ticket as a follow-up for that partition and your PR carries the five Dockerfiles alone; if a `__tests__` home exists outside `scripts/` (read first), put it there. Do not write into `scripts/`.
- **Driven leg, if cheap:** `docker build` ONE of the five locally and boot its health route from the built image (docker is up on this Mac); else NOT-TESTED by name in the READY — the gate decides the rest. Tier at READY: expected tier 2 through-code with that one image as the driven cell.
- **NOT in this PR:** anything outside the five runtime stages; E-1 (`APP_DB_PASSWORD`, KS-762 — Kam's coordination, correctly not taken); E-5 → KS-769 (correct).

## 2. (2) then (3), each its own PR
- **(2) the governance dev tree:** the runtime-import check FIRST — which dev dependencies does the runtime `require()` (measure by booting the built image or by a static import walk over the runtime entry) — then `--omit=dev` in the runtime install or a prune before the copy. A dev dep that the runtime imports is the finding, not a reason to skip.
- **(3) the stale Azure pointer (`main.parameters.json:17,25`):** the tenant it names was decommissioned 2026-06-25 and is DEAD — never log into it. The live values come from the client `CLAUDE.md`'s Founders Hub section (read it at the time of the edit; never from memory or from this mail). Two lines, no deploy, stated on the ticket as a template correction — a deploy is Kam's word and is not asked for here.

## 3. The register corrections and the method note — scored
E-5 "FIXED" with its third lockfile never re-checked; 1 → FIVE Dockerfiles with a 24-file control — both understating, both found by re-reading the register against the tree. And two of your OWN zeros caught by their controls (the port regex; the workflows at the repo root, not under `Blockchain/Dev/`). **That is the fleet's rule stated by its own case: a zero without a control is not a reading.** Score for the register pass: 1.0 (micro, read-only). Your keeper is right; keep it.

## 4. State, from Wednesday's seat
develop **`e08472c6ef44ccede29001a64fdba5f4b5a20c0b`** (seat B's #842 merged 11:4x; parents `3dffe10d6…` + `8286e5d1d…`; tree `9a02a91a3…` — verified at origin, no fetch). **#845 @ `87450b54c…` HELD** under `QA/Secuura-s138-ks843-half2` (launched 11:39). KS-856 filed (read on your word; seat B's to build). Nothing on the demo; no deploy; never `--no-verify`; never delete a branch; handovers to Peter are test blocks from Kam.

PROVENANCE:
- develop `e08472c6e…` with parents and tree | `git ls-remote origin` + `git cat-file -p` over the shared object store from Wednesday's seat, NO fetch | read 2026-09-06 11:5x
- Seat A's mail (KS-856; the pick; the register rows with their controls; the three proposals; no branch cut) | `[Secuura/Blockchain -> Wednesday] KS-856 filed; pick = KS-490 (Review E) …` 2026-09-06T01:47:33Z, read whole | read 2026-09-06 11:5x
- Seat B's merge receipt (#842 → `e08472c6e`) | 2026-09-06T01:45:33Z, read whole; verified above | 11:5x
- The dead Secuura tenant (decommissioned 2026-06-25, never log in) and the Founders Hub as the live one | the workspace `CLAUDE.md` hard rule 4 (read at Wednesday's boot) — the exact ids are for the agent to read from the client `CLAUDE.md`, not copied here | boot
- The partition (seat B = `scripts/` + harness; seat A = product) | Wednesday's 10:1x seat-B brief + the category-1 list (`projects_index/entries/Secuura__Blockchain.md`) | 11:2x

SELF-CHECK: re-read end-to-end | 2026-09-06 12:02
(checked: the ruling picks ONE of the three and sequences the other two as their own PRs, each with its measurement-first step; the partition rule keeps `scripts/` out of seat A's hands; the Azure pointer's values are pointed at the client file, not asserted; the develop tip is Wednesday's own read; consistent with the 11:42 mail (continue on a NEW branch off develop; KS-856 for seat B's partition; #845 HELD); no NexusAI content.)
