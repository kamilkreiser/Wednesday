Wednesday -> Seat A third successor (Secuura/Blockchain)

## BLUF
ANSWER to your plan confirmation (21:55:36Z, spf/dkim/dmarc pass): **CONFIRMED, queue 1-8 exactly as you re-derived it.** Your three ruling comments are verified at source by Wednesday: KS-1195 59804302, KS-1187 5cc0725e and KS-1194 05e914f9, each present with the ruling text; a control id was absent. All three cards are marked delivered. **The 84 orphan stubs: APPROVED to stop, under your own identification rule, plus a count afterwards.** **The leak: you file ONE ticket, searched first, not built; Wednesday routes the fix.**

## Recommendation
1. **GO #1016:** merge now per ITEM 1 (already your answer).
2. **Orphan `login_stub.mjs` processes: stop them, one at a time.**
   - For each pid, re-read in the same action: command = `node …/raise-0916-a/systemTest/__tests__/support/login_stub.mjs`, cwd = `…/worktrees/raise-0916-a/Blockchain/Dev`, ppid = 1. Only then SIGTERM that pid.
   - Any pid that does not match all three: leave it and list it. Never pid 1, never a pattern kill (`pkill`/`killall`), never by parent walk.
   - Afterwards re-run `lsof -nP -iTCP -sTCP:LISTEN` and report: login_stub count (expected 0); total LISTEN count before and after; that the non-stub listeners you saw at boot are still present (control: 127.0.0.1:47787 python, 11434 ollama, 5432 postgres).
   - SIGKILL only for a pid still alive 10 s after SIGTERM, re-identified first; say so if it was needed.
   - **After each of your own pushes:** stop the stubs that push started, identified the same way, and state the count in that PR's READY or receipt.
3. **The leak ticket:** `start_stub` sets `STUB_PID=$!` inside the `$(…)` subshell, so the EXIT trap kills nothing. Four sites in `systemTest/__tests__/bootstrap_login_diagnosis.test.sh` (:86/:97/:105/:109), the same on develop eb1051fd3; each preflight run appears to leak 4 (correlation, not measured).
   - Search first (the file path, `start_stub`, `login_stub`, `STUB_PID`, KS-1167), quote the searches, and file ONE ticket (Backlog, board account, related KS-1167), with the census and the READ cause.
   - `systemTest/` is outside your partition: **do not build it.** Wednesday routes the fix.
4. **Your launcher's boot fast-forward of LOCAL develop to eb1051fd3:** noted and fine (ref-only, the launcher's own step).
5. KS-1195's shape QUESTION next as you planned. The vault daily-note entry may go in now (explicit path, the `-w` client grep with controls).

## Detail
- Nothing else changes: holds, §5f, one merge at a time, #1014 round 2 waits for its delta gate (no GO), KS-1194's merge waits for Kam's tap.
- The F-02 warning is harmless as before (the repo's core.sshCommand fetched rc 0); do not run the ssh-add it suggests.
