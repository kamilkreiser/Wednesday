STARTABLE: YES - the kit for lane M-4 (B1876, seat M172, MPSCALC-420 and MPSCALC-417) is written, its sidecar is complete (`stamp_check.py` exits 0), no path to a customer was found for either document, and every sentence the seat will write was prototyped on copies and hashed; the seat is not startable until Tuesday stamps the ten slots.

# DRAFTER REPORT B1876 (lane M-4) - drafted 2026-11-21 23:09 to 23:25 AEDT (clocks by `date`) by a read-only drafter for Tuesday

## BLUF
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1876_SEAT-M172_mps-docs-x39-and-runbook-words.md` (55802 bytes), sidecar `...md.measured` (124 lines, 76 measured, 48 "unmeasured by design" command or word literals), this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s307/d1876/` (tarball of main, prototype copies, probes, `facts.txt`, `claims.txt`, `prototype_checks.out`, the Jira GET-only helper).
- Base: code main `28d8d31b73c6475b33921c679499b0777fdf0448` (read 23:09:15 and again 23:22:25 AEDT, equal), 0 open pull requests, `matching-refs/heads/b1876` 0 rows (control `heads/b1790` 1 row). Both blobs the lane writes equal the sweep's: `docs/ENGINE.md` `3b5ffc81...`, `infra/README.md` `55171ec9...`.
- Customer reach: none found (table below). Tuesday's C-109 reading (developer-only) is supported; the kit still STOPs the seat if its own re-run finds a path.
- The edit is small and fully frozen in the kit: ENGINE.md one clause of line 166 (1 line changed), README.md 16 lines added and none changed. Applied byte for byte the blobs are `5539adca563c8880bddb2ecdad8234c8d9233012` (ENGINE.md) and `99eedfba00450e73d96b35e5ada54c116cd2f58d` (README.md): the seat's blobs must equal these.
- Reading load: 92512 bytes in all (breakdown below); aim under 300 kB met; the kit itself is under the 80 kB bar.

## The files and the form
Form: B1791's kit (read whole in pages), its `.pre-stamp` Stamp section and the first lines of its sidecar. Same shape (STATUS channel, marks, REFUSE AT ONCE, THE WORK, PRIOR WORK, lane partition, HOLDS, Questions with defaults, ten stamp slots as four underscores, launch line with `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, last line `READ-WHOLE-BY-TUESDAY: ____`; slot-line count by `grep -c -F` = 10). READY is a pushed branch `b1876/mps-docs-420-417`, no PR. Model row C2 (`model-routing.md:92`), model id from `models_latest.json:23`, gate tier G2 (`model-routing.md:109`).

## The customer-reach measurement (commission: grep the web build, the API, the infra templates and the packaging)
| Probe (frame: 244 files of src, infra without its README, web without tests, package and deploy scripts, ci.yml) | Result (MEASURED at main, `reach_probe.py`, python -I) |
|---|---|
| `ENGINE.md` | 9 lines: 6 comment lines, 3 non-comment, all in `web/src/api/generated/openapi.snapshot.json` (contract description strings); that JSON is imported only by 2 test files; not a read of the file |
| `infra/README` | 4 lines, all comments (including the bicepparam header, `validate.sh:4`, `ci.yml:3`, and a comment naming another project's README); 0 other |
| controls: `wwwroot`, `index.html` (files the build does ship and serve) | 11 comment + 28 other; 2 comment + 9 other: the probe finds shipped paths |
| what ships | `package.sh` = `dotnet publish` of the Api + `web/dist/**`; the Api serves only `ContentRoot/wwwroot` (`HostedWeb.cs:101,105,106`); 0 lines for MapOpenApi/AddOpenApi/Swagger (control: UseStaticFiles/MapFallback 2 lines); csproj items reaching outside the project 0 (control: 3 ProjectReference); vite config `publicDir`/glob/`?raw`/alias to docs 0 (control: 26 lines with build/server/plugins); `web/public` holds only `proposal/`; the repository is private |
Limits said plainly: source text only; no web bundle was built and no published zip opened (UNMEASURED); a comment line is judged by its first characters.

## Questions for Tuesday (each with the default the kit assumes; none blocks the start)
- Q1 clause boundary (420): default replace `Engine only: the contract and the screens do not carry it`, keep `(the web table, T-V5-7)`. Alternative: replace the parenthetical too.
- Q2 budget sentence (417): default hedged (what the template does; first create "not measured"; move to a `yyyy-MM-01` date only "if a first create is refused"). The ticket's rule is "relayed from memory of the API reference"; the drafter would not write it as fact.
- Q3 step 2 (417): default mark steps 2 and 3 as the record of the first deploy and name the export for an existing site. The ticket's alternative (add the export to step 2) cannot work for a new site: the ids come from step 5 (`README:56-62`).
- Q4 what-if list (417): default the ticket's items only; `sku.tier` NoEffect (record `B1755_STATUS.md:110`) left out because the ticket does not name it.
- Q5 step 6 (417): `README:63-64` stays byte-equal (ticket acceptance) and the new list says "count changes net of them". Its words "expected: Modify of the site's `appsettings` only" are contradicted by what the 2026-11-20 what-if showed (7 changes, 3 Modify) unless read net of the list. Alternative: change those words (breaks the insertions-only property of the README diff).
- Q6 gate G2 (Tuesday may lower to code-only). Q7 one commit, both tickets. Q8 branch `b1876/mps-docs-420-417`, subject ending `(MPSCALC-420, MPSCALC-417)` (subject length by program: 108). Q9 level sonnet (C2). Q10 the seat prints every count.
D-decisions (all Tuesday's as coordinator, each sourced in the kit): D1 C-109 reading with the reach measurement; D2 pure insertions for the README (so "no other byte changes" is checkable by blob reconstruction); D3 hedge every hosted fact as "read on 2026-11-20"; D4 the ENGINE.md `old_string` is the 57-character clause only (the words `Engine only` occur on 7 lines of the file).

## The census of what pins the old behaviour (by program)
- `docs/ENGINE.md`: 0 tests or scripts open it (all other `ENGINE.md` mentions are comments, doc strings, or contract descriptions); no docs lint or link check (markdownlint/lychee/remark/mdl/cspell/CODEOWNERS 0; control `tests/.editorconfig` 1). The old phrase is on exactly 1 line of docs, src, tests, web, .github (`docs/ENGINE.md:166`).
- `infra/README.md`: 1 reader, `infra/tests/test_validate_script.py:111-114` (`assertNotIn("az bicep", ...)`, 6 tests by the indented pattern, column-1 pattern 0); `test_infra.py` mentions README 0 times (control `bicep` 45). The prototype holds `az bicep` 0 times (control `az deployment` 1 at base). No test pins the old claim that the contract or screens do not carry the projection (0).

## Corrections to the commission and to the sweep's row
- Sweep: the blob `34ebbeda` for `infra/tests/test_infra.py` (read at debb5e28) is stale: main `28d8d31b` holds `c0e6a2720e3e64aeb879d55c178b9715ff4cb20b` (the B1791 change has landed, 43 tests by that kit's count). It is not this lane's file, but it changes the CI python loop's `Ran N` for `test_infra.py`; the kit says to print it, not to expect 35. The two blobs this lane writes are unchanged since debb5e28.
- Sweep M-4 row lists `infra/README.md (46, 49 to 51, 63)`: those are the statements the ticket names and they stay byte-equal; the insertions land after lines 32 and 48.
- Sweep says 417's budget sentence "rests on the budget service's published rule (relayed, not fetched)": confirmed; the kit does not state it as fact.
- Commission: no error found in the main sha, the C-109 line number (2716, quote confirmed) or the lane table.
- 417 ticket: "add the export of the two ids to step 2" is unworkable for the case step 2 documents (ids exist only after step 5); 417's acceptance that line 63 "still reads true" is in tension with the new list (Q5).
- Outside the lane, noted in the kit for FOR TUESDAY: `infra/scripts/validate.sh:4` says the what-if is README step 3; it is step 2.
- `infra/README.md:3-4` already holds a tenant id and a subscription id (existing text, not changed, not a secret); the kit forbids the seat to add any id, site name or host.

## Chain-step inputs (each produced by an earlier step or present at base)
| Step | Inputs | Where they come from |
|---|---|---|
| 0 | the kit, `.tools/.git-lock` | the stamped kit; the lock dir is made in Step 1 |
| 1 | S2, project repo identity, deploy key | stamp slot S2; `config --local` of the project repo; `3_Access_Keys/github_deploy_rw` (present, 2 files match the name) |
| 2 | the clone at base | Step 1 |
| 3 | Step 2's counts | Step 2 |
| 4 | the clone; the probe text | Step 1; embedded in the kit (the drafter ran the same text, `reach_probe.py`) |
| 5 | the clone's code lines | Step 1 |
| 6 | frozen text; anchors | the kit; anchors measured once at base (ENGINE old clause 1; README anchors 1 each) |
| 7 | the edited files, the base blobs, the prototype blobs | Step 6; FACT 2; the kit |
| 8, 9 | Step 7's green checks; the ssh key | Steps 6-7; FACT 6 |

## The checks of the kit that the seat runs: run once on the drafter's PROTOTYPE (`proto/prototype_checks.out`), each with its control
- (b) ENGINE.md: only line 166 differs, by the clause: PASS; control (a second changed line): FIRED.
- (c) README.md: 16 added, 0 removed: PASS; removing the added lines reproduces blob `55171ec94dbf77ae6b70cd1409ebbfc0e266d007`: True; control (one existing line edited): removed count 1, FIRED.
- (d) old phrase 0 in the prototype (1 at base); `az bicep` 0 (control `az deployment` 1).
- (e) added text non-ASCII lines 0; control planted U+200B: 1.
- (f) GUID, `microsoftonline`, `app-mpscalc`, `u6agl3` over the added lines 0 each; controls fire (sidecar).
- (g) underscore-aware name scan, 12 names, 0 hits; control `_by_<name>_` fires for all 12.
- The git-based checks (`git diff --numstat`, `--name-only`, `git log` identity), gitleaks and the CI python loop were NOT run (no git write was allowed and the drafter ran no test): marked in the kit as the seat's checks with planted controls.

## UNMEASURED (named so nobody reads them as measured)
- Every `Ran N tests` total (6 for `test_validate_script.py`; the 15-file loop) and every rc of the CI python loop at base and head.
- What the hosted what-if showed on 2026-11-20 and that an update with the same past budget start was accepted (RELAYED from the deploy record `B1755_STATUS.md:104,112,113,122`; no hosted read was allowed).
- Whether the budget service accepts a past start on a FIRST create.
- Any inspection of a built web bundle or the published package (the reach probe reads source).
- The words status of the projection table (`ProjectionTable.tsx:8-19` WORDS-PENDING); the kit says only what main's code does.
- The Edit-tool mechanics on the real clone (anchors measured on the tarball copy; the seat's clone will differ only if main moved).
- Disk free, pane list and load at the stamp (read at 23:13:31; panes re-read at the end: 3 panes, no `Datasec/MPS-`).

## Reading load of the seat, by program (bytes)
kit 55802 + `infra/README.md` 9213 + ENGINE.md line 166 2474 + main.bicep 20-41 1131 + showcase.bicep 41-53 and 104-117 1373 + bicepparam 728 + test_validate_script 105-118 554 + API.md 604-617 1320 + PurchaseMapping.cs 262-280 and 321-343 2281 + PurchaseResultView.tsx 199-203 377 + ProjectionTable.tsx 2933 + the deploy record's five lines 3185 + the gate standard's line 31 3038 + the project CLAUDE.md 8103 = **92512**. (Sidecar 13649 bytes, not read by the seat. Tuesday's own stamped kits are on no READ list.)

## Outside the fences, disclosed
Read-only reads beyond the form kit and the sweep: the project's `CLAUDE.md`; `CLARIFICATIONS.md` line 2716 region (C-109) and a count of C-188/C-189; the deploy record `1_Project_Definition/Briefs/2026-11-19_B1755_STATUS.md` (greps and lines 104-122, 183, 212-219; the ticket names it as the thing to read each word against). Those lines hold a site name and ids: the site name `app-mpscalc-showcase-u6agl3...` and a masked GUID scan reached my terminal output once, and were written into no file (the sidecar and kit carry only the dated facts and the prefix `u6agl3` as a scan pattern). I listed the `Briefs/` folder names (ls | grep) and the `.tools` folder names (counts only). `evidence/05a_whatif.txt` was listed, not opened. Jira: GET of MPSCALC-420, 417 and 361 (control) with my own helper (credentials in-process, never printed). `gh api -X GET` only (commits, pulls 174/219/220, matching-refs, tarball). `tmux list-panes`, `git hash-object`, `git config --local --get` (lengths only). No git write; no network call but `gh` and Jira; nothing outside the scratch folder, the kit, its sidecar and this report was written. Not read: `Source_Documents/`, `.local/`, HPSM-POC or any other client, `fleet/briefs_staged/`, the scoreboard, the ledger, any decision card, M-2's files (`d1875/`, the B1875 kit), the B1790 kit, `docs/ENGINE.md` beyond line 166 and greps.
