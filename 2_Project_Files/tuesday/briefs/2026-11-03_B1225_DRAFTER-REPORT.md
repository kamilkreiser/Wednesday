STARTABLE: YES (after Tuesday stamps the 10 slots and answers Q-1; no word slot exists in this kit)

# B1225 drafter report (SEAT-H112, HPSM-POC HPSMPOC-442 round 2: hygiene + one pin)

## BLUF
Kit written, 66 lines (target 60 missed by 6; the two traps below needed their own facts). The gate's findings B1221-1, -2, -4 are the whole scope; B1221-3 (message) is answered by the squash. No other Blocker/Major exists in the gate's FINDINGS table (read whole), so no STOP-for-Tuesday item was built or left out. Two traps in the brief as you asked it are put in the kit as facts 3 and 5.

## Facts re-measured (instrument, control)
- Head `af6fd4c74dd77bb79efbc6773e6ad7ccff811e08` and main `f464376b1f7b62e4a5bf0c73af6c14a8c29993ea` by `gh api -X GET` at 18:24:59 AEDT (`date`), both equal to the gate's. ls-remote not used (gh -X GET, same ref).
- Brief-number census: `python3 -I -B` over `git diff -U0 f464376b af6fd4c7` in the gate's clone (read verbs only), regex `(?<![A-Za-z0-9])[bB][0-9]{3,4}(?![0-9])`, control planted `+// B9999 x` = 1: **52 added lines, 28 files; 51 carry a token no removed line of the same file has** (B1206 x45, b1206 x4 = screenshot names, B169 x2, B267 x1 at `SqliteNonTransactionalMigrationsTests.cs:32`, b241 x1). The gate said 51 lines / 48 with B1206; the difference is the case-insensitive pass (screenshot names, b241) and my token-level frame; both frames are in the kit as "re-print at YOUR start".
- 35 paths main..af6fd4c (`diff --name-only`), 0 contain `shell` (H111 partition; gate measured 0 overlap with b1097's 9 paths).
- Line pointers printed by `grep -n`/`sed -n` at af6fd4c: `page.tsx:11` lead, `FeedbackButton.tsx:1` ("use client") and `:26-27`, `ReviewHeldMigrationTests.cs:84/:101/:111/:112`, `playwright.config.ts:5` PLAYBOOK, `e2e.mjs:51` SHARDS and `:98` LIVE_API_ORDER, `FeedbackReview.test.tsx:72-74`, `model-routing.md` C1 `:91`, C4 `:94`, G1 `:108` (`awk`/`grep -n`), `models_latest.json:17` = claude-opus-5-5.
- Rename target `playbook-feedback-review.spec.ts` absent in `web/e2e/` (control: `-b241` present). `PLAYBOOK` regex matches the new name; shards list runs, not files.
- Ports: block 9630-9639 is the ONLY free 10-block in 9500-9990 by a word-bounded scan of the 150-odd non-`.pre-` SEAT kits of 11-02 and 11-03 (program printed `[9630]`); `lsof -nP -iTCP:9500-9999 -sTCP:LISTEN` = 0 lines. H111 holds 9690-9699, G321 9740-9749 (and a range text with 9759). Live panes (`tmux list-panes`): tuesday, Datasec/Security-Composer-G322, Datasec/NexusAI-N96, Datasec/HPSM-POC-H111, Datasec/MPS-G318, fleet-monitor; H112 not live. `.tools/b1225` absent (control `.tools/b1221`, `.tools/b1206` exist).
- Round count: the verdict line of B1221 reads "round 1 on class held review page and erase, NO GO 0 of 2 before"; this round is 2 of 2, a second NO GO is the cap.

## D-decisions
- D-1 Model Opus, row C4 (`:94`) plus C1's counter "same seat model" (`:91`); no row puts a hygiene-only round on Sonnet, and the files are erasure/migration code.
- D-2 Token-level hygiene property (fact 3), because the regenerated one-line strings (`openapi.yaml:7`, two `openapi.merged.json` lines of 29117 and 2885 chars) re-emit old numbers B100..B213; a literal "0 matches on every added line" cannot pass without rewriting old text, which is outside scope.
- D-3 B1221-2 not a one-line import (fact 5): `FeedbackButton.tsx` is `"use client"`, `page.tsx` is a server component; vitest would pass while `next build` or the render breaks. Kit names two shapes and requires `npm run build` + the renamed e2e on the production build.
- D-4 A6 step: `bug`/`held` row (state CHECK at head accepts `held`, old category CHECK accepts `bug`), refused Down, state asserted; settle at `:111-112` must also cover the new row (count changes from 2). Red-first under PDown (one plant, SQLite migration's Down).

## Q-questions for Tuesday
- Q-1 Accept the token-level frame (D-2) for "0 matches"? Default: yes. If the product owner wants a literal 0, the seat would have to rewrite old changelog text: a scope change, not in this kit.
- Q-2 Also strip `WORD-*` slot names and "row A6/W2/E1" mentions from comments? Default: no (not brief numbers; the gate did not list them).
- Q-3 Timing: H111 is live on shell files only; default launch right after stamping, window to Tuesday.

## UNMEASURED
- Whether option (a) or (b) of fact 5 builds under Next (seat measures with `npm run build`; the drafter ran nothing in the project).
- SQL Server behaviour of the new A6 step (docker forbidden; CI runs it).
- That PDown applies to the SQLite migration at one anchor (the gate ran its own PDown against the migration; the anchor text is the seat's to count).
- Exact count of lines the seat's fix will leave as re-emitted old strings (expected 3 to 5).

## Outside the fences
None. Reads only: the kit files named, DRAFTER_RULES, B1221 STATUS (not the evidence folder: `residue.md` NOT read, the STATUS carries the findings), B1206 template kit, model-routing/models_latest, git read verbs in `.tools/b1221/repo` with `--no-optional-locks`, one `gh api -X GET` pair. One scratch diff file written to the session scratchpad. No decision_queue, no ledger, no Jira, no HTTP to any host.
