STARTABLE: YES (after Tuesday's stamp; the PR's CI was still running at the drafting read, which the kit handles; one port-block caveat in Q1)

# B660 drafter report (SEAT-G111, tier-2 gate, round 1 of 2 on its class, PR #215)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B660_SEAT-G111_hpsmpoc-215-gate-tier2.md` (153 lines). Drafted 11:22-11:30 AEDT, Sun 25 Oct 2026.

## BLUF
- The kit is B644's shape rebuilt for a one-commit PR on a base that equals main (behind 0): 9 checks, the round trip against the base file AND the head file, drift plants, mutants (CM-a..CM-v plus CM-s, CM-t, CM-w), the equivalents, the CI-matrix table, and the weakening trade (builder hazard 2) measured and classified as a Note carrying Tuesday's B652 stamp ruling (Q-2).
- Everything the lead listed re-measured matches: head `afcedf03`, base `754bf1e7`, ahead 1 behind 0, one file, +57 -42, ticket HPSMPOC-350. Differences are listed under "Where I differ".
- B660 and G111 are unused; B659/G110 are not on disk yet (so Q1 on the port block and Q2 on the names).
- The kit carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes (B644 launch-line shape), pane `Datasec/HPSM-POC-G111`, ports 9570-9579.

## Facts re-measured (instrument; control)
- **PR #215** (`gh -X GET pulls/215`, project GH_CONFIG_DIR): open, not draft, head `afcedf0374803c989cf17646e6be9ae176219697`, base `754bf1e7f6eed2f140468dd283551eca1299d46e`, commits 1, changed_files 1, +57 -42, `mergeable` true, **`mergeable_state` blocked at 11:23** (checks running; required-checks list empty, strict false); opened 11:22 AEDT. `compare 754bf1e7f6ee...afcedf03` = ahead 1 behind 0, file `web/src/audit-dev.test.ts`; `compare 754bf1e7f6ee...main` = identical (a different pair than the first: the control that compare reports behind 0). `ls-remote`: main `754bf1e7`, `refs/pull/215/head` = `afcedf03`, `refs/pull/215/merge` = `0546e7fa`. Local `git diff --numstat` = `57 42`; `rev-list --left-right --count 754bf1e7...afcedf03` = `0 1`; both shas answer `commit` in the shared clone.
- **Merge commit `0546e7fa`:** parents `754bf1e`, `afcedf0`; tree `10343f43...` = the head commit's tree (`git log -1 --format=%T`). Expected, since behind 0.
- **Blobs** (`rev-parse ${sha}:path`; zsh `$H:path` first failed as a modifier, re-run with braces): test file `65b997c9` at main, **`73740494ff85e9990f88a2fcc8dcff2dab758c2e` at the head (333 lines)**; `ci.yml` `87d7590e` at both (a main copy hashed by `git hash-object` also reads `87d7590e`). `ci.yml` anchors at main by `grep -n -F` (control `NOSUCH-zz7f3a` = 0): `web-build:` 371, production step 389-390, dev step 394-395.
- **Checks at 11:23** (`commits/afcedf03/check-runs`): 13 listed, 5 success, `CodeQL` umbrella **neutral** (two Analyze still running), 7 in progress; runs `ci` 40146445422 queued and `PR #215` 40146444118 in progress; analyses 2 of 4 (python, actions). Open alerts 0, dismissed 0 (repo-wide; no positive control, said in the kit). Rules: code_scanning (errors / high_or_higher), `required_status_checks` empty, strict false.
- **Head file read** (`git show afcedf03:web/src/audit-dev.test.ts` lines 136-333): the real-file row, the `prodRun`/`devRun` helpers, the eight derived rows, `entryKeyLines`, `document(..., entries = AUDIT_STEPS)`, the new row, matching the builder's account. Kit anchors for CM-s (`const firstKey = entryKeyLines(entries[0])[0].length;`), CM-q (`Object.entries(entry)`), CM-t (`const i = candidates.findIndex(...)`) come from that reading, to be re-derived by the seat.
- **CI-matrix** (read as text from a main copy of `ci.yml`): no matrix or shard around vitest; the rows run only in `web-unit` (line 450, `npm test`, Node 24); `web-build` reads the file via lint and typecheck; e2e (5 shards) and SQL Server (2 shards) never reach it. `vitest.config.mts` read via `git show`.
- **Jira** (GET, in-process `.env`, scratch reader `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/0642a44c-c521-4651-9987-831028b00c43/scratchpad/jget.py`, token never printed): HPSMPOC-350 Backlog, 0 comments, 0 links; Done-when matches the builder's relay. JQL `project = HPSMPOC AND ( key in (HPSMPOC-350, HPSMPOC-348) OR text ~ "qqxxzzvvnosuch" )` returned exactly the two keys (350 Backlog, 348 Done); the nonsense token contributed 0 (proves nothing alone). The project has no Jira read helper in `tools/`, so I wrote a scratch reader; the kit tells the seat the same.
- **Names:** `ls` of `tuesday/briefs/` and the project's `Briefs/` for `B66[0-9]`, `B659`, `G110`, `G111`: no B660/B659/G110/G111 file. (The only `B66` hits are the 2026-09-30 B66 files.)
- **Panes** (`tmux list-panes -a -F '#{@cockpit_name}'` 11:22): `tuesday`, `Datasec/Security-Composer-R40`, `Datasec/MPS-M21`, `Datasec/HPSM-POC-H21`, `Datasec/NexusAI-M9`, `Datasec/MPS-G107`, `fleet-monitor`.
- **Ports:** word-boundary scan of 49 non-`.pre-` SEAT kits of 10-25 per 10-block (9200-9999); control: yesterday's SEAT kits hit 9300-9309 six times, today's `*` kits hit it three times. 9570-9579: today 0, yesterday's SEAT kits 0 (other yesterday files, not SEAT kits, hit 6 times; not counted by the rule). `lsof -nP -iTCP:9570-9579 -sTCP:LISTEN` rc 1; `lsof` over 9200-9999 printed nothing. 9600-9609 and 9610-9619 were rejected because yesterday's finished kits B608/B609 name them.
- **B651 (sibling):** one path `web/src/server/mock/attribution-preview.test.ts`, pane `Datasec/HPSM-POC-H21`, ports 9300-9309, branch `b651/hpsmpoc-nonascii-digit-exempt` (not on origin at 11:23: `ls-remote 'refs/heads/b65*'` printed only `b652/...`). Named as NOT the gate's, including `.tools/b651/`.
- **Model:** `model-routing.md` rows G2 (line 109) and G-cap (line 111) confirmed by `sed -n 105,115p`; `models_latest.json` `levels.sonnet.model_id` = `claude-sonnet-5-5` at line 23.
- **Kit hygiene** (grep, controls from the template): four-underscore lines 8 (7 slots + last line), `@[A-Z_]+@` 0, non-ASCII 0, person-name pattern 0.

## Where I differ from the lead's brief
1. The lead said verdict word "GO WITH FINDINGS"; B644 used "GO WITH FOLLOW-UPS". I used FINDINGS as instructed (the shape otherwise B644's).
2. "Re-measure ... head afcedf03 ... ahead 1 behind 0": same. The base tip equals main, so there is no moved-main coupling check as in B644; 8e collapses to one run (the base and head `ci.yml` blobs are the same `87d7590e`).
3. `CLARIFICATIONS.md:138`: B652's drafter said line 138 of the root copy "is about other decisions". In `1_Project_Definition/CLARIFICATIONS.md` line 138 does contain "squash-merged head-pinned" (a record of an earlier PR). The kit cites it as evidence of a convention, not a rule, and says so.
4. The fence says scan today AND yesterday for ports; the lead said today. I did both (the fence wins).
5. The commit's trailer is `Co-Authored-By: Claude Opus 5.5` (the builder ran on Opus although its kit routed Sonnet; its STATUS says so). B644's trailer test named Sonnet 5.5, so the kit's trailer test is "one Co-Authored-By: Claude line" and the model mismatch is a provenance Note.

## Decisions for Tuesday's stamp
- **D1** Verdict word GO WITH FINDINGS (per the lead). Accept, or switch to the fleet's FOLLOW-UPS.
- **D2** Weakening trade (builder hazard 2): classified as a Note carrying your B652 stamp ruling (Q-2). If you want the gate to count it a Major, say so before launch.
- **D3** X-keep (a `run` ending in a blank line, the builder's HOLD): the kit has the seat reproduce it under base and head and classify; default Minor/Note, escalates to a SAME-class Major only if the seat shows a legitimate table can produce it.
- **D4** CodeQL umbrella `neutral`: the kit treats a final non-`success` umbrella as NOT success (verdict at most GO WITH FINDINGS, conditional) after reading its output. Accept or loosen.
- **D5** Round count wording: "round 1 of 2 on class 'audit-dev rows derive from the table'", NO GO 0 of 2 read from B636 (NO GO, other class) and B644 (GO WITH FOLLOW-UPS).
- **D6** Squash message: PR title carries `HPSMPOC-350` and the body `Builder B652 (seat H22)`. The kit tells the seat to log this as a Note for the squash wording, not a finding. Reword the PR or the squash subject yourself.
- **D7** Hard stop: suggested target verdict 1.5 h and HARD STOP 3 h after Step 0 (no absolute cap written; B644 had 12:30). Pick an absolute cap if you want one.

## Questions with defaults
- **Q1** Port block: 9570-9579 chosen. The Composer gate kit being drafted (B659) might also pick the descending sequence (9950-9959 is the next free in that style); I avoided it. Default: keep 9570-9579; re-run the scan and lsof at the stamp, move if B659 took it.
- **Q2** B660/G111: unused now; B659/G110 do not yet exist. Default: keep B660/G111; if B659's drafter lands G111 first, take G112 and say so in the stamp.
- **Q3** Should the gate wait for CI to finish before heavy work? Default: no; Checks 1-6 and 8 are CI-independent, and the kit makes the verdict conditional on pending checks.
- **Q4** `mergeable_state` was `blocked` with checks running. Default: the seat reads it at the end and, if still blocked with all checks green, names the rule or review that blocks (kit 8c).

## UNMEASURED
- Nothing was run (no npm, vitest, lint, typecheck, build, worktree, clone, fetch, mutant): the 25-red fan-out, the 28 of CM-h/CM-i, the plant tables, and the regression row red/green are all the builder's claims.
- Whether the three kit anchors (CM-s, CM-q, CM-t) are unique in the file (read, not `grep -c`-counted); the seat counts them.
- Whether the CodeQL umbrella ends `success`; whether `blocked` clears; the final `web e2e` shard list (not yet listed at 11:23).
- Whether B651 opens a PR before this gate ends.
- HPSMPOC-346 and other tickets were not re-read by me.

## Outside-the-fences disclosures
- I wrote one scratch file outside the two named outputs: `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/0642a44c-c521-4651-9987-831028b00c43/scratchpad/jget.py` (Jira GET reader), plus `ci_main.yml`, `kits.txt`, `kits25.txt` in the same scratchpad (copies/lists read from main and the briefs folder). All scratch, in the designated scratchpad; none in a project folder.
- Read the Jira ticket HPSMPOC-350 and one JQL (GET only, in-process token, never printed). Parenthesised JQL used.
- No `gh` write, no `-X` other than GET, no HTTP to hosted hosts, no cd, no worktree/fetch/merge-tree.
- A first `git rev-parse $H:path` call in zsh failed (modifier parse) and a tool hook printed three advisory case-sensitivity warnings on grep; none blocked or changed a result.
- I did not read `fleet/briefs_staged`, `scoreboard.md`, `_ledger.md`, the card store, WEDNESDAY/FRIDAY trees, or any non-Datasec project. I read B651's kit only for its lane lines (path, pane, ports, branch).
