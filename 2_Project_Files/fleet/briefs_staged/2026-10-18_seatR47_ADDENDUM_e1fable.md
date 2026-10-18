## BLUF

ADDENDUM to the gate E1 GO. The GO itself is unchanged: merge #1570, then #1572, as sent. The Fable 5.1 trial gate on the same PRs (a comparison, not the authority) found one more TEST gap on #1570 that the Opus gate did not report. Add it to the same follow-up ticket as M1. Do not build it.

- #1570, scripts/__tests__/ks1547_preflight_step_header_denominator.test.sh:56-97: no cell drives a step header with a SECOND `/` after the denominator, though 7 of the 16 live headers carry one. Mutant `${1#*/}` -> `${1##*/}` on preflight.sh:225 survives 12/12 and is NOT equivalent. One cell closes it.
- Verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-18_gate-E1-pr1570-pr1572/fable/verdict.md (Wednesday's project), sha256/16 6af5896fb794a797 (recomputed equal).

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-18 22:24
