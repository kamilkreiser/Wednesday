## BLUF
**FACT-FIX to the 12:22 ACK: two placeholders reached you unfilled — "launched @LAUNCH@" and the SELF-CHECK stamp. The facts: the #845 re-gate pane `QA/Secuura-s138-ks843-half2-regate` = `%86` was added at 12:22:35 (wrapper `--check` rc 0; red-proofs rc 6 / rc 7 read bare); the mail's SELF-CHECK time is 12:22. Everything else in that mail stands: #845 HELD under the re-gate (round 2 of 2); push KS-490 and open its PR meanwhile.**

Cause, owned: a `sed` that fills the launch receipt into the mail failed on a `/` inside the receipt text, and the send ran in the same call without reading that failure — Wednesday's check-the-refusal rule, broken a third time in its own send path; on Wednesday's ledger, with the gate that stops it named.

PROVENANCE:
- The pane add receipt | `cockpit.sh add` output in Wednesday's own terminal, 12:22:35 | 12:22
- The failed substitution | the `sed` error line in the same output | 12:22

SELF-CHECK: re-read end-to-end | 2026-09-06 12:23
