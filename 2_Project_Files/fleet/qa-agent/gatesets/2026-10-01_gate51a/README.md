# Gateset 2026-10-01_gate51a — README for Wednesday

Written by the drafter on 2026-10-01. All times are UTC from `date -u`. Every figure below comes from the kit's own output file, which is named beside the figure.

## 0. Status and what remains

**KIT COMPLETE. It is READY to launch once the routing line (section 4) is added.**
- Launcher `--check`: rc 0 before AND after the controls (launcher_check_1.out, launcher_check_2.out).
- Launch-action `--dry-run`: rc 0 (repin_dryrun_1.out, 02:52:15Z). The ONLY thing it reports is the missing routing line. It reads `BOTH INSTRUMENTS AGREE with the pin, 1 of 1`, and the census reads `0 touch a kit path or carry a kit key outside reported_overlaps`.
- Controls: normal **rc 0, 112/112 OK**; `--invert` **rc 1, 112/112 MISMATCH** (section 5).
- **Still Wednesday's: the routing line (section 4) and the launch (section 9).**

Drafted **PINNED**. Wednesday named PR #1365 at head `bf277eead26897bb648c801f92308681dbdaffdc`, on base develop `c56dd7c32edf203177ade6c4d0c9040e624681b8`. The drafter re-read both:
- at 02:20:43Z and again at 02:26:14Z, by `ls-remote` (develop, the branch and `refs/pull/1365/head`);
- by the PULLS API (gh_read_1.out): open, base develop @ c56dd7c32edf, mergeable True / `unstable`.

A new head means a RE-DRAFT (section 8).

**Proportionate by design (usage 87%, hard stop 90%).** gate50b's sources / linear / baseline instruments are dropped. Two cheap instruments are new to this kit:
- **specdiff_gate51a.py** covers requirement 1 and the red-cell census. It reads blobs and applies the six Spark goldens under a temp index.
- **handlers_gate51a.py** covers requirement 3 as a static reading, with a control operation that must read ACCEPTS.

No install, suite, tsc or generator run happened in drafting. Those are the gate's job (requirements 2, 4 and 5).

**What the drafter did and did not do.**
- It launched nothing and added no routing line.
- It sent no mail, posted nothing, and changed no ticket or PR.
- It merged, committed and pushed nothing, and deleted nothing.
- It wrote only to this kit directory and to `g51a_sp/` in its session scratchpad. Every git write verb (fetch, `apply --cached` under a temp index, `hash-object`, `commit-tree`, the control plants) ran in the scratch clone only.
- In `/Volumes/DevMASTER/!CODING/` it ran only `ls-remote` (through the launcher and the launch action) and read-only `clone --shared` as a source, and it read files.
- External reads were GitHub REST GETs only: PR, files, commits, the open-PR census and compare. GH_TOKEN was read by name and never printed. Linear was not read.

**Incident, kept for the record.** One drafting command used an UNQUOTED heredoc, so the shell executed the backtick spans in a docstring. The following ran in the WEDNESDAY cwd:
- `git ls-remote` (read-only; it printed the Wednesday remote);
- a failed `git clone --shared --no-checkout` (no repo argument, so nothing was created);
- a failed `git ls-tree` (usage error);
- a failed `required: true` (command not found).

There were no writes and no side effects. The broken pin file it produced was regenerated from a quoted script (`g51a_sp/mkpin.py`).

## 1. The PR and the BLUF

| PR | ticket | tier | head | parent | ahead / behind | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1365 | KS-1364 (Refs, narrows 11 of 17) | T2 | `bf277eead26897bb648c801f92308681dbdaffdc` | `c56dd7c32edf` (= develop, #1364's merge) | 1 / 0 | 11, **+316/-6** | 81 -> 89 (PR title == commit subject) |

- Pane: `QA/Secuura-batch1365` (**not routed**, see section 4). GO string (the GO mail's SUBJECT): `GO (Seat B 52nd): merge 1365 on gate51a`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-01-batch1365-g51a/` (it does not exist yet).
- Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE51A #1365 (Seat B52 author and merger, round 51a; T2 OpenAPI: eleven request bodies marked required, 6 new spec-rendering tests, the generated yaml)`.

**END_TREE `da849aa1d5c3d60f62b49b7f625fca01e3d59059`.** It was computed as gate50b did it. pin_gate51a.py (F) ran `git merge-tree --write-tree develop head`, then `commit-tree -p develop` as the simulated squash, in the scratch clone; the result was `11 files changed, 316 insertions(+), 6 deletions(-)`. end_tree_crosscheck_1.out cross-checks it with two more instruments:
- the head's own tree (parent == develop, 0 behind);
- GitHub's test-merge `refs/pull/1365/merge` (`85265e75ff9d`, parents develop + head).

All three read `da849aa1d5c3`. The control that differs is develop's own tree, `90fe6bbb79eb` (= gate50b's END_TREE, as it should be).

**Drafter predictions (the gate re-derives each one):**
- **pin_1.out `PASS`:**
  - 11 paths, all inside the allowed prefixes (the 4 services' `src/` + the yaml), with 0 package/lock paths;
  - all 11 paths are 100644 (control: `scripts/run-migrations.sh` 100755 at develop / head / END);
  - the hook, preflight, generator, check-spec-examples and package.json are identical in every tree;
  - **11 unchanged pins byte-equal**: every handler file (`nft.routes.ts`, `analytics.ts`, `billing.ts`, m365 `index.ts`), `analytics.types.ts`, the 4 express.json mount files, `generate-openapi.ts`, `package.json` and `package-lock.json`.
- **specdiff_1.out `SPECDIFF PASS: 0 FAIL of 7 checks`:**
  - S1: exactly the 11 paths, `*.openapi.ts` +4/-2, +1/-1, +2/-0, +4/-3 (sum +11/-6), whole PR +316/-6.
  - S2: on the + side, drop `required: true,` lines and strip `, required: true`; the result == the - side in every file. 11 added, all inside a `request: { body }` block, as **6 replacements / 5 insertions**.
  - S3: yaml +11/-0, all `        required: true`, all directly under `requestBody:`, landing on exactly the 11 POST operations (count 60 -> 71).
  - S4: the six goldens applied in order onto develop under a temp index (0 offsets) give a tree **blob-equal to the head on all 10 non-yaml paths**. The yaml is the control that differs.
  - S5: 11 RED cells == the kit's list, plus 18 control cells. Each test imports only `vitest`, `@secuura/shared` and its own `../<svc>.openapi`.
  - S6: 0 runtime source paths (control: develop^..develop lists #1364's 2 audit paths).
- **handlers_1.out `HANDLERS PASS: 11 of 11 operations REJECTS-EMPTY`.** The runtime is express 4.22.3 / body-parser 1.20.8 from the root lock, with an express.json mount in all 4 services. Per operation, route:validator at head:
  - NR1 `nft.routes.ts:128/:130`, NR2 `:184/:186`, NV1 `:387/:393`, NV2 `:421/:428`;
  - AR1 `analytics.ts:388/:390`;
  - BL1 `billing.ts:410/:412`, BL2 `:546/:551` (a truthy check);
  - MS1 `index.ts:754/:756`, MS2 `:881/:883`, MS3 `:1462/:1464`, OD1 `:1050/:1053` (a truthy check).
  - **Control TENANT-CTL** (`PATCH /api/platform/tenants/{id}`, `tenant-provisioning/src/index.ts:440/:442`, every field optional) reads **ACCEPTS-EMPTY**, as expected.
- **keyscan_1.out `KEYSCAN PASS: 6 checks, 0 FAIL, 0 FLAG`.**
  - Subject keys {KS-1364}; it lands at 89.
  - `Refs KS-1364` is on its own line, once. There is no closing keyword.
  - The PR body, commit, title and branch carry no foreign hyphenated key. The de-hyphenated KS 255 and KS 1015 are present.
- **gh_read_1.out:** 22 other open PRs, of which **0** touch a kit path or carry KS-1364 in the title. kit.json `reported_overlaps` is therefore EMPTY. Peter's #1360 and #1362 are reported as client-human.

## 2. What the gate must rule
The prompt names each item, and the launcher refuses a prompt that is missing any of the 28 keywords.
1. **PATHS-ELEVEN, REQUIRED-ONLY, YAML-ELEVEN, GOLDENS-BYTE-EQUAL.**
2. **GENERATOR-REPRODUCES, CHECK-OPENAPI-RC**: `generate-openapi --check` at head with the base-yaml control, a non-check regeneration that leaves the yaml blob unchanged, and `check:openapi` at head AND base.
3. **HANDLER-REJECTS-ABSENT, NO-RUNTIME-CHANGE**: file:line per operation at head. The `{}`-default must be cited from body-parser's installed source. An accepting handler is a Major. TENANT-CTL is the control.
4. **RED-FIRST, CONTROLS-GREEN**: product hunks reverted, tests kept; 11 RED by assertion, 18 controls pass; 29 pass at head.
5. **SUITES-BASE-HEAD, TSC-NO-REGRESSION**.
6. **SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, DEHYPHENATED-KEYS, SIX-REMAINING-NAMED, NOT-COVERED-HONEST, PR-BODY-CLAIMS**: X5 allows one read of KS-1364 to check the 11 + 6 = 17 list.
7. **CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS; TIERING, DISK-ENOSPC, REPORT-HASH-LAST.**

**Doubts the drafter found (all are in the prompt for the gate to rule):**
- (a) **The PR body says "Five of the eleven product edits are replacements, six are insertions". The measured split is 6 / 5** (specdiff S2). The replacements are analytics 1, m365 3 (sites, documents/sync, verify-hash) and nft 2 (record, estimate). The insertions are billing 2, onedrive 1 and nft-verify 2. Six deletions = six replacements. Polish.
- (b) **"the handler's zod schema answered 400"** appears in the PR body AND the commit message. That is true of 9 operations. BL2 (`default-payment-method`, `billing.ts:551`) and OD1 (`onedrive/files/{id}/sync`, `index.ts:1053`) are TRUTHY checks, not zod. The subject itself ("where handlers reject an absent body") is accurate. Imprecise; Minor at most. The six test-file headers already describe BL2 and OD1 correctly.
- (c) **The runtime-truth argument rests on `express.json()` turning an absent body into `{}`.** That is body-parser 1.x behaviour (1.20.8 in the root lock; express 4.22.3). The prompt requires the gate to cite body-parser's own installed line, not memory. If a service ever moved to express 5, `req.body` would be `undefined`. BL2 and OD1 destructure `req.body` directly, so they would throw: 500 (OD1 through `next(error)`) and 500 (BL2's catch), rather than accept. Still a rejection, but not a 400.
- (d) The rendered spec paths are `/api/m365/...` for sites, documents/sync and verify-hash, but `/api/onedrive/files/{id}/sync` with no `/m365`. This PR did not change any path. Route resolvability is preflight leg 4, which the seat SKIPPED (stack not up). Information, NOT COVERED.
- (e) Two test files carry a hyphenated `KS-442` in a code comment. That is not a squash-body key; the gate says whether it matters (it should not create back-references).
- (f) **NOT the gate's (Wednesday rules them):** KS-1364 moved itself to In Progress through the GitHub integration, 10 s after the PR opened. And `mergeable_state: unstable`, whose cause is unreadable (the PAT gets 403 on status and check-runs). The drafter's gh_read also reads `unstable`.
- (g) The PR body closes with a tool-attribution line ("Generated with Claude Code") on a client-visible surface. Information. The merger composes the squash body, so it does not land in the commit.
- (h) The correction mail fixes the READY's fuse line: 189.7 h at 02:19:54Z, 3 rows. It is not a requirement here and is context only.

## 3. Pins and what the gate owes
- `fill_gate51a.py` FILLS the prompt `2026-10-01_secuura-batch1365.prompt.txt`, the launcher `launch_qa_secuura_batch1365.sh` and COMMISSION.md (fill_1.out rc 0). The fill refuses unless three things hold:
  - gate50b's report still hashes to `a2bb0cddbf9f…`;
  - `end_tree_crosscheck_1.out` carries END_TREE three times;
  - specdiff / handlers / keyscan / gh_read each end in their PASS / OK line, at this develop and head.
- The launcher's exits are re-keyed from gate50b's:
  - **34**: the NO-RUNTIME rule (no live server, no Schemathesis, no image, no database);
  - **36**: the RUNTIME-TRUTH rule ("A HANDLER THAT ACCEPTS AN ABSENT BODY IS A MAJOR", the TENANT control, "never from memory");
  - **37**: the NOT-THE-GATE'S items (KS-1364 state, mergeable_state);
  - **38**: proportionality at 87% with the 90% hard stop;
  - **33**: also requires `ASSERT THE FILENAME TOO`.
- Named exceptions:
  - X1: the registry reads of `npm ci`;
  - X5: ≤2 read-only Linear queries (KS-1364);
  - X6: read-only GitHub GETs for the census.
  - gate50b's X4 (the advisory API) is NOT granted.
- `reported_overlaps` and `sequenced_out_of_kit` are EMPTY. An overlap at launch refuses with rc 15.

## 4. Routing line — NOT added
Back up the file first (`inbox_routing.conf.pre-<date>`). Then add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-batch1365|coagent@agentmail.to|yes
```
Until that line is present, step 0 of the launch action refuses with rc 1 (control R1). R8 shows a routed temp file passing step 0 and stopping after 3b.

## 5. Controls: `controls_gate51a.sh <scratchpad> [--invert]`
- **112 controls, one unedited script**: `controls_gate51a.sh`, sha256 `a25db455834d…`. controls_sha.txt shows it identical before and after run 1 (02:34:36Z) and run 2 (02:41:48Z – 02:51:39Z).
  - Normal run (controls_1.out): **rc 0, `112 controls, OK 112, MISMATCH 0 | ssh-denied retries 0`**.
  - `--invert` run (controls_2.out): **rc 1, `112 controls, OK 0, MISMATCH 112 | ssh-denied retries 0`**.
- Both runs wrote to the scratchpad first and were then copied in, byte-checked with `cmp`. This avoids the gate50b sync-truncation incident.
- Side effects, kept:
  - R1 and R8 wrote `launch_<HHMMSS>.*` step outputs here.
  - The PN simulations wrote `pins_gate51a.SIM-*.json`.
  - `repin_dryrun_0_before_controls.*` is the first dry run; `repin_dryrun_1.*` is the final one. Both rc 0.
- **Coverage:**
  - **PN0–PN6** (pin):
    - the real head as a simulation: END, shortstat, 12 mode pins, a handler blob BYTE-EQUAL;
    - `--develop` refused without `--simulate`;
    - a runtime handler file (`nft.routes.ts`) edited -> (K);
    - a develop move on the yaml -> (C);
    - the yaml recorded 100755 -> MODE MISMATCH;
    - an unrelated develop move -> NONE;
    - a path outside the prefixes -> (B).
  - **SD0–SD5** (specdiff):
    - the real head: 7/7, 6 replacements / 5 insertions, goldens 10 of 10 with the yaml control, 60 -> 71;
    - a second key changed in analytics.openapi.ts -> S2;
    - one new yaml line `required: false` -> S3;
    - one byte of the billing golden changed -> S4 9 of 10;
    - a handler file in the diff -> S6;
    - develop as head -> S1.
  - **HD0–HD3** (handlers):
    - the real head, 11/11, with TENANT-CTL ACCEPTS-EMPTY and express 4 / body-parser 1;
    - EstimateCostSchema made all-optional -> NR2 ACCEPTS-EMPTY FAIL;
    - the record validator removed -> NR1 FAIL;
    - the tenant schema given a required field -> the CONTROL itself fails.
  - **KS0–KS7** (keyscan).
  - **L0–L23 + LK1–LK28** (launcher): every exit, including 34 / 36 / 37 / 38 and the filename rule. L9 is the real non-TTY path.
  - **R0–R8** (launch action): census; routing refusal; an extra kit path -> OVERLAP #1360; a title key -> OVERLAP; sequenced right / wrong head; DISJOINT; wrong head rc 11; old develop rc 10; a bad scratchpad rc 9; routed stop-after-3b.
  - **PNZ / KJZ / PRZ**: the pins, kit.json and the filled prompt are unchanged.
- **Not controlled:** on a real launch, the usage gate (12), `cockpit.sh add` (14) and the override refusal (16); a `mergeable=False` refusal; and a real re-pin across a develop move (only the dry run's rc 10 is controlled). gh_read and fill are exercised by their real runs, not by plants.

## 6. Could not measure (the drafter)
- No install, suite, tsc, generator, vitest or red-first run happened. Requirements 2, 4 and 5 are entirely the gate's, and the seat's figures are claims until the gate runs them.
- The handler reading is static. It does not send a request.
- Linear was not read.

## 7. Files
- **Config:** kit.json · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md (this file) · READY_1365_mail.md and READY_1365_CORRECTION_mail.md (Wednesday's; unchanged).
- **Pin:** pin_gate51a.py -> pin_1.out, pins_gate51a.json (+ `pins_gate51a.SIM-*.json` from the controls) · end_tree_crosscheck_1.out.
- **Instruments:**
  - specdiff_gate51a.py -> specdiff_1.out;
  - handlers_gate51a.py -> handlers_1.out;
  - gh_read_gate51a.py -> gh_read_1.out / gh_read_1.json / gh_body_1365.md;
  - keyscan_gate51a.py -> keyscan_1.out;
  - each with its .rc.
- **Prompt and launcher:** prompt_gate51a.TEMPLATE.txt + launcher_gate51a.TEMPLATE.sh.txt, filled by fill_gate51a.py (fill_1.out) -> `2026-10-01_secuura-batch1365.prompt.txt`, `launch_qa_secuura_batch1365.sh` and COMMISSION.md. Checks: launcher_check_1.out (before the controls) and launcher_check_2.out (after).
- **Launch:** repin_and_launch_gate51a.sh -> repin_dryrun_0_before_controls.out, repin_dryrun_1.out.
- **Controls:** controls_gate51a.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt.
- **Provenance:**
  - pin, fill, gh_read, keyscan and repin are NEW COPIES of gate50b's (re-keyed by quoted python in `g51a_sp/mk*.py`, then edited);
  - specdiff, handlers, the templates and the controls are new;
  - gate50b's kit is untouched.

## 8. Re-draft recipe (a new head on #1365, or a develop move that reaches a kit path)
1. Keep kit.json as `kit.json.pinned-bf277eea`.
2. Set `prs.1365.head` (and `pinned`) to the new head.
3. Run, in order: `pin_gate51a.py <sp>` -> `gh_read_gate51a.py` -> `specdiff_gate51a.py <sp>` -> `handlers_gate51a.py <sp>` -> `keyscan_gate51a.py <sp>`.
4. Re-run the three END_TREE instruments into a new `end_tree_crosscheck_1.out`.
5. Run `fill_gate51a.py`.
6. Run the controls both ways. Update the head-specific patterns first: the PN0k blob, the S4 golden equality, and the handler line numbers if the handlers moved.
7. Run `--check`, then the dry run.

A develop move that does NOT reach the 11 paths is re-pinned by the launch action itself (step 3b: pin -> specdiff -> handlers -> fill).

## 9. The ONE launch command (run it after the routing line in section 4 is added)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-01_gate51a/repin_and_launch_gate51a.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-01_gate51a/launch_qa_secuura_batch1365.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/cb6b682a-5afd-4a5e-a1e3-be903cfa4469/scratchpad
```
- Append `--dry-run` for a dry run.
- Argument 2 may be ANY existing Claude session scratchpad. If `g51a_sp/clone` is absent there, pin_gate51a.py rebuilds it from the checkout on a re-pin.
- After the gate's verdict and a GO, the squash key set is exactly {KS-1364}. Wednesday still owns the KS-1364 state question (doubt f).
