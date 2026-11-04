STARTABLE: NO until the squash lands (slots S4, S5, S12 are Tuesday's; TARGET does not exist yet); the kit itself is complete and has no open defect I know of.

**BLUF.** Kit B1290 (seat D52, UAT only, Opus) is 131 lines, built on B1283 (UAT lineage, `.tools/b1283/`, not the B1286 demo tree). Stamp has 13 slots + last line = 14 `____` lines (MEASURED `grep -c`). Slots S9/S13 carry decisions only Tuesday/the product owner can make: S13 (the printed-report palette, because `BrandTokens.cs` changes the PDF colours; B1280 FOR TUESDAY asked him, I did not find his answer) is a HOLD gate. Hard stop = earlier of Step 0 + 120 min and 06:15 AEDT; DONE by 06:45. Launch only after the landing and after B1289 reads GO/GO WITH FINDINGS.

## Facts re-measured (instrument; control)
- Clock at drafting: `date` read Thu 5 Nov 2026 00:27:57 to 00:33:57 AEDT.
- Range: `gh api -X GET compare fc2bc2fc...a7b82c27` (project GH_CONFIG_DIR): status ahead, ahead_by 10, behind 0, 10 commits, 118 files; files outside `web/`: exactly `api/src/HpsmPoc.Modules.Reporting/Pdf/BrandTokens.cs`; schema/infra/csproj/package/appsettings regex matches 0; +2072 -344; 37 test/spec/e2e + 81 non-test (80 web + BrandTokens). Control: the same jq instrument printed the one non-web path (it fires); the schema-regex 0 is a suspect until the seat's control (`a3a06b9a...69338b64`) fires; the kit orders it.
- Branch `b1272/hpsmpoc-visual-round-2` = `a7b82c27...` (git/ref); commit `a7b82c27` parent `9061c291...` (commits). Main = `fc2bc2fc` (branches/main, and `git ls-remote https://github.com/datasecau/HPSM-POC.git` read-only; the ssh form failed "Repository not found", https worked). Open PR for the branch: none listed (pulls?head= empty).
- PREV packages: `shasum -a 256` of `.tools/b1283/repo/out/deploy-packages/fc2bc2fc.../web/web.zip` = `8feea5b1...e7aa`, api.zip = `af8a43d1...7c55`; MANIFEST `commit` = fc2bc2fc for both; sizes 16,289,971 / 49,591,501; zip files 2115 / 121; RUN 41792358518; both digests equal the B1283 STATUS values. Control: web and api digests differ. The dir also holds a `live` subdir and no `rollback/` copy of PREV (B1283's `rollback/` holds the 77f56644 packages and two wwwroot BEFORE zips: the kit says they are NOT the way back).
- B1283 last line: `DEPLOYED: UAT @ fc2bc2fc (WEB + API)`, build `lTe-lsvVumX0lWioBKFc4`, deployments web `6031a7e1-724f-418a-9cab-8c7ffa0ee51e`, API `8475fc61-a609-46b7-b974-e3646dc609f9` (`B1283_STATUS.md:208`), deploy 08:13:25Z-08:15:30Z.
- B1280 pointers printed by `grep -n`/`sed -n`: Step 2 words `:43-49`, menu white 18 of 18 `:54`, toggle `:55`, ring/contrast `:56-57`, width 0.9300 in 84 `:69`, logo link `:99-102`, page-end max 48 / over 64 0 of 72 `:106`, header 72 in 24 and Menu 0 of 28 `:108`, Switch customer `:109`, account menu four items `:110`; round 1 first line `:1` = NO GO round 1 of 2. B1289 STATUS does not exist yet (`ls`).
- Ports: `lsof -nP -iTCP:9910-9919 -sTCP:LISTEN | wc -l` = 0; all-listener control 12; word-boundary scan `991[0-9]` over 125 non-`.pre-` SEAT kits of 3-5 Nov: 0 files; controls `990[0-9]` 14 files, `982[0-9]` 4 files (B1283 included). Panes (`tmux list-panes`): `%0 tuesday`, `%231 Datasec/HPSM-POC-G343`, `%1 fleet-monitor`.
- Model: `model-routing.md` line 96 (C6 Deploy, Opus 1st) and line 145 (Sonnet as deploy seat: no rows); `models_latest.json` line 17 `claude-opus-5-5`.

## D-decisions (mine; defaults apply if Tuesday is silent)
- D-8 widened: the census runs over all 80 product files + BrandTokens, and the check is SUBSET of the gate's closed list read by program from B1280 Step 2 and B1289 (I do not hard-code the strings; I did not see B1289's word section).
- D-13 rewritten for the gate's properties; B1283's hamburger names ("Collapse menu" exact) would FAIL on purpose now; the kit says so.
- D-14 (new): the logo link goes to the feedback review page; the kit reads href and name from the DOM and never clicks, and keeps B1283's no-feedback-content rule. D-11: the account menu is opened and read, no level item is clicked (they POST a sign-in).
- D-15 (new): no live PDF on UAT (reads a customer assessment); the assembly proof is by the 11 BrandTokens strings (UTF-16 bytes), with a heap-diff fallback if the lengths differ.
- D-12: "no shorter cell" is replaced by the gate's own facts (below 1024 head shorter by 32-52 px, Admin at 768 56; at 1024+ taller up to +44), each shorter cell must be explained.
- D-1 adds a tree-equality check of TARGET against the branch head `a7b82c27` (a head-pinned squash on an unmoved main must have the same tree).
- Clocks: 45-min Step-0 window (B1283: 60), CI wait capped by hard stop minus 40 min, a stated cut-down of the BEFORE walk if time is short.

## Q for Tuesday (with defaults)
- Q-1 The API restart for a minute or two (B1283's Q-1, accepted before). Default: accepted.
- Q-2 S13: has the product owner ruled that the printed report follows the new palette? I found no ruling in what I read. Default: kit stays HOLD-capable; write HOLD if not ruled (nothing deploys).
- Q-3 Port block 9910-9919 is my pick (Tuesday assigned none). Default: accepted.
- Q-4 If the squash lands later than about 05:00 the CI wait + 35 min of checks cannot fit before the 06:15 write cut-off. Default: seat ends `STOPPED: NEEDS TUESDAY not enough time` with UAT untouched.
- Q-5 Launch line uses `launch_when_cool.sh` as B1283/B1286/B1289 did, not the `cockpit.sh add` form in DRAFTER_RULES. Default: as written.

## UNMEASURED
Everything hosted (no az, no HTTP). B1289's closed list and verdict (not written). Whether the 11 BrandTokens strings are equal length. Whether the gate's page-end cells exist on UAT (B1283 said not). Whether `.tools/b1280/g/*.cjs` and `ring1280.cjs` files named in BUILD 6 all exist (I listed `g/` and `ring/` partly; `ring1280.cjs` was cited by B1280 STATUS but not listed by me). Whether `shellprobe1283.cjs` can be reworked within the time. Mock rows: whether they show on UAT at all (they live in the prototype/mock mode per the spec file name; not checked).

## Outside the fences
None intended. One slip: my first compound command typed `cd /dev/null` and the hook refused it before it ran (nothing executed). Used `gh api -X GET` only; one `git ls-remote` over https (a read verb) after the ssh form failed. Scratch file `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/607a25a6-4816-4b85-a174-fe1225050fde/scratchpad/files.txt` (file list only). I read `B1289_SEAT-G343..pre-stamp` and its slots for the stamp shape only.
