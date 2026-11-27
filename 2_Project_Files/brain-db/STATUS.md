WORKING

**INTERIM, written 2026-11-27 18:06 AEDT: everything below is final EXCEPT the mutant figures. The pane is waiting on its own mutant re-run (about 45 minutes) and will finish this file by itself. This is not a stop and the first line stays WORKING until then.**

# ROUND 4 (answer to `ANSWER-6.md`: qualify or stay out; the right database inside the same session)

Fresh build seat, 2026-11-27, 16:42 to (still running) AEDT (both from `date`). All HOLDS kept: this lane and my scratchpad only (sockets under short `/tmp` paths of my own), no shared file edited, neither checker's folder written, no git write, no mail, post or network call, nothing installed, no `rm`, no `cd`. No file in any real `4_Credentials` or `3_Access_Keys` was opened. The drive cluster ran once, for one rebuild and the ten questions, and is STOPPED.

**In one paragraph.** The deciders are rebuilt as qualify-or-stay-out and the fence and section-span code is deleted. The suite is 682 passed, 0 failed, under Python 3.14.10 and 3.9.6. The checker's `f1_new.py`, run unmodified, has 0 of its 58 must-be-absent shapes entering (28 entered in round 3) and 0 of its 20 index variants leaking. The F2c swap is refused with exit code 4 and the cluster that was never addressed is untouched. Mutants: the first run caught 59 of 61 (57 on the line I named, 2 on another line) and 2 survived; both causes are fixed and **the full set is being re-run on the final code as this is written.** **One thing differs from what the brief expected and it is large: read as written, clause (d) leaves out 57 real lessons, not 5.** 55 of them simply name Datasec somewhere in their text. I built the stricter reading, as `BRIEF.md` directs when a brief disagrees with itself; the question is at the end. It costs answers: the right lesson for questions 2 and 9 of the ten is now left out.

## The qualify rule as built, clause by clause

`qualify_lesson()` in `braindb_index.py`. The first clause not met is the one the lesson is named under. Every planted lesson in the fixtures qualifies on every clause except the one it is planted for, so its absence proves that clause alone; `tests/run.sh` section 6b compares the rebuild report's "file, clause" list with the fixture builder's own table (128 lessons, exact match required).

| Clause | What qualifies (everything else is left out and named) | Planted cases | Neighbours that must be in | Mutants (each lets an unqualified lesson in) |
|---|---|---|---|---|
| (a) one row | Exactly one rules-index row whose key EQUALS the file name (both sides NFC, format characters removed; no case folding, no stripping, no path). `#n` rows allowed when each is read and none repeats. No line of the index that could not be read holds the file's name anywhere. A row is read only in the spec's shape: 7 TAB fields, none empty or padded, no control character, key `<file>.md` or `<file>.md#n` with n at least 2, status `live`, `dead` or `superseded`, seats as in (b). A comment line below line 1 counts as a line that could not be read. | 31: no row; key without `.md`, quoted, other case, a path, padded, a typo, a wikilink; TABs turned to spaces; 8 fields; 6 fields; CR; `#1`; good row plus damaged row; the same key twice; `#2` twice; commented-out row; a comment or a line of prose naming it; `#2` with no plain row; nine bad seats or status cells; a zero-width space making a second row for it | 4 (plain plus `#2`; file name NFD with key NFC; a row carrying injection strings; the base lessons) | `Qa_no_row_qualifies`, `Qa_unread_lines_ignored`, `Qa_duplicate_rows_ok`, `Qa_duplicate_hash_rows_ok`, `Qa_seats_cell_loose`, `Qa_key_any_shape`, `no_index_not_refused` |
| (b) this seat | That one row's seats cell is `all` or holds this seat. The spec, quoted: "`seats` — `all`, or a comma list of `wednesday`, `tuesday`, `friday`". A `#n` row naming this seat does not rescue a lesson whose plain row names another seat; a `#n` row naming another seat keeps that rule line out of an indexed lesson. | 5 | 3, and one rule line that must be absent inside an indexed lesson | `Qb_seat_not_tested`, `Qb_any_row_counts`, `Qb_other_seat_rule_line_in` |
| (c) frontmatter and tier | Line 1 exactly `---` (after an optional BOM); a later line exactly `---`; every line between a plain `key: value` with a lower-case ASCII key; no key twice; exactly one key `tier` and no other key holding "tier" once folded hard (NFKC, format characters and non-alphanumerics dropped, case folded); no other value carrying a tier assignment; no second block after the first. Tier VALUE on a closed list: `W`, `M`, `P-<own client>/<project>`. | 45: no tier; `MIXED`; another client's project in both spellings; unknown client; the bracket spelling; `w`; `W ` with a space; `W # ...`; quoted; a list; `Tier:`; `TIER:`; quoted key; `tier :`; `tier (project):`; `tier = `; `tiers:`; `tier_project:`; tier twice both ways; another key twice; list item; nested; folded; block scalar; tab indent; YAML comment; blank line; a tier inside another value (two forms); unclosed; leading blank; indented fence; fence with a space or a comment; four dashes; `+++`; a line before the block; no block; two blocks (near and 80 lines down); empty file; a file that is only `---` | 9 (M; `P-General/Claude to Claude`; BOM; the other keys real lessons use; a status line naming a "three-tier-routing" lesson; a `---` rule in the body; "tiers", "three-tier routing" and "frontier" in the body; unclosed code fences; an impossible date) | `Qc_any_tier`, `Qc_no_tier_is_W`, `Qc_line1_loose`, `Qc_odd_lines_skipped`, `Qc_dup_key_ok`, `Qc_keylike_ok`, `Qc_value_tierlike_ok`, `Qc_second_block_ok`, `Qc_closed_list_loose` |
| (d) no marker, no other client's name | No `<!--` or `-->` anywhere. No line that starts with the word tier, or assigns one, outside the one frontmatter line. No `deny_clients` name in the text, the file name or the lesson's own rules-index line (compatibility forms unfolded, accents and the marks `* _ \` ~ \\` removed, case folded). No numeric character reference. A lesson with a mixed section is out WHOLE. **No fence or section-span code is left: `drop_foreign_sections`, `MARKER`, `P_MARK`, `tier_verdict` and the fence toggling in the decider are deleted.** (`heading_lines` still skips fences when it splits an already-qualified file into search rows; it decides nothing.) | 26: six marker forms (other client, OWN client, nested fences, three-line comment, list item, no word "tier"); any comment; a stray `-->`; six tier-like body lines; the name plain, in capitals, in a domain, split by emphasis, accented, full-width, in a heading; a numeric reference; the name in the FILE NAME, in the rule line, in a frontmatter value, in an own-client project name | 1 (the seat's own client named, and "data security") | `Qd_comment_ok`, `Qd_tierlike_line_ok`, `Qd_name_ok`, `Qd_name_not_squeezed`, `Qd_name_not_folded`, `Qd_only_body_tested`, `Qd_entity_ok` |
| (t) plain text (mine; it is what makes (c) and (d) mean what they say) | Valid UTF-8; no control, format or line-separator character other than LF and TAB; every letter an ASCII letter once accents are removed. | 17: Latin-1; UTF-16; NUL; 0x1E; CRLF; CR only; form feed; U+2028; U+0085; zero-width space; soft hyphen; Cyrillic (twice); Greek; a Latin small capital; a right-to-left override; invalid bytes | 1 (accents, em dash, arrow, multiplication sign, tab) | `Qt_any_bytes`, `Qt_controls_ok`, `Qt_letters_ok` |
| (f) file level | Opened with `O_NOFOLLOW` inside its already-open folder; `fstat` on that descriptor says regular file, link count 1; the bytes come from the same descriptor (N6). Applies to every kind, not only lessons. | 4: symlink to a credentials file, hard link to one, a directory, a FIFO; plus section 12f, the file flipped between regular and symlink during 14 rebuilds | - | `Qf_hard_link_through`, `Qf_symlink_followed` |

**The tier values really in use** (`0_Brain/learnings/20*.md`, 293 files, measured before the list was written; every one opens on line 1 with exactly `---` and every frontmatter line is a plain `key: value`):

| Value | Files | Under the Wednesday scope |
|---|---|---|
| `W` | 236 | allowed |
| `M` | 43 | allowed |
| `P-General/Claude to Claude` | 1 | allowed (own client) |
| no tier line | 6 | OUT (3 of the 6 were indexed in round 3 as "untagged"; the other 3 are scoped to other seats anyway) |
| `MIXED` | 5 | OUT |
| `P-Datasec/HPSM-POC` | 1 | OUT |
| `P (Datasec/OXPd)` | 1 | OUT |

No real lesson holds a control or format character, a non-Latin letter, a CR or a numeric reference, so clause (t) costs nothing today. The real rules index: 379 rows, all read; 0 lines that could not be read; 1 comment line (line 1); 0 keys naming no file.

## The other kinds: a closed table in the code (N5), validated before anything exists (N7)

- `SEAT_DAILY`, `SEAT_LEDGERS`, `SEAT_PICKUP`, `ROOT_RULES`, `SHARED_DIRS`: one folder per kind and, for ledgers, pickup files, the rules index and the rules files, exact names, per seat. A scope line outside the table is REFUSED at load with exit code 2. The daily folder is also taken from `tools/seat_note.sh` (`SEAT_NOTE_REL`) and the two must agree.
- Wednesday's ledger table is `_ledger.md` and `_ledger_archive.md`; Tuesday's `_ledger_laptop_datasec.md` and its archive; Friday's `_ledger_friday.md` and its archive.
- **My reading, to confirm:** the pickup table. Wednesday `NEXT-PICKUP.md` and `WEEK-INSTRUCTION.md`; Tuesday `NEXT-PICKUP-TUESDAY.md` and `WEEK-INSTRUCTION-TUESDAY.md`; Friday `NEXT-PICKUP-FRIDAY.md` and `WEEK-INSTRUCTION-FRIDAY.md`. I took these from the file names in `0_Brain/tasks/`; I found no tool that states the mapping. `NEXT-PICKUP-DATASEC-LAPTOP.md`, `TASKS.md`, `EXPIRING-GRANTS.md` and the rest are in no seat's table. It is a new kind, `pickup`; no shipped or proposed scope has a line for it, so nothing from `tasks/` is indexed today.
- Tests, section 7: 17 widening lines on the Wednesday tree each refused, index unchanged; 12 lines on trees named TUESDAY and FRIDAY asking for Wednesday's ledger, archive, daily notes and pickup file each refused with no cluster created; the seat's OWN pickup line accepted and its token present. Section 12e: four scope files that exist but are refused, four commands each: exit code 2, no cluster directory, no lock file, no server, 16 of 16. Mutants: `N5_names_not_closed`, `N5_folders_not_closed`, `N5_rules_not_closed`, `N7_scope_validated_late`, `F4_scope_checked_late`.

## The right database, inside the same session (N3, N10, N11, N13)

- Every `psql` session the tool opens starts with two statements: a `set_config` holding the addressed data directory, and a `DO` block that raises unless `current_setting('data_directory')` equals it. In a rebuild they are the first statements inside the one transaction that drops and reloads; in `check`, `search` and `at` the first statements of the reading transaction. There is no separate connection between the test and the write.
- **Where I did not do what the brief says, and why.** The brief asks for both sides "through realpath". SQL cannot resolve a path. So `braindb.sh` resolves the data directory once, at the top, and that one spelling is used for `-D`, the pid-file test, the lock file and the assertion. A trailing or doubled slash, or a symlink to the directory, is therefore the same cluster (N10, tested). The server's side is compared as the server spells it, which is that same real path whenever this tool started it. A server someone started by hand through a symlink is REFUSED rather than accepted: the safe side, not the letter.
- **F2c lifted, section 12c**, in two forms. A: the checker's own (the server is swapped while the rebuild waits for the lock). B: narrower, swapped after every separate session of the tool and before the load session opens; for this the indexer has a test-only pause, `BRAINDB_TEST_HOLD`. Both: exit code 4, "serves data directory X, but this command is addressed to Y", no `rebuild: done`, and the cluster that was never addressed still holds its own one file and nothing of the other tree. Then `check`, `search` and `at` addressed to the stopped cluster: exit code 4 each, no GREEN and no result printed. Control: a rebuild that waits for the lock and is not swapped ends rc 0. Mutants: `N3_no_assert_in_load` (only form B catches it), `N3_no_assert_in_reads`, `N3_assert_always_true`.
- N11: nothing answering is exit code 3, "not answering", and never "another cluster"; `status` exits 4 when it prints REFUSED. N13: the indexer's lock wait gives up after 150 s (`BRAINDB_LOCK_WAIT`) with the same sentence as `braindb_lock.py`, exit code 75.

## What fails closed is visible (N8)

- `rebuild` names every left-out lesson under its clause; its LAST line reads, on the real tree, `rebuild: done; no file was unreadable and no row was truncated; 93 lesson file(s) LEFT OUT by the qualify rule: b=28, c=8, d=57`.
- `check` prints the same count and up to five names per clause; `doctor`'s one line carries the count; `status` shows it.
- `search`, when it finds nothing, adds `NOTE: N lesson file(s) are LEFT OUT of this index ... and are not searched`.
- **Not done, on purpose:** `search` does not say "your word exists only in a left-out file". That would mean reading, at search time, files that did not qualify, and telling this seat what is in them.

## The checker's attacks, re-run on the final code

| Attack | Round 3 | Round 4 |
|---|---|---|
| `f1_new.py`, unmodified from where it lies, 58 must-be-absent shapes | 28 entered | **0 entered** (`evidence/checker_f1_new_round4_unmodified.txt`) |
| its 20 whole-index variants | 2 leaked | **0 leak**: 15 refused with rc 2, 5 built with neither token present; its control token present in all 5 |
| its 9 "want present" cases | - | 2 present, 7 absent. All 7 are the new rule working as ruled: an untagged lesson, a lesson with no row (twice), two rows with one key, a commented-out row, a marked section whose lesson is now out whole, a look-alike letter |
| The same script with ONE change: a case that had no row gets one good row scoped `all` (`tests/f1_new_adapted.py`) | - | **0 entered**; the 64 left out fall under a=10, b=4, c=35, t=15, so each shape is stopped by its own clause and not by "no row" (`evidence/checker_f1_new_round4_every_case_has_a_good_row.txt`). Every left-out case is named in the report. |
| `seat_f2.sh` F2c | rc 0, wrote into the other cluster | refused, rc 4 (lifted into section 12c; its script holds its own scratch paths, so I did not run the file itself) |
| `seat_f2_part2.sh` S6 (T1 to T7) and its F4 block | Wednesday's ledger, archive, daily notes and pickup file entered; cluster left running | each line refused at load, nothing created (lifted: sections 7 and 12e) |
| `f3_f5_f7.sh` F3c, the symlink flip | the secret entered in 10 of 40 rebuilds | 0 of 14, while the file flipped about 18,000 times; seen as a regular file 6 times and as a symlink 6 times in my first full run (lifted: section 12f) |

In the adapted run one of the checker's "record only" cases is IN, as it was in round 3: `tier: P-General/DS-NexusAI`, an own-client tier whose project is the other client's by abbreviation. The rule reads names, not abbreviations.

## The real tree: cost of the stricter rule

One rebuild, 2026-11-27 17:58 AEDT (`evidence/real_rebuild_round4.txt`).

| Measure | Round 3 | Round 4 |
|---|---|---|
| Files indexed | 419 | 354 |
| Lesson files matching the allow line | 292 (plus one conflict copy) | the same |
| Lessons indexed | 264 | **199** |
| Lessons left out | 28 (26 by seats, 2 by tier) | **93**: b=28, c=8, d=57 |
| Rule lines | 345 | 242 |
| Search rows | 22,267 | 22,096 |
| Other files not indexed | 4 conflict copies | 4 conflict copies |
| `at` against `rules_card.py --at`, 22 triggers | 802 and 802 | 559 against 802; none only in the index (`evidence/at_crosscheck_round4.txt`) |
| Rebuild time | 4.7 to 4.9 s | **19.2 s, one run** (parse 2.9 s, load 16.4 s) |
| `check` | 0.48 s | 3.9 s |
| Search latency, ten questions | 121 to 230 ms | 124 to 373 ms |
| Size on the drive | 174 MB, database 118 MB | 174 MB, database 117 MB |

The three slower figures were taken with the Mac's load average at 24 (`uptime` at 17:59; other seats were running, and my own mutant run had just ended). I was allowed one rebuild and did not repeat it, so I cannot separate the load from the new code. I have not shown that the new code is as fast as round 3's.

**Every real lesson now left out, by clause** (`evidence/left_out_lessons_round4.txt` has each with its reason).

(b) 28, the row is scoped to other seats. These are the same lessons round 3 left out by seats (26), plus the two Datasec project lessons that round 3 left out by tier.
- `tuesday,friday` (9): 2026-08-12_hpsm-continuous-readiness-grant; 2026-09-17_guard-against-reinventing-prior-work-check; 2026-09-22_ornith-is-studio-only-not-datasec; 2026-09-27_hpsmpoc-every-hp-ask-is-its-own-email-plus-a-register; 2026-09-29_datasec-github-commits-go-through-codeql; 2026-09-30_qa-gates-may-switch-to-opus48-when-flagged; 2026-10-16_tuesday-boot-sweeps-project-feedback-into-tickets; 2026-10-16_tuesday-inherits-push-to-demo-hpsmpoc-unfrozen-account-controls-datasec; 2026-10-23_hpsmpoc-build-only-this-phase-next-phase-funds-it
- `friday` (10): 2026-09-23_spark-kit-running-a-local-coding-model; 2026-09-23_use-the-local-model-as-much-as-possible; 2026-10-01_friday-cloud-threshold-90; 2026-10-03_hp-security-manager-azure-deploy-grant; 2026-10-06_push-to-demo-when-ready-no-card; 2026-11-16_architecture-agents-run-on-the-newest-fable; 2026-11-16_grant-build-coagent-overnight-until-the-morning-review; 2026-11-21_a-holding-helper-gets-the-next-useful-job; 2026-11-21_friday-runs-on-opus-fable-only-when-flagged; 2026-11-21_windows-helper-launches-without-permission-prompts
- `tuesday` (9): 2026-10-12_boot-sweeps-all-feedback-repositories; 2026-10-20_tuesday-no-90pct-line-two-accounts; 2026-10-22_tuesday-sonnet-default-usage-is-a-guide; 2026-10-24_every-boot-works-the-actionable-tickets-unprompted; 2026-11-18_the-kit-stamp-checklist; 2026-11-19_no-hpsm-work-for-three-weeks-or-until-kam-asks; 2026-11-19_oxpd-runs-on-the-newest-fable-tuesday-boots-on-fable; 2026-11-21_no-fable-unless-flagged-opus-is-the-default; 2026-11-24_oxpd-jira-holds-the-latest-design-docs-and-kams-actions

(c) 8. **These are the 5 the checker counted, plus the 3 untagged ones.**
- tier `MIXED` (5; each also holds a section marker, so (d) would leave it out too): 2026-08-07_a-check-that-cannot-fail; 2026-08-13_headline-must-match-the-operative-case; 2026-08-14_i-read-representations-they-read-sources; 2026-08-16_a-recorded-blocker-is-not-a-boundary; 2026-08-16_an-overstated-record-gets-discounted-wholesale
- no tier line (3; "untagged is W" reversed): 2026-10-12_be-more-careful-with-coding-files-and-deploys; 2026-10-12_clear-fleet-activity-once-answered-as-a-rule; 2026-10-31_never-invoke-a-write-command-to-read-what-it-would-say

(d) 57. All are tier `W` or `M`, scoped to this seat, with clean frontmatter.
- a tier-like line in the body (2): 2026-09-05_three-tier-learnings-wednesday-management-agents-project (line 26); 2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice (line 19, "Tier 2 stays on Sonnet")
- names Datasec in its text, file name or rule line (55): 2026-08-03_role-beyond-code-three-priorities; 2026-08-04_delegation-v2-observability; 2026-08-05_identities-float-verify-always; 2026-08-06_ask-format-client-project-options-rec; 2026-08-07_authorship-is-checkable-dkim; 2026-08-07_autonomy-grant-ship-decisions; 2026-08-07_enumerate-every-surface-before-done; 2026-08-12_morning-ticket-sweep-autostart; 2026-08-13_containment-never-run-is-a-claim; 2026-08-13_establish-authority-before-reconciling; 2026-08-13_shared-bus-tag-filter-or-leak; 2026-08-15_a-cap-is-never-neutral; 2026-08-15_a-gui-open-is-a-write; 2026-08-16_classification-is-the-field-that-grants-authority; 2026-08-25_travel-drive-stale-pointers; 2026-08-26_a-sync-that-cannot-refuse-a-deletion; 2026-09-02_rotate-in-the-70-80-band-conditionally; 2026-09-02_style-guides-never-mixed; 2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact; 2026-09-05_tickets-are-the-channel-whatsapp-via-kam-is-the-escalation; 2026-09-07_a-census-complete-over-a-frame-that-is-not; 2026-09-07_a-prior-ruling-gate-refusal-is-a-research-prompt; 2026-09-07_name-the-field-that-says-whose-it-is; 2026-09-07_production-ban-lifted-for-the-week; 2026-09-08_a-false-absence-is-usually-my-own-instrument; 2026-09-08_a-ghost-suggestion-is-dangerous-in-proportion-to-what-is-unwritten; 2026-09-08_take-ownership-of-wed-work; 2026-09-09_a-guard-refuses-malformed-input-and-the-real-failure-is-stale-input; 2026-09-09_quarantine-by-rename-is-not-removal-on-an-additive-sync; 2026-09-10_a-refusal-nobody-reads-is-indistinguishable-from-working; 2026-09-14_kams-instruction-stands-until-he-withdraws-it; 2026-09-14_the-coordinator-adds-value-or-it-is-waste-three-duties-not-watching; 2026-09-16_a-fix-authored-on-one-machine-is-a-claim-until-the-other-machine-runs-it; 2026-09-16_measure-the-whole-interface-before-answering-can-it-be-done; 2026-09-16_never-edit-a-bash-script-that-is-currently-running; 2026-09-17_every-project-keeps-kams-clarifications; 2026-09-20_a-closure-inherits-the-scope-of-its-measurement; 2026-09-20_a-control-in-the-wrong-scan-mode-buys-confidence; 2026-09-20_an-absence-goes-stale-while-you-compose-the-complaint; 2026-09-20_an-early-return-disarms-tests-outside-the-diff; 2026-09-20_most-of-a-project-folder-is-outside-its-git-repo; 2026-09-20_prepared-in-a-scratchpad-is-lost; 2026-09-20_refuting-a-mechanism-is-not-refuting-the-defect; 2026-09-21_a-partition-table-must-identify-seats-by-what-they-can-measure; 2026-09-24_decisions-go-on-the-fleet-activity-panel; 2026-09-25_three-tier-routing-ornith-spark-cloud-always-on; 2026-10-04_as-much-secuura-work-as-possible-spark-and-claude; 2026-10-08_ornith-15-replaces-10-push-it-harder; 2026-10-18_new-account-tickets-backlog-routing-definition-spark-max; 2026-10-23_kam-items-on-fleet-activity-morning-card-48h-email; 2026-10-23_tuesday-never-wait-on-kam-cards-morning-card-48h-email-priorities; 2026-11-10_never-wait-a-green-item-ships-and-every-wait-watches-the-board; 2026-11-11_nas-dev-working-dated-offload; 2026-11-11_wednesday-offloads-to-dev-working-nas; 2026-11-27_fleet-structure-project-fable-postgres-brain-tiered-briefs-skills

## The ten questions on the real index, before and after

Same questions, typed as before (`evidence/ten_questions_round4_raw.txt`; round 3's are in `evidence/ten_questions_round3_raw.txt`). "First five" is the knowledge results; the two incident rows under them are unchanged in kind.

| # | Question | Round 3, first five | Round 4, first five | Lost? |
|---|---|---|---|---|
| 1 | what must be true before I close a pane | #1 `a-pane-close-is-a-session-kill` | #1 the same | no (old #4, a neighbour, is left out) |
| 2 | what do I check before telling Kam something is absent | #1 `a-false-absence-is-usually-my-own-instrument` | that lesson is LEFT OUT (d: it names Datasec); #1 is now `a-safety-claim-names-the-property-it-checked`, a neighbour | **yes, the answer is lost** |
| 3 | rules about typed clock times | #1 the "GENERATE timestamps" section of `i-read-representations-they-read-sources`; #2 `read-the-clock-at-boot` | the first is LEFT OUT (c: MIXED); `read-the-clock-at-boot` is now #1 | partly: one of two right answers |
| 4 | what provenance does each fact in a brief need | #1 `brief-provenance-enforcement`; #2 `classification-is-the-field-that-grants-authority` | #1 the same; #2 is LEFT OUT (d) | partly: the second answer |
| 5 | an agent has gone quiet ... | #1 `an-instruction-to-wait-must-name-what-wakes`; #2 `exercise-mechanisms-before-arming` | #1 to #4 the same | no |
| 6 | what do I do instead of deleting files | #3 `never-delete-cleanup-means-quarantine` | #1 to #4 the same | no |
| 7 | a deploy failed, can I skip it | nothing right; #1 `if-something-blocks-move-on-to-the-next` | the same wrong neighbour first | no change (still wrong) |
| 8 | the usage gauge is high ... | #1 to #3 the usage and routing lessons | #1 to #5 the same | no |
| 9 | how do I word a decision card for Kam | #1 `decisions-go-on-the-fleet-activity-panel` | that lesson is LEFT OUT (d); #1 is now `wednesday-go-counts-as-kams-word-for-starting-work`, not the answer | **yes, the answer is lost** |
| 10 | what do I verify before merging after the QA gate | #4 `secuura-we-approve-and-merge-our-own-tested-work` only | #1 to #4 the same | no change |

Right lesson in the first five: 8 of 10 in rounds 2 and 3; **6 of 10 now**, and for question 2 the tool gives a confident neighbour where it used to give the answer. Both lost lessons are left out for one reason: they mention Datasec in passing. `check` and `doctor` say 93 are left out; nothing tells a seat that the lesson it wanted is one of them unless it reads the list.

## Suite and mutants

- Suite, final code: **682 passed, 0 failed**, Python 3.14.10 (`evidence/test_run_round4.log`) and `/usr/bin/python3` 3.9.6 (`evidence/test_run_round4_python39.log`). 128 planted lessons left out under the planned clause; 34 lessons that must qualify. Round 3 was 483.
- Mutants: RE-RUN IN PROGRESS on the final code; the figure goes here.
- The checker's surviving mutants named in the brief: N06 and N07 (`N5_names_not_closed`, `N5_folders_not_closed`), N10 (`N3_no_assert_in_reads`, which section 12d's `status` test also catches), N11 (`N13_no_rebuild_lock`), N14 and N15 (`N14_sock_mode_untested`, `N15_sock_symlink_ok`; the mode test now uses a short path so it reaches the mode check), N24 (`N24_scope_change_unseen`: a scope file that differs by one comment line makes `check` red with 0 paths differing). **N27, a credentials folder below the top level, has no mutant of its own that can go red:** the closed table now refuses that line first, so removing the credentials test alone changes nothing. The line is refused in section 8; I count that guard as doubled, not as proved separately.
- N9: `search quillwort marshwort` puts the rules row first at the default limit, at `--limit 20` and at `--limit 1`, with eight lessons outscoring it (mutant `N9_rules_row_after_the_cut`).

## What I could not make sound

1. **Clause (d)'s name test reads words, not meaning.** It finds the name plain, in any case, accented, full-width, inside a domain, split by markdown emphasis, and clause (t) removes look-alike letters and invisible characters. It does NOT find the name written with a space or a hyphen inside it ("Data sec"), with a digit for a letter, as an abbreviation ("DS"), or by a project's name alone ("NexusAI", "HPSM"). A lesson about the other client's work that never uses the client's name qualifies. I do not think a name list can close this, and I have not pretended it does.
2. **Clause (c) trusts the tier line.** A lesson that says `tier: W` in a clean block and is in fact about the other client qualifies on (c). Only (b) and (d) stand behind it.
3. **Folders are checked once, not held.** Each file is judged on the descriptor it is read from, inside its own folder opened without following a link. The folders above it are checked by `realpath` before that. A process that can swap a whole brain folder for a symlink mid-rebuild is outside this guard. Not tested.
4. **"Both through realpath"** is met for the addressed side only; see above. A server started by hand through a symlink is refused, not recognised.
5. **A hard link whose original is gone, and a secret pasted into a lesson,** as in round 3.
6. **The `BRAINDB_TEST_HOLD` pause is test-only code in the indexer.** Set in a real shell it delays a rebuild by up to 60 s and does nothing else. It is the only way I found to make the in-transaction assertion a test that can fail.

## Slips of mine in round 4

1. **A redundant guard hid a mutant.** Two tests both caught "two rows with one key", so the mutant removing one survived my first mutant run. I removed the redundancy and added a mutant for the `#n` case.
2. **Three mutants left a scratch server running each** (their broken guard let one start, and my suite did not stop it). I stopped the three with `pg_ctl` on their own data directories and added a stop line to the suite. Process lists here select by executable and then read `-D`.
3. **Four mutant expectations were mis-aimed in the first run** (caught, but on a line my pattern did not name; one test's scope kept the lines the mutant was meant to bypass). Corrected; the full set was re-run on the final code.
4. Two shell commands of mine were refused by the hooks before running (an unquoted list variable under zsh; a bare `======`). Nothing had run.
5. My first fixture builder made a symlink before its folder existed, and wrote the rules index before the last lessons had added their rows. Both showed as failures in the first two suite runs.
6. The interim status I wrote at 17:12 said "60 mutants"; the run had 61.

## Not tested in round 4

- A real TUESDAY or FRIDAY tree; another machine or drive; ejecting or syncing with the server up; unison with the proposed `Path` lines; a real Postgres major-version difference; the proposed blocks inside the real `doctor.sh` or launcher.
- A second real rebuild, so no timing on a quiet machine and no check of rebuild-to-rebuild sameness on the real tree (the suite proves it on fixtures).
- The first checker's attack tree (`tests/attack_tree.sh`): not re-run. Its 69 expectations include "present" cases that the new rule reverses on purpose (untagged lessons, lessons with no row, marked sections), so its count would no longer mean what it meant.
- The second checker's `seat_f2.sh`, `seat_f2_part2.sh` and `f3_f5_f7.sh` as files: they hold that checker's own scratch paths. Their F2c, S6, F4 and F3c are lifted into the suite; their S1 to S5 (seat names), F2a, F2b, F5 and F7 blocks are covered only as far as round 3's own sections and section 12d go.
- The NFD file-name case on the drive volume (the suite ran on the internal volume, where it passes).
- The 150 s lock limit to its end (2 s, by `BRAINDB_LOCK_WAIT`).
- `proposed/scope/tuesday.scope` and `friday.scope` beyond the fixtures. Their allow lines are all inside the table; their comment text still describes round 3's seat-word rule and I left it.
- Search quality beyond the ten questions.

## What exists (bytes)

`braindb.sh` 16,242; `braindb_index.py` 72,538; `braindb_lock.py` 1,446 (unchanged); `scope/wednesday.scope` 2,151 (comments only changed); `tests/run.sh` 63,735; `tests/make_fixtures.py` 35,343; `tests/mutants.sh` 20,228; `tests/f1_new_adapted.py` 21,020 (the checker's script with the one change named above); `DESIGN.md` 16,392; `proposed/PROPOSALS.md` 13,477 (item 7 is now `Path` lines, N12); `proposed/INSTRUCTIONS-for-other-seats.md` 16,311 (step 1 rewritten: a seat adopts by confirming; the Python sentence, the row count and the "names every lesson kept out" sentence corrected). New evidence: `test_run_round4.log`, `test_run_round4_python39.log`, `mutants_round4.log`, `checker_f1_new_round4_unmodified.txt`, `checker_f1_new_round4_every_case_has_a_good_row.txt`, `real_rebuild_round4.txt`, `ten_questions_round4_raw.txt`, `at_crosscheck_round4.txt`, `measurements_round4.txt`, `left_out_lessons_round4.txt`.

**End state of the drive cluster** (`evidence/measurements_round4.txt`, 17:59:26): `stop` rc 0 (pid 18598), second `stop` rc 0, `server: STOPPED`, no `postmaster.pid`, socket directory empty, 0 processes whose executable is postgres with a data directory in this lane (1 postgres on this Mac, another project's, not touched; control: 33 bash). 

## QUESTION (does not block QA; it decides how useful the index is)

**Clause (d) as written costs 57 lessons; the brief expected 5.** The brief says a lesson must hold no other-client "marker or token ANYWHERE in its text (the tier-marker comment in any spelling, or another client's name from the seat's own short list)", and then "the checker counted 5 such real lessons today". The 5 are the lessons with a marker. The name test is what takes the other 55, and `ANSWER-1.md` ruling 1 had said nothing is dropped by client name. I built what the sentence says. The two readings, measured:

| Reading | Lessons indexed | Left out under (c) and (d) | Questions 2 and 9 |
|---|---|---|---|
| As built: marker, tier-like line, or the other client's name anywhere | 199 | 65 | lost |
| Marker or tier-like line only (drop the name test; measured by a dry run with no `deny_clients` line) | 254 | 10 | both lessons are back in the index |

Going from the first to the second is one test removed (`Qd_name_ok` is that change, as a mutant). It would also let in a section about the other client that carries no marker at all, which is the thing the second checker's N2 was about. Which do you want?

---

# ROUND 3 (superseded where ROUND 4 says so; its first line was READY FOR QA) (answer to `ANSWER-3.md`: the checker's NO GO on F1, and Wednesday's list of eleven fixes and four notes)

WED build seat "brain-db". Round 3 finished; the last process check printed `2026-11-27 13:40:45 AEDT`, and one more suite run under Python 3.9 ended 13:41:32 with 0 postgres executables running. All HOLDS kept: this lane only (plus my scratchpad and socket directories under `/tmp`), no existing shared file edited, the checker's directory read and never written, no git write, no mail, post or network call, nothing installed, no `rm`.

**In one paragraph.** All eleven MUST FIX items and the four notes are built and tested. The suite is 483 passed, 0 failed (also under Python 3.9.6). The checker's own attack tree, re-run by me against the new code, gives **0 unexpected of 69** (it saw 26). A mutant harness breaks the tool 24 ways in a copy, one at a time, and the suite goes red on the matching assertion for 24 of 24, including the checker's M2. **One item ended differently from its first instruction, as that instruction allowed:** WEAK MATCH is removed. The checker's fix was built and measured on 36 questions; no threshold separates right from wrong, so the tool now states a fact instead of a verdict. The drive cluster is STOPPED. Four things I got wrong while working are listed under "Slips of mine".

## The verdict against the answer, where they differ (the stricter taken each time)

| Point | Checker's verdict | `ANSWER-3.md` | Built |
|---|---|---|---|
| F2 rating | Major | Blocker | fixed either way; every server-talking command now checks the server's data directory |
| F6 stale pid file | "move it into quarantine and continue, or at least print the instruction" | do NOT move it; print the `mv -n` line | prints; never moves |
| F11 | test the name when it begins `_ledger` or the folder is unusual | refused whatever kind the allow line gives | name tested everywhere except a file in its own kind's home folder; ledgers only by `allow ledger`, daily folders only by `allow daily` |
| Look-alike daily names (zatk81 to 83) | counted as passes | target is 0 unexpected | a daily note must be named as a plain date, so all four are out |

## The eleven items

| # | Item | What changed | Tests (the mutant named is the proof the test can fail) |
|---|---|---|---|
| 1 | F1 lesson deciders fail closed | (i) BOM stripped, leading blank lines skipped, frontmatter keys folded; a lesson is EXCLUDED and named when the frontmatter is unclosed, `tier` occurs more than once (block, second block, or stray line above the first heading), or a tier line yields no value. (ii) Own clients are matched on the CLIENT segment only. (iii) Rejected rules-index rows are kept; a lesson named by any of them (stripped, case-folded, path removed) is excluded and listed with the row's line; keys of good rows are normalised the same way; no usable rules index means `rebuild` and `check` REFUSE (rc 2). (iv) Markers in any case, indent and spelling, blank lines allowed; the dropped span runs to the next heading of the same or a higher level; a marker with no heading under it drops to the next heading. (v) UNTAGGED lessons are listed by name. | Every case of `atk_build.py` is lifted into `tests/make_fixtures.py` under its own name and token, each with a neighbour: 23 frontmatter cases and 9 neighbours, 11 marker cases and 6 neighbours, 13 rules-index cases and 2 neighbours. Sections 6, 6b, 7b, 8b. Mutants: `F1i_key_not_folded`, `F1i_faults_ignored`, `F1i_bom_kept`, `F1ii_client_substring`, `F1iii_rejected_rows_ignored`, `F1iii_keys_not_normalised`, `F1iii_no_index_not_refused`, `F1iv_marker_strict_spelling`, `F1iv_marker_blank_line`, `F1iv_subsection_kept`. |
| 2 | F2 server identified by its data directory | `need_server()` runs `show data_directory` and dies with rc 4 unless it equals the directory the command was addressed to. `rebuild`, `check` and `status` print the data directory. `doctor` reports "ANOTHER cluster is answering". | Section 12b reproduces the checker's P6: main cluster up, second cluster stopped, same socket directory, self-start off. `rebuild`, `check`, `search`, `at` each rc 4; the main index's file count and tree are unchanged; no GREEN is printed. Mutant `F2_any_server_will_do`: 16 lines red. |
| 3 | F3 hard links | A file with a link count above 1 is skipped with "hard link (link count N)". `DESIGN.md` point 15 says what this cannot do. | Planted `4_Credentials` file hard-linked into `learnings/`; absent, and named in the report. Mutant `F3_hard_link_through`. |
| 4 | F11 seat words independent of kind | See the table above. | Section 7a widens the allow-list under five kinds onto both other ledgers, both other daily folders, `2_Project_Files/tuesday/`, and `0_Brain/tasks/` (the checker's two routes: `allow skill 0_Brain/tasks/*.md` and `allow lesson` / `allow skill` over `_ledger_*`). All seven planted tokens stay out, while this seat's own pickup file enters by the same line. Mutant `F11_seat_word_by_kind`. |
| 5 | F4 scope first | `need_scope` runs before anything is created or started, for `rebuild`, `check`, `search`, `at`, `up`. | Section 12: a tree named TUESDAY with no scope file; five commands refused, no cluster directory, no server. Mutant `F4_scope_checked_late`: 6 lines red. |
| 6 | F5 two commands at once | `init`, `start`, `stop` and the self-start run under `flock` on `pgdata-<seat>.lock` (`braindb_lock.py`); rebuilds take the same lock; after a failed `pg_ctl start` the tool re-tests "running". | Section 13b: two searches on a stopped cluster, two starts, and three trials of two searches with no cluster at all; every command rc 0 and the new cluster survives. Mutant `F5_no_lock`. |
| 7 | F6 stale pid file | `start`, `search` and `up` print `STALE PID FILE: ... names pid N, which is alive but is NOT this index's server` and the exact `mv -n` line; the file is not moved. The row is in the instructions. | Section 14. Mutant `F6_stale_pid_unexplained`. |
| 8 | F7 one bad file | An unreadable file is skipped and listed; a row over 80,000 characters is cut with a marker and listed; the rebuild's LAST line says so; `check` prints the counts. | Section 9b: a mode-000 lesson and a 300,000-word section; rebuild rc 0, no traceback, both listed, last line `DONE WITH FAULTS: 1 unreadable file(s) skipped, 1 row(s) truncated`. Mutants `F7_unreadable_aborts`, `F7_row_not_capped`. |
| 9 | F8 separator bytes | 0x1E and 0x1F are stripped on read. | Section 11: the row holding them is found by `search`; the database holds it once. Mutant `F8_separators_kept`. |
| 10 | F9 the foreign-process test | The sleeper now sets SIGINT back to default and is killed with SIGINT at the end to show it can die. | Mutant `F9_stop_trusts_pidfile` is the checker's M2: `the foreign process was killed by stop` now FAILS under it (3 lines on that assertion, 29 red in all). My first attempt did not: see slip 1. |
| 11 | F10 WEAK MATCH | Removed. See the section below. A rules-file row now goes first only when it holds every one of the question's rarest words. The instructions carry the sentence about retrying with three or four key words. | Section 11: the last line states score and held and lacking words; no "WEAK" anywhere. Mutants `rules_row_always_first`, `lessons_first_off`. |

## The four notes

| Note | What changed | Test |
|---|---|---|
| Seat follows the tree | `braindb.sh` takes the seat from the tree through `tools/seat_note.sh` (read, sourced, not edited). `WED_AGENT` disagreeing, or a folder with another name, is refused with rc 2. Where a copied tree lacks `seat_note.sh` the same rule is applied inline over `seat_resolve.sh`. | Section 1. Mutant `seat_follows_WED_AGENT`. |
| `devnas.prf` | The proposal says line 53. The ignore lines are now `pgdata-*`, `pgdata-*.lock` and `_probe_*`, which covers the quarantined probe cluster. | read against the file |
| `PORTABILITY.md` item number | The file's last item today is 31. The proposal says NN and that the sibling `nas-backup` lane proposes one too, so Wednesday numbers both. I did not read that lane. | read against the file |
| Test socket directory | Unique per run (`/tmp/wed-bdb-t<pid>` and `...b`), moved into the run directory at the end. | Section 18 |

Also from the checker's N2 and N5: the doctor logic moved into `braindb.sh doctor` (no hard-coded Postgres path; every exit code named); `at` with a trailing newline is refused; a non-numeric setting is a plain message; a broken pipe during a rebuild no longer prints "Exception ignored".

## Tests

`evidence/test_run_round3.log`, tail:

```
finished 2026-11-27 13:39:45 AEDT
RESULT: 483 passed, 0 failed
```

483 PASS, 0 FAIL, 33 lines marked `(can fail)`; 91 planted tokens absent and 61 neighbour tokens present in the whole-index dump (round 2: 295 passed; 36 and 37). The same suite under `/usr/bin/python3` 3.9.6: 483 passed (`evidence/test_run_round3_python39.log`).

**The suite now runs the tool from its own copy** in `<scratch>/.../sim/WEDNESDAY/`, because the tool refuses a tree not named for a seat. Its result no longer depends on which scope files a tree has adopted.

**Mutants** (`tests/mutants.sh`, output `evidence/mutants_round3.log`): control 483 passed, 0 failed; **24 of 24 mutants caught on the expected assertion.** Each mutant is one change to a copy; the lane is never modified.

**The checker's attack tree, re-run by me** (`tests/attack_tree.sh`, which runs the checker's `atk_build.py` unmodified from where it lies; output `evidence/attack_tree_round3.log`): 69 expectations, **0 unexpected**; control `xneighbour01` found 9 times; this lane's own canaries found 0 times; no PWNED file; 0 server processes left.

## Real run on the drive cluster (`evidence/measurements_round3.txt`, `evidence/real_rebuild_round3.txt`)

| Measure | Round 2 | Round 3 |
|---|---|---|
| Files indexed | 419 | 419 |
| Lessons indexed, of 293 lesson files | 264 | 264 |
| Lessons kept out because the tier or a rules-index row could not be read safely | not measured | 0 |
| Damaged rules-index rows | not measured | 0 of 379 |
| Hard links, unreadable files, truncated rows | not measured | 0, 0, 0 |
| Untagged lessons indexed, now named | not shown | 3 |
| Search rows | 22,246 | 22,267 |
| Rebuild | 4.4 to 4.6 s | 4.7 to 4.9 s |
| `check` | 0.20 s | 0.48 s |
| Size on the drive | 157 MB | 174 MB (`du`); the database is 118 MB |
| Search, default order | 117 to 237 ms | 121 to 230 ms |
| Cold start: one search on a stopped server | 0.53 s | 0.46 s |
| `at` against `rules_card.py --at`, 22 triggers | 802 and 802 | 802 and 802, none only on either side |
| End state | STOPPED | STOPPED: `stop` rc 0 (pid 12933), second `stop` rc 0, `server: STOPPED`, no `postmaster.pid`, 0 processes whose executable is postgres (control: 8 bash) |

So fail-closed costs the real Wednesday index nothing today. The first-five lists for the ten questions are the same as round 2's second table (`evidence/ten_questions_round3_raw.txt`).

## F10: the threshold study, and why WEAK MATCH is gone

The questions and what counts as a right first result were written to `evidence/threshold_questions_round3.tsv` before any was run under the new measure: my ten, the checker's eight, eight of its nine probes (the ninth repeats my question 5), and ten new ones. 36 in all; 2 I could not judge and left out; of the 34 judged, the first result is right for 21 and wrong for 13.

| Measure | Best single threshold | Wrong first results NOT flagged | Right first results flagged | Errors |
|---|---|---|---|---|
| Round 2's (all terms of the question) | 0.0251 | 4 of 13 | 1 of 21 | 5 of 34 |
| The checker's fix, rarest 3 terms | 0.0243 | 5 of 13 | 2 of 21 | 7 of 34 |
| The checker's fix, rarest 4 terms | 0.0340 | 2 of 13 | 3 of 21 | 5 of 34 |

Source: `evidence/threshold_study_round3_confidence_measure.txt`, which has the full 36-row table.

- The new measure is no better overall. It trades two missed wrong answers for two more false alarms.
- Its best line sits between a wrong first result at 0.0337 and a right one at 0.0343: a gap of 0.0006, narrower than the 0.004 the checker called over-fitted, and chosen on the same 34 questions it is scored on.
- It does not cure the length problem it was meant to cure. My question 5 (right first result) scores 0.0001 on its rarest four words, against 0.0717 for the checker's four-word form of the same intent: the lesson holds "wake" and "wait" but not "quiet", "gone" or "prove".
- The two wrong answers it never flags are the dangerous kind: `how do I name a git branch` (0.0546, an unrelated lesson) and `Kam`.
- To flag every wrong first result, any of the three measures has to flag all 21 right ones.

No threshold separates right from wrong honestly, so, as item 11 directs, the line is replaced by a neutral one:

```
(7 results, 125 ms; first result: score 0.0172; of the question's 4 rarest words it holds 2 [skip move] and lacks 2 [deploy fail])
```

That is a fact a reader can weigh. It is not a safe verdict either, and I have not made it one (`evidence/threshold_study_round3_neutral_line.txt`): of the 21 right first results 18 hold every rare word of their question; of the 13 wrong ones, 4 do.

**What this changes in an accepted reading.** `ANSWER-2.md` accepted "a rules row goes first only when its match is not weak". With no threshold left, the rule is now: a rules-file row goes first only when it holds every one of the question's rarest words (up to four); otherwise it competes on score. Same purpose, no fitted number. On the 36 questions the first results are unchanged by this.

## Could not fix, or fixed only in part

1. **WEAK MATCH** has no honest threshold; removed, as above. The guard against "a weak answer that looks confident" is now the reader's eye on the last line plus the instructions, not the tool.
2. **A hard link cannot be told from a copy** once the original is gone, and pasted secret text is invisible to any path rule. Stated in `DESIGN.md` point 15 and in the instructions.
3. **The Wednesday seat's own records carry no seat word in their names** (`_ledger.md`, `daily/`, `tasks/NEXT-PICKUP.md`), so a Tuesday or Friday scope is kept out of them by its allow-list and by "a ledger only by `allow ledger`, a daily folder only by `allow daily`", not by a word. A Tuesday scope that wrote `allow ledger 0_Brain/learnings/_ledger.md` would index Wednesday's ledger. The instructions say so in step 1.
4. **Fail closed has a cost I chose:** "a second frontmatter block" is detected as a `---` line directly after the frontmatter with another within 40 lines, and a stray tier-looking line is looked for in the 60 lines before the first heading. A real lesson shaped like that would be kept out and named. None is today.
5. **The checker's own harness needs two small changes to run against round 3,** because of fixes it asked for: its mutant anchors for M4, M6, M7 and M13 point at lines that no longer exist (M1, M2, M3, M5, M8, M9, M11 and M14 still match), and any copy of the tool it runs directly must sit in a folder named WEDNESDAY, TUESDAY or FRIDAY. Its `atk_build.py`, `proc.sh`, `crash.sh` and `sim_tuesday.sh` set `WED_AGENT=wednesday` on the real lane or use a tree named TUESDAY, which the new seat rule accepts; I ran only `atk_build.py`.

## Slips of mine in round 3

1. **My first fix for F9 repeated the fault it was fixing.** I swapped `sleep` for a Python sleeper and killed it with SIGTERM to "prove" it could die. A background child of a non-interactive bash starts with SIGINT ignored and Python keeps it ignored, so under the M2 mutant "still alive" still passed. The mutant run showed it. The sleeper now resets SIGINT and is killed with SIGINT.
2. **I signalled a process by a text pattern.** Cleaning up after the mutant run I selected "postgres with a `-D` under my scratchpad" by grepping command lines, and the only match was my own shell, whose command line held the pattern. I sent it SIGINT; it was my own tool shell and nothing else was touched. The scratch server I was after had already exited. Process lists in this status come from a script that selects by executable, then reads each one's `-D`.
3. **The F9 mutant left a scratch test server running for a time** (its `stop` is broken on purpose). It had exited by the time I looked. The harness prints the count; it does not clean up.
4. Smaller: I edited `tests/mutants.sh` while it was running, which aborted that run (re-run whole afterwards); a lifted token (`xcanary151`) contained an older one as a prefix and produced false failures until I renumbered; a recursive grep of a fixture tree hung on a planted FIFO; I typed one clock time into an interim status and removed it; the indexer source briefly held a literal BOM character where an escape was meant, found by a mutant anchor failing to match.

## Not tested in round 3

- Any real TUESDAY or FRIDAY tree, another machine or drive; ejecting or syncing with the server up; a real Postgres major-version difference; the proposed blocks inside the real `doctor.sh` or launcher (they ran in a stub harness: `evidence/proposals_simulated_round3.txt`).
- The checker's `proc.sh`, `crash.sh`, `sim_tuesday.sh`, `atk_scopes.py` and `atk_inject.py` as scripts. Their cases are covered by my own sections 7a, 9b, 12, 12b, 13b and 14, not by running them.
- More than three trials of the double-init race.
- Search quality beyond the 36 questions.

## QUESTION (does not block QA)

The neutral last line replaces a warning Wednesday asked for in `ANSWER-1.md` item 7 ("when the top result's rank is weak ... the tool prints one line"). `ANSWER-3.md` item 11 allows the replacement when no threshold separates honestly, and that is what the data shows. If a warning is still wanted despite the numbers, the least bad one on this data is "the first result lacks one or more of the question's rarest words": it would flag 9 of 13 wrong first results and 3 of 21 right ones. I have not built it.

---

# ROUND 2 (answer to `ANSWER-1.md`: four rulings, three changes)

WED build seat "brain-db". Round 2 finished; last process check printed `2026-11-27 12:23:19 AEDT`. All HOLDS kept: this lane only, no existing shared file edited, no git write, no mail, post or network call, nothing installed, no `rm`.

**In one paragraph.** All seven items are done and tested: 295 of 295 scratch tests pass, and the drive cluster is STOPPED. The `at` cross-check is now exact (802 rule lines on both sides). Lessons-first puts the right lesson in the first five for 8 of the ten questions with no flag needed, and the new WEAK MATCH line fires on both misses. **One expectation in the answer is not met: question 7 still does not find the hard rule**, because that rule's sentence is in the workspace file `/Volumes/DevMASTER/CLAUDE.md`, which item 6 rules out; the tool now says WEAK MATCH there instead of looking confident. Two new questions are at the end of this section.

## The seven items

| # | Item | What changed | Tests (each able to fail) |
|---|---|---|---|
| 1 | Boundary is path-and-tier | No code change. The boundary is stated in Wednesday's words in `DESIGN.md` ("The boundary") and at the top of `INSTRUCTIONS-for-other-seats.md` and in the proposed `PORTABILITY.md` item 32. No row is dropped by client name. | - |
| 2 | Narrow the name test | Lessons are decided by the rules index `seats` column: out when every row names only other seats; no row means the tier rule alone. `tuesday` / `friday` / `laptop_datasec` are now `deny_seat_word` lines: they exclude a folder name (any kind) or the file name of a ledger or daily note, and never a lesson, skill or architecture file. | Section 6: planted lessons scoped only to `friday` and only to `tuesday` are absent; neighbours present: a lesson with `tuesday` in its name scoped `all`, one with `laptop_datasec` in its name and no row, one with a row for another seat plus a row naming this seat, a skill and an architecture file named for Tuesday. Section 7a: with the ALLOW-LIST widened onto `daily_tuesday/`, `daily_friday/`, both other ledgers and `2_Project_Files/tuesday/`, the seat words still keep all five out; 7b: with the deny lines removed too, all five enter (the failing case). |
| 3 | On demand, stopped at wrap | `rebuild`, `check`, `search`, `at` start the server themselves (and create the cluster if there is none); `search` and `at` build a missing index. `BRAINDB_NO_AUTOSTART=1` turns that off for `doctor.sh`. `proposed/PROPOSALS.md`: launcher block does `up`; wrap line stops; item 6 is the one-line eject and sync note; item 7 is the exclusion line for the sync profile I found. | Section 13: with self-start off, `check` on a stopped server is rc 3 and starts nothing (the failing case); `search`, `check`, `at` each bring it up. Section 16: a self-start on a mismatched version marker is refused. Section 17: `search` on an emptied index rebuilds it. Section 18: `search` with no cluster at all creates one, builds and answers. |
| 4 | Other seats' scopes are theirs | Both stay in `proposed/scope/`. `INSTRUCTIONS-for-other-seats.md` now opens with "STEP 1, before anything else: confirm or change your seat's scope file before the first rebuild" and a table of what each line does. Nothing is decided for them; Friday's missing `deny_clients` line is marked as my guess. | Section 12: a seat with no scope file is refused; the wrong seat's file is refused. |
| 5 | Lessons first by default | No `--kind`: rules files, lessons, skills and the like by score, then up to two incident rows under their own heading. `--all` gives the old mixed order. | Section 11: for a word in five ledger headlines and one lesson body, the lesson is result 1 by default and a ledger row is result 1 under `--all`. |
| 6 | Rules files in scope | `CLAUDE.md` and `0_Brain/CLAUDE.md`, kind `rules`: 45 rows (34 and 11), one per numbered rule (including `0a` and `3b-i`) and one per heading section's other text. A rules row whose match is not weak is listed ahead of every lesson. A root file can be allowed only by exact name. | Section 6: seven expected rows with exact headings; a third `CLAUDE.md` elsewhere and a conflict copy of the root one are absent. Section 8: `../CLAUDE.md`, a root wildcard and a root file of another kind are refused. Section 11: the rules row is result 1; with the threshold raised above every score the same row is not promoted (the failing case). |
| 7 | Say what a result is | Every result line carries its kind. `WEAK MATCH` is printed when the best result scores under 0.035, `NO MATCH` when nothing matches; both point at `at <trigger>`. | Section 11: all result lines carry a kind (3 of 3); a one-word-in-four query prints WEAK MATCH; a good match does not; the same good match does when the threshold is raised; an excluded word prints NO MATCH and a found word does not. |

## Tests

`evidence/test_run_round2.log`, tail:

```
finished 2026-11-27 12:20:09 AEDT
RESULT: 295 passed, 0 failed  (run directory .../scratchpad/braindb-test-20261127-121953-12601)
```

295 PASS, 0 FAIL, 22 lines marked `(can fail)`; 36 planted tokens absent and 37 neighbour tokens present in the whole-index dump (round 1: 217 passed; 35 and 23). The first round-2 run had 6 failures, all from two fixture tokens I had not renamed for files that are now rightly indexed; fixed in the fixtures.

## Real run, round 2 (`evidence/measurements_round2.txt`)

| Measure | Round 1 | Round 2 |
|---|---|---|
| Files indexed | 433 | 419 |
| Lessons indexed | 281 | 264 |
| Search rows | 22,203 | 22,246 (45 of them rules rows) |
| Rule lines | 364 | 345 |
| Not indexed, of files matching an allow line | 16 | 32: 26 lessons by the seats column, 2 by tier, 4 conflict copies |
| Rebuild | 4.6 to 4.8 s | 4.4 to 4.6 s |
| Size on the drive | 158 MB | 157 MB |
| Search, default order | - | 117 to 237 ms |
| Cold start: one search on a stopped server | - | 0.53 s in all |
| End state | STOPPED | STOPPED: `stop` rc 0 (pid 17759), second `stop` rc 0, `status` rc 3, no `postmaster.pid`, 0 processes whose executable is postgres (control: 5 bash) |

**The `at` cross-check after ruling 2** (`evidence/at_crosscheck_round2.txt`): 802 rule lines in the index, 802 on the card, none only on either side, across all 22 triggers. The 5 lines that were only on the card in round 1 are in the index. What still differs is order only: the first five differ in order for 12 of 22 triggers and in membership for 10, because the index counts citations in this seat's two ledgers and the card counts every seat's.

**What ruling 2 moved.** Two lessons excluded by name in round 1 are back (`claim-a-task-with-tuesday-before-starting-it`, `tuesday-never-wait-on-kam-cards...`), and so is the architecture file `2026-09-16_tuesday-vs-wednesday-structure.md`. In the other direction, the seats column now removes 26 lessons that round 1 indexed; they are listed by name in `evidence/excluded_files_round2.txt`. See question A.

## The ten questions, second table (default order, round 2)

Same questions, typed as before. The first table, below in the round-1 report, is unchanged. Scores are on the new normalised scale, so they are not comparable with round 1's numbers; the ordering rule is the same.

| # | Question | Default `search`, first five | WEAK MATCH printed? | Against round 1 |
|---|---|---|---|---|
| 1 | what must be true before I close a pane | #1 `a-pane-close-is-a-session-kill` (0.0501) | no | same as before |
| 2 | what do I check before telling Kam something is absent | #1 `a-false-absence-is-usually-my-own-instrument` (0.0382) | no | same |
| 3 | rules about typed clock times | #1 the "GENERATE timestamps, never type them" section (0.0260); #2 `read-the-clock-at-boot` | yes, wrongly | was five ledger rows and no lesson; now right without `--kind` |
| 4 | what provenance does each fact in a brief need before I send it | #1 `brief-provenance-enforcement` (0.0716); #2 `classification-is-the-field-that-grants-authority` | no | same |
| 5 | an agent has gone quiet, what proves the wake can fire before I wait on it | #1 `an-instruction-to-wait-must-name-what-wakes` (0.0067); #2 `exercise-mechanisms-before-arming` | yes, wrongly | now right without `--kind`; but this morning's ledger row for exactly this failure, #3 in round 1, is no longer shown (the two incident rows printed are older ones); `--all` still shows it |
| 6 | what do I do instead of deleting files when cleaning up | #3 `never-delete-cleanup-means-quarantine`; #1 is a neighbour (0.0294) | yes, rightly | was absent from the first five; now #3 |
| 7 | a deploy failed, can I skip it and move on | nothing right; #1 is still `if-something-blocks-move-on-to-the-next` (0.0172); no rules row in the five | yes, rightly | same wrong neighbour, now flagged |
| 8 | the usage gauge is high, which model do I launch a seat on | #1 and #2 the two usage lessons (0.0544), #3 the routing lesson | no | same |
| 9 | how do I word a decision card for Kam | #1 `decisions-go-on-the-fleet-activity-panel` (0.0674) | no | was #4; now #1 |
| 10 | what do I verify before merging after the QA gate returns | #4 `secuura-we-approve-and-merge-our-own-tested-work` only; the QA-gate lesson is not in the five (#1 scores 0.0340) | yes, rightly | was nothing right; now a related lesson at #4, flagged |

Right lesson in the first five: 8 of 10 with no `--kind` (round 1: 5 of 10 without it, 8 of 10 with `--kind lesson`). Right lesson first: 7 of 10.

**Question 7 and the rules files (item 6), reported as found.** The sentence "Never skip a failure. If a deploy fails..." is hard rule 7 of `/Volumes/DevMASTER/CLAUDE.md`, the workspace file one level above the tree, which item 6 excludes. The tree's own `CLAUDE.md` holds only rule 6, "`always-verify-and-check` and `no-skip-on-failure` apply here exactly as in the main workspace", and the question's words do not match it (Postgres stems "failed" and "failure" to different words). `search "..." --kind rules` returns that rule 6 row first with a score of 0.0004. Searching the rule's own name, `no-skip-on-failure`, does return `CLAUDE.md:89` (rule 6) first. The rules kind itself works: "portability first" returns `CLAUDE.md` rule 0 first at 0.1027, ahead of the portability lesson. To make question 7 find hard rule text, the workspace `CLAUDE.md` would have to be allowed, which is a ruling for Wednesday (question B).

**The threshold, 0.035, and how far to trust it.** On the ten questions the first result's score was 0.0382 to 0.0716 for the five right answers that were not flagged, and 0.0172, 0.0294 and 0.0340 for the three wrong first results, all flagged. The two right answers at 0.0260 and 0.0067 are flagged wrongly. So on this data the line catches every wrong first result and cries wolf on 2 of 7 right ones. It is fitted to ten points and the gap it sits in is narrow (0.0340 to 0.0382). I set 0.035 before I had seen the normalised scores, as a conversion of a 0.30 cut on round 1's scale, and kept it when the data agreed; a probe outside the ten ("ledger archive rows older than three days") found the right rule first at 0.0304 and was flagged. Read WEAK MATCH as "check this", not as "wrong". `BRAINDB_WEAK` overrides it.

## Readings and deviations in round 2

1. **Tier is still tested before the seats column.** Ruling 1 keeps another client's project files out; ruling 2 says a lesson with rows is decided by `seats`. Where both apply I keep the stricter: a lesson of a denied client's project tier stays out even if a row scoped it `all`. The two such lessons today are scoped to other seats anyway, so nothing turns on it yet.
2. **"Rule lines ahead of ledger rows" (item 5):** rule lines are not separate search rows. Each lesson's rules-index line is indexed inside that lesson's rows at heading weight and printed under every lesson result. `at <trigger>` remains the list of rule lines.
3. **A rules-file row goes ahead of lessons only when its match is not weak** (score at or above the threshold). Item 6 says "ranked above lessons"; ranking every rules row first regardless would make the rules file the new confident wrong neighbour that item 7 guards against.
4. **Default output is five knowledge results plus up to two incident rows**, so it prints up to seven. The cost is in question 5's row above.
5. **`search` and `at` do not rebuild a stale index**, only a missing one. A rebuild is about five seconds; `check`, and `up` in the launcher, are where staleness is caught.
6. **Pickup and week files** (ruling 2 names them) are not on any allow-list and there is no record kind for them. If a scope ever allowed `0_Brain/tasks/` under a document kind, a file named `NEXT-PICKUP-TUESDAY.md` would not be stopped by its name. Today the allow-list is what keeps them out.
7. **Scores changed scale** (divided by the query's rarity mass). Order within a query is unchanged by that.
8. **Evidence files:** round-1 files are untouched; round 2 wrote `*_round2*` files beside them.

## Not tested in round 2 (in addition to round 1's list below)

- Two commands racing to self-start the server at the same moment.
- The proposed `doctor.sh`, launcher, wrap and sync lines in place.
- The threshold on any question beyond the ten and the probes named above.

## QUESTIONS from round 2 (none blocks QA)

A. **The seats column now removes 26 lessons from the Wednesday index** that round 1 held, because every rules-index row for them names only other seats. Some look as if this seat might want them: `2026-11-18_the-kit-stamp-checklist.md`, `2026-09-23_use-the-local-model-as-much-as-possible.md`, `2026-09-22_ornith-is-studio-only-not-datasec.md`, `2026-11-21_a-holding-helper-gets-the-next-useful-job.md`. That is the rules index's data, not the tool, and I did not read those lessons to judge it. Is the list in `evidence/excluded_files_round2.txt` what you intended?

B. **Question 7 cannot find the hard rule under item 6 as written**, for the reason above. Do you want the workspace `/Volumes/DevMASTER/CLAUDE.md` allowed as a third rules file (it is outside the tree, and it carries the other client's tenant and environment detail), or is WEAK MATCH the accepted answer there?

---

# ROUND 1 report (as submitted; its figures are round 1's, superseded where ROUND 2 above says so)

WED build seat "brain-db" (WED-170 step 4). Last process check printed `2026-11-27 12:09:04 AEDT`. Nothing shared was edited; no git write, mail, post or network call was made.

**In one paragraph.** The index works on the drive: `braindb.sh` creates a Postgres 15 cluster in `pgdata-wednesday/` on DevMASTER, serves it on a Unix socket only, rebuilds from 433 files in under 5 seconds, and the scratch test suite passes 217 of 217. The drive cluster is STOPPED. On the ten questions, lesson search put the right lesson in its first five for 8, against 6 for `rules_card.py --at`; the two miss different questions. Full text is useful enough to build on without vectors, with two real weaknesses stated below. Four questions for the coordinator are at the end; the first matters most: the brief's exclusions (by path and by tier) do not keep the other client's name out of the index.

## What exists (bytes, from `stat`)

| File | Bytes | What it is |
|---|---|---|
| `braindb.sh` | 8,777 | the tool: `init start stop status up rebuild check search at` |
| `braindb_index.py` | 37,109 | the indexer (standard library; database access through `psql` only) |
| `scope/wednesday.scope` | 1,153 | the live allow-list for this seat |
| `DESIGN.md` | 4,795 | one page, written before the code |
| `tests/run.sh` | 22,926 | the suite; takes a scratch directory |
| `tests/make_fixtures.py` | 7,273 | builds the fixture brain (planted `xcanaryNN` files, `xneighbourNN` neighbours) |
| `proposed/PROPOSALS.md` | 9,807 | text for `PORTABILITY.md` 25 and a new 32, `doctor.sh`, the launcher, the wrap, the sync profiles; a rollback line each |
| `proposed/INSTRUCTIONS-for-other-seats.md` | 9,095 | exact steps for Tuesday and Friday |
| `proposed/scope/tuesday.scope`, `friday.scope` | 918, 1,028 | proposed allow-lists, NOT live |
| `evidence/ten_questions.md` | 1,285 | the ten questions, written before any search existed |
| `evidence/ten_questions_raw.txt` | 100,780 | every result for all ten, three ways |
| `evidence/at_crosscheck.txt` | 1,958 | `at` against `rules_card.py --at`, all 22 triggers |
| `evidence/measurements.txt` | 3,169 | size, rebuild time, latency, other-client counts |
| `evidence/excluded_files.txt` | 2,367 | the 16 files the exclusions removed, with reasons |
| `evidence/test_run_final.log` | 15,017 | the final test run, whole |
| `.gitignore` | 133 | ignores `pgdata-*/`, `_probe_*/`, `_quarantine_*/` |
| `pgdata-wednesday/` | 158 MB | the drive cluster, STOPPED, gitignored |
| `_quarantine_2026-11-27/` | 39 MB | the first drive probe cluster and its socket directory (moved, not deleted) |

## Facts re-measured (no difference from the brief)

- `/opt/homebrew/bin/postgres` and `psql` report 15.19.
- `diskutil info /Volumes/DevMASTER`: Case-sensitive APFS, Owners Disabled.
- Drive proof, before anything else: `initdb` on `_probe_1127/` in this lane succeeded (directory mode 700), a socket-only server started, answered `select version()`, and `lsof -i` on its pid printed nothing.
- One thing the brief did not say: another project's seat had its own Postgres running on this Mac during my first test run (data directory under a Secuura scratchpad, `listen_addresses=127.0.0.1`). My tools never touched it; `stop` identifies a server by its data directory only. It was gone by the end.

## Tests (`tests/run.sh <scratch>`, scratch cluster only)

Final run, tail of `evidence/test_run_final.log`:

```
finished 2026-11-27 12:08:54 AEDT
RESULT: 217 passed, 0 failed  (run directory .../scratchpad/braindb-test-20261127-120844-70326)
```

217 PASS lines, 0 FAIL lines, 18 lines marked `(can fail)`. What the suite proves:

| Section | Proof | How it is shown able to fail |
|---|---|---|
| 5, 6 | The indexed path set is exactly the 15 expected paths. 35 planted tokens are absent from a whole-index `pg_dump`; 23 neighbour tokens are present. One planted file per exclusion: `tuesday`, `friday`, `laptop_datasec`, `(conflict_on_`, `.pre-` (both name shapes), two Datasec tier spellings, a project tier naming no client, a Datasec-marked section inside a MIXED lesson, `0_Brain/dashboard/` (chat store and markdown), `0_Brain/reference/`, `4_Credentials/` (reached through a symlink), `3_Access_Keys/`, other seats' ledgers and daily folders, a sub-folder, an off-list folder | the absence assertion pointed at a neighbour token is red; the presence assertion pointed at a planted token is red |
| 7 | With the `deny_path` and `deny_clients` lines removed from the scope, 11 of the planted files DO enter the index | this is the failing case for section 6, run for real |
| 8 | Ten scope lines naming credentials, keys, dashboard, reference, a chat store, `..`, an absolute path, a wildcard directory, a non-`.md` pattern or an unknown kind are each refused, and the index is unchanged. A symlinked directory is skipped | `check` stays green after the refusals |
| 9 | `check` is red on a changed, added and removed file and names the path; an excluded file changing is not named; 26 differences print exactly 20 paths and `(+6 more)`; green after `rebuild` | green control before the first change |
| 10 | Two rebuilds give byte-identical dumps (the build time and `pg_dump`'s random token aside) | the permissive dump, filtered the same way, differs |
| 11 | `search` finds by word, honours `--kind` and `--limit`, gives zero for an excluded file's word and for stop words; `at pane` lists the right two rules, most reinforced first, and refuses a trigger that is not one word | zero-result assertion is red on a neighbour word |
| 12 | Seat `tuesday` is refused with no scope file; the wrong seat's scope file is refused; the proposed Tuesday and Friday scopes give mirror-image results on the fixtures | - |
| 13, 14 | `stop` leaves no process; a second `stop` is rc 0; a pid file pointing at a live foreign process is refused and that process stays alive; a pid file naming another data directory is refused; a stale pid is a no-op | one-process control before the stop |
| 15 | A socket path over 103 bytes and a socket directory not mode 700 are refused, and nothing starts | - |
| 16 | A start on a mismatched `PG_VERSION` marker is refused with the word "rebuild" | with the real marker back, the same start succeeds |
| 17 | After an immediate (unclean) stop the index is empty, `check` says so, `rebuild` restores it | - |

The first test run had 10 failures. All ten were faults in the tests, not the tool: a `ps | grep` that counted itself, an override the test wrapper did not pass through, and a random token `pg_dump` 15.19 writes into every dump. Fixed in the tests.

## Real run on the drive cluster

| Measure | Value | Source |
|---|---|---|
| Files indexed | 433 (281 lessons, 115 daily notes, 21 architecture, 9 skills, 2 ledgers, 2 identity, 2 people, 1 rules index) | first `rebuild` output |
| Search rows | 22,203 (19,289 daily, 1,938 ledger, 684 lesson sections, 237 architecture, 47 skill, 6 identity, 2 people) | first `rebuild` output |
| Rule lines | 364 of the 379 in the rules index (15 belong to excluded lessons) | first `rebuild` output |
| Source bytes | 19,637,231 | `evidence/measurements.txt` |
| Rebuild time | 4.82 s first; then 4.72, 4.72, 4.56 s | `rebuild` output |
| Size on the drive | 158 MB for `pgdata-wednesday/` (`du`), of which the database is 117 MB | `evidence/measurements.txt` |
| `check` | GREEN, 433 files, 0.20 s | `evidence/measurements.txt` |
| Query latency | 28 to 34 ms with `--kind lesson`; 96 to 233 ms across all kinds | the figure `search` prints, 18 runs plus the ten questions |
| Whole command, lesson search | 0.13 s | `time` |
| `at`, all 22 triggers | 790 rule lines against the card's 802; none only in the index; the 5 only on the card all belong to two lessons excluded for "tuesday" in their name | `evidence/at_crosscheck.txt` |
| End state | STOPPED: `stop` rc 0 (pid 48946), second `stop` rc 0, `status` rc 3, no `postmaster.pid`, 0 processes whose executable is postgres (control: 5 bash) | process checks at 12:06:41 and 12:09:04 |

## The ten questions

Questions were written before any search existed and typed exactly as written; no ranking constant was changed after seeing results. "Right lesson" is my judgement from the rules index. For 7, 9 and 10 I looked the right lesson up by grep after seeing the results.

| # | Question | `search`, all kinds, top 5 | `search --kind lesson`, top 5 | `rules_card.py --at`, top 5 | Found it |
|---|---|---|---|---|---|
| 1 | what must be true before I close a pane | #1 `a-pane-close-is-a-session-kill` | #1 same | `pane` (21): not in the top 5; nearest is `check-the-refusal-before-the-kill` | search |
| 2 | what do I check before telling Kam something is absent | #1 `a-false-absence-is-usually-my-own-instrument` | #1 same | `report` (62): #4 and #5, the same lesson | both |
| 3 | rules about typed clock times | five ledger rows, each a typed-clock incident; no lesson | #1 the section "GENERATE timestamps, never type them"; #2 `read-the-clock-at-boot` | `report`: #2 "generate it... never retype it" | both; search only with `--kind lesson` |
| 4 | what provenance does each fact in a brief need before I send it | #1 `brief-provenance-enforcement`; #2 `classification-is-the-field-that-grants-authority` | same | `brief` (115): the provenance rule is not in the top 5 | search |
| 5 | an agent has gone quiet, what proves the wake can fire before I wait on it | #3 today's ledger row for exactly this failure; the rest are related incidents | #1 `an-instruction-to-wait-must-name-what-wakes`; #2 `exercise-mechanisms-before-arming` | `wait` (25): #5 the same lesson | both |
| 6 | what do I do instead of deleting files when cleaning up | not in the top 5 | #3 `never-delete-cleanup-means-quarantine` | `drive` (23): #1 | card |
| 7 | a deploy failed, can I skip it and move on | nothing right | #1 `if-something-blocks-move-on-to-the-next`, which reads as the opposite advice | `deploy` (16): nothing right | neither |
| 8 | the usage gauge is high, which model do I launch a seat on | #1 and #2 the two usage lessons, #4 the routing lesson | #1 to #4 | `usage` (8): #2, #3, #4 | both; search better ordered |
| 9 | how do I word a decision card for Kam | #4 `decisions-go-on-the-fleet-activity-panel` | #1 same; the BLUF-first lesson is not found | `card` (52): none of the card-shape rules | search, partly |
| 10 | what do I verify before merging after the QA gate returns | nothing right | #5 `secuura-we-approve-and-merge-our-own-tested-work` only | `merge` (20): #5 `qa-gate-before-my-verification` | card |

Right lesson in the first five: search across all kinds 5 of 10; search with `--kind lesson` 8 of 10; the rules card 6 of 10. They miss different questions (search misses 7 and 10; the card misses 1, 4, 7 and 9).

**Is full text too weak? No, but it has two weaknesses and one trap.**

1. **It matches words, not meaning.** Question 6 says "cleaning up"; the lesson says "cleanup", which Postgres stems to a different word. Question 10's words (verify, merge, gate, returns) are spread thinly over dozens of lessons. This is the case vectors exist for. I would not add them yet: the cheaper fix is that the card already covers this case when the seat knows its trigger.
2. **Ledger rows crowd lessons out.** There are 1,938 ledger rows and 19,289 daily rows against 684 lesson sections, and an incident row repeats the question's words more densely than the rule does. Questions 3, 5 and 6 only work with `--kind lesson`. Showing lessons first by default is the obvious next change; I did not make it after seeing the results, so that the table above stays an honest first reading.
3. **The trap: a confident wrong neighbour.** Question 7's rule lives in `CLAUDE.md` hard rule 7 and a vault skill, neither of which is on the allow-list, so search returned the nearest lesson, which says to skip a blocked item. A seat reading that mid-task would be misled. The root rules files are worth adding to the scope.

What search adds that the card cannot: the section of the lesson and a snippet, the incident rows (question 5 surfaced this morning's wake failure), and no need to know the trigger word. What the card has that search lacks: fleet-wide reinforcement order, and it works with no server.

## Deviations from the brief, each with its reason

1. **Untagged lessons are indexed** (5 on this seat). The brief names only lessons whose tier names another client; `boot_digest.py` also treats untagged as included.
2. **Stricter than the brief on tiers:** a project tier that names none of the seat's own clients, or any unrecognised tier value, is excluded. None exists today.
3. **Sections marked `<!-- tier: P-Datasec/... -->` inside an indexed lesson are dropped** (2 on this seat), mirroring `boot_digest.py`. The brief only speaks of whole lessons.
4. **Daily notes:** a non-bullet line is folded into the bullet above it, or kept as its own row, rather than dropped. The brief says one row per bullet line; dropping the rest would lose text.
5. **`at` weights count this seat's two indexed ledgers only**, so the order of the first five differs from the card for 12 of 22 triggers (and the set of the first five for 10). Reading the other seats' ledgers to count citations would break the allow-list.
6. **`deny_path` words are matched case-insensitively on the tree-relative path**, so the tree's own folder name (`/TUESDAY/`) can never exclude everything.
7. **Extras not asked for:** an `up` command (the launcher line needs it), `at --top N`, `check` also going red when the indexer or the scope file has changed, and the Tuesday and Friday scopes as proposals exercised on fixtures.
8. **The test socket lives in `/tmp/wed-braindb-501-test`, not the scratchpad.** The scratchpad path is about 98 bytes and the macOS socket limit is 103. The scratch cluster itself is in the scratchpad.
9. **Left behind outside the lane:** two empty mode-700 directories, `/tmp/wed-braindb-501-wednesday` and `/tmp/wed-braindb-501-test`. Not removed (no `rm`).
10. **`__pycache__/` (60 KB) in the lane**, made by my own syntax check; gitignored.
11. **Read beyond the read-first list, all read-only:** parts of `boot_digest.py`, `seat_resolve.sh`, the head and some greps of `doctor.sh`, greps of `Launch_Wednesday.command`, the `ignore` lines of `devnas.prf`, lesson frontmatters, sample ledger rows and one daily note's line starts. `rules_card.py --at` was run 32 times (it writes nothing). `git check-ignore` and `git status` were run.
12. **Hooks:** one command was refused (an unquoted variable in zsh) and rerun under bash; several advisories fired on case-sensitive greps and on reading `$?` after a pipe. One early line printed `initdb rc=` blank for that reason; the `initdb` result was read from its own output and the start that followed.

## What I did NOT test

- Any other machine, drive or seat tree. The Tuesday and Friday scopes ran on fixtures only.
- The `doctor.sh` block and the launcher block in place (I edit no shared file). Their three `check` exit codes were exercised through `braindb.sh`.
- Ejecting the drive with the server running, a drive pulled mid-run, and the drive sync or NAS sync copying `pgdata-wednesday/`.
- A real Postgres major-version difference (only a changed `PG_VERSION` marker).
- Running under Python 3.9 (the file parses under 3.9.6; it ran only under 3.14.10).
- Two seats' servers on one Mac at once, and a `search` during a `rebuild`.
- Whether the launcher's environment differs from this pane's in a way that matters to `pg_ctl`.
- Search quality beyond these ten questions.

## QUESTIONS (none blocks QA)

1. **The brief's aim and its mechanism disagree.** It says "Another client's text must not be able to enter this index" and defines the exclusions by path and by tier. With exactly those exclusions, the index still names Datasec in 53 of 281 lessons, 815 of 19,290 daily rows, 79 of 1,938 ledger rows, 56 architecture sections and 11 of 364 rule lines (control: 6,478 rows name Secuura). These are the Wednesday seat's own files, which it already reads at boot, so the index exposes nothing new; but the sentence as written is not met. Is path-and-tier the accepted boundary, or do you want rows that name the other client dropped as well (which would also drop shared rules)?
2. **"Path contains tuesday or friday" removes 9 lessons and one architecture file from the Wednesday index**, and 5 rule lines that the rules index scopes to all seats and that `rules_card.py --at` shows this seat today (`claim-a-task-with-tuesday-before-starting-it` and four from `tuesday-never-wait-on-kam-cards...`). I took the strict reading. Should the word test apply only to the ledger and daily names it was meant for? The list is `evidence/excluded_files.txt`.
3. **Stop at wrap, or leave it running between sessions?** The launcher line starts the server; nothing stops it unless the wrap does. `proposed/PROPOSALS.md` item 5 has the line.
4. **Friday's proposed scope denies no client**, because Friday works for both. That, and the Tuesday scope's `deny_clients secuura`, are my reading and need the coordinators' word before `INSTRUCTIONS-for-other-seats.md` is sent.
