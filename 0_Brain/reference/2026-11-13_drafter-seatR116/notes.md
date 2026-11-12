# Notes for Wednesday, Seat R 116th brief (drafter, 2026-11-13 06:1x to 06:3x AEDT)

Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatR116_raise.md` (STAMP block blank). All five rows KEPT; none dropped.

## Rule or check BEFORE stamping

1. **READ BY YOU BEFORE STAMPING: KS-1197 and KS-1776 are UNREAD BY WEDNESDAY.** The only daily-note lines are 10-28 lines 162 and 165 (Spark operator held them as HOLD-WITH-DECISION: "KS-1776 + KS-1197 drafter's fix shapes"); the 10-28 raise ruling (line 191) names letters (PR A..Q), not these keys, and the one "read every" line in the 10-28 note is that ruling. No "read every +/- line" line names either. Positive control: the phrase search returned 1 hit in 10-28 and 2 in 11-11, so the search works. The shape decisions (below) are open.
2. KS-1105, KS-1913: READ EVERY +/- LINE found: `daily/2026-11-11.md` line 56 (15:12, o136: "3 PASS held: KS-1904 p4, KS-1913, KS-1105 ... Wednesday READ every +/- line at source: ACCEPTED") and R 95th ADDENDUM 2 (15:11, "READ every +/- line of the three READYs at source", tier 2, rows 24 and 25). KS-1912: daily line 58 (15:43, o137: "3 PASS (KS-1904 p5, KS-1912 refusal half, KS-1868 anchors) read at source, ACCEPTED") and R 95th ADDENDUM 3 rows 26 to 28. **That wording is "read at source", NOT "read every +/- line"**: treat KS-1912 as READ AT SOURCE, not verified line-by-line; read it (api.ts return-type change) if you want the exact phrase. There is no pickup file for 11-11 in daily/ (none found by name).
3. **Rule KS-1197's shape.** Patch coerces a non-string level to 'none' inside the gateway (`enforcement.ts`); the ticket's own recommendation was to validate at principal build (`middleware/auth.ts`) and to make the verify handler's rejection reach the error handler. The 10-12 ticket comment says an ISSUER_ADMIN can mint `verificationLevel: "__proto__"` through `routes/users.ts` 622-647 and `userRepo.ts mapDbVerificationLevel`: the upstream cause is untouched. Options: (a) raise as a partial defence, Refs only (what the brief says; row 54 last); (b) drop to the board for a shape ruling. Also unmeasured: whether `meetsVerificationLevel` is called by `routes/verification.ts` 556-557 (the hang half).
4. **Rule KS-1776's shape** (ticket says "No fix is proposed"; patch is the drafter's try/catch around the timer). It is the likely cure of the whole-suite exit-1 flake named in PR 2216's body (gate 321 Q5: 3 of 4 pristine runs). Fine to raise; brief asks the seat to run the suite a stated number of times before and after and claim only counts.
5. **Tiers (my lean, yours to rule; definition used: learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md tier 1 = security surfaces: auth doors, tokens, MFA, session minting; data destruction; deploys; handovers):**
   - KS-1105 Login.tsx: a login PAGE but a 1-line placeholder string; **tier 2** (your own R 95th ruling, "gate reads it carefully"). Tier-1 surface? Only by the rendered-auth-door reading.
   - KS-1913, KS-1912: admin frontend styles and error display: tier 2.
   - KS-1197 enforcement.ts: an AUTHORISATION decision on document creation and verify (level ranking, fail-closed), api-gateway: **I lean tier 1** (its gate Opus). Not a token or a door, so it is arguable.
   - KS-1776 auth.ts: file is the auth service's routes module (`services/auth/src/routes/auth.ts`, which holds login routes), but the change is error handling around a seeding timer; precedent: you ruled the seeder log-meta row (KS-2174 part 2, userRepo seeder) **tier 2**. **I lean tier 2** but it is the file a tier-1 reflex would catch; rule it. If 1197 is tier 1 and 1776 tier 2 they go in separate READYs (tier-1 never mixed with tier 2).
   The brief's QUEUE says "per STAMP" for 53/54/55 where unsure; fill the stamp items.
6. **Fetch:** the brief needs a fresh YES for the URL-form develop fetch into `worktrees/s-r90-base` (410feda is not in any local store; the shared checkout `cat-file` is fatal). The drafter fetched by SHA into the scratch clone only, through the project's own repo-local `core.sshCommand` (read, never printed).
7. **Pace:** five rows, five ~14 min pushes. My arithmetic (extrapolated from R 115th: plan 32.9 to wrap about 53 for a hand-built row with a new gate) is a guess; I wrote 4 to 7 points per held row. Expect 4 rows, 54 left over. Rule whether the seat is told to take 54 last or to skip it unless the shape is ruled.
8. **Kit/ordinals:** R 115th's HANDOVER NEXT ROWS (KS-2173 part 2, fix round, email.ts) are superseded by this brief; the brief says so. R 115th's PR 2219 shows MERGED (from the merged list); I did NOT read a gate verdict for it.
9. **Docs-fragments / NO-PAIR:** unmeasured whether the repo check wants a fragment pair for these held-patch rows (R 95th's addendum was silent). The brief tells the seat to measure and say.

## Established facts (instrument, time)

- develop = `410feda1a85e54b82a65464607f4761c2da3bb1b`: `git ls-remote origin refs/heads/develop` 06:11:44 AEDT; equals the commission pin.
- **Applies-check, scratch clone** `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatR116/scratch_clone` (git init, `fetch --filter=blob:none --depth=1 origin <sha>`, product files checked out from FETCH_HEAD; `git apply --check -v` of each canonical `patch.diff` from `local-model/runs/*/out.md.checker/`). Every patch inspected is the one each READY file names as CANONICAL:
  - KS-1105: PASS rc 0 (Login.tsx + new ks1105 test). No offset.
  - KS-1913: PASS rc 0 (PlatformAuditLog.tsx + new ks1913 test). No offset.
  - KS-1912: PASS rc 0 (ClientList.tsx, api.ts + new ks1912 test). No offset.
  - KS-1197: PASS rc 0; enforcement.ts hunk #2 "succeeded at 153 (offset 1 line)".
  - KS-1776: PASS rc 0; auth.ts hunk #1 "succeeded at 62 (offset 3 lines)".
  - Negative control: a planted wrong-context hunk on Login.tsx: "error: patch failed ... patch does not apply". The five new test files do not exist at 410feda (`ls-tree` count 0 each; `git apply --check` of a new-file diff would otherwise fail).
  - Offsets mean a "strict, zero-offset" builder would FALSE-FAIL rows 54 and 55; the brief says to accept a pure offset of 1 and 3 and verify `+` bytes.
- READY headers quoted (date, tip, targets): KS-1105 held 15:08 2026-11-11 tip 4a91ff3e1c56, Login.tsx + ks1105 test (numstat 1/1, 39/0); KS-1913 held 14:59 2026-11-11 tip 4a91ff3e1c56, PlatformAuditLog.tsx + ks1913 test (3/0, 56/0); KS-1912 held 15:24 2026-11-11 tip 249be7c8cd14, ClientList.tsx (11/2) + api.ts (5/4) + ks1912 test (79/0); KS-1197 held 13:50 2026-10-28 tip 1d07ce26ae2f, enforcement.ts (3/2) + ks1197 test (102/0), byte-identical to the drafter's golden per its header; KS-1776 held 13:50 2026-10-28 tip 8894c7486f82, auth.ts (10/3) + ks1776 test (102/0), also byte-identical to golden. All five checker A2 "PASS diff applies at the tip", A3 file-set equal; those were at the tips named, NOT at 410feda (my check is the first at 410feda).
- Board (Linear read-only, 06:1x, own script, key read from the project .env inside python, never printed): all five Backlog; assignee `kamil.kreiser@secuura.ai` (Kam's Secuura account; not Peter, not Stuart); no attachments; KS-1197 has 2 comments, KS-1776 1.
- PRs: `gh pr list --state open --limit 500` 92 open (control 2079 present); no open PR title/branch/body carries any of the five keys (whole-word regex); no open PR touches any of the six product files; no open PR path contains the ks keys. Merged (1000 back to 2026-09-20): no title/branch carries them (control KS-2174 hits 2216 and 2219). The gh `--search "KS-n in:title,body"` returned fuzzy hits (2089, 2130 etc.) that the literal regex did not confirm: noise, not evidence.
- Caller check at 410feda (`git grep` over frontend/admin/src): `updateTenantStatus` and `deleteTenant` are called only in ClientList.tsx (81, 87); `describeFailure` is already imported at api.ts:15 from `lib/settingsSavePayload.ts`.
- Floor 06:16: only %0 and %1; load 2.94; 2.2 TiB free; push lock absent; history guard R 115th = 1, R 116th = 0.

## Could not establish (and what closes it)

- Whether the local frontend/admin harness runs on this drive (build_deps.sh state): the seat's set-up proves it.
- Whether `frontend/admin/package.json` has gained a test runner since 11-11: the seat re-reads.
- Whether `meetsVerificationLevel` is the verify-handler call at `verification.ts` 556-557: the seat reads it.
- Gate verdict for PR 2219 and any ADDENDUM on `(Seat R 115th)`: mail only, not read.
- R 95th ADDENDUM rows 23 to 28 (these same rows) were apparently never raised (no KS-1105/1913/1912 in R 95th to R 98th HANDOVERs, no PR): why is not measured (R 95th wrapped with "four rows committed not pushed" per daily 11-11 line 58; whether those trees still exist is unmeasured and no seat should assume them).
- The tier-1 definition is my reading of the 2026-09-05 lesson file, not a table of surfaces.
- Pace figure above is an extrapolation.

## Fences kept
Wrote only the brief, this file and `scratch_clone/` plus two scratch files in the session scratchpad (lin.py, open.json, merged.json, neg.diff). No push, PR, comment, mail, Linear write; git write verbs only in the scratch clone; the one network read beyond gh/Linear was the `fetch` into the scratch clone using the source repo's own deploy-key ssh command (read config only).
