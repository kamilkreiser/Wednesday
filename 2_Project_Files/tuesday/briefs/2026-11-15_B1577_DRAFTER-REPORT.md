STARTABLE: YES (after Tuesday's stamp; six questions, each with a default that lets it start; Q-1 and Q-3 change what ships to the client tester, read them first)

# B1577 drafter report: HPSM-POC builder, HPSMPOC-168 (the product owner's 2026-11-15 ruling, option a), seat H166

Drafted 2026-11-15 14:37 to 14:53 AEDT (`date` printed 14:37:30, 14:37:57, 14:42:01, 14:45:42, 14:47:16, 14:52:36). Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1577_SEAT-H166_hpsmpoc-168-industry-choice.md` (82 lines), sidecar `...industry-choice.md.measured` (70 claims plus S01-S03, S06, S07, S21, S30-S32), work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1577/`.

## BLUF
- **The field.** The Profile step's "Assessment context" draws its inputs from the ruleset named by the snapshot set of the Playbook screens' package (`profile-values.ts:18` -> `registry.ts:76`, package 0.7.0 -> ruleset `snapshot-policy-aligned@0.1.2`), where `P-industry` is `"type": "text"`. The card text agrees: changing it "needs a new question-set version". Versioned content files are never edited (each package's canonical hash is its stamp), so the build is **ruleset 0.1.3 + package 0.7.1**. They are made by program from 0.1.2 and 0.7.0. The only changes are the version strings, the snapshot set's ruleset link, and `P-industry` becoming single-choice with the four labels. The drafter prototyped both files: 23 and 25 diff lines, and the four hashes are written into the kit for the seat to match.
- **It is a pin chain, not a one-file change.** It follows the house pattern of `6185fed5` (ruleset 0.1.2 + package 0.6.1, 63 files):
  - the web loads the new files (registry, ruleset list, client copies);
  - `playbookPackage` and `snapshotStartPackage` move to 0.7.1, while `readinessPackage` stays on 0.7.0;
  - the showcase seed's `SnapshotPackageVersion` moves to 0.7.1;
  - the hosted demo's one scorable draft moves to 0.1.3 in all three places `test_hosted_demo_pin.py` ties together (Bicep, the infra baseline, the API test factory). That makes it a **G1 gate**: it changes what the client tester sees and a deploy setting, although nothing is deployed.
- **Census by program (the commission's ask).** It covers 315 rows in 82 files for `0.1.2` / `0.6.1` / `0.7.0` / `P-industry` outside the versioned-content folders. Two further patterns: the field fetched as a textbox (14 lines in 2 files) and the shipped-count pins (`7` packages ×2, `17 client copies` ×1). Each row is classified as REWRITE or UNAFFECTED by a stated property (table below). The kit adds a **dynamic census**: the seat runs every suite after the product files and before any test edit, and every red must map to a REWRITE row or the seat stops. This applies the ledger's 2026-11-15 B1555 rule.
- **Two things the build cannot avoid changing, which need Tuesday's eyes (Q-1, Q-3):**
  - The four showcase samples store a free-text industry in `P-industry`, which 0.1.3 refuses. They need a mapping: Government -> Public sector, Manufacturing and Logistics -> Other.
  - Free-text industries already stored on hosted profiles show no choice, and are cleared on the next Save. In-progress 0.6.1 snapshots stop scoring on a hosted demo that names 0.1.3 (the B97 precedent did the same).
- **Held:** the ticket's fleet-size note (its words are not written yet) and its "with provenance C-34" line (a provenance text would be a new word). Nothing deployed, no HP-tool integration.
- Base `8766b253bb11e9ef23978abc6741e1c6146e74c4` (#318 landed), 0 open PRs. Seat H166 (the highest earlier `SEAT-H` is 165), pane `Datasec/HPSM-POC-H166`, branch `b1577/hpsmpoc-168-industry-choice`. Ports 9920-9929: WEB 9922, hosted 9923, stub 9924, chooser 9925, SQL Server 9920, Azurite 9921. Model Sonnet (`model-routing.md:92` C2), gate G1 (`:108`), id `claude-sonnet-5-5` (`models_latest.json:23`).

## Facts re-measured with instruments
- Card: `decision_queue.sh show hpsmpoc-168-industry-list-1115` into `card.txt` (10 lines; the id appears 1 time): status ruled, `choice='a'`, `ruled_ts=2026-11-15T13:49:37`. The option a text equals the commission's quote.
- Ticket: `jget.py HPSMPOC-168` (GET only; the token is read in-process and never printed) gave the description plus comment 41027. The 2026-11-11 acceptance covers the choice list AND the neutral fleet note. The comment says the note's "own words are not written yet; they come to the product owner before they ship". Held-label JQL: COUNT 0; the control without the key: 27. `text ~ "industry"` JQL: COUNT 9.
- Main: `gh api branches/main` gave `8766b253...` at 14:37 (2026-11-15T02:14:47Z). `pulls?state=open` gave 0. Control: `state=all&per_page=3` gave 318, 317, 316 (all closed). `pulls/99999` returned 404. `matching-refs/heads/b1577` returned 0; control `heads/b1541` returned 1. **`heads/b1571` returned 0: H165 has not pushed yet.**
- JSON recipe: `json.dumps(indent=2, ensure_ascii=False)+"\n"` reproduces 0.7.0 and 0.1.2 byte for byte (round-trip True for both). The Python canonical recipe reproduces the registry hash for 0.7.0 (`a6476338647056f7cd75...`) and the PROVENANCE value for 0.1.2 (`11275e43e272...`). The web source and the API seed are `cmp`-identical for both.
- Prototype (scratch only, `proto/`): 0.1.3 has file sha256 `9bbe9b7d...`, canonical `sha256:4035158720cd...`. 0.7.1 has file sha256 `030df89f...`, canonical `sha256:0f179147c495...` (full values in the kit). `"type": "text"` occurs once in each source, so the transform touches exactly one field per file.
- Ports: `lsof -nP -iTCP:9920-9929 -sTCP:LISTEN` gave 0; the unfiltered list gave 18. Scan of the 22 non-`.pre-` SEAT kits of 14-15 Nov for `992[0-9]`: 0 each. Control: `989[0-9]` over the B1571 kit gave 2. Panes at 14:42: `%0 tuesday`, `%39 Datasec/MPS-M138`, `%36 Datasec/HPSM-POC-H165`, `%31 Datasec/MPS-M139`, `%22 Datasec/NexusAI-N130`, `%1 fleet-monitor`, plus unnamed panes. Load 10.20.
- CI pointers at 8766b253 (S21) are the same lines as in the B1565 kit: 87, 184, 252, 255, 303, 314, 396, 409, 413, 426, 478, 494, 518, 630. `global.json` pins 10.0.404 with rollForward disable. `.nvmrc` reads 24.
- Template drift found: **`brief_seat.sh`'s default-Opus line is now line 31, not 24.** Line 24 is now a KDATE check. The kit cites 31 (S32).
- CodeQL suites exist at `javascript-queries/2.5.0` and `csharp-queries/1.11.0` (`ls`).
- Version-bump precedents: `a4ff52da` (38 files), `6185fed5` (63), `fa401da9` (48), counted by `--jq '.files|length'`.

## Census by program (frame: every file of the 8766b253 tarball except `web/src/content/{client,packages,rulesets}/` and `api/src/HpsmPoc.Api/SeedContent/`)
Program `scripts/census.py` produced 315 rows in 82 files: R012 76, P061 95, P070 107, FIELD 37. Rows are in `census_rows.tsv`. Hand patterns: `textbox[^)]*Ind|industryField` gave 14 lines in 2 files (control: the `group ... Organisation` row reads 1); count pins: 3 lines.

**Property:**
- REWRITE when the line asserts or sets which package or ruleset is CURRENT (screens, new snapshot, hosted demo, seed), a shipped count or list, or the field's text shape.
- UNAFFECTED when the line is history, a fixture stamp of an existing snapshot, readiness, a 0.1.0 package or `snapshot-placeholder@0.1.0` source, a test of a version's own files (they stay shipped), or a contract/OpenAPI version string.

| file | verdict | why |
|---|---|---|
| `web/src/content/registry.ts` | REWRITE (product) | imports, RAW_PACKAGES, PACKAGE_HASHES, playbook/snapshot-start pins (`:76`, `:80`); readiness `:84` stays |
| `web/src/lib/ruleset.ts` | REWRITE (product) | import of 0.1.3 into RULESETS (`:10`, `:22-25`) |
| `web/scripts/client-content.mjs` | REWRITE (tooling) | SOURCES + 2 (`:19`, `:23` rows are the neighbours) |
| `web/src/content/PROVENANCE.md` | REWRITE (doc) | two new rows |
| `ShowcaseSeeder.cs` | REWRITE (product) | `:90` -> 0.7.1; `:205` free text -> option id (Q-1); `:85` stays |
| `infra/modules/appservice.bicep:141`, `test_security_baseline.py:278`, `HostedDemoTests.cs:31` | REWRITE | the hosted pin trio |
| `HostedDemoTests.cs` (other rows `:184`, `:341`, `:373`, `:599`), `HostedDemoSeedRulesetTests.cs` (`:35`, `:40-41`, `:129`) | REWRITE | name 0.1.2 as the scorable draft |
| `Content061ApiTests.cs` (`:16`, `:58` rows) | REWRITE | "the hosted demo names 0.1.2 now" turns false; mirror into a 0.7.1 file |
| `ProvenanceViewTests.cs` (`:56`, `:116`, `:196`) | REWRITE | the demo's scoring ruleset |
| `ShowcaseSeedDraftContentTests.cs` (`:118`, `:124`) | REWRITE | P-industry equals the overview's free text |
| `ContentCatalogTests.cs:101`, `ReadinessContentTests.cs:21` | REWRITE | `7` shipped packages -> 8 |
| `profile-values.test.ts:23-25` | REWRITE | rulesetVersion 0.1.2 and `["P-industry","text"]` |
| `ApiProfile.test.tsx` (6 textbox rows) | REWRITE | the field is a radio group now |
| `web/e2e/playbook-profile-fields.spec.ts` (8 rows) | REWRITE | the same, end to end (playbook shards) |
| `client-content.test.ts:37`, `:68` | REWRITE | 17 -> 19 copies; ruleset key list |
| `content.test.ts:88`, `:114`; `deck-v3.test.ts:53-54`; `content-050.test.ts:52-55`; `content-060.test.ts:66-67`; `content-061.test.ts:44-46`; `content-070.test.ts:115-119`; `audiences.test.ts:27`; `SnapshotLauncher.b56.test.tsx:22` | REWRITE | package lists and playbook/snapshot-start version asserts |
| `HostedDemo.cs:35`, `infra/README.md:123`, `web/e2e/playbook.ts:11` | REWRITE (comment) | present-tense statement of the current version |
| `InternalNotesScanTests.cs` | UNAFFECTED | `Scored()` derives package and ruleset from the two pins by program (read at `:38-51`) |
| `ProfileApiTests.cs`, `PersonalDataTests.cs`, `ContractTests.cs`, `ProfileValidatorTests.cs`, `ContentPackageLoaderTests.cs`, `customer-profile.test.ts` | UNAFFECTED | sources are package 0.1.0 (`Journey.cs:26-27`, `Seed.cs:13`) or `snapshot-placeholder@0.1.0` (`customer-profile.test.ts:14`) |
| `Content061Tests.cs`, `Content070Tests.cs`, `content-061/070` other rows | UNAFFECTED | tests of those versions' own files, which stay |
| Golden scenarios (3 `expected.hand.json`, README, `DemoScenarioTests.cs`, both csproj links), `B112R009RefusalEvidenceTests.cs` | UNAFFECTED | they score 0.1.2's file; 0.1.3's rules are identical (the seat's deep-diff test proves it) |
| readiness files (`readiness-stamp.test.tsx` 17 rows, `AssessmentsHub*`, `ReadinessRunner/Result.tsx`, `parts.tsx`, `readiness.ts`, `types.ts:153`, `FirmwareTask.tsx`, `playbook-readiness.spec.ts`, layout extract) | UNAFFECTED | readiness stays on 0.7.0 (D-3) |
| `playbook-feedback-b241.spec.ts:100`, `playbook-read-retry.spec.ts:19`, `SnapshotLauncher.alias.test.tsx:17`, `SnapshotLauncher.b97.test.tsx:17`, `playbook.test.tsx:84` | UNAFFECTED | fixture stamps or history of existing snapshots |
| `playbook-content-050-live-api.spec.ts` | UNAFFECTED, NOT RUN | live-API only (`e2e.mjs:103-107` LIVE_API_ORDER), in no CI shard |
| contract/OpenAPI files, `schema.gen.ts`, three `ruleset.schema.json` copies, `TestContentAmbiguous`, `seat-a` testdata, `ProfileContextFields.tsx:3` (comment says "still placeholder", still true) | UNAFFECTED | version strings of the API contract, descriptions or own fixtures |

The seat re-runs this at its base and reconciles it against the dynamic census (Step 4). A verdict here is the drafter's reading of each line's context, not a run.

## Chain table (rule 4)
| step | inputs | produced by |
|---|---|---|
| 0 | kit, project identity, dotnet 10.0.404, node 24, docker, pinned MSSQL image | exist at BASE / on the box (the seat checks; the drafter checked none of the toolchain: no clone) |
| 1 | `mut`, gh | step 0 |
| 2 | `mut` with npm ci, dotnet restore; writes `base-unit.json`, `base.trx`, `census.tsv` | step 0 |
| 3 | `head`; 0.1.2 and 0.7.0 sources (BASE); Q-answers (stamp) | steps 0, stamp |
| 4 | `head` product files and a build | step 3 (build listed inside step 4 before the Playwright run) |
| 5 | REWRITE list (steps 2 and 4), `mut` for red-at-BASE runs | steps 2, 4 |
| 6 | `head` complete; `base-unit.json`; containers (started in 6d) | steps 2, 5 |
| 6e | CodeQL CLI and suites (on the box), the diff | step 5 |
| 7 | all green | steps 4-6e |
| 8 | pushed sha, census files | steps 2, 4, 7 |

## D-decisions (made in the kit, each reversible by Tuesday at the stamp)
- D-1 New versions, never edits. Ruleset 0.1.3 and package 0.7.1 are made by program, with a no-edit round-trip control and a deep-diff property check. Label, help, required and provenance of `P-industry` are unchanged (no new word).
- D-2 Option ids are `industry-healthcare`, `industry-financial-services`, `industry-public-sector`, `industry-other`, prefixed like `P-size`'s `size-1`. They are not shown to users: labels are.
- D-3 `readinessPackage` and the seed's `ReadinessPackageVersion` stay on 0.7.0. This mirrors how 0.7.0 kept snapshots on 0.6.1, and no readiness stamp moves.
- D-4 No web code change. The radio group and option-id save already exist (`ProfileContextFields.tsx:57`, `profile-values.ts:47`). Existing data effects are measured and pinned by tests, not "fixed" with new words.
- D-5 All eight e2e shards run at head, because the change moves the package every Playbook screen reads. The full API suite and both SQL Server parts run as well, as does infra.
- D-6 Added code comments may cite `HPSMPOC-168` (the house provenance style). The commit message carries no ticket key; no brief number, seat, coordinator or person anywhere.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q-1 Showcase samples' industry.** The seed writes the sample's own industry as free text into `P-industry` (`ShowcaseSeeder.cs:205`), which 0.1.3 refuses.
  - Default (a): Healthcare -> Healthcare; Government -> Public sector (the code already reads the HP meeting's "public sector" as Government, `industries.ts:6-7`); Manufacturing and Logistics & warehousing -> Other. An unknown industry throws at seed time. This keeps HPSMPOC-184 (samples' Profile step not empty) true.
  - (b): record it only where the industry exactly matches a choice label (only Healthcare); the other three samples show "Not recorded".
- **Q-2 The package-level `P-industry` in 0.7.1.** Default yes: it gets the same four choices, so the one field never has two shapes in one package. No: only the ruleset's field changes. The screen reads the ruleset's field either way.
- **Q-3 Existing data, as deploy notes.**
  - A free-text industry already stored on a hosted profile renders with no choice selected, and the next Save of the Profile step clears it.
  - In-progress snapshots started on 0.6.1 are no longer scored on a hosted demo that names 0.1.3. The B97 precedent refused 0.6.0 the same way.
  - Default: accept both, pin both with tests, and state both in the PR body. Nothing is deployed by this kit. The deploy (and whether the hosted seed re-seeds) is a later card.
- **Q-4 Builder model.** Row C2 says Sonnet, and the gate is G1 (Opus). The build is about 40 files across C#, TS, JSON and infra, on the 63-file precedent's pattern. Default: Sonnet as written. Raise to Opus if Tuesday weighs the size and the hosted pin over the table.
- **Q-5 Held items.** The fleet-size neutral note (no words yet) and the ticket's "with provenance C-34" acceptance line (a provenance `sourceRef` text is shown in the provenance view, so it would be a new word). Default: both held, named in the PR body. The records seat B1575 owns the ticket comment.
- **Q-6 Window and hard stop.** The READY target is 360 minutes after Step 0. The work includes eight e2e shards, two SQL Server parts and two CodeQL databases, with four seats live (load 10.2). Default: one window as written, with the context band and handover form included.

## UNMEASURED
- Everything the seat runs. The drafter ran no build, no test, no browser, no container and no CodeQL. In particular:
  - the red set of Step 4: the census predicts it, nothing has run it;
  - whether `test_hosted_demo_pin.py` stays green when all three pins move together;
  - the client-copy count line after the change (DERIVED 19);
  - the report's label rendering for an option id (DERIVED from `RulesetLookup.cs:94-95`).
- The verdicts in the census table are context readings of each line, not runs.
- The landing-rule quote (CLARIFICATIONS.md line 3617) and the hosted CodeQL languages are RELAYED from the H-2 kit and drafter.
- Whether H165 (B1571) pushes or lands during the work: it shares no path. A MOVED MAIN covers it.

## Outside-the-fences disclosure
Reads:
- `DRAFTER_RULES.md`, the commission file, the B1571 kit (`.pre-stamp`) and drafter report, the B1565 kit (grep for its API/SQL Server method), and the ledger row for B1555 in `_ledger_laptop_datasec.md` (by grep, as the commission names it).
- `model-routing.md`, `models_latest.json`, `brief_seat.sh` (grep of its level lines).
- The one card, by `decision_queue.sh show <exact id>` into a scratch file.
- HPSMPOC-168 and three JQL searches, via my own GET-only copies of the B1571 drafter's `jget.py` and `jsearch.py` (credentials read in-process from the project `.env`, never printed).
- `gh api -X GET` under the project's `GH_CONFIG_DIR`: main branch, pulls, matching-refs, the branch list, three commits' file lists, commits for three paths, and the tarball of 8766b253.

Local runs, in my work folder only: tarball extraction; the census program; the JSON round-trip and hash checks; the prototype writer (`proto/`, two files never placed in any repo); `lsof`, `tmux list-panes`, `uptime`.

Writes, besides those scratch files: only the kit, its sidecar (by `stamp_check.py --init`, then filled by my script) and this report.

Nothing else was touched: no `decision_queue.sh list`, no Jira write, no git or GitHub write, no file under `/Volumes/Datasec_DEV/!CODING/`, no message, no tmux send-keys, no az, no docker, nothing deployed, no `_ledger.md`, no WEDNESDAY, FRIDAY or non-Datasec tree.

DRAFTED B1577: kit 82 lines, sidecar rc 0, questions 6
