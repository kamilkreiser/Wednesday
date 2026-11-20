PR 2266: GO WITH NOTES (at head bd7f05bf01ae944ec106876343c998a07c182b1f; tier 1)

# Gate 389, tier 1 (Opus), PR 2266 (KS-2272), 2026-11-20 ~12:14-12:35 AEDT

## Pins
- **gh, twice** (12:14:01 before the first measurement, 12:30:06 before this file), same values both times:
  - PR 2266 OPEN, not draft, head bd7f05bf01ae, base 35d677937401, 1 commit, 11 files, +695 -62, updatedAt 2026-11-20T01:11:34Z;
  - develop = 35d67793740137b5014a516731ab6391af9f4b89;
  - PR 2099 head = 8967de8b17558890dc4ace2732cb8350768df601.
- **Merged state = the head.** The head's only parent is 35d677937401 = develop tip, so a merge is a fast-forward. Every "merged" figure below was measured on the head.
- **Closing keywords:** 0 in the commit, 0 in the PR body (`/usr/bin/grep -i -E`); controls: "KS-2272" appears 2 times in each.
- **PR body at source** (14,750 bytes, sha256 73cf81c9be72…) is byte-identical to the builder's drafts/pr_body.md.

## How I measured
- **Clone:** `_work/g`, from the GitHub URL, `--reference-if-able` the shared checkout, `--dissociate` (no alternates left). Into my clone only: develop, refs/pull/2266/head, refs/pull/2099/head.
- **Worktrees:** `h` (head = merged state), `d` (develop 35d677937401), `x` (mutants, planted controls), `m` (a scratch merge commit of head + PR 2099's head, made in my clone only, for Q7).
- **node_modules:** `cp -c` (APFS clone) of root, packages/shared, services/auth and services/shared from gate 387's finished `_work/h`. No seat tree was touched. 0 absolute symlinks in each tree. That source predates the `effect` bump (root effect 3.21.4, not 3.22.5); auth declares no `effect` dependency (0 hits in services/auth/package.json; control: 1 hit in the root package.json), and both arms ran on the same copy. packages/shared/dist built with tsc in every tree (rc 0).
- **Run conditions:** Node v26.8.1 (not LTS, same as the builder's), vitest 4.1.12, TMPDIR /private/tmp/g389t.
- **Scripts** (all in `_work/`): `run_cwd_g389.py` (sets the cwd, so no `cd`), `suites_g389.sh`, `mutants_g389.py` (exact-count edit, tsc, the four touched test files, restore, sha256 check), `eslint_g389.mjs`, `probes/probe_cells.ts` (appended to the PR's own harness to make a probe file).
- **Evidence:** `_work/evidence/`. Planted files and the probe file are in `_work/_quarantine/{planted,probes}/`.
- **End state:** h, d, x and m each show 0 porcelain lines. auth.ts in x after the mutants: sha256 352b28a01388…, the same as h.

## Findings

### MEDIUM
**G389-2266-1 (deploy dependency, not a code defect): after deploy, no invitee can finish a claim through any UI.**
- FOUND: the claim link is `FRONTEND_URL/reset-password?token=…` (auth.ts `issueInviteClaimLink`). No page in this repository serves that route. Before this PR an invitee could (insecurely) claim by signing up. After it, the claim needs the link, so it needs this page AND mail delivery (outside items 3 and 6). Until both exist, invited people cannot activate their accounts except by calling the API by hand. The PR says this (outside items 3 and 6, the fragment's "Not measured" row), so it is disclosed, not hidden. It belongs in front of the deploy decision, which Kam's card keeps for himself.
- TESTED: a tree-wide search at the head for any page.
  - NOT tested: a booted frontend, any box's SMTP/ACS configuration.
- HOW: `git grep -i "reset-password"` over `Blockchain/Dev/frontend/**` and `Blockchain/Dev/mobile/**`: 0 hits. `git grep -l -i "resetPassword|reset-password|ResetPassword" -- '*.tsx'`: 0 files. Positive control: `git grep -l -i login -- '*.tsx'` returns files (admin App.tsx and others).

### LOW
**G389-2266-2: no cell pins the 600 s cooldown at the route (mutant G1 survives).**
- FOUND: ruling 3 sets "cooldown 10 minutes per user, at most 6 claim mails per hour". `INVITE_CLAIM_COOLDOWN_SECONDS = 10 * 60` changed to `10` passes all 106 cells of the four touched files.
  - The E cells pin the SQL only for the value they pass in themselves (600).
  - R7 sends five registers inside about 0.5 s, so any cooldown longer than that passes.
  - A 10 s cooldown would allow about 360 claim mails an hour to one invitee.
- TESTED: mutant G1 compiles (tsc 0) and 0 of 106 cells fail. The shipped value IS 600 s (read at source: line 181).
- HOW: `mutants_g389.py G1_cooldown_10s_not_600s` (evidence/mutants.out, mut_G1_*.json). Positive control in the same run: G15 (`make_interval(mins => …)`) is killed by E1 on all four DDL copies.

**G389-2266-3: "the link work runs after the 202, so timing cannot tell a send from a cooldown skip" holds at the head, but no KS-2272 cell pins it.**
- FOUND: mutant G2 awaits `issueInviteClaimLink` before writing the 202. Only one cell catches it, KS-1107 C2, and only by accident: that harness answers 500 when the awaited link work runs. No ks2272 cell fails.
- TESTED, on the real head code: my probe G389-P1 checks four invited states.
  - The states: first send; a live token inside the cooldown; a mail provider that takes 1.5 s; `issueInviteClaimToken` throwing.
  - Each gave status 202, the same 80-byte body, the same headers apart from `date` (including the same ETag `W/"50-92WG9NTQXJB9MJ6eavwfX9G+z0Q"`), and answered in 2 ms (24 ms for the first request, which was warm-up).
  - None of them ran hashPassword or isPasswordBreached. No session, user create, user update or email-token write.
  - NOT tested: timing on a real database or the gateway (each register makes one `getUserByEmail` round trip before the 202 or 409; this was not measured on a real engine).
- HOW: `_quarantine/probes/g389-probe.test.ts` (the PR's harness plus probe_cells.ts), evidence/probe_log_h.txt; mutant run evidence/mut_G2_*.json.

**G389-2266-4 (outside the PR, for routing): forgot-password is now an activation path, and it mails the REQUEST's spelling of the address.**
- FOUND: ruling 1 accepts that forgot-password on an invited address activates the account. forgot-password (auth.ts ~901-909, unchanged) mails `data.email`, not `user.email`. The lookup folds case and trims (`getUserByEmail`: `toLowerCase().trim()`), so a caller's case variant reaches the stored mailbox under a spelling the caller chose.
  - Only a provider whose local part is case-sensitive could tell the two apart. That is practically nil, but it falls short of the "STORED address, never the caller's" standard this PR sets for its own sender (M10).
  - forgot-password tokens are also not one-live-link. After two forgot-password calls an invited stub holds 2 live activating tokens. A forgot-password token younger than 10 minutes also suppresses the claim mail (it counts as live).
- TESTED: probes P4 and P5 on the head harness.
  - P4: forgot-password with `INVITEE-F@EXAMPLE.COM` mailed `INVITEE-F@EXAMPLE.COM`; that link activated the stub (ACTIVE, emailVerified true).
  - P5: two forgots left 2 live tokens; a register then answered 202 and sent 0 claim mails.
  - NOT tested: a real mailbox.
- HOW: evidence/probe_log_h.txt. Ruled OUT of this PR (ruling 3), so it is not a defect of PR 2266. Route it with outside items 1-6.

### INFO
**G389-2266-5: the "90 of 90 over the four touched test files" figure (READY, PR body Test Evidence) is stale. It is 106 of 106 at this head.**
- The builder's own green_four.json counts 56 + 9 + 5 + 20 = 90; it was taken before the 16 E cells were added. With the E cells the four files hold 56 + 9 + 5 + 36 = 106, and all pass (my mut_BASE.json). The figure is out of date and nothing is wrong. The PR body's "36 of 36 in the new file" is correct.

**G389-2266-6: the PR body cites cell R7 for "the same for every invited address".**
- R7 compares five registers on ONE address. The cross-address identity holds (my P1 checked four addresses in four states), but no PR cell compares two addresses. The wording is a little loose; the fact is true.

**G389-2266-7 (parity, no change made by this PR): two pre-existing patterns carry over to the claim link.**
- (a) When SMTP is unconfigured and NODE_ENV is not `production` (staging included), the claim URL carrying the live token is logged (`Invite claim link (SMTP not configured)`), exactly as the verify and reset links already are. On such a box, log access is enough to claim an invited account.
- (b) `consumeResetToken` is unconditional (`WHERE token_hash = $1`). Two concurrent resets with one token can both write. Only the token holder can do this.
- Both read at source; neither measured.

## Q1 ENUMERATION
- **Byte-identity across invited addresses: YES** (G389-2266-3 above: same status, body, header set, ETag; no cookie; 2 ms, whatever the link work does).
- **What an unauthenticated caller learns by status alone** (probe P2 on the head harness, plus a read of the handler order):
  - 400: schema-invalid. 422: `role` or `organizationId` present (KS-82, KS-1107). Both run before any lookup, so they say nothing about the address.
  - **202: the address holds an INVITED stub, in any tenant** (the lookup is global by email hash).
  - **409: the address is registered** as ACTIVE, SUSPENDED, DEACTIVATED or PENDING. These four cannot be told apart from each other.
  - 201: the address was free, and an account plus session is now created for the caller.
  - **422 (weak or breached password): the address was free, and NOTHING is created.** The strength and breach checks run only after the INVITED/409 branch.
- So with one weak-but-schema-valid password (P2: `aaaaaaaa` gave fresh 422, invited 202, active 409, suspended 409) a caller sorts any address into free / invited / registered, writes nothing, and only causes a claim mail to the invitee, capped by the cooldown.
  - On develop the same probe gave invited and free the same answer (422); 409 already revealed "registered".
  - The single new disclosure is "invited". That is exactly what option a's detail accepts ("it reveals to anyone that an address was invited").
  - No other new difference was found: no body field, no header (P2's header key sets are equal across 202, 409, 422 and 201 in the harness), no cookie, and no timing signal from the link work.
- **Timing class:** 202 and 409 both answer after the one lookup (fast). 201 and the breach 422 follow a breach lookup and/or the hash (slow). This split already existed between registered and free addresses.
  - NOT tested: real-engine timing; the harness has no cookie-parser, so the 201's refresh cookie was not observed there.

## Q2 NO WRITE ON REGISTER: holds
- Read at source: the INVITED branch writes the 202 and returns before `checkPasswordStrength`, `isPasswordBreached`, `hashPassword`, `createUser`, `storeEmailToken`, `createSession` and `publishEvent`.
- P1: on four invited addresses, hashPassword and isPasswordBreached were never called, and sessions, creates, updates and emailTokens were 0, 0, 0, 0.
- M1 (store the posted hash on the stub) is killed by 7 cells: R1 and R3 in both body forms, R2, R5, and KS-1107 C2.
- The trap-1 P1/P2 cell R3 passes at the head and fails under M1.

## Q3 THE CLAIM LINK
- **One statement** (userRepo 1295-1317): three parts.
  - `recent` CTE (same user, unused, unexpired, younger than `$4` s);
  - `retired` UPDATE gated on NOT EXISTS recent;
  - INSERT gated on NOT EXISTS recent.
  The data-modifying CTE and the INSERT share one snapshot, so the new row is not the one retired.
- **No write and no mail while a live token is younger:** E2 on 4 DDL copies; route side, the `if (!issued) return` comes before `sendInviteClaimEmail`.
- **Retire scoped to THAT user:** M7b and G17 (cooldown not scoped) are each killed by E3 on all 4 copies. G7 (no retire) is killed by E1 on all 4.
- **Entropy and lifetime:** 32 random bytes (256 bits), hex, sha256 at rest, 24 h (password.ts 24-25, 284-291).
- **Single use:** `getResetToken` filters `used_at IS NULL`; the consume runs after the write (R4: reused link 404).
- **Expiry:** checked in the handler (R4: 400).
- **Mail goes to the stub's STORED address:** `sendInviteClaimEmail(stub.email, …)`. G3 (send to `data.email`) is killed by R1 in both forms; R1 posts `Invitee-A@Example.com` and expects `invitee-a@example.com`.
- **Can two live tokens exist?**
  - (a) A same-instant race: YES, by reading. Under READ COMMITTED both `recent` snapshots are empty and both INSERTs land. Disclosed in the PR as a residual. Bounded: the next issue after the cooldown retires both.
    - NOT measured: PGlite is a single connection and cannot interleave two transactions.
  - (b) A second invite: NO. `createInvitedStub` on an existing address returns the existing row and issues no token.
  - (c) forgot-password: YES, outside this PR (G389-2266-4).
- **Cooldown value:** see G389-2266-2.

## Q4 RESET ON AN INVITED ROW
- **The write:** ONE `updateUserOrThrow(user.id = the token row's user, {passwordHash, status ACTIVE, emailVerified true, role OWNER})`, then the revocation, then the consume LAST (R2 checks the order `['update','consume']`).
- **Is OWNER right?** `createInvitedStub` makes the stub with role `USER`, no organisation, and the issuer's tenant (userRepo ~777-790). The invite carries no role or organisation of its own.
  - The claim overwrites USER with OWNER. Develop's register claim did the same (`role: 'OWNER'`).
  - It touches neither tenant_id nor organization_id; R2 and P3 show tenant and organisation unchanged.
  - That is exactly ruling 8 ("role on activation stays OWNER and the tenant stays the stub's … moves WHEN, not WHAT"). G4 (drop `role: 'OWNER'`) is killed by R2 and KS-1460 C3.
- **If the update throws:** P3 measured 503; the token was not consumed (usedAt null); the stub stayed INVITED; the same link then succeeded (ACTIVE, OWNER, verified, tenant and organisation kept). That is the KS-1052 write-before-consume design.
- **M9** (unconfirmed `updateUser`) is killed by 5 cells: KS-1460 R1, R2, C3, and KS-2272 R2, R5.
- **Non-invited reset exactly as before:** the else branch is byte-identical to develop's line. M12 (every reset activates) and G8 (a plain reset also marks verified) are each killed by C3.
- **G18** (claim without status ACTIVE) is killed by 5 cells.

## Q5 MUTANTS (merged state; tree x; each compiled, tsc 0; product sha256 restored after each)
| mutant | failing cells (of 106 in the four touched files) |
|---|---|
| BASE | 0 |
| M1 persist the posted password | 7: KS-1107 C2; R1 ×2, R3 ×2, R2, R5 |
| M7b unscoped retire | 4: E3 ×4 |
| M9 unconfirmed claim write | 5: KS-1460 R1, R2, C3; R2, R5 |
| M12 every reset activates | 1: C3 |
| G1 cooldown 10 s | **0, survives** (G389-2266-2) |
| G2 link work before the 202 | 1: KS-1107 C2, by accident (a 500) (G389-2266-3) |
| G3 mail the request spelling | 2: R1 ×2 |
| G4 claim keeps the stub role | 2: R2, KS-1460 C3 |
| G5 cooldown counts used tokens | 0, survives; **equivalent**: an INVITED stub can only hold a used token younger than 10 min if a newer live token also exists, so the outcome does not change |
| G7 no retire | 4: E1 ×4 |
| G8 a plain reset marks verified | 1: C3 |
| G15 cooldown in minutes | 4: E1 ×4 |
| G16 202 for any non-ACTIVE status | 3: C2 ×3 |
| G17 cooldown not scoped to the user | 4: E3 ×4 |
| G18 claim without status ACTIVE | 5 |

- The four required mutants (M1, M7b, M9, M12) reproduce the builder's firing cells exactly.
- The commission's suggested gap mutants are all covered:
  - "emailVerified set on register" is the M1 class (any user write on the INVITED branch fails R1, where updates must be 0);
  - "token not bound to user" is the builder's M4, killed by R5;
  - "case-folded address match" is G3/M10, killed by R1.
- The only non-equivalent survivor is G1.

## Q6 WHOLE (head vs develop, same node_modules)
- **Auth suite whole:** develop 1,956 of 1,956 in 161 files; head 1,992 of 1,992 in 162 files. Failure-name sets are equal (both empty). The probe file was not in the run (0 hits for it in suite_h.json; control: the ks2272 file 1 hit).
- **tsc --noEmit (auth):** rc 0. Planted TS2322: rc 2.
- **eslint on the 8 changed TS files:** 0 errors. One warning (`afterAll` unused, auth.integration.test.ts 11:55), identical on develop. Planted `debugger`: 1 error (no-debugger).
- **Test-types ratchet (auth):** head 41 errors, 41 baselined, 0 new, 0 stale, 162 test files; develop the same with 161. Planted test file: rc 1, 2 new.
- **check:openapi:** CHECK PASS on head and develop; spec-examples OK (422 blocks). Planted one-word yaml edit: CHECK FAIL.
- **The yaml (+14):** register `"202"` with the same description text and `$ref AuthSuccess` (`{success: boolean, message?: string}`, which fits the answer body), plus the reset-password description. Both are byte-consistent with auth.openapi.ts 740-748 and 807-811; the generator's --check passing is the proof.
- **docs-fragments check:** OK on both arms (flow and cheat 302 new on develop, 303 on head). Planted unbalanced tag: FAIL.
- **NOT run:** the standalone preflight ratchet script and its leg test; the four platform suites; a booted service; Node 24.

## Q7 OVERLAP WITH PR 2099
- `git merge-tree --write-tree` of the head against PR 2099's live head 8967de8b1755: **rc 0**. Against develop: rc 0.
- Planted control: a commit in my clone editing yaml line 3779 (PR 2099's first hunk) merged against 2099 gave rc 1, `CONFLICT (content) … secuura-api.yaml`.
- Further check: the textual merge of 2266 + 2099 (scratch commit aeba1ce4580d, worktree m) passes `check:openapi` (CHECK PASS). So the merged yaml is already what the generator produces.
- The PR body's "whichever of PR 2099 and this PR merges SECOND regenerates the yaml" is present verbatim (rulings 5(a) and 5(b) both hold). Today the regeneration would be a no-op, but it stays the right safeguard if either head moves.

## Q8 PR BODY, TEST EVIDENCE, FACTS COMMENT
- **PR body:** every factual sentence I checked holds, except the two INFO items (G389-2266-5: "90 of 90" is stale, the true figure is 106; G389-2266-6: R7 is cited for the cross-address claim).
  - Holds: the summary of develop's old claim; the 202 bytes; "never hashes, breach-checks or stores"; "publishes no user.registered event"; the 422s first; 201 and 409 kept; the single update payload; the revocation and consume order; the statement's semantics; the no-row-lock residual; no migration needed (created_at is present in all four DDL copies; E0 green on each); the OpenAPI line counts (+14); the mutant table rows for M1, M7b, M9 and M12; the whole-suite figures; the merge-tree figures; the old-assertion quotes for T1, T2 and T3 (checked against the diff).
- **KS-2272 facts comment 1f9b68e5: NOT read at source (UNMEASURED).**
  - The Secuura Linear key lives only in the Blockchain project's `.env`, which this gate may not read (same limit as gate 387).
  - I read the builder's drafts/linear_comment.txt. Every factual sentence in it matches my measurements, including 36 cells, 16 E cells, 1,956 and 1,992, and the 2099 merge-tree.
  - Whether the posted text equals the draft is UNMEASURED.
- **The six outside-auth items to route (PR body, verbatim targets):**
  1. mobile `mobile/secuura-app/src/contexts/AuthContext.tsx` 140-147: auto-login after register must handle the 202;
  2. admin `frontend/admin/src/pages/Users.tsx` 304-314: a 202 means "invitation link sent";
  3. a `FRONTEND_URL/reset-password` page that posts `{token, password}` (none exists; see G389-2266-1);
  4. `frontend/issuer/src/services/api.ts` 399: the register wrapper has no caller;
  5. systemTest and e2e fixtures that register over a stub must expect 202;
  6. mail delivery on the boxes (SMTP/ACS, `EMAIL_RECIPIENT_ALLOWLIST`).
- **Also for routing:** G389-2266-4 (forgot-password request spelling, and its multiple live tokens), plus ruling 7's two noticed items (the reset mail says 1 hour against a 24-hour token; existing squatter claims are not looked for).

## Why GO WITH NOTES
- The account-takeover path is closed: register on an invited address writes nothing and issues nothing, and only the stored mailbox's link activates the stub.
- What a claim grants is unchanged, per ruling 8. The only new disclosure is the "invited" status that Kam accepted.
- The suites and static checks are clean against develop, and the required mutants reproduce.
- The notes are a deploy dependency (G389-2266-1), one unpinned constant (G389-2266-2), one unpinned timing property that holds today (G389-2266-3), and out-of-PR routing (G389-2266-4). None of them blocks the merge.

Nothing was written to GitHub, Linear or any !CODING path. No mail was sent, nothing was launched, no database server or container was run (PGlite in-process only, through the PR's own cells), no process was killed, and no sub-agents were used.
