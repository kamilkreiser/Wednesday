This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Report by appending "ADDENDUM 2 (gate test rulings)" to `coagent/5_Project_History/STATUS_M2_POLICY.md`; last line when done exactly `READY FOR QA M2-POLICY r2b`.

# M2 POLICY — two rulings on the round-1 gate tests, so check.sh can be green before the delta gate

You were right to stop on both and not to change them yourself. Friday, as owner of the gate's files, rules:

1. **`z_timing`:** it is a report, not a property. Convert it to a bounded assertion: keep every measurement it takes, replace the final `panic!("TIMING REPORT …")` with assertions that each measured case is under the bound your `docs/POLICY.md` section on bounds states (the brief's 50 ms per decision at the bounds, with the margin you documented for a debug build stated in a comment and in STATUS), and print the report with `eprintln!` so it is still visible with `--nocapture`. An input that the old code overflowed the stack on must remain in the test.
2. **`f8` last line:** `recognise_powershell("gci -Rec .", true).unwrap()` expected a parameter PREFIX to be recognised. Under the default-deny rule that is exactly what must NOT happen. Change that one line to assert the command is `execute`, with a comment `// RULING (Friday, 2026-11-17): prefixes are never recognised; was unwrap()`.

Make those two edits and nothing else in the gate file, in one commit whose message says "gate test rulings (Friday)". Then `scripts/check.sh` must exit 0; run the red controls once more; push. Do not touch anything else. The delta gate will rule independently on both edits.
