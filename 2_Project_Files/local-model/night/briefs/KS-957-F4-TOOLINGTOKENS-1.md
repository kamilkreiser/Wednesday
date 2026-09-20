# KS-957 F4-TOOLINGTOKENS-1 PIN THAT THE RE-LINK GUARD'S EXEMPTION ARM DENIES A FINAL STAGE WHOSE ONLY NODEISH SIGNAL IS THE TOOLING TOKEN npm, yarn OR pnpm (the three tokens the KS-930 round-2 gate's tamper T9 deleted with the main suite staying green — F4, the red-proof gap that is still live at this tip: 106/106 under T9, measured) — a NEW bash suite beside `check_shared_relink.test.sh`, the guard driven on fixture Dockerfiles, no product file — Wednesday's task for Ornith, TEST_ONLY, **ONE NEW bash suite, one hunk, 3 red cells + 3 controls, no product file** (written 06:5x on 2026-09-21, board widening round 25)

File: `Blockchain/Dev/scripts/__tests__/check_shared_relink_tooling_tokens.test.sh`
Tip: `362e51fe0db7e73d5557924902763fe3f10fd8c7`

Written from develop `362e51fe0db7e73d5557924902763fe3f10fd8c7` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 06:08 on 2026-09-21, read verbs only; the #1111 squash-merge). The test file does NOT exist at that tip: you CREATE it (`git ls-tree` of `Blockchain/Dev/scripts/__tests__/`: 29 files, ONE of them names relink — `check_shared_relink.test.sh`, the main suite, blob `867ce728ab4a`, 1228 lines, which this brief does NOT touch). The product the cells pin is `Blockchain/Dev/scripts/check-shared-relink.sh` (blob `d41c79538503`, **690 lines**, read whole): the per-file awk classifier records `nodeish[stage]` from two clauses — **the tooling clause at `:338` `        if (L ~ /node_modules|npm|npx|yarn|pnpm/) {`** and its `else if` word-arm at `:342` (`node|nodejs|bun|deno`, with a version/variant suffix); the exemption arm at `:541-567` grants `A_EXEMPT` to a final stage that writes no node_modules ONLY when `nodeish[final]` is unset, the base is not a JS runtime (`:553`), not an earlier stage (`:555`), IS in `NON_JS_BASES` (`:557`, the allow-list `nginx httpd caddy alpine busybox scratch static` at `:534`) and every line was classified (`:563`); `nodeish` set → `A_FAIL` with the message `names a JavaScript runtime or its tooling` (`:552`), rc 1. `pm_writes` (`:169-218`) decides whether a `RUN` line is a node_modules WRITE: `npm run <script>` IS one (`run` is deliberately not on the read-only allowlist, `:397-403`), so the ticket's own F4 discriminator `RUN npm run build` no longer reaches the exemption arm at this tip (it is judged by clause A: `final stage has NO ln -s`, rc 1 with or without T9 — measured); a `CMD ["npm", "start"]` line does reach it: CMD is not RUN, so nothing records a write, and the token is the stage's only nodeish signal. Runner: **bash** (a `*.test.sh` suite, run by the checker as `/bin/bash <file>` from the clone root, bash 3.2.57; `scripts/run-shell-suites.sh --list` reaches it by glob — measured).

## THE MODE — read this twice

**TEST_ONLY, NEW FILE.** Your diff touches EXACTLY ONE file: the new suite above (`--- /dev/null` / `+++ b/<path>`, the path exactly as written above, ONE hunk `@@ -0,0 +1,74 @@`). You never touch `check-shared-relink.sh`, `check_shared_relink.test.sh` or any other file: the behaviour is already what it is at the tip, and these cells PIN it.

## What the cells pin (one paragraph)

KS-957 F4 (MAJOR — red-proof gap): the KS-930 round-2 gate's tamper T9 deleted `npm|yarn|pnpm` from the tooling clause and the main suite stayed `71 passed, 0 failed`; "a third of the tooling clause has no red-proof". Round 3 widened the clause with `npx` and red-proofed ONLY the `npx` token (`R3 F2: npx in the final CMD is DENIED`, main suite `:818-821`); every other cell that reaches the clause names `node_modules` (which the word-arm also catches, `R3 ORDER`, `:900-903`) or a runtime word. **Re-measured at THIS tip: T9 leaves the main suite `106 passed, 0 failed`; deleting `npm|` alone, or `yarn|` alone, also leaves it 106/106** — the gap is live. This NEW suite drives the real guard (`bash "$GATE" "$d"`, the main suite's own idiom) on fixture Dockerfiles whose final stage is `FROM alpine:3.20` + `COPY --from=builder /app /app` + ONE `CMD`: three RED cells put `npm`, `yarn`, `pnpm` in that CMD (`["npm", "start"]` etc.) and assert rc 1 with the `names a JavaScript runtime or its tooling` message; three CONTROLS prove the same stage shape is judged by the OTHER clauses — `npx` in the CMD is DENIED (the token T9 kept), `CMD ["/bin/sh"]` is EXEMPT (`the re-link invariant does not apply`, rc 0), and `RUN npm run build` is a node_modules write judged by clause A (`final stage has NO`, rc 1) — so a red in the first three is the token and nothing else. Nothing in the product is edited; F5 (the `$` clause that cannot fail, `:486`) and F6 (the hand-written `56 of the 79` census, `:456-457`) are NOT touched — they are guard edits for the owner. **It pins TODAY's tooling clause, token by token, and changes no product byte.**

## The exact change — ONE new file

Copy every line byte for byte. All 74 `+` lines are ASCII only, contain NO backslash (the Dockerfile body is written with `echo "..."` spanning lines, not `printf '%s\n'`, for that reason) and no bash-4 idiom. There is no blank line anywhere in the fence (comment lines `#` separate the sections). Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- /dev/null` then `+++ b/Blockchain/Dev/scripts/__tests__/check_shared_relink_tooling_tokens.test.sh`.**

```
@@ -0,0 +1,74 @@
+#!/usr/bin/env bash
+# Unit tests for check-shared-relink.sh -- KS-957 F4: each tooling TOKEN of the nodeish clause is red-proofed.
+#
+# The exemption arm reads a final stage that writes no node_modules and denies it when any line names a JS
+# runtime or its tooling. The tooling clause is `if (L ~ /node_modules|npm|npx|yarn|pnpm/)`. The KS-930 round-2
+# gate's tamper T9 deleted `npm|yarn|pnpm` from it and the main suite stayed GREEN: its cells name npx, a
+# node_modules path, or a runtime word the word-arm (`node|nodejs|bun|deno`) catches on its own, so no cell
+# depended on npm, yarn or pnpm. Round 3 red-proofed only the npx token it added.
+#
+# Each red cell here is a final stage on a non-JS base that names ONE tooling token in its CMD and nothing
+# else nodeish: no node_modules write, no runtime word, no unclassified line. So the verdict is the exemption
+# arm's, and that one token is the only thing between DENIED (rc 1) and EXEMPT (rc 0).
+#
+# Every cell prints `ok <desc>` or `FAIL <desc>` so a reader can see each verdict, not only the tally.
+set -uo pipefail
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+GATE="$(cd "$HERE/.." && pwd)/check-shared-relink.sh"
+PASS=0; FAIL=0
+TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
+ok()  { PASS=$((PASS+1)); echo "  ok   $1"; }
+bad() { FAIL=$((FAIL+1)); echo "  FAIL $1"; echo "       $2"; }
+NODEISH_MSG="names a JavaScript runtime or its tooling"
+EXEMPT_MSG="the re-link invariant does not apply"
+NO_RELINK_MSG="final stage has NO"
+# final_stage <name> <expected_rc> <final stage lines> <expected substring>
+# The builder stages are the main suite's row_case preamble; the trailing COPY --from=shared-builder line puts the
+# file in the guard's class and closes the final stage, exactly as row_case does.
+final_stage() {
+    local name="$1" want="$2" body="$3" want_out="$4" d out got first
+    d=$(mktemp -d "$TMP/case.XXXXXX")
+    mkdir -p "$d/services/thing"
+    echo "FROM node:24-alpine AS shared-builder
+WORKDIR /shared
+RUN npm ci --ignore-scripts
+FROM node:24-alpine AS builder
+WORKDIR /app
+RUN npm ci && npm run build
+$body
+COPY --from=shared-builder /shared /shared" > "$d/services/thing/Dockerfile"
+    out=$(bash "$GATE" "$d" 2>&1); got=$?
+    first=$(printf '%s' "$out" | grep -m1 '::' | cut -c1-220)
+    if [ "$got" != "$want" ]; then
+        bad "$name" "expected exit $want, got $got: $first"; return
+    fi
+    if ! printf '%s' "$out" | grep -qF -- "$want_out"; then
+        bad "$name" "exit correct, WRONG rule fired (wanted /$want_out/): $first"; return
+    fi
+    ok "$name (rc=$got)"
+}
+echo "check_shared_relink_tooling_tokens:"
+# --- the three tokens T9 deleted, one cell each, nothing else nodeish in the stage -----------------------
+final_stage "KS-957 F4 npm: CMD [npm, start] in a final alpine stage is DENIED by the tooling clause" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["npm", "start"]' "$NODEISH_MSG"
+final_stage "KS-957 F4 yarn: CMD [yarn, start] in a final alpine stage is DENIED by the tooling clause" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["yarn", "start"]' "$NODEISH_MSG"
+final_stage "KS-957 F4 pnpm: CMD [pnpm, start] in a final alpine stage is DENIED by the tooling clause" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["pnpm", "start"]' "$NODEISH_MSG"
+# --- controls: the same stage shape judged by the OTHER clauses, so a red above is the token and nothing else ---
+final_stage "CONTROL npx: CMD [npx, tsx, ...] is DENIED (round 3's own red-proof, the token T9 kept)" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["npx", "tsx", "/app/src/index.ts"]' "$NODEISH_MSG"
+final_stage "CONTROL none: the same stage with CMD [/bin/sh] is EXEMPT (no tooling token anywhere)" 0 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["/bin/sh"]' "$EXEMPT_MSG"
+final_stage "CONTROL install verb: RUN npm run build is a node_modules write, so clause A judges it, not the exemption" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+RUN npm run build
+CMD ["/bin/sh"]' "$NO_RELINK_MSG"
+echo "  $PASS passed, $FAIL failed"
+[ "$FAIL" -eq 0 ] || exit 1
+exit 0
```

The suite defines its OWN `ok` / `bad` helpers (a NEW file has no helper to reuse): `ok` prints `  ok   <desc> (rc=N)`, `bad` prints `  FAIL <desc>` and one detail line indented seven spaces. `final_stage <name> <rc> <final-stage lines> <substring>` writes the fixture (the main suite's `row_case` preamble — two builder stages — then the cell's final-stage lines, then the `COPY --from=shared-builder /shared /shared` line that puts the file in the guard's class), runs the guard on that directory, and pins BOTH the exit code and the arm message (the main suite's rule: "the right exit can arrive from the wrong rule"). `$GATE` resolves from the suite's own directory to `scripts/check-shared-relink.sh` — the clone's copy, so the tampered copy when a tamper is planted. `mktemp -d`, `trap ... EXIT`, `grep -m1 '::'`, `cut -c1-220` are the main suite's idioms (`:27-49`).

## Cells

- `npm` = `KS-957 F4 npm`
- `yarn` = `KS-957 F4 yarn`
- `pnpm` = `KS-957 F4 pnpm`

## Red cells

The three cells below are GENUINE assertion-reds (a `FAIL` line the suite prints, tallied into its rc): each fails under the tamper(s) named for it and passes at the tip.

- KS-957 F4 npm
- KS-957 F4 yarn
- KS-957 F4 pnpm

*(A bash cell is named by a LITERAL PREFIX of the description that ends at a word boundary: each prefix above is followed by `:` on both the `ok` line (`... (rc=1)` appended) and the `FAIL` line, and matches exactly one cell. The controls below are named the same way — `CONTROL npx`, `CONTROL none`, `CONTROL install verb` — each followed by `:`.)*

## Tampers

Three single-line tampers on the SAME line of `check-shared-relink.sh` (`:338`, the tooling clause; it occurs EXACTLY ONCE in the file — `grep -c -F -x`, 1; positive control `grep -c -i nodeish` over the same file: 10). Each `From` is the tip's line at that number, byte for byte (8 leading spaces); each `To` is the same statement with one or three alternatives removed from the regex, and each parses under `bash -n` (the checker's rule for a shell tamper: the awk program is inside a single-quoted bash string, and no quote is touched), so the guard runs and the difference is WHICH tokens set `nodeish`, never a load error. The checker plants them ONE AT A TIME and restores the file by bytes between them.

### TOOLINGTOKENSGONE — the gate's T9: `npm|yarn|pnpm` deleted from the tooling clause; only `node_modules` and `npx` remain
File: `Blockchain/Dev/scripts/check-shared-relink.sh`
Line: 338
From:
```
        if (L ~ /node_modules|npm|npx|yarn|pnpm/) {
```
To:
```
        if (L ~ /node_modules|npx/) {
```
Reds: `npm`, `yarn`, `pnpm`

### NPMGONE — only `npm|` deleted (a per-token proof; `pnpm` still matches the pnpm cell, `yarn` the yarn cell)
File: `Blockchain/Dev/scripts/check-shared-relink.sh`
Line: 338
From:
```
        if (L ~ /node_modules|npm|npx|yarn|pnpm/) {
```
To:
```
        if (L ~ /node_modules|npx|yarn|pnpm/) {
```
Reds: `npm`

### YARNGONE — only `yarn|` deleted
File: `Blockchain/Dev/scripts/check-shared-relink.sh`
Line: 338
From:
```
        if (L ~ /node_modules|npm|npx|yarn|pnpm/) {
```
To:
```
        if (L ~ /node_modules|npm|npx|pnpm/) {
```
Reds: `yarn`

## Controls

- `CONTROL npx`
- `CONTROL none`
- `CONTROL install verb`

*(Prefixes of the suite's three control cells, each matching exactly one cell on both its `ok` and `FAIL` spelling. All three are green under all three tampers, measured: `npx` stays in the regex under every tamper, so `CONTROL npx` is DENIED by the same clause; `CONTROL none` has no token to lose and is EXEMPT either way; `CONTROL install verb`'s `RUN npm run build` is recorded as a node_modules WRITE by `pm_writes` (`:404-409`) before the nodeish clause matters, so clause A's `final stage has NO` fires regardless of the regex.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip all six cells pass: for the `npm` cell the guard's class selector finds the fixture (`COPY ... --from=shared-builder`, `:108`), the awk walks three stages, the final stage's `COPY --from=builder /app /app` has destination `/app` (not `node_modules`, `:372`) so `nmwrite` stays unset, `CMD ["npm", "start"]` is not a `RUN` so `pm_writes` never runs, and the line matches `/node_modules|npm|npx|yarn|pnpm/` at `:338` → `nodeish[3] = 1`; in `END`, `!(final in nmwrite)` → the exemption arm → `nodeish[final]` → `A_FAIL` `names a JavaScript runtime or its tooling`, rc 1 (measured). `yarn` and `pnpm` are the same path on their token. `CONTROL npx` matches `npx` → rc 1. `CONTROL none`: no clause matches `CMD ["/bin/sh"]`, `alpine` is in `NON_JS_BASES`, unclassified 0 → `A_EXEMPT`, rc 0 with `the re-link invariant does not apply`. `CONTROL install verb`: `RUN npm run build` → `pm_writes` → `run` is not allow-listed → `nmwrite[3]` set → `!(final in relink)` → `final stage has NO`, rc 1.

Under **TOOLINGTOKENSGONE** the regex is `/node_modules|npx/`: `CMD ["npm", "start"]`, `["yarn", "start"]`, `["pnpm", "start"]` match neither clause (the word-arm wants `node|nodejs|bun|deno`), `nodeish` stays unset, the base is `alpine`, nothing is unclassified → `A_EXEMPT`, rc 0 — all three RED cells print `FAIL ... expected exit 1, got 0` (measured: `3 passed, 3 failed`). Under **NPMGONE** (`/node_modules|npx|yarn|pnpm/`) only the npm cell reds (`pnpm` is not a substring of `npm start`; `yarn` and `pnpm` still match their own lines): `5 passed, 1 failed` (measured). Under **YARNGONE** only the yarn cell reds: `5 passed, 1 failed` (measured). A `pnpm`-only deletion is NOT a tamper here on purpose: `npm` is a substring of `pnpm`, so `["pnpm", "start"]` would still match `npm` and no cell could red — the pnpm token is proved by T9, where all three go. Under every tamper the three controls print `ok` and the suite exits 1 because `FAIL` is non-zero — an assertion red, not a diagnostic.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` line.** `check-shared-relink.sh` at `362e51fe0`, line 338 is `        if (L ~ /node_modules|npm|npx|yarn|pnpm/) {` (8 spaces), byte for byte; it occurs **exactly once** (`grep -c -F -x`, 1; control `nodeish`, 10 lines). `git blame` at the tip: `:338` last touched by `cdd1dcc70` (KS-930 F-QA-2, 2026-09-07); the file's last change is `852e1fff7` (KS-945, #879, 2026-09-08). Guard sha256 `56e5a44ba1016b6f`; the checker plants and restores it (T8).
- **Premise: the ticket's claim, re-derived at THIS tip.** T9 on the tip's guard: main suite `106 passed, 0 failed` (the ticket measured 71/71 at `3047bcb1d`; the suite has grown by 35 cells since and none pins the three tokens). `npm|` alone deleted: 106/106. `yarn|` alone deleted: 106/106. The ticket's own discriminator `RUN npm run build` is rc 1 at the tip AND under T9 — but by clause A (`final stage has NO`), because #879 made `npm run` a write; the CMD shape is the discriminator that survives #879, and it is the shape the main suite already uses for npx (`:818-821`).
- **Premise: the suite's contract.** Cells are printed by the file's own `ok` (`  ok   <desc> (rc=N)`) and `bad` (`  FAIL <desc>` + a detail line at indent 7) — the checker's CELL shape (indent 0-3, detail lines deeper); the tally exits 1 on any FAIL. The suite needs nothing on PATH beyond `bash`, `awk`, `grep`, `find`, `comm`, `sort`, `mktemp` (what the guard itself needs); no docker, no node, no network.
- **Premise: `+` lines that also occur at the tip.** None — the file is new. **No backslash** in any `+` line (0, counted). **No non-ASCII** (0, counted with `LC_ALL=C grep '[^ -~]'`). **No blank line** (0, counted). No bash-4 idiom (0: no `mapfile`, `readarray`, `declare -A`, `${x,,}`, `timeout`, `|&`, `&>>`, `coproc`). `bash -n` rc 0.
- **Premise: the runner.** A `*.test.sh` suite selects runner `bash`; the clone is not node-farmed for it. The checker runs `/bin/bash Blockchain/Dev/scripts/__tests__/check_shared_relink_tooling_tokens.test.sh` from the clone root; `HERE` resolves to the clone's `scripts/__tests__` and `GATE` to the clone's `scripts/check-shared-relink.sh` — the tampered copy when a tamper is planted. `scripts/run-shell-suites.sh --list` in the clone lists the new file (1; control `check_shared_relink`: 2 with it present).
- **Premise: no live-lane collision.** NEW file, so no hunk overlap with anything is possible. `check-shared-relink.sh` is not `preflight.sh`, `index.ts`, `enforcement.ts` or under `services/anchoring/**`, and is not in any of the fifteen's files. The ONE banked READY naming it is `READY_KS-958_..._2026-09-16` (bash_patch, PASS 7/7, KS-958 still Backlog/unassigned, no PR) — it changes EXACTLY the two lines `:338` and `:342` to `tolower(L) ~ ...` and adds its OWN new suite `check_shared_relink_case.test.sh`. See Collision: both orders measured; if KS-958 lands FIRST, the three tampers' `From` line becomes `        if (tolower(L) ~ /node_modules|npm|npx|yarn|pnpm/) {` and this brief's tamper fences must be re-anchored (the cells themselves stay green under KS-958: `tolower` only widens).
- **Premise: the surface.** A shell guard driven on scratch fixture directories under `mktemp -d`; no product bytes; not an auth surface.

## Collision

**NEW file — no hunk overlap is possible.** `grep -il 'check_shared_relink_tooling_tokens' night/READY_*.md night/briefs/*.md`: 0 / 0 (this brief excepted). `grep -il 'check-shared-relink.sh' night/READY_*.md`: 1 — `READY_KS-958_..._2026-09-16` (held, unmerged: the tip's `:338` has no `tolower`). **Both apply orders measured on fresh clones** (`KS-957/collision_orders.sh` → `collision_orders.log`): KS-958's diff then this file, and this file then KS-958's diff — `git apply --check` rc 0 both ways, ONE sha256 over the guard + both new suites, and after each order the new suite is 6/6, KS-958's `check_shared_relink_case` suite is 6/6, and the main suite is 106/106. Sequencing needed: none for the raise; the tamper `From` re-anchor above only if KS-958 merges first. Other open tickets on the same guard with no brief and no READY: KS-956 (row 1d, a design decision), KS-957 F5/F6 (guard edits).

## MEASURED by the writing seat (2026-09-21 06:3x-06:5x, `--shared` scratch clone `m_clone_957` at `362e51fe0`, bash runner — no node farm; source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_round25-drafter-precheck/KS-957/`)

- `measure.sh` → `measure.log`: guard 690 lines (sha256 `56e5a44ba1016b6f`), main suite 1228 lines; `:338` exact-line count 1; main suite at the tip **106 passed, 0 failed** (`tip_suite.out`); under T9 **106/106** (`t9_suite.out`), under npm-only **106/106**, under yarn-only **106/106**; the six fixture Dockerfiles at the tip and under each tamper (the table in the log: npm/yarn/pnpm rc 1 → rc 0 under T9; npm rc 0 under npm-only; yarn rc 0 under yarn-only; npx rc 1 always; no-tooling rc 0 always; `RUN npm run build` rc 1 always with `final stage has NO`). Guard restored by bytes after each (sha256 identical; `git status --porcelain` 0 lines).
- The new suite at the tip: **6 passed, 0 failed**, rc 0 (`tamper_runs.log`, first block). `tamper_runs.sh` → `tamper_runs.log`: TOOLINGTOKENSGONE **3 passed, 3 failed** (npm, yarn, pnpm); NPMGONE **5 passed, 1 failed** (npm); YARNGONE **5 passed, 1 failed** (yarn); guard restored after each; `run-shell-suites.sh --list` counts 1 / 2.
- (the golden checker runs, the wrong variants and the collision orders are appended below after the runs)

## Output

Exactly ONE ```diff block, nothing outside it: `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/check_shared_relink_tooling_tokens.test.sh`, then the ONE hunk above exactly as shown (`@@ -0,0 +1,74 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes, new file. **Raise tier: TIER 2 (a shell-suite file, no product change). Refs KS-957** (F4 only) and KS-930 (the guard's ticket, In Progress). **NEVER Closes** — KS-957's F5 (the `$` clause at `:486` that cannot fail) and F6 (the hand-written `56 of the 79` census at `:456-457`, measured 62 of 95 by the ticket) are guard edits for the owner and are not touched here.
- **Not from a gate cell.** Found by the 2026-09-21 board widening (round 25): the ticket names the gap and its tamper (T9); the discriminator was re-derived because the ticket's own (`RUN npm run build`) is now judged by clause A after #879.
- **Not pinned here, said plainly:** the `node_modules` token (already outcome-pinned by `R3 ORDER`); `npx` (round 3's own cell; a control here); the F5/F6 items; the KS-958 case axis (its own READY).
- **Instrument note:** if KS-958 merges before this raise, the three tamper `From` fences in this brief no longer match `:338` (it becomes `tolower(L) ~ ...`) — the builder will refuse the stale From and the brief needs a one-line re-anchor; the SUITE itself is unaffected (6/6 measured with KS-958 applied in both orders).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-957 night/inputs/test_only_957F4-TOOLINGTOKENS-1.json night/briefs/KS-957-F4-TOOLINGTOKENS-1.md tip=362e51fe0db7e73d5557924902763fe3f10fd8c7 ctx=65536
```

## MEASURED — appended after the golden runs (artefacts `runs/2026-09-21_round25-drafter-precheck/KS-957/`, `golden_runs.log`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md` = this brief's own fence with the two file-header lines, byte-equal to the measured suite file — `cmp` rc 0; fresh `--shared` clones at `362e51fe0`, runner bash, no farm): **run 1 `gb_clone_957_1` RESULT: PASS (8/8)** · **run 2 `gb_clone_957_2` RESULT: PASS (8/8)** — T1 one fenced block; T2 touched set == the new file only; T3 strict apply of the `--- /dev/null` diff; T4 every `+` line byte-exact; T5 green at the tip **6/6, every declared cell present**; T6 TOOLINGTOKENSGONE red set == {npm, pnpm, yarn}, NPMGONE == {npm}, YARNGONE == {yarn}, every red an assertion failure; T7 the three controls green under all three; T8 `check-shared-relink.sh` restored to sha256 `56e5a44ba101` after each. Source tracked-modified count 0 before and after (`prepare.out.log`, `checker.out.log` — the LAST run's; `golden_runs.log` has both verdicts).
- Wrong variants REFUSED (fresh clone each, `golden_runs.log`): `altered` (one fixture line changed to `CMD ["npm", "run", "start"]`) → **FAIL T4** (missing `+` line); `dropcontrol` (the `CONTROL none` cell's three lines dropped, header recounted) → **FAIL T4**; `twofiles` (the diff also carries a `:338` hunk on the guard) → **FAIL T2** (touched set); `weak` (the npm cell's fixture names `npx` instead of `npm`, built into its OWN input so T4 passes) → **FAIL T6** — TOOLINGTOKENSGONE "declared but GREEN ['KS-957 F4 npm']" and NPMGONE "reds NOTHING (0 of 6 cells failed) — the cells do not reach the tampered code": a cell that is green at the tip AND under its tamper is refused mechanically.
- Collision, both orders with the held KS-958 READY (`collision_orders.sh` → `collision_orders.log`, fresh clones `col_957_A` / `col_957_B`): `git apply --check` rc 0 for both diffs in both orders; ONE sha256 `f26ac906ac0892e5` over the guard + both new suites; after each order this suite **6/6**, KS-958's `check_shared_relink_case` **6/6**, the main suite **106/106**. With KS-958 applied `:338` reads `        if (tolower(L) ~ /node_modules|npm|npx|yarn|pnpm/) {` — the tamper `From` re-anchor named above.
