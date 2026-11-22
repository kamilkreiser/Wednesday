STARTABLE: YES

# B1931 drafter report (Datasec / NexusAI, lane N-L ROUND 2: the fix round after gate B1925 NO GO)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1931_SEAT-N163_nexusai-lane-nl-round2.md` (813 lines, 97699 bytes, sha256 `f7adee7520b05fdf...`; seat `Datasec/NexusAI-N163`). Sidecar `...round2.md.measured` (111 claims; `stamp_check.py <kit>` exits 0; 47 of the claim lines are marked UNMEASURED-BY-DRAFTER or "see": these are instruction literals the seat runs or produces, verify outputs the drafter did not run, and the Deploy-demo `skipped` read). Unstamped: 5 four-underscore lines (four slots and the last line). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1931/`. Reads ran from 22:42:38 to 23:38 AEDT (`date`). **Seat read load at Step 0:** about 194 KB plus this report (the kit 97699, VERDICT 18685, round 1's STATUS 29258, round 1's kit lines 433-491 and 559-560 20794, B1771 lines 568-589 and 621-649 21788, the CodeQL README and GATE_STEP 5479).

## BLUF
- **The round:** ONE fast-forward commit R on `b1911/nexusai-lane-nl-brand-contrast`, on top of PREV `081f4221` (pushed; main `8858e5d1` unmoved; 0 open PRs; `b1931/*` 0 at origin). Seven paths: `index-styles.css`, `dark-mode.css`, `scripts/derive-brand-tokens.js`, `static/css/tokens.css` (regenerated), `docs/BRAND.md`, the round-1 test file (rewritten whole, 15 to 19 cells) and the counts file. **To keep it one commit with a MEASURED counts file,** the chain makes a scratch commit R0 in a detached tree (never pushed, never a branch), runs every jest step and `--update-counts` against R0, then makes R in `wt` from the same frozen programs plus the measured counts file.
- **F-1 (Major):** chip text `#212529` becomes `#333333` (`--nx-text-strong`, 12.635:1). The generator path works and is MEASURED: the pin goes 22 to 23 with a call-site comment, and `node scripts/derive-brand-tokens.js` regenerates `tokens.css` with exactly one line changed (`x22` to `x23 measured`). At PREV the generator's `--stdout` is byte-equal to the committed file (the control). C1 now requires the chip colour to be a light token value read from `tokens.css`. It is RED at PREV on `#212529` and green at the patched tree. Plant Q1 (the round-1 line put back) is caught by C1 AND by `brand-token-conformance` (the pin).
- **F-2 (Minor):** the repo's rule is BRAND.md R8 (`docs/BRAND.md:744`): a `graphic` ("a bar, an indicator; WCAG 1.4.11") clears 3:1. **No single dark track token clears all four fills** (table below). So the fix uses two tokens:
  - the dark track becomes `#262626`, the dark value of the light track's own token `--nx-surface-raised`;
  - a new rule makes the dark black fill `#8c8c8c` (`--nx-text-muted` dark).

  Every dark fill stop then clears 3:1: black 4.500, magenta from 3.481, cyan from 6.590, yellow from 9.284. Round 1's `#313131` also left magenta's first stop at 2.992. The new cell C5 is RED at PREV.
- **F-3 (Minor):** R5's "it is never text" becomes "never text on a DARK ground" (3.45, 3.13 and 2.78 are the dark page, card and raised grounds). One paragraph adds the light uses (5.44 / 5.16 / 4.58) and quotes the records verbatim. **RD-251's ruling is NOT in CLARIFICATIONS** (0 hits; control RD-349 5), so the paragraph quotes it from the repo's `.tab-button` comment, plus HISTORY.md's "Shipped, and explicitly not ratified as his meaning". This is Q-3, STOP-class. BRAND.md's count table moves 15 to 16 with a note, by its own rule "change it in both places".
- **F-4 (Minor):** the new cells S1 (drag-over) and S2 (file-chosen) composite the state's translucent ground over `.import-section`; S3 proves that the dark panel rule outranks both state rules (specificity). All three are green at PREV by design (the states pass since round 1). S1 and S2 are RED at round 1's BASE, and plants Q5, Q6 and Q7 turn S1, S2 and S3 red at the patched tree.
- **Everything below was MEASURED in real jest 29.7.0 on Node v24.22.2 and in headless Chromium 151, on scratch copies:**
  - new file: 2 red / 17 green at PREV (C1, C5), 19/19 at the patched tree, 11 red / 8 green at round 1's BASE;
  - the 78-file run list: per-file counts equal at PREV and patched except the lane file (15 to 19); the same 29 environment reds (no `.git`) at both;
  - BRAND.md readers and token guards: 134/134 at the final text;
  - 19 plants plus P0 (82 cells): every plant caught, every revert equal by blob;
  - browser at PREV and patched in both modes.
- **Suggested level:** Sonnet, row C2 (`model-routing.md:92`), id `claude-sonnet-5-5`; the launch line has `BRIEF_SEAT_LEVEL=sonnet` in its quotes. The gate after is tier 1 with a rendered leg in both modes (round 2 of 2).

## Facts re-measured (instrument; control)
- **Refs** (`gh api -X GET` under the NexusAI `GH_CONFIG_DIR`):
  - main is `8858e5d11ec101de0a49a819c2d29f4eadf95c40`;
  - the branch is `081f4221f442bbd7ee68be6475f5f64280d558d5`, tree `d9dd23ae...`, parent `8f4b7166...`;
  - `matching-refs/heads/b1931` 0 (control: `matching-refs/heads/b1911` lists the branch);
  - open PRs 0;
  - open alerts 22, in the same six backend/test files as round 1; none in this round's paths.
- **PREV blobs** of the round-1 files equal round 1's STATUS (`1d9889946996`, `45fc7bfded9f`): the tarball control.
- **Generator:** `--stdout` at PREV is `cmp`-equal to `tokens.css`. After the pin, the `diff` is `33c33` only.
- **Ratios** come from `progs/cr.py`, the repo formula (control: `#000` on `#fff` 21.000), and agree with jest's `contrastRatio` and the engine. Dark track candidates against the fill gradient stops:

| dark track candidate | black | cyan | magenta | yellow | all four >= 3? |
|---|---|---|---|---|---|
| `#121212` page | 1.706-2.017 | 8.157-9.075 | 4.309-6.126 | 11.493-12.249 | no |
| `#1c1c1c` card | 1.552-1.835 | 7.421-8.255 | 3.920-5.573 | 10.455-11.143 | no |
| `#262626` raised | 1.378-1.629 | 6.590-7.331 | 3.481-4.949 | 9.284-9.895 | no (yes once black has a dark fill) |
| `#313131` surface-3 (round 1) | 1.184-1.400 | 5.664-6.302 | 2.992-4.254 | 7.981-8.506 | no |
| `#6f6f6f` border-strong | 2.186-1.849 | 2.188-2.434 | 1.156-1.643 | 3.083-3.286 | no |
| `#8c8c8c` / `#b4b4b4` / `#dedede` | | | | | no (cyan/yellow fail) |

  Black-fill tokens on `#262626`: `#6f6f6f` 3.012 (too thin), `#8c8c8c` 4.500, `#909090` 4.740, `#b4b4b4` 7.299, `#dedede` 11.249.
- **Track against its cell ground** in the real table (`index.html:930` `table table-hover`; dark odd rows `#262626`, hover `#313131`): this is decorative in both rounds. Light reads 1.186. Dark `#262626` reads 1.126 on even rows and 1.000 on odd rows (round 1's `#313131`: 1.310 / 1.163). The screenshot `br/B1931_r0_dark.png` shows the odd-row track blending into the row while every fill stays clearly visible.
- **The two F-3 sources:**
  - `CLARIFICATIONS.md:2752-2753` (C-258 question, option, accepted recommendation): quoted verbatim;
  - `index-styles.css:669` (RD-251's recorded words) and `HISTORY.md:7224-7227` ("applied INVERTED ... Shipped, and explicitly not ratified as his meaning").

  The new BRAND.md text scans 0 names (underscore-aware list from `scanlib1114.py:20`, controls fire) and 1 owner-attribution hit (the C-258 citation line). The kit's HOLD 51 makes that the one allowed hit.
- **Composites for F-4:** drag-over 4.8936 unrounded / 4.900 rounded; file-chosen 4.9711 / 4.979; BASE grey 3.130 / 3.180. Cell I1 pins the unrounded values (4.89, 4.97).
- **Chain input table** (each input comes from an earlier step or exists at PREV):

| step | inputs |
|---|---|
| 0, 1 | PREV, the run list (Step 1b) |
| 2 | PREV and the frozen test file |
| 3 | PREV and the frozen programs (produces R0) |
| 4, 5, 6, 8 | R0 |
| 9 | PREV and step 8's counts file |
| 10 | R (step 9) |
| 7, 11 | Step 1's clone |

  CQ-1 and CQ-2 run after step 11, on R0 and R.
- **Ports:** slot 17's band 30880-31519 had 0 listeners (machine-wide control 12-14). Only round 1's kit names it among the SEAT kits of 21 and 22 Nov. The live pane list holds `tuesday` only.
- **Slot names** come from the project's rule (sha256 of the path, first 4 bytes, mod 19; control `b1911-nodot/old11` reads 17): `prev10 probe7 new5 mut9 v30 chk38` all read 17. This prevents round 1's Corrections 1.

## D-decisions (mine, in the kit)
- **D1 (one commit, measured counts):** a scratch commit R0 in a detached tree carries the measured steps, and R is made once from the same frozen programs. There is no amend, reset or second branch commit; R0 is never pushed. A main move is a STOP, not a merge (a merge would make a second commit).
- **D2:** C1 is pinned to `--nx-text-strong` by name AND to light-token membership. Q2 (`#636c73`, a token) is therefore also red. Overruling Q-1 changes that literal.
- **D3:** the plant set adds `css-ratio-comments` and `brand-token-conformance` to round 1's pair. Round 1's P-plants are re-anchored (P5 and P9 text) and all re-run.
- **D4:** the browser harness adds the real table classes, so the dark striped and hover grounds are present. It reads every fill's computed stops against its computed track. It reuses the gate's modal-extraction approach, in my own code.
- **D5:** a run handed zero test paths is refused by the wrapper. My first script ran jest with none, and jest then ran the whole suite (disclosed below).

## Q-questions for Tuesday (each with a default; STOP-class marked)
- **Q-1 (STOP-class: the off-guide fix is the Major).** The chip text colour. **Default `#333333` `--nx-text-strong`** (12.635), with the pin going 22 to 23 and `tokens.css` regenerated (measured; the generated diff is one line). Alternatives: `#636c73` `--nx-text-secondary` (5.353, no pin, no generated file, two fewer paths) or `#00719f` (5.437; blue chip under blue labels). Changing it means editing `CHIP` in `apply1931.py` and C1's token name.
- **Q-2 (STOP-class: two tokens where the commission said "the track or the fill").** **Default:** dark track `#262626` plus dark black fill `#8c8c8c`, so every dark fill clears 3:1 (BRAND.md R8). Alternative: only a black fill (`#b4b4b4` 6.274 on the kept `#313131`), which leaves magenta's first stop at 2.992. A dark black fill of `#b4b4b4` instead of `#8c8c8c` is a one-literal change.
- **Q-3 (STOP-class: attribution text in a product document).** RD-251's ruling is not in CLARIFICATIONS, so the commission's "as quoted in CLARIFICATIONS" can only be met for C-258. **Default:** the frozen paragraph (`apply1931.py` B2). It quotes RD-251 from the repo's own `.tab-button` comment and HISTORY.md's "not ratified" sentence, quotes C-258's question and recommendation verbatim, and states no rule. Alternative: drop the RD-251 quote and keep only the measured light uses plus C-258.
- **Q-4.** BRAND.md's count table moves `text-strong` 15 to 16 and gains a five-line note (the RD-333 / RD-840 precedent). **Default yes.**
- **Q-5.** HOLD 51: the owner-attribution scan allows exactly the one BRAND.md citation line. **Default yes.**
- **Q-6.** The LIGHT toner fills on the light track stay below 3:1 (cyan 1.741, yellow 1.290, magenta 2.579). This is pre-existing and outside the gate's findings. **Default:** leave it as a candidate ticket (LEFT FOR OTHERS 2).
- **Q-7.** The one-commit mechanism (D1, scratch R0). **Default yes.** The alternative is to allow a second counts-only commit K.
- **Q-8.** Main moving during the run is a STOP rather than a merge. **Default yes.**
- **Q-9.** Slot 17 and band 30880-31519 are reused, under new tree names. **Default yes.**
- **Q-10.** The gate after is tier 1 with a rendered leg in both modes; a NO GO goes to the product owner as a card. **Default yes.**

## UNMEASURED
- **Not run by the drafter:** the full `npm run verify` and `--update-counts`. The counts pair 6235 / 394 is PREDICTED from per-file counts over the 78-file frame. Readers outside the frame were not run; the seat's verify is the net.
- CodeQL was not run (predicted rc 0; no product JavaScript is added).
- The five git-dependent files read red in my no-`.git` trees at both PREV and patched (environment) and are expected green in a clone.
- **Not rendered:** the live page (CDN Bootstrap, page scripts, CSP) and other viewports.
- The compare read of the branch is the gate's (`ahead 4, behind 0`), not mine.

## Outside-the-fences disclosure
- **Read-only:** `gh api -X GET` (refs, the commit, the open PRs, alerts, the tarball of `081f4221`); `CLARIFICATIONS.md` by `grep`/`awk` only (lines 2062, 2067, 2412, 2751-2754); the project's Briefs STATUS last lines; `.tools/b1911/` listing and `slot.py`; `scanlib1114.py:20` by `sed -n 20p` into scratch (the names are not printed anywhere). No Jira, no `decision_queue.sh`, no `briefs_staged`, no scoreboard, no `_ledger.md`, no WEDNESDAY/FRIDAY tree. The gate's scratch (`s311/g1925`) and round 1's drafter scratch (`s310/d1911`) were read, never written. Round 1's BASE stylesheets came from `s310/d1911/tree`; their blobs are `eb79bc10cff1` / `e90297efa71f`.
- **Wrote only:** the kit, its sidecar, this report, and scratch under `fleet/state/s311/d1931/` (tarball extract, trees `head p0 p1 p2 b0 m mq_Q5 mq_Q6 mq_Q7`, programs, jest and browser outputs). Nothing was deleted. Nothing was written in the project, Jira or GitHub; nothing was sent to any human.
- **Jest and Chromium** ran from `.tools/b1911/clone/node_modules` (read-only) against scratch trees, with `--maxWorkers=2` and my own cache, while no NexusAI lane held the jest lock (`queue-jest` empty, no `Datasec/NexusAI-*` pane).
- **My fault, disclosed:** at 22:53 a run-list script failed on bash 3.2's `mapfile` and handed jest zero paths, so jest ran the whole suite in the scratch `head` tree for about 2.5 minutes. I stopped it by pid (the script, the jest parent, two orphaned workers and one child). Afterwards there were 0 listeners in any test band and 0 of my processes left. The wrapper now refuses an empty list (control rc 2), and the kit carries that refusal.
- **One plant anchor** (Q5) matched twice on its first run. `plants1931.py`'s assert refused it before any write (blob unchanged), and Q5 and Q6 were re-anchored on their selector lines.
- The kit names no person and no decision-card id. It quotes "his meaning" (a pronoun) inside the frozen BRAND.md paragraph.
