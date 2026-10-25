# B597 DRAFTER REPORT (SEAT-G86, HPSM-POC tier-2 gate kit for PR #209, fast-uri 3.1.8 -> 3.1.9)

Drafted 2026-10-24 19:01-19:10 AEDT, read-only (model claude-sonnet-5-5, row drafter).

## BLUF
The kit is written: `2026-10-24_B597_SEAT-G86_hpsmpoc-209-gate-tier2.md` (75 lines; 6 checks, no mutant matrix). Instruments: `/usr/bin/grep -c` of the four-underscore pattern = 8 (seven slots + last line, as in B590); the at-sign pattern = 0; non-ASCII bytes = 0. **One thing Tuesday must know before stamping: the repo's own dev-audit step (`web/scripts/audit-dev.mjs`, and the production `npm audit --audit-level=high`) blocks only HIGH and CRITICAL, and an earlier gate recorded the fast-uri finding as MODERATE (records C-174 "Not settled", B578-2). So that step is expected to exit 0 at main AND at head and cannot show this fix. The kit therefore makes the red-first the `npm audit --json` advisory list (four ids at main, none at head), with the repo's exit codes recorded as "no worse", and says the hypothesis is to be measured, not trusted.**

## Facts read (instrument)
- PR #209 (`gh api -X GET pulls/209`, 19:02:09 by `date`): open, not draft, author `dependabot[bot]`, head `4dabf18903cc2fc0a8e6b7c66f70a981cf8f7973`, base/main `f5241f20861808a44a2ca8ba51910c6e9726b358`, 1 commit, 1 file, +3 -3.
- Patch (`pulls/209/files`): only version, resolved, integrity inside `node_modules/fast-uri`; `"dev": true` follows unchanged.
- Check-runs on the head (`commits/<sha>/check-runs`): 16 completed, 15 success, CodeQL neutral (names listed in the kit).
- Dependent (`contents/web/package-lock.json` at the head, grep): `ajv` requires `fast-uri ^3.0.1`; `web/package.json` pins `ajv 8.20.0`. Other dependents UNMEASURED (the gate enumerates).
- CI audit steps (`contents/.github/workflows/ci.yml` at the head, lines 387-393) and `audit-dev.mjs` (69 lines, `EXCEPTIONS` empty, blocks high/critical).
- Records rules (`gh api contents` of the records repo's `1_Project_Definition/CLARIFICATIONS.md`, 3086 lines, grep): landing = squash head-pinned by the coordinator (`:138`, C-173, C-175); braces exception C-44 / C-99 POC-4 lapsed (C-174); no rule found that changes the gate; the kit tells the gate to confirm.
- Ports: `lsof -nP -iTCP:9300-9499 -sTCP:LISTEN` printed nothing. The B59x briefs contain 9490-9499 only inside scan ranges (grep hits are B586/B591/B593 files); I did not classify each hit as allotment or range. The block is the lead's assignment and the kit tells Tuesday to re-read it.

## Decisions Tuesday must confirm at the stamp (stamp decisions: 5)
1. **Audit red-first is the `npm audit --json` list, not the repo's exit code** (recommend: confirm; otherwise the gate would "fail" a control that cannot fire).
2. **Local suite is conditional**: relies on the PR's green web unit and web build jobs unless load1 < 8, then runs lint, typecheck and the vitest suite (recommend: confirm; a one-package dev-only lockfile bump with 15 green checks does not justify a forced 4-minute suite under load).
3. **Hard stop**: suggested target verdict 45 min, hard stop 90 min after Step 0 (recommend: confirm; much smaller than B590's 2 h / 3.5 h).
4. **Port block 9490-9499** reserved though no host is expected (recommend: confirm it is still free at the stamp).
5. **Jira**: allowed as optional GET only (zero control), no ticket written (recommend: strike it if you want the gate Jira-free; nothing in the checks needs it).

## Choices the drafter made, no decision needed
- Pane name `Datasec/HPSM-POC-G86`; B-number B597; no `.pre-stamp` file written (you asked for exactly two files; the unstamped copy of the kit is the file as written, 8 slot lines, until stamped).
- Gate fetches `refs/pull/209/head` inside its own clone (the head is not a named branch); an advisory-feed-lag control (two audits a minute apart) and a withdrawn-advisory control (GHSA-vfj7-8cjw-p6xm) are included.
- A moved head gives NOT GATED; PR not open gives NOT GATED; a Dependabot alert or CodeQL alert is never dismissed.

## UNMEASURED
Everything needing a run: `npm ci`, `npm audit` at either side, which of the four ids npm reports at main and at what severity (I did not run npm; the "moderate" is RELAYED from the records), whether any package besides `ajv` requires fast-uri, `npm ls --omit=dev`, the registry integrity of 3.1.9, CodeQL's neutral reason, code-scanning alerts on `refs/pull/209/head`, `mergeable_state`, the commit's verification status, the four advisories' own fields (not fetched), HPSMPOC-346's text (no Jira read), lint/typecheck/vitest at either side.

## Fences
Inside: two files written with Bash heredoc (allowed by the session's bypass note; the Write tool was not used). Read-only GitHub GETs under the project's `GH_CONFIG_DIR` only; no git command in any project repo (I ran one `git ls-remote` with no URL in the Tuesday folder, which errored, "illegal line count", nothing read or written); scratch files (`clar.md`, `ci.yml`, `audit-dev.mjs`) in the session scratchpad. Outside the fences, disclosed: my first Bash call used `cd` and was refused by the hook (no effect). No Artifact, Docs, mail, chat, Jira, decision_queue, npm, or hosted-site call. The records file is the project's own, not another client's.
