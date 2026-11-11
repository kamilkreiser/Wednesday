# Gate 321, TIER 1 (OPUS, routing v1.0 rule 4: local-model edits inside an auth service get a tier-1 Opus gate): Seat R 103rd round 1 = ONE batched tier-1 READY, two PRs. Both are KS-1868 (catch and log sites read a thrown value unguarded) in services/auth:
- PR 2197 (row 39, held Spark pass o143 P1): services/auth/src/routes/issuerCerts.ts +21 -3, plus a new 9-cell test.
- PR 2198 (rows 30+33, o138 P2 + o139 P1, one commit): services/auth/src/services/issuerCert.ts +32 -5, plus two new tests (9 + 7 cells).

Commissioned 2026-11-12 ~08:0x AEDT by the 07:51 Mac mini Wednesday seat, after the 07:49 reboot (R 103rd died with it; its successor R 104th does NOT push to either branch while this gate runs). A tier-1 gate: be adversarial. A wrong GO here changes what an auth service logs, or what error text it can surface, for certificate issuance and signing.

Method: copy-and-change of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate319-tier1-pr2195/commission.md and of gate 316's commission. Read both whole: the Constraints, the output shape and the controls all apply. Calibration: read the verdict.md files of gates 318, 319 and 320.

Pins (Wednesday's ls-remote at ~08:0x AEDT; RE-READ them at start and end): develop c78c80bd537015674fa5e22701d745946f94d4fb; refs/pull/2197/head 2f10c9750a90acc5df816f481db1804de43955bc; refs/pull/2198/head 5064d0e99dd8ac709cbf4e938df4127a28a2570f. Both are cut on c78c80bd5370. Merge-tree each onto the newest develop, AND the two together.

READY (read it whole; reproduce, do not trust): ready_r103_round1_mail.txt in THIS folder.

Questions:
1. Is each change what KS-1868 asks for (read the ticket and its comments, including 8f95e4d8 and 24b8c3cc, read-only Linear)? Is either change a design choice the ticket leaves open?
2. PR 2198, verifyKeyMatchesCert: its first catch classifies on the message, so an unreadable thrown value now takes the GENERIC branch. Enumerate every caller of the five functions (parseCert, verifyKeyMatchesCert x2, signContentHashWithCert x2) and every route that turns an IssuerCertError into an HTTP response. Make a table: route -> status/body before -> after, for (a) a normal Error, (b) a throw of a non-Error value, (c) an object whose .message getter throws. Can the fallback text 'unreadable thrown value', or any part of a cert, key or hash, now reach a client response or a log line where it did not before? R 103rd marked the route layer's real answer as UNMEASURED: measure it.
3. PR 2197: the three changed catches (POST /, POST /:id/rotate, POST /sign). Confirm the log field and the constant 500 body are unchanged, the untouched GET /:id catch included. Does the guarded read ever log secret material (key PEM, cert private part, signature input)?
4. Reproduce red-first and green with the PRs' own tests (2197: 6 of 9 red by assertion with the product reverted; 2198: 10 of 16 red). Then your own mutants: (a) drop the guard and read .message directly; (b) the fallback text changed; (c) the classification branch inverted. Each mutant must turn a cell red, or that is a finding.
5. R 103rd's FINDING: the whole services/auth suite sometimes exits rc 1 with every test green ("No seedDemoUsers export is defined on the userRepo mock", from the 2000 ms setTimeout at src/routes/auth.ts:63-68, raised in two EXISTING test files). Reproduce it on pristine develop: run it 4 times and give the rc count. Is it independent of both PRs? State it as a pre-existing finding (a board filing for the S lane), not a defect of these PRs, unless you measure otherwise.
6. Run a census on the five paths (GraphQL; the control PR 2125's api-gateway/src/index.ts must fire). Is either PR import-coupled to another open PR?

Spark shadow (after your verdict): run spark_gate.sh / spark_review.py WITH --pr-body-file on each PR, and record its verdict, recall and false claims. The scripts refuse a work dir under /Volumes/DevMASTER/WEDNESDAY, so use the session scratchpad as gate 318 did.

OUTPUT: verdict.md in THIS folder.
- First lines: 'PR 2197: GO / GO WITH NOTES / NO GO (at head ...; tier 1)' and the same for PR 2198.
- Findings G321-<PR>-N, graded Major / Minor / Note / Info, each with its evidence.
- The route/response table.
- NOT TESTED.
- The Spark shadow result.
A Major is a NO GO. If your Write is refused, return the verdict text in full.

Constraints, as for gates 313-320:
- Write only in this folder (scratch under scratch/).
- Read-only git verbs in the shared Secuura checkout, with GIT_OPTIONAL_LOCKS=0. Run any write verb (merge-tree --write-tree, worktree) only in your OWN clone under scratch/.
- No push, no PR comment, no Linear write, no mail.
- No rm, no cd.
- Never print .env values, keys, certs or passwords (placeholders only).
- GitHub reads are GET only; GraphQL preferred; never a per-PR or per-file REST loop.
- No real Postgres, Redis or Docker stack is started.
