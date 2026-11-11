STARTABLE: YES, once the DOCKER, IDENTITY, WORDS-27 / DEPLOY-MD-RECORD and Q-answers slots are filled. Nothing is dropped as Done or ruled. Part 26a (a registry read) and Part 27 (a failure hint) need your answers below before they are built; 26b needs none; 21 measures and records only on ALLOW.

# B1504 DRAFTER REPORT: Security Composer lane C (PCOMP-26, PCOMP-27, PCOMP-21)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1504_SEAT-C95_composer-lane-c-stack-deploy-hygiene.md` (122 lines, 12 lines carrying a run of four underscores: eleven slots and the last line; sha256 prefix `24f46f2ab5586116`). I did NOT write the `.pre-stamp` copy (the rules allow two files only): `cp` the kit to `<kit>.pre-stamp` before stamping.

## BLUF
- **What I dropped: nothing.** All three keys are Backlog with 0 comments and last updated 2026-10-23 (Jira GET 15:36). The 14:15 ruling "accept all 7 quick recommendations" and the 14:44 records entries C-136 to C-142 (`CLARIFICATIONS.md:2596-2692`) name PCOMP-46, -94, -83, -74, -80, -81, -11, -52, -98, -116, -127 and none of -26, -27, -21 (`grep -o -c -i -E 'PCOMP-(26|27|21)([^0-9]|$)'` prints 0, 0, 0; control `PCOMP-83` prints 13). So no C-entry governs a lane-C key. Two older rulings bound the work and are quoted in the kit: C-79 (`:1469`) and C-80 (`:1482`, "Keep Chainguard free tier for local and CI only"; the demo's default image stays).
- **Origin main is `b14467e2` (PR #122's squash, 2026-11-11T04:07:19Z), as expected.** Open PRs are #85, #86, #91 only. #85 holds 0 paths under `scripts/`, `docker/`, `compose*` or `DEPLOY*` (control: it holds `document-pdf.ts`); #86 and #91 hold only `package-lock.json` / `package.json`, which the kit forbids touching.
- **The three tickets are not all of the same size.**
  - PCOMP-26: premise present (the digest is in `scripts/ci.sh:16` and the `compose.yaml:126` comment, equal, once each). Whether it still resolves is UNMEASURED (I may not touch a registry). Kit: measure (26a), plus a small drift check (26b) that the B281 gate asked for and PR #80 never got.
  - PCOMP-27: premise present; the recovery exists only as a comment (`compose.yaml:127-128`; the ticket's `:125-126` is stale). Kit adds a hint to the failed-step diagnostics and `up.sh`.
  - PCOMP-21: the sweep's "dated" warning is right but narrow. 0019 is proven (`DEPLOY.md:121`); the 0020 section still says "Not yet run end to end on a seat stack" (`DEPLOY.md:150-151`). Sections 0022 to 0027 also say "UNMEASURED" for Route B, but the ticket asks about 0019/0020 only, so I did not widen it.
- **Two traps the seat would otherwise fall into, found by reading source:**
  1. `scripts/stack-diagnostics.sh` runs `compose ps -a` and `compose logs` WITHOUT `--env-file`, and `compose.yaml` requires the four generated passwords, so the diagnostics cannot simply be wired into `up.sh` (which passes `--env-file`). The kit has `up.sh` run its own logs call.
  2. `scripts/stack-diagnostics-test.sh` pins three `ci.sh` lines by whole text (lines 111, 123, 124 at main) and its fake `docker` exits 97 for any verb but `compose ps|logs`. The kit forbids touching those lines and forbids any other docker verb in the new function.
- **DEPLOY.md is the sensitive file.** PRs #96 to #121 hardened its 0021 Route B check, and two tests read it at run time (`b616-deploy-commands.db.test.ts`, `b778-route-b-script-complete.db.test.ts`). The kit allows exactly lines 150-151 and only on ALLOW; a Route B refusal at 0020 STOPs (the two-step form is a new operator command).

## Facts re-measured (instrument; control)
- Main `b14467e20402f955a81b95b929490ff557ec5c2c`: `gh api -X GET .../commits/main`; author email is the GitHub noreply address. Tree 1041 paths (`git/trees?recursive=1`); migrations `0001` to `0027` = 27 files (`grep -c` over the tree list; control: rollback recipes 0019 to 0027 listed).
- Jira: issue GET and comment GET for the three keys (python `-I`, credentials in-process). Statuses Backlog; labels `composer-seed-1023` plus `plan-comp-323/324/291`; `COMMENTS total 0` each. Control: the script ran for three keys and printed three blocks; I did not run a JQL, so no parentheses issue.
- Digest agreement: `grep -o -c -F` of the full `cgr.dev/chainguard/minio@sha256:709099319add...e510` prints 1 in `scripts/ci.sh` and 1 in `compose.yaml`, 0 in `DEPLOY.md` and `scripts/up.sh` (control: those are the two expected hits). `search/code` for `709099319add` and for `PC_OBJECTS_IMAGE`: the same two files each.
- Pointers (all by `grep -n` / `awk NR` over raw copies at main, just before writing): ci.sh `:16 :111 :116-118 :123-124 :130-131`; compose.yaml `:118 :126 :127-128 :129`; up.sh `:5 :9 :10 :11`; stack-diagnostics.sh `:30 :40-42 :44-45 :49`; its test `:65 :138-151`; DEPLOY.md `:22 :24-29 :95 :101-103 :113 :121 :128 :147-151 :153 :265 :585`.
- PR census: 122 PRs over three pages, 0 titles for the keys, 0 for `preflight|volume|65532`, 1 for `minio|chainguard|objects` (#80, the pin's source); control `deploy guide` 10, `pulls/9999` 404. Refs: 0 for each of eleven lane words; `heads/b14` printed seven refs (control).
- Tests that read the lane's files (by `search/code` plus my own `grep -c` over the 40 top-level `packages/db/test` files): `DEPLOY.md` is read at run time by exactly two (`b616-deploy-commands`, `b778-route-b-script-complete`; each regex count 1); `compose.yaml` by `packages/db/src/compose-db-healthcheck.test.ts` (db healthcheck only); `ci.sh` by `scripts/stack-diagnostics-test.sh`. The other `search/code` hits for `ci.sh` are comments (b51b, s47, b20; read, 3 lines).
- Ports: `lsof -nP -iTCP:9660-9669 -sTCP:LISTEN` rc 1; word-boundary scan of the 71 non-`.pre-` SEAT kits of 11-10 and -11: `966[0-9]` 0 hits, control `967[0-9]` 5. `965[0-9]` is B1497's block (1 hit) and `964[0-9]` has 4: not used. `18080`/`18180` (the stack defaults) also free (rc 1).
- Heavy lock `.tools/composer-heavy.lock` absent (`ls -d` rc 1); `.tools/b1504` absent; `.tools/b1495/scripts/heavy.sh` 1724 bytes, three lines naming `b1495`/`C93`. No Composer pane live (`tmux list-panes`: `%0 tuesday`, `%1 fleet-monitor`, `%48 Datasec/NexusAI-N122`, others unnamed). Load1 23.18 at 15:39:55 (above the gate; the waiter handles it).
- Model: Sonnet, row C2 (`model-routing.md:92`), id `claude-sonnet-5-5` (`models_latest.json:23`); `brief_seat.sh:24` defaults to Opus, so the level is inside the launch quotes.
- Landing rule: `CLARIFICATIONS.md:1799`, C-101 (1), quoted as B1495 did; control: `PR #88` finds the line.
- Identity answer copied from B1495: the seat set `user.name` and `user.email` once in its clone with `git config --local`, equal to main's author (B1495 STATUS `:13`; the values are `kamilDatasec` and `88359143+kamilDatasec@users.noreply.github.com`; I kept them out of the kit text, so the IDENTITY slot is yours to fill).

## D-decisions (drafter's recommendation first)
- **D-1 (order):** 26a, 27, 26b, 21 (the cheap and light first; 21 is the heaviest and has a stop branch). The sweep's order was 26, 27, 21; I only inserted 26b after 27.
- **D-2 (Part 27 route):** D, failure text, over a preflight. A preflight needs a throwaway container to `stat` the volume and can misfire; text needs no new docker verb and is testable with the existing fake-docker pattern. Weakness: it fires after the failure, not before.
- **D-3 (Part 21 frame):** a throwaway `postgres:16` at the digest pin, not a compose seat stack. Route B is a database operation; the previous build's behaviour is `migrate()` over the filtered list. The ticket says "seat stack", so the DEPLOY.md sentence names the frame honestly; S (two worktrees, as B18 and B114 did) is the alternative and much heavier.
- **D-4 (controls for 21):** a positive control at 0019 (the pc-b18 row, exit 0), a negative control at 0021 (exit 1, "cannot drop schema pc"), and a planted fault. Both documented results already exist in DEPLOY.md, so the instrument is checked against known answers.
- **D-5 (re-pin):** if the digest is gone, the default is STOP; a new third-party pin is a supply choice and the full stack proof belongs to the gate.

## Q-questions for Tuesday at the stamp (each with my default)
- **Q-1 (registry read).** May the seat run `docker manifest inspect` against `cgr.dev` anonymously (an empty `DOCKER_CONFIG`, one read plus an all-zero-digest control)? It is not the demo and not a Composer host, but it is HTTP to a hosted registry, which the drafter rules forbid for drafters. Default YES (the ticket cannot be answered otherwise; C-79 is the precedent for one anonymous pull test). If NO, you can run the read yourself and stamp the result.
- **Q-2 (pin gone).** STOP or BUILD the re-pin? Default STOP.
- **Q-3 (Part 27 route).** D or P. Default D.
- **Q-4 (Part 21 frame).** B or S. Default B.
- **Q-5 (partition).** `scripts/stack-diagnostics.sh` is not in the sweep's file list for the lane; Part 27 edits it (only the hint function and the objects-log capture). No other lane or open PR touches `scripts/`. Default YES.
- **Q-6 (26b).** Build the digest-agreement test (a new file and a new `ci.sh` step)? Default YES; it is the B281-3 regression that was never added, and it makes the ticket's "both must match" mechanical.
- **WORDS-27.** The hint line is new operator-facing text in a dev script (proposed text is in the kit's WORDS CARD, built from the ticket's and `compose.yaml:127-128`'s own words). Default AS PROPOSED. Under the project's strict "no new word" habit you may prefer NOT YET and a card; then Part 27 is not built.
- **DEPLOY-MD-RECORD.** Is a one-sentence measured-fact replacement at `DEPLOY.md:150-151` "operator words"? The product owner's 2026-11-10 15:51 approval on PCOMP-113 ("Leave the paragraph as it is", option detail "No new operator words", C-133) shows he cares about those words. My default is ALLOW because it adds no instruction or command, only a result; HOLD is safe and costs nothing (the measurement still runs and goes to STATUS).
- **Seat id.** The commission said SEAT-C95; the highest id before it was C93, so C94 is unused. I kept C95.
- **K1-K10.** Your brief cites "Composer K1-K10: nothing is deployed without the card". `CLARIFICATIONS.md:1600-1609` K1 to K10 are ten answered decision rows, not a deploy rule; I cited the real rule instead (project `CLAUDE.md:30`, and C-142's "a deploy only on the product owner's card").

## UNMEASURED
- Whether the pinned digest still resolves (no registry contact by a drafter).
- What `compose up -d --wait` does when `objects` exits 1 (B281 ran only `objects` alone, so the kit's real-image control (v) measures it).
- Whether `shellcheck` is on the PATH; Docker's image cache (Desktop was freshly started at B1495 and pulled the pinned tool images).
- Whether Route B succeeds at 0020 (expected yes by reading migration 0020: six nullable columns, grants, no function or trigger; `grep -c` of create-function/trigger/policy over 0019 to 0027 prints 0 for 0019, 0020, 0023, 0026, 0027 and 1 to 5 for 0021, 0022, 0024, 0025, so the 0021 failure class applies to 0021, 0022, 0024, 0025 and not to 0020).
- Whether the test census over `packages/db/test` is complete: it covers the 40 top-level files; `search/code` showed 23 hits in all and no deeper test dir.

## Outside the fences (disclosure)
- Scratch files only under `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/3bf2c1bb-1001-4c07-ac61-f6312d3309c4/scratchpad/` (`jget.py`, raw copies of origin files and 40 test files, `tree.txt`, `prs.tsv`, `jira.txt`). The Jira script was written to a file there and run with `python3 -I` (the template ran its python inline); it printed no credential. Nothing written in any project folder.
- No git ref write, no Jira write, no GitHub write; `gh api -X GET` only (including `search/code`, 5 queries). No `decision_queue.sh`, no `fleet/briefs_staged/`, no scoreboard, no ledger, no other client's tree. No docker, az, ssh or HTTP to a hosted host. Read-only `ls` of the project's `.tools/`, `Briefs/` and `BACKLOG.md` (stale local checkout: used for the row texts #291, #323, #324 only, which Jira's descriptions repeat).
- I read the DRAFTER_RULES' `/Volumes/Laptop-DEV` paths as `/Volumes/Datasec_DEV`, as instructed.
- The commit-rule scan regex in the kit names `Wednesday` and `Friday` as banned words in commit messages (copied from the template); no person's name appears in the kit.

READ-WHOLE-BY-TUESDAY: ____
