STARTABLE: YES (subject to Q-1 to Q-3 defaults; launch queues behind G368 on the jest lock)

# B1378 drafter report (SEAT-N113, NexusAI RD-973 merge-main resume)
Clock at drafting: `date` printed Mon 9 Nov 2026 08:56:36 AEDT. Kit 55 lines. Files: `briefs/2026-11-09_B1378_SEAT-N113_nexusai-rd973-merge-main.md` (+ identical `.pre-stamp`, `cmp` rc 0), `2026-11-09_B1378_slots.json`, this report.

## BLUF
Main is `9926903f25489d0fc9879e98daa6c51306aba9bc` (PR #182 merge; compare main...b1369: ahead 1, behind 10). The branch is still `1f3365eb8608d34da2016a2221a755487febadae` at origin. The only path in both change lists is `scripts/verify-expected-counts.json`, so the merge should conflict there alone. Predicted merged pair **5493 / 326**.

## Facts re-measured (instrument, control)
- main sha: `gh api git/ref/heads/main`; PR list `state=all` shows 182 closed with merge_commit_sha `9926903f` (control: 181 reads `fe75d7b2`). Open PRs 0.
- b1369 ref via `git/matching-refs/heads/b13` = `1f3365eb`; parent `fe75d7b2`; contents-API blobs: simpleDb `c2e4274b` (804 lines), rd973 test `a41027cb` (187), counts `3b3419c1` (5374/323). `git hash-object` of the saved bytes equals each. `awk NR==629` and `NR==641` of the saved simpleDb both print the ROLLBACK-callback line.
- main counts blob `6e3e934e`, `awk NR==4` 5488, `NR==5` 325 (control: old `a27fbeb5` 5369/322). Main's `simpleDb.js` blob `572b4e0d` (unchanged), rd973 absent on main (404; control: present at the branch).
- File lists by `compare/...` (`--jq .files[].filename`): branch = simpleDb, rd973 test, counts; main-since-`fe75d7b2` = the 7 files named in the kit incl. counts. Intersection = counts only (control: both lists print the counts name).
- Pair derivation: 5488 + 5 and 325 + 1. The 5 is `/usr/bin/grep -c -E "^\s*test\("` over the saved rd973 blob (control: `.each|.skip|.only|.todo` count 0); matches the builder's `jest --json` 5 tests/1 suite (RELAYED, B1369 STATUS D7).
- b1376 branch `8f94d795`: compare main...: ahead 1, behind 10, files = the three port-band files; no counts file, no simpleDb. No `refs/heads/b1378*` (matching-refs length 0). `worktrees/b1378*`, `session-tools/b1378` absent.
- Ports 9650-9659: `lsof` 0 listeners (control 13 listeners overall); word-boundary scan of non-`.pre-` SEAT kits 8-9 Nov: `965x` 0, control `964x` 1 (B1377 only). Panes: `tuesday`, `Datasec/NexusAI-G368`, `fleet-monitor`.
- Repository variables `total_count` 0 (gh api). CLARIFICATIONS `grep -n 'Merge path'` prints `:2067`.
- `verify-suite.sh:242`-`:252` parses the expectation file in the non-bypass branch (the node -e block), even when `--update-counts` is given. So conflict markers in the counts file would fail the run. The kit therefore has the seat write main's blob bytes into the file by redirect first, then run `--update-counts` once. This is the drafter's reading of the script; the seat's first run decides (STANDING LINE 8).
- `build.yml:83`/`:84` and `verify-suite.sh:91`/`:92` re-printed by `awk NR==n` at `9926903f`.

## D-decisions
- D1 One merge commit carrying the regenerated counts file, not the two-commit shape used on b1340 (merge `510a4068`, then regen `2b60ff66`). One commit keeps "regenerate once" tied to the merge and leaves one fast-forward push.
- D2 Fresh clone `worktrees/b1378-n113` (B1369's REFUSE forbids reusing `worktrees/b1369-*`); it costs one `npm ci`.
- D3 No CodeQL pre-scan of new lines: the diff against main is the same three files; the kit says so and leaves the hosted verdict UNMEASURED.
- D4 Gate row G2, as for B1369.

## Q for Tuesday (each with a default)
- Q-1 One merge commit with the regenerated counts, or two commits as b1340 did? Default: one.
- Q-2 Absolute latest time in S5. Default 13:00 AEDT 2026-11-09 (target +90 min, hard stop +150 min).
- Q-3 If a lane lands tests on main before launch, re-issue (kit STOPs on a second counts conflict) or let the seat re-derive? Default: the kit allows a newer main with the pair re-derived as main + (T,1); it STOPs only on a non-counts conflict or on commits to simpleDb/rd913/rd973.

## UNMEASURED
- The merge itself (`merge-tree` forbidden to the drafter): "conflict in the counts file alone" rests on file-list disjointness.
- That main's committed pair equals main's measured pair (CI says so; not run here).
- CodeQL on the merged head; the Deploy demo switch beyond `total_count` 0 (organisation variables were not read).
- G368's lock state.

## Outside-the-fences disclosure
Reads only: `gh api -X GET` under the NexusAI `GH_CONFIG_DIR`, `lsof`, `tmux list-panes`, `ls`, and reads of kit/briefs/CLARIFICATIONS/model-routing/models_latest/status_watch/brief_seat/nexusai-lock header lines. Saved blobs went to the session scratchpad. No Jira call, no decision card, no git command in the project repo, no write except the four files in `briefs/` (plus the scratch stamp copy in the scratchpad, from which stamp_brief.py printed `OK: 8 slots stamped by label, 0 four-underscore lines left`). The slots.json values carry only drafter facts, `PROPOSED DEFAULT` text and `@NOW@`; none attests a Tuesday read beyond the stamp's own `@NOW@` template wording, which Tuesday should overwrite. S1 and READ-WHOLE name "Tuesday" as the stamper (as the template does); Tuesday must make these true by doing the reads before stamping.
