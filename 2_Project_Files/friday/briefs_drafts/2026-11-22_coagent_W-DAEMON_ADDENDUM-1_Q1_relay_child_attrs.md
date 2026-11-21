This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat W-DAEMON only. It answers your STOP Q1. Report under "## ADDENDUM 1 (Q1 ruled)" in your STATUS file.

# W-DAEMON — ADDENDUM 1: STOP Q1 ruled (a)

**Ruling: (a), exactly as you proposed.** You may ADD three lines to `crates/coagent-daemon/src/relay_child.rs`, one `#[cfg_attr(not(unix), allow(dead_code))]` directly above each of `FRAME_SHORT` (:485), `FRAME_LENGTH` (:486) and `read_frame` (:491), and NOTHING else in that file: no body, comment, order or other line changes. Why (a): the three items are dead on Windows only because hosting is out (W-7), the attribute changes nothing for a non-Windows build, and keeping `-D warnings` whole is worth more than an `-A dead_code` exception on the gate line.

Proof at the end, in STATUS section (8):
- `git diff origin/main...HEAD -- crates/coagent-daemon/src/relay_child.rs` shows exactly 3 added lines, each that attribute, and 0 removed lines (count both with a positive control);
- the file's end hash is recorded beside its start value, with "changed only by ADDENDUM-1's 3 lines";
- the Windows type-check (a) and (b) then end with 0 warnings, and the clippy gate line of section 4 item 4 runs WITHOUT `-A dead_code` and exits 0.
Section 5 item 6's "byte-identical" check for `relay_child.rs` is replaced by that proof; all the other forbidden files stay byte-identical. Add one BACKLOG line under the hosting entry: "relay_child.rs: three items carry cfg_attr(not(unix), allow(dead_code)) until hosting is ported to Windows; remove them then."

Good work on 25 -> 0, and on finding that the program file shows no error.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
