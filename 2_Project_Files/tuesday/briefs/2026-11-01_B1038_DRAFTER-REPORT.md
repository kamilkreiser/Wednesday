STARTABLE: YES (after Tuesday's stamp; launch it after B1037's launch is verified; its heavy jobs wait on `.tools/composer-heavy.lock` while B1037 holds it)

# B1038 drafter report: SEAT-G258, Security Composer, tier-2 gate of B1017 Part B (PCOMP-112) @ dea1d09f, round 1 of 2 on "the date-rule setup-failure kill"

Drafted 2026-11-01 11:09 to about 11:2x AEDT (`date`), in the same session as B1037. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1038_SEAT-G258_composer-pcomp112-date-rule-setup-row-gate-tier2.md` (84 lines). Its `.pre-stamp` is a byte-exact copy (`cp -n`, `cmp` rc 0, sha256 of both `f97ed4b006754a863e2df0bb2fbed869d82da0a0f773d59209b7b1323e241883`). Four-underscore line count 9: eight slots plus the last line. Non-ASCII bytes 0. At-sign-capitals pattern 0. Person-name and card-id greps 0.

## BLUF
- The kit gates `b1017/composer-pcomp112-date-rule-setup-row` @ `dea1d09fc7a8fec41134387341e295570017d761`: one commit on `075b2b23`, one test path +15 -0, no PR.
- **Routing:** tier 2, G2 (`model-routing.md:109`), **Sonnet first** (`claude-sonnet-5-5`, `models_latest.json:23`). The launch line carries `BRIEF_SEAT_LEVEL=sonnet`; without it, `brief_seat.sh` defaults to Opus.
- **Why not G1:** the row's mechanism is the request validator's date format plus one create/read as the file's own consultant. It touches no authorization, tenant boundary, secret, deletion, migration or deploy, and no product byte. A hand-up STOP covers a security-shaped surprise.
- The heart is D3, with plants of the gate's own:
  - **k1:** the `(\D\d{3})` kill, run with the head's AND main's test file. The JSON readings `numFailedTests` 0 and `numFailedTestSuites` 1 are shown side by side; that is the title's claim.
  - **k2:** how much the title covers (`(\d{3}\D)`, `(\D?\d{4})`).
  - **p1:** the GET returns another date.
  - **p2:** the builder's stored-date plant; the other rows it turns red are re-counted.
  - **p3:** another digit-first input; expected green, which shows the row reads the input and not a literal.
  - **p4:** a non-digit-first input. It is a setup kill, which makes the regex `expect` unreachable; graded Note or Minor.
- The other checks:
  - D1: delta, hygiene, identity, gitleaks.
  - D2: the file at main and head, x3, the row alone, a shuffle, and the `apps/api` group once at head and once at main (names lost 0, added 1).
  - D4: eslint and prettier on the file, tsc coverage, the duplicate `./flows.js` import.
  - D5: title and message truth.
  - D6: merge, Part A independence, CodeQL NOT SCANNED as a Condition, the four landing files.

## Facts (instrument; control)
1. Pins 11:09 (`ls-remote`): branch `dea1d09f...`, main `075b2b23...`, `b1038*` absent (control: `b1017*` lists two). PRs for the branch: 0 (control: b985's 1). `compare`: ahead 1, behind 0, `+15 -0` `ee26b4e9`.
2. Commit `dea1d09f`: tree `657b1067...`, author domain noreply (local part elided), one trailer. Subject 112 characters.
3. Blobs equal at main and head (`rev-parse`): `app.ts` `2c5d5ad1`, `flows.ts` `46010d8b`, `harness.ts` `693e4f6b`, `package.json`, `package-lock.json`.
4. Source lines at main (`git show | /usr/bin/grep -n -i`):
   - b626 `beforeAll` at 136; `createEngagement(h, TENANT_A, "date rule rows draft")` at 141;
   - `flows.ts` `engagementInput` at 113, `due_date: "2026-12-01"` at 116, `ok<EngagementBody>(` at 143;
   - `app.ts:105` `const DATE = /^(\d{4})-(\d{2})-(\d{2})$/;`.
5. `eslint.config.js` at main holds no `duplicate` rule text: count 0 (control `rules` 1).
6. The diff adds a second `import ... from "./flows.js"` line (line 5). Line 4 is unchanged.
7. Seat G258 is named in 0 kit files. Ports 9680-9689 are mentioned in 0 of the 10-31/11-01 SEAT kits; B1036 uses 9290-9299 and 9740-9749. `lsof` rc 1; panes as B1037; load1 2.48.

## D-decisions
- D-1. Sonnet on G2. The row's mechanism is not on a G1 surface (cited above). If Tuesday prefers Opus because it rides on a tier-1 lane's builder, that is Q-1.
- D-2. The `apps/api` db group runs once at head and once at main. CI's db step runs it, and the builder did not. If load or the lock leaves no room, it is NOT TESTED and the verdict is conditional.
- D-3. The full `unit.sh ci` chain is not required, because the file is not in the unit config (shown by `vitest list` with a control). Only eslint and prettier run on the file.
- D-4. Landing files are written as data (no PR). The squash subject is written WITHOUT `(#n)`; Tuesday appends it, as Composer squash subjects carry it.
- D-5. Kit B waits on the shared project lock behind B1037; a wait is not a STOP until `HEAVY_MAXWAIT`.

## Q-questions (each with a default)
- Q-1. Sonnet (G2 `:109`). Default: accept.
- Q-2. Seat G258, ports 9680-9689. Default: accept.
- Q-3. The `apps/api` group at head and main. Default: YES; strike it to save about 20 minutes, which leaves the verdict conditional.
- Q-4. Launch after B1037's launch is verified (one waiter at a time). Default: accept.
- Q-5. PR title and squash subject in words, no ticket key (Composer convention). Default: accept.

## UNMEASURED
- No test, container, image listing, plant or lint run by me. Every expected result in D2-D4 is a prediction.
- RELAYED, not measured: 40 / 41 rows, the builder's plant result, the tsconfig reading.
- Not run: the round-count loop, the open-PR overlap, the `apps/api` group size.

## Outside-the-fences disclosure
The same as the B1037 report (one session): writes under `tuesday/briefs/` and the session scratchpad only; `gh` GET only; read-only git; no docker; the one no-op `cd` slip at 11:20, disclosed there.
