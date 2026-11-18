This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It answers the QUESTION at the end of your STATUS section "BLOCKERS (A1 item 5 …)". Everything in addendum 1 that is not named here stands.

# M3_AUDIT-FIX — ADDENDUM-2: ruling on the wrapper question

RULING (Friday, 2026-11-18): YES. Add `crates/coagent-audit/tests/qa_fix_wrapper.rs` on the model of `tests/gate_r5_wrapper.rs`: `#[rustfmt::skip]`, `#[allow(clippy::int_plus_one, dead_code)]` with one written justification per allow (the file is the independent check's and is kept byte for byte), and `#[path = "qa_fix.rs"] mod qa_fix;`. Point the `[[test]] name = "qa_fix"` entry at it. `tests/qa_fix.rs` stays byte for byte (sha256 `ebca51aecad605c3f58c34ea21bd4d0dbc94c051108f4ca2a54c30b7cb5eb6e8`): no rustfmt run on it, no attribute inside it.

Limits of the ruling:
- Only those two lints are allowed, and only for that module. If clippy or rustfmt then asks for anything else, do not widen the allow: quote it and STOP.
- The wrapper holds nothing but the attributes, their justifications and the `mod` line.
- Addendum 1 section 2 item 5's diff-stat list gains exactly this one file: `crates/coagent-audit/tests/qa_fix_wrapper.rs`. Six files, nothing else.
- After the change, run the seven `qa_fix` tests again through the wrapper and confirm each gives the result your item 1 recorded.

Then resume at addendum 1 section 2 item 5 from its beginning. The last line is unchanged: `READY FOR MERGE CHECK M3-AUDIT-FIX r2`. Good catch, and the right call to stop instead of editing the check's file.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
