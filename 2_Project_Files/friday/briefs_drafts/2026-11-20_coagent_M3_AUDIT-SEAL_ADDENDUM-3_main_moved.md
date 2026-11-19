This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. For the M3 AUDIT-SEAL seat. It changes the ORDER of your brief's section 5, nothing else.

# M3 AUDIT-SEAL — ADDENDUM 3: main has moved; merge it before the final runs

`origin/main` moved after your brief was written: the daemon lane merged, and Friday read `git ls-remote origin main` = `8b8c6c755db66a1c481d9719707c3cdc924fb70c` (it holds `36537eb`, your base, plus `crates/coagent-daemon` and `crates/coagent-mcp`; `crates/coagent-audit` and `crates/coagent-roster` are unchanged by it, read with `git diff --stat 36537eb 8b8c6c7` per crate).

Your brief's section 5 item 1 would merge it at the end and re-run everything. To avoid running the final suite twice: finish (or stop at a clean point) the run you are in, then do section 5 item 1 NOW (`git fetch origin`; `git merge origin/main` INTO `m3-audit-seal`, never a rebase; a conflict outside your owned paths is a STOP; note that `coagent-daemon` does not depend on `coagent-audit` at `8b8c6c7`, so nothing of yours should break there, but if a new dependant of `coagent_audit` appears and fails, STOP), then run section 5 items 2 to 8 ONCE on the merged tree. Record in STATUS which runs were on the unmerged head and which on the merged one; only the merged-tree runs count for READY.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
