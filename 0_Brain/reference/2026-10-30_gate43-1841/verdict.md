## QA GATE - TIER 1, round 1: GO WITH NOTES
(Filed by the Wednesday seat from gate 43's returned text, 20:5x AEDT. Opus, tight scope.)

**Subject:** PR #1841, KS-1791, head 20fba453956d at start and end. Spark_gate head 59/59, base product 58 pass 1 fail (R1). Both docs conflict with develop 4c14143b, not code.

**FIX BEFORE MERGE:** none in code; docs merge-in is mechanical.

**FOLLOW-UP**
- F1 MEDIUM, pre-existing, same class: a 200 valid-JSON answer whose access_token holds a newline makes fetch throw TypeError "Headers.append: Bearer tok\n<bytes> is an invalid header value"; the callback echoes it whole, unbounded, including the token. Stub mode through the real route, marker in the 400 for github, google, linkedin, microsoft_personal; facebook not exposed. #1830 does not close it. Durable fix: allowlist adapter-authored or AppError messages, not a denylist of one error name.
- F2 LOW: JSON null token answer echoes internals (Cannot destructure ...), all six adapters, no provider bytes.
- F3 LOW: POST /social/link answers the same body with a generic 500; logs the raw SyntaxError (~10 quoted bytes).
- F4 LOW: R1 covers GitHub token stage only; gate probes covered the rest, no shipped cell pins them.

**Answers:** Q1 discriminator right for its target: token stage on 6 adapters, profile on 5, GitHub emails, Apple id_token; false swallow none (try wraps only exchangeCode). Q2 other paths: F1. An operator loses the excerpt and stage in the log. Q3 no change to a legitimate flow: status was ALREADY 400, so only the text differs; "new status" in the claim is inaccurate. Q4 test bites: M1, M3 red R1; M2 4 cells; M4 instanceof equivalent. Q5 #1830: no code interaction, 64/64 applied together.

**NOT TESTED:** whole auth suite at head, a real provider sign-in, a running stack or DB, Node 24, a limiter run. vitest 4.1.10 vs the seat's 4.1.12.
