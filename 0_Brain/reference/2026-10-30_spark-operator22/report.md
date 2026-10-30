# Spark operator 22 — report (saved by Wednesday from the returned text)

Basis develop 40c06084919d; one drainer (pid 97411), none started.

1. Tickets: three KS-1410-class sites (a thrown error's text in a 500 body), found by a pattern grep across services/*: ks_1410_p6 api-gateway routes/platform.ts (:994 templates-read catch, :1091 clone 500; no ticket covers these two sites); ks_1410_p4 tenant-provisioning index.ts (6 of 7 sites; POST /api/tenants untouched: Kam's open card secuura-ks1240-tenant-create-key-fail-answer-1028); ks_1410_p5 mcp-server http-server.ts (9 of 10; POST /hash left: KS-1214).
2. Rung 4 (code_patch2 LOOSE: model writes product lines, hunk headers dictated, one source-text vitest file given whole); 2, 6 and 9 hunks.
3. p6 + p4 original brief only; p5 original + ONE rebrief (counter spent).
4. p6 PASS 7/7 (52 s, golden byte-identical); p4 PASS 7/7 (56 s, byte-identical); p5 FAIL x2 at A2/A2a, MODEL: it wrote the new res.status(500) line as context and never emitted the '-' line, in all 9 hunks; the rebrief fixed only hunk 9.
5. Held by hand (hold_ready refuses loose PASSes): local-model/night/READY_KS-1410-KS-1410-P6_spark-dsv4flash_BRIEFED-CODEPATCH2-LOOSE-PLATFORM-500-NO-DETAILS-PASS-7of7_2026-10-30.diff.md and READY_KS-1410-KS-1410-P4_..._TENANTPROV-500-NO-ECHO-PASS-7of7_2026-10-30.diff.md (full patches inside).
6. Tooling faults (IMPROVEMENTS.md): hold_ready cannot hold a loose PASS; the A4 declaration-splice read `router` inside a regex literal; the A2 diagnostic prints a bogus MISMATCHED HEADER for a wrong old side; hooks refuse `git -C <scratch> checkout`; the planted open-PR control gdpr.ts stopped firing after #1823 merged (use reconciler.ts / routes/users.ts).

Where the model breaks: rung 4 holds at 2 and 6 dictated hunks of one shape and broke at 9 ("replace this line" read as "show the end state as context"; obeys a hunk-specific instruction, ignores a general one). p5 -> Opus 5.5 by the counter, OR split into two briefs of <=5 hunks (a new brief, a new counter: Wednesday's call).

Raise notes: Refs KS-1410 (never a close word). p6: no ticket for those two sites; the 500 body loses details.detail. p4: six routes' 500 message becomes constant. Both tests are source-text guards. p5: the ks_1530_p1 PASS edits the same file at :233-239.
Left: run dirs (~335 MB each) for the prune; scratch clone .../scratchpad/op22/clone; tools in this folder; briefs in night/briefs/ (ks_1410_p4/p5/p5_rebrief/p6).
