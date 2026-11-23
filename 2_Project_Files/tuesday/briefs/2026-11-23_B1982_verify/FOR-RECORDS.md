# FOR RECORDS: OXPd 2 lab device-reach tool (lane L1, kit B1971, seat X45), gate G1 round 1 of 2 of lane L1, reader B1982

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: this round's cut (kit B1971 Q1 = a in words at its stamp S4:
`probe` only, `read` a later round), every choice inside it (D1 to D9, Q2 to Q7 the defaults), and the landing order
(L1 next; TA may land first). Nothing here says the product owner decided, ruled or approved anything about this lane
(kit B1971's CLARIFICATIONS greps for the subject words counted 0, RELAYED).

## State at this gate

- Verdict GO WITH FINDINGS at `8dc7390d` on main `da8d64a8` (round 1 of 2 of lane L1). Lands as ONE squash
  (landing.txt): C# totals +37 on both legs, RULES +18, skipped 4 / 21 unchanged, unit tests 111, floor 111. With main
  `da8d64a8`: 1846 / 0 / 1842 / 4, RULES 571 (measured locally and on the push run). With TA first (its head alone):
  1874 / 0 / 1870 / 4, RULES 580 (measured locally, tree `2da9cc72`).
- Lane L1 (WP0.1, WP0.2 tooling) is a lab-only project, `probe` only; `read` is a later round after lane TA and a first
  real or simulated `servicesDiscovery` answer (RELAYED from kit B1971).
- Nothing has run against a printer or a simulator. The first run of `probe` on the product owner's printer is a
  separate commission after his four steps (Q6).

## From this gate (for the backlog)

1. **Owed, Minor (VERDICT FOUND 1): a no-pin run with `--plain-discovery-tree` sends the plain discovery tree GET
   when the HTTPS port gives no handshake** (MEASURED on 127.0.0.1: exit 3 with one plain GET; with the IPP ports also
   silent, exit 0 with one plain GET and no certificate read). The README (`:19-20`) and `ProbeCommand.cs:158` say a
   no-pin run sends nothing. Matters for Q6: the needs list's row 0 is exactly the discovery tree. Fix in a fix round
   (refuse the option without `--pin`, or stop a no-pin run at its first no-answer) or correct the sentence.
2. **Owed, Minor (FOUND 2): a body of another type that starts with `{`, `[` or `<` and parses is shown, masked by name
   only;** XML comments and processing instructions are shown. The README (`:28`) and `Masking.cs:16` say such a body is
   not shown. Same exposure class as the named limit "masking is by name only".
3. **Owed, Minor (FOUND 3): a JSON answer with one property name twice throws `ArgumentException` out of the masking;**
   the run ends unhandled, without its summary; no value is written (the message names the property only).
4. **Info: the trust rule MEASURED beyond the cells:** one TLS connection per request; after a pinned success, a wrong
   pin and then no pin on the same stub are each refused with no request (no cached-session bypass), macOS only;
   Linux and Windows UNMEASURED for that order.
5. **Info, named limits confirmed (no cell):** values under unlisted header names (`Location`, `WWW-Authenticate`,
   `X-Auth-*`) are shown; the plain-HTTP refusal reads the call's own flag, not its path; B02 reads `*.csproj` under
   `src/` only (a reference by an imported props or targets file is not covered).
6. **Carried (RELAYED from kit B1971 FOR RECORDS):** named limits (masking by name only; one pin per run; IPv6 literals
   refused; IPP collections shown by count; what an HP device answers is UNMEASURED); owed item 43(4) waits for the
   first real probe; whether the needs list's row 0 is widened to `probe`'s reads or the first run is limited (Q6).
7. **UNMEASURED:** everything an HP device answers; the hosted legs of the merge with any main (the pull request's run
   is the first); CodeQL on the pull request.
