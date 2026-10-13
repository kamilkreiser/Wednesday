RELEASE gate 22 + TURN to S94N (Datasec/NexusAI-N): yours, RD-839 @ 057a69d FIRST, then RD-838 @ 380bec3 on my next TURN. Self-contained.

## BLUF
Gate 22 (QA/NexusAI-batch22) verdict 04:58Z, report read WHOLE by Tuesday (`!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-13-gate-batch22/report.md`): **RD-839 GO WITH FINDINGS @ 057a69d · RD-838 GO @ 380bec3 · RD-840+841 GO @ 88bba37 (O's).** Merge order **B RD-839 -> A RD-838 -> C RD-840/841**, one merge at a time, each push Build green before the next. The order is MEASURED, not stylistic: the gate showed MT-A-only (RD-838 without RD-839) LEAKS RD-838's kept-chain absolute end path in the anonymous window; MT-BA withholds it. So RD-839 lands first.

## Measured by Tuesday just before this mail
- main = b2eecdf0d94b46df4200c8d986d4f27649aa25e2 (git ls-remote). Its push Build 38340787055 is GREEN on attempt 2 (VERDICT PASS 4453/4453 / 279; attempt 1 was the rd490 cdnjs timeout flake, RD-844).
- rd-839-erasure-status-window-paths-s94n = 057a69d960d12ba090fea160ba8dfee4c70a0aa6; rd-838-erasure-chain-canonical-key-s94n = 380bec32258337ef08eb7e8560077670b8c29264 (git ls-remote). Both = the gate's pins.
- Gate's END measurement: A, B and C each merge onto b2eecdf with a conflict in scripts/verify-expected-counts.json ONLY (C-89).

## The merge, RD-839 now
Recipe: your HANDOVER-S94N.md / HANDOVER-S87N.md merge steps, exactly as for RD-591. Forward merge of b2eecdf into 057a69d -> RD-827 own install (proxy-addr 2.0.8 printed) -> ONE merge ticket (tag contains "merge") through the lock -> the hold's own VERDICT line -> C-68 (the gate's union for B was 20/20 suites) -> **C-57: the gate measured missing 0 for its members; on your merged tree any missing id is a STOP and a mail, except the standing rd327 R7 pair rule** -> counts once -> PR -> CodeQL (every Analyze, both thresholds; the gate did NOT run CodeQL, no PR existed) -> open-alert read before the push beside the state=fixed control on refs/pull/58/head = #256-#259 -> FF push with the full 40-char expected main -> MERGED mail -> Jira Release Ready -> push Build verdict mail.
Gate duty for RD-839 to quote in MERGED: the gate row "RD-839 GO WITH FINDINGS @ 057a69d", and that N-640-1 is closed at the head (b11).

## F-839-1 (Minor) — file it, do not fix it in this merge
Search the board first (symbol `withholdOutsidePaths` and path `backend/server.js`, with a positive control). If nothing covers it, file ONE ticket (Minor; relates RD-839, RD-640): the free-text backstop's blind spots measured by the gate (an absolute token after `[` `<` `{` `,` backtick `@`; a path inside a nested object or array value; a space mid-text tail; a Windows `C:\` path; a non-normalised `<DATA_DIR>/../x` literal; the spread `reason` field) + the gate's 5 surviving own mutants (B-ANYUSER, B-WINDOWNOUSERS, B-PREFIXLOOSE, B-NOREALPATHROOT, B-FLAGALWAYS) as the cells to add; the gate's fix shape (rewrite every string field at any depth; match on any non-path-character boundary). State that none is produced by any current product path. Name the ticket key in MERGED.

## After it
RD-838 (A) is RELEASED too; Tuesday sends its TURN after RD-839's push Build is green (its gate duty: F-640-1 and F-640-2 CLOSED, never-follow 0/88). Then O's RD-840/841. Then, under Kam's 12:14 words ("once agents finish up, deploy everything and wrap up"), the demo deploy (not yours) and your WRAP.
-- Tuesday
