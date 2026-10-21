# B425 drafter report (read-only drafter, Sonnet 5.5, 2026-10-21 about 23:2x AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B425_SEAT-L37_nexusai-land-pr101.md` (89 lines; one stamp slot `@STAMP_TIME@` at line 23; last line `READ-WHOLE-BY-TUESDAY: PENDING`).

## BLUF
Brief is ready to stamp, with ONE thing you must rule on first: `land.sh` as it stands would exit 8 on this PR, because PR #101's ref carries open alert #151 (the expected R1 alert) and `land.sh:33` stops on any non-empty list. I wrote an exact-row allowance for your copy of the tool into Step 2; strike it if you disagree and the seat has no way to land.

## Questions for Tuesday (each with a recommendation)

**Q1. Authorise the one-line, exact-row allowance for #151 in the seat's COPY of land.sh (Step 2 edit 2)?**
Why it arises: MEASURED `gh api ...alerts?ref=refs/pull/101/head&state=open` = one row, `151 js/file-access-to-http medium warning tests/uat-run.js` (line 43). `session-tools/s100o/land.sh:33` = `if [ -s alerts-pr<N>.tsv ]; then ... exit 8`. B394 and B414 never hit this because their PRs added or kept no alert on the PR ref. Gate B420 `:7` says #151 on the PR ref is "R1: expected, not new", and the checklist (`:90`) says "any other new number = STOP", which is exactly a number allowlist.
Recommendation: YES, as drafted. The edit is an equality test against the full measured TSV row (number, rule, security level, severity, path); a second row, a different level or path, or a different number still exits 8; the seat must prove that with five scratch controls and `bash -n` before running, and STOPs if it cannot. Alternatives, worse: (a) have the seat STOP at exit 8 and ask (a guaranteed wasted launch); (b) you edit and stamp a Tuesday-owned land script (outside the briefs/specs scope of this drafter).

**Q2. Keep `deploy-demo` as an expected-skipped run, not an expected-absent one?**
The workflow's `paths-ignore` is `**.md`, `docs/**`, `tests/**`; #102 (HISTORY.md only) produced no run, but #101 touches `__tests__/` and `scripts/`, so a run should exist and read `completed/skipped` like the last three on main (MEASURED `gh run list --workflow "Deploy demo"`). The repo variable `CI_DEPLOY_ENABLED` could not be read (HTTP 404; org variables 403 per B420 §6), so the skip is inferred from three prior skipped runs, not read.
Recommendation: keep as written (expected skipped; waiting or running = STOP and approve nothing). No action needed unless you want the variable read by someone with the right.

**Q3. One combined landing, two ticket records: fine?**
Both tickets sit in one PR, so Step 5 posts one comment each on RD-874 and RD-875 (each `To Do`, each with 1 existing comment, MEASURED) and transitions each by id 31 only to Testing, per `CLAUDE.md` "When completing work" step 2 and the B414 precedent for RD-780. The comment bodies are new text I wrote from B420's findings (N33-1, N33-6, N33-7); they are marked for your byte-for-byte approval and each figure is asserted by the seat against its source before posting. Recommendation: read the six sentences in Step 5 before stamping; cut N33-7 (Polish, PR body wording) from RD-875's Findings if you think a ticket comment is the wrong home for it.

**Q4. C-68 `:671` (counts regeneration after a merge) is not triggered here and the brief says so.**
The seat lands the gated head itself, no forward merge; the counts blob `c050e783…` (4971/305) is the one the gate's full verify ran on. If main moves before launch, the brief STOPs (a new head, new gate). Recommendation: no action; just note that the B414 open item (`:671` vs "no regeneration") does not apply to this landing.

## Measured pins (instrument beside each; all 2026-10-21 23:1x-23:2x AEDT, `date` confirmed)

| Pin | Value | Instrument |
|---|---|---|
| main | `b8715182808a2c1cf64f009b1a6e23758c63e43a` | `git --no-optional-locks ls-remote origin refs/heads/main` |
| branch and `refs/pull/101/head` | `7c11c78f174a91ed2a376110966da19e775311e7` (both) | `ls-remote` |
| head tree | `71817e8c6b4f211752ca0d49beaa285f1363f1a4`; main tree `fbef3a20…` | `rev-parse <sha>^{tree}` |
| parents of head | `5cc06298…` + `b8715182…` | `rev-list --parents -n1` |
| ancestry | rc 0; `0 5` left-right | `merge-base --is-ancestor`, `rev-list --left-right --count` |
| PR #101 | open, draft false, mergeable true, `clean`, 5 commits, 6 files, +147/-15, base sha `b8715182…` | `gh api pulls/101 --jq` |
| delta | six paths (4 test files, counts json, `tests/uat-run.js`); 12466 bytes; sha256 `52081b4c…0530a` | `git diff --name-only`, `| wc -c`, `| shasum -a 256` |
| counts | tests 4971, suites 305; blob `c050e783…`; main blob `a2f40639…` | `git show <sha>:scripts/verify-expected-counts.json | python3 -I`, `rev-parse` |
| Build | run `39572998589`, `pull_request`, `completed/success`, head_sha = `7c11c78f…`; control run `39539672911` (old head `5cc06298`) `completed/failure` | `gh api actions/runs/<id>` |
| other runs at head | Gitleaks `39572998565` success; npm-audit `39572998620` and push `39572991934` success; CodeQL `39572992680` dynamic success | `gh run list --commit` |
| PR-ref alerts | exactly #151, medium, warning, `tests/uat-run.js:43`; main #151 open at `:30`; control `refs/pull/58/head` fixed = 4 | `gh api --paginate code-scanning/alerts?ref=...`, `alerts/151` |
| open alerts on main | 141 | same, `ref=refs/heads/main&state=open` |
| Deploy demo history | last 3 on main skipped (`39548454701`, `39512084383`, `39463981478`); repo variable unreadable (404) | `gh run list --workflow`, `gh api actions/variables/...` |
| Jira | RD-874 `To Do`, 1 comment; RD-875 `To Do`, 1 comment; id 31 -> Testing present on both; id 51 = Declined trap | python `urllib` GET by issue key, token in-process, not printed |
| root checkout | 34 porcelain lines (33 modified tracked) | `git --no-optional-locks status --porcelain` in `2_Project_Files` |
| land.sh | s100o sha256 `ae98c68f…`; b414 copy differs in line 8 only | `shasum -a 256`, `diff` |
| C-rules | C-190 `:2062/:2067/:2073/:2076-2080`, C-68 `:665/:671`, C-184 `:1966`, C-209 `:2270`, C-218 `:2362` (last entry; file 2368 lines) | `grep -n -E 'C-190|C-68|C-184|C-209'` over `CLARIFICATIONS.md` (positive control: hits at all those lines; `^\*\*C-` tail printed C-217 and C-218) |
| Model row | C5 "Merge on a GO", `model-routing.md:95`: Sonnet first, 12 rows mean 0.958, text says "squash" (NexusAI's verb wins) | `grep`/`sed -n 95p` |
| No earlier B425 artefacts | 0 `b425*` worktrees, 0 `b425*` remote refs, 0 B425 files in NexusAI Briefs | `ls`, `ls-remote` |

## How the root-checkout hazard is handled
`land.sh` does `cd "$W"` into the seat's own detached worktree, runs `git diff --quiet HEAD` there, and pushes one named commit (`git push origin <sha>:refs/heads/main`), so the 33 dirty files in `2_Project_Files` are never read for staging or swept. The worktree comes from `worktree add --detach`, which writes only `.git/worktrees/` metadata (B414 did the same and its root count stayed). The brief forbids every write verb in the root checkout and has the seat record the porcelain line count before and after. If `land.sh` could not be run from the worktree, the brief says STOP.

## Not measured / judgment calls
- Pane `L37` free: no tmux read (fence).
- The Step-2 allowance block was never executed by me (no scripts run); the brief makes the seat prove it with scratch controls before use.
- The `Deploy demo` result, the push CodeQL analysis, and whether #151 reads `:43` on main immediately after the push are the landing's own results.
- Only one stamp slot, `@STAMP_TIME@`, as instructed (the B414 "launch authority: Tuesday s135" session slot was dropped to plain "Tuesday"; add the session id if you want it).
- Ticket comment wording is mine (new text, not copied from B414), built from B420 findings; flagged in Q3.
- Fences kept: two files written, git read verbs only (no fetch, merge-tree or worktree), `gh` GETs only, Jira GETs by issue key (no JQL), no land.sh run, no scoreboard, ledger, briefs_staged or `decision_queue.sh` read, no tmux, no `cd`.
