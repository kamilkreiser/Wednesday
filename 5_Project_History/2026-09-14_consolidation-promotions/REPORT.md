# 2026-09-14 — consolidation promotions 15 / 3 / 17 + Kam-decision item 4 (option a)

Built by Wednesday's subagent, 07:33–07:42 AEST. Nothing committed (Wednesday commits). Nothing deleted.
Every edited file has a dated `.pre-0914-<topic>` backup beside it. Proof outputs sit in this folder.

Read first (as briefed): `_audits/2026-09-14_consolidation.md` — Promotions EARNED rows 3, 15, 17 and
"For Kam's decision" item 4; lessons `2026-08-06_exercise-mechanisms-before-arming.md` and
`2026-08-07_a-check-that-cannot-fail.md`. Both branches (fire and quiet) were run for every mechanism,
and each harness was shown able to FAIL before its pass was believed (item 1's first run was 0/23).

---

## Item 1 — grep case-insensitivity advisory hook (promotion 15)

**FOUND.** `2_Project_Files/fleet/hooks/pretooluse_no_cd.sh` reads hook JSON on stdin, extracts
`tool_input.command`, exits 2 to refuse, 0 to pass; parse failure passes (fail-open, stated). In
`.claude/settings.local.json` the `PreToolUse` entry (matcher `Bash`) is a LIST of two command hooks
(`pretooluse_no_cd.sh`, `pretooluse_seat_scoped_chat.sh`) — so the wiring form is "multiple hooks
listed", and the brief's first option applies: add a third list entry; `pretooluse_no_cd.sh` is NOT
touched. Contract detail checked against the Claude Code docs (v2.1.270, hooks reference, PreToolUse
decision control): a hook's **exit-0 stderr goes only to the debug log — neither the user nor the
model sees it**; the way an advisory reaches the model is a stdout JSON line
`{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"…"}}` with NO
`permissionDecision` (so the permission flow is untouched — no implicit allow).

**BUILT.**
- `2_Project_Files/fleet/hooks/pretooluse_grep_case.sh` (new, +x) — wrapper: same stdin contract;
  pipes the JSON into `grepcase.py`; exit is ALWAYS 0.
- `2_Project_Files/fleet/hooks/grepcase.py` (new) — the checker. Strips heredoc bodies (prose is not
  a grep — the same false-positive class both sibling hooks met on their first live fire); finds
  command-position `grep` / `/usr/bin/grep` (line start, `;`, `&&`, `||`, `|`, `(`, backtick, `$(`,
  `then`, `do`, `xargs`); tokenises the invocation honouring single/double quotes and backslashes;
  parses short flags in any order and combination (`-ciE`, `-qF`, `-nE`), long forms (`--count`,
  `--quiet/--silent`, `--line-number`, `--ignore-case`), `-e PAT` / `--regexp`, `--`. WARNS when
  (a) flags include c/q/n AND no `i` AND the pattern token was QUOTED and holds a space, or
  (b) the pattern (as written or as parsed) contains `$(`. Warning → stderr AND the JSON
  `additionalContext` line. `git grep` deliberately not covered (different tool; stated in the file).
- Wired: `.claude/settings.local.json` PreToolUse/Bash hooks list gains a third entry
  `bash "$CLAUDE_PROJECT_DIR/2_Project_Files/fleet/hooks/pretooluse_grep_case.sh"` (backup
  `.claude/settings.local.json.pre-0914-grepcase`; the file is gitignored, so the backup is the only
  record). Hooks are read at session start → the advisory is live from the NEXT seat boot, not in
  the session that built it.

**TESTED — 23/23** (`item1_grep_hook_exercise.txt`; harness `grep_hook_exercise.sh` copied here).
FIRE ×10: `grep -c 'do not push'` · `/usr/bin/grep -q "Context limit"` · `grep -c 'x $(y)'` ·
`grep -n -E 'a b'` · `/usr/bin/grep -nE "a b"` · `cat f | /usr/bin/grep -c 'do not push'` (pipeline)
· `--count 'a b'` · `grep -c -e 'a b'` · `grep -c 'a b' | grep -qi 'c d'` (one warning, the right
one) · `grep -q "$(cat /tmp/phrase)"`.
QUIET ×12: `grep -ci 'do not push'` · `grep -c foo` · `grep -qi "a b"` · `grep -F -i -c 'a b'` ·
`/usr/bin/grep -iF -q "a b"` · `grep 'a b'` (no c/q/n) · `grep -c "$VAR"` (no space) · a quoted heredoc
whose PROSE contains `grep -c 'do not push'` · `--count --ignore-case 'a b'` · `git grep -c 'a b'` ·
`grep -c 'single' && grep -qi 'two words'` · `ls -la`. Plus malformed stdin → quiet, rc 0. Every
case rc=0. The emitted line parses as JSON (checked through the exact wired command form with
`CLAUDE_PROJECT_DIR` set).

**HOW the harness proved it can fail:** the first draft held the checker in a quoted heredoc inside
`$( … )`; macOS bash 3.2 cannot parse a backtick-bearing heredoc there — 23/23 FAILED with a bash
syntax error before any grep was inspected. Split into `grepcase.py` (the `pathguard.py` precedent,
recorded in both files' headers); then 23/23 PASS.

**NOT DONE / limits (stated):** not live in the current session (hooks load at boot); `git grep` not
covered; an unquoted multi-word pattern cannot exist (the shell would split it) so only quoted
phrases are inspected; `-f FILE` patterns are skipped.

---

## Item 2 — `predicted-by` column (promotion 3)

**FOUND.** `2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md` has ONE table: §2a LEGITIMATE SHAPES
(lines 46–50) — the tamper/red-proof table the 09-13 row named. No `predict`/`slip`/`drafter` token
existed anywhere in the file (0 hits, matching the audit's "NO — 0 hits").

**BUILT.** Column `predicted-by` added (header + separator + three example rows, each carrying
`<drafter / Wednesday-read>` in backticks — a slash, not a pipe, because a literal `|` inside a cell
breaks the table; my first attempt used a pipe AND dropped each row's closing pipe, was caught by the
diff, restored from the backup and redone). One sentence under the table, verbatim from the brief:
"The gate reports prediction slips against `Wednesday-read` rows as Wednesday's; a `drafter` row's
prediction is weighed as a drafter's claim."

**TESTED.** `diff` before/after (`item2_template.diff`): only lines 46–50 changed and lines 52–53
added; 176 → 178 lines; `diff <(sed '46,50d' backup) <(sed '46,50d;52,53d' new)` → empty:
**every other line byte-identical.**

```
46,50c46,50
< | shape — its ordinary form, as a seat or user really produces it | expected verdict | the rule clause that yields it |
< |---|---|---|
< | `<e.g. first push with -u, which writes branch.<b>.remote/.merge>` | `<CLEAN>` | `<config IDENTICAL except branch.<pushed>.* — clause N>` |
< | `<e.g. a refused push that leaves the tracking ref stale>` | `<the verdict you intend, and its exit>` | `<clause>` |
< | `<each defect class the checker exists to catch>` | `<DIFF / refuse>` | `<clause>` |
---
> | shape — its ordinary form, as a seat or user really produces it | expected verdict | the rule clause that yields it | predicted-by |
> |---|---|---|---|
> | `<e.g. first push with -u, which writes branch.<b>.remote/.merge>` | `<CLEAN>` | `<config IDENTICAL except branch.<pushed>.* — clause N>` | `<drafter / Wednesday-read>` |
> | `<e.g. a refused push that leaves the tracking ref stale>` | `<the verdict you intend, and its exit>` | `<clause>` | `<drafter / Wednesday-read>` |
> | `<each defect class the checker exists to catch>` | `<DIFF / refuse>` | `<clause>` | `<drafter / Wednesday-read>` |
51a52,53
> The gate reports prediction slips against `Wednesday-read` rows as Wednesday's; a `drafter` row's prediction is weighed as a drafter's claim.
>
```

**NOT DONE.** The gate-side half of the 09-13 row ("the gate reports slips only against
Wednesday-read rows") is a change to the QA gate / `send_brief.sh`, not to the template — not in
this brief; the template now carries the column the gate would read.

---

## Item 3 — boot-prompt line (promotion 17 + 15's line)

**FOUND.** `Launch_Wednesday.command` line 419: `INITIAL_PROMPT="ultrathink` — a DOUBLE-QUOTED bash
string ending at line 581 `  session-end ritual in ./CLAUDE.md."`. Inner quotes are `\"` (the
2026-09-02 lesson, `2026-08-29_unquoted-heredoc-executes-backticks.md` §"The rule, extended").
The STANDING BEHAVIOUR section runs lines 518–581; its last bullet is "Wrap-up phrases … trigger the
session-end ritual". **The WED-141 doctor check does NOT exist** — `doctor.sh` has no
`INITIAL_PROMPT` / WED-141 reference; the lesson says "WED-141 puts that into doctor.sh" and nothing
did. I ran the method it describes by hand (`prompt_end_proof.sh`, copied here): extract the block,
`eval` it under `set -u` with every `${VAR}` it expands set to a dummy (12 of them — the first run
tripped on `DEVMASTER_VAULT`, so the list was enumerated from the block, not guessed), print the
variable's line count, char count and LAST line, and count `note_entry.sh` as the positive control.
`2_Project_Files/tools/note_entry.sh` exists (2706 B, 2026-09-02).

**BUILT.** ONE line inserted at 580, inside STANDING BEHAVIOUR, immediately before the "Wrap-up
phrases" bullet (so the section gains the line and the prompt still ENDS on the same line):
`- Note stamps and prompt-log stamps are GENERATED: write daily-note lines through 2_Project_Files/tools/note_entry.sh and never type a clock; every phrase grep whose zero enters a sentence is /usr/bin/grep -i with a positive control from the same file (ledger w=3, 2026-09-11).`
Asserted before writing: the line contains no `"`, no `$`, no backtick.

**TESTED** (`item3_prompt_end_proof.txt`):
```
BEFORE: block lines 419-581; INITIAL_PROMPT chars=11367 lines=163 ; LAST LINE:   session-end ritual in ./CLAUDE.md. ; note_entry present: 0
AFTER : block lines 419-582; INITIAL_PROMPT chars=11645 lines=164 ; LAST LINE:   session-end ritual in ./CLAUDE.md. ; note_entry present: 1
bash -n: parses
```
Last line unchanged; exactly +1 line, +278 chars (277 + newline); positive control 0 → 1.
`doctor.sh` line 583 exempts `Launch_*.command.pre-*` from the stray-root-file warning.

**NOT DONE.** The WED-141 doctor check itself (a permanent version of `prompt_end_proof.sh` inside
`doctor.sh`) — not in this brief; the proof script is in this folder if Wednesday wants it filed
there.

---

## Item 4 — WRAP CHECK reads the day's LAST retro block (Kam item 4, option a)

**FOUND.** `2_Project_Files/scheduler/close_wednesday.sh` lines 155–166: the predicate was
`grep -qE '^## Session retro'` (presence) then `grep -qF -- '- Went well / do differently:'`
(placeholder ANYWHERE in the note → FAIL). Since the template block at line ~15 is never the block a
rotating seat writes (they append `### hh:mm SESSION RETRO …` / `## Session retro (sN leg)` below),
the first block's placeholder failed the check every night a retro WAS written — 10 in 12. Test
hooks in the header: `WEDNESDAY_TEST_HOUR` (window guard only) and `WEDNESDAY_DRYRUN=1` (exit before
the stamp). No hook existed to point the check at a scratch note.

**BUILT** (`item4_close_wednesday.diff`, 81 lines):
- `WEDNESDAY_TEST_NOTE` — documented in the header; `NOTE="${WEDNESDAY_TEST_NOTE:-$BRAIN_DIR/daily/$TODAY.md}"`.
- `retro_verdict()` (python3 via a quoted heredoc inside a function — NOT inside `$( )`, so the bash
  3.2 trap from item 1 does not apply; the function is called with `$( )` from outside, which is
  fine): finds the LAST heading `##`/`###`/`####` whose text contains `retro` (**case-insensitive**),
  takes the block to the next heading of the same or higher level, and returns one of `PASS` /
  `PASS_NOLABEL|n` / `PLACEHOLDER|<heading>` / `NO_WENT_WELL|<heading>` / `NO_RETRO`. PASS when the
  block's "Went well" line carries text after the label (bold, dash and `hh:mm —` prefixes tolerated).
- **Fallback, added during the exercise and stated in the file:** the real-note controls showed
  three of four genuinely written retros (09-08 "LESSONS THAT FIRED", 09-11 "**Lessons APPLIED**",
  09-13 "**What the seat did**") carry NO "Went well" label at all. The brief's literal predicate
  would have swapped one false FAIL ("template placeholder") for another ("no Went-well line") on
  most nights — a check aimed at the wrong property again. So: an unlabelled last block PASSES when
  it holds ≥ 2 non-empty lines that are not template placeholder bullets, and the log names that
  branch (`PASS (last retro block has no Went-well label but N filled lines)`). A near-empty
  unlabelled block still FAILS (fixture j).
- FAIL texts: placeholder text KEPT verbatim, now suffixed with the heading it judged:
  `retro still on its template placeholder (last retro block: <heading>)`; `daily note has NO retro
  section at all` kept; new `last retro block has no Went-well line (<heading>)`; and an explicit
  FAIL if the predicate returns nothing (python missing) — a silent pass is not allowed.
- A separate log line `WRAP CHECK retro: PASS …` so the retro verdict is readable independently of
  the git-dirty count that shares `WRAP_ISSUES`.

**TESTED** — the REAL script, `WEDNESDAY_TEST_HOUR=23 WEDNESDAY_DRYRUN=1 WEDNESDAY_TEST_NOTE=<scratch
copy>` (`item4_close_exercise.txt`; fixtures under the session scratchpad `t4/`):

| fixture | verdict |
|---|---|
| (a) template placeholder first, filled `### 21:40 SESSION RETRO` last | **PASS** (filled Went-well line) |
| (b) both blocks on placeholder | **FAIL** `retro still on its template placeholder (last retro block: ## Session retro (s300 leg))` |
| (c) one filled block | **PASS** |
| (d) real 09-13 copy (no Went-well label) | **PASS** (no label, 6 filled lines) — literal predicate would have failed it |
| (e) real 09-14 live copy (placeholder only, as of 07:38) | **FAIL** placeholder — correct: no retro yet today |
| (f) real 09-08 copy | **PASS** (no label, 6 lines) |
| (g) real 09-09 copy (`- 10:27 — **Went well / do differently:** …`) | **PASS** (filled Went-well line) |
| (h) real 09-11 copy | **PASS** (no label, 8 lines) |
| (i) no retro heading at all | **FAIL** `daily note has NO retro section at all` |
| (j) unlabelled block with one placeholder bullet | **FAIL** `last retro block has no Went-well line (### 21:40 SESSION RETRO)` |

After all runs: live note md5 unchanged (YES), `state/last_close` still 2026-09-13, no
`wrap_check_2026-09-14` state file written, `bash -n` passes. The real close ritual was never run
against the live note.

**Residue, stated:** each dry run appended its `DRYRUN:` / `WRAP CHECK` lines to the real
`scheduler/logs/close_2026-09-14.log` (the script has no log override; same as the 08-27 / 08-30
exercises). Tonight's 23:00 entry will follow them in the same file.

**NOT DONE.** Option (b) (the close writes the retro itself) was not chosen and not built.

---

## Files changed (all under `/Volumes/DevMASTER/WEDNESDAY/`) and their backups

| file | change | backup |
|---|---|---|
| `2_Project_Files/fleet/hooks/pretooluse_grep_case.sh` | NEW (+x) | — |
| `2_Project_Files/fleet/hooks/grepcase.py` | NEW | — |
| `.claude/settings.local.json` (gitignored) | +1 PreToolUse/Bash hook entry | `.claude/settings.local.json.pre-0914-grepcase` |
| `2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md` | §2a table + column, +1 sentence | `BRIEF_TEMPLATE.md.pre-0914-predictedby` |
| `Launch_Wednesday.command` | +1 line at 580 (STANDING BEHAVIOUR) | `Launch_Wednesday.command.pre-0914-bootlines` |
| `2_Project_Files/scheduler/close_wednesday.sh` | retro predicate → last block; `WEDNESDAY_TEST_NOTE` | `close_wednesday.sh.pre-0914-lastretro` |

Untouched: `pretooluse_no_cd.sh`, `doctor.sh`, every daily note, every learnings file.
Proofs in this folder: `item1_grep_hook_exercise.txt`, `grep_hook_exercise.sh`, `item2_template.diff`,
`item3_prompt_end_proof.txt`, `prompt_end_proof.sh`, `item3_launcher.diff`, `item4_close_exercise.txt`,
`item4_close_wednesday.diff`.

---

## Summary to Wednesday

1. All four built, none committed; six files touched, four of them backed up as `.pre-0914-*`, two new.
2. Item 1: `pretooluse_grep_case.sh` + `grepcase.py`, wired as a THIRD entry in the settings PreToolUse list (the list form existed, so `no_cd` is untouched). 23/23 fixtures, both branches, rc always 0.
3. Item 1 contract: exit-0 stderr never reaches the model (docs) — the advisory is delivered as JSON `additionalContext`; no `permissionDecision`, so nothing is auto-allowed. Live from the next seat boot.
4. Item 1 caught its own first draft: bash 3.2 cannot parse a backtick heredoc inside `$( )`; 0/23 → split to a .py → 23/23.
5. Item 2: column + sentence in; diff shows only lines 46–50 changed and 52–53 added; all other lines byte-identical. My first attempt broke the table and was redone from the backup.
6. Item 3: line at 580, prompt's last line unchanged, 163 → 164 lines, positive control 0 → 1.
7. Item 3: the WED-141 doctor check was never built — `doctor.sh` has no such check. The proof script is in the folder if you want it filed there.
8. Item 4: the check now judges the LAST retro block; the placeholder FAIL text is kept and now names the block it judged.
9. Item 4 deviation, stated: three of four real filled retros have NO "Went well" label — the literal predicate would still have failed most nights. Unlabelled blocks with ≥ 2 filled lines PASS, logged as that branch; a near-empty one still fails.
10. Item 4 exercised via the REAL script under DRYRUN + a new `WEDNESDAY_TEST_NOTE` override on 10 scratch fixtures (incl. copies of 09-08/09/11/13/14). Live note untouched; `last_close` untouched.
11. Residue: the dry runs appended labelled lines to the real `close_2026-09-14.log`.
12. Tonight's 23:00 close is the first live fire of item 4; today's note is still on its placeholder as of 07:38, so it will FAIL honestly unless a retro block is written before then.
