KS-1293 HERMETIC-UNPINNED: no cell in the originate suite pins the hermetic property KS-1266 established — reverting ks1213's env line stays green
state In Progress

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

- [ ] a regression that removes or overrides `ANCHORING_SERVICE_URL` in any of the seven files **reds** the originate suite
- [ ] the port-1 shape is covered too: a change back to a Fetch-spec bad port is caught, not silently accepted

## SEARCHED BEFORE FILING

Literal census over **1,282** KS issues (archived included) and **3,625** comments: `127.0.0.1:2` → **1** hit (KS-1266 itself); `ANCHORING_SERVICE_URL` → 8, none owning this property; `hermetic` → 7, none this; `no cell pins` → 17, a generic phrase rather than this finding. Controls: `KS-1263` → 3 (so the instrument matches), a nonsense token → **0** (so it discriminates). **Unfiled.**

## PROVENANCE

Tier-2 gate `2026-09-25-batch1215-t2-r1` on #1221 (KS-1266), verdict GO with this as a disposition (`NEW: HERMETIC-UNPINNED (TICKET)`). Filed by Seat L1 on Wednesday's instruction of 2026-09-25 05:36:36Z, after the merge of #1221 as `9e744421ada2166c8944764017cad76d94737286`.

Refs KS-1266.
