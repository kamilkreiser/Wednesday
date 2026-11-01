STARTABLE: YES

# B1042 DRAFTER REPORT | SEAT-R113 | ATTIO records: PR #3 landed (854d6dbc), FOLLOWUP_DIGEST_TO changed, ATTIO-29 design doc corrected

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1042_SEAT-R113_attio-records-29-digest-route.md` (112 lines, sha256 `a6aedc036e88a8d360a792f4c35faad1725c18adb41a629e4647c31c063636ee` at 13:38:57). The slot count is 8 (seven Stamp lines plus the last line). Control: a scratch `x ____ y` line prints 1. **No `.pre-stamp` was made:** DRAFTER_RULES allows two files only, so Tuesday copies it before stamping (B1030 practice).

## BLUF
- Sonnet records kit: C8 (`model-routing.md:98`), C7 (`:97`) for the comment text, no gate (G3 `:110`). Model id `claude-sonnet-5-5` from `models_latest.json:23`. The launch line uses `launch_when_cool.sh` with `BRIEF_SEAT_LEVEL=sonnet` inside the quotes. Ports: none.
- **Scope:**
  - One records branch `records/b1042` in `datasecau/attio`, touching at most three paths:
    - the design doc: lines 135-136 corrected, plus one dated note
    - `BACKLOG.md`: two rows by default (the undeployed tag, and gate Note N1)
    - `history.md`: one top entry
  - One commit, pushed by the seat. The seat opens one PR and **lands it itself as a merge commit** once `Analyze (javascript-typescript)` passes on the PR head.
  - After that, **one** Jira comment on ATTIO-29.
  - **0 transitions, 0 edits.**
- **Done:** ATTIO has no Done rule. ATTIO-29 has no Done-when, and history:388/:394 records it as "deliberately not Done" for reasons PR #3 does not touch. The default is COMMENT-ONLY (Q-1).
- **Description:** comment only, so the product owner's commission text stays as written (Q-2).
- **CLARIFICATIONS:** none exists and no C-entry convention exists. The kit creates neither (Q-4).

## Facts re-measured (instrument; control)
- **PR #3** (`gh api -X GET` under the Vision `GH_CONFIG_DIR`, 13:31; control `pulls/9999` 404):
  - merged 2026-10-31T23:37:40Z = **10:37:40 AEDT**, converted with `date -r`
  - merge commit `854d6dbca444020756cf4f4e551bc49edf2cc713`
  - parents `fae239bb` + `fd9d4f9d`; tree `9023e02e` = the gated head's tree
  - 3 files, +21 -2; blobs `ef75add0` / `542f2f7a` / `67d47be0`
  - verification valid; one trailer
- **Check-runs:**
  - head: CodeQL success 10:36:28, Analyze success 10:36:34
  - merge commit: Analyze success 10:39:15
- **Alerts:** open alerts on main 0 and on `refs/pull/3/head` 0. `state=fixed` also reads 0, so the live control is `code-scanning/analyses` (results 0 on both refs).
- **Main and branches:** main = `854d6dbc`; first page of `commits?sha=main` reads 2, 1, 1 parents. Open PRs #1 and #2. `records/*` heads: none.
- **Ruleset and repo settings:**
  - ruleset `code_scanning` CodeQL errors / high_or_higher; `required_status_checks` empty
  - merge, squash and rebase all allowed; `delete_branch_on_merge` false
  - workflows 2, both dynamic; environments 0; default setup configured (extended)
- **Local checkout is STALE:** local main is `fae239bb`, origin is `854d6dbc`. The four record blobs at origin main equal `fae239bb`'s:
  - design doc `5e6e5de8`
  - BACKLOG `62977c50`
  - history `0813b706`
  - CLAUDE `9c65b610`
- **Design doc:** `git grep -n -i -e wednesday -e tuesday` finds 4 lines (135, 136, 138, 150). Control `agentmail`: 1 line (135). Only 135 (address) and 136 (tag) are routing lines.
- **Record census** (BACKLOG / history / design doc):
  - `854d6dbc`, `tuesday-agent`, `FOLLOWUP_DIGEST_TO`, `2026-11-01`: 0 / 0 / 0 each
  - control `405df9c`: 1 / 1 / 0
- **CLARIFICATIONS:** `find` minus `node_modules` and `session-tools` for `*clarif*` finds 0. Control `BACKLOG*` (maxdepth 1): 1.
- **Jira** (in-process GET reader; myself 200; control `ATTIO-99999999` 404; every JQL in parentheses):
  - ATTIO-29: In Review; 3 comments by field AND endpoint (36645, 36648, 36671); transitions 11/21/31/41 (41 = Done)
  - description sha prefix `3e429cd500e65dfe`; no Done-when clause
  - project: total 30, Done 13
  - JQL: `tuesday` 0, `854d6dbc` 0, `digest` 4, `FOLLOWUP_DIGEST_TO` 2 (ATTIO-29, -30), `zzqxnonexist` 0
- **B1035 STATUS:** WRITE START 10:42:51, WRITE DONE 10:42:53 (`:79`, `:81`), restart proved (`:99`), DONE line `:157`. sha256 prefixes:
  - B1035 `3f1ade28c3aa6f28`
  - B1030 `8763b502d124bb83`
  - B1028 `4e7b6af9a7d9f2cc`
- **Seat:**
  - `R113` 0 kits (control R112: 2)
  - `B1042` 0 (control B1041: 2)
  - ATTIO `Briefs/` B1042|R113: 0 (control B1035: 3)
  - `session-tools/b1042` absent
  - panes `%0 tuesday`, `%157 Datasec/Security-Composer-R112`, `%1 fleet-monitor`; load1 2.27 (13:32)
- **Push route:** ATTIO deploy key present (`3_Access_Keys/github_deploy_rw`). `/Volumes/DevMASTER` is absent, so the shared checkout's `core.sshCommand` cannot work. The seat clones as B1028 did, with a clone-local sshCommand.

## Corrections to the relay
1. **B1035's time:** "B1035 (10:45:59)" is the STATUS close (sweep, `:155`). The setting write ran **10:42:51 to 10:42:53 AEDT** (`:79`, `:81`). The kit uses the write times.
2. **Design doc lines:** "around line 136" is two lines. 135 holds the address `wednesday-agent@agentmail.to`; 136 holds the tag. Lines 138 and 150 also say "Wednesday", but they are not routing (who set the default; who may enable task writes), so they stay unchanged.
3. **Landed time:** "landed 10:37" is `merged_at` 10:37:40 AEDT.

## D-decisions (drafter)
- **D-1: Landing source.** ATTIO records hold no landing rule. The rule quoted is Tuesday's gate-stamp ruling (B1030 kit `:97`, S3 Q-1: MERGE commit, head-pinned, never squash or rebase, after Analyze/CodeQL success). It was executed once as `854d6dbc`, the repo's first merge commit. The repo itself allows all three shapes.
- **D-2: Order.** Branch, then land, then the Jira comment, so the comment can cite the landed records merge sha. If landing stops, the comment uses its NOT LANDED clause.
- **D-3: Design-doc form.** Lines 135-136 are changed in place (token swap only), plus one blockquote note that quotes the old values. History stays visible without editing lines 138/150.
- **D-4: No B-numbers or person names** anywhere the seat writes into the repo or Jira. This is ATTIO's code-repo convention (B1028/B1030 hygiene). "Tuesday"/"Wednesday" are allowed only inside the two tags and the two agent inbox addresses. The one non-ASCII byte allowed is the em dash of the existing history heading form.
- **D-5: Identity class wording.** "The coupled Vision Sales Portal project's agent service principal", with no SP name, app id or object id.
- **D-6: BACKLOG defaults.** BL-DEPLOY ROW and BL-N1 ROW. BL-DEPS NONE, because it would add a line inside an existing row.

## Q-questions for Tuesday (default in brackets)
- **Q-1: Move ATTIO-29?** [COMMENT-ONLY, 0 transitions] There is no Done rule. history:388/:394 says "deliberately not Done" over signal gaps, and PR #3 is one output surface. The kit allows no move.
- **Q-2: Edit the ATTIO-29 description?** [COMMENT-ONLY] It is the product owner's verbatim commission; an edit rewrites history. The comment records the current values.
- **Q-3: GH identity for the seat's `gh pr create`/`gh pr merge`?** [the coupled Vision `GH_CONFIG_DIR`, the same under which Tuesday opened and merged PR #3] ATTIO has no `.gh-config` of its own. The alternative is that the seat pushes and Tuesday lands, which DRAFTER_RULES' records-seat rule argues against.
- **Q-4: Create an ATTIO `CLARIFICATIONS.md`?** [NO] The B1035 STATUS FOR TUESDAY raised this ("create it or drop it from the launch template"). It is a structural decision outside a records run. Separately, the launch template that names CLARIFICATIONS for ATTIO seats is Tuesday's to fix.
- **Q-5: BL-DEPS:** append GitHub's Dependabot count (critical 1, medium 2) to the stale "1 moderate" row? [NONE]
- **Q-6: Markdown-only PR and CodeQL.** If default setup never posts an Analyze run, should the seat stop with the PR open? [YES, `RECORDS PUSHED:`; never merge without it]

## UNMEASURED
- Whether CodeQL default setup analyses a Markdown-only PR.
- The hosted bridge at any time (B1035 facts RELAYED; Tuesday's 10:49 re-read RELAYED from the daily note line 126).
- Every gate cell (RELAYED).
- Whether main, Jira or panes moved after about 13:39.
- Who merged PR #3 (`merged_by.type` User; no name read).
- ATTIO-30's text about `FOLLOWUP_DIGEST_TO` (not opened; the kit has the seat read and list it, with no write).

## Outside the fences (disclosed)
1. One command carried an unquoted `=====` separator; the zsh hook refused it, nothing ran, and it was re-run with `----`. A first `gh api` call used an invalid `-c` flag and printed only help, then was re-run correctly.
2. Jira reads went through an inline `python3 -I -B` heredoc (GET only, `.env` read in-process for the three JIRA_ values, nothing printed but host and fields), not a project helper; ATTIO has none. I read the header of `session-tools/b1030/jira_get.py` (lines 1-40) only to see the key-name map.
3. The tree reads used the stale shared checkout's `fae239bb` objects for files whose blob shas I confirmed equal at origin `854d6dbc` (GitHub tree API).
4. GitHub reads used the coupled Vision `GH_CONFIG_DIR` (ATTIO has none), GET only, `repos/datasecau/attio/...` only.
5. No decision store, scoreboard, `briefs_staged/`, ledger, WEDNESDAY/FRIDAY tree or non-Datasec project was read. No az, ssh (beyond none), docker, HTTP to a hosted host, mail, or write outside these two files.
