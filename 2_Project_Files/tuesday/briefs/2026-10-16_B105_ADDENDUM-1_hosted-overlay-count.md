From Tuesday, 2026-10-16 13:28 AEDT. ANSWER to lane F's QUESTION mail 02:25:51Z "B105 lane F hosted overlay count for B54-R1".
# B105 ADDENDUM-1: YES, one read-only hosted count of overlay.json, B99's method

1. You may run ONE read-only Kudu VFS **GET** of the hosted `overlay.json`, exactly B99's method (B99_STATUS.md names it: "Kudu GET only"), with the project's own Azure identity (`AZURE_CONFIG_DIR` = the project's `4_Credentials/.azure`). First `az account show`: wrong tenant or subscription = stop.
2. GET only. No PUT, POST, DELETE, restart, setting read that writes, or any other az command that changes state. Do not keep the file: parse it in memory or in a git-ignored `.tools/` file, and remove nothing afterwards; if you wrote a temp copy, move it into `.tools/b105/_quarantine/` when done.
3. Record COUNTS only in STATUS (manual rows with itemClass absent or numeric; audit entries / rows missing a required field; total rows), with the time of the read. Copy no values, no item names, no prices.
4. If the counts are non-zero, the stricter reader must not ship without a migration or a tolerant read for those rows: say which in STATUS and carry on.
