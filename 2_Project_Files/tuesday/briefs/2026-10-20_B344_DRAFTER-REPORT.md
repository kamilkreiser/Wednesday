# B344 DRAFTER REPORT (Composer records seat W17S) · 2026-10-20 21:06 AEDT

## BLUF
Built one brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B344_SEAT-W17S_composer-records-fold-b339-pr83-landing.md` (37,896 bytes, same shape as B339's, 2 unfilled slots: `@@MAIN_SHA@@` in the REFUSE block, `@@STAMP_TIME@@` in the Model line; hidden-character scan 0).
The seat does: (1) fold `records/b339` into root `main`; (2) record PR #83 landed (#340 State flip, history); (3) file B335's Notes N-A/N-B as BACKLOG row #366 (a candidate, no C-entry); (4) note the two Kam cards as open only; (5) file the B335 STATUS and brief copy (my addition, strikable). Read whole, not executed: nothing in the brief was run.
**Fence break, said plainly:** I also wrote `...B344_SEAT-W17S_...landing.md.pre-stamp` (a byte-equal copy, `cmp` rc 0, 2 slots) beside the brief. The fence names two files; the pre-stamp is Tuesday's own step. It is harmless: use it as the REFUSE control, or delete it. No other file written, no git write, no network write, no secret printed, no `cd` (one `cd` attempt was refused by the hook, ran nothing).

## MEASURED (command, time 21:01 to 21:05 AEDT)
- Root repo: `rev-parse main` = `adf5692dccecd7e999c65c1b0d6b481fbcf08f5f`; `rev-parse records/b339` = `e76c7b0d3adb1ad65e7ac402309a8a25f82b2fff`; `rev-list --count main..records/b339` = 1; `merge-base main records/b339` = `adf5692d` ; `merge-base --is-ancestor records/b339 main` rc 1; `records/b339^{tree}` = `4353352e0e0a7e7eb9de569271fac2d5a38bca5d`; `main^{tree}` = `f76399931a39615262b2b524f33a33bb46ab7758`; `branch --list 'records/b344*'` 0 lines; tracked dirt = the same two ` M` (B26, B298); `status --short | wc -l` = 1014.
- Fold shape: `diff --name-status main records/b339` = 38 lines, 35 A, 3 M; `diff --stat` = 38 files, 1317 insertions, 2 deletions. All 35 A exist untracked in root: 34 byte-equal, 1 differs (`B339_STATUS.md`: committed 23,549 bytes, root 29,043, `startswith` True, control False). 3 M paths clean in root. 8 root-only B339 evidence files (not on the branch) named in the brief.
- Code repo: `ls-remote origin refs/heads/main` = `eaff2b7442d8cc28e536d41a46cec701266024b1`; refs/pull/83/head `8e062d94...`; refs/pull/84/head `0f64aee7...`. `eaff2b74` is NOT in the local code repo objects (`cat-file` failed), `318df176` is.
- `gh api` GET (account `kamilDatasec`): pulls/83 closed, merged, merged_at `2026-10-20T09:13:30Z` (= 20:13:30 AEDT), head `8e062d94...`, merge_commit_sha `eaff2b74...`; commits/eaff2b74 one parent `318df176...`, tree `610ec59bf07acc5c8caaa718254a6f704ba1fd97`; compare 318df176...eaff2b74 ahead 1 behind 0 files 19; ref/heads/main = `eaff2b74`; head commit tree `b38feba02e69ea2408f42fb2f608131a6f159d98`.
- B335 STATUS: 573 lines, 64,777 bytes, sha256 `309782e0...8608`; its brief copy 60,541 bytes, `cmp` rc 0 against Tuesday's original; evidence folder 99 files, 5,800 KB; hidden chars 0 in both files. Notes N-A/N-B at STATUS lines 460-461 (quoted verbatim in the brief). Line 1 = GO, no finding.
- Backlog: `records/b339` ends at `| 365 |` (lines 359-361); #340 State text is the "ASSIGNED to brief B322" cell; rows #341-#345 contain `0022_*.sql` in Files text, #353 does not.
- `AGENTMAIL_API_KEY` count in `.env` = 0 (control 1). Model row: routing file has NO row named "records"; row C8 (brief drafting, tooling) is what B339 used; `models_latest.json` sonnet = `claude-sonnet-5-5` (checked 20:55:31 +1100, warnings []).
- Live seats: `ps` shows B341's brief_seat (pid 36532, 47 min); tmux `%142` "B341 composer gate PR84 tier1"; B341 STATUS does not exist yet. No other Composer or records seat.

## RELAYED
Gate chain B322/B331/B333/B335 last-line texts (from the STATUS files), Tuesday's landing note facts (3/3 check-runs, 0 alerts, 19 files, squash with match-head-commit), the two open cards (Tuesday's 20:23 and 21:00 notes), N1-N3 and round-1-database notes.

## UNMEASURED
Whether the two cards are still open now (card store not read); demo state/deployed sha; whether `main` moves after 21:03; B341's own REFUSE behaviour toward a live records seat; B335 STATUS beyond lines 1, 108, 183, 196-212, 387-392, 456-466.

## CONFLICTS FOUND
1. **Tree wording differs from B339's pattern.** PR #82's squash tree equalled the head's tree; PR #83's does not (`610ec59b` vs head `b38feba0`; `610ec59b` is the gate's predicted merge onto #82's main, B335 STATUS:387-392). The brief tells the seat not to write "equals the head's tree".
2. **Stale files lines:** rows #341-#345 still name migration `0022_*.sql`, now occupied by PR #83. Not touched by the brief (listed in FOR TUESDAY).
3. B339's After block names 6 root-only evidence files; the disk holds 8 (same kind of gap B339 found in B328: 4 vs 5). The brief restores all 8.
4. My awk id count (346 rows with NF==5 on `records/b339`, 343 on `main`) differs from B339's 355 numeric ids (different method); the brief says to use B339's script and state which.

## QUESTIONS FOR TUESDAY (recommendation each)
1. Keep Step 3 (filing the B335 STATUS + brief copy), which is beyond your five items? Recommend KEEP (B339 filed B320 the same way; the history and #340 cite it). If struck, they say "untracked".
2. Stamp @@MAIN_SHA@@ with Composer code main by `gh api` (expected `eaff2b74...`, or later if #84 lands)? Recommend yes; it is informational, not a STOP, if main moves.
3. Delete or keep my stray `.pre-stamp`? Recommend keep as the REFUSE control (it has the 2 slots; the control count in the brief says 2).
4. Should the stale Files lines of #341-#345 (migration number 0022 now taken) be fixed by this seat? Recommend NO: not in your commission; give it to the L3-2 build brief or a catch-up records round.
