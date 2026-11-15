# Drafter notes, Seat W (KS-1882 wallet sessions), 2026-11-16 01:1x AEDT

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatW1_ks1882_wallet_sessions.md

## Findings that change the commission
- Ordinal: the commission expected W 1st = 0. MEASURED 1 (a 2026-10-27 entry); W entries run 1st to 30th, so the brief names the seat W 31st (file name kept as commissioned). Wednesday's STAMP decides.
- POST /api/wallets/sign HAS the same gap (read from code: memory lookup by id, no caller read, no DB fallback). It is the third and last id-taking route; GET, DELETE, sign are the whole family. No other route takes a session or wallet id.
- DELETE runs its table UPDATE before checking existence: a refused caller could still flip a database-only session off. The fix puts the check before any write (closes KS-2042 item 1 as a side effect).
- The session records no owner and `svc_wallet_sessions` is defined twice (migration 002 vs the gateway's startup-migrations), so a persisted owner column is a Kam migration. Brief builds owner-in-process (separate Map, so no response prints it) and fails closed for a session with no known owner; this is W2.
- Existing cell changed by design: ks1360's authenticate stand-in sets no user, so under D3 its POST would 401.
- Open PRs: 72, wallet-connector touched only by 649 (a pg dependency bump of package.json). No PR fixes this.

## Drafter judgement calls (Wednesday may overrule in the STAMP)
- Platform admin may read and end any session (matches KS-1845 list gate) but not sign.
- 404 bytes, never 403.
- No key-principal special arm.

## Not done
Nothing run; no stack; suite not run; write targets were only the brief and this folder.

UNMEASURED
whether the services/wallet-connector suite is green at develop; replica count; any key principal opening a session; callers outside the Secuura checkouts or built dynamically; the files of PRs 2240 and 2241; the push hook's refusal branches; the live board state of the ks1695 ownerless card.
