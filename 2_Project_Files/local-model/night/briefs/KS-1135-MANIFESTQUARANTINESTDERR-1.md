# KS-1135 MANIFESTQUARANTINESTDERR-1 MAKE A RED IN `manifest_quarantine.test.sh` DIAGNOSABLE — WHEN ANY CELL FAILS, PRINT THE tsx DRIVER'S STDERR TAIL BEFORE THE EXIT TRAP REMOVES IT WITH `$TMP` — one line of the suite changed (`cleanup()`), no product file, no cell added — Wednesday's task for Ornith, TEST_ONLY, **ONE existing bash suite, one hunk (one line replaced), no product file** (written 2026-09-21 15:5x after the #1119-#1128 batch gate; its NOT-PINNED row MANIFESTQUARANTINESTDERR, "the leg-14 intermittent (item 3 / 14) … a row for the RECORD (Polish / ticket candidate for Wednesday)"; **briefed under KS-1135 — see the provenance note in the raise section: no ticket names this row; KS-1135 is the nearest live ticket and names the same class**)

File: `systemTest/__tests__/manifest_quarantine.test.sh`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`

Written from develop `9f0265eb06ecf24d4de18149ce862ad2330a61ee` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 15:30 on 2026-09-21, read verbs only; the tree `23d60cace7c3` that carries the ten #1119-#1128 squashes). The suite at that tip is **200 lines** (blob `2ae67f244ddd`), read whole; its full content is in `files[...]` of your input. It lives at the REPOSITORY ROOT under `systemTest/` (not under `Blockchain/Dev/`) and drives the real `quarantineManifest()` of `systemTest/fixtures/manifest.ts` (172 lines; `export function quarantineManifest(provisionedAt: string, target: string = manifestPath())` at `:137`, `if (!fs.existsSync(target)) return null;` at `:138`, `const dir = path.dirname(target);` at **`:139`**) through a throwaway `npx tsx "$TMP/drive.ts"` driver written at `:41-:46`. Runner: **bash** (a `*.test.sh` suite, run by the checker as `/bin/bash <file>` from the clone root, bash 3.2.57; `tsx` comes from the npx cache — no install, no network on this machine).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the suite above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above — it starts with `systemTest/`, NOT with `Blockchain/`). You never touch `systemTest/fixtures/manifest.ts` or any other file: no product behaviour changes and no cell is added — the ONE line that changes is the suite's own `cleanup()`.

## What the change does (one paragraph)

Every cell of this suite reads the driver's STDOUT (`moved="$(… npx tsx "$TMP/drive.ts" … 2>>"$TMP/driver.err")"`) and appends its STDERR to `$TMP/driver.err` — at SEVEN sites (`:82`, `:119`, `:131`, `:145`, `:147`, `:172`, `:191`; the eighth `driver.err` mention, `:60`, is the KS-1078 comment that says the streams are separated). Nothing ever PRINTS `driver.err`: the only stderr shown is the harness probe's `probe.err` (`:66-:70`), and the EXIT trap (`:32-:34`: `TMP="$(mktemp -d)"`, `cleanup() { rm -rf "$TMP"; }`, `trap cleanup EXIT`) removes `$TMP` — `driver.err` with it — before anyone can look. So when a driver run dies (tsx could not start, the module threw, a socket/IPC failure under load), its stdout is empty, the cell prints `returned ''` or `got ''`, and the one thing that would say WHY is gone. That is what the #1119-#1128 gate hit on #1125's first push: leg 14 of the pre-push preflight went red on this suite once, never again serially (0/3, 0/2), and the red was un-diagnosable — MANIFESTQUARANTINESTDERR, "a row for the RECORD". This change replaces the ONE `cleanup()` line: when at least one cell has failed (`$FAIL -gt 0`, the counter `bad()` increments at `:30`) AND `driver.err` is non-empty, print a one-line header and the LAST 40 lines of `driver.err`, each prefixed `     | ` (five spaces, a bar, a space — deeper than any cell line, so no reader or parser mistakes them for cells), then remove `$TMP` exactly as before. A green run prints nothing new (`FAIL` is 0); a red run with a silent driver prints nothing new either (`-s` is false); a red run whose driver wrote to stderr now shows it, after the tally, in the same log.

**Why `cleanup()` and not `bad()`, said plainly (a deviation from the gate row's letter):** the row proposed printing `tail -5 "$TMP/driver.err"` "beside `returned '…'`", i.e. inside `bad()` at `:30`. That line is followed by the blank `:31`, and a hunk that ends on `:30` has no non-blank trailing context (strict `git apply` refuses a mid-file hunk with none — measured: `patch does not apply`; the harness never uses `--unidiff-zero`), and a blank context line is never in a fence. `cleanup()` at `:33` sits between two non-blank, unique lines and is the ONE place that already knows the file is about to disappear — one line, all seven sites covered, the tail printed once at exit instead of once per failed cell (with nine driver runs appending to one file a per-cell `tail -5` would show the same last lines anyway). `tail -40` rather than `-5` because a tsx failure is a ~18-line stack trace and the file is shared by all nine runs — 40 keeps the last two traces whole.

## The exact change — ONE hunk in the suite

ONE `-` line, ONE `+` line, with ONE leading context line (`:32`, `TMP="$(mktemp -d)"`) and ONE trailing (`:34`, `trap cleanup EXIT`) — each unique in the file. The `+` line KEEPS the original removal (`rm -rf "$TMP"; }`) as its last statement, byte for byte; everything added sits in front of it inside one `if … fi;`. Copy every line byte for byte. The `+` line is ASCII only, carries NO backslash, no backtick, no template, and no `printf` — `echo` for the header (the string starts with two spaces and the word `driver`, so `echo` is safe), `tail -40` for the lines, `sed 's/^/     | /'` for the prefix (single quotes; five spaces, `|`, one space). `$FAIL` is the counter `:27` declares (`PASS=0; FAIL=0`), so under `set -u` it is always set when the trap fires. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/systemTest/__tests__/manifest_quarantine.test.sh` then `+++ b/systemTest/__tests__/manifest_quarantine.test.sh`.**

```
@@ -32,3 +32,3 @@
 TMP="$(mktemp -d)"
-cleanup() { rm -rf "$TMP"; }
+cleanup() { if [ "$FAIL" -gt 0 ] && [ -s "$TMP/driver.err" ]; then echo "  driver stderr (tail -40 of driver.err, shown because $FAIL cell(s) failed; the EXIT trap removes it next):"; tail -40 "$TMP/driver.err" | sed 's/^/     | /'; fi; rm -rf "$TMP"; }
 trap cleanup EXIT
```

Do NOT touch `bad()` (`:30`), the probe block (`:66-:72`), any `2>>"$TMP/driver.err"` site, or the tally lines (`:198-:200`). Do NOT add a `printf` (its format would need a backslash). Do NOT change `tail -40` to another number or `sed`'s prefix to another string: the checker holds you to the `+` line above byte for byte.

## Cells

- `stale_gone` = `the stale manifest is gone from the path consumers read`
- `copy_exists` = `a superseded copy exists`
- `copy_content` = `the superseded copy still carries the stale content (moved, not deleted)`
- `copy_named` = `the copy is named for the rejecting run AND its slot`
- `slot3` = `slot 3's copy carries slot3, so the same stamp on two slots cannot collide`
- `no_clobber` = `a second quarantine at the same stamp does not clobber the first`
- `first_content` = `the first quarantine still holds its own content`

## Red cells

No cell is ADDED by this diff — the seven cells below already exist at the tip and are GREEN there; they are declared as the red set of the tamper below, which models the exact failure this change exists to diagnose (a driver that dies mid-suite), and they are named by the literal prefixes the suite prints on its `ok`/`FAIL` lines.

- the stale manifest is gone from the path consumers read
- a superseded copy exists
- the superseded copy still carries the stale content (moved, not deleted)
- the copy is named for the rejecting run AND its slot
- slot 3's copy carries slot3, so the same stamp on two slots cannot collide
- a second quarantine at the same stamp does not clobber the first
- the first quarantine still holds its own content

## Tampers

One single-line tamper on the product the driver imports, `systemTest/fixtures/manifest.ts:139` — the line AFTER the existence check: it appends a `throw` that fires only for a September stamp (`provisionedAt.startsWith('2026-09')`). The `From` occurs EXACTLY ONCE in the file as a whole line (python whole-line scan: 1 hit at 139). The `To` is valid TypeScript (one statement added after the existing one; tsx transpiles and runs it — measured: seven driver runs die with the thrown error, nine run). **Why the condition:** the suite's four `slot $slot: …` cells (`:170-:177`) print a `$slot`-EXPANDED description that is not literally in the file, so the harness cannot name them; the slot loop and the default-path cell (`:189-:195`) use the `2026-01-01` stamp while the seven cells above use `2026-09-07` stamps, so a September-only throw reds exactly the seven nameable cells and leaves the two CONTROLs (their path does not exist — `:138` returns `null` before the throw), the four slot cells and the default-path cell green. **The tamper is the leg-14 symptom made deterministic:** the driver's stdout is empty (`returned ''` / `got ''`), its stderr carries the stack trace, and at the tip that trace is deleted with `$TMP`; with this hunk it is printed under the tally. The checker plants it and restores the file by bytes.

### DRIVERTHROWS — quarantineManifest throws after the existence check for a September stamp: the driver dies with an empty stdout and a stack trace on stderr
File: `systemTest/fixtures/manifest.ts`
Line: 139
From:
```
    const dir = path.dirname(target);
```
To:
```
    const dir = path.dirname(target); if (provisionedAt.startsWith('2026-09')) throw new Error('KS-1135 tamper: the quarantine aborted for a September stamp');
```
Reds: `stale_gone`, `copy_exists`, `copy_content`, `copy_named`, `slot3`, `no_clobber`, `first_content`

## Controls

- `CONTROL: with no manifest present it reports nothing moved`
- `CONTROL: with no manifest present it creates nothing`
- `default path resolves at call time`

*(All three are literal prefixes of the descriptions the suite prints — `:134`, `:137`, `:193`/`:194` (the ok line continues `: slot set after import …`, the FAIL line stops at `time`; the prefix ends at a word boundary and matches exactly one cell). For a BASH suite the checker matches a declared cell by a literal PREFIX; no declared name is a prefix of another (`a superseded copy exists` vs `the superseded copy still …` differ at their first word). Under DRIVERTHROWS the two CONTROLs stay green because `:138` answers `null` for a path that does not exist before the tampered `:139` runs; the default-path cell stays green because its stamp is `2026-01-01`.)*

## THE CHANGE — state it to yourself before you write a line

At the untouched tip the suite is `14 passed, 0 failed`, rc 0, and prints nothing from `driver.err` (measured — `FAIL` is 0, the `if` is false, the trap only removes `$TMP`); with this hunk it is STILL `14 passed, 0 failed`, rc 0, and prints nothing new (measured). Under **DRIVERTHROWS** with this hunk: the seven September-stamp cells fail by assertion (`returned ''`, `got ''`, `first='' second=''`), the tally reads `7 passed, 7 failed`, rc 1, and BELOW the tally the trap prints `  driver stderr (tail -40 of driver.err, shown because 7 cell(s) failed; the EXIT trap removes it next):` followed by 40 lines prefixed `     | ` — the thrown error, `manifest.ts:139`, and the `drive.ts` frames (measured: header 1, prefixed lines 40). Under the same tamper WITHOUT this hunk: the same seven reds, `7 passed, 7 failed`, and NO stderr anywhere (measured: header 0, prefixed lines 0) — the before/after the row asked for. The seven reds are assertion reds in both trees (no bash diagnostic; the prefixed lines carry no `line N:` bash diagnostic form).

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From line.** `manifest.ts` at `9f0265eb0`, line 139 is `    const dir = path.dirname(target);` (4-space indent), byte for byte; it occurs **once** as a whole line. The checker plants and restores it (T8 by sha256 after).
- **Premise: the gate's claim, re-derived.** `grep -c 'driver.err'` over the suite = **8** lines (`:60` the comment, then the seven `2>>` sites `:82 :119 :131 :145 :147 :172 :191`); `grep -c 'probe.err'` = 3 (`:66`, `:70` — shown — and the comment); no `cat`/`tail`/`head` of `driver.err` anywhere (0). Agreed: the driver's stderr is never shown.
- **Premise: the anchor.** `:32`, `:33`, `:34` are non-blank and each occurs once (`grep -c -F -x` 1 / 1 / 1); `:31` and `:35` are blank and are NOT in the fence. The hunk is a one-line replacement with one leading and one trailing context line.
- **Premise: `+` lines that also occur at the tip.** None (the `+` line contains the `-` line's removal as its tail but is a different line). ONE `-` line, the tip's `:33`.
- **No backslash** in the `+` line (0, counted). **No non-ASCII** (0). **No backtick** (0). Length 253 bytes. No bash-4 idiom (`tail`, `sed`, `echo`, `[ -s ]`, `[ -gt ]` are all bash-3.2 / POSIX).
- **Premise: the runner.** A `*.test.sh` File selects runner bash; no `Runner:` line. The suite after the fence parses (`bash -n` rc 0, measured). **The suite needs `tsx`:** `npx tsx` resolves from the npx cache on this machine (`~/.npm/_npx/fd45a72a545557e9`, tsx 4.23.15; no global tsx, no `systemTest/node_modules` — the package declares no dependencies on purpose, KS-993); the checker's bash clone is not node-farmed and needs none. On a machine with an empty npx cache the probe would fetch tsx from the registry (the KS-1078 comment at `:52-:60` describes exactly that runner).
- **Premise: the surface.** A shell suite driving a fixture helper on a `mktemp -d` directory; the default-path cell writes and restores `systemTest/fixtures/generated/actors-slot4.json` INSIDE the clone (`:189-:196`), never outside it. No stack, no port, no product bytes. Not an auth surface.

## Collision

`/usr/bin/grep -il 'manifest_quarantine' night/READY_*.md` = **0** of 259; `fixtures/manifest.ts` = **0**; `systemTest/` at all = 9 (positive control). No brief in `night/briefs/` names the suite (0). No other brief of this round touches `systemTest/`. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 15:5x-16:0x, `--shared` scratch clone `m_main` at `9f0265eb0`, bash runner — no node farm; source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_gate1119rows-drafter-precheck/MANIFESTQUARANTINESTDERR/`)

- `bare_bash.sh` → `tip_suite.out`: the suite at the bare tip **14 passed, 0 failed**, rc 0, 9 s.
- `probe_notrailing.sh`: a mid-file hunk on `:29-:30` with no trailing context — strict `git apply --check` rc 1 (`patch does not apply`), `--unidiff-zero` rc 0 — the reason `bad()` is not the anchor.
- `measure_manifest.sh` + `measure_manifest2.sh` → `measure.log`: `git apply --check` rc 0, `git apply` rc 0, numstat `1 1`; `bash -n` rc 0. With the hunk, no tamper: **14 passed, 0 failed**, rc 0, dump header 0 (`applied_suite.out`). Under DRIVERTHROWS with the hunk: **7 passed, 7 failed**, rc 1, the reds EXACTLY the seven declared, the two CONTROLs + four slot cells + default-path cell green, dump header **1**, prefixed lines **40** (`under_DRIVERTHROWS.out`). Under DRIVERTHROWS at the tip WITHOUT the hunk: 7/7, dump header 0, prefixed lines 0 (`tip_under_DRIVERTHROWS.out`). `manifest.ts` restored by checkout: blob `a6bfe3e76627` == tip. Also measured, NOT declared: an unconditional throw reds 12 (the four slot cells too — unnameable, see Tampers); a stderr-FREE red arm (`slotTag` replaced by a constant, `:143`) reds 7 with dump header 0 — the dump stays silent when the driver wrote nothing (`under_SLOTTAGGONE.out`).
- **Golden and variants:** see the drafter report (`runs/2026-09-21_gate1119rows-drafter-precheck/REPORT.md`, Row 3) — `golden_runs.log`.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/systemTest/__tests__/manifest_quarantine.test.sh` / `+++ b/systemTest/__tests__/manifest_quarantine.test.sh`, then the hunk above exactly as shown (`@@ -32,3 +32,3 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes, no new cell. **Raise tier: TIER 2 (a systemTest shell suite; no service, no runtime image).** **Refs KS-1135** — **PROVENANCE, said plainly:** no ticket names this row. The #1119-#1128 gate filed it as "a row for the RECORD (Polish / ticket candidate for Wednesday) … filed by nobody here"; the seat's board search found KS-1135 (`run-shell-suites.sh fails 6 of 25 suites under a long TMPDIR — tsx's IPC socket`, "diagnosis-first: which of the six suites spawns tsx … is UNMEASURED") as the nearest live ticket — the same class: a tsx-spawning shell suite red for a reason its output does not show. If Wednesday files the row's own ticket, re-key the brief (the fence is unchanged). **NEVER Closes.**
- **Deviation from the row's letter:** the tail is printed by `cleanup()` at exit (once, `tail -40`), not by `bad()` beside each `returned '…'` (`tail -5`) — the harness cannot anchor a hunk on `:30` (blank `:31`; see the paragraph in the brief). Same information, one place, after the tally.
- **Not touched, said plainly:** the KS-1078 probe block (`:66-:72`) already shows `probe.err`; the `tail -40` bound is a choice (two tsx stack traces); the four `slot $slot` cells cannot be declared to the harness and are outside T6's set by construction, not by omission.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1135 night/inputs/test_only_1135MANIFESTQUARANTINESTDERR-1.json night/briefs/KS-1135-MANIFESTQUARANTINESTDERR-1.md tip=9f0265eb06ecf24d4de18149ce862ad2330a61ee ctx=65536 repo_subdir=systemTest
```
