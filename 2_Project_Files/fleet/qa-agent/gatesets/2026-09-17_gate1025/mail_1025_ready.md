SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1025 KS-528 @9954a7069a16987da140654337555c9a13268b1f (Seat B)
TS: 2026-09-17T09:22:23.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat B

BLUF
READY FOR QA: PR #1025, ticket KS-528, the re-date of rows 11 and 12 (GHSA-wrjc-x8rr-h8h6, GHSA-337j-9hxr-rhxg): expires 2026-09-30 -> 2026-10-02 per Kam's 18:31:25 ruling and your 2026-10-01 landing. Head 9954a7069a16987da140654337555c9a13268b1f, read from origin in the same action as this mail. Tier 2 through-code, as your ANSWER set.

WHAT IT DOES
- audit-baseline.json only; one commit on develop efaaa6034 (three-dot: 1 file).
- The two rows: expires -> "2026-10-02", and reason gains a dated "RE-DATED 2026-09-17" sentence (KS-528, Kam's ruling verbatim, relayed by you; landing 2026-10-01; slip -> report, no second re-date). The prior reason text is kept.

EVIDENCE (all in the PR body)
- Conservation vs develop: rows 34 -> 34; 0 added / 0 removed; 2 altered on exactly [expires, reason]; every other row deep-equal; key order preserved. Controls unchanged: GHSA-jjmj 2026-09-30, GHSA-frvp 2026-09-30, GHSA-rgwj 2026-09-24.
- isLapsed (shipped baseline-contract.mjs), frozen clocks:
  - today: wrjc live, 337j live, jjmj live;
  - 2026-09-30: wrjc live, 337j live, jjmj LAPSED;
  - 2026-10-01: wrjc live, 337j live;
  - 2026-10-02: wrjc LAPSED, 337j LAPSED.
- audit-gate rc 0 (33 reported / 34 baselined, 0 CLEANUP); audit-locks rc 0 (32/32); npm run audit:contract 59/59 (0 fail / skip). Control: develop's baseline on the same tree, rc 0 / 0.
- In-hook preflight: PREFLIGHT INCOMPLETE, 12/15 legs ran, 3 SKIPPED (3, 4, 8: no stack), nothing failed. Leg 2 35/35, leg 5 59/59, legs 6 and 7 OK.

NOT COVERED
- No unit or platform suites (no code or dependency moved; no stack). No image.

POST-PUSH CHECKS
- Push rc 0; origin = local.
- Stub killer: ps rows 1121; 4 login_stub.mjs from this push ended by verified pid; 0 of mine remain; 17 non-node controls unchanged.
- attachmentsForURL(pull/1025) = KS-528 contributes, closedAt null. Body: 0 closing phrases; "Refs KS-528".
- Open-PR overlap on audit-baseline.json: 0 of 19.

LINEAR, AND A MEASUREMENT FOR THE FLEET
- KS-528 WALKED Backlog -> In Progress at 09:21:22Z (botActor GitHub), about 30 s after the PR opened.
- The branch name carries NO ticket id (chore/audit-redate-react-router-rows-v7-landing), chosen to prevent exactly this. So the trigger was the body's "Refs KS-528" attachment.
- Before the push: Backlog, 0 transitions, 0 attachments, so the instrument could see a change. Not reversed.
- KS-528 comment naming the PR, and stating the walk came from the link and not from the migration starting: f2ba8180-e7b4-4285-9a4a-05d332325879.
- Memory updated: an attaching reference in a PR body walks the ticket regardless of branch name.

NEXT
PR-3 (js-yaml + vitest + baseline-browser-mapping) is prepared read-only only. Under "one root-lock PR open at a time", #1025 does not touch the root lock. Do you want PR-3 built and pushed while #1025 is gated (both edit audit-baseline.json, different rows: whichever merges second takes develop in), or held until #1025 merges? My default: build PR-3 now and hold its push until you answer.

Seat B

