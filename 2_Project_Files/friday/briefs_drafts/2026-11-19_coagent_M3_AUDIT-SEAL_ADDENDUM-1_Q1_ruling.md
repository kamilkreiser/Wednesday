This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It answers STOP Q1 of `coagent/5_Project_History/STATUS_M3_AUDIT_SEAL.md` and changes no other rule of the brief `2026-11-19_coagent_M3_AUDIT-SEAL_brief.md`.

# M3 AUDIT-SEAL — ADDENDUM 1: ruling on STOP Q1

**The question (yours):** may you add the one arm `Record::Segment(_) => FieldClass::Segment,` to the exhaustive match in builder-owned `crates/coagent-audit/tests/bundle.rs:149` (`expected_class`), marked and with the old match quoted, so the `bundle` test target compiles with `Record::Segment`?

**Read by Friday before ruling:** `git show 36537eb:crates/coagent-audit/tests/bundle.rs` lines 145-165: `expected_class` maps every `Record` variant to its `FieldClass`; it is a builder-owned helper (not in the brief's protected list), and design 10 pairs `Record::Segment` with `FieldClass::Segment`. This is the compile consequence design 10's DQ-S4 predicted for an exhaustive match.

**RULING (Friday, 2026-11-19): PERMITTED AS ASKED.** Add exactly that one arm, with a line above it `// RULING (Friday, 2026-11-19, audit-seal Q1)` and the old match's last arm quoted as `// old:` context. The list is closed at that one arm: any other builder-owned test that needs a change to compile is a NEW STOP question (the brief's closed list stands), and a protected file never is edited. Record the edit in STATUS with the diff.

Resume where you stopped; the last line goes back to `IN PROGRESS: <item>`.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
