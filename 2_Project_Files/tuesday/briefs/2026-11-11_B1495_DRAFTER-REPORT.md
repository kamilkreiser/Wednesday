STARTABLE: YES, once the DOCKER, IDENTITY, PART-75/WORDS and Q-answers slots are filled. Part 77a needs no ruling and no new word. 77b waits on a words card. 75 waits on Tuesday's reading of the Guided hold. 15 measures only.

# B1495 DRAFTER REPORT: Security Composer lane B (PCOMP-77, PCOMP-75, PCOMP-15)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1495_SEAT-C93_composer-lane-b-web-api-polish.md` (130 lines, 12 runs of four underscores, sha256 prefix `c9d0a8ebdb9d1fc4`). An identical `.pre-stamp` sits beside it (`cmp` equal).

## BLUF
- **PCOMP-77 is bigger than the sweep's "M".** The ruling (C-71 COMP-11 (a), `CLARIFICATIONS.md:1307`) has three blockers in code:
  - the web validation (`apps/web/src/screens/w2/model.ts:733`);
  - the API refusal (`apps/api/src/routes/inputs.ts:979-986`, 422 `DECISION_INCOMPLETE`);
  - a database CHECK (`packages/db/migrations/0001_core_schema.sql:318`) that refuses a NULL rationale on any custom row.

  The contract already allows a null rationale, so it needs no change. I split the ticket in two:
  - **77a** removes the justification for a secret field's local value. It is ruled and adds no new word. By default it uses no migration: the empty string is stored for that one case and shown as null to every reader (D-1).
  - **77b** is the "mark all local" action. It needs new words (a label, a result line, a part-way line), so it is listed as a words card (W1 to W5) and built only when the WORDS slot carries them.
- **PCOMP-75 may be under a hold.** C-71 COMP-2 (a) (`CLARIFICATIONS.md:1298`) does not list row #76, and the ticket has no `held` label. But the ruling's consequence column reads "No Guided work until you turn it back on", and the demo runs with Guided OFF. 75(b) is Guided-only (the End page). The kit builds it only if PART-75 reads BUILD. I recommend DROP until Guided is switched back on.
- **PCOMP-15 is measure-only.** The ticket says "fix only if it shows" and gives no threshold. The kit measures the query count and time share of `buildSnapshot` inside `listControls` and proposes a Done-when. Any fix needs a criterion from Tuesday (Q-3).
- **Two environment blockers measured:**
  - the Docker daemon was NOT running at 13:53. 77a's red-first API rows run only through `scripts/test-db.sh`.
  - No git identity is configured anywhere for this project's clones (repo-local, resolved and global all empty). Under the new no-override rule, a seat cannot commit until Tuesday names how the clone gets its identity (IDENTITY slot). Earlier Composer kits, B1422 among them, used `GIT_AUTHOR_*` env overrides, which are now forbidden.
- **Seat id collision:** `SEAT-C93` was already used by B1423 (2026-11-10, READY, pane closed). I kept the commissioned file name. Every path in the kit is named `b1495`, so only the pane name repeats. If you want the house counter kept clean, rename to C94 at the stamp.

## Facts re-measured (instrument; control)
- Main `c684e808225ef04402b9e83f784831b2574ba633` (`gh api -X GET .../commits/main`). Open PRs #91, #86 (Dependabot, 2 files each) and #85 (draft, held, 57 files). Lane paths in their file lists: 0 (control: `document-pdf` 1 in #85). #85 holds four `apps/api` test files that the kit marks not-yours.
- Jira:
  - JQL `project = PCOMP AND ( key in (PCOMP-75, PCOMP-77, PCOMP-15, PCOMP-9999999) )` returned exactly the three keys (the nonexistent key was the control).
  - Issue GETs: all three are Backlog with 0 comments. Labels: seed marker plus `plan-comp-104/76/169`.
  - Full open census `project = PCOMP AND ( statusCategory != Done )` = 89, equal to the sweep's count. 75, 77 and 15 carry neither `held` nor the waiting-on-product-owner label.
- PCOMP-75's pointer is stale. The file is `apps/web/src/screens/GuidedWizard.tsx`: the heading is at `:724` and the section list at `:721`. The CSS cause is `guided.css:151` (`.gw-sections` margin 0) and `:42` (`.gw-card h3` margin `0 0 6px`). The defect is present by CSS reading; the rendered page is UNMEASURED.
- PCOMP-15's premise is present. `last-generate.ts:76` rebuilds the snapshot per call and is reached from `inputs.ts:899`/`:920`. `snapshot.ts` holds 13 `tx.query` lines; the ticket says "8 queries", so the seat recounts.
- PRIOR WORK: none.
  - 121 PRs over two pages: 0 title hits for the lane's subjects (control: `deploy guide` 10).
  - The only refs matching the lane's words, `b58/guided-end-handoff` and `s43/fx-lv-local-values`, predate the tickets.
  - The last commits on the lane's files are 2026-10-24 or older.
- Ports 9630-9639: `lsof` rc 1. Word-boundary scan over 63 non-`.pre-` SEAT kits of 11-10 and 11-11: 0 (control `964x`: 9).
- Model: Sonnet, row C2 (`model-routing.md:92`); id `claude-sonnet-5-5` (`models_latest.json:23`). `brief_seat.sh:24` defaults to Opus, so the level is written in the launch line.
- Lock `.tools/composer-heavy.lock` is absent. `.tools/b1421/scripts/heavy.sh` exists for the seat to `cp`. `.tools/b1495` is absent.
- Tests route: `ci.sh:116-118`, then `test-db.sh:58`, which runs `packages/db/vitest.config.ts` and then `apps/api/vitest.db.config.ts`. No hosted test CI; CodeQL only.

## D-decisions (drafter's recommendation first)
- **D-1 (77a storage): E.** Store `''` for a secret value-ref custom decision with no justification. API bodies answer null, and the snapshot omits `justification`. There is no migration, no DEPLOY.md operator words and no deploy-bearing change. The alternative, M (relax the CHECK in migration 0028 plus a rollback recipe plus a DEPLOY.md rollback section), is cleaner in the schema. But it adds operator words that the product owner rules word by word, and it touches lane C's file and a deploy-bearing path, so it needs its own Opus kit. A gate may call E a sentinel. The kit makes the seat close a census of every reader of the column, so no reader can show `''`.
- **D-2 (77b scope): mark only undecided secret fields that are in the current resolution.** Never overwrite a recorded decision. Run one PUT at a time with If-Match chaining, and stop at the first refusal. Client-side only, so no new endpoint and no contract bump.
- **D-3 (order): 77a, 77b, 75, 15.** The sweep's order was 75, 77, 15. I moved 77a first because it is the ruled, word-free core, and 75 is gated.

## Q-questions for Tuesday (each with a default)
- Q-1 = D-1. Default E.
- Q-2 = D-2. Default: no overwrite.
- Q-3 (PCOMP-15 fix criterion). Default: none; measure and report.
- PART-75: BUILD or DROP. Default DROP, per C-71 COMP-2's consequence column. If you read the hold as limited to its listed rows, BUILD is a CSS-only change plus one stylesheet test.
- WORDS: W1 to W3 (label, result line, part-way line), W4 optional (default: hide the action, no word), W5 optional (the S6 hint `ControlDetail.tsx:766`, which becomes untrue for a secret local value). Default NOT YET, which means 77b is not built.
- IDENTITY. Default: the seat sets clone-local `user.name`/`user.email` once with `git config --local`, equal to main's author identity (the GitHub noreply address of main's author). Whether that counts as "the repo's own configured identity" under the new rule is yours to say.
- DOCKER. The daemon must be running at launch; the seat never starts it.
- Seat id: keep C93 or rename to C94.

## UNMEASURED
- Rendered End page gap (75).
- Whether any existing test row pins the justification rule for a secret local value. The seat greps at Step 1 and STOPs if one does, because it may not edit existing tests.
- Whether `apps/api/vitest.db.config.ts` includes every `apps/api/test/*.db.test.ts`; the seat checks.
- Real query counts and timings for 15.
- Whether 77b's Controls list body carries field types for every item. ControlDetail reads `field.type` from the same control body shape, but this was not checked on `listControls`.
- Base red set.
- Docker image cache state.
- Whether `''` passes `refuseCredentialText` and the engine's string scan without effect.

## Outside the fences (disclosure)
- I wrote scratch files under `/tmp/b1495d/`: raw copies of origin files, ticket texts, the open-issue dump and PR file lists. No helper script file; the python ran inline from stdin with `-I`.
- I created the `.pre-stamp` copy with `cp` (Tuesday asked for it; it is byte-identical by `cmp`). I wrote nothing in any project folder.
- No git ref write, no Jira write, no GitHub write. No `decision_queue.sh`. No docker, az or ssh, apart from a read-only `docker version`, which found the daemon down.
- I used `gh api search/code` (GET) in addition to `contents` and `trees`.
- I read the DRAFTER_RULES' `/Volumes/Laptop-DEV` paths as `/Volumes/Datasec_DEV`.

READ-WHOLE-BY-TUESDAY: ____
