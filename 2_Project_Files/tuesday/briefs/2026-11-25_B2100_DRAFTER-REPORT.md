STARTABLE: YES (only with Q1, Q2 and Q7 answered "a" in words at Stamp S4, and Stamp S8 naming the heavy runner's sha256: Q1 cuts row 4 from row 3's landed squash; Q2 keeps the button read inside the writer, so the read catalogue is not widened; Q7 keys `undo-owed` by write family, the row-3 gate's FOUND 1 fix)

# B2100 DRAFTER REPORT: M577 first-run row 4, BUILD lane (UIConfiguration register and unregister, no device), seat Datasec/OXPd2-X75

Drafter B2100 (Opus, in-session, read-only toward the project, GitHub and every device). The drafter's first `date` printed `Wed 25 Nov 2026 23:26:55 AEDT`; the sidecar's first line carries the write clock (`2026-11-26 00:54:57 AEDT`, printed by `date`). Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2100_SEAT-X75_oxpd2-row4-uiconfig.md` (270 lines, 93488 bytes, 0 bytes outside ASCII, 9 unfilled slots) and its sidecar `.measured` (`stamp_check.py`: 195 claims, 195 measured, rc 0). Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s328/d2100/` (below `<d>`). Gate tier G1 (`fleet/specs/model-routing.md:108`), round 1 of 2 of the row-4 write lane. **Nothing was sent to, run on or read from the printer or any device, by me; the kit forbids it to the seat.**

## BLUF
- **Built, frozen in `1-red.diff` and `2-fix.diff`: 11 paths (2 A, 9 M), all in the four OXPd 1.x folders.**
  - **The client.** `Oxpd1WriteKind` gains `RegisterTopLevelButton` and `UnregisterTopLevelButton`, two rows of HP's committed UIConfiguration binding. The register takes an `Oxpd1TopLevelButton`: an id, a title of 1 to 100 characters, a position of 1 to 65535, an absolute https target page; no icon, no credentials, no post body. Its undo is the unregister of the same id.
  - **The records read.** `Oxpd1Writer.ReadTopLevelButtonsAsync` sends `GetTopLevelButtonRecords` as `admin` through the LANDED `SendAdminReadAsync` (no code line of `Oxpd1Client.cs` changes; two of its comments do). It answers only when every record holds ONE id of HP's UUID form. `Holds` matches in any letter case.
  - **The lab.** `oxpd1 write --write RegisterTopLevelButton|UnregisterTopLevelButton --button-id ... [--button-title --button-target [--button-position]]`.
    - An executed register reads the records first; an id held in any case is exit 10, nothing written, no undo (the agent register's landed rule, not row 3's exit 0: HP's register of a held id overwrites it).
    - An answered register or unregister reads the records after and prints whether the id is listed. The exit code is unchanged.
    - `undo-owed` owes the unregister of a register, and now matches every write only within its own family (sign-in agent, Test service, CA store, button): gate B2096 FOUND 1's fix.
  - **The read catalogue (`Oxpd1Read.cs`) is untouched.**
- **Measured in a fresh `<d>/clone3` with the frozen patches (BASE `1ccf6d0c`, pull request 52's squash):**
  - RED: adapter `Total: 104, Errors: 0, Failed: 14`; Lab `Total: 297, Errors: 0, Failed: 13`. All 27 are red by an `Assert.` line, all in the two new classes.
  - GREEN: `total: 2338`, `failed: 0`, `succeeded: 2334`, `skipped: 4` (BASE 2297 + 41).
  - Mutants: `MUTANTS: 17 of 17 MATCH, 17 of 17 undone equal` (twice: prototype and frozen). Then the rebuild (dlls later than the mutated files) and the solution green again.
  - Chain: `locks equal 36 of 36`; 2338/0/2334/4; `GUARD: clean (14 files)` and `(15 files)`; `Ran 117 tests` OK; `RULES: clean (679 files)`; `CHECKS: 10 of 10 PASS`; `WORDS: clean (2 files)`; `B2[0-9]{3}` 0 and 0.
  - gitleaks: control rc 1; the clone and 16 neutral files rc 0.
- **PREDICTED hosted (never run on a head of this lane):** `--total 2338 --rules 679`, skipped 4/21, guards 14/15, unit 117.
- **Seat id X75 is free.** An underscore-aware scan (`(?<![A-Za-z0-9])X75(?![0-9])`, control `_by_X75_` fires) of the 44 non-`.pre-`, non-`.measured` SEAT kits of 2026-11-24 and 2026-11-25 found X75 0 times; the control X74 was found in 3 (B2091's own kit among them). Panes named X75: 0. `Briefs/` files naming B2100 or X75: 0 (control: B2091 2). `<project>/.tools/b2100`: absent.
- **The partition holds by ORDER, from both sides.** Row 3 landed (pull request 52); this lane shares nine of row 3's eleven paths (the eight the commission names plus `Oxpd1Client.cs`, comments only) as a serial dependency. Open pull requests 0; both newest OXPd STATUS files end READY (`READY B2097: 1d907789...`, `READY B2091: be650e1b...`).
- **The 1.9 scope line (not a hold):** the record (C-85, `CLARIFICATIONS.md:1146`) says "whether anything is built on 1.9 before HP's package arrives (nothing is)"; the card `datasec-oxpd-hp-19-target-1125` (read by `decision_queue.sh show` into `<d>/scratch/card-1125.txt`, id filter: 1 occurrence) is ruled `a` with the detail "H7 asks HP for the 1.9 SDK; design updated once it arrives", which equals the record's quote at `:1136`. **Record and card agree**; so no Question. The lane builds on the committed 1.8.4.1 descriptions.

## Facts re-measured (instrument)
- **Origin.** `gh api -X GET` under the project `GH_CONFIG_DIR` (`gh auth status`: `kamilDatasec`).
  - `main` = `1ccf6d0c6a4d9af1da986ec528ac142c565c2edd` (read at 23:27:55 and again at 00:54; unchanged).
  - Pull requests 52 to 43 closed and merged; open 0.
  - `matching-refs/heads/b2100` 0 rows (control `b2091` 1 row). `.private` and `.permissions.push`: `true true`.
- **BASE's push run.** `hosted3.py 1ccf6d0c... --total 2297 --rules 677 ...` printed `HOSTED 1ccf6d0c6a4d9af1da986ec528ac142c565c2edd: PASS` (`<d>/logs/hosted-base.out`; run 45576025564).
- **Row 3 landed byte for byte:** the nine BASE sha256 values of this kit's code table equal kit B2091's "After both" column (compared by a program over the two kits' code tables: 9 of 9 equal).
- **HP's committed text** (`contracts/oxpd1/hp/...uiconfiguration_2010_04_14/`, CR stripped into `<d>/scratch/uic.wsdl.txt`, `uic.xsd.txt`):
  - `RegisterTopLevelButton`: overwrites a record of the same guid; ids compared as case-sensitive strings; "may return before the new button ... has become manifest"; cleared "by a disk init or restore factory settings"; admin; faults `RequiredElementMissing`, `InvalidParameter`, `IllegalOperation` (no room), `InternalError`.
  - `UnregisterTopLevelButton`: an id not held "will succeed ... but will have no effect"; admin.
  - `GetTopLevelButtonRecords`: admin; the result "Will be empty if there are no top level buttons".
  - The binding's soapActions (`UIConfigurationSoap12Binding.wsdl:61`, `:88`, `:97`); service name `UIConfigurationService` (`:255`).
  - The schema: `TopLevelButtonRecord` sequence id, title, description, requestedPosition (1 to 65535), browserTarget (optional post string, then webApplication), optional icon; common `UUID` pattern 8-4-4-4-12; `LocalizedStrings` 1 to 64; `LimitedUri` at most 256; `Binding` Plain or Soap12. B01 validates both bodies against it (control: position 0 refused).
- **`CLARIFICATIONS.md`** (sha256 `b2bc7f4a...`, 1196 lines; was 1186 at B2091: the records pass B2097 wrote C-87):
  - 0 lines each for `RegisterTopLevelButton`, `UnregisterTopLevelButton`, `GetTopLevelButtonRecords`, `UIConfiguration`, `top-level button`; `home-screen app` 3 (`:1088`, `:1114`, `:1192`); control `OXPd` 195.
  - Quoted by `awk NR==n`: `:734` (C-72), `:1088` (his detail "We ask again before any home-screen app is added."), `:1136`, `:1144`, `:1146` (1.9), `:1192` (C-87: "Row 4 is built only after row 3 has landed, never beside it" and "Its button goes on the home screen only after his word").
- **Toolchain.** `dotnet` 10.0.404 from `<project>/.tools/dotnet`; gitleaks 8.30.1.
- **Model.** `models_latest.json:17` (`claude-opus-5-5`); `<project>/CLAUDE.md:7` (newest Opus); `model-routing.md:108` (G1).
- **Landing rule.** `<project>/CLAUDE.md:55` (seats push a branch only) and `:82` (Tuesday lands by SQUASH pinned to the head, one parent), both re-read.
- **Lock and load.** `wave1-heavy.lock.d` absent at the start and at the end; lock waits per job 0. Load1 reached 13.65 during the frozen mutants; `heavy.py` waited it out. The NexusAI pane `Datasec/NexusAI-N177` was live at my first read and gone at my last (00:54).
- **CI predicates at BASE** (`ci.yml`): `:40`/`:70` restore, `:42`/`:72` build, `:45`/`:75` test, `:46`/`:76` `total: +[1-9]`, `:48`/`:78` publish, `:50`/`:80` guard, `:211` `FLOOR=117`, `:218` `repo_rules.py`.

## How the patches were cut (for the stamp's spot checks)
- **The red tree** is the fixed tree with the 17 mutant edits of `mutants_b4.py` applied at once (by its own `apply` verb), its READMEs at BASE (red tree `4d51510296c2e72991f96c46c0ff17deea076422`).
- `1-red.diff` = BASE..red tree, cut in `<d>/clone2` (`git diff --cached --binary`); `2-fix.diff` = red tree..fixed tree.
- `2-fix.diff` alone on BASE: `apply --check` rc 1. After both patches in `<d>/clone3`: 11 of 11 files equal to the prototype.
- **The mutants' expected red sets** were written before any mutant ran and were MEASURED to match on the prototype (`<d>/logs/mutants-proto.out`, 17 of 17), then again with the frozen tool on the frozen tree (`<d>/logs/mutants-frozen.out`, 17 of 17). Each red set follows from the cell's assertions (for example `mNoReadBefore` reds T05's 403 row because that row asserts two requests, and without the read there is one).

## D-decisions (Tuesday's as coordinator; each is a Q)
- D1 cut from row 3's landing (Q1). D2 the records read inside the writer through the landed send (Q2). D3 answered only when every record has one UUID-form id. D4 a held id (any case) is exit 10. D5 the read after is reported only. D6 the record: id, title (also description), position (default 1), https target; no icon, credential or post body. D7 `undo-owed` matched within one family (Q7; gate B2096 FOUND 1). D8 one landed literal moves (`WriteTests.cs:44`, 6 to 8); no new Lab source file, so `LabCertTests.L03` holds. D9 one commit, push by sha; local CodeQL not runnable.

## Questions for Tuesday (defaults as built)
- **Q1 (STOP-class): the partition with row 3.** Default **a**: cut from BASE = row 3's squash; serial, nothing open beside it. Alternative b: wait for row 3's records or device run (no gain: none of their files is here).
- **Q2 (STOP-class): where `GetTopLevelButtonRecords` lives.** Default **a**: in the writer (`ReadTopLevelButtonsAsync`) through the landed `SendAdminReadAsync`; `Oxpd1Read`, its seven rows and the pinned read counts unchanged. Alternative b: an eighth `Oxpd1Read` row (it has a `Get` name, so the read-only rule admits it; `ContractTests` and `TestServiceTests` counts move; a re-draft).
- **Q7 (STOP-class): take gate B2096 FOUND 1's fix here.** Default **a**: key `undo-owed` by (host, family, id) (T08 and `mFamilyDropped` prove it; no landed cell changes). Alternative b: keep (host, id) and add the button kinds only (button ids then share the collision; a re-cut).
- Q3 every record one UUID-form id (default) vs skip the unreadable ones.
- Q4 a held id: exit 10 in any case (default) vs exit 0 as row 3's import (wrong here).
- Q5 the read after: reported only (default) vs exit 8 when not listed (HP: may show late).
- Q6 no icon, credential or post body (default) vs an icon option.
- Q8 the dry run prints the whole envelope (default; no secret in it).
- Q9 G1 (the commission names it).
- Q10 gate B2096 FOUND 2 to 7 not taken (none is in this lane's behaviour; FOUND 4's `OnlyElements` is shared and unchanged, so the button reader inherits its no-break-space limit); no local CodeQL; Opus; 120/90; pane X75.
- **S8 (HEAVY-SHA).** Default: the canonical `31adedc8...` (my runs used it; `<src>/heavy.py` hashes to it; the item-138 fix was not adopted after two NO GOs, per the commission).

## The later device run (FOR TUESDAY in the kit; not this kit's)
- **It needs the product owner's word first** (`CLARIFICATIONS.md:1088`, his detail: "We ask again before any home-screen app is added."; C-87 `:1192`). I read a test button as on the home screen, as the readiness note did. Card him only when the run is near, as the commission says.
- A PRESS on the panel is a physical act no agent can make; a target page must be reachable from 192.168.8 (owed item 118's route is UNMEASURED). Without a served page the press tests nothing of the callback.
- The unregister always follows when owed; then `undo-owed` must print "nothing is owed". Never a reset or a disk init (C-72; HP clears button records only by those).

## Chain inputs (MEASURED LITERALS rule 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | the kit, Stamp S1 to S8 | Tuesday's stamp |
| 1 | `<src>` (10 files, `heavy.py` per S8), `<repo>` local values, origin BASE, BASE's push run | `<d>/seat-tools` (exists); `<repo>` (exists); GitHub (read at drafting) |
| 2 | the files at BASE | the clone of Step 1 |
| 3 | `1-red.diff`, the clone at BASE | Step 1 |
| 4 | `2-fix.diff`, `mutants_b4.py`, the red tree built | Step 1, Step 3 |
| 5 | the green tree, mutants undone and rebuilt | Step 4 |
| 6 | the staged tree, `checks_b4.py`, `words.py`, `commit-message.txt` | Step 5, Step 1 |
| 7 | the commit, `origin/main`, `run_step.py`, `hosted3.py` | Step 7 (a), the fetch, Step 1 |

## STOP-severity checks run once on the drafter's own output (with controls)
- The tools by sha256 (but `heavy.py`, a slot); `clone.py`, `hosted3.py`, `run_step.py`, `words.py`, `heavy.py` `cmp`-equal to kit B2091's.
- RED by assertion, 27 of 27 (controls: the two `Total:` lines).
- The mutants, 17 of 17, twice.
- `checks_b4.py` 10 of 10, each control firing.
- Lock files 36 of 36.
- `RULES: clean (679 files)`, the R5 hash half NOT RUN (no `--source-documents`; no supplied-source folder in the lane).
- gitleaks: control rc 1.
- `words.py`: control 13 of 13; over 1114 added lines and the message, clean.
- `B2[0-9]{3}` 0 and 0 (control: the kit 26).
- The guard counts 14 and 15; `Ran 117 tests`.
- `2-fix.diff` alone refused.

**NEVER RUN:** `clone.py seat`, the branch, the commit and its identity, `run_step.py`'s neutral scan of a lane commit, the push and its read-back, `hosted3.py` on a lane head, the rebase, every hosted leg, CodeQL.

## UNMEASURED
- Everything the M577 does with a button: what it shows with no icon, where it places it, how long it takes to show, how it writes an id in its read, what happens when the target page is unreachable, its button limit.
- Whether a test button counts as a "home-screen app" in the product owner's sense. That is his call; the readiness note and I read it as yes.
- Whether the printer can reach this Mac (owed item 118).
- Every hosted leg. The Windows and Linux behaviour of these cells (macOS arm64 only).

## Outside the fences (disclosures)
- **Write verbs in my own scratch clones only.** `git apply`, `git add` and `write-tree` ran in `<d>/clone2` and `<d>/clone3`, and the Edit tool changed files of `<d>/clone`. All three are draft clones (push URL `invalid://no-push`, no identity). Nothing ran in `<repo>` or any project repo. `<d>/base-ref` is a `cp -Rc` copy of the draft clone at BASE, used for the BASE reads.
- **Heavy jobs.** Every `dotnet` job and test executable ran through the canonical `heavy.py` and the OXPd wave lock, one at a time (two background runs of my own chains, each serial). The released lock folders are in `<d>/_quarantine/locks/`. No other holder's lock was touched, and no NexusAI lock was taken.
- **One card read.** `decision_queue.sh show datasec-oxpd-hp-19-target-1125` went into `<d>/scratch/card-1125.txt` and was read through an id filter (1 occurrence). The commission asked me to compare the record with Kam's 1125 card. No `list` was used.
- **Reads outside the project.** `NEXT-PICKUP-TUESDAY.md` lines 1 to 25 only; `DRAFTER_RULES.md` whole; the commission, the readiness note B2089, kit B2091 and its report, and gate B2096's VERDICT.md and FOR-RECORDS.md, each whole; the headers of `brief_seat.sh` (lines 20 to 30), `decision_queue.sh` (1 to 40) and `stamp_check.py` (1 to 40); `model-routing.md` by grep; `models_latest.json` by grep. None of `briefs_staged/`, `scoreboard.md`, `_ledger.md`, a WEDNESDAY or FRIDAY tree, or another client.
- **Harness files.** The harness saved one large Read (kit B2091) and the background tasks' output under its own folders (`4_Credentials/.claude/...` and `/private/tmp/...`). The chain logs are in `<d>/logs/`.
- **One refused command.** One command failed in zsh with `bad substitution` (`$B:src`, a zsh modifier) before anything ran (the clone's status was unchanged). I re-ran it as a `python3 -I` script, and the kit's HEAVY section now warns about it.
- **No Jira, no HTTP but `gh api -X GET`, nothing to any human, no device, no Azure.**
