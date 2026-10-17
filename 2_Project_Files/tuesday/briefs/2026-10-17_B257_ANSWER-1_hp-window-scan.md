From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC, to seat B257 (pane Datasec/HPSM-POC-R3). ANSWER-1 to your STOP (B257_STATUS.md, 16:33 AEDT): the HP-mail window-scan source.

## BLUF
RULED: **do NOT run the hpwin window scan yourself, and do NOT open the Source_Documents copy** (that hold stands). Carry on with everything else in the brief. Record the scan in NOT TESTED as "owed to Tuesday: run at the PR, before it opens", and go to your RECORDS DONE line as normal.

## Why
- The source moved on purpose: on 2026-10-16 B250 found it held a live credential, so it now sits in Tuesday's own credentials folder. A seat is never pointed at a secret-bearing file, even through a process that prints only counts.
- Tuesday will run `hpwin.py` herself, with its source set by environment variable, over every path on `records/b257` (read from the pushed branch), with the `--control` arm firing, BEFORE opening the PR. A hit means the PR is not opened and the file goes back to you.

## What to keep doing
- Every other scan stays yours: gitleaks per path with the canary, the person-name / customer-name / key-value checks, and the byte-equal read-backs.
- Write by hand what you would have checked: list every Jira text and committed path in STATUS under a heading `HPWIN OWED TO TUESDAY` so she scans exactly that set. For Jira texts already posted, that is a read-back list (ids), not a re-post.
- Do NOT quote HP's mail in anything; the rule is unchanged. If you are unsure whether a sentence came from HP's mail, leave it out and say so.
