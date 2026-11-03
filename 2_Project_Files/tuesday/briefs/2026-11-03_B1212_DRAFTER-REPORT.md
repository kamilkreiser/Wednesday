STARTABLE: YES (once Tuesday fills the 9 stamp slots; no live Datasec/MPS pane, no heavy.lock or light.lock under .tools/*, load1 2.21, 218 GiB free)

# B1212 drafter report: SEAT-M90, MPSCALC-359 round 2 (tests only), branch b1194/mps-359-persite-no-sites-refusal

Kit: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1212_SEAT-M90_mps-359-round2-persite-rows.md (74 lines, 9 slots; ASCII: `LC_ALL=C grep -c '[^ -~]'` 0; slots `grep -c -E '_''_''_''_'` 9).
Clocks (date, AEDT, 2026-11-03): 13:56:20 start, 13:56:37 origin reads, 13:58:02 hand figures, 13:59:00 last origin read. Nothing is later than these.

## BLUF
- Round 2 of 2 on the class (NO GO 1 before, B1207). One commit on the existing branch, ONE file (ComponentQuantityRuleTests.cs), 5 new results (4 methods, one a 2-case Theory) pinning the 5 surviving plants GX1, GX3, GX4, GX5, GX7. No product byte.
- **Branch vs main: the commit goes on the branch AS IS; main is not merged in.** Evidence below. No rebase, no merge, no force.
- No row for GX8 (equivalent) and none for Notes B1207-7..13 (product-owner or word items).

## Facts re-measured (instrument, control)
- Branch head: `gh api -X GET repos/datasecau/MPS-Commercial-Calculator/git/ref/heads/b1194/mps-359-persite-no-sites-refusal --jq .object.sha` = 0afa8e053491c92e41b23b6844b9193aab9dd028. Control: same call on heads/main = 5a483a908a1766591adc77279d657dbd59d5dd7b (differs, as expected). Open PRs (pulls --jq .number): 121 120. `matching-refs/heads/b1212` length 0; control `heads/b1093` length 1. (`matching-refs/heads/b1` also lists b12/api-hosted-entra and b12b/hsts-linklocal-hop: they do not match the prefix b1212.)
- Blob equality with the gate: `git hash-object` of the raw files fetched at the head: test file 782707c3 (962 lines), PurchaseCalculator.cs 0f2bf14c (1060), PurchaseInput.cs 14be6902 (170), PurchaseRecomputation.cs 60653e01 (266), ENGINE.md 5482b1e0 (213): all equal to the gate's Step 1 list.
- Head commit: subject "Count a per-site line once per site with a device and refuse the quote when none has one (MPSCALC-359)", parent e49630b9 (commits API). `compare 987eb25c...0afa8e05`: ahead 2, behind 0, the five paths.
- Main's movement: `compare 987eb25c...5a483a90` files = docs/ENGINE.md, RentalRecomputation.cs, TemplateIsolationTests.cs, VolumeBasisTests.cs, contract.sync.test.ts. Filter `ComponentQuantityRuleTests|PurchaseCalculator|PurchaseRecomputation|PurchaseInput` over them: 0; control, same filter over the branch's own compare: ComponentQuantityRuleTests match count 1.
- ENGINE.md overlap (`diff` of raw base 987eb25c vs main 5a483a90, and base vs head): main changed lines 40 (R-29) and 160 (X-34); the branch changed 166 (X-40), 169 and 170 (X-43, X-44) and added 171 (X-45). Disjoint rows. `git merge-file -p <head> <base> <main>` rc 0, `grep -c '^<<<<<<<'` 0. (Control for the diff instrument: the head's rows 160 and 166-171 print under `grep -n -i` with the X-34/X-40/X-45 labels.) The gate's MAIN-MOVE section (STATUS lines 114-167) says the same: merge clean, tree equal to its squash, Engine 734 / Import 196 / Api 3359, 0 failed, 1565/1565 and 20,803/20,803 on 5a483a90; it also records that plants were NOT re-run on the new main because #154 touches neither planted file.
- Code lines at the head (`grep -n -F` over the raw files): PurchaseCalculator.cs :181 per-device extension, :184 per-site extension, :187 poolQty, :202 TierForPool, :206 line results, :310-area Block, :376 `if (!sectionIds.Contains(l.SectionId))`, :378 UNKNOWN SECTION, :398 the refusal (`PerSite && sectionIds.Contains(l.SectionId) && SitesWithDevices(...) == 0`), :583 SitesWithDevices (`x is not null && x.Devices >= 1`). PurchaseRecomputation.cs :54 (its own count, `x.Devices >= 1`), :55 QuantityOf, :72 use. Test file: Group :56, Calc :62, Ok :65, L :72, Book :75, Sited :746, AssertRefusedAt :750, AssertPerSiteLine :763, AssertReconcilesUpfrontAt :906, last reconciler row :933, guards comment :940. CI: ci.yml :42 and :43 (awk NR over raw), Directory.Build.props :6 TreatWarningsAsErrors true. CLARIFICATIONS.md :774 (squash, head pinned), :2218 (red-first). Model rows model-routing.md :92 (C2), :93 (C3), :108 (G1); models_latest.json :17 claude-opus-5-5.
- Panes: `tmux list-panes -a -F '#{@cockpit_name}'` lines matching Datasec/MPS: 0; matching -x Datasec/MPS-M90: 0; control `tuesday` 1. Locks: `ls .tools/*/heavy.lock .tools/*/light.lock` no match (zsh "no matches"; control `grep -c light.lock .tools/b1194/heavy.sh` = 1). `.tools/b1212` absent (ls -d fails; control .tools/b1139 exists). Sources present in .tools/b1194: heavy.sh hb.sh env.sh ci-dotnet.sh jira_read.py scratch/{plant.py,run_plants.sh,trx_count.py} (8).
- Listening ports (lsof -nP -iTCP -sTCP:LISTEN): *:49152 *:5000 *:59869 *:7000 *:8770 127.0.0.1:49166 :49168 :49171 :9660-9662. None assigned or needed (Engine tests bind no listener, per round 1's scan; not re-run). Word-boundary scan of today's SEAT kits for the path: only the B1194 kit (the builder of this branch), finished; B1203 lists VolumeBasisTests.cs only.

## Hand figures (python decimal, /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/8ade374d-0a0f-45f0-bf14-6cca67fc2a0e/scratchpad/hand.py, `python3 -I -B`; section percent 0.2: manual d 100 -> 120, o 5 -> 6; DevA 900 -> 1080, 1000 -> 1200)
| Row | Figures at the head | Under its plant | Code line each relies on |
|---|---|---|---|
| 1 GX1 | N 3, sites 1/0/2: S 2; d x3 cost 300 sell 360; o per site q3 -> 6, cost 30 sell 36 margin 6; quote 396 / 330 / 66 | S 1: option 3; reconciler 378 / 315 / 63 (the gate printed 378 vs 396 for sell) | PurchaseCalculator.cs:583 (S), :184 (extension); PurchaseRecomputation.cs:54-:55 (reconciler); plant at :54 |
| 2 GX3 | Group 7, line 2 in section zz: one Blocking UNKNOWN SECTION, "Line 2 names section zz, which the quote does not have.", bomLines[2].sectionId | the call throws InvalidOperationException at `input.Sections.First(...)` (:398) | :376, :378, :398 |
| 3 GX4 | Group 7, no sites, credit per-site o: refused, note, bomLines[2].quantityRule | prices sell 840 cost 700 (line counted 0) | :398 |
| 4 GX5 | same, included | same 840 / 700 | :398 |
| 5 GX7 | N 10, sites 3/3/4: S 3; DevA per site q4 -> 12; pool 12 = Growth: unit cost 900 sell 1080, line cost 10,800 sell 12,960 margin 2,160; 12 devices | pool 4 = Core: unit 1000, cost 12,000, sell 14,400, margin 2,400 (reconciler still agrees: trusts recorded unit cost) | :184 before :187 (pool), :202 (tier); Growth from 10 per the existing row at test :319 |
Not the gate's figures for row 5: the gate's 13,014 / 10,845 includes a book option whose pricing I cannot derive from the fixture here; mine is the device line alone (see Q-3). Row 1, 3, 4 equal the gate's (396 / 330 / 66; 840 / 700).
Credit and included lines in rows 3 and 4 never reach arithmetic at the head (refused), so no sign or rounding path is relied on.

## D-decisions
- D-1 Branch vs main: on top as is, no merge (evidence above; the commit touches a file main never touched).
- D-2 Rows: one Fact each for GX1, GX2, GX5; one Theory (credit, included) for GX4/GX5-plants; each in the file between the last reconciler row (:933) and the guards comment (:940). Rows are lines to add, no helper edited.
- D-3 Plants: the kit names the five anchors by line; GX7 is left for the builder to write (it must yield Core 1000 / 12,000 / 14,400). Round 1's twelve plants (PA..PL) re-run via run_plants.sh with the new file; the gate's 14/20 included GX plants which the builder does not have in its tools, so the gate re-derives them.
- D-4 Hard window 90/180 minutes as the sibling round 2 (M89): 5 new rows, 5 new plants, 12 old plants (~2 min each on a free machine) fit; stated not after the stamp's hard stop.
- D-5 Naming: no "GX", PA.., B-numbers, names or card ids in rows, comments or the commit message (kit property, STANDING line 1, step 8b).
- D-6 Partition: no MPS seat live; M90 is the only builder; the gate G316 and records R157 are closed.

## Q-questions for Tuesday (each with a default)
- Q-1 Routing: Opus C3 as round 1 (model-routing.md:93), or Sonnet C2 (:92) since this round is test-only? Default: Opus C3 (round 1's row; the gate is tier 1 and a wrong hand figure is a STOP either way).
- Q-2 Confirm D-1: the round-2 commit goes on the branch as is, no merge of main? Default: yes, as is.
- Q-3 Row 5 uses the device line alone (cost 10,800 / sell 12,960) rather than the gate's book-option figures 13,014 / 10,845, which I could not derive from the fixture; accept? Default: accept (the plant GX7 is killed either way; the gate re-derives).
- Q-4 The ENGINE.md sentences the gate calls short (X-44 "as the unset quote does", X-45's refused-shape list; Note B1207-11) and the three-rule INVALID QUANTITY RULE text (Note -7) stay out of this round? Default: stay out (tests only; they are product-owner and word items; the cap is this round).
- Q-5 Hard stop to write in the stamp: not after what clock? Default: 17:00 AEDT today (the previous M88 kit's), launch window from the stamp until 15:30 AEDT, one waiter at load1 below 7.
- Q-6 If the builder's own run finds a hand figure the head does not meet (a product defect), it STOPs with both numbers; confirm no round-2 product fix is authorised without you. Default: confirmed.

## UNMEASURED
- Whether the new rows turn any of round 1's plants PA..PL differently (guesses only in the kit); whether Assert.Single(r.Issues) holds for the unknown-section row (the gate says "exactly one" and the code at :376-:398 gives one, but I did not run it); the builder tools' plant.py and run_plants.sh contents (not read); Engine tests' listener scan (round 1's, not repeated); hosted CI and CodeQL (no PR).
- Row 5's reconciler assertion: AssertReconcilesUpfrontAt asserts Compared 5 upfront measures; not run for a book device with tier (the existing row :225 shows the book-device shape prices).

## Outside the fences (disclosure)
Read-only: gh api -X GET under the project's GH_CONFIG_DIR (refs, pulls, compare, raw contents, commits); local reads of the project's 1_Project_Definition (gate STATUS, evidence, CLARIFICATIONS lines) and listings of the project's .tools (names only; no file inside read); tmux list-panes, lsof, df, uptime. Raw files saved to my scratchpad (the scratchpad also held other drafters' files, untouched). No decision_queue call, no Jira call (the ticket's state is the gate's read, RELAYED; the kit re-reads it at Step 1), no fetch, no git ref write. The shell-hook advisories about case-sensitive greps were noted; the counts above that matter were run with -i or with controls.
