# B564 DRAFTER REPORT (2026-10-24, Sonnet drafter, read-only)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B564_SEAT-H9_hpsmpoc-snapshot-customer-name-drop.md` (92 lines, long ones; unstamped copy reads **9** lines with `/usr/bin/grep -c -E '_''_''_''_'`, matching the Stamp text: 8 slot lines + the last line). Template: B558 brief and drafter report, read whole.

## What I read
- Base: `git --no-optional-locks ls-remote origin refs/heads/main` -> `08af828bd0eff92c82169e240fb4d6d9f5dc2fe7`; `gh api -X GET .../git/ref/heads/main` agrees; commit subject "Test-only follow-ups ... (#204)". The local clone does NOT hold that object (`cat-file -t` fatal; local main/origin-main are older), and I may not fetch, so every source below was read with `gh api -X GET repos/datasecau/HPSM-POC/contents/<path>?ref=<sha>` raw (GET, read-only; not a hosted-site call). Blob shas read: `SnapshotLauncher.tsx` `2739b428...`, `edge-trim.ts` `5ffd4c15...`.
- Findings: `Briefs/2026-10-23_B526_STATUS.md:162` (B526-f1), `2026-10-23_B549_STATUS.md:192` (B549-5), `2026-10-24_B557_STATUS.md:241,414` (the records seat's rows). Both quoted in the brief.
- Source at main: `SnapshotLauncher.tsx` (whole), `CustomerManagement.tsx` (`:100-125`, greps), `profile-values.ts`, `CustomerName.tsx`, `edge-trim.ts`, `client.ts` (`:100-125`, greps), `customer/api.ts` `createCustomer`, `CustomerManagement.edgeTrim.test.tsx` and `customer-name.test.ts` (heads), test-file names for the launcher.
- Cards (`decision_queue.sh show <exact id>`): `hpsmpoc-refuse-more-invisible-characters` (ruled `a`, 2026-10-01 09:17), `hpsmpoc-class-c-wording-six-tickets-1022` (ruled `a`, 2026-10-22 16:42). `hpsmpoc-edge-characters-refused` (named in the B526/B549 files 19 times) is NOT in the queue (`show` -> "no decision with id"): the brief says so and points to `edge-trim.ts:1-6`. No `list` was used.

## Code behaviour found
- **Primary path (Customers page):** `trimEdge(name)` at `CustomerManagement.tsx:107` and again `trimEdge(input.name)` in `customer/api.ts`; `maxLength` 120; a 400 shows the API's own sentence (#203). The five characters trim() would strip (U+000B, U+000C, U+FEFF, U+2028, U+2029) are kept at the edge, reach the API, and are refused in its words. A name of only those is not "blank".
- **Second path (`SnapshotLauncher.tsx:108`):** `newName.trim()` then `api.createCustomer(name)` (`client.ts:109`, no trim). So an edge hidden character is silently removed and the name created; a name of only those reads as blank. Over-long: same `maxLength` 120 (`:168`) as the primary. Interior special characters: sent as typed in both. Error display: same `describeFailure` in both. Only the edge handling differs, so no new word is needed.
- B549-5 itself is a class note on OTHER free-text fields (`override.ts`, `session.ts`, `profile-values.ts:45`, `customer/api.ts` industry); the one with a real drop and a customer name is B526-f1 (SnapshotLauncher). I scoped the brief to the SnapshotLauncher path and put the sibling list under NOT IN THIS ROUND / FOR TUESDAY.

## Decisions and why
1. **Fix is `trimEdge` in the launcher, not a trim in `client.ts`.** B526-f1 names it ("Same fix: `trimEdge`"); `client.ts` is a shared file, so changing it widens the blast radius. Paths: 2 (`SnapshotLauncher.tsx`, new `SnapshotLauncher.edgeTrim.test.tsx`). Unlike B558 this is not test-only: one product import plus one changed line, with a program check that no string literal is added.
2. **Rows copy the Customers-page twin** (real mock API in-process, body read on the way) plus a parity row so the two paths cannot drift. Controls (rows green at main) are named. Mutants S1-S5 on the launcher, E1-E6 on a scratch copy of `edge-trim.ts` (read-only to the seat).
3. **Rulings conformed to:** refuse the five, keep joiners/NBSP/soft hyphen (row 6), no new words (STOP + WORDS-DRAFT otherwise).
4. **Gate tier 2 (Sonnet):** client-side trim of a name box; no auth, session, permission, deploy or destroying surface; the API still validates. Tuesday confirms at the stamp.
5. **No Api row**, so the SQL Server rule is not engaged; the standing line is kept verbatim as asked.
6. All six standing lines you listed are in the brief verbatim or near-verbatim (HP-tools line is verbatim; seat-local NuGet/npm/heavy-lock line is STANDING LINE 9; push-only line is in STANDING LINE 2).

## Port check
Block **9120-9129**. How: `grep -ohE` over all `2026-10-2[34]*.md` briefs for port ranges 89xx-9xxx: the highest named are 9110-9119 (7 hits) and 8960-9099; `grep -c -E '\b912[0-9]\b'` over every brief in `tuesday/briefs/*.md` = 0 and over HPSM-POC's `Briefs/*.md` = 0 (control: `\b9110\b` counts 5); `lsof -nP -iTCP:9120-9129 -sTCP:LISTEN` printed nothing (rc 1). Not checked: panes started after this read.

## Dependency on B563 (records seat)
The branch is `b564/hpsmpoc-<key-number>-snapshot-name` and the brief has a `TICKET-KEY:` stamp slot. **Do not launch until B563 has created the Jira ticket and you have its key** (the REFUSE check treats an unfilled TICKET-KEY as unstamped). The seat also reads that ticket whole at PRIOR WORK. The key is allowed in the branch name and STATUS only, never in code, tests or the commit message.

## UNMEASURED
No npm, vitest, mutant run; no Jira read (ticket text, HPSMPOC-323); that the new rows go red at main (reasoned from source); the `useSearchParams` mocking the launcher test needs (the `b56` test file not read); `CLARIFICATIONS` and `git log -S`/blame (base objects absent locally; the seat does them); intersection program over `b5*`/`b6*` branches; baseline suite counts at `08af828b`; whether the mock refuses an interior hidden character with the identical sentence (`customer-name.test.ts` header says yes; not run); whether any pane has started since I checked ports.

## Reviewer: check first
1. The "silent drop" reading: `trim()` strips U+FEFF/2028/2029/000B/000C (edge-trim.ts header says so) and `client.ts:109` does not re-trim, so SnapshotLauncher.tsx:108 loses them. This is from source only; the seat's census-by-run confirms.
2. That `SnapshotLauncher.tsx` has no other `trim()` on this path and that "Enter a name for the sample customer" staying for blank-only (row 4) is what you want (it differs from the Customers page's "Enter the customer's name"; the brief keeps existing words per the no-new-words rule and does not unify them).
3. Whether to widen to B549-5's sibling fields (the brief says no; they sit in FOR TUESDAY).
4. Row 6 / E6 wording (joiner at the edge) and the stamped branch name once the key exists.

## Files written
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B564_SEAT-H9_hpsmpoc-snapshot-customer-name-drop.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B564_DRAFTER-REPORT.md`
Also wrote scratch copies of source files under the session scratchpad only. No Jira, mail, chat, publish, fetch, worktree or hosted-site HTTP was used (GitHub `gh api -X GET` reads only). Two small Edit calls were made on my own brief file after Write (launch path, one mutant sentence).
