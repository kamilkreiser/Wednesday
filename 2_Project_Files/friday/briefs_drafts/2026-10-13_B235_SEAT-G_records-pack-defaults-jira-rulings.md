From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to (your STATUS file is the wrap).
# BRIEF B235 · SEAT-G: HPSM-POC RECORDS: Kam's 12 pack defaults (POC-1…POC-12) as C-99 with their BACKLOG lines, and Friday's Jira rulings P1–P4 + P10 (read first, then write as ruled)
**Fired: 2026-10-13 03:52 AEDT.** Pane `Datasec/HPSM-POC-G`. Your commission is THIS file, at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B235_SEAT-G_records-pack-defaults-jira-rulings.md` (Friday's tree, read-only to you). Step 0: copy it into your `1_Project_Definition/Briefs/` unchanged, as the project's record. **Tier: records + Jira only. No product code, no deploy, no setting, nothing on Azure, no hosted access.** Nothing pushed to any `main`. The last SEAT-G seat, B222, is finished (`Briefs/2026-10-12_B222_STATUS.md` ends `RECORDS DONE (ADD-1): d96b7c3 …`; landed as analysis PR #113 → `bb1e8887`).
**Report:** `1_Project_Definition/Briefs/2026-10-13_B235_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · Records). Last line exactly `RECORDS DONE: records/b235 <sha>, C-99 y, rows <n> lines, Jira <keys> read back` or `STOPPED: NEEDS FRIDAY` and ONE question.

## AUTHORITY
- **Kam's pack:** `FRIDAY/0_Brain/reference/2026-10-12_datasec-decisions-pack/decisions-pack.html` §3 (POC-1…POC-12) + words list (POC-12). Card `hpsmpoc-decisions-pack-1012`, read by the drafter (`decision_queue.sh show`, 03:4x AEDT): `ruling: choice='a' ruled_ts=2026-10-12T20:12:51.308002+11:00`; option a verbatim: *"All defaults for this project"* / *"Accept every bold default POC-1 to POC-12. Workflow changes go through the CodeQL-gated PR route. The Azure resource and the header change go on deploy cards after 13 Oct."* Open the pack read-only; copy text **byte for byte**.
- **Friday's rulings:** `friday-calls-RULED.md` (03:38 AEDT; P-rows ruled AS PROPOSED) + rows P1–P10 of `friday-calls-proposed.md`. Record them as **"Friday's ruling (coordinator), 2026-10-13"**, never as a C-entry. **N4 (UAT login window) is carded to Kam: record nothing for it.**
- **Pack → row/ticket map:** `friday-calls.md` §3 "HPSM-POC" table.

## Records route (the B222 shape; re-read it yourself)
- Records repo = project root, origin `git@github.com:datasecau/HPSM-POC-analysis.git`. `ls-remote origin refs/heads/main` (drafter, 03:42) = **`bb1e8887687c07695dbca4b8dd35ff29d9df2344`** ("Records: B222 catch-up … (#113)"); local `origin/main` = the same. The root checkout's local `main` = `76bb8ba` (stale): **the root is not yours**; plain reads only there.
- `CLARIFICATIONS.md` (`1_Project_Definition/`) at bb1e8887: last `### C-98` at `:1097`. Drafter scanned **every** ref `ls-remote origin` lists (all present locally): max C = **98** on `main`, `records/b222-catchup`, `refs/pull/113/head`; no ref holds C-99+. **Next free = C-99.** Re-scan every origin ref just before your commit; a duplicate is a STOP.
- `BACKLOG.md` at the root, 195 lines at bb1e8887. **"The backlog of record is Jira `HPSMPOC`"** (`:3`).
- Work in `.tools/wt-b235` from a freshly fetched `origin/main`; every ref write under the shared lock (`.tools/b198/lock.sh <cmd>`, copy it to `.tools/b235/` identical). Push ONE branch, `records/b235`, plainly (never force), read back with `ls-remote`. **Friday opens the PR and merges it after CodeQL and the checks.**

## 1. C-99: Kam's pack (one commit)
`### C-99 — Kam accepts every default of the HPSM-POC decisions pack (POC-1 to POC-12) (2026-10-12, 20:12 AEDT)`, in C-87's card-ruling shape: channel (Kam's live decision board, as read by Friday from his register), `ruled_ts` quoted, option label + detail verbatim, "as relayed in Friday's `Briefs/2026-10-13_B235_SEAT-G_records-pack-defaults-jira-rulings.md`". Then one table row per POC-n: question · options · default (verbatim) · "if you pick the default" (verbatim) · row/ticket (map). Then the POC-12 words-list rows verbatim.
**Where built (cite, never claim more than the file shows):** POC-1 → `Briefs/2026-10-13_B234_STATUS.md` last line `READY FOR REVIEW: b234/ci-api-timeout-25 8ece2522f30f87160cf33bca9490abdd4ad3026e`; PR **datasecau/HPSM-POC#148** (GitHub pulls API 03:46: `open`, `mergeable_state` `clean`, base `a5fd6355`). Re-read #148 when you write; say "open, not merged" unless it has merged. Every other POC-n: "not built yet" (POC-2, POC-3 explicitly "after 13 Oct, on a deploy card").
Commit: `Records: C-99, Kam's HPSM-POC decisions pack defaults POC-1…POC-12 (B235)`.

## 2. BACKLOG lines (one commit; append a dated sub-bullet, never edit or delete)
`  - Ruled 2026-10-12 (C-99, POC-n): <default, verbatim>. <"if you pick the default", verbatim>.` on the rows the map names (drafter's lines at bb1e8887; re-find by text): POC-4 → `:40` (braces, HPSMPOC-218) · POC-3 → `:47` (HSTS) · POC-9 → `:63` (console 4xx) · POC-12 → `:96` (row "Hosted "Reset demo" success message misdescribes a live reset"; the quoted sentence is its sub-bullet `:98`) and `:76` (the "It may still finish" row; POC-12's timing sentences are "to be drafted", so it stays open) · POC-6 → `:165` (B220 N-3) · POC-10 → `:168` (B220 N-4) · POC-11 → `:181` (B220 S-N2). Tick `[x]` only POC-10 and POC-11 (their defaults are "accept" / "no change; record it" and need no build). Friday's P5 (`:105`, hash CHECK migration): append `Friday's ruling 2026-10-13 (P5): hold; fold into the first HPSM round that needs a migration anyway.` Do not tick it.
Commit: `Records: pack rulings (C-99) and P5 on BACKLOG rows (B235)`.

## 3. Jira (read first; write only if the ruling still applies; quote every read)
Credentials by name only (`4_Credentials/.env`: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`; project `HPSMPOC`, `JIRA.md`). B222's helper method (`B222_STATUS.md:65`), fresh copy in `.tools/b235/`. Never print, log or write the token.
Per key: (1) `GET …/issue/<key>?fields=status,summary,comment` + `GET …/transitions`; quote status + newest comment id. Drafter: **every Jira state below is UNMEASURED**. (2) Already Done / already carries the text → SKIP, say so. (3) Write the line verbatim (one ADF paragraph, no person named). (4) Read back by id, byte-equal; a comparator control that fires.
| Row | Key | Comment (verbatim) | Transition |
|---|---|---|---|
| P1 | HPSMPOC-154 | `Friday's ruling 2026-10-13: (a) close. The laptop showcase is single-user; ShowcaseStartup.cs (last commit ca554a6, B14) stays as it is.` | Done |
| P2 | HPSMPOC-245 | `Friday's ruling 2026-10-13 on gate B189's notes: N-1 and N-2 accepted (durations only). N-4, N-5 and N-6 go into the next BFF lane (web/src/server/bff.ts); its blocker, PR #147 (B231), merged as main b7dbaf9f on 2026-10-12.` | none |
| P3 | HPSMPOC-246 | `Friday's ruling 2026-10-13 on gate B193's notes: N-2 accepted (< 0.02 % of the floor). N-4 is recorded by the next HPSM deploy seat. N-5 to N-7 go to a timing lane after 13 Oct.` | none |
| P4 | HPSMPOC-248, HPSMPOC-249 | `Done by PR #144 (caa5a971, B224; gate B227 GO WITH NOTES). Transitioned by Friday's ruling 2026-10-13.` | Done (each) |
| P10 | HPSMPOC-232 | `Friday's ruling 2026-10-13: this ruling's window ("nothing changes before 13 Oct") is spent as of 13 Oct. Not reopened. HPSMPOC-92, -96, -117 and -234 stay parked.` | none |
| POC-4 | HPSMPOC-218 | `Kam's decisions pack 2026-10-12, POC-4, default (a): renew the braces exception to 30 Nov (C-99). Dependabot alert #1 read 2026-10-13: state open, first_patched_version null, vulnerable <= 3.0.3; not dismissed.` | none |
| POC-8 | HPSMPOC-226 | `Kam's decisions pack 2026-10-12, POC-8, default (a): confirm both as built (C-99): the Jira automation rule ignores the two extra fields; the privacy export lists attachment details, not the files.` | none |
Before P4, confirm from `2_Project_Files` (read verbs only): `git cat-file -t caa5a971` and `git merge-base --is-ancestor caa5a971 origin/main` (after a fetch); if either fails, comment without the SHA and do not transition; say so. Before POC-4, re-read the alert (`friday_as.sh` is Friday's; use `gh api repos/datasecau/HPSM-POC/dependabot/alerts/1` only if your launcher's `gh` is signed in as the Datasec identity, else copy the drafter's read above and say so). No ticket is created. No other Jira write.

## 4. Push and read back
`records/b235` pushed plainly under the lock; `ls-remote origin refs/heads/records/b235` = your head. Assert on your head: C-99 present once; C count = bb1e8887's + 1; the 8 BACKLOG lines present; nothing else changed (`git diff --stat bb1e8887..records/b235` = `CLARIFICATIONS.md`, `BACKLOG.md`, your STATUS, this brief only).

## HOLDS
- **HP Restricted material.** No HP Restricted document is given to ANY AI tool without HP's written approval (signed SOW §4.1.4(c)). Do not open `HP Reporting and Docs/` or the SOW file in the project root.
- **Datasec only.** No other client's names, tickets or paths.
- No product code; `2_Project_Files`: `fetch` + read verbs only. No PR, no merge, no deploy, no history.md (Friday's), never open `4_Credentials/.env` except through the helper that reads the three Jira names, never delete, never force-push, never dismiss an alert. No ports: bind nothing.
- Build seat B236 (`Datasec/HPSM-POC-D`) runs beside you in `2_Project_Files`; you touch nothing there.
- If a measurement contradicts this brief, the measurement wins; say so, and STOP if it changes what you would write.
