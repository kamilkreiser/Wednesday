STARTABLE: YES - once the new card is ruled and the slots are filled; stamp_check exits 0 (80 of 80 claims measured); no infrastructure step is needed (30 of 30 infra/CI/script blobs equal), so the kit is a package swap with a read-only settings guard.

# B1792 drafter report (SEAT-D69 kit, MPS hosted deploy of main debb5e28)
Drafted 2026-11-20 18:00 to 18:13 AEDT (`date` printed 18:00:30 ... 18:12:42) by a read-only Opus drafter for Tuesday (seat s299). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/d1792/`.

## BLUF
- Files: kit `2026-11-20_B1792_SEAT-D69_mps-hosted-deploy-main-debb5e28.md` (56,901 B, 129 lines, ASCII, 15 four-underscore lines) + `.measured` (80 lines, 0 TODO; `stamp_check.py <kit>` rc 0); `2026-11-20_B1792_CARD-FACTS.md` (10,099 B, ASCII, 0 B-numbers and 0 card ids by scan, control: the kit reads 27 and 2); this report.
- **Byte sum of the kit plus its READ WHOLE list: 114,368 B** (kit 56,901 + B1755 STATUS 48,162 + C-185 lines 3526-3542 9,305). No Tuesday-stamped kit is on the seat's list.
- **No infrastructure step:** every path under `infra/` (8), `.github/` (1), `scripts/` (21) has the same blob at debb5e28 as at 50d2a471 (30 of 30; control fires); the 13 changed paths are all under `web/src/`. B1755's apply already brought the live settings to the committed 18 names (its M10/end dump). B1755's run did: backup, what-if, one apply (+Templates path), the swap, checks. This kit: backup, the swap, checks; no `az deployment`, no client id handled.
- **Predicted settings difference: "added none; removed none; changed none"** against `B1755_evidence/30_end_appsettings_namehash.tsv` (18 rows; names set-equal to the committed list, read by first column only). The swap writes no setting (`deploy-from-ci.sh` holds `appsettings` 0 times, control README 3). The kit keeps a read-only guard (G1 before, G2 after) with the B1755 dump comparator and its three controls.

## Facts re-measured (instrument, clock)
- main `debb5e28f7bbd4e0f641a829eb353ac356afdd81`, 0 open PRs (gh GET 18:01:42); compare 50d2a471...debb5e28: ahead 2, behind 0, 13 files, merge base 50d2a471 (18:01:44); #221 565ba142 4 paths, #222 debb5e28 12 paths, one parent each; tree 8c937570.
- CI: 8 of 8 success; ci run 44677646353, CodeQL 44677645476; artifact 14602844323 expires 2026-11-27T05:12:52Z; way-back artifact 14515692831 expires 2026-11-26T09:30:43Z (18:02:31). Analyses by commit_sha: debb5e28 4 (results 0), control 565ba142 4, zero-sha 0; open alerts 0.
- Package: mpscalc.zip sha256 f75b5e3c...b9f7, 3,331,166 B, 51 files; verify rc 0, wrong-commit control rc 1 (18:03). File list vs 50d2a471 package: 45 equal; 4 changed (3 DLLs: 96 bytes each = commit stamp + 20 identity bytes; index.html); 2 swaps (`index-BmiOY3BZ.js`->`index-DB6HI3fz.js`, `EntraRoot-CBewh7rM.js`->`EntraRoot-Dx82EsgF.js`). New bundle holds the three words 1 each, old 0.
- Words census (DERIVED, program over the three production files): new visible literals = the three words only; plus the printed-line pattern (`ProposalDocument.tsx:199`); everything else code (control fires).
- Local repo: lacks debb5e28 (control 50d2a471 `commit`), sshCommand still names Laptop-DEV, HEAD b03/api, not shallow (18:04:54). `.tools/wt-B1755-release` HEAD 50d2a471. No B1792 STATUS or qa folder yet.
- Last-line loop over 486 STATUS files: newest DEPLOYED is B1755 (15 DEPLOYED lines in all).
- Cards (show, one id each, 18:01:27): `mps-278-unpriced-option-three-words-1120` ruled a 12:52:39 (project string `Datasec/MPS Calculator`); `mps-hosted-deploy-main-50d2a471-1119` ruled a, delivered `DEPLOYED 50d2a471...`.
- Live panes holding MPS (18:06): 1, `Datasec/MPS-M169` (B1790 build seat; its kit: no merge, no deploy, `mpscalc-showcase-rg` 0, az-verb 0, control MPS 24).

## Chain-step inputs (each produced earlier or existing at BASE)
| Step | Inputs | Source |
|---|---|---|
| 0 | stamped kit, card ids, main, CI, login reference `B166_evidence/00_c2.txt`, c2_1755.py | BASE / Tuesday's stamp |
| 0W | words1755_0w.py, classify1755.py, compare 50d2a471..debb5e28 | BASE (.tools/qa-B1755) / one fetch at target asserts |
| 1 | b1755.py, cmpdump1755.py, B1755 30_end_* evidence, 50d2a471 package folder | BASE |
| 1P | Step 1 dump, 30_end_appsettings_namehash.tsv, names list at debb5e28 | Step 1 / BASE / Step 4 worktree or gh raw |
| 2 | Kudu reads, backup-B1755 manifest | Step 1 / BASE |
| 3 | Step 2 backup, counts1755.py | Step 2 / BASE |
| 4 | the one fetch, worktree, CI artifact, filelist1755.py, way-back folder | target asserts / BASE |
| 5 | Step 4 package, C-2, Step 1 dump, Step 2 backup | Steps 1, 2, 4 |
| 6 | Step 1S token (only if run) | Step 1 |
| 7-8 | Step 4 package, Step 5 check download, leak1755.py, secret tool | Steps 4, 5 / BASE |
Note: Step 1P names the committed list "at debb5e28": before the Step 4 worktree exists the seat reads it with `gh api -X GET` raw (the blob equals 50d2a471's, so the copy in `.tools/wt-B1755-release` is also valid).

## What differs from B1755 and why
1. No infrastructure step, no what-if, no M1-M10, no client ids, no budget read: the infra is blob-identical and already applied.
2. Settings guard G1/G2 against B1755's end dump (0/0/0) replaces the apply comparison.
3. Slot WORDS now covers the printed-line pattern (`approved as built` / `not approved`); the three words are ruled by the 1120 card, read at Step 0.4.
4. Backup adds `data/templates/` (the folder exists since the B1755 apply).
5. Way back is now the 50d2a471 package in `.tools/wt-B1755-release`.
6. Corrections carried from the B1755 run: C-2 reference is `B166_evidence/00_c2.txt` (B1755 kit named B1607's; its tool used B166's); az is 2.92.0; deploy answer owner tag masked in evidence; no file may hold an id (expected 0 now that no what-if/create runs); leak tool label fixed; no `rm`; expected publishxml pairs 10 as measured; C-entry number left to the records pass.
7. Activity-log baseline 2026-11-19T22:36:00Z (after B1755's last check), control 22:29Z.

## STOP list (kit S-1 to S-22)
Unfilled slot; card not ruled as S0 / earlier cards not as quoted; S2 not debb5e28; main moved; production; disk/other az pane; slot values, WORDS not approved, unruled string; CI/package; target asserts (incl. any path outside web/src); login expired (two lines for the product owner), C-2 unequal, auth error; site not 50d2a471 / already debb5e28 / foreign write; G1 difference; backup unproven; file list property / way-back unverified; deploy rc 1; rc 3 unproven -> way-back rule; G2 difference; template warning or Start refused; test login refused; synthetic template not listed; end-check / leak / secret; hard stop.

## Corrections to this commission
1. B1755's STATUS has no Corrections or Deviations section and stopped 0 times; its open items are under "Fixed / Deferred / Open" (lines 230-233) and the BACKLOG candidates (213-223). I read those instead.
2. The 1120 card's project string reads `Datasec/MPS Calculator`, not the full project name (the reason C-185 refused to cite the C-152 ruling); C-186 cites it anyway. The kit says this is not a STOP (Q4).
3. PR #222's title carries MPSCALC-278 only (GitHub read); MPSCALC-426 is in C-187, not the title.
4. DRAFTER_RULES paths name `/Volumes/Laptop-DEV/`; read as `/Volumes/Datasec_DEV/`.
5. `analyses?sha=` does not filter (20 for both commits); counts are by `commit_sha` instead.

## D-decisions (drafter's, in the kit)
D1 no infra step (above). D2 keep the read-only guard anyway: cheap, and it catches a hand-set since 09:36. D3 carry TEMPLATE-CHECK (C-185 owes it; paired with SELLER-CHECKS = run, as the last card did). D4 no budget read (the swap cannot touch it). D5 seat reads only B1755 STATUS and C-185 whole.

## Q-questions for Tuesday (each with a default)
- Q1 card recommendation: default option a (deploy now, line approved as built, seller checks skipped). If you read C-45 as needing the separate pack first, recommend c.
- Q2 G1 any difference STOPS before any write: default yes.
- Q3 template restart only after W2, once: default yes.
- Q4 the 1120 card's project string is not a STOP: default yes.
- Q5 S8: R-1 to 50d2a471 allowed? default NO (roll forward only, as last time).
- Q6 timing: the live B1790 build seat may land and move main; default: stamp and launch before any MPS landing, else re-cut.

## UNMEASURED
Live settings, store and activity log since 09:39 AEDT; the az login's validity; the test login (expired as of 16 Nov); real code lengths and real lines with codes; other browsers; a rendered proposal on the hosted site; who holds which role today; the 20 identity bytes per DLL (DERIVED as build identity fields, not decoded).

## Outside-the-fences disclosure
No az, no request to any hosted host, no build, no test, no mail, no Jira, no git or GitHub write; gh `-X GET` only under the project GH_CONFIG_DIR; local git read verbs only (`cat-file`, `config --get`, `rev-parse`, `show`). Ran the project's `deploy-package.py verify` (read-only) on a scratch copy, as B1755's drafter did. `decision_queue.sh show` on two exact ids; no `list`. Read the B1790 kit only by four counts (pane check). Read nothing under `.local/`, no `.env`, no price book; read the settings dump's first column only. Wrote only the three outputs and the scratch folder; deleted nothing.
