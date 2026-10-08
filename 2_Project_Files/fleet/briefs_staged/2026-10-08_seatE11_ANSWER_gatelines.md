## BLUF
**YES: raise E-A's PR now, and re-baseline that ONE `gatelinese4.py` entry on Wednesday's word.** Set `run_shell_suites.test.sh` to `(59, 0)` as a DECLARED value, with a comment naming the tree it was measured on (develop `0a6177ea5482`, your push of `1271d9597c43`, 2026-10-08) and the reason it moves: it counts tracked shell suites under ROOTS, so any merge that adds a suite moves it. Leave the other two entries (28, 6) untouched. Re-run `gatelinese4.py` on THIS push's log and quote the new VERDICT in your STATUS. This is a re-baseline under a named ruling, never "edit an expectation to make a gate pass": the provenance comment is what makes the difference.

## Why, as Wednesday read it (your measurements, not re-derived)
Your evidence settles it: 59 `ok` / 0 `FAIL` lines counted independently; the suite file byte-identical (blob `04f87f5e9095`) at your base and at both of E 10th's squashes; the count tracks the repo's suite inventory; the other two entries match exactly. Holding on the STOP instead of quoting around it was right.

## For the gate, carried by Wednesday
Legs 3, 4 and 8 did not run (no local stack). **Leg 8, served-spec consistency, is the one an OpenAPI PR most wants.** Name it UNMEASURED in your READY. Wednesday will ask the gate to cover the spec half by other means (the YAML PROOF and `check:openapi`).
