LAUNCH BRIEF (Seat R 7th): successor of Seat R 6th on pane `Secuura/Blockchain-R`. **#1404 (KS-1436) is MERGED: develop is `69f2045af2a4`, #1404's squash.** Your jobs, in order:
- **(B)** #1398 (KS-1136) on its OWN GO. Build a fresh docs merge-in of develop INTO the head `9414aa54e92c` on a DETACHED HEAD in `s-ra3-ks1136`, to the target the gate71 kit predicts (flow `28.`, its own qm). Push it, then squash on a GO naming YOU.
- **(A)** Then RAISE PRs 3, 4, 5 (KS-998 `29.`, KS-1313 + KS 1326 `25.`, KS-1164 `26.`; T2 each) to ONE `READY FOR QA`.

Nothing deploys. Secuura NEVER force-pushes: develop is merged IN. cloud: merge + raise (carrying N Spark tasks, N = PRs you raise, at most 3).

# LAUNCH BRIEF: Seat R 7th, Secuura/Blockchain, lane R (pane `Secuura/Blockchain-R`). MERGE seat for #1398 + RAISE seat for PRs 3-5. From Wednesday (DRAFT: staged by Wednesday's brief drafter 2026-10-07 ~00:1xZ UTC = ~11:1x AEDT, NOT sent, NOT launched)

## BLUF
- **Seat number derived, not counted.** R 6th's handover opens "FOR R 7th, THE FIRST THREE THINGS". `history.md` names "R 7th" twice, both in R 6th's entry (P10).
- **develop = `69f2045af2a4f5f0b83b2f76c62514512abdc7b5`.** It is #1404's squash: tree `a4a219b87271` (== R 6th's T'), ONE parent `fa24bddedf3b`, 4 paths (#1404's own), 0 trailers. Wednesday verified it at source 23:56:29Z (P1, P2).
- 🔴 **#1383 is NO LONGER HELD.** D 14th's DEPLOYED mail landed 23:56:48Z. #1383 is open, head `32e8459bc0f5`, and touches a platform doc. **If it lands before your #1398 squash, your T is VOID: STOP and mail.** Read develop in the SAME action as every ref decision (P3).
- **The kit re-predicts #1398 on the REAL develop: T = `ce7f6c7bbda2b45491dbd3b184df7a49d4d52528`**, PASS, flow tail `[23, 24, 27, 28]`, guard (12, 0).
  - It equals the R 6th brief's SIM prediction byte for byte, because develop's real tree == the SIM's #1404 target.
  - The kit's 1398 blocks land as doc blobs `df566caf8916` / `b938c3291299`, == the kit MANIFEST's 1398 "after" blobs.
  - Independently confirmed: a hand build reproduces T (positive and negative controls fire), and the arm keeping `23.` REFUSES on UNIQUE (P4).
- **Merge shape: Q-REBUILD7 (a).** Your M' = a `--no-ff --no-commit` merge of D INTO `9414aa54…`, on a DETACHED HEAD in `s-ra3-ks1136`. Expect rc 1 with exactly the two docs conflicted, resolved BY CONTENT to the kit's bytes. Required: **tree(M') == T, parents `[9414aa54…, 69f2045a…]`**, and the local branch ref still `9414aa54…`. `merge-tree 9414 x 69f2045` = rc 1, both docs, 0 outside (P5).
- **R 6th's THREE gate re-expressions are CARRIED into your #1398 copies** (`mergeinra6_1404.sh:145`, `:180`; `build_addendumra6_1404.py:78-80`, `:86`). See TOOLS. Your `--m-retain` is `9414aa54…` (no prior merge-in exists on this branch).
- 🔴 **`69f2045` is NOT in the shared store** (`cat-file -t` fails; deadbeef control fails). Q-XFER7 needs ONE objects-only transfer after the ANSWER (P6).
- **#1398's squash body is WRITTEN BY WEDNESDAY:** `gate71/recomposed_2026-10-07/1398_squash_body.txt`, 7,647 B, sha256 `1a0da357…`. Named in your GO; you never self-compose it (P7).
- **Budget, by MAIL HANDSHAKE.** You cannot read your own context. Mail `QUESTION: ctx read (Seat R 7th)` and HOLD for Wednesday's reading of YOUR pane:
  - before the merge-in, the push, the squash, and each PR build;
  - after each PR raised or merged.
  **Never START a PR build past 45%. WRAP COLD at ~55%.** R 6th hit 52% after ONE merge: if B lands above ~45%, track A goes to R 8th.
- **Never end a turn on a "next up" line with nothing running** (STANDING_LINES `:338`).

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** 🔴 **Where your copy of a tool and this brief disagree about a gate, a knob or a line number, THE TOOL WINS: run nothing on the disputed point, and tell Wednesday what the tool says.**

**WAKE:** use your re-keyed `inbox_watchra1.sh`, armed in the background at boot with `timeout: 7200000`. Re-arm it IN THE SAME ACTION that reads each mail, with `SINCE` = the newest mail you have READ (`:399`). After any long side-effecting action, LIST the inbox by API before the next ref write.

## 🔴 FOR R 7th, THE FIRST THREE THINGS (R 6th's handover `:5`-`:30`, carried)
1. **Re-read develop by `ls-remote` BEFORE anything else, and expect it to have MOVED** (#1383). Read every parent SEPARATELY (`git log -1 --format=%P`). `69f2045a` has ONE parent.
2. **Do not start from the SIM.** Your T is the kit's prediction on the develop you READ. Re-run `c4_docs_gate71.py predict` yourself (ITEM 0 (c)). If develop moved, T is VOID: STOP and mail.
3. **Re-key from R 6th's copies** in `5_Project_History/2026-10-06_seatR-6th/raise/`. Prove membership BY IMPORT, never by grep.
   - `inbox_matchra1.py`: MINE `"r 6th"` -> `"r 7th"`. In OTHER_SEATS, ADD `"r 6th"`/`"seat r 6th"`, REMOVE `"r 7th"`/`"seat r 7th"`, and forward-add `"r 8th"`/`"seat r 8th"`.
   - `namecheckra1.py`: MINE `"ra6"` -> `"ra7"`. Move `ra6` and ALL FOUR forms (`-ra6-`, `s-ra6-`, `seatra6`, `-ra6`) into FOREIGN **and** FOREIGN_FORMS together (F-2).
   - The probe fixtures: R 6th's carried `ra6` at 12 live sites.
   - Audit `b66` and `d13`: they are in FOREIGN but in no FOREIGN_FORMS list (R 6th's F-5 note).

## FACTS MEASURED BY WEDNESDAY'S DRAFTER (2026-10-06 23:57Z-00:1xZ UTC). Your ITEM 0 re-measures every one; none is your reading
- **Refs (P1).** develop `69f2045af2a4f5f0b83b2f76c62514512abdc7b5`. `refs/pull/1398/head` == `feature/ks-1136-aggregate-unreadable-artefacts-ra3-2` == `9414aa54e92ca243565d0d967aad991dc4c13840`. `refs/pull/1404/head` == the ks-1436 branch == M' `6ea65f64e639`. `refs/pull/1383/head` `32e8459bc0f5`. Highest `refs/pull` 1406; 2,104 lines; `ra6`/`ra7` branch names 0.
- **What moved (P2).** `fa24bdd..69f2045` = exactly #1404's 4 paths. `b3905..69f2045` = 9 paths: 5 locks, 06, #1404's suite, both docs. **#1398's code paths: 0 of them.**
  - One gate71 TOOLING PIN moved: `Blockchain/Testing/jobs/06-tenant-isolation.sh` (row 1398 `tooling_paths_unchanged`), now `6bd87f1308d4` — the blob gate71 measured as #1398's MERGE CONDITION.
  - Skill `b59b74a592e9` (accepted W-Q1). vitest 5.0.3 in `systemTest/performance`.
- **#1398 predicted (P4).** `predict --pr 1398 --head 9414aa54… --develop-after 69f2045a… --num-map 23:28`: rc 0, PASS M1 `ce7f6c7bbda2…`. The flow block is re-composed 105 -> 103 lines and the cheat block 66 -> 64, visible text conserved.
  - The kit default num-map gives the same tree.
  - `--num-map 23:23`: rc 1 `develop ALREADY carries 23`.
  - `guard --tree ce7f6c7b…` from `/private/tmp`: rc 0 **(12, 0)**.
  - `mergetree`: rc 1, DIVERGENCE on both docs (1 marker each), 0 paths outside (printed, never picked).
  - `targets --develop-after 69f2045`: REFUSES at T1 ("develop moved a CODE path of #1404": #1404 is already ON develop). This is expected post-#1404, so `targets` is not the instrument now; `predict` is.
  - Hand build (read-tree D + head code blobs + kit blocks inserted VERBATIM before `</body>`) = `ce7f6c7bbda2`. Positive control: the same recipe for #1404 on fa24bdd = `a4a219b87271`. Negative control: `23.` kept = `6db4e4c89353`. `diff D..T` = #1398's 4 paths.
- **Counts for the merge-in tool, measured on T (P5).** `9414..T` **197** paths: 195 non-doc, **2 deletions** (`systemTest/schemathesis/tests/test_billing_idempotency.py`, `test_seed_demo_gate.py`, carried from develop as in #1404). `69f2045..T` **4**. merge-base(9414, 69f2045) = **`d75bfe2deb80`** (NOT develop's previous tip; R 6th's wrong-`--base` lesson). D's parent count is 1, first parent `fa24bdd`.
- **Shared store, read verbs only (P6).**
  - `rev-parse --all` 1,610 lines, sha256/16 `63d58abcdcc5a0b6` before and after the drafter's clone + fetch; `.git/config` `4f624a213933d54b` both readings.
  - `69f2045` ABSENT. Local `feature/ks-1436-…-ra4-6` = M `7849f0a23d06` (RETAINED, VOID). `feature/ks-1136-…-ra3-2` = `9414aa54e92c`.
  - `s-ra3-ks1136`: HEAD `9414aa54`, ATTACHED to that branch, porcelain 0. `s-ra4-ks1436`: HEAD M' `6ea65f64` (detached).
  - 0 `.push-lock-*` (maxdepth 3).
- **PRs 3-5 payloads at `69f2045` (P8).** STRICT apply (temp index): check 0 / apply 0 for all three, trees `52517493279f` / `1b59ec4ae75b` / `66d5c4fa433f`. KS-998 tamper control: rc 1 at `check-package-format.sh:177`. These are NOT your base: RAISE_BASE is after #1398.
- **PR state, GET 00:00:16Z (P9).**
  - #1398: open, `mergeable_state unknown`, head `9414aa54`, title 83, body 7,430 B sha256/16 `aba1d9423478a0b6` (== the gate's), 1 commit, 4 files (+164/+14/+105/+66).
  - #1404: closed merged 23:54:09Z -> `69f2045af2a4`. #1383: open. #1051: merged 2026-09-18 ("Item 1 merged as #1051" HOLDS).
  - 23 open PRs.
- **Linear, read-only, HTTP 200 (P9).**
  - KS-1136 In Progress, board, att `pull/1398` + `pull/1051`. KS-1436 In Progress, 0 comments.
  - **KS-1313 In Progress, UNASSIGNED** (Q-A owed at PR 4 open). KS-998 Backlog. KS-1326 Backlog. KS-1164 In Progress, att `pull/1271` + `pull/1200`.
  - None archived.

## WEDNESDAY RULES (OPEN; the drafter rules none; recommendation given)
- **Q-REBUILD7.** (a) **Recommended:** the BLUF shape, subject `Merge develop 69f2045af2a4 into the KS-1136 branch (docs re-composition)`, 0 trailers, qm Q1-Q6 strict. The branch ref is never moved, so `:145`/`:180` read `$BR == 9414aa54…`. (b) An ATTACHED merge would advance the branch: not proposed.
- **Q-COVER7 (R 6th's five conditions, carried from Q-COVER6).**
  - (1) The head is unchanged: yes.
  - (2) 0 code paths. The docs moved by #1404, the chain the gate predicted. **The 06 pin moved: Wednesday accepts it BY NAME (`4d077ab30259 -> 6bd87f1308d4`, the merge condition itself) or rules a re-gate.**
  - (3) Each delta is on its own GO (gate72, gate71).
  - (4) and (5) are yours.
- **Q-XFER7.** ONE objects-only transfer of D into the shared store, under the lock, `rev-parse --all` byte-identical before and after. R 6th's method was a pack from `D ^fa24bdd` in your clone, then `index-pack --stdin --fix-thin`. Later, ONE more for RAISE_BASE if it is absent.
- **Q-BASE7.** RAISE_BASE = develop by `ls-remote` at the START of A (expected: #1398's squash), named in `STATUS: raise base (Seat R 7th)` and accepted BY NAME. `docblockra3.py`'s `--expect-tail-before` / `--cheat-tail-key` are READ from that base (expected `28` / `KS-1136`).
- **Q-GATE7.** PRs 3-5 go to a FRESH gate, its number named by Wednesday in the ANSWER to your READY (expected gate73; `gatesets/` holds gate72 as the newest).

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **Kam 2026-09-11 16:56 "we approve and merge our own TESTED Platform K work"** (EXPIRING-GRANTS, open-ended) is the merge authority, exercised only through Wednesday's GO.
- **Card `secuura-capped-prs-1245-1278-disposal-1005` = a:** #1245 CLOSED; its ONE pointer comment is owed AFTER PR 4 MERGES, not this round.
- **Card `secuura-advisory-freeze-3-ghsa-1007` = a** (executed as #1406). It authorises NO lock, baseline or manifest edit by you.
- **Kam's /login ~08:4x AEDT:** the 100% row EXPIRED; the 90% stop applies.
- **Ticket rules:** one ticket per TEST PASS (Kam 2026-09-07 13:23, `:86`); new tickets go to OUR board account (`:94`); batch the gates, ONE READY (Kam 2026-09-18 09:22); drive hygiene (Kam 2026-10-05 12:13:55, `:397`).

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **R 6th's round:**
  - Q-REBUILD6 (a); Q-COVER6's five conditions; Q-XFER6; Q-BASE6; Q-GATE6.
  - **`:145` and `:180` re-expressed** (23:05:20Z ANSWER; 23:18Z ANSWER rule 1).
  - **`build_addendum :78-80` reads `ACTIONS VERDICT (Wednesday):` AND the zero-new-failures clause from Wednesday's ADDENDUM mail ONLY** (SPF/DKIM/DMARC checked). R 5th's GO and your own words REFUSE.
  - **`:86` is `SUBJ_LANDS == len(SUBJECT)`, with the `(#` refusal kept** (10:48 ADDENDUM).
  - The Actions method: class 1 has no develop-branch run, so its comparator is sibling heads; accepted.
- **F-3** (the docs guard no-ops under a symlinked `/tmp`): run every kit tool and guard from `/private/tmp`. **F-4 / F-5** namecheck repairs stand in R 6th's copy.
- **gate71 RULINGS (`RULINGS_wednesday.md`, sha256/16 `4b8f2c1e300de84d`):**
  - Q2: #1404 is #1398's merge condition, now MET.
  - Q4: the body per the file the GO names.
  - **W-Q3 VERBATIM** (kit bytes; qm Q2 STRICT).
  - W-Q6: the key-anchored target, merge-tree printed never picked.
  - **W-Q8:** the GO names the REAL post-#1404 develop and its own qm.
  - Q1 / Q3 residue (board search first).
- **Q-N5:** numbers UNIQUE and keyed by ticket; ascending NOT asserted; a collision with develop's at your base is a STOP. **Q-TOOLS5:** every PR-, seat- and gate-keyed constant is a REQUIRED arg with a wrong-value arm before the first run.
- **MG-11 (G 3rd's ANSWER 22:03:31Z; STANDING_LINES `:318` fixed 2026-10-07):** the declared subject IS the landed subject; `len <= 92`; any `(#` is refused; the tools append nothing.
- **Pre-existing-failure rule (gate69 Q5 = gate70 Q1 = gate71 P7):** classes (1) Security Scanning; (2) KS-168 by the failing SET; (3) `pr` stack slot. A `##[group]` positive control on every grep; runs by FULL `head_sha`.
- **Carried from earlier rounds:**
  - Q-BUNDLE one PR per ticket.
  - Q-1326: `Refs KS-1313` hyphenated, KS 1326 de-hyphenated.
  - **Q-A:** assign KS-1313 to `kamil.kreiser@secuura.ai` at PR 4 open, read before and after.
  - Q-TIER T2.
  - Q-SRC2: raise from `out.md.checker/patch.diff`.
  - **F-1:** PR 3's suite lands 100644, said so in its body.
  - Q-F: no fetch in the shared checkout.

## THE PROJECT'S RULES (quote each again from your base at ITEM 0, with blob ids)
- Skill `.claude/skills/secuura-test-discipline/SKILL.md` blob `b59b74a592e9`:
  - §4 both docs in the same commit;
  - §5b red then green;
  - §5c systemTest files < 400 lines;
  - §5d WHY + ticket on every changed line;
  - §5f `live sweep owed`;
  - §6e LTS (node v24.7.0 vs engines `>=24.11.0`: state the gap).
- `systemTest/CLAUDE.md` MUST 1, 2, 3, 7, 8. No `Co-Authored-By`, no tool trailer. `.githooks/pre-push` refuses a non-fast-forward.

## THE PARTITION AND THE LOCK
| Seat | Pane | Token / lock | Yours to write |
|---|---|---|---|
| **R 7th (you)** | `Secuura/Blockchain-R` | `ra7` / `.push-lock-d8` | ON A GO ONLY: ONE merge-in M' + squash of #1398 (ADOPTED `s-ra3-ks1136`); after B: NEW `s-ra7-ks998`, `s-ra7-ks1313`, `s-ra7-ks1164` |
| R 6th (WRAPPED ~00:0xZ) / R 5th / R 4th / R 3rd | same pane | `ra6`-`ra3` | NEVER: M `7849f0a23d06` + its branch ref; `s-ra4-ks1436` (detached at M') |
| D 14th (DEPLOYED 23:56:48Z; live state NOT read by the drafter) | `Secuura/Blockchain-D` | `d14` | none; never its clone, pane, mail, records or demo |
| G 3rd (WRAPPED) / B / E / F | `-G`, base, `-E`, `-F` | `.push-lock-g1` / `-56` / `-e4` / `-f3` (WAIT) | none; `s-g3-advlock` FOREIGN |
- **`lockra1.sh` takes `.push-lock-d8`** with `LOCK_SEAT='Secuura/Blockchain-R ra7'`. A holder `…-R ra6` (or `ra1`-`ra5`) is FOREIGN: rc 12, decided by the holder's `seat` field.
- Every ref write needs the lock HELD by you. **Push tools take the lock ITSELF: call them BARE.** Never hold it across `npm ci`, a build or a suite.
- Run lock ARMS from a scratch COPY (`.my-last-release` lands beside the script).
- **Take and release in ONE invocation** (R 6th: a release from a later Bash call is refused).

## TOOLS (copy R 6th's `raise/` into YOUR record folder's `raise/`; hash each into `_COPY_HASHES_ra7.txt`; `cmp` each; NOT `__pycache__`, `*.pre-*`, push records, `.my-last-release`)
- **R 6th's copies, sha256/16 (P11):** `mergeinra6_1404.sh` `b87a619f0ef042e3`, `build_addendumra6_1404.py` `72a09e3fe4b65b0b`, `mergera1.py` `aaf230e7d1975213`, `pushra1_ff.sh` `dd8b1083a37fb82d`, `inbox_matchra1.py` `4428c51d2937a993`, `namecheckra1.py` `93747f6c7d76c635`, `lockra1.sh` `a3ea5618e62d713c`, `pushra1.sh` `9c8387cd0c8bebf9`, `twolockra1.sh` `0a7a828e44461ba3`, `inbox_watchra1.sh` `e50b6448c89ec292`, `docblockra3.py` `c4827645b53bce19`, `commitra3.sh` `f1357d1a956984fb`.
- **THE #1398 MERGE SET.** `mergeinra7_1398.sh` is copied from `mergeinra6_1404.sh` (the original stays pristine). Required args:
  - `--wt` `s-ra3-ks1136`, `--br` the ks-1136 branch, `--ours 9414aa54…`;
  - `--dev` D, `--dev-parent fa24bdd…`, **`--dev-parent-count 1`**, **`--base d75bfe2deb80…` (the COMPUTED merge-base)**;
  - `--predicted-tree` T; `--flow-blob` / `--cheat-blob` the GO's;
  - **`--m-retain 9414aa54…`**; `--lock-seat …ra7`; `--my-ref-ns seatra7`; `--own-key KS-1136`;
  - `--head-paths` the TWO code paths;
  - `--dev-paths` the non-doc paths develop's advance must keep: the drafter expects the 7 non-doc paths of `b3905..D`. Re-derive this by the tool's own meaning (R 6th's wrong-input lesson);
  - **`--expect-ours-paths` / `--expect-dev-paths` re-measured on M'** (drafter's expectation: 197 and 4);
  - `--control-commit bf277eead268`; `--subj` the GO's merge-in subject.
  STALE values (D `fa24bdd`, 195, `--m-retain 7849f0a2`, `KS-1436`) must REFUSE.
- `build_addendumra7_1398.py`, copied from R 6th's: re-key `RA6_` -> `RA7_`, point it at YOUR GO and Wednesday's #1398 ADDENDUM, and keep `:78-80` and `:86` AS R 6th re-expressed them.
  - Arms: R 6th's real #1404 GO REFUSES (wrong seat/PR/D); this GO without the ADDENDUM REFUSES (its Actions line is a placeholder); your own classification typed without Wednesday's prefix REFUSES; a GO declaring `LANDS 91` REFUSES.
  - `RA7_EXPECT_PATHS 4`, `RA7_MODE_CENSUS` MEASURED from T (drafter: `{100644:3, 100755:1}`), `RA7_WRAP` RELATIVE (`:141` joins it to `5_Project_History/`).
  - **Fix what it PRINTS, not only what it asserts** (R 6th's item 10).
- `mergera1.py`: `--scratch` REQUIRED, `--seat 'Seat R 7th'`, `--gate gate71`, `--go-ts`, `--expect-develop`; ONE `Merged by`; MG-11 untouched.
- `pushra1_ff.sh` positionals `WT TARGET EXPECT`; run `FF_DRYPROOF=1` first.
- **Tool defects to sweep for:** `mergein :31` hardcoded `REPO=` (correct here; it is why M-0 precedes M-2); the base-mismatch line prints the CLAIMED base, not the computed one. **Add a bare-project-path pattern to THE SWEEP.**
- 🔴 **THE SWEEP before ANY first run** (`:405`, `:418`, `:391`):
  - foreign-seat literals and bounded `ra[1-6]`;
  - lock names, `refs/seat*/`, `LOCK_SEAT=`, `*_SCRATCH`;
  - other seats' absolute paths;
  - every live 12+-hex constant, UNBOUNDED (`fa24bddedf3b`, `c117c0160684`, `a4a219b87271`, `6ea65f64e639`, `7849f0a23d06` must not survive as live defaults);
  - every literal count.
  Print `N checked` per tool; `0 checked` is a FAIL. A hit is a STOP-and-mail or a REQUIRED arg with a wrong-value arm.
- **Positive control FIRST, every time.** An arm that returns the same rc as the all-correct control was not reached, so it is not passed (R 6th's items 7-8).

## ITEM 0 — read-only; plan confirmation (QUESTION `plan confirmation (Seat R 7th)`). STOP until Wednesday's ANSWER
Before the ANSWER, NONE of: lock, transfer, worktree change, ref write, install, ticket write, comment, PR edit. You MAY write in your record folder and YOUR scratch clone (`git clone --shared --no-checkout`; fetch BY FULL SHA from the GitHub URL with `env -u GIT_SSH_COMMAND`, `-c core.sshCommand=…`, `--no-tags --no-write-fetch-head`; `cat-file -t` + deadbeef control; shared `rev-parse --all` and `.git/config` identical before/after).
- **(a)** `ls-remote` (the checkout's own sshCommand, `GIT_SSH_COMMAND` unset): develop, `refs/pull/{1383,1398,1404}/head`, the ks-1136 branch, `feature/ks-{998,1313,1164}*`, highest `refs/pull`, the time.
- **(b)** Disjointness, `fa24bdd..develop-now` AND `b3905..develop-now`, intersected with #1398's and PRs 3-5's paths and with the kit tooling pins. Plant a positive control. A move past `69f2045`: list it by first-parent PR; anything touching the sets is a STOP.
- **(c)** `python3 -I -B <kit>/c4_docs_gate71.py predict --repo <your vclone> --pr 1398 --head 9414aa54e92ca243565d0d967aad991dc4c13840 --develop-after <develop, 40-hex> --num-map 23:28`.
  - Expected T `ce7f6c7bbda2…`, plus the `23:23` arm and `guard --tree T --out <fresh /private/tmp dir>` (12, 0).
  - Your own hand build must agree, with both controls.
  - MODE goes as `argv[1]`. Run with `-B` and confirm 0 `__pycache__` in the kit after.
- **(d)** Q-COVER7: the five conditions, each with its reading; name the 06 pin.
- **(e)** Payloads: three STRICT applies at develop-now + the tamper control; vitest version.
- **(f)** The guard on develop's docs (0 findings) and on a planted `<p>` (must report). Both runs from `/private/tmp`.
- **(g)** Shared store:
  - `cat-file -t` D / M / deadbeef;
  - `rev-parse --all` count + sha256/16, two readings;
  - the branch refs;
  - `s-ra3-ks1136` HEAD (`rev-parse --abbrev-ref HEAD` + porcelain; read verbs only);
  - locks by holder `seat`, two polls, with a planted control (`<lock>/holder`, F-4).
- **(h)** Linear (KS-1136, KS-998, KS-1313, KS-1326, KS-1164) and PR GETs (#1398, #1383): state, `mergeable_state`, body sha256/16. Name each contradiction.
- **(i)** Tool block `ra7 on d8: 56 + e4 + f3 + g1 WAIT, 16 STOP, catch-all, foreign-holder rc 12, DEFECT_A 2x2 (Seat R 7th)`:
  - copy receipt; THE SWEEP; re-key receipts with REAL subjects;
  - R 6th's WRAP and its `GO (Seat R 6th): merge 1404 on gate71` read FOREIGN, and so do D 14th's;
  - your brief reads FOR ME;
  - `(Seat R 8th)` reads NOT FOR ME; `(Seat R 19th)` exercises `_addr is None`;
  - DEFECT_A has ONE FOR-ME cell;
  - the merge set's omit- and wrong-value arms; `twolockra1.sh` arms; the `:414` equality BY ROLE.
- **(j)** Handovers re-hashed: R 6th's (209 lines, 16,907 B, `7bc86aab5da1773a`) and R 3rd's (235 / 18,818 / `35ad164280e587d5`, the #1398 merge_note's authority).
- **(k)** Seat identity: `$TMUX_PANE`, then `tmux display-message -t "$TMUX_PANE" -p '#{@cockpit_name}'` (never bare; R 6th's item 1).
  Also:
  - the watcher pid from a ps FILE;
  - `df -m /Volumes/DevMASTER`;
  - launcher warnings VERBATIM;
  - `WED_USAGE_STOP` as read;
  - refuse the step-1 pull, with `FETCH_HEAD` unmoved;
  - your restatement of Q-REBUILD7 / Q-COVER7 / Q-XFER7 / Q-BASE7 / Q-GATE7.
- **(l) OPTIONAL, after B and only if ctx allows: F-3.** Board search (symbols `html_docs_check.mjs`, `import.meta.url`). If 0 hits, file ONE ticket on the board account with both runs + the nine controls; otherwise name it in your handover. Do not fix it.

## QUEUE
**B. #1398 (ITEM M2), only on `GO (Seat R 7th): merge 1398 on gate71`.**
- **The GO carries** (missing any = INCOMPLETE, ask): D; the head; T; the two doc blobs; the kit's two composed doc files; the merge-in subject; the declared squash subject (83, lands 83); the body file + sha256; the verdict line; the `merge_note` (`HANDOVER-seatR3-2026-10-06.md sha256 35ad164280e587d5`).
- **The Actions verdict comes in a SEPARATE ADDENDUM**, after your push; it releases M-4.
- **M-0 objects.** Q-XFER7 under the lock; `cat-file -t D` -> commit; `rev-parse --all` byte-identical.
- **M-1 second hand, in your clone.**
  - `hash-object` each composed file == the GO's blobs;
  - T rebuilt == the GO's T;
  - the guard on both docs: 0 findings;
  - flow numbers UNIQUE, and every D block byte-present.
  A mismatch is a STOP + `QUESTION: merge-in 1398 target tree (Seat R 7th)`.
- **M-2 merge-in, under the lock.** In `s-ra3-ks1136` (porcelain 0, HEAD == `9414aa54` read first): `git switch --detach 9414aa54…`, then `mergeinra7_1398.sh`.
  - Expect rc 1, exactly two docs conflicted, the STAGED blobs asserted, 0 markers, 0 trailers vs a non-empty control.
  - **tree(M') == T; parents `[9414aa54…, D]`; branch ref still `9414aa54…`.**
  - Then `qm --pr 1398 --head 9414aa54… --merge-in-head <M'> --develop-after <D> --out <fresh /private/tmp dir>`: Q1-Q6 PASS, run in YOUR clone (the tool refuses the shared checkout).
  - Record any first-run failure exactly; never round it.
- **M-3 push M'.** Outside the lock: `npm ci --ignore-scripts` in `Blockchain/Dev` + `npm run build --workspace=packages/shared`; ASSERT `dist/index.js`; DRY read of legs 6/7.
  - Then `env -u GIT_SSH_COMMAND LOCK_SEAT='Secuura/Blockchain-R ra7' bash <REC>/raise/pushra1_ff.sh /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-ra3-ks1136 feature/ks-1136-aggregate-unreadable-artefacts-ra3-2 9414aa54e92ca243565d0d967aad991dc4c13840` (FF_DRYPROOF=1 first).
  - Read the result from `.rc` + `ls-remote`. Quote PREFLIGHT, legs 6/7 and `html_docs_matrix` EXACTLY. Shell suites expected `(of 70)`: develop's 69 + ks1136.
  - `PREFLIGHT FAILED` is a STOP. Rc 141 with the ref unmoved: retry under the lock, report the attempts.
  - Then the Actions on M' by full `head_sha`, classified, PENDING waited out over two agreeing polls. Mail the evidence; WAIT for the ADDENDUM.
- **M-4 squash (GO + ADDENDUM, M' at origin).**
  - The builder's targets == `GET /pulls/1398/files` (4). `no_trailer: true`. `body_verbatim` = the GO's file, re-hashed.
  - `mergera1.py --dry` first, and READ the `.DRY` body: ONE `Merged by`, 0 trailers, subject byte-equal, `(#` absent.
  - Merge with the head PINNED to M'.
  - Verify by `ls-remote` + API: tree == T, ONE parent == D, 0 trailers, landed == declared (83), exactly 4 paths. KS-1136 still In Progress.
- **M-5.** Mail `STATUS: merged 1398 (Seat R 7th)`. A §5f comment only with Wednesday's text.

**A. THE RAISE TRACK (after B, ctx < 45%; one PR at a time; ticket order).** R 5th's brief ITEMs R3-R5 stand (`2026-10-07_seatR5_raise_prs3to5_and_merge_gate71.md` `:131`-`:144`), with:
- RAISE_BASE per Q-BASE7: `git worktree add --detach …/worktrees/s-ra7-ks<n> <RAISE_BASE>` under the lock, never `-b`.
- Branches `feature/ks-998-format-gate-push-label-literal-ra7-3`, `…ks-1313-child-verdict-json-reporter-ra7-4`, `…ks-1164-breakdown-counts-locale-grouped-ra7-5`.
- PR 4's REAL vitest 5.0.3 JSON compared field by field with the 4.1.9 fixtures (a difference is a STOP).
- **Q-A at PR 4 open.** `pushra1.sh` BARE.
- READY: `READY FOR QA (Seat R 7th): #<a> (KS-998) + #<b> (KS-1313) + #<c> (KS-1164) -> gate<N>`, naming every unraised row as UNRAISED.

## PR BODIES / HOLDS
- PR bodies:
  - the own key hyphenated ONCE, every other key de-hyphenated;
  - Test Evidence names node v24.7.0 / npm 11.5.1 / vitest 5.0.3;
  - "Raised from a Wednesday-held Spark pass (PASS 7/7), re-proved by Seat R 7th on develop `<12-hex>`";
  - a closing-regex scan of 0, with a firing control;
  - written from QUOTED heredocs.
- **No merge without the exact GO subject.** No commit on #1398 but the ONE merge-in. **Never write `refs/heads/develop` or `refs/remotes/origin/develop` in the shared checkout; never move or delete M's branch ref or the ks-1136 branch ref.**
- Forbidden, always:
  - deploy, `az`, SSH, migrations, Docker;
  - comments to Peter or Stuart; the extranet; #1245;
  - **`--no-verify`, force push, `-u`, `--admin`, `push --dry-run`**;
  - `git fetch` in the shared checkout;
  - `GIT_SSH_COMMAND` set for any network verb;
  - any dependency / lock / manifest / baseline / spec edit;
  - deleting anything (quarantine instead);
  - touching #1383, another lane's worktree/branch/lock, or any gate kit or report (`-B`, `--repo` = your clone, `--out` = your scratch).
- Signature classes pause for Kam: production · money · external communication · anything irreversible.
- Never `cd`. Absolute paths; `TZ=UTC stat`; `-z` for paths (`Projects Documents/` has a SPACE); rc on its own line, never through a pipe; macOS has no `timeout`.
- **One inbox** (`secuura-blockchain@agentmail.to`): act only on mail whose subject carries `-R` AND `(Seat R 7th)`. A new mail from `kreiser.org@me.com` = STOP and mail Wednesday.

## THE GO (verbatim; nothing else authorises a merge)
The subject comes from `wednesday-agent@agentmail.to`, DKIM pass, EXACTLY: `[Wednesday -> Secuura/Blockchain-R] GO (Seat R 7th): merge 1398 on gate71`. It is followed, before M-4, by an ADDENDUM from Wednesday naming the same GO and carrying `ACTIONS VERDICT (Wednesday):`. The declared subject is `KS-1136: report a present but unparseable security artefact instead of a clean scan` (83, lands 83).

## MAIL FORMATS (to `wednesday-agent@agentmail.to`, prefix `[Secuura/Blockchain-R -> Wednesday] `; every subject names `(Seat R 7th)`)
- `QUESTION: plan confirmation | ctx read | <topic> (Seat R 7th)`, one question per mail. `STATUS: <item> (Seat R 7th)`, `STATUS: merged 1398 (Seat R 7th)`, `STATUS: raise base (Seat R 7th)`, each with the LIVE watcher pid. `READY FOR QA (Seat R 7th): … -> gate<N>`.
- `WRAP (Seat R 7th): …` carries:
  - the ps file;
  - the handover `5_Project_History/HANDOVER-seatR7-<date>.md` (sha256/16, `wc -c`), opening "FOR R 8th, THE FIRST THREE THINGS";
  - the history entry at the TOP of `history.md`, re-read immediately before writing;
  - UNRAISED / UNMEASURED / UNMERGED;
  - `df -m`; mail counts COUNTED;
  - "this seat = 1 Claude launch, clause cloud: merge + raise (carrying N Spark tasks)".
  Record folder: `5_Project_History/<UTC boot date>_seatR-7th/`.

## UNMEASURED (with why, and the instrument that closes it)
- M', its qm, legs 6/7 on it, its Actions: none exists. Closed by M-2 / M-3 and by Wednesday's ADDENDUM.
- Whether #1383 (or anything) moves develop before the GO or the squash: `ls-remote` in the same action as each ref decision.
- **Whether the gate71 verdict still COVERS #1398 with the 06 pin moved:** Wednesday's Q-COVER7 (2) ruling.
- `mergeable_state` of #1398 (`unknown` at 00:00:16Z): re-GET at the GO.
- The live state of D 14th (no tmux read by the drafter): Wednesday's pickup.
- PRs 3-5 at RAISE_BASE, every suite figure, and vitest 5.0.3 vs the KS-1313 fixtures: your worktrees.
- The drafter's `--dev-paths` expectation (7) is an inference about the tool's meaning: you re-derive it.

PROVENANCE:
- P1 refs as listed | `env -u GIT_SSH_COMMAND git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" -c core.sshCommand=<its own> ls-remote git@github.com:Secuura/Distributed_Secuura.git` 23:58:07Z-23:58:13Z rc 0, 2,104 lines (scratchpad `r7/lsr1.out`) | read 2026-10-07
- P2 69f2045 tree/parent/subject/4 paths; b3905..69f2045 9 paths; 06 blob 6bd87f1308d4; skill b59b74a5; vitest 5.0.3 | `git log -1 --format`, `git diff --name-status`, `ls-tree` in the drafter's scratch clone `…/0e6aaa67-…/scratchpad/vclone` after a by-SHA fetch rc 0; kit.json `rows.1398.tooling_paths_unchanged` | read 2026-10-07
- P3 #1383 not held; D 14th DEPLOYED 23:56:48Z | `5_Project_History/HANDOVER-seatR6-2026-10-06.md` `:7`-`:15`; `briefs_staged/2026-10-07_seatR6_WRAP.txt` | read 2026-10-07
- P4 T ce7f6c7bbda2…, arms, guard (12,0), mergetree, targets refusal, hand build + controls | `python3 -I -B /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate71/c4_docs_gate71.py {predict,guard,mergetree,targets}` (outputs `scratchpad/r7/c4_*.out`); `scratchpad/r7/handbuild.py`; 0 `__pycache__` in the kit after | read 2026-10-07
- P5 197/195/2 deletions, 4, merge-base d75bfe2deb80, D parent count 1 | `git diff -z --name-only`, `--name-status`, `merge-base` in the vclone | read 2026-10-07
- P6 shared store as listed | `git -C <checkout> rev-parse --all | shasum`, `cat-file -t`, `rev-parse refs/heads/…`, `git -C <worktree> rev-parse HEAD / --abbrev-ref HEAD / status --porcelain`, `find -name '.push-lock-*'` | read 2026-10-07
- P7 1398_squash_body.txt 7,647 B sha256 1a0da357… | `shasum -a 256`, `wc -c` on the kit file; built by `scratchpad/r7/build_body.py` from the GET body | read 2026-10-07
- P8 payload strict applies at 69f2045 | `scratchpad/r7/payloads7.sh` over `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_*/out.md.checker/patch.diff` | read 2026-10-07
- P9 PR + Linear reads | `scratchpad/r7/reads7.py` (GET api.github.com …/pulls/{1398,1404,1383,1051}, …/files, …/commits; Linear GraphQL), GH_TOKEN / LINEAR_API_KEY by name from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, never printed; 00:00:16Z | read 2026-10-07
- P10 history.md "R 7th" x2 (R 6th's entry, `:29`, `:39`) | `/usr/bin/grep -c -i` / `-n` on `5_Project_History/history.md` | read 2026-10-07
- P11 R 6th tool hashes; gate sites :145/:180/:78-80/:86; --m-retain arg | `shasum -a 256`, `sed -n`, `grep -n` on `5_Project_History/2026-10-06_seatR-6th/raise/`; HANDOVER-seatR6 §"THE THREE GATE RE-EXPRESSIONS" | read 2026-10-07
- KS-1136 (#1398), KS-1436 (#1404), KS-998 / KS-1313 / KS-1326 / KS-1164 (PRs 3-5): state and assignee as listed | P9 (Linear issue reads, HTTP 200) | read 2026-10-07
SELF-CHECK: re-read end-to-end for contradictions; GO field formats parsed by R 6th's builder regexes | 2026-10-07 11:1x AEDT
