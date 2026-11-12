STARTABLE: NO (by design: S4 `DEPLOY SHA` cannot exist until the messaging squash lands; then YES once the 17 slots are filled and Q-1 and Q-2 are answered)

# B1540 DRAFTER REPORT (kit: `2026-11-12_B1540_SEAT-D61_hpsmpoc-uat-deploy-messaging.md`, 446 lines, 17 stamp slots)
Drafter, s272, 13:09-13:25 AEDT 2026-11-12 (clocks by `date`). Work folder `fleet/state/s272/d1540/` (raw JSON, the downloaded API artifact, the deploy script copy).

## BLUF
- The kit is a CODE-ONLY UAT deploy of main at the landed messaging sha. It is built on B1466's shape (identity pass, REFUSE list, closed-list proof, words gate, BEFORE/deploy/AFTER walks, STATUS forms, way back stub-run) with the database half removed on a measurement: **no migration is in the range** and the API package's `assessment.sql`/`feedback.sql` equal what UAT runs.
- **Last UAT deploy per the records: B1466, `009421a2`, 2026-11-10 22:07-22:09 AEDT** (`B1466_STATUS.md:271`). Nothing deployed to UAT since (deploy-STATUS listing: B1391, B1454, B1460, B1466; B1490 only deleted the copy database).
- **Main since then: 5 commits, linear, 28 files, +696/-36** (#310, #311, #309, #312, #313), none on UAT. Their only customer-visible text is one walkthrough step title. They ride with the messaging deploy; **that needs a ruling (Q-2)**.
- **The records still say "UAT is held"** after B1466 (analysis `CLARIFICATIONS.md` C-363 `:6254`, C-365 `:6275`, C-366 `:6285`, written today). The kit treats the product owner's 10:51 and 11:21:32 words as the deploy word for this change and makes the hold-lift a slot (S13) instead of an inference (Q-1).
- The grant row for push-READY (`EXPIRING-GRANTS.md:23`) excludes "new customer-facing words". The two messages carry the words; the kit says so plainly.
- Expected range at Step 0: 6 commits / 50 paths (7 / 52 with the minimatch commit); the seat refuses if main is not exactly S4.

## Facts re-measured (instrument; control)
| Fact | Value | Instrument | Control |
|---|---|---|---|
| main now | `c717ba1a945191ffa31f13320c19967a6cf7f15a` (13:10:02) | `gh api -X GET branches/main` | open PRs 0 (`pulls?state=open`); `pulls/99999` 404 |
| range PREV..main | ahead 5 behind 0, 5 commits, 1 parent each, 28 files +696/-36 | `compare 009421a2...main`, python over JSON | tree compare: 28 blob paths differ = 28 files |
| PR numbers | 310, 311, 309, 312, 313 (heads `15be8814`, `a2461ce7`, `0ccb1ec1`, `43a06592`, `b6ab804a`) | `commits/<sha>/pulls` | each merge sha equals the commit |
| gate lines | all five `GO WITH FINDINGS`; Majors 0 in all (Minor rows 4, 3, 5, 3, 4) | `head -n 1` of the five VERDICT files; `grep -i -c` of `\| id \| Major` | Minor rows counted beside; row count `^\| ` printed |
| schema in range | 0 paths match `Migrations\|Persistence\|\.sql$`; 109 schema-regex blob paths identical PREV vs main | contents list + `git/trees?recursive=1` (truncated false both, 1524 vs 1528 blobs) | planted `Migrations/X.cs` reads 1; planted blob makes the sets unequal |
| API package at `c717ba1a` | 122 = 122 files; `assessment.sql` `03f1afb3...` and `feedback.sql` `2a587ac2...` = PREV's; 14 files differ: 5 HpsmPoc DLL + 5 PDB + 2 Pkcs DLL + `HpsmPoc.Api` (app host) + `HpsmPoc.Api.deps.json` (6 hunks: Pkcs 10.0.14 to 10.0.15 only) | downloaded `deploy-api-c717ba1a...` (artifact 13848431501, GET), python zipfile/sha256 against `.tools/b1466/target/api/api.zip` | the two SQL digests printed equal to B1466's; difflib hunk count printed |
| deploy tooling | `deploy-from-ci.sh` `0024302d1ea35f`, `deploy-package.py` `77dc49939859ab`, `ci.yml` `06402836c6cfa7`: identical at `009421a2` and `c717ba1a`; script lines `:25 :49 :68 :69 :89` printed | `contents?ref=` blob shas; `awk NR==n` over the raw script | both shas printed side by side |
| CI at `c717ba1a` | `ci` 43003397930 success; CodeQL 43003397326 success; 22 check-runs (21 success, 1 skipped = dependency review); open alerts 0 | `commits/<sha>/check-runs`, `actions/runs?head_sha=`, `code-scanning/alerts` | `state=fixed` reads 1 |
| PREV's packages | web 9d6bb36c...19f 16,558,555 B; api 1fd65b62...f9ec 49,644,626 B; RUN 42773429652 in `.tools/b1466/target/`; artifacts `expired=false`, expire 2026-11-17T07:24:32Z / 07:26:23Z | `shasum -a 256`, `stat`, `actions/runs/42773429652/artifacts` | digests equal the B1466 STATUS lines |
| messaging branch | `9308afa0...`, 3 commits, ahead 3 behind 0 of main, 24 files +199/-151; 0 schema/deploy paths | `compare main...b1535%2F...` | schema regex 0, control 1 |
| overlap | messaging files overlap the 28 on `steps.ts`, `steps.test.ts` only; union 50 (+2 = 52 with minimatch) | python set arithmetic over the two compare JSONs | sizes 28, 24 printed |
| minimatch branch | `b1538/hpsmpoc-minimatch-alert-9` does NOT exist on origin yet (404) | `branches/...` | the b1535 branch of the same query returns a sha |
| ports | `lsof` 9900-9999 LISTEN 0 rows (13:13); kits of 11-11/11-12 hit 9900-9959 only; proposed 9960-9969 | `lsof -nP -iTCP:9900-9999 -sTCP:LISTEN`; `grep -o -E '\b99[0-9]{2}...'` over SEAT kits | all listeners 18 |
| panes | `%0 tuesday`, `%168 Datasec/HPSM-POC-H161`, `%153 Datasec/MPS-M129`, `%1 fleet-monitor` + 5 unnamed | `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` | names print |
| instruments | 17 `.tools/b1466` files with sha256 prefixes and line counts in the kit; `walk1466.cjs` and `cmpwalk1466.py` DIFFER from the digests B1466's STATUS printed | `shasum -a 256`, `wc -l` | seat must `cmp`/record what it got |
| stamp slots | 17 lines contain `____` (17 occurrences) | `grep -c`, `grep -o -E '_{4}' | wc -l` | after-edit recount printed 17 / 17 |
| names | 0 person names in the kit (Kam, Kamil, Kreiser, Friday, Wednesday, Steve, Peter, Stuart, Paul); no card id | python regex `(?<![A-Za-z])<name>(?![a-z])` | `_by_Kam_` fires 1 |

## Words in the five earlier landings (reading all 28 patches)
One customer-visible text change: step `offers` title "Service offers: ..." to "Delivery phases: Assess / Implement / Optimize" (#309, cites the product owner's 2026-11-11 ruling). Everything else is layout classes, a `main` landmark move (PlaybookShell), an accessible region name, a tap height, the register's starting-owner cut (logic), a Pkcs pin (csproj) and an exact SDK pin (global.json). The kit's words list therefore is: the 52 frozen rows (`.tools/b1535/frozen.jsonl`) plus this title.

## HOLDS FOUND (the product owner's words do not obviously cover; all in the kit under H-1 to H-6)
1. UAT hold C-300 "ends on the product owner's word and on nothing else" (`CLARIFICATIONS.md:5655`), and every entry written after B1466 still ends "UAT is held" (`:6254`, `:6275`, `:6285`). C-366 itself (`:6280`) calls the 11:21 words "an instruction to deploy on the map ... it decides none of the map's held questions".
2. `EXPIRING-GRANTS.md:23`: the push-READY grant says NOT "new customer-facing words". `EXPIRING-GRANTS.md:15`: the 11-06/08 UAT-hold row ("ends on his word, not by inference").
3. The five earlier landings were merged "main only; UAT held" and have never been seen on UAT.
4. Project `CLAUDE.md`: no UAT hold (UAT 0, deploy 0; control Coordinator 1).
5. HP review in session: UNMEASURED.

## D-decisions (drafter's; the kit's defaults)
- D-1 pin: refuse if main != S4 at Step 0 (no "deploy S4 anyway" before Step 0), list every commit by program.
- D-2 single write class: the project script's two deploy lines (plus the way back).
- D-3 no API stop and no migration; D-4 temporary access NONE (proof: firewall list and 0 `firewallRules` rows, no `sqlcmd` in the tree).
- D-5 database stays awake, read by ARM GET only. D-7 way back is code only (B1466's COPY rollback is retired by B1490).
- D-8 words closed list = frozen.jsonl + the step title, and the substitution is applied (old absent, new present). D-9 held/next-phase items absent, as a closed check list with controls. D-12: page text AFTER = BEFORE with frozen substitutions applied, residue 0.
- Backup form (S14): `CODE BACKUP AND RESTORE POINT READ; NO DATABASE COPY`.
- Model: Opus (`model-routing.md:96`, row C6 "Deploy", Opus column "1st"); `claude-opus-5-5` (`models_latest.json:17`/`:37`); `BRIEF_SEAT_LEVEL=opus` is written inside the launch line.
- Clock: 120 min to the write cut-off (the work has no migration), 150 to DONE; a context band and handover form are in.

## Q-questions for Tuesday (each with a default)
- **Q-1 (S13):** are the product owner's 10:51 and 11:21:32 words read as lifting the UAT hold for THIS deploy only, even though the records (C-363, C-365, C-366) and grant row :15 still say held, and grant row :23 excludes new words? Default: YES, for this deploy only (as B1466 read his "go ahead and deploy to UAT").
- **Q-2 (S16):** do the same words cover the five earlier landings (#309-#313) riding this deploy? Default: YES; the words list sent beside the deploy names the step title. If NO, there is no sha on main that excludes them: the kit cannot be used.
- **Q-3:** #309 and #312 landed on heads that differ from their gated heads (`0ccb1ec1` vs `4f084fb`; `43a06592` vs `40217c1`); the compares read ahead 4/5 because the heads were rebased. Do you hold a re-gate or rebase-only note? Default: no note; the seat proves product patches equal PR-diff against PR-diff and STOPS on any product-path difference.
- **Q-4 (S14):** want a database copy as in B1466? Default: NO (no schema change, no data change, the copy cost billed storage and was deleted); the restore point T0 and the platform window are read and recorded.
- **Q-5:** the messaging branch has no gate yet (the builder says READY at `9308afa0`). The kit needs a gate line at the landed head in S6. Default: no stamp until that gate reads GO or GO WITH FINDINGS.
- **Q-6 (S10 (d)):** accept both apps restarting (web then API, a few minutes in all) with NEW API code, with the HP-review question unmeasurable? Default: accept (B1466 accepted a stop of 3 min 45 s).
- **Q-7 (S11):** words beside the deploy or before it? Default: SENT BESIDE THE DEPLOY. Note for his list: nine D rows ship in qualified form (P4, W5, W6, W8-W10, W17, R1, P6); R1/R3 and several B rows are new sentences he has not read in this form; P6 keeps "SIEM integration if available" on the page with the planned line (map question 11 default).
- **Q-8:** if the minimatch commit lands first, should the deploy wait for it? Default: do not wait; it is lockfile-only and the kit proves it dev-only if present, so either order is handled by S4.
- **Q-9:** ports 9960-9969 OK? Default: yes (free at 13:13, no kit hit).

## UNMEASURED (nobody has run it)
Whether UAT still runs `009421a2` and BUILD_ID `NQga609FQ4iKZFwQ1rtsT`; whether the sign-in screen (S1-S3) is reachable on UAT (the UAT start page replaces it; the kit says "not shown on UAT" if no route reaches it); whether R2's tiers sentence renders on UAT's sample result; the messaging squash sha, its CI and its gate; the web package at any sha (only the API package was downloaded); the minimatch commit; whether #309/#312's product patches are equal across the rebase; HP reviewer presence; any Azure fact (every Azure line in the kit is RELAYED from B1466/B1490 with its line).

## Outside-the-fences disclosure
- Read-only GitHub GETs only (branches, compares, trees, contents, commit/PR lists, check-runs, runs, artifacts list, code-scanning alerts) under the project `GH_CONFIG_DIR`, on `datasecau/HPSM-POC` and one raw read of `datasecau/HPSM-POC-analysis` `1_Project_Definition/CLARIFICATIONS.md`. I downloaded ONE CI artifact (`deploy-api-c717ba1a...`, 49.7 MB) to the work folder to measure the API package; no hosted host, no az, no ssh, no docker, no Jira, no card read (no `decision_queue.sh`).
- `gh auth status` was run once (prints the account and a masked token prefix, no secret).
- Read-only on this volume: `.tools/b1466` (ls, shasum, wc; target zips), `.tools/b1535` (ls; `frozen.jsonl` parsed), project `Briefs/` STATUS files, the project `CLAUDE.md`, `EXPIRING-GRANTS.md`, `model-routing.md`, `models_latest.json`, the messaging map, the B1535/B1538/B1539 kits and STATUS, the five gate VERDICT files. No `fleet/briefs_staged`, no scoreboard, no `_ledger.md`, no non-Datasec tree.
- `lsof` and `tmux list-panes` for the ports/panes lines. I created the work folder and the two kit files only.
- Slips: two Bash calls were refused by hooks (an `echo ======` and a `set -- $pair`, then a `cd /tmp` attempt); nothing ran from them. I did not re-read the whole D58 kit (636 lines): I read B1466's kit and STATUS whole and B1460's STATUS BLUF/NOT TESTED/FOR TUESDAY/Corrections plus its D-12/D-13/D-17 text; the seat is told to read both kits whole.
- One counted difference to be aware of: `DRAFTER_RULES.md` names `/Volumes/Laptop-DEV/...` paths; I used the `/Volumes/Datasec_DEV/...` paths from the commission.
