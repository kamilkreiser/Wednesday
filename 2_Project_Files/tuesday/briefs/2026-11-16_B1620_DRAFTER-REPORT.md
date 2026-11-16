STARTABLE: YES (after Tuesday's stamp; four questions, each with a default that lets it start)

# B1620 drafter report: HPSM-POC lane H-3, owner cut at whole characters (HPSMPOC-470 point 3), seat H175

Drafted 2026-11-16 from 15:44 to 15:51 AEDT (`date` printed 15:44:23, 15:44:45, 15:45:18, 15:46:47, 15:49:28, 15:50:29, 15:50:35).
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1620_SEAT-H175_hpsmpoc-lane-h3-owner-cut-whole-characters.md` (297 lines).
- Sidecar: `...owner-cut-whole-characters.md.measured` (105 lines: 68 stamp_check claims plus S01-S37). `stamp_check.py <kit>` exits 0 (run unpiped, `rc=0`; "68 claims, 68 measured, 0 not measured").
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s283/b1620/` (Jira GET read `jira470.txt`, raw files at main, `probe*.mjs`, `owners.mjs`, `mk_sidecar.py`).
- Template: B1616 (H-4 web lane, read whole with its sidecar and the B1615 report) for shape, toolchain by path and G3 proofs; B1615 for the red-first and landing sections.

## BLUF
- **The bug is real and measured.** `startingOwner` (`web/src/components/customer/remediation-store.ts:56-66`) walks code points (`:61`). Run under the project's node `v24.21.0`, the base loop cuts a joined family after 97 letters to a result ending in a dangling joiner (U+200D), a 95-letter version to a different, shorter family, drops a skin tone, leaves half a flag, strips a keycap's enclosing mark and drops an accent. A grapheme walk (`Intl.Segmenter`, `"grapheme"`) gives the whole-character cut in all 9 probe rows, and the same result for locales `undefined`, `en`, `tr`, `th`.
- **The build** is one function and its doc comment, plus 10 added test rows inside the existing `startingOwner` block (0 removed lines). The code walks segments when `Intl.Segmenter` is a function and the base code-point walk otherwise (the code is `"use client"`, so it runs in customer browsers). Rows 1-6 and 8 are red at base by assertion; rows 7 and 9 are green by construction and are proven by mutants (5 listed; mutant 5, granularity `"word"`, is killed only by the keycap and accent rows: measured).
- **No shipped value reaches the cut:** 12 `owner` strings in `web/src` JSON, longest 21 units, 0 over 100. So the lane changes no shipped content; it fixes a latent defect for loaded or live values. No words, no migration, nothing deploys.
- **Held keys:** the pickup and the last two daily notes hold no DROPPED or HELD line for 470 point 3. Hits are records mentions only: B1571 landed point 1 (#319, pickup and 11-15 note), B1605 ended point 4 NO-BUILD, and the 11-16 notes list H-3 as the sweep's lane. The ticket stays open for points 2 and 5 ("Not decided"); the kit says the lane does not close it.
- **Partition:** owns `remediation-store.ts` (lines 53-66) and its test (added rows only). Open PR #326 (H-4) names only the Reporting README and `stamped-set.test.ts`; H-1 owns two api files. No shared path, no port. Sonnet (row C2, `model-routing.md:92`), tier G3 as commissioned (`:110`).

## Facts re-measured with instruments
- **Main** `678a1153d28be006a088a3b1fba8f5aab52e8d0e` at 15:44 (`gh api -X GET branches/main`). **Open PRs: 1** (#326, `b1616/hpsmpoc-stale-statements`; `pulls/326/files` lists exactly the README and `stamped-set.test.ts`). `pulls/99999` HTTP 404; `pulls?state=open` HTTP 200. `matching-refs/heads/b1620` length 0 (control `heads/b1599` length 1).
- **Pointers** (printed by `awk NR==n` over raw files at main): `remediation-store.ts:18`, `:45`, `:53-55`, `:56-66`; `remediation-store.test.ts:454-492`, `:455-456`, `:487-491`; `RoadmapScreen.tsx:72`, `:99`, `:130`; `ci.yml:384`, `:396`, `:409`, `:413`, `:478`; `package.json:10-12`; `vitest.config.mts:10-13`; `tsconfig.json:4`. All in the sidecar (S01-S37).
- **Newest commit on both owned files** `c014503d` (2026-11-11, "Register: start an over-long default owner at the field's limit"), by `gh api commits?path=` (the H-1 clone is depth 1, so `git log` there is not a history).
- **Probes** (node `v24.21.0` from `HPSM-POC/.tools/node24/bin`): old and new results for nine inputs (`probe2.mjs`), granularity `word` and the `>=` mutant (`probe3.mjs`), the `Intl.Segmenter` stub-and-restore form (`typeof` printed `undefined`, then `function`).
- **No test row reads a joiner, modifier, flag, keycap, accent or multi-code-point cluster today**; the 7 existing `it(` rows are at `:459 :463 :469 :473 :479 :483 :487`. `/usr/bin/grep -rn -F 'Segmenter'` over `web/src` is 0 (control: `startingOwner` over the same tree is 14).
- **Shipped data scan** (`owners.mjs`, control: it counted 12 owners): see BLUF.

## D-decisions (the drafter's)
- **D1 Grapheme clusters, not an emoji-range regex.** `Intl.Segmenter` is in node 24 and in the project's `lib` (`esnext`); an emoji regex would go stale at each Unicode release and is a refused shape.
- **D2 Fixed locale `"en"`** for determinism; the result was identical for four locales (S14), so this is not a behaviour choice.
- **D3 Keep the code-point walk as the fallback** when `Intl.Segmenter` is not a function (the code runs in browsers; Firefox before 125 lacks it). Row 9 stubs the segmenter and pins the base result. The stub's restore is `finally`; vitest's `restoreMocks` does not undo a hand-replaced property, so row 1 asserts `typeof Intl.Segmenter` is `"function"` first.
- **D4 A first cluster longer than 100 units gives `""`** rather than a split cluster (Q-2). `checkEntry` bounds only the length (`:45`), so an empty start is accepted.
- **D5 Test rows are added inside the existing block, existing rows byte-identical**, so the check is "0 removed lines" by `--numstat`.
- **D6 Red-first is by assertion for rows 1-6 and 8; rows 7 and 9 are green at base** and have named mutants (`>=`, no-guard) as their control.
- **D7 Sequences are written as `\u{...}` escapes only**, because `infra/tests/test_hidden_characters.py` walks every tracked file (DRAFTER_RULES fence 8) and a literal joiner or variation selector is what it hunts.
- **D8 Build and lint run at head** (`npm run build` once), because `web build` runs it and `check-client-bundle.mjs` reads the client bundle; the e2e shards are not run (no browser, no port).
- **D9 Sonnet writes the whole function from a stated property, not a pasted body** (the kit gives the rule and the shape, not the code), so the seat's own typecheck decides the exact types.

## Q-questions for Tuesday (each with a default)
- **Q-1 Scope of the ticket after landing.** The kit says the lane does not close HPSMPOC-470 (points 2 and 5 are "Not decided"). **Default: records seat comments point 3 built and leaves the ticket open.**
- **Q-2 A single cluster longer than the limit** (a letter plus 150 combining marks). **Default: the start is empty** (never split a cluster), pinned by row 8. Alternative: fall back to the code-point cut for that case only (adds a branch and a row; keeps today's output).
- **Q-3 Keep the no-`Intl.Segmenter` fallback?** **Default: keep it and test it (row 9).** Alternative: assume the browser has it and drop row 9 and the guard (smaller code; throws on an old browser, which is the customer's tab).
- **Q-4 Gate tier.** The commission says G3 ("no gate"). This is product code behaviour, with 5 mutants and red-first rows as the safety net, but no second reader. **Default: G3 as commissioned.** Alternative: G2 on Sonnet (a pure function, mechanism measured here), which costs one more kit.

## Step input table (MEASURED LITERALS rule 4)

| Step | Inputs | Produced by |
|---|---|---|
| 0 | stamped kit, deploy key, project git config, node 24 at `.tools/node24` | exists at BASE / Tuesday's stamp |
| 1 | origin reads, the clone | Step 0 |
| 2 | `probe-cut.mjs` (written in Step 2), node 24 | Step 0 (node); Step 2 writes the script |
| 3 | clone with `npm ci`, `base-unit.json` path | Step 0 (`npm ci` at item 7) |
| 4(a) | the clone, the test rows (D2) | Step 3 (base runs) |
| 4(b) | the red tree | 4(a) |
| 4(d) | scratch copy of the fixed tree | 4(b) |
| 5 | the Step-4 diff, name lists | Step 4; project files at BASE |
| 6 | `base-unit.json`, `npm ci` | Steps 3 and 0 |
| 7 | Steps 2-6 green | Steps 2-6 |
| 8 | the diffs, mutant table, pushed sha | Steps 2-7 |

## UNMEASURED
- Whether `tsc` accepts `Intl.Segmenter` under the project's `lib` and TypeScript `^5` (kit: Step 6 typecheck decides; `lib` is not the seat's to change).
- Whether lint (`--max-warnings=0`, flat config) refuses any shape in the new code or rows; no lint run.
- The base totals of vitest and of the `startingOwner` block (the kit says 7 `it(` rows from the line scan; the seat prints the run total).
- Whether `npm run build` runs on this machine without network (kit allows "not run at base" with the error printed).
- Whether CI's `setup-node` 24 and the local `v24.21.0` carry the same ICU for the chosen sequences; the sequences are old (Unicode 8-11 era) and the result was identical across four locales, but no CI run was made.
- Whether any live or loaded `owner` value is over 100 units.
- The e2e shards: none names `startingOwner` (0 lines), ten files name the roadmap; none was run.

## Outside-the-fences disclosure
- **Reads outside the two files.** `gh api -X GET` under the project's `GH_CONFIG_DIR` (branch, pulls, pulls/326/files, matching-refs, commits by path, raw contents of the two owned files, `package.json`, `tsconfig.json`); a GET-only Jira read of HPSMPOC-470 through my own copy of `jdesc.py` (copied from the H-1 drafter's scratch, no token printed); the H-1 drafter's depth-1 clone under `fleet/state/s282/r1615/repo` (read only, no git write; used for `RoadmapScreen.tsx`, `vitest.config.mts`, `web/e2e`, `web/scripts`); B1615, B1616 kits and sidecars and the B1615 report; the commission and the sweep; the pickup and the two daily notes by `grep -n`; `model-routing.md`, `models_latest.json` and `brief_seat.sh` by `awk NR==n`.
- **Run.** Node probes (`probe.mjs`, `probe2.mjs`, `probe3.mjs`, `owners.mjs`) with the project's `.tools/node24` binary; `node -I -e 1` once to confirm that option is refused (the kit says not to write it).
- **Not run.** No build, no lint, no vitest, no npm, no docker, no `az`, no mail, no board, no `decision_queue.sh`, no Artifact, no `_ledger.md`, no WEDNESDAY or FRIDAY tree, no `cd`, no fetch/clone/ref write in any project repo.
- **Not written.** Only the kit, its sidecar, this report and my scratch folder. One in-place edit by `sed -i ''` of my own sidecar to correct clocks (a drafter file, not a seat's).

DRAFTED B1620: kit 297 lines, sidecar rc 0, questions 4
