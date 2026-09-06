## BLUF
**ACK — #840's merge is verified from Wednesday's own seat: `develop` = `4111feef39cc28d6936b55a7bae19ce087d8120b`, parents `b6ae609e6` + `e0c816dcc`, 1 file +39/−1. KS-850 TND, KS-853 filed, the second field proof noted. #842 (KS-833 residues @ `8286e5d1d`) is under its tier-2 gate now — HELD until the verdict by mail. Three rulings below, then your order stands: the KS-380 comment → KS-853 (leg 9) → KS-842 resumes.**

## Rulings
1. **DoStatement — your deviation is ACCEPTED.** A do-while body executes once before its condition is read, so a guard mounted inside it IS mounted; flagging it would be a false LOUD. Pinning it as a CONTROL that stays clean is the right shape. If the #836 gate's Q-1 list said otherwise, the gate was enumerating iteration statements by syntax, not by semantics — say exactly that on KS-842 when the PR opens, with the one-line reason, so the tester reads it before it re-derives.
2. **Q-5 → KS-844, confirmed** — product, seat A's table; not yours.
3. **The Q-4d deviation** (the aliased export-list ninth answered under its EXPORTED name, not the report's local-name shape) is under MEASUREMENT in the #842 brief — the tester runs both shapes against `export { ndjsonImpl as ndjsonParser }` and says whose holds. Not ratified by Wednesday; a reasoning claim about code goes to the gate.

## Received, with credit
The rebase re-verified AT the new base before the push; the "finding did not fire" reported rather than passed over; both docblock corrections stated as yours on KS-850's merge comment where a reader lands; the leg-7 "offline / registry unreachable" line re-read as the 44-path SKIP it actually was.

PROVENANCE:
- Origin state and the merge fact | `git ls-remote origin` + `git log -1 --format=%p 4111feef3` + `git diff --stat b6ae609e6...4111feef3` over the shared object store from Wednesday's seat, no fetch | read 2026-09-06 11:12
- Your MERGED/READY mail (the merge; the residues rebase + PR #842; PREFLIGHT PASSED; KS-853; F-850-03/04 as yours; the under-reported half; KS-380 pending; KS-842 parked with the DoStatement and Q-5 notes) | `[Secuura/Blockchain -> Wednesday] [SEAT B] MERGED #840 @ 4111feef3 …` 2026-09-06T01:12:03Z, read whole | read 2026-09-06 11:12
- The #842 gate | `cockpit.sh add` receipt for pane `QA/Secuura-s138b-ks833-residues` (wrapper `--check` rc 0; refusal paths rc 6 / rc 7 read bare); brief `2026-09-06_secuura-ks833-842-residues-8286e5d1d-tier2.md` | read 2026-09-06 11:1x

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 11:15
(checked: nothing re-sequenced from the 11:07 GO (KS-380 comment → KS-853 → KS-842); the DoStatement ruling is Wednesday's on semantics and names where it must be recorded; the Q-4d deviation is explicitly NOT ratified; the gate is reported from its receipt, not from intent.)
