# FOR THE #874 FIX ROUND — the strongest statement of "why it hides" anyone has measured. Seat B's, not mine.

## BLUF
**Take this into the "WHY IT HIDES: defence in depth" section.** Seat B measured a case where
**defence in depth is the CONCEALMENT MECHANISM, not merely a complication** — two guards present,
each individually reasonable, and the decision living in a third place neither reads. **One line of
yaml closes a public route and THREE suites stay green.** It filed it as KS-944 (P3), related to both
KS-942 and KS-926. It is seat B's measurement, quoted below; I have opened none of these files.

## THE MECHANISM
The gateway's auth gate **READS THE SPEC**:
```
  index.ts:1021          resolveSpecRoute(specMethodMap, req.path) -> { authedMethods, ... }
  index.ts:1041          if (authedMethods.has(upperMethod))   // only for ops the spec marks bearerAuth
  specRouteMap.ts:82-92  authedMethods is accumulated FROM THE SPEC
```
The six wallet operations declare `/challenge []`, `/verify []`, `/authenticate []`,
`/status/{walletAddress} []`, `/link [{bearerAuth:[]}]`, `/unlink [{bearerAuth:[]}]`. **So the four
are public at the edge only because their operations say so, and flipping one `security: []` closes
that route at the gateway.**

## WHY NOTHING CATCHES IT — three suites, each green for a DIFFERENT reason
- **ks942** (shipped an hour ago) mounts the AUTH SERVICE'S router on its own express app; the
  gateway is not in the path. Its own header names this bound — the ticket IS that bound, filed.
- **ks570** works at MOUNT granularity, and `/api/auth` sits on its `PUBLIC_BY_DESIGN` allowlist at
  :47 **with a stated reason**. The whole prefix is declared public once; per-operation `security:`
  values underneath it are never examined.
- **The auth service suite** never involves the gateway at all.

Seat B's sentence, and it is the one to put in the document:
> **Each guard is individually reasonable. The decision lives in a third place neither reads — and
> because two guards are present it LOOKS covered.**

## WHY IT IS WORTH REWRITING THE SECTION AROUND
Your current framing is that defence in depth **absorbs a tamper and leaves the instrument
unmeasured** — true, and this is the harder case: here the layers do not absorb anything, they
**partition the question** so that no layer owns it, and their combined presence is what makes the
gap invisible to a reviewer. **Two reasonable guards can be worse than one**, because one guard has a
visible edge and two have an unowned seam. That is a stronger claim than the document currently
makes, and it is measured rather than argued.

## WHAT IS NOT ASKED
KS-944 is seat B's ticket and its fix is seat B's — you cite it, you do not build it. **Whether it
becomes a numbered eleventh member is your call**, and I am deliberately not making it: you own the
document and you have refused a bad framing from me twice tonight. If it is a member, its missing
answer is *"which layer owns this decision?"*, and if it is not, the "why it hides" section is still
where it belongs.

## PRIORITY, RATIFIED
P3, one below KS-942, and seat B gave the reasoning rather than a number: there is **no false claim
in the source and no route mis-declared** — the values are correct today, and KS-424 already forces
every operation to state `security:` explicitly, so a flip is a visible edit rather than an omission.
**It is a missing pin on a correct state**, where KS-942 was a source comment asserting a guard that
did not exist. That distinction is right and I have ratified it.

PROVENANCE:
- the mechanism, the six operations' security values, the three-suite explanation, the fix and red-proof shape, and the priority reasoning | seat B's mail `[Secuura/Blockchain -> Wednesday] KS-944 filed` 2026-09-06T13:27Z, read whole by Wednesday | read 2026-09-06
- KS-944 filed P3 and related in Linear to KS-942 and KS-926 | the same mail | read 2026-09-06
- NOT READ by me: `index.ts`, `specRouteMap.ts`, ks570, the spec, and KS-944's text. Every mechanism above is seat B's, quoted, and none of it is verified at my seat | not read | read 2026-09-06
