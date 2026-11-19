# B1753 | Datasec / OXPd: the Fable review pass of the architecture and the plan (C-5). READ-ONLY. FOUR REVIEWERS, ONE LANE EACH.

From Tuesday (Datasec coordinator seat). Client: Datasec. Project: OXPd. Model: the newest Fable (`0_Brain/dashboard/data/models_latest.json`, key `fable`), by the product owner's instruction for this project. Drafted 2026-11-19 by Tuesday (s294); NOT launched at drafting: it launches on the account switch or the allowance renewal (pickup DELTA 1267), or on the product owner's word to start now.

## Why this exists (the authority, quoted)
- CLARIFICATIONS C-5 (the product owner, Friday's terminal, 2026-11-18): "no problem.  use opus now and we will run a fable run to review". The architecture and the plan were synthesised on Opus; two of the twelve analysis reports (C1, C2) were written on Opus. This is that Fable run.
- The product owner to Tuesday (terminal, 2026-11-19): "i would like you to switch to latest fable and use fable agents when working on this project".
- Both documents are DRAFTS (handover section 5): no independent review has read them. You are that review. You owe the documents nothing: a claim you cannot trace is a finding, however plausible it reads.

## What you review, and against what
All paths are under `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-18_datasec-oxpd/`.
- UNDER REVIEW: `02_architecture.md` (801+ lines) and `03_plan-of-attack-and-build.md` (337+ lines).
- SOURCES, in order of authority: (1) `CLARIFICATIONS.md` C-1 to C-30 (the product owner's words; C-1 is the brief and is the requirement list); (2) the library itself, read-only, at `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd` (a verified copy; the reports cite `library:path:line`); (3) the twelve reports in `analysis/` (A1 to A7, B1 to B3, C1, C2). A report is a representation of the library, not the library: where a document's claim is load-bearing (a platform limit, a protocol, a security property, anything a phase exit rests on), open the library file the report cites and read the lines. Where the report and the library disagree, the library wins and BOTH are findings.

## The four lanes (read your lane's sections WHOLE; read the other document's BLUF and change log for context)
| Lane | Sections under review | Main sources |
|---|---|---|
| R1 parity | 02 sections 3 (all requirements), 5.6, 7.4 to 7.6; 03 phases 3 to 5 and their work packages | A1, A2, A3, A4, A5, A6; C-16 (full match of everything), C-20, C-28, C-29 |
| R2 platforms | 02 sections 4, 5.1 to 5.5, 5.7 to 5.10, 8; 03 phases 0 to 2, section 5 (tests), section 6 (dependencies) | B1, B2, B3, C1, C2, A7; C-6, C-10, C-17, C-19, C-21, C-22, C-23, C-26, C-30 |
| R3 security and integration | 02 sections 6 (all), 7.1 to 7.3, 9 (decisions), 10 (risks) | A1, A4, A5, B2; C-3, C-7, C-9, C-13, C-14, C-24, C-25, C-27 |
| R4 consistency and coverage | 03 whole against 02 whole; both against C-1 to C-30 one by one; 03 section 8 (the question table) against CLARIFICATIONS | both documents, CLARIFICATIONS, `00_kam-brief_verbatim_2026-11-18.txt` |

## The questions each lane answers
1. UNSUPPORTED: which claims in your sections are stated as fact and are supported by no report line and no library line? Quote the claim, say where you looked.
2. CONTRADICTED: which claims disagree with a report, the library, or a C-entry? Quote both sides with their lines.
3. GAPS AGAINST FULL PARITY (C-16, "Full match of everything"): what does the existing Workpath suite do (by the A reports and the library) that the architecture or the plan does not carry? R1 owns this; every lane reports what it meets.
4. GAPS AGAINST THE BRIEF (C-1): deployment methodologies, integration into Entra environments, integration with existing Workpath for mixed fleets, the componentry, OXPd 2 and OXPd 1.x: is each answered specifically enough to build from, or only named? R4 owns this.
5. FEASIBILITY: which design steps rest on a platform capability that the cited guide or contract does not actually grant (R2), or on a security property the mechanism does not actually give (R3)? Say what a phase-0 spike must measure to settle each.
6. INTERNAL: where do 02 and 03 disagree with each other or with themselves (a phase that builds what the architecture forbids, an exit criterion nothing measures, a dependency in the wrong order)? R4 owns this.
7. THE THREE OPEN READINGS (handover section 3 item 2: Q1 covers HP's position only; Q7 an optional stored device-admin copy, off by default; Q15 everything Workpath does, no more): does any design step in your sections DEPEND on one of them? Name the step. Do not resolve the reading: it is the product owner's.

## Rules of the review
- READ-ONLY. You write exactly ONE file: `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-18_datasec-oxpd/review/R<n>_<lane>.md` (create the `review` folder if absent). You edit neither document, no report, nothing under `/Volumes/DEV-Working` (it is another seat's backup: never write, move or delete there), nothing in any project folder.
- No network call of any kind, no message to any human or to HP, no `az`, no `gh`, no git write. No build, no scaffold, no install.
- SECRETS (C-3): the library holds old key material. Never print, copy or quote a secret VALUE (a key, a client secret, a password, a card key, a keystore content) into your file or your reply: give the LOCATION (path and line) only. If a tool output shows one, do not repeat it and say in your report that it happened.
- Every finding carries its instruments: the document line, and the report line and/or library line you opened. Before you write that something is ABSENT (from a report, the library or a document), run a search that would find it if it were there and show a positive control from the same corpus (`/usr/bin/grep -r -i -c` on a distinctive token, never through `cut` or `head`); otherwise write "not found by <the search>", never "does not exist".
- Do not grade plausibility. "Probably right" is not a verdict: either you traced it (CONFIRMED, with the line) or you did not (UNSUPPORTED).
- Count your denominator: how many load-bearing claims you checked in your sections, how many CONFIRMED, UNSUPPORTED, CONTRADICTED. A list of findings with no denominator cannot be weighed.
- PRIOR-WORK CHECK (Datasec standing rule): before you file a finding, read the change log of the document (02 section 11, 03 section 9) and its decisions and risks: a point the document already records as an open risk or a decision with its reason is cited as such, not re-found.
- If you run out of room: stop at a section boundary and say exactly which sections you did NOT read. A partial review that says so is useful; one that implies it was whole is not.
- No `cd` in shell commands; absolute quoted paths (`!` and spaces occur in paths).

## The file you write
```
# R<n> <lane>: Fable review of the OXPd architecture and plan (B1753)
## BLUF (five lines at most: is this part buildable as written; the worst three findings)
## Denominator (claims checked / confirmed / unsupported / contradicted; sections read whole; sections NOT read)
## Findings
| id | severity (Blocker = the design cannot work as written or breaks a C-entry; Major = a phase would be built wrong or a requirement is missing; Minor = wording, an unsupported detail nothing rests on) | where (document, section, line) | the claim, quoted | what the source says (report path:line and/or library path:line, quoted briefly) | verdict (UNSUPPORTED / CONTRADICTED / GAP / INFEASIBLE-AS-WRITTEN / INTERNAL) | the correction you propose, as text ready to apply, or the spike that settles it |
## Parity or brief gaps (lanes R1 and R4: a table of Workpath behaviour or brief item -> where the documents carry it, or MISSING)
## Steps that depend on an open reading (Q1, Q7, Q15)
## Confirmed load-bearing claims (the ten most important you traced, with their lines: the review's positive controls)
## FOUND / TESTED / HOW (what you tested, what you did NOT, the commands, any instrument error)
```
Your reply to Tuesday is the BLUF, the denominator line and the path of your file. Tuesday reads the file, checks a sample of your findings at source, and applies corrections as new change-log entries: your proposed text is a proposal, not an edit.
