# B328 drafter report (SEAT-W14, Composer, K1..K10 rulings into the records)

Drafted 2026-10-20 14:00 to 14:08 AEDT. Read verbs only. Nothing was run, built, written or sent outside the two files named by Tuesday. Brief: `2026-10-20_B328_SEAT-W14_composer-sro-vic-K-rulings-records.md` (one slot, STAMP_TIME; `grep -c '@SLOT:…@'` = 1).

## Measured facts (MEASURED = the drafter ran it, read-only)
- Root `main` = `0d2d8b5d2ad4c24a5fe1b0362dc65b8f7f15a43d` (B321's fold of `records/b301`). `records/b321` = `dca7a220b68080a0df321c77602bfc2735225cd3`, 1 commit ahead, `merge-base --is-ancestor records/b321 main` rc 1: **NOT folded**. Newest records branch: `records/b321`. No `records/b328*`.
- `git diff --name-status main records/b321`: 52 paths, 49 A + 3 M (BACKLOG, CLARIFICATIONS, history; all 3 clean in the root). All 49 A paths are untracked in the root: 48 byte-equal; 1 differs (B321 STATUS, root = committed 20,216 B + After block = 23,446 B, append-only True, control False). 1 root-only evidence file (`refs-after-commit.txt`, 30 vs 29).
- On `records/b321`: C-84, C-85 last (C max 85); BACKLOG 352 ids, rows #328..#362 = 35 `SRO_VIC` rows; State cells read whole (30 name a K card; #340, #341, #342, #344, #345 do not).
- sha256: plan `4c5d3014…ed0`, gap analysis `d35f1a04…41ad` (both = B321's values); B321 STATUS root `b2f5146a…a93f`; sample docx `2ce98130…7e09` (= B314 STATUS:29).
- `Content/` does not exist; the planned folder and note paths are not gitignored (control `Source_Documents/x` -> `.gitignore:11`).
- `AGENTMAIL_API_KEY` count 0 (control 1). Root status 996 lines; ` M`: B26 and B298 STATUS (not ours).
- tmux 14:06: `%123` SEAT-W12 (B322) live; no B323, B320 or other Composer pane.
- The plan's K5 "C-23" and conflicts' "C-20/C-22" are **HPSM** entries (`Reference_from_HPSM/HPSM_CLARIFICATIONS.md:199,217,226`); Composer C-22/C-23 are unrelated (feedback pill, feedback round). Brief warns the seat.
- Q-03/Q-04 = `ARCHITECTURE.md:151-152`, both ACCEPTED AS WORKING ASSUMPTIONS (HPSM C-25). Q-04's answer says "Ship no HP-internal identifiers".

## Fold decision
**This seat folds `records/b321` first (Step 0b, B298 method, exactly as B321 folded `records/b301`), then branches `records/b328` from the new `main`.** Why: B321 is finished (`RECORDS COMMITTED`), the collision set is measured and clean (48 equal + 1 append-only), a fold keeps every records branch one commit on `main` (Tuesday's later fold of b328 stays a one-step merge), and the 30 State-cell edits then diff against a `main` that already holds the rows. Stacking on b321 would leave two unfolded branches and a two-commit fold. The B321 STATUS root block and its one root-only evidence file are restored in b328's commit (B298 precedent).

## Open questions (each with a recommended answer)
1. **C-entry shape.** Rec: one umbrella (C-86) + one per card (C-87..C-96), not grouped by lane: cards map many-to-many onto lanes, and later briefs cite "C-90 (K4)" unambiguously.
2. **B323 and B320 will STOP on a live B328.** B323 brief:24 names "a live Composer seat other than B321/B322" a STOP; B320 brief:80 needs "no other Composer seat live". Rec: launch B328 AFTER B323 and B320 have passed Step 0 (or now, and give both an ADDENDUM naming B328 as allowed: records only, root repo, disjoint).
3. **B320's r7 expects `main` = `bbd5ddb3…`** (pre-fold); B321 already moved it, B328 moves it again. Rec: ADDENDUM to B320: r7 reads `records/b301` is ancestor of `main`, not an exact sha.
4. **K4 "after a Q-03/Q-04 check" — who checks?** Rec: B328 records the check on paper (verbatim texts, item by item) and concludes nothing; Tuesday confirms in the L1 brief. If Tuesday reads Q-04's "no HP-internal identifiers" as covering install-read item ids, card it before L1.
5. **Template wording (K9 a vs the plan's why/customisation columns).** Rec: carry the sample's sentences de-identified as `*_source_wording`, labelled "not Datasec's words", rewording on L2-3's words card. Alternative: leave the columns empty.
6. **Folder name.** The plan says `Content/2026-10-20_sro-template/` (client's initials). Rec: `Content/2026-10-20_hpsm-baseline-template-DRAFT/` (in the brief).
7. **Gaps the rulings open with no plan ticket:** K1's "today" column, K7 (b)'s header/footer field. Rec: FOR TUESDAY lines, no new rows; Tuesday's planner tickets them at the L2/L6 briefs.
8. **L4-2's "Kam to confirm in K3" (warn, never block)** is not in K3's card text. Rec: treat as still open; card it with the L4 brief.
9. **HPSM C-22 (Preview severities) vs the template's severities** (gap §5 item 2): not stated by the tap. Rec: FOUND only; card at the L2 brief.
10. **Paul note wording.** Drafted in the brief (names the client only as "SRO", no internal ids, asserted by regex). Rec: Kam reads it before sending; the "working assumption" sentence in Q4 reflects K1 (a) and can be cut if Kam prefers not to signal it.
