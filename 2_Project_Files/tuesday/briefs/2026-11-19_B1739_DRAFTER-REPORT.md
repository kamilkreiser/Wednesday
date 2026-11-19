STARTABLE: YES - stamp_check exits 0 (151 of 151 claims measured, drafter's run); the kit cannot launch until the N-F pull request is merged (its REFUSE 4).

# B1739 drafter report (SEAT-N159, NexusAI lane N-J: RD-445 item 2)
Saved by Tuesday (s293) from the drafter's in-session reply. Condensed by Tuesday; the kit is the authority. Every figure
here is the DRAFTER's measurement, not Tuesday's.

## Files
Kit `2026-11-19_B1739_SEAT-N159_nexusai-lane-nj-marketplace-jwt-bypass.md` (270 lines, 81614 bytes, ASCII, 5 four-underscore
lines: four slots plus the last line); sidecar `.measured` 151 lines. Scratch `2_Project_Files/fleet/state/s293/d1739/`
(census1739.py, readers1739.py, apply1739_ascii.py, probes/rd445-final.test.js; the kit does not depend on them).

## What the kit builds
- `backend/marketplaceJwt.js`: two helpers and one logger.error line in production; the bypass block kept for
  non-production; production falls through to the existing verification. +30 -4, 138 to 164 lines, blob d2feb537adac to
  8583d059c9b6 (the embedded ASCII apply script reproduced it on a copy; node --check rc 0).
- One new test file `__tests__/rd445-marketplace-jwt-skip-flag.test.js`: 20 indented `test(` cells, 0 at column 1.
- Commits A445, T445, at most two merges, then K; one lock acquisition; main-move absorbed inside it.
- Gate G1 Opus with CQ-1 and CQ-2.

## Recommended slots
Model C2 Sonnet (model-routing.md:92), id claude-sonnet-5-5; pane Datasec/NexusAI-N159; branch
b1739/nexusai-lane-nj-marketplace-jwt-bypass; jest slot 16 (band 30240-30879); HEADS: main
9373976efc7d93f522f97648beb608b4d3e16fb2, marketplaceJwt blob d2feb537adac, counts file blob 4d667a4d798d (ALL THREE MUST BE
RE-READ AFTER N-F LANDS: main and the counts file will have moved); HARD STOP and launch window left for Tuesday (about
1.5 h reading plus about 1.2 h of lock hold predicted).

## Drafter's measurements (jest 29 on scratch copies)
BASE 8 red (R1 to R6, B6, C2) and 12 green; patched 20 of 20 green; plants P1 to P12 received and recorded (three
pre-run predictions were wrong and the kit holds the RECEIVED values: P1 also reddens C2, P4 reddens B4 not R5, P6
reddens B1 to B4); 19 reader files 428 of 428 green at base and patched; 490 heads compared, 0 touch the two files.

## Corrections to the commission
1. No test relies on the flag; it appears only in scripts/test-marketplace-webhook.js (hand-run, sets NODE_ENV development).
2. The bypass already warns per request (:114); the lane adds a boot log and an error line in production.
3. The real `jose` is ESM-only and cannot load under jest: the cells mock it, so "bad token refused, good token accepted"
   proves ROUTING, not real signature verification.
4. rd385 pins the GUID lines of the file; the new lines do not touch them (58 of 58 green).
5. Every jest slot is named somewhere in 18-19 Nov kits; 16 chosen (named only in one finished kit's control sentence).
6. /Volumes/Datasec_DEV used throughout.

## D / Q (all Tuesday's defaults when stamped, none the product owner's)
Q-1 refuse in production, keep the flag. Q-2 add the factory-time boot log. Q-3 compare NODE_ENV trimmed and
case-insensitively (stricter than the backend's exact === 'production' precedent). Q-4 log wording is the change's default.
Q-5 mock jose and the logger, no real-jose cell. Q-6 G1 with CQ-1 and CQ-2. Q-7 slot 16. Q-8 STOP if any head or main
changes marketplaceJwt.js before the push (RD-415 is the one to expect).

## UNMEASURED
N-F's final diff; hosted app settings and any instance with NODE_ENV unset or not production (it KEEPS the bypass when the
flag is on; the kit says so); real-signature or JWKS behaviour; open CodeQL alerts on the file; jest-cli's NODE_ENV=test
default; the content of PR #220; whether a test reaches a backend file by a route other than image-manifest; lock-hold time.

## Process disclosures
The drafter ran jest 29 OUTSIDE the project lock (1 or 2 workers, own scratch and cache, no server) while B1737's chain
held the lock and load was about 8; node_modules in scratch is a symlink to the B1733 clone's (read-only); git init and
commits in the scratch copy only; one `cd` refused by the hook and re-issued; nothing deleted (strays to _quarantine);
the slot scan covered the briefs only, not the s291/s292 state folders.
