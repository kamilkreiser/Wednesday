STARTABLE: YES

# B1125 drafter report (kit B1125 / SEAT-M77, drafted 13:17 to 13:32 AEDT by `date`)

## BLUF
Kit `2026-11-02_B1125_SEAT-M77_mps-363-contract-copy-guard.md` (18,249 bytes by `wc -c`, 9 slot lines of four underscores by `grep -c`, 0 non-ASCII) builds the MPSCALC-363 CI guard: half 1 (byte equality of `docs/api/openapi.json` and the generated snapshot) unconditionally, half 2 (generator output equals the `schema.ts` body) only if the seat measures the pinned generator deterministic on Node 24 and equal to main's committed body; otherwise half 1 ships and half 2 is reported "NOT BUILT" with the `cmp` results (not a stop). Your cost call is quoted verbatim in the kit as the coordinator's. Sonnet C2, gate G2, pane `Datasec/MPS-M77`, branch `b1125/mps-363-contract-copy-guard`, test files only, no port block, no CI edit unless proved needed (then a STOP). Startable once stamped; no STOP found. Half 1 is green at main today.

## Facts re-measured (instrument, time)
- Main `7104179f3c7c9d1eb98b23ba7a3f7c1fe742e9e1` (`gh api -X GET git/ref/heads/main`, 13:17 and 13:31); open PRs #121, #120 (dependabot; each only `web/package-lock.json`, `pulls/<n>/files`); no `b1125*` ref (matching-refs 0); `.tools/b1125` absent. Tree not truncated, 755 lines; control `web/nonexistent.ts` not asked; `contract.sync` 0 hits and `contract.test.ts` 1 hit in the same list.
- **Byte equality at main (`cmp`, `shasum -a 256`):** `docs/api/openapi.json` and `web/src/api/generated/openapi.snapshot.json` identical, sha256 92f1c36333f0f00b371881f4c2f6e9c011bd27c836202e8627f6936cc22bb7be, 212029 bytes, 2270 lines; control: `cmp` of two one-byte files differing exits non-zero. `schema.ts` 3619 lines; line 1 to 3 header, line 4 `/**`. So half 1 is born green; the "copies of MPS #139 pass" clause holds for half 1.
- `contract.test.ts` 16 lines: `:8`, `:11`, `:13`, `:14` by `grep -n`. `sync-contract.mjs`: `:17-19` (blob read from a committed ref), `:24`, `:30`, `:31` (`npx openapi-typescript`), `:37` by `grep -n`. The script holds non-ASCII on 2 lines (byte scan); the `schema.ts` header shows an em dash and a middle dot. `web/package.json`: `:14` test, `:16` lint, `:17` typecheck, `:42` `openapi-typescript` 7.13.0.
- CI: `ci.yml:46` job name, `:58` `node-version: 24` (also `:107`, the package job), `:61` `npm ci`, `:62` `npm run lint`, `:63` `npm test`. A new test under `web/src/api/` is run by `:63`; no `.gitattributes` in the tree (0 hits), `tests/.editorconfig` only.
- **b1093** head `531c83beaeb0c42e6db4087c5aa61b9085e2cc41` (unchanged 13:31), ahead 4 behind 3, 14 files: `docs/API.md`, `docs/api/openapi.json`, `Program.cs`, four `Templates/*`, four `tests/*`, and the three generated files. At that head `docs/api/openapi.json` and the snapshot are byte-identical (sha256 82a33eb3063912e648fbac97fb3a4f004e62922533fcca6ec561342de2af134c); so it syncs the contract pair; half 2 on its `schema.ts` UNMEASURED. The guard goes red if b1093 lands unsynced: written in the kit.
- b1116 @ 574cd22e: 3 files, none of mine. M76 (kit B1117, 3 paths): none of mine; its text names `ci.yml` only as a CI predicate source (my program flagged it; read). Program (`python3 -I -B`) intersections of my 3 candidate paths with b1093, b1116, #120, #121, kits B1115, B1117, B1120: 0 hits; control `docs/IMPORTER.md` found in b1116. Only shared directory: `web/src/api/` (b1093 holds three generated files).
- Node 24: the MPS project has none; `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/.tools/node24/bin/node --version` v24.21.0; default Node here v26.8.1 (`command -v node`, `--version`). `ci.yml` pins the major only.
- Ports: `vite.hostguard.test.ts:19` `server.listen(0, ...)` (ephemeral); `lsof -nP -iTCP:9500-9999` listeners 9561, 9571, 9572 (HPSM seats); word-bounded scan over 125 non-`.pre-` SEAT kits names 9570, 9579 among many (control: names 9561, 9900). No block needed; 9580-9589 free by both instruments if wanted.
- Live panes (13:21): tuesday, HPSM-POC-H101, -G285, -H100, -G280, MPS-G284, -G283, -M76, fleet-monitor; no M77, no M74, no M75. `df -g` 36 GiB; load1 7.19 at 13:31.
- Jira (project helper `.tools/b562/jira.py jql`, parenthesised JQL): MPSCALC-363 exists and is not Done; `text ~ "openapi.snapshot"` neighbours 364, 316, 312, 290, 288, 236, 235, 234, 171, 45. The ticket's acceptance text is RELAYED from the sweep (the helper's `keys` mode writes into `.tools`, so I did not use it).
- Landing: `commits/7104179f` has 1 parent (squash). MPS `CLARIFICATIONS.md:722-731` record earlier squash landings; no written squash-or-merge rule line was read.

## Severity and REFUSE cross-checks (done)
- Every step 0 to 8 carries its failure class (STOP, FIX or REPORT): step 3 baseline red = REPORT if it passes alone, STOP if red alone; step 4 half 2 = REPORT not STOP; step 6 required red that stays green = STOP; step 7 and 8 FIX or STOP.
- Every REFUSE line run against what will be live at launch: stamp slots (pre-stamp reads 9; fires until stamped by design); `.tools/b1125`, `wt-b1125-*` absent (control `.tools/b1116`); `b1125*` ref 0 (control `heads/b1093` 1); `contract.sync.test.ts` on main 0 (control 1); main-moved grep over the files of `compare main...main` 0; no M77 pane; `df` 36 against 25; `gh auth status` kamilDatasec. None fires now. If b1093 lands before launch the main-moved line fires its re-measure branch, not a stop (b1093's head is equal on the pair).

## D-decisions made in the kit
- D-1 Property-first path set: `web/src/api/contract*.test.ts`, at least a NEW `contract.sync.test.ts` (existing `contract.test.ts` untouched). A CI edit is not needed because `ci.yml:63` runs every vitest file; if the seat proves otherwise it STOPs first.
- D-2 Half 2 gate: build only if three Node-24 runs of the pinned generator are byte-equal AND equal to the body of main's `schema.ts` (body = bytes after the third newline). Equal-but-different-from-main also means NOT BUILT (the committed file would need regenerating, outside the path set).
- D-3 Node 24 source: copy HPSM-POC's `.tools/node24` read-only into `.tools/b1125/node24` (version printed); if unusable, half 2 NOT BUILT.
- D-4 Half 2 test: pinned `node_modules/openapi-typescript` through `process.execPath`, output to the OS temp folder, explicit timeout (default 5 s fails under load: MPSCALC-369).
- D-5 Plants PA to PE: PA (one byte in `docs/api/openapi.json`) shows the old row stays green; PD (header line 2) is an equivalent that must stay green; PE (final newline removed) red.
- D-6 Commit subject may end `(MPSCALC-363)` as sibling MPS kits do; no person's name, card id or B-number anywhere.
- D-7 The b1093 reading (head sha, three copies synced, the guard's verdict on scratch copies) is REPORT only.

## Q-questions for Tuesday (each with a default)
- Q-1 May the seat copy HPSM-POC's Node 24 (cross-project read of a binary, write only under its own `.tools`)? Default: yes. Otherwise half 2 cannot be measured on Node 24 and ships NOT BUILT.
- Q-2 If half 2 turns out deterministic but unequal to main's committed body, accept "NOT BUILT, regenerate in a separate lane"? Default: yes.
- Q-3 Developers on other Node versions may see half 2 red if output differs (the generator uses the pinned `typescript`, so unlikely). Default: accept; the seat prints the default-Node result for information.
- Q-4 Gate round count printed as "round 1 of 2 on a new class, NO GO 0 before" (no earlier gate on this class). Default: as written.
- Q-5 Launch order: B1124 first, then this kit, one waiter at a time. Default: yes.

## Contradictions
- The sweep puts `ci.yml` in the path set "if needed" and names `contract.test.ts` as a path to edit; the kit makes the new file the home of both halves and leaves both `contract.test.ts` and `ci.yml` untouched (D-1).
- The sweep says a Node 24 install "is not assumed"; one exists in a sibling project (HPSM-POC `.tools/node24`, v24.21.0). The sweep's "STOP `NEEDS TUESDAY` on half 2" became "ship half 1, report half 2" per your instruction.
- The sweep says b1093 "does sync all three copies (its file list)"; measured: it changes all three paths and the contract pair is byte-equal at its head, but whether its `schema.ts` body is generator output is unmeasured.

## UNMEASURED
No npm, vitest, generator or plant was run. Not measured: generator determinism (run-to-run and against main's body, on Node 24 or 26); the time half 2 takes; whether `npx vitest` lists the new rows (follows from vitest defaults; the seat proves it); whether any dotnet test regenerates or compares `docs/api/openapi.json` (not read); the written squash-or-merge rule; whether CodeQL treats a test-only PR as quiet.

## Outside the fences
None. Read-only: `gh api -X GET` (refs, trees, contents at the pins, compare, pulls files, commits) under the MPS `.gh-config`; project Jira helper `.tools/b562/jira.py jql` with parenthesised JQL (prints keys only); `ls`, `lsof`, `tmux list-panes`, `df`, `uptime`, `node --version` (HPSM's and the default); one `git --no-optional-locks ls-remote` and one `git config --get core.sshCommand` read in the MPS repo. Scratch copies under the session scratchpad only. No decision_queue, Jira write, Azure, mail or message; no `cd`; no Artifact or Docs call.
