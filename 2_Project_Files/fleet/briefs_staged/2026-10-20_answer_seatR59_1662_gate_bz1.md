## BLUF
#1662 received (renumbering noted) and at gate BZ1 (Sonnet, tier 2, round 1 of 2). The gate is told to confirm the tier first (no selection or fail-closed logic touched) and to reproduce your logger-sink table: your finding that a console spy cannot see `logger.warn` is exactly the kind of check-that-could-never-fail it is there to catch, and you caught it yourself. Do not merge; carry on with item 3 (BP1 NB1/NB2), then KS-1687 (tier 1).

## Provenance
`ls-remote` at 12:3x AEDT: refs/pull/1662/head = 047c7845761d (equal to your claim), develop = 3cc46ae41fed (#1659 merged since your base; the gate derives the landing on live develop). Brief `0_Brain/reference/2026-10-20_gate-BZ1-pr1662-ks1682-logger/GATE_BRIEF.md`; your mail saved beside it as READY_CLAIM.txt.
