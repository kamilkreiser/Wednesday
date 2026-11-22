STARTABLE: YES

# B1948 DRAFTER REPORT: Security Composer lane CW-2 (PCOMP-36, PCOMP-37), seat SEAT-C107

Drafter: Opus (in-session, read-only), on commission `2026-11-23_B1948_COMPOSER-CW2_DRAFTER_COMMISSION.md` (read whole) and `DRAFTER_RULES.md` (read whole). Clock from `date`: 03:20:34 AEDT at the first instrument, 03:41:44 at the last. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1948_SEAT-C107_composer-cw2-baselines.md` (sidecar `.measured`: 90 claims, 90 measured; `stamp_check.py <kit>` exit 0). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s313/d1948/`.

## BLUF
1. **Startable.** Base is code main `3638da61` (PR 85 landed; 0 open PRs); `content/baselines/` is absent there (0 of 1060 tree paths; control `content/release-demo` 5), settling the sweep's UNMEASURED note. Seat id `SEAT-C107` is free (0 file names in either briefs folder; control `SEAT-C106` 3 and 1).
2. **PCOMP-36's "target value per field" is met for 4 fields, not 34.** 34 of the bundle's 351 fields are typed boolean, but a value follows from the template's class without reading a sentence on only 4 (the item's own switch on an enforce or disable row: M001 false, M030 true, M083 false, M098 true). 16 typed fields sit on variable rows (`"variable"`), and 14 are sub-fields whose value would need a reading of the template's target sentences (null, `typed_not_switch`). The plan's and sweep's "34 typed fields meet it" overstated it.
3. **PCOMP-37's 28 holds by program:** template `variable` true on 28 rows, exactly CONDITIONAL 25 + MANUAL 3. **No content links any Composer question (D-001 to D-026) to any item** (0 non-null `show_when`/`required_when`/`applicable_when`, 0 `UQ-` ids in the discovery text), so every one of the 28 gets the control decision of its item's control as its setter (C-54 kept: never a questionnaire key).
4. **Three existing tests will read the new files** (fence 8): `fixture-fence.test.ts` walks all of `content/`, `b330-sm316-qgate.test.ts` scans every `packages/*/test` file (the new test), and `prettier --check .` covers `content/baselines/` (not in `.prettierignore`). The kit has the seat run the whole workspace project.
5. **Prettier rejects a `json.dumps(indent=2)` file**, measured on the prototype, so the kit adds a `prettier --write` step and a `json.loads` equality. My first prettier run passed everything, including two planted bad files. It had read nothing, because prettier honours the ignore files of the working directory. The re-run with `--ignore-path /dev/null` fired the controls. The kit warns about this.
6. **Remediation:** 33 rows carry states the engine lacks ("After validation" 20, "Controlled / staged" 13; PCOMP-42 is held), so they get null plus a flag and never a new state word. 21 rows read "Enable" with the non-automatic label: the kit maps them to `on` and keeps `remediation_automatic` false. This is a slot (REMEDIATION-ENABLE), Q-2.

## Facts re-measured (instrument, value, control)
- Code main `3638da611ce8483628b03b2550367b6eb15aa69c` (`gh api -X GET branches/main`), tree `e9ded89d…` equal to B1803's head `2a58dc5d` tree (so B1803's base and head counts apply, RELAYED). Check runs on main: 4 success. Open code-scanning alerts 0. Ruleset: CodeQL, required checks `[]`.
- Release files at main: release-demo CONTENT_HASH `5db37614…` (blob `23cd95f5`), release-draft `5679855b…` (blob `09d597c6`). The kit's CK10 holds both unchanged. DRAFTER_RULES line 99's "05070f1d at main" is history: main now carries `5db37614`.
- Bundle (python): 137 items, 351 fields (34 boolean), 132 controls, 26 discovery questions, `baseline_values` 0.
- 0025 enums: severity low/medium/high, remediation on/off/manual_approval, unsupported ignore/fail.
- Template (root main `53b286cd`, sha256 `a43f5c51…`) and crosswalk (sha256 `d3434b54…`): enumeration counts in kit FACT 8. The template's sentence columns were read by program only and never printed.
- No reader: `git grep` over tree `e9ded89d` for `content/baselines|"baselines"|baselines/` found 0 files (exit 1); control `content/release-draft` 34 files.
- Join: control id alone over-assigns shared controls, and SM key alone pulls in the six shared sub-items. Their intersection (rule J) gives 130 rows with items, no item on two rows except M007 and M008 (resolved by J-H1), and 7 items on no row. These equal the crosswalk's 7 unattached map entries.
- Prototype checks run once on `proto_fmt.json` (`chk.py`): no-whitespace 0 (control 1); no-copy line/window 0/0 (controls (1,148), (0,6), (1,9); 437 sensitive strings, 3 catalogue id strings excluded per C-154 (3)); names, card ids and ruled/ruling 0 (control 1; 6 name tokens, never printed); fixture ids 0 (control 1); q-gate patterns 0 (control 1); keys and enums 0 (mutants ≥1); ASCII 0 (control 1). ALL PASS.
- Name scan of the kit itself (same lists plus the owner's and reviewer's first names): 0 hits on every line. Card-id pattern hits are on line 7 (a Jira label, `composer-seed-1023`) and line 100 (the verbatim refusal block) only.
- Load at drafting 6.87; heavy lock absent; no Composer pane live.

## Chain inputs (rule 4: every input exists at BASE or is made by an earlier step)
| step | inputs | from |
|---|---|---|
| 0 | kit, clone of `2_Project_Files`, deploy key, IDENTITY slot | BASE / slot |
| 0b | gh, Jira, ls-remote | hosted, read |
| 1 | template and crosswalk (root main), plan, sweep, C-entries, BASE files | BASE |
| 2 | clone at BASE, docker | Step 0 |
| 3 | Step 1 copies, BASE bundle, prototype claim | Steps 0-1 |
| 4 | Step 3's `out/` files, test text, prettier binary | Step 3 |
| 5 | head commits, the image rebuilt at head | Step 4 |
| 6 | Step 5 green | Step 5 |

## D-decisions (the drafter's, for Tuesday to keep or change)
- D1 Shape: one data file `content/baselines/default-baseline.json` (rows, with `field_targets` keyed by item and field) plus README and one test file `packages/content/test/b1948-cw2-baselines.test.ts`. No section, group, label or SM id is carried. The file joins back to the template by `template_id`/`analysis_row`.
- D2 Join rule J (control AND SM key) and hand rule J-H1 for M008 (its field comes by the bundle's `sm_sub_setting_id`; its setter is that item's `UQ-008`, although the crosswalk carries no control on M008).
- D3 Target rule TV (class to the item's own switch only). No sentence is read.
- D4 Gate G2 proposed: the test reads the file to check it, but nothing loads it into the bundle. A slot decides.
- D5 The DRAFTER_RULES refusal line is carried verbatim, as the commission requires. It contains a card id, which conflicts with fence 7 (no card id in kit text). It sits in a block marked never to copy, and the CK5 card-id scan covers every output.
- D6 Seat name `Datasec/Composer-C107` as commissioned. The launch line has no usage-stop variable and runs at level sonnet (row C2).

## Q-questions for Tuesday (each with a default)
- Q-1 May PCOMP-36 close with 4 typed values, 16 variable and 14 null? **Default: it stays open, with a comment saying what is met** (the commission's default). A later lane could read the 14 targets from the template sentences into typed values. That is a reading, not a sentence copy, but it needs your word.
- Q-2 Does "Enable" map to `on` or to null? **Default `on`** (the slot REMEDIATION-ENABLE; under `null` the 21 rows get `REMEDIATION_LABEL_UNMAPPED`).
- Q-3 Gate tier. **Default G2**; G1 if you read "a test that reads it" as the trigger.
- Q-4 Severity follows the template where the bundle's `item_defaults` differ (14 of 56 comparisons). **Default: follow the template (approved, C-100)** and state it in the README; L4-1 decides how the layers merge.

## UNMEASURED
Docker daemon state; every vitest, lint, format, typecheck, build and content:check run (the base counts are RELAYED from B1803); the CODE_PATTERNS scan of a real test file (only the data file was scanned); whether the template's `target` sentences give values for the 14 `typed_not_switch` fields; the live demo's running release (no hosted read; this lane deploys nothing); live panes after 03:35.

## READ LOAD (by program)
Kit 54,095 bytes. Plan lines 104-113: 4,842. Sweep lines 65-92: 5,119. CLARIFICATIONS slices: 16,291. Whole files: 39,974. **About 120 kB in context**, with the template, crosswalk, bundle and catalogue read by program only.

## Outside-the-fences disclosure
Writes went only to this report, the kit, its `.measured` sidecar, and the scratch folder `fleet/state/s313/d1948/`. I made no write to the Composer project, Jira, GitHub or any lock. Reads in other trees used git read verbs only (`rev-parse`, `config --get`, `grep`, `show`) on the finished clone `.tools/b1803/clone` and `cat-file` on the root records repo. I ran the project's `node_modules/.bin/prettier` (3.9.6) on scratch copies only, without the heavy lock (the lock was free; this was not a test run). I ran no docker, no `cd`, made no hosted request beyond GET, sent no message and deleted nothing. One stale line in my scratch `join.py` compared a dict to a string; it affected only a printed counter and was superseded by `join2.py` and `proto.py`. Other drafters' folders (`d1944` to `d1947`) were listed by `ls` of `s313/` and not opened.
