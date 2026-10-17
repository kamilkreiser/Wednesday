# B167 drafter report · 2026-10-17 10:58 AEDT · for Tuesday
Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B167_SEAT-V3_mps-gate-r2-classes-carepacks.md` (271 lines). It is NOT launched.

## BLUF
- **SHAs measured** (`git --no-optional-locks ls-remote origin` at 10:43:55 and again at 10:57:51, the same both times; `cat-file -t` = commit ×4):
  - T `b103/mpscalc-158-target-whatif-noaudit-r2` = `88c84cd449e07565b5856d606df703b4bc4638b8` (= `B103_STATUS.md:463`)
  - CL `b103/mpscalc-142-155-item-classes` = `b50441f877d8ea8d514ba0e524ffafbd432858d1` (= `:464`)
  - CP `b104/mpscalc-140-care-packs` = `d355620ede35cfe073b1984492b7a7a76684836d` (= `B104_STATUS.md:381`)
  - `main` = `ed72606842474f69c435a375f882eea1a15be315` (#74, a one-parent squash over `12f8e56`; tree `77b40d86` = B165's gated C tree)
  - All three have merge-base = main and are 0 behind (7 / 9 / 8 ahead), so each alone is a fast-forward. Parentage checked: `0af733d` = `f1a4b21` + `ed72606`; `45a64da` = `cba5121` + `ed72606`; `d355620` = `46df44a` + `ed72606`, and its tree equals `46df44a`'s (`0b0e433d` both), so lane E's "0 files changed" is true.
- **T changed no product code.** Every `src` hunk of `diff ed72606 88c84cd` equals `diff 12f8e56 f1a4b21` (diff of the two hunk sets, rc 0). `diff 0af733d 88c84cd` touches the test (+59) and the two header files only. The contract and API.md blobs at T (`e240e49d`, `de9d8beb`) are B165's auto-merged pair blobs.
- **Conflicts measured** (throwaway shared clone, `merge-tree --write-tree`):
  - T and CL conflict in either order in `SOURCE.txt` + `schema.ts` only: one hunk each, header lines 2-3, markers at `schema.ts:2,5,8`. Both orders auto-merge `openapi.json` and the snapshot to the same blob `6b8f5c91`, and `API.md` to `50e62cb4`.
  - CP is clean with T (`89070719`) and with CL (`28608269`) in either order. It shares no file name with either and touches no contract or generated file.
  - Triples (T+CP)→CL and (CL+CP)→T give the same two header conflicts and nothing more. The (T+CL)→CP orders were not built, because they need a sync-contract resolve first; the seat builds them.
- **My order reading (the gate decides): CP → CL → T.** CP never needs a regen. Putting CL next unblocks lane E's care-pack class line (OPEN a). T is last because nobody stacks on it, so it absorbs the header regen, and it is also the branch that may drop out (round 2 of 2).

## Traps found (each is written into the brief)
1. **T's new test has 5 rows; B165's probe had 7.** The rows are unitCost, yieldPages, partNumber, added and removed. Re-order and description have no row (`whatif.py:148-154` vs the theory added by `fbec080`), and the test sets the mono target only. Lane D proved red using the gate's own `mutate165.py T-iiib` (`B103_STATUS.md:443`). The brief therefore has the seat build one mutant per row. **I set the grading:** a survivor on a row that ADDENDUM-8 asked for is Major, which makes T NO GO and T does not ship. A survivor on re-order or description is REPORT + Minor. Overrule this if you want strict B165 rules.
2. **Red-first of the new test at `ed72606` is red for the wrong reason.** At main, targets are audited, so it goes red on "no target in the entry" and not on B165-1. The T-iii-b run is the real proof, and the brief says so.
3. **CL vs the overlay's class rules.** Lane D says "an overlay file stores the class number" (`B103_STATUS.md:401`). But `CatalogueOverlayStore.cs:465-466` and `:481` (`allowIntegerValues: false`) read classes by name only. Meanwhile PRE-1 (`deploy-package.py:456-464`) passes an int from 0 up to the class count (`by_number`). So PRE-1 may pass a number that the app refuses at boot. That is pre-existing for 0-5, and CL extends it to 6-7. The brief has a PRE-1 vs app-boot matrix.
4. **`deploy-from-ci.sh:24-26` takes `PKG` from its own checkout, not from the sha it deploys.** A CL deploy run from an older checkout would apply the 6-class list. This is REPORT only for Kam's deploy card, and the seat never runs the script.
5. **The care-pack class gap (OPEN a).** 142's acceptance says "care-pack rows (T05) carry it". CP imports care rows as `ItemClass.Service` (`PurchaseCatalogue.cs:148`), and CL adds no importer line. Lane E plans the one-line change for "whichever lands second" (`B104_STATUS.md:323`). Neither branch has it, so on the triple `?class=carePack` lists no book rows. The services subtotal should be identical either way (X-31 groups both as 3). MPSCALC-142 cannot close until that line lands.
6. **Rollback one-way doors (OPEN c).** An overlay with a carePack row, opened by main, is refused at boot by reading. A CP reference store opened by main has its care rows silently dropped: there is no `UnmappedMemberHandling` in `ReferenceStore.JsonOptions`, and the format string is still `/1`. REPORT for the deploy card.
7. **CP edited two pre-existing expectations.** B42-e08 changed from F to V. B42-e07 keeps F, but now for an unknown device rather than a key collision, so its name no longer matches what it tests. The allow-list assertion also changed. The brief grades a lost document-level collision guard (Major if nothing replaces it, Minor if it is replaced at key level only).
8. **Key stability is a Blocker check.** Every pre-B104 key must be byte-equal on CP vs main, or stored quotes stop resolving. The brief adds a collision table and an escape-order mutant.
9. **The real-book parity numbers are claims only.** These are 509 rows, 371 SKUs and 2,933 agreeing cells (`B104_STATUS.md:37-38`, `:354`). They come from `.local/`, which the seat never opens, so they are UNMEASURED. The seat plants its own synthetic workbook, including a sentinel in BID G/H/I.
10. **Stale docs made stale by CP but not edited by it:** `API.md:215-216` ("default #13: care packs … are manual items") and `openapi.json:361` (book rows "devices, options, software"). These are Notes.
11. **Names.** The Jira labels for 140/142/155/158 carry a person's name, and the 155/158 descriptions carry a client quote code and a competitor brand. The brief tells the seat to quote only the "Acceptance check:" sentence. B104 STATUS's title line carries a name, and the brief says never to reuse it. A case-insensitive grep of the brief for those names returns 0, against a control of 10 hits for "kam".
12. **Shell traps I hit myself:** zsh `$h:w…` history modifier (10:45), and macOS bash 3.2 has no `declare -A`. Both are written into HOLDS.

## Shared machine (measured)
- **Heavy slots:** none exist (`ls -d .tools/heavy-slot*`: No such file, at 10:48:00 and 10:57:51), so all three are free. The seat uses B165's `slot.sh` mkdir 1→2→3 sequence, one slot at a time. Lane D (`%17`) and lane E (`%18`) are alive and will compete for slots.
- **Ports 6820-6829:** `lsof` rc 1 at 10:48:00 and 10:57:51, and `6700-6999` rc 1 at 10:48. B165 used 6810-6819 and released it. No 10-16 or 10-17 brief names 682x (a grep finds only sha substrings).
- **Load1:** 11.81 (10:43), 16.20 (10:48), 11.32 (10:57).
- **Pane:** `Datasec/MPS-V3` is free. The `cockpit.sh status` MPS panes are only `MPS-LE` (%18) and `MPS-LD` (%17); B165's `MPS-V2` is closed.
- **GitHub:** PR #75 (`b104/mpscalc-deals-won-list-title` @ `c5751ff`, tier 2) is the only open PR. It shares no file with the three, but it is the likely main-mover during the gate. main `ed72606` checks are 8/8 success.

## UNMEASURED by me
- Any build, test, API run, `sync-contract.mjs` resolve, or the (T+CL)→CP triple orders.
- Whether the r2 regen reproduces byte-equal from `0af733d`. The header and blobs are consistent, but I did not regenerate.
- The PRE-1 vs app-boot mismatch. It is from reading only.
- `info.version` at the heads (I did not read `openapi.json:5`).
- Real-book anything.

## Choices you may want to overrule
- The T row-mutant grading (trap 1).
- The pre-granted main fetch, kept on B163 ANSWER-1 terms as in B165.
- PRE-1 mismatch on a CL value set at Minor rather than Major.
- Store-compat 5xx set at Major.
- The CP edited-test grading (Major if nothing replaces the guard, Minor if replaced at key level).
- The seat is allowed to stop building triple orders once their trees are shown equal.

## Instruments
- Read verbs only on the project checkout (`ls-remote`, `log`, `show`, `diff`, `cat-file`, `rev-parse`, `rev-list`, `merge-base`, `grep`, `ls-tree`), all `--no-optional-locks`.
- Throwaway clone at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2392c438-09c4-4ba2-9b32-b68afb3a6e21/scratchpad/b167clone` (`--shared --no-checkout`, push `DISABLED`). Only `merge-tree` and two scratch `commit-tree` objects (`d42d0b6`, `f780740`) ran there, never pushed.
- `gh api` GETs (open and closed PRs, check-runs) under the project's `GH_CONFIG_DIR`.
- Jira GET ×4 (140/142/155/158) with the project's `.env` read by name inside a Python client. No secret was printed.
- No HTTP to the hosted site, no az, no fetch, no write under `!CODING`.

## Exact launch line
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-V3 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B167_SEAT-V3_mps-gate-r2-classes-carepacks.md'"
```
Before launch: re-read the four pins, check that `MPS-V3` is still free, read the slots and load, decide on trap 1's grading and the fetch, then re-stamp the SELF-CHECK line.
