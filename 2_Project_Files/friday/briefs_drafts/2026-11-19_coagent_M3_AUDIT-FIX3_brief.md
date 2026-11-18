This brief is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. You are a NEW seat, M3-AUDIT-FIX3, with no memory: the seats that built audit-fix and audit-fix2 are gone and their work is merged. You work on a NEW branch `m3-audit-fix3` in a NEW worktree `coagent/worktrees/m3-audit-fix3`, cut from `origin/main` at `bfe435abbe86302363b4472b967f016484417e61`. Your report is a NEW file `coagent/5_Project_History/STATUS_M3_AUDIT_FIX3.md`; while working its last line is `IN PROGRESS: <item>`, updated at least every 20 minutes; when section 2 is done its last line is exactly `READY FOR QA M3-AUDIT-FIX3`.

# M3 AUDIT-FIX3: no accepted limit gives any part of the own space more room than the defaults (closes the resume-defaults state and QA2-m1)

Paths. Project: `/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/` (repository `2_Project_Files/`). Briefs: `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/`. Design and verdicts (READ-ONLY): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/` ([07] = `07_audit-storage-accounting-redesign.md`; the check = `m1_review/gate_M3_AUDIT_FIX2_verdict.md`, its tests in `m1_review/gate_audit_fix2_tests/`). Every line number and function below was read at `bfe435a` with `git show` by the drafter (the seat that prepared this file for Friday). Nothing was run: a figure the drafter worked out is "(computed, not run)". Friday's two rulings are written in below (R1, R2). If a line still says `RULING NEEDED`, STOP and ask.

## 0. Start (changes no rule)
1. Read WHOLE, in order: `coagent/CLAUDE.md`; this file; the check (section 5 above all, QA2-m1, QA2-n1 to n4, "NOT TESTED") and `clamp_proto.py`, `clamp_proto_summary.txt`, `clamp_prop1024_strict.txt`, `fix_qam1_seat_seed_variant.diff`; the audit-fix2 brief and its addenda 1 and 2 (the standing rules); [07] §1.4 and §1.6; then the code: `src/session.rs` (`StoreLimits` :63-118, the session's initial limits :255, `resume` :329, `resume_with_anchor` :536, `try_set_limits` :557-634, `set_limits` :636-642), `src/budget.rs` (`own_seat` :156-158, `free_part` :161-163, `requested_allowance` :166-169), `build.rs` (controls list, `limits_strand_seat` :136), `tests/fix_qam1_seat.rs`, `tests/qa_fix2.rs`, `tests/fix_r5m1_limits.rs`, `docs/AUDIT.md`, `BACKLOG.md` (:337, :362, :378, :383), `scripts/red-controls-audit.sh` (row format :21, row `limits_strand_seat` :218).
2. Worktree, from the remote only: `git fetch origin`; `git ls-remote origin main` and `git rev-parse origin/main` must both print `bfe435abbe86302363b4472b967f016484417e61`; then `git worktree add --no-track -b m3-audit-fix3 ../worktrees/m3-audit-fix3 origin/main`. If main differs (it may have moved), record the SHA it shows and STOP for Friday; also STOP if the branch or folder exists. `CARGO_TARGET_DIR=tools/target/m3-audit-fix3`; run the audit runner with `COAGENT_AUDIT_RED_TARGET` and `COAGENT_AUDIT_RED_LOGS` in your own directories. Every other `m3-audit*` worktree belongs to a dead seat: leave it.
3. sha256 of the six gate files must equal (prefixes, read from main): `gate.rs` d6a29f1e2966b1a6, `gate_attacks.rs` 6ef41612b4e4241c, `gate_r2.rs` adca67f33b042632, `gate_r3.rs` c1726e9d84744d7b, `gate_r4.rs` addc9f79bb321b3a, `gate_r5.rs` d16e82d53356b062; also `qa_fix.rs` b4100b5aa2251839 and `qa_fix2.rs` 4df31445ff57eab5.
   Record the full values. Any difference: quote it and STOP.
4. `scripts/check.sh` and the audit runner at the start, tails recorded.
   Friday's clean clone at `bfe435a`: check.sh exit 0, "CHECK OK", 930 passed / 0 failed / 18 ignored; runner exit 0, "RED CONTROLS OK", green run 265 tests, no row not red. Different totals or a failure: STOP.
5. Show the state present: run the pin `qam1_finding_resume_defaults_leave_an_owed_checkpoints_payer_without_room`, the recogniser test and `qa2_finding_n1_and_resume_defaults_together_neither_named_remedy_works` with `--nocapture`; all three PASS today; record each printed line.

## 1. The authority
The check of audit-fix2 (GO WITH NOTES) found that after `resume` the log is on the DEFAULT limits, and limits with fewer records give each allowance MORE bytes than the defaults, so a requester's owed checkpoint can be refused after a restart (the resume-defaults state, carved out of the property by addendum 1), and with N1's state the caller's documented remedy fails (QA2-m1).

Its section 5 proposed a crate-side rule and tested it in a copy.

Kam's decision card, 2026-11-18, option verbatim: "Close it before the beta". Friday rules: one small round, then ONE short independent check, which rules on every edit permitted here. You do not merge. A NO GO goes to Kam, not back to you: build as if nobody gets a second look.

## 2. What to do, in order
1. **The rule (the drafter's reading of the code; confirm or correct it in STATUS).**
   Every part of the member's own space is a monotone function of the offered seat (pb, pr) = `per_peer()` = (bytes/8, records/8): the seat (pb, pr); the own seat `own_reserved()` = (pb ∸ pr, pr) (`budget::own_seat`, one byte less per record); the free part = own/2; each requested allowance = (own − own/2)/7; the peer pool = 7·seat. RECORDS of every part grow only with pr, and pr ≤ dr is already enforced by the per-component cap (:599-603). BYTES of the seat grow only with pb ≤ db (same cap), but the own seat's bytes (pb ∸ pr), and so the free part's and every allowance's bytes, GROW when pr falls.
   Hence ONE comparison decides "no part has more room than the defaults", per part, in bytes and records: `pb ∸ pr <= db − dr`, with (db, dr) = `StoreLimits::default().per_peer()` = (5,097,490, 28,604), so db − dr = 5,068,886, the defaults' own-seat bytes (`docs/AUDIT.md:182`). Write this argument in STATUS and in the doc comment.
   - **Why it ends the state:** after the change, every limit ever in force (the session's initial defaults :255, every accepted offer, the defaults `resume` installs) is at most the defaults in every part, so `resume` can only RAISE a part relative to the last accepted limits: an owing allowance whose usage plus one checkpoint fitted the accepted allowance fits the defaults' (clause (A) never refuses the defaults; the payer always has room), and a seat that fitted fits the defaults' seat. QA2-m1 needs an accepted allowance above the defaults' (the check's L, 40,619,920 / 16,000: own bytes 5,075,490 > 5,068,886, computed, not run), so it cannot be built either.
   - **RULING (Friday, 2026-11-19): R1 = CLAMP**, as the check's prototype does and as the existing per-component cap already lowers a component above the defaults: it is the tested form, it keeps "when nothing is owed it refuses nothing" and "limits on a new session are always accepted", and it honours a records-only lowering. The doc comment says plainly that an offer can be LOWERED and that the caller reads `limits()` back to see what is in force. REFUSE is not built.
   - **Build (CLAMP):** in the cap step of `try_set_limits` (:596-604), after the per-component `min`, the defaults clause as the prototype words it (private arithmetic, `SEATS` is already imported :40); clauses (A) and seat then test the limits that will be installed, unchanged byte for byte.
   - Red control `limits_above_defaults` in `build.rs`, removing ONLY the new clause; `limits_may_raise` keeps removing the whole cap.
   - No public item, no new variant; `set_limits` stays `let _ = self.try_set_limits(limits);`.
   - Rewrite the doc comment (:557-593; src is not frozen this round): the cap stated whole, the defaults clause and its one-comparison argument, "That is the whole rule" true again, the parenthesis at :589-593 removed.
2. **Tests (in `fix_qam1_seat.rs`, builder-owned).**
   - Model `capped()` (:63-70) mirrors the new cap (the prototype's edit).
   - Deterministic: a grid of offers (default bytes with records from dr down to 8 per seat; bytes and records each at, one above and one below the boundary) where, after `try_set_limits`, every part of `limits()` (seat, `own_reserved`, `free_part`, `requested_allowance`, `peer_pool`) is at most the defaults' part in bytes and records, and the boundary offer itself is installed unchanged; the pin's offer (default bytes, 3/4 records) reads back `bytes 40,722,712` (computed, not run).
   - **The property, new P4** (text `QA2-m1 property P4`): after every `try_set_limits` answered `Ok`, every part of `limits()` is at most the defaults' part. Reach key `limit offer lowered by the defaults clause`, asserted above zero at EVERY size (the `Aim` records ops reach it, computed, not run).
   - **The carve-out REMOVED.** Drafter's reading: `resume_defaults_state` (:929-988) is used only by the P3 carve-out (:1083-1104), the P2 carve-out (:1328-1354) and its own test (:742-850); `restarted` (:1240-1242, `change()` :1136, :1152), `Refusal` (:920-927) and `RD_CASES` (:917, :1801, :1830-1847) exist only for it. Nothing else needs it, so it goes. P2's N1 arm and P3's N1 exception stay exactly.
   - **RULING (Friday, 2026-11-19): R2 = QUARANTINE.** The recogniser, its test, `Refusal`, `RD_CASES` and the tracker are moved verbatim (never deleted) to `crates/coagent-audit/tests/quarantine/fix3_resume_defaults_recogniser.rs.txt` (not compiled), with a header naming this round and what it guarded; the property's doc comment (:1781-1796) loses the addendum-1 and QA2-n1 sentences and states that P2 and P3 now hold with no carve-out. The independent check rules on the removal.
   - **Seeds.** Add the check's `FIX_QAM1_SEED` knob (`fix_qam1_seat_seed_variant.diff`, to `runner()` :1764-1779), unset = today's seed.
     The property in release at 1,024 cases at the committed seed AND at `FIX_QAM1_SEED=7` and `=200`: PASS, NO carve-out; give every reach count of each, P2's N1 count, and the P4 key above zero.
3. **The three tests that show the state become ruled edits**, each with the line above `// RULING (Friday, 2026-11-19, audit-fix3)` and every replaced line quoted as `// old:`; record failure text and printed line BEFORE the edit.
   They state the fixed property for the test's OWN input, using only values the test already computes or reads back:
   - the pin (:671-740): the offer `fewer` is lowered by the defaults clause (`v.limits() != fewer`, `v.limits().requested_allowance().0 <= d.requested_allowance().0`); after `resume`, 3 of 3 checkpoints `Ok`; `try_set_limits(d)` `Ok`; the checkpoint covers the newest own event. Rename only if Friday rules so (it is not ruled here).
   - the recogniser test: per R2.
   - `qa_fix2.rs` `qa2_finding_n1_and_resume_defaults_together_neither_named_remedy_works` (:491-605): `try_set_limits(l)` at :497 still `Ok` but `limits() != l`; :498 and :596 (the allowance above the defaults') become their negation for the limits in force; after `resume`, `cp_d` `Ok` and `set_d` `Ok` (the check's prototype saw "checkpoint Ok(()), defaults Ok(())").
     Every other line of `qa_fix2.rs` stays.
   - If an input no longer builds what a later line needs, do not weaken: record it and STOP on that test.
4. **Consequences, read by the drafter (each becomes a named check in STATUS).**
   - **Gate-file limits**, from every `set_limits` in the six gate files: `small(…)` per seat ≤ 48,000 bytes in `gate_r4` (:82, :354, :422, :570, :653, :806 generator 1,500..40,000, :1591, :1728, :1744, :1781) and `gate_r5` (:54, :205 generator 6,000..48,000, :373 `Op::Lower` lim·(4..7)/8 with floors 8·600 / 8·4, :605, :620, :664, :689, :736);
     `gate_r3` `SMALL` (1 MiB, 100,000, :48); `gate_r2.rs:460` (b0 + 2,000,000 bytes, 1,000,000 records: records capped to the defaults, so pr = dr); `gate.rs` and `gate_attacks.rs` set none.
     Every one has own-seat bytes far below 5,068,886: NONE is touched by the clause (computed, not run).
     If any gate test changes colour, do not edit it: quote it and STOP.
   - **Tests that put bytes near the defaults with fewer records on purpose,** all builder- or check-owned: `fix_qam1_seat` pin :676, recogniser :759, `Op::Aim` even :1464, "different after resume" :1715 (bytes ×3/2, records ×3/4); `qa_fix2` :216 (records-only steps) and :496; `fix_r5m1_limits` `Op::Raise` :713 (rarely reaches the bytes cap).
     Each: green, or named and handled under items 2-3.
   - `fix_r5m1`'s `scaled` floors and `qa_fix.rs:557` scale both components together: unaffected.
5. **Red control.** ONE runner row: `limits_above_defaults|fix_qam1_seat|qam1_prop_no_owed_checkpoint_is_refused_for_room_after_an_accepted_limit_change|QA2-m1|QA2-m1 property P4`.
   - Red on P4's text at the default 64 cases (the drafter's reason for P4: per the check, section 5(1), the 64-case seed never reaches the resume-defaults state, so P2 and P3 alone would stay green under this control).
   - `limits_strand_payer` and `limits_strand_seat` stay red on their own texts.
6. **Docs and BACKLOG made true** (old and new quoted in STATUS).
   - `docs/AUDIT.md`: "Changing the limits" (:201-256: the cap gains the defaults clause; the after-`resume` paragraph loses the two-step remedy, QA2-m1's third limit and QA2-n3's search, keeping: re-offer your own limits and read `limits()` back);
     the `own_reserved` sentence (:189-192: fewer records would give more bytes; the cap now lowers the bytes so they never do);
     "Restart" (:385-402); the charging-table row (:289); "Limits, stated" (the restart entry :560-585 and the QA2-m1 passage): closed, in the form the file uses for closed entries.
   - `BACKLOG.md`: :383 audit-fix3 and :378 closed in the file's own form (`- [x] <original sentence unchanged> — CLOSED in commit … (M3 AUDIT-FIX3, the owner's answer "Close it before the beta"): …`, the clause, tests and red row), never deleted;
     What remains for the daemon is :337 / :362 (after every `resume` re-offer its own limits with `try_set_limits` and read `limits()` back; N1's exception), corrected to say no limits need be kept for correctness.
7. **Final tree.**
   - `scripts/check.sh` exit 0; the audit runner to its final line, its exit code captured (`; echo "exit=$?"` in the same command, not backgrounded); every row red on its own text, the clean run green;
   - the six gate files byte-identical to main; `git diff --stat bfe435abbe86302363b4472b967f016484417e61 HEAD` within `crates/coagent-audit/` (`src/session.rs`, `build.rs`, `tests/`), `docs/AUDIT.md`, `BACKLOG.md`, `scripts/red-controls-audit.sh`;
   - a case-insensitive scan of added lines for any person, account, machine, drive or client name and any home or volume path: zero, with a positive control.
   - `git push -u origin m3-audit-fix3`; record `git ls-remote origin m3-audit-fix3` and `git merge-base --is-ancestor origin/main HEAD` (exit 0); read `git ls-remote origin main` again just before the last line and report if it moved (do not merge it).
   - While a STOP is open the last line is that question, not READY.

## 3. Decisions you are NOT making
- Not merging; not touching `main`; never a force-push or a rebase of a pushed branch. No other crate; no public item changed or added; no new error variant.
- Not changing a bound, table or constant of [07], rulings I-A11 to I-A15, or the earlier rulings: clause (A) and the seat clause as built, "owed" as defined, no free-part clause, N1 and N2 stay pinned, P2's N1 arm and P3's N1 exception stay exactly.
- No gate-file edit at all; no edit of `qa_fix.rs`; of `qa_fix2.rs` only the ruled edit of item 3. A test that changes colour otherwise is quoted and asked about, never edited, weakened, ignored or deleted. No feature beyond this rule; no second rule.
- Fixtures from data generated in the test, never a real drive; no person's, machine's or drive's name and no real path in code, tests, docs, commits or STATUS output.
- Never delete: quarantine. `coagent/CLAUDE.md` rules bind you: no model runs, no network beyond `git fetch`, your branch's push and locked crates. Report disk used. Another seat builds on this machine: at most TWO heavy runs at once (the three 1,024-case runs count as heavy).
- Standing lessons: a red control is red on its NAMED property, not a side effect; no assertion on truncated text; no test depends on map order; "equivalent mutant" is a written claim; prefer the Edit tool to heredocs.
- Kam is not asked: questions go in STATUS; approval-class items are a STOP under BLOCKERS. Not wrapping on a dry queue: when section 2 is green, write READY and wait.
- After ANY context compaction, re-read this brief and your STATUS file WHOLE before writing anything more.

## 4. STATUS sections
- (1) Start: SHA, worktree command, hashes, start tails, the three state tests' lines.
- (2) The rule: the per-part argument confirmed or corrected, the code as built, `pub` lines of `src/` sorted, start against end.
- (3) Tests: each deterministic test's printed line; each ruled edit (test, line, old, new, text before); the three 1,024-case runs with reach counts.
- (4) Red row and failure text.
- (5) Docs and BACKLOG, old and new.
- (6) Final totals, diff stat, scan, push, ls-remote, ancestor.
- (7) DESIGN QUESTIONS, STOPs, NOT DONE, disk, processes left (none).

The last line, when all of it is done, exactly: `READY FOR QA M3-AUDIT-FIX3`

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
