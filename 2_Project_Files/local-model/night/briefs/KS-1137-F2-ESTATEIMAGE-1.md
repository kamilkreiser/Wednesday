# KS-1137 F2-ESTATEIMAGE-1 PIN THAT JOB 04'S IMAGE FILTER SCANS THE ESTATE'S REAL DIGIT-BEARING IMAGE (dev-m365-integration:latest — digits MID-name, the one of 33 compose `build:` services base scanned 0 times) — the KS-867 class proven on the real name, not the synthetic dev-auth2 — the container_trivy_image_filter bash suite, stubs on a private PATH — Wednesday's task for Ornith, TEST_ONLY, **ONE existing bash suite, one hunk, one cell added, no product file** (written 02:55 on 2026-09-21, board widening round 23)

File: `Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh`
Tip: `cbae988dbe90ebe556459ada2cb437eaf80e2402`

Written from develop `cbae988dbe90ebe556459ada2cb437eaf80e2402` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 02:55 on 2026-09-21, read verbs only; the #1105 squash-merge). The suite at that tip is **159 lines** (blob `dec2db8dee63`), read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Testing/jobs/04-container-trivy.sh` (blob `88444463f9d4`, **133 lines**, read whole): the image corpus is read at **`:62` `done < <(docker images --format '{{.Repository}}:{{.Tag}}' | grep -E '^dev-[A-Za-z0-9._-]+:latest$' | sort -u)`** — the KS-867 class (`:63-70` comment: the class was `[a-z-]`, which admits no digit); the no-images alarm at `:72-81`; the per-image trivy loop at `:86-121` (`:94` and `:114-117` are KS-1136's failed-scan handling, merged as #1051 — `42afaa9e6`, the file's last change). The suite runs the job with `docker` and `trivy` STUBS on a private PATH (`build_fixture` `:57-79`, `run_job` `:83-88`), reads which images were scanned from the trivy stub's record (`scanned_times` `:91`), and prints one `ok`/`FAIL` line per cell (`:40-41`). Runner: **bash** (a `*.test.sh` suite, run by the checker as `/bin/bash <file>` from the clone root, bash 3.2.57).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the suite above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `04-container-trivy.sh` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1137 F-2 (Polish): the KS-867 regression cell proves the digit class on a SYNTHETIC name, `dev-auth2:latest` (`:49`, `:101-103`), while the producible digit-bearing instance on this estate is **`dev-m365-integration:latest`** — the `m365-integration` `build:` service of `docker-compose.yml` (`:852-857`, one of 33 `build:` services; compose names a built image `<project>-<service>:latest`, and the gate measured base scanning 32 of 33 with that one scanned 0 times, "across 32 image(s)", rc 0, no alarm). The ticket asks for "an owner cell that feeds the 33 real `build:` names (or at least `dev-m365-integration:latest`) through the recording stub and asserts it is scanned — it says why the class matters here". This change adds CELL 3b: a corpus of `dev-m365-integration:latest`, `dev-auth:latest` and `postgres:15` fed through the suite's own `build_fixture` / `run_job` / `scanned_times`, asserting the job exits 0, the estate image is scanned EXACTLY once, and the artefact's `images[].image` names it exactly once. The name's digits sit MID-name (`m365`), so a class that admits only a TRAILING digit — enough to keep the `dev-auth2` cell green — still skips it; that is the seam this cell closes, and the tampers below plant exactly it. Every existing cell is unchanged; nothing in the product is edited (F-4, the `jq` PATH check at `:33`, is NOT touched — it is a suite edit the ticket leaves to its owner, and on this platform `/usr/bin/jq` 1.7.1 makes the shipped suite green). **It pins TODAY's filter on the estate's real name and changes no product byte.**

## The exact change — ONE hunk in the suite

The new cell goes between CELL 3 and CELL 4: directly above the separator line that opens CELL 4's comment block (`:140`, `# ---------------------------------------------------------------------------` — `#`, a space, 75 dashes, 77 characters; it is the ONE trailing context line; the same separator occurs 8 times in the file, and `git apply` anchors this hunk by its line number). There is NO leading context: the line above (`:139`, blank) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only, contains NO backslash (the existing cells use `\` continuations; this one does not — its `if` is ONE line) and no bash-4 idiom. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh` then `+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh`.**

```
@@ -140,1 +140,20 @@
+# ---------------------------------------------------------------------------
+# CELL 3b - KS-1137 F-2. The ESTATE's real digit-bearing image. dev-auth2 is a
+# synthetic name; the producible instance on this estate is
+# dev-m365-integration:latest (docker-compose.yml's m365-integration build:
+# service, the one of 33 that base scanned 0 times). Its digits sit MID-name,
+# so a class that admits only a trailing digit keeps CELL 1 green and still
+# skips it. Same stubs, same record: the image must be scanned exactly once
+# and the artefact must name it.
+# ---------------------------------------------------------------------------
+CORPUS_ESTATE='dev-m365-integration:latest
+dev-auth:latest
+postgres:15'
+build_fixture "$WORK/estate" "$CORPUS_ESTATE"
+rc_estate="$(run_job "$WORK/estate")"
+if [ "$rc_estate" = 0 ] && [ "$(scanned_times "$WORK/estate" dev-m365-integration:latest)" -eq 1 ] && [ "$(jq -r '.images[].image' "$WORK/estate/run/04-container-trivy.json" 2>/dev/null | grep -cx dev-m365-integration:latest)" = 1 ]; then
+  ok "KS-1137 F-2 - the estate's real digit-bearing image (dev-m365-integration:latest) IS scanned, once, and the artefact names it (rc=$rc_estate)"
+else
+  bad "KS-1137 F-2 - the estate's real digit-bearing image (dev-m365-integration:latest) is scanned" "rc=$rc_estate, scanned $(scanned_times "$WORK/estate" dev-m365-integration:latest) times of $(scanned_total "$WORK/estate") total, output: $(paste -sd ' ' "$WORK/estate/out.txt")"
+fi
 # ---------------------------------------------------------------------------
```

`build_fixture` (`:57-79`), `run_job` (`:83-88`), `scanned_times` (`:91`), `scanned_total` (`:92`), `ok` / `bad` (`:40-41`) and `$WORK` (`:36`, removed by the trap at `:37`) are the suite's own — you add NO helper. The corpus is a plain `'…'` literal spanning three lines exactly as `CORPUS_DEFAULT` (`:47-51`) is; the job's `sort -u` and the stub's record make the order irrelevant. `jq` is the one the suite already requires at `:33`; `grep -cx` prints its count and exits 1 on zero matches, which the `"$(...)" = 1` test absorbs (the same idiom as `:91`). `paste -sd ' '` joins the job's output lines for the FAIL detail without a backslash.

## Cells

- `estate` = `KS-1137 F-2 - the estate's real digit-bearing image (dev-m365-integration:latest)`

## Red cells

The cell below is a GENUINE assertion-red (a `FAIL` line the suite prints, tallied into its rc): it fails under each tamper and passes at the tip.

- KS-1137 F-2 - the estate's real digit-bearing image (dev-m365-integration:latest)

*(A bash cell is named by a LITERAL PREFIX of the description that ends at a word boundary: the prefix above is followed by a space on both the `ok` line (`… IS scanned, once, …`) and the `FAIL` line (`… is scanned`), and matches no other cell. The existing KS-867 cell is named the same way in the second tamper's `Reds` — its prefix `KS-867 — a digit-bearing dev image (dev-auth2:latest)` is the FILE's own text, em dash included; nothing this diff writes carries it.)*

## Tampers

Two single-line tampers on the SAME line of `04-container-trivy.sh` (`:62`, the corpus read; it occurs EXACTLY ONCE in the file — `grep -c -F -x`, 1; positive control `grep -c -i latest` over the same file: 3, `:5`, `:62` and `:78`). Each `From` is the tip's line at that number, byte for byte, each `To` is the same pipeline with ONLY the `grep -E` class changed, and each parses under `bash -n` (the checker's rule for a shell tamper), so the job runs and the difference is WHICH images reach trivy, never a load error. The checker plants them ONE AT A TIME and restores the file by bytes between them.

### TRAILINGDIGITONLY — the class admits a digit only at the END of the name: dev-auth2 still scanned, dev-m365-integration skipped
File: `Blockchain/Testing/jobs/04-container-trivy.sh`
Line: 62
From:
```
done < <(docker images --format '{{.Repository}}:{{.Tag}}' | grep -E '^dev-[A-Za-z0-9._-]+:latest$' | sort -u)
```
To:
```
done < <(docker images --format '{{.Repository}}:{{.Tag}}' | grep -E '^dev-[a-z-]+[0-9]?:latest$' | sort -u)
```
Reds: `estate`

### KS867REVERTED — the class is the pre-KS-867 `[a-z-]`, which admits no digit anywhere
File: `Blockchain/Testing/jobs/04-container-trivy.sh`
Line: 62
From:
```
done < <(docker images --format '{{.Repository}}:{{.Tag}}' | grep -E '^dev-[A-Za-z0-9._-]+:latest$' | sort -u)
```
To:
```
done < <(docker images --format '{{.Repository}}:{{.Tag}}' | grep -E '^dev-[a-z-]+:latest$' | sort -u)
```
Reds: `estate`, `KS-867 — a digit-bearing dev image (dev-auth2:latest)`

## Controls

- `CONTROL — postgres:15 and dev-old:v1 stay OUT`
- `CONTROL — with no dev-*:latest image the job still writes reason=no-images`
- `CONTROL — the job talks to the`

*(Prefixes of CELL 2, CELL 3 and CELL 4's descriptions, each matching exactly one cell on both its `ok` and `FAIL` spelling — CELL 4 prints `STUB` on `ok` and `stub` on `FAIL`, so its prefix stops before that word. All three are green under both tampers: CELL 2's four names are lowercase-only or non-dev and behave identically under `[A-Za-z0-9._-]`, `[a-z-][0-9]?` and `[a-z-]`; CELL 3's corpus has no `dev-*:latest` under any class; CELL 4 never reaches `:62` (docker `info` fails first). The KS-867 cell (CELL 1) is a declared RED of the second tamper and is green under the first, as measured below.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: `build_fixture "$WORK/estate"` copies the job, writes the three-line corpus, and writes the two stubs; `run_job` runs the job with `PATH="$root/bin:/usr/bin:/bin"`; `:20` finds the trivy stub, `:25` the docker stub's `info` (exit 0); `:62` reads the corpus through `grep -E '^dev-[A-Za-z0-9._-]+:latest$'` — `dev-m365-integration:latest` and `dev-auth:latest` pass, `postgres:15` does not — so `IMAGES` has 2 entries; the loop calls the trivy stub once per image (each appends its last argument to `trivy_scanned.txt` and prints `{}`), `:96` normalises `{}` to `counts: {}`, `vulns: []` (non-empty `norm`, `trc` 0 — KS-1274's own "bare `{}` reads clean" row, which is what makes the stub usable here), the artefact holds two `image` entries, `failed` is 0, the job exits 0. `scanned_times … dev-m365-integration:latest` is 1, `jq -r '.images[].image' | grep -cx dev-m365-integration:latest` is 1, `rc_estate` is 0 — the cell prints `ok`.

Under **TRAILINGDIGITONLY** `:62` admits `dev-auth:latest` (all lowercase) but not `dev-m365-integration:latest` (`3`, `6`, `5` sit before more letters, and `[a-z-]+[0-9]?` allows a digit only immediately before `:latest`): `IMAGES` has 1 entry, the estate image is scanned 0 times — the cell prints `FAIL` (`scanned 0 times of 1 total`). CELL 1 stays green: `dev-auth2:latest` ends in its digit, so it passes `[a-z-]+[0-9]?`, and the artefact still names 3 images. Under **KS867REVERTED** neither `dev-m365-integration:latest` nor `dev-auth2:latest` passes `[a-z-]+`: the new cell FAILs (0 of 1) and CELL 1 FAILs (`dev-auth2:latest scanned 0 times`, artefact 2 images) — both declared. Under BOTH, CELL 2, CELL 3 and CELL 4 stay `ok` (see Controls), and the suite exits 1 because `fail` is non-zero (`:158`) — an assertion red, not a diagnostic.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` line.** `04-container-trivy.sh` at `cbae988db`, line 62 is `done < <(docker images --format '{{.Repository}}:{{.Tag}}' | grep -E '^dev-[A-Za-z0-9._-]+:latest$' | sort -u)` (column 0), byte for byte; it occurs **exactly once** (`grep -c -F -x`, 1); the positive control `latest` (case-insensitive) matches 3 lines. `git blame` at the tip: `:62` last touched by `3fc158c39` (KS-878 + KS-867, 2026-09-13); the file's last change is `42afaa9e6` (KS-1136, #1051). The checker plants and restores it (T8 by sha256 after each; tip blob sha256 `0720a4bfa4a4e8d3`).
- **Premise: the ticket's claim, re-derived.** `docker-compose.yml` at the tip has **33** `build:` services (`grep -c`), none with an explicit `image:` under a `dev-` name (0), and the `m365-integration` service at `:852` builds from `services/m365-integration/Dockerfile` (`:857`) — compose's default image name for it is `dev-m365-integration:latest` (project `dev`, from the `Blockchain/Dev` directory), the name the ticket's gate measured. `dev-m365-integration` occurs **0** times in the suite at the tip (control `dev-auth2`: 6).
- **Premise: the anchor.** The suite is **159** lines; `:140` is the 77-character separator (`# ` + 75 `-`), the ONE trailing context line; it occurs 8 times in the file (`:94`, `:98`, `:109`, `:116`, `:125`, `:129`, `:140`, `:146`) and the hunk is anchored by its line number, as every bash hunk of this kind has been. `:139` (blank) is not written. The insertion is pure; no blank line anywhere in the fence.
- **Premise: the suite's contract.** Cells are printed by `ok` (`:40`, `  ok   <desc>`) and `bad` (`:41`, `  FAIL <desc>` + an indented detail line) at an indent of 2 — the checker's CELL shape; the tally at `:157-159` exits 1 on any FAIL. The suite refuses to run without `jq` on PATH (`:33`) and runs the job on `$root/bin:/usr/bin:/bin` (`:85`): on this platform `/usr/bin/jq` is 1.7.1, so both PATHs see it (F-4's host-shaped gap does not fire here).
- **Premise: `+` lines that also occur at the tip.** Three, all added by this brief (so T4 accepts them): the separator line (`:94` etc.), `else` and `fi` (every cell's). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted — `paste -sd ' '` replaces the suite's `tr '\n' ' '` idiom for that reason). **No non-ASCII** in any `+` line (0, counted — the cell text uses `-`, the file's own cells use `—`). No bash-4 idiom (no `mapfile`, `declare -A`, `${x,,}`, `|&`, `&>>`, `coproc`, `timeout`). The suite after the fence parses under `bash -n` (measured below).
- **Premise: the runner.** A `*.test.sh` suite selects runner `bash`; the clone is not node-farmed for it (`prepare_clone.sh` skips the farm). The checker runs `/bin/bash Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh` from the clone root; `REPO_ROOT` (`:24`) resolves to the clone root and `JOB` (`:30`) to the clone's `Blockchain/Testing/jobs/04-container-trivy.sh` — the tampered copy when a tamper is planted.
- **Premise: no live-lane collision.** `04-container-trivy.sh` is not `preflight.sh`, `index.ts`, `enforcement.ts` or under `services/anchoring/**`; the suite is none of Seat B 11th's six. The ONE held `READY_*` naming `04-container-trivy.sh` is `READY_KS-1136-item1` (a bash_patch) — merged as #1051 (`42afaa9e6` is IN this tip: the `:94` / `:114-117` / `:125-130` KS-1136 lines are the tip's), a spent hold. Briefs naming the file: `KS-1134.md`, `KS-1136.md`, `KS-1264.md` (mentions; KS-1134's READY modifies `aggregate_report_trivy_artefact.test.sh`, a different suite). No READY and no brief names `container_trivy_image_filter` except KS-1136's (a mention). See Collision.
- **Premise: the surface.** Two stubs on a private PATH, a temp dir the suite removes, no docker daemon, no trivy, no network, no product bytes. Not an auth surface.

## Collision

**No unmerged READY and no brief touches this suite** (`grep -il container_trivy_image_filter night/READY_* night/briefs/*.md`: 1 / 1, both KS-1136's, whose PR #1051 is in this tip), so no hunk overlap is possible. Product file `04-container-trivy.sh`: KS-1136-item1's hold is spent (merged); the open tickets KS-1273 (`--exit-code 0`) and KS-1274 (bare `{}` as scan-failed) name the file but have no brief and no READY — if KS-1274's fix lands first, the trivy stub's `{}` would read as `scan-failed` and EVERY cell of this suite (CELL 1 included) would need the stub updated; that is the suite owner's change, not this cell's, and it is not pending anywhere. Tamper line `:62` is shared with nobody. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clone at `cbae988db`, bash runner — no node farm; source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_round23-drafter-precheck/KS-1137/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md` = this brief's own hunk with the two file-header lines, fresh `--shared` clone `r23_clone_2` at `cbae988db`, runner bash, no farm): **RESULT: PASS (8/8)** — T1 one fenced block; T2 touched set == the suite only; T3 strict apply; T4 every `+` line byte-exact; T5 green at the tip **5 passed, 0 failed** (4 existing + the new cell); T6 TRAILINGDIGITONLY red set == {estate} (`FAIL KS-1137 F-2 …`, detail `scanned 0 times of 1 total`; `4 passed, 1 failed`) and KS867REVERTED red set == {estate, KS-867 cell} (`3 passed, 2 failed`), every red a `FAIL` line the suite printed, no bash diagnostic; T7 the three controls `ok` under both; T8 `04-container-trivy.sh` restored to sha256 `0720a4bfa4a4` after each (`KS-1137/out.md.checker/`). Source tracked-modified count 0 before and after (`KS-1137/prepare.log`).
- The applied suite parses under `bash -n` (rc 0) and is kept as `KS-1137/suite_with_cell.test.sh` (sha256 `991ca27811298d2c`). The two sibling trivy suites, untouched by this diff, run green on the same clone: `aggregate_report_trivy_artefact.test.sh` rc 0 and `container_trivy_failed_scan_is_loud.test.sh` rc 0 (`KS-1137/sibling_*.out`) — the whole-suite before/after for a bash cell is the suite itself: 4/4 at the bare tip, 5/5 with the cell.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh` / `+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh`, then the hunk above exactly as shown (`@@ -140,1 +140,20 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2 (a shell-suite cell, no product change). Refs KS-1137** (item 1 / F-2; and KS-867, whose class this cell proves on the estate's real name). **NEVER Closes** — KS-1137's item 2 (F-4, the `jq` PATH check at `:33`) is a suite edit for its owner and is not touched here.
- **Not from a gate cell.** Found by the 2026-09-21 board widening (round 23): the ticket names the cell shape itself ("feeds … at least `dev-m365-integration:latest` through the recording stub and asserts … scanned").
- **Not pinned here, said plainly:** the other 32 `build:` names (the ticket's "or" — a cell walking `docker-compose.yml` would need yaml parsing in bash 3.2 and is a bigger change); F-4; the KS-1273 / KS-1274 rows on the same job (product changes).
- **Instrument note:** the trivy stub prints `{}`, which the job reads as a clean scan today (KS-1274's open row). If KS-1274 lands, the suite's stub — every cell's, not just this one's — needs a `Results` array; recorded so the raise does not read a later red as this cell's.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1137 night/inputs/test_only_1137F2-ESTATEIMAGE-1.json night/briefs/KS-1137-F2-ESTATEIMAGE-1.md ctx=65536
```
