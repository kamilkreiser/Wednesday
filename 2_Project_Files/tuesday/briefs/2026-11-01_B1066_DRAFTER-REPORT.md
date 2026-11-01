STARTABLE: YES (after Tuesday's stamp; launch beside J38 through launch_when_cool; its heavy jobs wait on `.tools/composer-heavy.lock`, held by J38 at 22:4x, load1 was 15.43)

# B1066 drafter report: SEAT-G263, Security Composer, tier-2 gate of B1061 (PCOMP-118) @ 1e9385fe, round 1 of 2 on the NEW counter

Drafted 2026-11-01 22:48 to about 23:0x AEDT (`date`) by a read-only drafter (claude-sonnet-5-5). Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1066_SEAT-G263_composer-pcomp118-gate-tier2.md` (81 lines). Shape from B1038; builder kit B1061 and its STATUS read whole.

## BLUF
- Gates `b1061/composer-pcomp118-route-b-check-rows` @ `1e9385fe4117ac7313e94921e6548bf2426c67cc`: one commit on `6e69886d`, one test path +271 -0, no PR. Routing G2 (`model-routing.md:109`), Sonnet; launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- The heart is D3: the gate re-derives the edit table itself (head 37 rows and main 23 rows under M0, M6, M7n, M7 literal, M8, M10, M14), classifies every red row as `verdict` or `throw`, and answers the M7 question in three parts with R1/R2/R3 readings and no kind default. A Minor for the records seat if R2 holds and no sentence in the diff over-claims; Major class (e) if one does.
- Also pinned: the 5 control rows' coupling to PCOMP-116 (a harmless rewrite of the check line, red rows listed by name and by how they fail), the typecheck gap (scratch tsc with a TS2322 control), CodeQL on the head (0 check runs, 0 alerts now; NOT SCANNED, a Condition), four landing files, head-pinned squash with C-101/C-111.

## Facts re-measured (instrument; control)
- Pins 22:48: main `6e69886d...`, branch `1e9385fe...` (`ls-remote`; control `b985*` @ `642a0472`). Compare ahead 1 behind 0, one file +271 -0, blob `5ce3df87`; tree `591dea16`. PRs for the branch 0 (`gh api -X GET pulls?head=`; control b985 branch 1). Open PRs #95 #91 #86 #85(draft).
- Seat G263 free: 0 files over the non-`.pre-` 10-31/11-01 SEAT kits, word-bounded (control `G258` found 2); no pane; `.tools/b1066` and `.tools/wt-b1066-head` absent. Ports 9770-9779: `lsof` rc 1, kit scan 0 files (control `970[0-9]` finds the B1061 kit).
- Round counter: no `GATE VERDICT` first line mentions `pcomp-118|pcomp118|b1061|check-rows` (control `pcomp-102|restore-footer` found 1; the B779/B787/B898/B918 lines match only `b778` and are other classes).
- Source: `DEPLOY.md` blob at main `2e48c823`, check line at line 203 read through `contents?ref=` raw; `scripts/test-db.sh:58`, `scripts/ci.sh:116-118`, `packages/db/vitest.config.ts`, `packages/db/tsconfig.json:8 include ["src"]`, `.github/workflows` 404; b778 file 1174 lines blob `a34c6008` at main, 1445 lines and 37 `it(` at head. Head commit message and trailer (`Claude Sonnet 5.5`) read by `gh api`.
- Ticket text read with `jira791.get` (GET only; PCOMP-118 200, 0 comments, Backlog; control PCOMP-999999 404). Its sentence says "Dropping one of the three footer-block compares"; the B1037 gate's table calls the footer edit "neutralised", not dropped (`B1037_STATUS.md:127`, `:209`). That is where the literal-versus-neutralised gap comes from.
- Lock: `.tools/composer-heavy.lock` held, holder `B1047 J38 97625 2026-11-01 22:43:44`. Load1 15.43.

## D-decisions
- D-1: Sonnet on G2; mechanism measured by an earlier gate, tests-only, no security surface; hand-up rule carried.
- D-2: `packages/db` group at head and main required (CI's first half of `test-db.sh:58`); `apps/api` half not required (no `apps` byte).
- D-3: the gate runs main's 23 old rows under the edits too, to re-derive the ticket's premise per edit, and builds its own line runner that does not use the test file's extractor, so the literal-M7 verdicts are seen without the throw.
- D-4: no Jira call for the gate; the ticket text is quoted in the kit as data.
- D-5: a control row red under an edit it does not name (the builder's M14/M10 deviation) is a Note unless it hides a defect.
- D-6: class (a)-(e) stated as a property first, "at least these", with a closing "prove it meets the property or report it".

## Questions for Tuesday
- Q-1 Sonnet on G2 (default YES). Q-2 seat G263 and ports 9770-9779 (default YES). Q-3 group at head and main (default YES; struck means conditional verdict). Q-4 the M7 reading stays a three-part grade with no kind default (default YES; the drafter's own lean is R2, but the kit does not say so, to keep the gate from anchoring). Q-5 PR title and squash subject in words, no ticket key (default YES).
- Q-6 launch spacing: launch_when_cool needs load1 below 7; it was 15.43 at 22:48, so the waiter may sit up to its 3600 s default. Default: start it now as a tracked background task; raise `MAX_WAIT` only if you want it to outwait the load.

## UNMEASURED
- No test, container, image listing, plant or lint run by me. Every D2-D4 expectation is a prediction or the builder's claim.
- RELAYED, not measured: 37/37, the per-edit tables, 19 of 23 and 31 of 37 under the literal M7, the group 538 to 552, lint/format/typecheck rc, CodeQL zeros (I read `check-runs` 0 and open alerts 0 myself at 22:48, both on a head with no PR).
- The 12 of 14 new rows that "read DEPLOY.md" under the literal drop is the builder's count; the kit makes the gate recount.

## Outside-the-fences disclosure
Read: `DRAFTER_RULES.md`; B1038 kit and report (head), B1061 kit and STATUS whole; `model-routing.md:109`, `models_latest.json:23`, `brief_seat.sh` 18-30, `launch_when_cool.sh` 1-25; the B1037 STATUS lines 126-128 and 209 by `grep`; project `CLARIFICATIONS.md` by `grep` (lines 1799, 2032 present; the landing quote is carried from the template and the B1061 kit, with the line numbers re-found); evidence directory listing of B1061 (names only). `gh` was `-X GET` only under the project config; raw `contents?ref=` reads of repo files at main and the head test file saved to the session scratchpad. One scratch program in the session scratchpad (`tk.py`) imported the project's `jira791.py` for two GETs (PCOMP-118, a 404 control); no token printed. No `decision_queue.sh`, no git write, no fetch, no docker, no az, no ssh, no HTTP to any hosted host. Fence slips: two `grep` calls lacked `-i` (hook advisories only; the zero results I relied on carry controls). One early `ls`/`cd` attempt was refused by the hook and re-issued without `cd`. Written: the two files only (plus the scratchpad files noted).
