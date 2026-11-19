This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is the LAUNCH addendum the deputy brief's addendum 0 refers to. Read, in order and WHOLE: `coagent/CLAUDE.md`; `2026-11-17_coagent_M3_DEPUTY_brief.md`; `2026-11-19_coagent_M3_DEPUTY_ADDENDUM-0_update_before_launch.md`; this file. Where they differ, the later file wins.

# M3 DEPUTY — ADDENDUM 0b: launch facts

1. **The daemon tip for addendum 0 §1's start check:** `8b8c6c755db66a1c481d9719707c3cdc924fb70c` (merged to `main` under daemon addendum 15; Friday launches you only after reading `git ls-remote origin main` herself). Your check: `git fetch origin`; `git merge-base --is-ancestor 8b8c6c755db66a1c481d9719707c3cdc924fb70c origin/main` exit 0 AND `git ls-tree origin/main crates/coagent-daemon` non-empty. If not: last line `BLOCKED: daemon not on main`, and wait.
2. **Branch from `origin/main` as it is at your start** (record its SHA). Note: addendum 0's pre-check read main at `bfe435a`; main has since gained audit-fix3 (`36537eb`) and the daemon. Neither touches `crates/coagent-roster`; `crates/coagent-daemon` now also depends on `coagent-roster` (addendum 0 §3 named it): re-read its uses at your branch point and add them to `tests/api_stability.rs`.
3. **Section 9's three sentences: RULED by Kam** (live board 2026-11-19 16:24:22, card `general-c2c-deputy-three-sentences-1119`, verbatim: "a — Use them as drafted"). Copy the brief's section 9 sentences into `docs/ROSTER.md` word for word, with the line "Approved by the owner, 2026-11-19 (use as drafted)"; NOT marked draft.
4. **Model and slots:** you run on the model set at launch. Heavy-run limit machine-wide: TWO (addendum 0 §6 item 5's count). Other seats build tonight.
5. **The method:** you end at `READY FOR QA M3-DEPUTY`; ONE independent check follows; a NO GO goes to Kam.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
