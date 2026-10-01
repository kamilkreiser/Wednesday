# Gateset 2026-10-01_gate50b — README for Wednesday

Written by the drafter, 2026-10-01 AEST (all times UTC from `date -u`; the host clock read 2026-09-30T23:4x–00:xxZ). Every figure below comes from the kit's own output files, each named beside the figure.

## 0. Status and what remains

**KIT COMPLETE — READY to launch once the routing line (section 4) is added.** Launcher `--check` rc 0 before and after the controls (launcher_check_1.out, launcher_check_2.out). Launch-action `--dry-run` rc 0 (repin_dryrun_1.out): the ONLY report is the missing routing line; `BOTH INSTRUMENTS AGREE with the pin, 1 of 1`; census `0 touch a kit path or carry a kit key outside reported_overlaps | 0 expected overlap(s)`. Controls: see section 5 (CONTROLS_RESULT). **Still Wednesday's: the routing line and the launch (section 9).**

Drafted **PINNED**: Wednesday named PR #1364, head `f7466281acf18fd7ea47be19bfa88ececdb3dbb8`, base develop `723dc0722b68482a03de8577fdb5eb5b3359e725`; the drafter re-read both at 2026-09-30T23:48:40Z by `ls-remote` (develop, the branch AND `refs/pull/1364/head`, all as named) and by the PULLS API (gh_read_1.out: open, base develop @ 723dc0722b68, mergeable True / `unstable`). A new head is a RE-DRAFT (section 8).

**Proportionate by design (usage 82%).** gate50a's kit carried lockdelta / reach / overlaps / capture instruments and 144 controls for a T1 lock refresh with a served-image consumer. #1364 is T2 (two files under `scripts/audit/`, no runtime code), so this kit drops those instruments, builds no image and adds two cheap ones of its own: **baseline_gate50b.py** (requirement 1 + 3 by parsing both blobs) and **sources_gate50b.py** (the cited lines behind the two texts). The capture is Wednesday's saved `READY_1364_mail.md` (it names the head in full) — no AgentMail re-capture.

**What the drafter did and did not do.** It launched nothing, added no routing line, sent no mail, merged / committed / pushed nothing, posted nothing on Linear or GitHub, changed no ticket or PR, deleted nothing. It wrote only this kit directory and its session scratchpad (`g50b_sp/`: `git clone --shared --no-checkout` of gate50a's scratch clone; develop, `refs/pull/1364/head` and `refs/pull/1364/merge` fetched from origin ONLY there; merge-tree / commit-tree and every control plant run THERE). In `/Volumes/DevMASTER/!CODING/` it ran `ls-remote` (launcher and launch action) and read files. External reads: GitHub REST GETs (PR, files, commits, open-PR census, compare), Linear GraphQL **queries only** (4 tickets, metadata + headings printed; no description stored in the kit). GH_TOKEN / LINEAR_API_KEY read by name, never printed. No install, no audit leg, no build, no SSH, no database.

## 1. The PR and the BLUF

| PR | ticket | tier | head | parent | ahead / behind | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1364 | KS-729 | T2 | `f7466281acf18fd7ea47be19bfa88ececdb3dbb8` | `723dc0722b68` (= develop, #1363's merge) | 1 / 0 | 2, **+2/-9** | 78 -> 86 (PR title == commit subject) |

- Pane `QA/Secuura-batch1364` (**not routed** — section 4). GO string (the GO mail's SUBJECT): `GO (Seat B 51st): merge 1364 on gate50b`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-01-batch1364-g50b/` (does not exist yet).
- Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE50B #1364 (Seat B51 author and merger, round 50b; T2 baseline cleanup: the dead mwp4 row removed 26->25, r53p reason, contract count line; ITEM 4 ticket text and KS-1397 comment ruled)`.

**END_TREE `90fe6bbb79eb487023eda4ab8cb237a29f924f8b`** — computed as gate50a did (pin_gate50b.py (F): `git merge-tree --write-tree develop head`, then `commit-tree -p develop` as the simulated squash, in the scratch clone; `2 files changed, 2 insertions(+), 9 deletions(-)`), cross-checked in end_tree_crosscheck_1.out by the head's own tree (parent == develop, 0 behind) and GitHub's test-merge `refs/pull/1364/merge` (`82f70c670826`, parents develop + head) — all three `90fe6bbb79eb`; develop's own tree `2a874956406c` (= gate50a's END_TREE, as it should be) is the control that differs.

**Drafter predictions (the gate re-derives each):**
- pin_1.out `PASS`: 2 paths, both 100644 (control `scripts/run-migrations.sh` 100755 at develop / head / END); 8 hook/audit paths identical; 11 unchanged pins byte-equal incl. `baseline-contract.test.mjs` `2379c0aeee6e`, `expected-case-count`, legs 6/7 code, the stub, and the ITEM 4 / ITEM 5 source files (nginx.conf, 039, 038a, run-migrations.sh, startup-migrations.ts).
- baseline_1.out `BASELINE PASS: 0 FAIL of 14 checks`: rows 26 -> 25; removed exactly `{GHSA-mwp4-54f8-5fhr}`, added none; only r53p differs and only in `reason`; that reason == `2026-09-30_seatB-49th/cleanup/r53p-reason-corrected.txt` character-exact (1948 B, **no trailing newline**; control: develop's reason != file); stale clause before/after True/False; 2026-10-09 cohort 4 -> 3 (337j, frvp, wrjc), survivors byte-equal (parsed AND raw block); no expires changed (histogram `{10-09: 4->3, 10-15: 3, 10-31: 1, none: 18}`); GRANDFATHERED block byte-equal, 18 ids == the head no-expiry set; contract differs on `:44` only (17 -> 18); test file blob-identical and `:217` carries `> 20` (control: the same probe on the WRONG file reads False); FUSE at END 3.
- sources_1.out `SOURCES READ: 0 FAIL of 12 reads`: ticket files == the mail (121 B `1facfe057646fd82`, 5364 B `c99de066b941f0cb`); `run-migrations.sh:118-122` and `startup-migrations.ts:137-141` are the skip lines and identical at develop and at the cited `91a8f6b721bc`; 039 lists `charge_events` since `46fb9f88d` (KS-458, pickaxe); 038a's charge_events DDL carries `tenant_id UUID`; B 50th's probe (before) and handover after-table both read charge_events rls false / force false / 0 policies / 8 rows; the ticket text has 0 internal-vocabulary hits; nginx.conf `:24 server_tokens off;` `:142 proxy_hide_header Server;`.
- keyscan_1.out `KEYSCAN PASS: 6 checks, 0 FAIL, 0 FLAG`; the PR body `gh_body_1364.md` == the seat's `item1/pr-body.md` byte for byte (sha256 `917a52976127…`); de-hyphenated KS 470 / 559 / 528 / 530 / 1378 all present; no foreign hyphenated key anywhere.
- gh_read_1.out: 22 other open PRs; **0** touch either path or carry KS-729 in the title (kit.json `reported_overlaps` is therefore EMPTY); Peter's #1360 / #1362 reported as client-human. The old KS-729 branch (`…-upgrade-ip-address-off-ghsa-mwp4-…`, `bac58b93acf3`) exists at origin with no open PR titled KS-729.
- linear_read_1.out: KS-1376 Backlog (unassigned), KS-1054 In Progress, KS-1397 Backlog, KS-729 In Progress (all four read by query; headings only).

## 2. What the gate must rule (by name in the prompt; the launcher refuses a prompt missing any of the 29 keywords)
1. **DIFF-REDERIVED, TWO-FILES-ONLY, ROWS-26-25, REASON-CMP, NOTHING-REDATED, GRANDFATHERED-BYTE-EQUAL, CONTRACT-ONE-LINE, FLOOR-NOT-LOWERED** — #1364's diff re-derived by parsing both blobs.
2. **MWP4-DEAD-BOTH-LEGS, LEG7-PROBE, LEGS-RC-HEAD, GATE-STILL-REFUSES** — leg 6 CLEANUP lists mwp4 at develop; leg 7's REPORTED map lacks it (throwaway probe with a positive control; never the CLEANUP block, empty by construction, `audit-locks.mjs:299`); legs 6/7/contract rc 0 at head with a refusal control each; plus one information parse of the `ip-address` versions in the locks KS-729 names.
3. **FUSE-COHORT** — 3 rows dated 2026-10-09 at END (frvp, wrjc, 337j), develop's 4 as the control.
4. **ITEM4-TICKET-TEXT** — POST AS-IS / POST AMENDED (full text) / DO NOT POST, sentence by sentence against B 50th's RECORDED readings (no DB read — the prompt says so), the migration files at develop, KS-1376 and KS-1054 on Linear.
5. **KS1397-COMMENT** — same scale, against nginx.conf :24 / :142 at develop and KS-1397's own description.
6. **SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, DEHYPHENATED-KEYS, PR-BODY-CLAIMS**.
7. **CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS**; **TIERING, DISK-ENOSPC, REPORT-HASH-LAST**. The prompt states 82% and THE CHANGE IS SMALL (launcher exit 38 without it); no image build, no service suite, no SSH, no database (exit 34 / 39 without those lines).

**Doubts the drafter found (all in the prompt for the gate to rule):**
- (a) **KS-1397 comment, a likely POST AMENDED:** "Upstream `Server` headers are already stripped: `nginx.conf:142`" is true of the LOCAL gateway config only. `nginx-demo.conf` and `nginx-production.conf` carry `server_tokens off` (the control, 1 each) but **0** `proxy_hide_header Server` (sources_1.out N2; case-insensitive). The comment reasons about "every nginx target", so on demo / production an upstream `Server` header may still pass through. KS-1397's own text makes the same nginx.conf-only citation.
- (b) **The KS-1397 draft's first line is internal** ("# DRAFT comment for KS-1397 (Wednesday, …). Gate it before posting; …": `Wednesday` 1, `gate` 1, `DRAFT` 1; with it removed the sweep reads NONE — control SO2). Strip it before posting. "Kamil's ruling" is Wednesday's relay, UNVERIFIABLE from the sources.
- (c) **The PR body (client-visible) says "Wednesday's to propose"** in its Residue section (and the commit message too; the merger composes the squash body, so only the PR body stays). Internal fleet vocabulary on a client surface. The planted contract id `GHSA-b51c-0nt-rol01` carries a seat number. Polish / Minor.
- (d) **"line count unchanged at 228"** (PR body and commit): `wc -l` and `awk 'END{print NR}'` read **227** at both trees. Polish (the seat probably counted `split('\n')`).
- (e) **ITEM 4 text:** "A fresh database from `91a8f6b721bc`: covered by KS-1054's fix" for `charge_events` sits beside KS-1376's own finding that the same 038a-then-039 path left `certifications` FORCED with no policy. 038a gives `charge_events` a `tenant_id` column, so 039 should apply its policy, but no fresh-DB `charge_events` reading is in the sources. Also "No fix is proposed in this ticket" sits beside "What done means" item 2 (a migration numbered after 039), and the claim that KS-1376's unwritten fix "also remediates" kintsugi's `certifications` is an inference. The scoping call (a new ticket vs a comment on KS-1376) is Wednesday's: the seat asked.
- (f) The ITEM 4 table's "before and after … identical both times" holds (probe_rls.out before, the handover after-table). But the controls it lists come from two sessions: `to_regclass` appears only in the after-read.
- (g) Mode control: both PR paths are 100644, so `scripts/run-migrations.sh` (100755, outside the PR) is the control that shows the instrument discriminates.

## 3. Pins and what the gate owes
- The prompt `2026-10-01_secuura-batch1364.prompt.txt` and the launcher `launch_qa_secuura_batch1364.sh` are FILLED by `fill_gate50b.py` (fill_1.out rc 0). The fill refuses unless gate50a's report still hashes to `1259cda7fe6f…`, `end_tree_crosscheck_1.out` carries END_TREE three times, and every drafter read ends in its PASS / READ / OK line at this develop / head.
- The launcher refuses on gate50a's exits (2–33, 39), re-keyed: **34** = the NO-RUNTIME + NO-DATABASE rules; **36** = the authority line (the brief's ITEM 1 + the route (a) one-time grant for base 723dc0722b68; "never its CLEANUP block"; "EMPTY BY CONSTRUCTION"); **37** = the two TEXT rulings (incl. the internal header line and the `proxy_hide_header Server` doubt); **38** = proportionality at 82%; **33** also requires `ASSERT THE FILENAME TOO`.
- Named exceptions: X1 registry reads of `npm ci` / `npm audit` (the legs); X4 advisory API GETs; X5 ≤5 read-only Linear queries; X6 read-only GitHub GETs for the census. (gate50a's X2 refresh containers and X3 image builds are NOT granted.)
- `reported_overlaps` and `sequenced_out_of_kit` are EMPTY. An overlap at launch refuses rc 15.

## 4. Routing line — NOT added
Back up the file first (`inbox_routing.conf.pre-<date>`). Then add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (currently 162 lines, the last `QA/Secuura-batch1363|coagent@agentmail.to|yes`):
```
QA/Secuura-batch1364|coagent@agentmail.to|yes
```
Until it is present, step 0 of the launch action refuses rc 1 (control R1); R8 shows a routed temp file passing step 0 and stopping after 3b.

## 5. Controls: `controls_gate50b.sh <scratchpad> [--invert]`
CONTROLS_RESULT

## 6. Could not measure (the drafter)
No audit leg, install, probe or suite: mwp4 being dead to both legs at develop, and every leg rc at the head, are the seat's claims until the gate runs them. No database read anywhere: the ITEM 4 facts are B 50th's recorded readings. Linear text was read but is not stored in the kit.

## 7. Files
- **Config:** kit.json · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md (this) · READY_1364_mail.md, ITEM4_ticket_text_mail.md, KS-1397_acceptance_DRAFT.md (Wednesday's; unchanged).
- **Pin:** pin_gate50b.py -> pin_1.out, pins_gate50b.json (+ `pins_gate50b.SIM-*.json` from the controls) · end_tree_crosscheck_1.out.
- **Instruments:** baseline_gate50b.py -> baseline_1.out · sources_gate50b.py -> sources_1.out · gh_read_gate50b.py -> gh_read_1.out / gh_read_1.json / gh_body_1364.md · keyscan_gate50b.py -> keyscan_1.out · linear_read_gate50b.py -> linear_read_1.out (each with its .rc).
- **Prompt and launcher:** prompt_gate50b.TEMPLATE.txt + launcher_gate50b.TEMPLATE.sh.txt, filled by fill_gate50b.py (fill_1.out) -> `2026-10-01_secuura-batch1364.prompt.txt`, `launch_qa_secuura_batch1364.sh`, COMMISSION.md; launcher_check_1.out (before the controls), launcher_check_2.out (after).
- **Launch:** repin_and_launch_gate50b.sh -> repin_dryrun_1.out (rc 0).
- **Controls:** controls_gate50b.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt.
- pin / gh_read / keyscan / repin are NEW COPIES of gate50a's (sed re-key, then edited); baseline / sources / linear_read / controls / templates are new. gate50a's kit is untouched.

## 8. Re-draft recipe (a new head on #1364, or a develop move that reaches a kit path)
Keep kit.json as `kit.json.pinned-f7466281`, set `prs.1364.head` (and `pinned`) to the new head, then: `pin_gate50b.py <sp>` -> `gh_read_gate50b.py` -> `baseline_gate50b.py <sp>` -> `sources_gate50b.py <sp>` -> `keyscan_gate50b.py <sp>` -> re-run the three END_TREE instruments into a new `end_tree_crosscheck_1.out` -> `fill_gate50b.py` -> the controls both ways (update the head-specific patterns) -> `--check` -> dry run. A develop move that does NOT reach the 2 paths is re-pinned by the launch action itself (step 3b: pin -> baseline -> sources -> fill).

## 9. The ONE launch command (run it after the routing line in section 4 is added)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-01_gate50b/repin_and_launch_gate50b.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-01_gate50b/launch_qa_secuura_batch1364.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/cb6b682a-5afd-4a5e-a1e3-be903cfa4469/scratchpad
```
- Append `--dry-run` for a dry run (rc 0 today, repin_dryrun_1.out). Argument 2 may be ANY existing Claude session scratchpad; if `g50b_sp/clone` is absent there, pin_gate50b.py rebuilds it on a re-pin.
- After the gate's verdict and a GO: Wednesday files the ITEM 4 ticket and posts the KS-1397 comment per the gate's POST rulings (then moves KS-1397); the squash key set is exactly {KS-729}.
