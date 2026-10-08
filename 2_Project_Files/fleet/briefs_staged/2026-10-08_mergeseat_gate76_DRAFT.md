LAUNCH BRIEF (Seat R 20th): successor of Seat R 19th on pane `Secuura/Blockchain-R`. **A MERGE SEAT for TWO PRs, ONE AT A TIME, each ONLY on its own GO: #1428 (KS-593) FIRST, then #1427 (KS-1274)**, which land only on gate76's verdicts and then Wednesday's GOs. Nothing deploys. Secuura NEVER force-pushes. **This seat pushes exactly ONE thing: the docs-only keep-both merge-in commit M on #1427's branch, through the hook, BARE.** Both squashes are API calls. cloud: merge (carrying 0 Spark tasks). **No raise work in this seat** unless Wednesday adds it after the second squash.

# LAUNCH BRIEF: Seat R 20th, Secuura/Blockchain, lane R (pane `Secuura/Blockchain-R`). From Wednesday.
DRAFT: staged by Wednesday's gate76 kit drafter, 2026-10-08 ~19:1x AEDT (08:1xZ). NOT sent, NOT launched. Every RULINGS item marked OPEN in `fleet/qa-agent/gatesets/2026-10-08_gate76/RULINGS_wednesday.md` must be ruled (or its default accepted) before this is sent; this draft assumes every DEFAULT. **Q-SEAT76 default = Seat R 20th, launched only after Seat R 19th (a RAISE seat, live at draft) has WRAPPED.** If Wednesday picks another seat, every `R 20th` / `ra20` below is re-keyed by her at send. Every figure here is the drafter's PREDICTION; you re-measure.

## USAGE AUTHORITY
- The weekly gauge read **91%** (07:27:47Z) and **93%** (08:02Z) during the draft.
- Launch with `WED_USAGE_STOP=100` on Kam's new-account grant: `0_Brain/learnings/2026-10-08_new-account-push-merge-test-as-much-as-possible.md` (status: live, card `secuura-raise-backlog-at-99pct-1008` = a). Clause: **MERGE**.
- Expiry is an EVENT: the account's allowance renewal (~Fri 9 Oct morning), an account switch, or Kam's word. Never inferred.
- Be economical: two squashes, one merge-in, no comment, WRAP.

## BLUF
- **Seat number derived, not counted:** R 19th's handover opens "FOR R 20th, THE FIRST THREE THINGS" (`5_Project_History/HANDOVER-seatR19-2026-10-08.md`; NOT WRITTEN at draft: Wednesday names its line count and sha256/16 at send). Its forward-add of `"r 20th"` into `OTHER_SEATS` is YOUR trap (FIRST THREE THINGS below).
- **develop at draft = `0a6177ea5482227e83d5045b68b8577a56326ffc`** (the #1426 squash, R 17th; its tree `5f456a0128fe` IS gate75's predicted squash tree). Read with `ls-remote` by the drafter at 07:28:27Z and 08:02:16Z, unmoved. **It will move:** #1429 (KS-1449, E 11th), #1430 (KS 1328, F 5th) and #1383 (KS-1401, held) all edit both platform docs, and R 19th / G 5th will raise more. Re-read develop before EVERY ref decision.
- **#1428 KS-593 (Seat G 4th, the AUTHOR; never named in a GO):** head `64eafead891e81f5adb4e46aaa94ff6a6ace1998`, branch `feature/ks-593-not-a-server-error-originate-three-passes-g4-1`, END_TREE `7f6e6fe0ca15702cab1b5e1a0d37ba7ff8f665b5`, ONE parent == develop. 9 paths +421/-4. **Lands FIRST, NO merge-in:** squash tree == END_TREE while develop is unmoved (gate76 kit `c4_docs_gate76.py chain`, step 1).
- **#1427 KS-1274 (Seat R 18th, the AUTHOR; never named in a GO):** head `2b6da5f561b05a820bbe1ab5e891bff9f4f531c8`, branch `feature/ks-1274-trivy-bare-object-guard-ra18-1`, END_TREE `9b6c3dfef865dfc35b05d4da8fcad7e24249fbb1`, ONE parent == develop. 6 paths +94/-8. **Lands SECOND, with ONE docs-only KEEP-BOTH merge-in M** (the two PRs append to the same doc tail: `merge-tree` of the two heads reads rc 1 on exactly the two docs). Predicted at develop `0a6177ea5482`: M's tree `57c9b5eaec95ddc86a7d139f9f2d957015a3fd97`, its two doc blobs flow `b2bd07dbae400c0ad15b89046a65967a117e1a15` / cheat `f4503e99d43e8a90ffe881291295695e7cd61ae1`, in `gatesets/2026-10-08_gate76/composed_2026-10-08/` (the `2_1427_*` files). **The real develop after #1428's squash is NOT the kit's SIM commit: re-run `chain` on it (M-1); the tree is predicted to be identical if nothing else lands in between.**
- 🔴 **THE KS-593 RESIDUE (Wednesday's commission, RULINGS Q-CLOSE593).** #1428's PUSHED commit message contains `NARROWING: this does not close KS-593.` A closing-keyword parser matches the adjacency `close KS-593`; the negation is not something to assume it understands. Secuura never force-pushes, so it stays on the branch. Therefore:
  - the squash commit message is the GO's declared subject + the GO-named body file ONLY, never GitHub's default concatenation of the branch messages; the composed body carries **0** closing adjacency under BOTH regexes (the kit's and the builder's broader `CLOSING`, which DOES catch `close KS-593` inside the negation: drafter's probe P6, `AssertionError: closing word before a key: [('close', '', 'KS-593')]`);
  - you READ KS-593's Linear state immediately BEFORE and AFTER the squash (state, and the PR attachment's link kind: G 4th measured `linkKind = 'contributes'`, `status = 'open'`). **If KS-593 walks to Done: STOP and mail `STATUS: KS-593 walked (Seat R 20th)` with both reads. Never move it back yourself** (no ticket state change is yours); Wednesday restores it.
- **THE TOOL CHAIN IS THE REAL WORK, and R 17th's builder cannot land the SECOND row (measured: RULINGS Q-BUILDER76).** It lands #1428 as is (`on-develop` + `DOCS=head`, probe rc 0) but its `merge-in` mode is UNREACHABLE: R 15th's by-SHA read makes it assert a commit is its own parent. You write a NEW COPY (spec below).
- **Both branch commits carry 0 trailers** (1 raw byte against the 55-byte control `bf277eead268`) and 0 Co-Authored-By. What LANDS must carry 0 trailers and 0 attribution lines: assert the SENT body and the LANDED commit (STANDING_LINES :371).
- **Neither ticket moves to Done** (§5f: both are runtime changes and both seats say a LIVE run is OWED; RULINGS Q-LIVE76). You post NO ticket comment: item 3 for both PRs is Wednesday's batch (Q-NOTIFY12).
- **Budget by MAIL HANDSHAKE.** Mail `QUESTION: ctx read (Seat R 20th)` before each squash and before the merge-in. **HARD CEILING 65%:** at that reading, WRAP COLD at the next safe boundary, naming the GO you hold.
- **Never end a turn on a "next up" line with nothing running** (STANDING_LINES :339).

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** 🔴 **Where your copy of a tool and this brief disagree about a gate, a knob or a line number, THE TOOL WINS.** Run nothing on the disputed point, and tell Wednesday what the tool says.

**WAKE:** your re-keyed `inbox_watchra1.sh`, armed in the background at boot with `timeout: 7200000`. It EXITS when it fires: re-arm it IN THE SAME ACTION that reads each mail, `SINCE` = the newest mail you have READ (STANDING_LINES :400). After each squash and after the push, LIST the inbox by API before the next ref write. Name a watcher pid only from a `ps` FILE read immediately before. Stop every watcher before your WRAP and prove 0 live with a positive control.

## FOR R 20th, THE FIRST THREE THINGS
Wednesday copies them from R 19th's handover at send. The drafter's EXPECTATIONS, from R 18th's handover and R 19th's brief (`2026-10-08_seatR19_raise_r3r5_ks1410_ks1139.md:27-28`), to be checked against R 19th's real tools:
1. 🔴 **R 19th's forward-add is YOUR trap:** the parsed `OTHER_SEATS` of R 19th's `inbox_matchra1.py` should contain `"r 20th"`/`"seat r 20th"` (R 19th's brief told it to forward-add them). REMOVE them FIRST; ADD `"r 19th"`/`"seat r 19th"`; FORWARD-ADD `"r 21st"`/`"seat r 21st"`; set `MINE` to `"r 20th"` (DOUBLE quotes preserved). Edit by byte span from the AST, never re-render the list; prove it by IMPORT with full-length real subjects through both files (the R-lane rows invert).
2. 🔴 **The sweep ordinal class inverts again.** R 19th's class should be `(?:[1-9]|1[0-8])` (matches 1-18, not 19): wrong for you (it does not match 19, a predecessor, and it is correct about 20 only by accident). Your class must match 1-19 and NOT 20: `(?:[1-9]|1[0-9])`, applied to two-digit ordinals with `20` excluded. Prove it on the PARSED patterns with per-row wants as DATA and an inverted-want control; count with `grep -o | wc -l`, never `grep -c`.
3. 🔴 **R 17th's builder's merge-in mode is dead (Q-BUILDER76), and R 12th's merge-in tool is the last one that ran** (`mergeinra12_gate73.sh` `253cf72c27b26f2b`, 312 lines, at R 12th's `raise/`; it lands M with parents `[head, develop]` read separately). Copy both, never edit the originals.

## THE PARTITION
| Seat | Pane | Token / lock | Writes | Never |
|---|---|---|---|---|
| **R 20th (you)** | `Secuura/Blockchain-R` | `ra20` / `.push-lock-d8` (`LOCK_SEAT='Secuura/Blockchain-R ra20'`) | ON THE GOs ONLY: ONE API squash of #1428; ONE merge-in commit M on `feature/ks-1274-trivy-bare-object-guard-ra18-1` (the branch NAME adopted for that one push, gate73 Q-ADOPT10 (a) precedent) in a FRESH detached `s-ra20-m1427`; its push; ONE API squash of #1427; ONE objects-only transfer into the shared store; your record folder | any other push, branch or raise; any ticket write or comment; `s-ra18-ks1274`, `s-g4-ks593` |
| R 19th (WRAPPED before you launch) and R 3rd-R 18th | your pane | `ra19`-`ra3` | nothing | their worktrees; report them in your WRAP |
| G 5th / E 11th / F 5th (if live) | `-G`, `-E`, `-F` | their locks (WAIT) | — | #1429, #1430, #1383 and every other PR: never merged by you |
| QA gate76 | `QA/Secuura-gate76` | none | its own report dir | never its kit, report, pane or mail |

## ITEM 0 — BOUNDED, read-only; then `QUESTION: plan confirmation (Seat R 20th)` and WAIT
Before the ANSWER, do NONE of these: lock take; worktree add; ref write; objects transfer; install; PR edit; ticket write; comment. The launcher's boot pull (sole seat) is the one recorded exception (STANDING_LINES :433): RECORD it.
Measure:
- **(a) Refs, one `ls-remote`:** develop; `refs/pull/{1427,1428,1383,1429,1430}/head`; both branches; any `-ra20-` ref (expect 0, with `-ra13-` = 2 as the control); `date -u`. A moved head = STOP and mail. A moved develop is NOT a STOP: name it and re-predict (b).
- **(b) The kit, re-hashed and run from YOUR clone** (`clone --shared --no-checkout`, origin = the GitHub URL, STANDING_LINES :407): `gatesets/2026-10-08_gate76/` `KIT_REPORT.md`, `RULINGS_wednesday.md`, kit.json `script_sha256` (12 pins). Run `c4_docs_gate76.py --selftest --repo <clone> --heads 1427=<h>,1428=<h>` (drafter 15/15), `c4_docs_gate76.py chain --repo <clone> --order 1428,1427 --develop <develop read now> --heads 1427=2b6da5f561b05a820bbe1ab5e891bff9f4f531c8,1428=64eafead891e81f5adb4e46aaa94ff6a6ace1998 --out <fresh dir>` (drafter: step 1 `7f6e6fe0ca15`, step 2 `57c9b5eaec95`, guard 12/0 both, ALL OK) and `cmp` its step-2 docs with the kit's `composed_2026-10-08/2_1427_composed_*`. The kit's lib refuses a write verb under `!CODING`, so `--repo` is always YOUR clone.
- **(c) Tools:** the copy receipt (TOOLS); THE SWEEP; the re-key; membership BY IMPORT; the builder spec read line by line.
- **(d) The shared store, read verbs only:** `rev-parse --all` count + sha256/16; `cat-file -e` of develop and both heads with a POSITIVE control at the same moment (R 18th: `rev-parse --verify` is not a presence check); locks by holder `seat`, two polls, planted control.
- **(e) Seat facts:** `$TMUX_PANE` -> `tmux display-message -t "$TMUX_PANE" -p '#{@cockpit_name}'`; the watcher pid from a ps FILE; `df -m /Volumes/DevMASTER`; every launcher preflight warning VERBATIM; both author handovers re-hashed (`HANDOVER-seatG4-2026-10-08.md` sha256/16 `d1e6b9e0f75235cf`, `HANDOVER-seatR18-2026-10-08.md` `1081ef422c811c0d`: the merge-note artefacts).
- **(f) Linear, read-only:** KS-593 and KS-1274 (state, assignee, newest comment, and each PR attachment's link kind), the fabricated-key control in ITS OWN query.
**Your plan confirmation carries:** (a)-(f), one block each; your builder spec as you will build it; the launcher lines VERBATIM; a ctx-read request. **Budget: mailed by ~25% ctx.**

## TOOLS
**Copy** from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/` into YOUR record folder; hash each into `_COPY_HASHES_ra20.txt` and `cmp` it. **Expected** (the drafter's `shasum -a 256 | cut -c1-16`, 2026-10-08 ~08:0xZ):

| tool | from | sha256/16 | lines |
|---|---|---|---|
| `mergera1.py` | R 17th `merge/` | `aaf230e7d1975213` | 604 |
| `build_addendumra17_gate75.py` | R 17th `merge/` | `04ed62b4ff18b3d3` | 386 |
| `provenance_ra17.py` | R 17th `merge/` | `d215ce0275a6e3f9` | 91 |
| `m7_squashra17.sh` | R 17th `boot/` | `c481b0ef18d7571b` | 89 |
| `m1_go_completera17.py` | R 17th `boot/` | `6041d71c0ad057a9` | 135 |
| `mergeinra12_gate73.sh` | R 12th `raise/` | `253cf72c27b26f2b` | 312 |
| `pushra1_ff.sh` | R 12th `raise/` | `dd8b1083a37fb82d` | 128 |
| R 19th's `tools/` (`inbox_matchra1.py`, `inbox_watchra1.sh`, `sweepra19.py`, `lockra1.sh`, `provenance_ra19.py`, …) | R 19th | Wednesday names them from R 19th's WRAP at send | |

- A different hash is a STOP and a mail.
- **Re-key: THE GENERIC CLAUSE BINDS, AND IT COMES FIRST.** Re-key every lane-bearing declaration, including LOCK_SEAT defaults, fixtures, GO-clause ordinals and every hardcoded constant in `m7_squash*` / `m1_go_complete*` / `mergein*` (REQUIRED arguments, STANDING_LINES :406, :419). The tool wins. Sweep every live 12+-hex constant outside comments before the first run; print `N checked` per tool; `0 checked` is a FAIL.

## THE BUILDER YOU WRITE FIRST (RULINGS Q-BUILDER76)
Copy `build_addendumra17_gate75.py` (R 17th's, `04ed62b4ff18b3d3`) to `build_addendumra20_gate76.py`. Never edit R 17th's file. Keep every inherited assert, and:
- `RA17_*` -> `RA20_*`; the GO-clause regex -> `GO \(Seat R 20th\): merge \d{3,5} on [a-z0-9]+`.
- The predecessor-claim tuple: ADD `"Seat R 17th"` (merged #1426: its claim is in develop's tip message), `"Seat R 18th"` (AUTHORED #1427), `"Seat R 19th"`, `"Seat G 4th"` (AUTHORED #1428). Assert `"Seat R 20th"` ABSENT.
- **ADD a REQUIRED `RA20_MERGE_IN_HEAD`** (40-hex, M), used only with `RA20_LANDING=merge-in` and refused otherwise: read M BY SHA; assert `parents(M) == [GO PR head, GO develop]` (two reads: count, then each), `tree(M) == T'`, and read `targets` / the mode census / the path count from M against `GO develop`. Without it, `merge-in` REFUSES by name (today it refuses by an unsatisfiable assert).
- **Row #1428 (step 1):** `RA20_LANDING=on-develop`, `RA20_NO_MERGE_IN=1`, `RA20_DOCS=head` (GO flow/cheat == the HEAD blobs `6c2038c3778f07fcebb78b5f28bc19260719a67b` / `c3de14c08d56d620c84f65884956ebb680ee4e59`), `RA20_OWN_KEYS=KS-593`, `RA20_EXPECT_PATHS=9`, `RA20_MODE_CENSUS={"100644": 9}`, `RA20_HEAD_TRAILER=refuse`.
- **Row #1427 (step 2):** `RA20_LANDING=merge-in`, `RA20_NO_MERGE_IN=0`, `RA20_MERGE_IN_HEAD=<M>`, `RA20_DOCS=merged` (GO flow/cheat == the COMPOSED blobs, asserted != the head's), `RA20_OWN_KEYS=KS-1274`, `RA20_EXPECT_PATHS=6`, `RA20_MODE_CENSUS={"100644": 5, "100755": 1}` (the job stays 100755), `RA20_HEAD_TRAILER=refuse`.
- **Arms — each must REFUSE, each run before the first real use, each at ITS OWN assert (STANDING_LINES :441, with a POSITIVE control that passes end to end):** merge-in without `RA20_MERGE_IN_HEAD`; an M with parents swapped; an M whose tree != T'; `DOCS=head` on row #1427; `DOCS=merged` on row #1428; the R 17th ordinal in the clause; a body planted with `Merged by Seat G 4th`; a #1428 body planted with `this does not close KS-593.`; #1427's PR TITLE (`KS 1274: …`) as the subject. POSITIVE controls: row #1428 on the real head; row #1427 on the real M after `qm`.
- **Then the chain per row:** builder -> `mergera1.py --dry` -> READ the `.DRY` body (ONE `Merged by Seat R 20th`, 0 trailers, 0 Co-Authored-By, 0 `Generated with`, the subject byte-equal to the GO's, the hyphenated key set == the own key).

## M1 — THE GO PARSER (each line exactly ONE match, extracted from YOUR builder by `ast`)
| line | #1428 (GO 1) | #1427 (GO 2) |
|---|---|---|
| `- develop D:` | the develop at GO time (`0a6177ea5482…` if unmoved) | develop AFTER #1428's squash |
| `- PR head:` | `64eafead891e81f5adb4e46aaa94ff6a6ace1998` | `2b6da5f561b05a820bbe1ab5e891bff9f4f531c8` (the GATED head; M rides in `RA20_MERGE_IN_HEAD`) |
| `- PR base B:` | `0a6177ea5482227e83d5045b68b8577a56326ffc` | `0a6177ea5482227e83d5045b68b8577a56326ffc` |
| `- END_TREE:` | `7f6e6fe0ca15702cab1b5e1a0d37ba7ff8f665b5` | `9b6c3dfef865dfc35b05d4da8fcad7e24249fbb1` |
| `- Target tree T':` | `7f6e6fe0ca15…` (== END_TREE) | M's tree (predicted `57c9b5eaec95ddc86a7d139f9f2d957015a3fd97`, re-read on the real develop) |
| `flow`/`cheat` lines | the HEAD blobs above | the COMPOSED blobs (predicted `b2bd07dbae40…` / `f4503e99d43e…`) |
| `Declared squash subject:` | `KS-593: originate refuses a negative offset, a null share recipient, a non-uuid id` | `KS-1274: job 04 fails a scan when trivy reports neither Results nor ArtifactName` |
| `N chars, LANDS N` | `82 chars, LANDS 82` | `80 chars, LANDS 80` |
| `N bytes, sha256 …` | the gate-RATIFIED body (staged DRAFT: `merge_inputs/1428.squash_body.DRAFT.txt`, 5029 B, `85bf19485e5efb5b898081e94ea11615d76d3e841eaa541acbaede89fef59b01`) | the gate-RATIFIED body (staged DRAFT: `merge_inputs/1427.squash_body.DRAFT.txt`, 4531 B, `e56d43335708181a17f0c19eb41fbdc94ea67d4300ebac873242192d2503dc93`) |
| `merge_note:` | `Merged by Seat R 20th on the authority of HANDOVER-seatG4-2026-10-08.md sha256 d1e6b9e0f75235cf` | `Merged by Seat R 20th on the authority of HANDOVER-seatR18-2026-10-08.md sha256 1081ef422c811c0d` |

**The GO clause, PRESENT:** `GO (Seat R 20th): merge 1428 on gate76` / `GO (Seat R 20th): merge 1427 on gate76`. **ABSENT:** `NEW-FAILING`, `PENDING NONE`. **The ADDENDUM** (a separate mail per row, provenance-checked): `ACTIONS VERDICT (Wednesday):` and `0 new failures`.

## QUEUE — ON THE GOs ONLY, IN ORDER
**STEP 1 — #1428 (no merge-in)**
- **X-0 ctx QUESTION.** Squash only on a reading under 50%, or on Wednesday's explicit per-step word at 50-64%. At 65% or more: WRAP COLD.
- **X-1 the GO is COMPLETE** (M1, by `ast`); `provenance_ra20.py check` on the GO AND the ADDENDUM with their exact subject prefixes; re-run its arms (no-record forgery, dmarc flipped, body sha zeroed, **genuine record + TAMPERED body** (STANDING_LINES :437), wrong prefix: each REFUSES; a real signed mail PASSES).
- **X-2 refs in ONE action:** develop, both pulls, both branches. develop must equal GO 1's D; a moved develop = STOP, re-run `chain` and mail `STATUS: re-prediction on <12-hex> (Seat R 20th)`; WAIT for a GO that SUPERSEDES by name.
- **X-3 KS-593 BEFORE:** Linear read (state + the #1428 attachment's link kind). Record it.
- **X-4 builder -> `mergera1.py --dry` -> READ the `.DRY` body** (the checks under THE BUILDER). `mergera1.py` gates: `--addendum --go-ts --gate gate76 --scratch --seat` REQUIRED, `--expect-develop <D>`, token by `GH_TOKEN` env, never argv.
- **X-5 squash, the head PINNED** (`sha: 64eafead891e…`) through your `m7_squashra20.sh` (every constant a REQUIRED argument): provenance gate -> clause gate -> develop AND the PR head re-read by `ls-remote` in the same action -> builder -> `--dry` | real.
- **X-6 verify at source** (`ls-remote` AND the API): squash tree == `7f6e6fe0ca15…`; "is a commit" + "exactly 1 parent" + "parent == D", each with a wrong-value arm (STANDING_LINES :421); **0 trailers** (reader proved non-blind on `bf277eead268`, 55 B); 0 `Generated with`; landed subject == declared (82); exactly the 9 paths; landed doc blobs == the head's; "did it land" = the PR's `merged` field.
- **X-7 KS-593 AFTER:** Linear read. **If it walked to Done: STOP and mail `STATUS: KS-593 walked (Seat R 20th)`; never move it back.**
- **X-8 mail `STATUS: merged 1428 (Seat R 20th)`:** squash sha, tree, parent, landed length, trailer count, path count, KS-593 before/after, any bot ticket move (report, never revert), the LIVE watcher pid. WAIT for Wednesday's word to start STEP 2.

**STEP 2 — #1427 (docs-only keep-both merge-in, then the squash)**
- **M-1 re-predict on the REAL develop D1** (= #1428's squash, or later if anything else landed): `c4_docs_gate76.py chain --order 1427 --develop <D1> --heads 1427=2b6da5f561b0…,1428=64eafead891e… --out <fresh>` in YOUR clone (fetch D1 by SHA from the GitHub URL first). A refusal naming a moved CODE path = STOP (RE-GATE). Mail `STATUS: re-prediction on <D1 12-hex> (Seat R 20th)` with the tree and the two composed blobs, then `cmp` them with the kit's `2_1427_*` files (IDENTICAL if nothing but #1428 landed).
- **M-2 objects:** ONE local objects-only transfer of D1 from your scratch clone into the shared store (fetch from the clone path BY SHA, `--no-tags --no-write-fetch-head`), under the lock, `rev-parse --all` byte-identical before and after, `cat-file -e` with a POSITIVE control (STANDING_LINES :405).
- **M-3 merge-in, under the lock,** in a FRESH detached `s-ra20-m1427` at `2b6da5f561b0…` (`worktree add --detach`, never `-b`): your `mergeinra20_gate76.sh` (copy of R 12th's, every knob a REQUIRED argument: `--ours` the head, `--dev` D1, `--dev-parent` the develop before #1428's squash, `--base` the COMPUTED merge-base, `--predicted-tree` from M-1, `--flow-blob`/`--cheat-blob` from M-1, `--own-key KS-1274`, `--head-paths` #1427's 4 code paths, `--dev-paths` #1428's 7 code paths (re-derived by the TOOL's own meaning), `--expect-ours-paths 9`, `--expect-dev-paths 6`, `--control-commit bf277eead26897bb648c801f92308681dbdaffdc`, `--subj` the GO's merge-in subject). Conflicts on EXACTLY the two docs, resolved BY CONTENT to the composed bytes VERBATIM. **NEVER `git merge-file --union`, never a hand edit of git's hunk** (the drafter re-measured the hazard on this pair: union drops #1428's closing `</td></tr></table>` from the FLOW doc, and html_docs_matrix still reads 12/0). Required: tree(M) == the predicted tree; parents EXACTLY `[2b6da5f561b0…, D1]`, each read separately; 0 trailers vs the 55-byte control.
- **M-4 qm, in YOUR clone:** `c4_docs_gate76.py qm --repo <your clone> --pr 1427 --head 2b6da5f561b05a820bbe1ab5e891bff9f4f531c8 --merge-in-head <M> --develop-after <D1> --predicted-tree <T> --out <fresh>`: Q1-Q6 PASS.
- **M-5 push M BARE:** outside the lock, S-1 in the pushing worktree (`npm ci --ignore-scripts` + `npm run build --workspace=packages/shared`, ASSERT `dist/index.js`; `npm ci --ignore-scripts` in EVERY `systemTest/*` with a package.json, STANDING_LINES :429). Then `env -u GIT_SSH_COMMAND LOCK_SEAT='Secuura/Blockchain-R ra20' bash <REC>/pushra1_ff.sh <abs worktree> feature/ks-1274-trivy-bare-object-guard-ra18-1 2b6da5f561b05a820bbe1ab5e891bff9f4f531c8` with `FF_DRYPROOF=1` FIRST. The delta carries all of #1428 (7 `Blockchain/Dev` paths): the hook runs the FULL preflight in-hook (~7 min; the drafter's by-hand run of the same tree read `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`, `shell suites: 71 passed, 0 failed, 0 skipped (of 71)`). Result = the tool's `.rc` + `ls-remote` (STANDING_LINES :402); on rc 141 with the ref unmoved, the KS-1149 class: report, retry under the lock, never loop. **`PREFLIGHT FAILED` or a refused push = STOP. Never `--no-verify`.** Quote the push's gate lines EXACTLY (STANDING_LINES :272).
- **M-6 Actions on M** by FULL 40-hex `head_sha`, classified against M's develop parent (three classes, SUBSET, two agreeing terminal polls, a fabricated-sha control); mail `STATUS: merge-in 1427 pushed (Seat R 20th)` with M, its qm, the push's gate lines and the Actions; WAIT for GO 2 and its ADDENDUM.
- **X-1..X-6 again for #1427** with `RA20_LANDING=merge-in` + `RA20_MERGE_IN_HEAD=<M>`; the squash PINNED to M (`sha: <M>`); verify: squash tree == T'; 1 parent == D1; 0 trailers; 0 `Generated with`; landed subject == declared (80); exactly 6 paths vs D1; the landed doc blobs == the composed blobs; the job `Blockchain/Testing/jobs/04-container-trivy.sh` still `100755`.
- **X-9 KS-1274:** read its state before and after; it must NOT move to Done (a live trivy scan is OWED). Mail `STATUS: merged 1427 (Seat R 20th)`.

**Actions:** you never author an Actions verdict; the ADDENDUMs are Wednesday's. The drafter read at 07:54Z-07:57Z, both heads: class (2) {Code Security Gates} ⊆ develop's; class (1) Security Scanning / Dependency Audit (KS-1148, pre-existing, 12 of the last 12 repo-wide runs failed); class (3) head {Akto, Performance, Playwright} ⊆ develop {the same + Schemathesis}; 0 pending. CI's own shell-suite step: develop and both heads `shell suites: 65 passed, 6 failed, 0 skipped (of 71)`; #1427's head `container_trivy_failed_scan_is_loud.test.sh` 5 passed, 0 failed (develop 3 passed, 0 failed).

## STANDING FINDINGS CARRIED (STANDING_LINES, by line)
`:439` html_docs_matrix 12/0 is NOT tag-balance evidence · `:437` authenticity gates bind the record to the BODY · `:371` a merge tool must not ADD attribution; check the SENT body · `:278` a hyphenated foreign key ATTACHES · `:319` the declared subject IS the landed subject · `:402` a result is the tool's `.rc` + `ls-remote` + the API · `:405` a merge-in needs develop's objects in the WORKTREE's store · `:406`/`:419` inherited tools fail closed on unset knobs · `:421` "ONE parent" is three reads · `:420` `ls-tree` for presence · `:429` `npm ci` in every systemTest package before any push · `:441` a refusal arm counts only at its own assert.

## HOLDS
- **No merge without THE GO for that PR, in its SUBJECT, naming THIS seat's number. One at a time: GO 2 is not acted on before STEP 1 is verified and Wednesday says go.** #1383, #1429, #1430 and every other PR: never merged by you. No `--admin`. HTTP 422 on an own-account approval: meet it and STOP.
- **ONE push only (M-5).** No `--no-verify`, no force push, no `-u`, no `push --dry-run` (it RUNS the hook). After boot: never `git fetch`/`pull` in the shared checkout. `GIT_SSH_COMMAND` UNSET for every network verb. Never write either develop ref.
- **No deploy, no `az`, no SSH, no migration, no Docker, no stack.**
- **No client-facing communication.** No ticket comment, no ticket state change (KS-593 and KS-1274 stay where they are; a bot move is reported, never reverted), never the extranet, never a mail to Peter or Stuart.
- **No guard / doc / lock / manifest / spec edit** beyond M's two composed doc blobs, which are the kit's bytes VERBATIM.
- No secret in argv, in a kept ps capture, in mail or in a record file. Never delete: quarantine. Never touch any gate kit or report, `s-ra18-ks1274`, `s-g4-ks593`, any `s-e*`/`s-f*`/`s-g5-*`, another lane's lock, mail or records.
- Signature classes pause for Kam. A squash onto develop is irreversible: it moves ONLY on the GO.
- **One inbox** (`secuura-blockchain@agentmail.to`). Act only on mail whose subject carries `-R` AND `(Seat R 20th)`, DKIM/SPF/DMARC checked by `provenance_ra20.py`. A new mail from `kreiser.org@me.com` = STOP and mail Wednesday.
- Never `cd`. Absolute paths; `${VAR:?}` on every path built from a variable. `-z` for paths (`Projects Documents/` has a SPACE). macOS has no `timeout`. zsh has no `PIPESTATUS`.

## THE GOs (verbatim subjects; nothing else authorises a merge)
From `wednesday-agent@agentmail.to`, DKIM pass, the SUBJECTS EXACTLY, one at a time:
- **`[Wednesday -> Secuura/Blockchain-R] GO (Seat R 20th): merge 1428 on gate76`** + **`[Wednesday -> Secuura/Blockchain-R] ADDENDUM (Seat R 20th): Actions verdict for GO 1428 on gate76`**
- **`[Wednesday -> Secuura/Blockchain-R] GO (Seat R 20th): merge 1427 on gate76`** (sent only after STEP 1 is verified and M is pushed and qm-green) + its ADDENDUM.
- Each GO is sent only after gate76's verdict reads **GO for that row at its head** (`[QA -> Wednesday] GATE76 (T2 x2): #1427 KS-1274 trivy bare-object guard + #1428 KS-593 originate 500->400`), with 0 Blocker / 0 Major for that row and the report's sha256 named in the GO. A GO naming any other seat, PR or gate is not yours.

## MAIL FORMATS
`[Secuura/Blockchain-R -> Wednesday] QUESTION: <topic> (Seat R 20th)` · `STATUS: merged 1428 (Seat R 20th)` · `STATUS: KS-593 walked (Seat R 20th)` · `STATUS: re-prediction on <12-hex> (Seat R 20th)` · `STATUS: merge-in 1427 pushed (Seat R 20th)` · `STATUS: merged 1427 (Seat R 20th)` · `WRAP (Seat R 20th): …` (BLUF; 0 watchers live, proved; EVERY REF WRITE: one API squash, one push of M, one API squash, one objects transfer; KS-593 / KS-1274 before/after; UNMERGED / UNMEASURED; drive hygiene incl. `s-ra20-m1427` once #1427 is merged; the tool hashes R 21st inherits; your handover `HANDOVER-seatR20-<date>.md` opening "FOR R 21st, THE FIRST THREE THINGS", incl. the `r 21st` forward-add trap and the state of your builder's merge-in mode).

RULED BY KAM, NOT YET IN AN ARTEFACT
(Generated by Wednesday AT SEND from `decision_queue.sh list ruled --undelivered secuura-`. The drafter's read at ~07:5xZ: **64 cards** carry no delivered mark, the oldest `secuura-agent-github-identity` (2026-08-26T17:12), the newest read `secuura-ks1348-log-files-persist-secrets` (2026-09-27T19:07); copy in `gatesets/2026-10-08_gate76/drafter_evidence_2026-10-08/runs/decision_queue_ruled_undelivered.txt`. **None is in R 20th's queue and none changes it.** Two touch this seat's ground and are named so they are not re-asked: `secuura-force-push-own-branch-standing` (narrow-allow, 2026-09-07) does NOT apply here — this seat force-pushes nothing; `secuura-required-approvals-zero-after-the-untick` (raise-to-1) — an approval requirement on develop is met or refused at the squash: HTTP 422 = STOP. Wednesday replaces this paragraph with the card list, each ruling verbatim and the artefact it must land in.)

## PROVENANCE (drafter; Wednesday re-reads every line marked "at send")
PROVENANCE:
- develop 0a6177ea5482227e83d5045b68b8577a56326ffc; pull/1427 == branch 2b6da5f561b0; pull/1428 == branch 64eafead891e; #1383 32e8459bc0f5; #1426 dd31aa0c998c (merged) | `git ls-remote` from the Blockchain checkout by the drafter, 07:28:27Z and 08:02:16Z | read 2026-10-08 (**re-read by Wednesday at send**)
- step 1 7f6e6fe0ca15 (== END_TREE, no merge-in); step 2 57c9b5eaec95, composed blobs b2bd07dbae40 / f4503e99d43e; merge-tree of the two heads rc 1 on the two docs; union hazard on the flow doc | `c4_docs_gate76.py chain` (selftest 15/15) in the drafter's scratch clone | read 2026-10-08
- R 17th's builder: on-develop rc 0 for each row alone; merge-in rc 1 both ways; ordinal hard-coded; residue refused | `drafter_evidence_2026-10-08/runs/builder_probe.out` on a byte copy (04ed62b4ff18b3d3) | read 2026-10-08
- both branch commits 0 trailers (1 B vs 55 B control), #1428's message `does not close KS-593` | `c1_pin_gate76.py` P5 / P8 (selftest 12/12) | read 2026-10-08
- the red/greens re-run: #1427 4/1 with only the KS-1274 cell and the control ok both ways; #1428 2f/3p, 2f/13p (share + hermetic), 3f/3p, whole originate 96 / 1093 / 0 | `c3_redgreen_gate76.py` in the drafter's worktrees | read 2026-10-08
- the final-tree preflight 12/15 INCOMPLETE, 71/0 of 71, legs 3 4 8 skipped | `c3_preflight_gate76.py preflight` on the SIM of 57c9b5eaec95 | read 2026-10-08
- the merge toolset hashes (TOOLS table) | `shasum -a 256` on R 17th's `merge/`, `boot/` and R 12th's `raise/` | read 2026-10-08
- Kam's usage grant | `0_Brain/learnings/2026-10-08_new-account-push-merge-test-as-much-as-possible.md` (status: live) | read 2026-10-08 (**expiry re-checked by Wednesday at send**)
- R 19th's handover, tools and wrap state | NOT READ (R 19th live at draft) | **Wednesday at send**
- KS-593 / KS-1274 Linear state | NOT READ by the drafter | **Wednesday at send**

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-08 19:2x (drafter); Wednesday re-runs it at send
