GATE B1910: GO WITH FINDINGS

Reviewer: G2, read-only except this file. Scratch: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/b1910/ (clone + local bare.git, harness.sh, nothing pushed to GitHub; the real script was run only against the scratch clone, under /bin/bash 3.2.57). Script under review: tools/safe_push.sh (276 lines) vs safe_push.sh.pre-1122-verifyscan; the diff is exactly the three hunks the evidence describes (PRE_STAGED line 86, scan block 92-143, _notin 266-275). Nothing else changed.

Summary: the ORDER defect (commit and push before scan) is fixed, and the FIRE/QUIET/NEUTRAL/CONTROL-FAIL/LEFT-OUT arms reproduce. But the path selector and two gitleaks behaviours let a token through in shapes a careful agent or a plain filename can produce. None is a regression against the old script (which scanned nothing before commit); three are silent misses of the very control being built. Ship, then fix the Majors.

## Findings

### Major M1 - non-ASCII filename in a verify folder is never scanned (silent miss, token pushed)
Line 104: `git diff --cached --name-only` C-quotes non-ASCII paths (core.quotePath default true), so the path arrives as `"2_Project_Files/.../caf\303\251.md"` with a leading double quote, and line 106 `grep -E '^2_Project_Files/...'` does not match. Measured: file `2_Project_Files/tuesday/briefs/g_verify/café.md` holding a ghp_ token: rc 0, no scan line, committed AND pushed (harness case nonascii-token). Fix: `git -c core.quotePath=false diff --cached --name-only` (or `-z` with a NUL-safe loop) at lines 86 and 104; apply to PRE_STAGED too so the set difference stays consistent.

### Major M2 - `gitleaks:allow` comment suppresses a finding
`gitleaks dir` honours an inline `gitleaks:allow` unless `--ignore-gitleaks-allow` is passed (see `gitleaks dir --help`). Measured: a verify file whose token line ends `# gitleaks:allow` gave rc 0, "scan clean (1 files, control fired)", pushed. The content under scan is agent-authored, so the agent controls that comment. Fix: add `--ignore-gitleaks-allow` to the scan call (line 137) and the control call (line 128, so the control exercises the same flags).

### Major M3 - "any depth" not met: `briefs/<x>/<name>_verify/` is not matched
Regex line 106 is `briefs/[^/]+_verify/`, i.e. one level only. Measured: `briefs/sub/a_verify/t.md` with a token: rc 0, no scan, pushed. (Files nested DEEPER inside `<name>_verify/` are matched and were refused correctly.) The kit's glob `briefs/*_verify/*` matches across slashes; the regex should be `^2_Project_Files/tuesday/briefs/(.*/)?[^/]*_verify/`. Judgement: the real agent folders sit at briefs/<name>_verify/, so this is a Major for the kit text, lower in practice.

### Major M4 - a staged DELETION (or a rename's old side) in a verify folder refuses every push with a misleading message
`--name-only` lists deleted paths; `git show :<path>` then fails (line 140) -> "cannot read index blob". Measured: `git rm --cached` of a committed verify file then safe_push with no verify arg: rc 3 "cannot read index blob .../del.md"; a `git mv` rename gave rc 3 on the old path. Safe direction (nothing committed or pushed) but a legitimate cleanup can never be pushed through this tool, and because the path was pre-staged it is NOT unstaged (see M5), so every later call refuses too. Fix: `--diff-filter=d` on line 104 (deletions have no blob to scan), or skip paths with no index entry.

### Minor m1 - caller-pre-staged paths remain staged after a REFUSE
By design the script unstages only what THIS call staged (STAGED_BY_CALL). Measured: pre-staged token file, call with no args: rc 3, nothing committed/pushed, but the file stays in the index and the next unrelated safe_push call refuses again. Behaviour matches the kit ("exactly the paths this call staged"), but the REFUSE text should say "left staged: <paths>; unstage with git reset". Also: a path staged before AND re-added by the call with new content is not reset.

### Minor m2 - gitleaks default global allowlist silently skips some file types in a verify folder
Measured with gitleaks 8.30.1 (`-l debug`): `node_modules/**`, `*.svg`, `*.png` are "skipping file: global allowlist"; a token in each gave rc 0 and passed. (Binary-looking .dat WAS caught; vendor/, .lock, .min.js, .json, .txt, .log, .sql were caught.) Control cannot detect this because it is a .txt. State it in the comment, or pass a config that drops the path allowlist.

### Minor m3 - exit code 3 is now overloaded
Header comment lines 26-29 still document 3 as "pushed but HEAD != origin"; refusal now also returns 3 with nothing pushed. I found no scripted caller that parses the rc (panel_sync.sh, wed_claim.sh only mention the script in comments), but the other seat and any human reading "rc 3" will assume a push happened. Update the Exit: line; consider a distinct code (e.g. 7).

### Minor m4 - `_notin` rc and rename display
Last statement of the script is `_notin`; its rc is the while loop's, so it is 0 today, but that is incidental (an explicit `return 0` would make "never changes the exit code" structural). A staged rename prints `old -> new` after the prefix strip. Cosmetic.

## Answers to the six questions
1. Reach: nested-too-deep (M3), non-ASCII (M1), deletions/renames (M4) fail; spaces and a leading dash (`-x y.md`) PASS (rc 3 refuse, scanned; `git show ":-x y.md"` is fine); caller-pre-staged PASS (scanned from the index; remains staged on refuse, m1); many files: a single-loop copy, no limit seen (the 3-file ignorefile case and 2-file seed worked; I did not run hundreds).
2. Misses: M2 (`gitleaks:allow`), m2 (default allowlist). `-i "$VT"` points gitleaks at a .gitleaksignore in $VT itself, a directory the blobs never occupy: a staged `.gitleaksignore` containing `*` and a staged `.gitleaks.toml` with `paths=[".*"]` inside the verify folder did NOT hide the token (rc 3). Config discovery is from the target `$VT/blobs`, which never contains a root toml. `--redact` only masks output; rc unaffected (FIRE refuses with redaction on).
3. Refusal branches: control fail (stub rc 0 and stub rc 2), missing scanner (PATH=/usr/bin:/bin), non-executable override, unreadable blob, finding: each printed REFUSED, left no new commit, bare main unchanged, and unstaged what the call staged (pre-staged excepted, m1). `exit 3` is reached everywhere: `_vrefuse` is called in the main shell (the blob loop uses a here-string, not a pipe); only the unstage loop is piped, and `exit 3` follows it outside the pipe.
4. bash 3.2: ran every arm under /bin/bash 3.2.57. `<(...)` process substitution, `<<<`, and `grep -vxF -f` with an empty PRE_STAGED (a single blank line pattern; -x makes it match only blank lines) all behave (seed run: empty index, rc 0). No mapfile/`${x,,}`/assoc arrays.
5. NEUTRAL: no verify path, no gitleaks call, no new output line except NOT IN THIS PUSH (confirmed again: modified tracked 0_Brain/tasks/DEPLOY-BLOCKERS.md printed `NOT IN THIS PUSH: 0_Brain/tasks/DEPLOY-BLOCKERS.md`, rc 0). `_notin` only prints; the non-matching branch still exits 3 as before.
6. Other seat: the scan block runs for any caller whose staged set touches that briefs path; unrelated seats are unaffected until they stage one. Risks: a stale pre-staged verify path (m1/M4) blocks that seat's pushes with rc 3 and the overloaded code (m3); a minimal PATH without gitleaks refuses (correct, but surprising under launchd/cron: the override env is test-only by comment). PRE_STAGED is read after step 2's checkout, fine.

## NOT TESTED
- Hundreds/thousands of verify files (time, argv limits are not involved; not measured).
- A real symlink, a submodule/gitlink, or a file over any gitleaks size limit staged in a verify folder.
- Concurrency: two safe_push calls at once (index.lock, shared $SC) and the other seat's real invocation or its machine's PATH.
- The pull/rebase, stash-count (rc 6) and conflict-resolution arms after a scan pass (unchanged code, not re-run here).
- Behaviour when TMPDIR is unwritable, or SAFE_PUSH_SCRATCH is shared between calls (fixed names under $SC/verifyscan are reused).
- gitleaks versions other than 8.30.1 (flag semantics, default allowlist, `-i`).
- Archives (max-archive-depth 0 means a zip/tar in a verify folder is not opened).
- The real repo, GitHub, and the real installed script's own run (only a byte-identical copy in the scratch clone was run).
