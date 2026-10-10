From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies to `friday-laptop-agent@agentmail.to`; if `4_Credentials/.env` has no `AGENTMAIL_API_KEY`, the STATUS file is the wrap.

# BRIEF B31 · SEAT-C — PART A: redeploy the hosted showcase to main `4f27f553…` (CODE ONLY, no app-setting change). PART B: one second sign-in account with the Approver role ONLY
**Drafted:** 06:55 AEDT 2026-10-11.
**Report:** `1_Project_Definition/Briefs/2026-10-11_B31_STATUS.md`. Its last line is exactly **`DEPLOYED: <sha> live-check <rc>`** or **`STOPPED: NEEDS FRIDAY`** followed by the one question that blocks you.
**Client:** Datasec only. **Project:** MPS Commercial Calculator only. **Tier:** 2. Production-class steps run only in the order below. PART B starts only after PART A is live and checked.
**Pane:** `*MPS*-C`. This is the newest `_SEAT-C_` file in `Briefs/`.

**Convention.** Records files under `1_Project_Definition/Briefs/` are untracked in the records repo. For them, `file:line` means the working-tree file as Friday's drafter read it on 2026-10-11 (morning AEDT). Code is cited as `path:line @ <sha>` in `2_Project_Files`. The drafter's local clone has no object `4f27f55`; code citations are at `42d6eca` (main before B28) unless stated.

## Target (PART A)
- **`4f27f553…` = main, read by Friday from the GitHub API at 01:2x AEDT 2026-10-11, tree `a61a36dd`.** The full SHA is yours to read. This is main after B28 (`b28/commercial-readiness-fixes` @ `206b82fe26a89fa2d878fa037e09b418a725b918`) merged on top of `42d6ecaf7805b746fbf28fe8b988fe76775650fc` (B25, PR #22).
- **Assert all of these before anything else.** On any mismatch: **STOP: NEEDS FRIDAY**.
  1. `git ls-remote origin refs/heads/main` → a full SHA that **starts with `4f27f553`**. Write the full 40 hex into STATUS; it is `<sha>` everywhere below. Anything else (main moved on, or a different commit): STOP.
  2. `git rev-parse <sha>^{tree}` = **`a61a36dde3a55ee9b759ebc8459f07405ba72b16`**: the tree gate B29 round 2 measured for "merged main `42d6eca` + b28" and graded GO WITH NOTES (`B29_STATUS.md:705-706`).
  3. `git merge-base --is-ancestor 42d6ecaf7805b746fbf28fe8b988fe76775650fc <sha>` rc 0, and `git rev-parse 42d6ecaf7805b746fbf28fe8b988fe76775650fc^` = `a168badaa4a88fcbbd91e7d1350cd45320969ce9` (the live build; drafter measured this one, rc 0).
  4. `git diff --name-only a168badaa4a88fcbbd91e7d1350cd45320969ce9 <sha> -- infra scripts .github` = **empty**. The drafter measured it empty for `a168bad`→`42d6eca` and for `a168bad`→`206b82f`; on `<sha>` itself it is UNMEASURED. Not empty: STOP (a code-only deploy assumes byte-equal deploy scripts and Bicep).
  5. `git log --oneline a168badaa4a88fcbbd91e7d1350cd45320969ce9..<sha>` → record it verbatim; expect the B25 commit (#22) and the B28 merge only.
- **Live today:** main `a168bad`, deployed by B24: package `mpscalc.zip` sha256 `2e46037c2aa9789dd9e33ac46a33ee8628fef63a69ad6ddbf27b4ca07c1ce1e9`, 2,730,652 bytes, 48 files; `check` rc 0; HSTS `max-age=31536000`; 16 app settings with `MpsCalc__CatalogueOverlay__Path=/home/data/catalogue-overlay/` (`B24_STATUS.md:10-12,72-78,83,205`).
- **Site:** `app-mpscalc-showcase-u6agl3edszqvs` in RG `mpscalc-showcase-rg`, https://app-mpscalc-showcase-u6agl3edszqvs.azurewebsites.net/ (`B24_SEAT-C_hosted-redeploy-overlay-persistence.md:19`).

## AUTHORITY
- **Kam, live board (Friday tab), 2026-10-11 06:48:47**, verbatim: *"Decision mpscalc-new-words-hosted-deploy-1011: a — Approve the wording and deploy"*. The card (`0_Brain/dashboard/data/decisions.json`, id `mpscalc-new-words-hosted-deploy-1011`, `ruled_choice` a, `ruled_ts` 2026-10-11T06:49:22+11:00) says, verbatim:
  - Title: *"Ship last night's calculator fixes to the hosted site? Approve the new wording first"*
  - BLUF (closing sentence): *"The deploy is code only: no setting changes, and the storage-path hold stays in place."*
  - Option a detail: *"A deploy seat ships main 4f27f55 to the same hosted URL, code only. Friday runs the gates' post-deploy checks herself and tells you the result."*
  - Default: *"Nothing is deployed until you answer; the hosted site stays on yesterday's build a168bad."*
- **Kam, live board (Friday tab), 2026-10-11 06:49:15**, verbatim: *"Decision mpscalc-second-approver-for-kam-test-1010: a — Friday's seat creates a second sign-in account with the Approver role only"*. The card (id `mpscalc-second-approver-for-kam-test-1010`, `ruled_choice` a, `ruled_ts` 2026-10-11T06:49:30+11:00) says, verbatim:
  - BLUF: *"…you cannot approve your own quote (your rule this morning: no self-approval), and your account is the only one on the hosted site, so alone you only reach a DRAFT proposal. A second account with the Approver role fixes it without changing your rule."*
  - Option a detail: *"A new user in the datasec-rd tenant (e.g. mps-approver@datasec-rd.com), Approver role on the calculator only, created by the MPS seat under your existing az login. You sign in as it in a private window to approve. Its first-time password goes to you only, never by email or chat. Removable in one command."*
- **Gates:** B27 (overlay class, B25) NO GO on H-1 only, shipped under the two-NO-GO cap with the residue ticketed (`B27_STATUS.md:17-27`; `B25_SEAT-A_ADDENDUM-1_gate-b27-residue-records.md:4-5`). B29 round 2 (B28) **GO WITH NOTES** for the b28 head and for the merged tree `a61a36dd…` (`B29_STATUS.md:703-706`). Their post-deploy items (below) are this brief's live checks; none of them is a gate pass.
- **Standing:** C-06/C-06a hosting in tenant `ec01829b…` under `kamil@datasec-rd.com`; C-12 no self-approval (PART B exists *because of* C-12, and does not change it); GST fixed at 10%; `PlatformModes = Accept`.
- **What this covers:** PART A, a code redeploy of `<sha>` to the existing site, its own restart, the read-back and live checks. PART B, one new Entra user in tenant `ec01829b…`, one app-role assignment (Approver) on the existing API service principal, and its proof.
- **What it does not cover:** any app setting, any Bicep apply or `az deployment`, any new Azure resource, any change to an app registration or service principal, any role for any other principal, any Entra directory role, any licence, any MFA / Conditional Access / security-defaults change, any price-book upload, any seed run, any overlay write, any mail or message to a human, any Jira write.

## HOLDS (verbatim lines, plus the site HOLD)
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: never push to main; never dismiss an alert; never ask for a bypass.
- No new paid Azure resource; no app-setting change; SITE HOLD stands.
- Nothing to any human; Friday tells Kam.
- Never delete; quarantine.
- Never print a secret.
- **SITE HOLD** (B24 ADDENDUM-1:22-24 + B25 ADDENDUM-1 item 2): none of `MpsCalc__QuoteStore__Path`, `MpsCalc__QuoteStore__HostedRoot`, `MpsCalc__ReferenceStorePath`, `MpsCalc__CatalogueOverlay__Path` changes, and **`MpsCalc:ReferenceStorePath` stays a regular file (never a link)**. This deploy carries the G-4 fix (B27 closed G-4), but H-1 is open, so the HOLD stands after it too.

## PART A — steps (in order; record each command verbatim, with `cmd > out 2>&1; rc=$?` and the measured line)
0. **Login (C-2).**
   - `echo "$AZURE_CONFIG_DIR"` must print `…/Datasec MPS Commercial Calculator/4_Credentials/.azure`.
   - `az account show --query '{t:tenantId,s:id,u:user.name}' -o json` must give `t=ec01829b-fdcb-4503-9834-eb2ffbd99169`, `s=a6b8fe11-d1b5-4293-8727-b34aba08a705`, `u=kamil@datasec-rd.com` (`B24_STATUS.md:47`; `scripts/entra_apps.py:43-44` @ `42d6eca`).
   - Anything else: **STOP: NEEDS FRIDAY**. Never run `az login` or `az account set` yourself. Never use another project's config dir or `~/.azure`. An authorization error is reported, never worked around.
1. **Pre-read (read-only), saved for the comparisons below** (the B24 evidence shape, `B24_evidence/01_pre_*`):
   - app settings → names plus non-secret values to `01_pre_appsettings.tsv`. Expect **16 names, `diff` empty against `B24_evidence/08_s2_after_appsettings.tsv`**. Any name not in that set: print the name only, never its value, and STOP. Assert `DOTNET_SYSTEM_IO_DISABLEFILELOCKING` absent.
   - `az resource list -g mpscalc-showcase-rg -o table` → the plan and the site, both Succeeded.
   - Kudu **VFS GET only**: quote-file count under `/home/data/quotes/` (6 at B24; **re-measure**: Kam's walkthrough may have added quotes, so the pre-read is the baseline, not 6); `/home/data/catalogue-overlay/` listing (names only).
   - **Reference path is a regular file (SITE HOLD; B27 P-7 read-only):** VFS GET of the listing of `/home/data/pricebooks/`; record the `reference.json` entry's `mime` and `size` (no content). A link (e.g. `inode/symlink`) or a missing entry: STOP. Whether VFS distinguishes a link is UNMEASURED; say what you saw.
   - Seed token, act-as Seller: `GET /api/v1/quotes` → refs and states; `GET /api/v1/catalogue/devices` → 200, count; `GET /api/v1/inventory` → 200, `overlayVersion` and manual-row count (0 and 0 at B24; **re-measure**). If `overlayVersion` > 0, say so: an `overlay.json` exists, and rollback compatibility (below) changes.
   - `reference.json` **MATCH** (step 4).
2. **Package from a CLEAN checkout.**
   - `git fetch origin` in `2_Project_Files`, then a new detached worktree `.tools/wt-B31-release` at `<sha>`, chmod 700. Assert tracked diff 0 and ignored files 0 before the build.
   - Project SDK only (`.tools/dotnet`), with `MSBUILDDISABLENODEREUSE=1` and `UseSharedCompilation=false`.
   - `bash scripts/package.sh <sha>`, then `python3 -I scripts/deploy-package.py verify .local/deploy-packages/<sha> --expect-commit <sha>` → rc 0.
   - Quote the package sha256, byte count, file count and B2-scan line. File count is UNMEASURED (48 at `a168bad`; B28 changed web code, so the count may differ: not a pass condition).
   - **Keep the rollback build:** `.tools/wt-B24-release` (detached at `a168bad`) and its package under `.local/deploy-packages/a168badaa4a88fcbbd91e7d1350cd45320969ce9/` stay where they are. Assert now: package sha256 = `2e46037c2aa9789dd9e33ac46a33ee8628fef63a69ad6ddbf27b4ca07c1ce1e9`, 48 files, `deploy-package.py verify … --expect-commit a168badaa4a88fcbbd91e7d1350cd45320969ce9` rc 0. If it is gone or differs: rebuild it in a NEW worktree `.tools/wt-B31-rollback` at `a168bad` and record its sha256 (the zip is stamped, so a rebuild's sha256 may differ; that is not a failure). Do not deploy before a verified rollback package exists.
3. **Deploy the CODE (no setting is touched).**
   - Re-run C-2. `scripts/deploy-from-ci.sh deploy <sha> mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs`. An `az` start-tracking timeout has happened while the site was up.
   - **Whatever `deploy` returns, run** `scripts/deploy-from-ci.sh check .local/deploy-packages/<sha> mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs` → rc (wwwroot byte compare plus HSTS `max-age>0` on https `/health`, else exit 3). Exit 3 = DEPLOYED BUT NOT PROVEN: investigate, never skip; unproven → R-1, then STOP.
   - **Start log (the B24 P-4 method, `StartupLogs/*_success.log` by VFS GET):** the new start shows the quote store's and the overlay's Accept warnings and **no "Start refused"**. This build carries the G-4 case-insensitive overlap guard; with the three live values it must start (B24 ADDENDUM-1:13-16). A refused start: R-1, STOP.
   - **Live check L1** (`curl -sS -D -`; status line and HSTS header verbatim), the B24 set (`B24_STATUS.md:96-112`): `/` 200 text/html · `/health` 200 · `/auth-config.json` 200 with tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, spaClientId `3c31a4fb-a750-48eb-83f8-ab6a46a227f1`, apiScope `api://c40e74df-3d09-4935-be5d-fb7cfd04514b/access_as_user` · `/api/v1/me`, `/api/v1/quotes`, `/api/v1/inventory` (no token) 401 each · `http://…/health` 301 · HSTS `max-age=31536000` · the five data paths 404 each · `/data/quotes/` the SPA fallback `cmp`-equal to `/` · `/api/v1/nope` JSON 404 `NOT_FOUND`.
   - **Read-back R1:** app settings `diff` empty against step 1 (**16 names, 0 added, 0 changed, 0 removed**: this is the "no app-setting change" proof); `az resource list` = pre-read; quote-file count = pre-read; seed `GET /api/v1/quotes` = the same refs and states; `GET /api/v1/inventory` → 200, `overlayVersion` = pre-read; `catalogue-overlay/` listing = pre-read; `reference.json` MATCH; reference entry still a regular file.
   - **Any L1/R1 failure:** R-1, then STOP.
4. **Price books untouched. READ-BACK ONLY: never call `upload-pricebooks.sh upload`.** `reference.json` on the site against `2_Project_Files/.local/pricebooks/reference.json`, sha256 compared in memory, printing **MATCH/MISMATCH only** (the B24 method, `B24_STATUS.md:114-120`). At the pre-read, after the deploy, and at the end of PART B. MISMATCH or a missing quote: STOP. Do not re-upload, do not re-seed.
5. **Leak check on the live wwwroot:** copy (never edit) `.tools/qa-B24/` tools and `lists/` into `.tools/qa-B31/` (0700); `control` must fire on all kinds; `scan-files` over the live wwwroot zip `check` downloaded (every file; `strings -n 4` for binaries) and the L1 public bodies. **COUNTS only**, with the denominator; adjudicate as B24 did (`B24_STATUS.md:161-170`). Any unadjudicable client hit: STOP; the site stays as deployed.
6. **Post-deploy check items** (next section): run what this seat can; the rest is NOT TESTED, never faked.

### Rollback (PART A)
- **R-1:** redeploy `a168bad` from the step-2 rollback package: `scripts/deploy-from-ci.sh deploy a168badaa4a88fcbbd91e7d1350cd45320969ce9 mpscalc-showcase-rg app-mpscalc-showcase-u6agl3edszqvs` (from `.tools/wt-B24-release`, or `.tools/wt-B31-rollback`), then `check` → rc, L1, R1. **No setting changes in R-1**: `a168bad` runs with the overlay setting set (B24 proved it).
- **Before R-1, re-read `overlayVersion`.** If it is higher than the pre-read (someone edited after the deploy), `overlay.json` was written by the new code; whether `a168bad` reads it is UNMEASURED. Then **do not roll back: STOP: NEEDS FRIDAY**, site as it is. Never move, edit or remove `overlay.json`/`overlay.lock`; a corrupt-file recovery is a person's move (`docs/API.md:256-260` @ b22).
- Every rollback ends in **STOP: NEEDS FRIDAY**, with its `check` rc and L1 table in STATUS. PART B does not run after a rollback.

## Post-deploy check items (verbatim from the gates; each needs RUN with evidence, or `NOT TESTED (<who>)`)
**From `2026-10-10_B29_STATUS.md` `## Post-deploy check items (each with its FAIL condition)` (`:485-493`), verbatim:**
> 1. **Hosted, a real Entra account with {Seller, Approver, PricingAnalyst}.** Open an own purchase draft as Seller, then click
>    "Switch to Pricing analyst". FAIL: the switch is missing, it lands on another persona, or there are 0 price controls after
>    it.
> 2. **Hosted, an account with {Seller, PricingAnalyst} only.** FAIL (until H-2 is fixed): the page says "Your sign-in does not
>    include them."
> 3. **Hosted, proposal content save with network throttling (Slow 3G).** FAIL: the previous document is visible and Print is
>    enabled after "Saved" and before the notice (H-1).
> 4. **Hosted NEW WORDS:** every string in the NEW WORDS table reads as listed. FAIL: any other wording.

**From `2026-10-10_B29_STATUS.md` `### Post-deploy check items (round 2 additions)` (`:670-674`), verbatim:**
> 1. **Hosted, an account with {Seller, PricingAnalyst} only:** FAIL if "Switch to All my roles" is missing, or if there are 0
>    price controls after it.
> 2. **Hosted, proposal content save under Slow 3G throttling:** FAIL if the document or Print appears before the "Saved. …"
>    notice, or if the "Updating the document after your save…" line is missing.

**From `2026-10-10_B27_STATUS.md` `## Post-deploy check items`, item 7 (`:326`), verbatim:**
> 7. **Deploy order + NEW WORDS:** Kam sees the NEW WORDS above before the deploy. The B24 HOLD on the four store path settings stands until this fix is merged **and** deployed.

**Who runs what (drafter's reading; you record the result per item):**
| Item | This seat | Why |
|---|---|---|
| B29 #1 | `NOT TESTED (needs Kam's browser; Friday runs it)` | Only Kam holds Seller+Approver+PricingAnalyst (`B14_STATUS.md:115,118-119`); the PART B account is Approver only and cannot own a draft. |
| B29 #2 / round-2 #1 | `NOT TESTED (no {Seller, PricingAnalyst}-only account exists; Friday decides)` | Round-2 #1 is the post-H-2 form of #2. PART B creates an Approver-only account, not this one; creating it is outside both Kam rulings. |
| B29 #3 / round-2 #2 | `NOT TESTED (needs Kam's browser; Friday runs it)` | A content save needs the quote's owning Seller in a browser; the seed is app-only. |
| B29 #4 NEW WORDS | **Bundle half: RUN.** For each user-visible string in `B29_STATUS.md` `## NEW WORDS` (`:393`) and `### NEW WORDS (round 2 delta)` (`:635`), and the web-facing ones in `B27_STATUS.md` `## NEW WORDS` (`:244`), count its presence in the live wwwroot `check` downloaded (count per string, denominator = strings checked; API-detail and log strings are server-side: mark them `n/a to bundle`). **Rendered half:** `NOT TESTED (needs Kam's browser; Friday runs it)`, except what the PART B account can see if it signs in (record those few, verbatim). | Presence in the bundle is not "reads as listed on screen"; say so. |
| B27 #7 | **RUN (records only).** Kam saw the NEW WORDS before the deploy: the card's BLUF quotes them and points to the full tables, ruled a at 06:48:47 (AUTHORITY). HOLD: state that this deploy completes the G-4 condition of the B24 HOLD, and that the SITE HOLD stands anyway (H-1 open). | — |

## PART B — one Approver-only account (only after PART A ended with `check` rc 0, L1, R1, MATCH and leak counts all passed)
**How Kam's account got its roles (follow this path; do not run the script):** `scripts/entra_apps.py` @ `42d6eca` (byte-equal at `a168bad`; drafter measured `git diff` empty) assigns app roles by Microsoft Graph through `az rest` under Kam's login: `me = az ad signed-in-user show` (`:250`), then `ensure_assignment(api_sp, me, rid)` for each role (`:262-263`), which is `POST /servicePrincipals/{api_sp}/appRoleAssignedTo` with `{principalId, resourceId, appRoleId}` after a duplicate check (`:147-152`). Role ids are fixed: **Approver = `6f0f2a52-5c1e-4b8e-9d1a-7a1b6c3e2d02`** (`:37`). The API service principal has `appRoleAssignmentRequired = true` (`:255`).
- **Do not run `scripts/entra-app-registrations.sh`.** Its docstring says *"Nothing else: no user is created, invited or assigned"* and its read-back fails unless there are *"exactly 4 user assignments, all Kam's"* (`entra_apps.py:15-16,291-296`). After PART B a re-run will exit 1 on that line. Record that in STATUS as a known consequence for Friday (BACKLOG: the script needs to learn the approver account); do not edit the script.

**Identifiers to MEASURE, not assume** (expected values from the records):
- Tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, subscription `a6b8fe11-d1b5-4293-8727-b34aba08a705`, login `kamil@datasec-rd.com` (`B24_STATUS.md:47`; `entra_apps.py:43-44`). Re-run C-2 first; **any other tenant: STOP.**
- API app `mpscalc-api-showcase`, appId `c40e74df-3d09-4935-be5d-fb7cfd04514b`, service principal `da29fcef-ad0f-4549-88e0-85379f123fec` (`B14_STATUS.md:112`); web (SPA) appId `3c31a4fb-a750-48eb-83f8-ab6a46a227f1` (`B14_STATUS.md:113`; live in `/auth-config.json`, `B24_STATUS.md:101`). Measure: `GET /servicePrincipals?$filter=appId eq 'c40e74df-3d09-4935-be5d-fb7cfd04514b'` → exactly one, id as above, its `appRoles` include `Approver` with id `…2d02`. Mismatch: STOP.
- Kam's object id `60270b08-c180-446b-93a5-0fe9406c8e74` (`B14_STATUS.md:115`) — read only, for the "unchanged" proof.
- The user domain: read `GET /domains` (names + `isVerified` only) and Kam's UPN domain; use `datasec-rd.com` only if it is verified there. Otherwise STOP.

**Steps (Graph through Python 3 stdlib, `-I`; the Graph token comes from `az account get-access-token --resource-type ms-graph` captured into the process's memory: never on argv, never printed, never in a file):**
1. **Before-read** (to `B31_evidence/20_before_*`): `GET /servicePrincipals/da29fcef…/appRoleAssignedTo` → count by `principalType` and, per assignment, `principalId` + `appRoleId` (expect **4 User, all Kam's, one per role + 1 ServicePrincipal (seed → Seller)**, `B14_STATUS.md:115-119`). Anything else: STOP. `GET /users?$filter=userPrincipalName eq 'mps-approver@datasec-rd.com'` → expect 0 (exists: STOP, never reuse or reset someone's account).
2. **Password:** generate in-process with `secrets` (≥ 24 chars, upper/lower/digit/symbol, satisfying Entra complexity). Write it **only** to `<MPS project>/4_Credentials/mps-approver_initial-password.txt`, created with `os.open(..., O_WRONLY|O_CREAT|O_EXCL, 0o600)` (refuse to overwrite), content: UPN line + password line. Assert mode `0600` and that `git -C <MPS project root> check-ignore` reports the path as ignored (rc 0); not ignored: STOP before creating the user. The password never reaches the pane, argv, an evidence file, STATUS, a ticket or a mail.
3. **Create the user:** `POST /users` with exactly `{accountEnabled: true, displayName: "MPS Approver (showcase test)", mailNickname: "mps-approver", userPrincipalName: "mps-approver@datasec-rd.com", passwordProfile: {password: <from memory>, forceChangePasswordNextSignIn: false}}`. No `usageLocation`, no licence, no group, no manager, no directory role, no `otherMails`. Record the new object id (not a secret).
   - *`forceChangePasswordNextSignIn: false` is Friday's drafting choice so the seat's one proof sign-in does not have to set a password Kam has not seen. Say it in STATUS; Kam can change the password at his first sign-in.*
4. **Assign Approver, nothing else:** `POST /servicePrincipals/da29fcef…/appRoleAssignedTo` with `{principalId: <new id>, resourceId: "da29fcef-ad0f-4549-88e0-85379f123fec", appRoleId: "6f0f2a52-5c1e-4b8e-9d1a-7a1b6c3e2d02"}` (the `entra_apps.py:151-152` body). Record the assignment id.
5. **After-read** (`21_after_*`): assignments = before **+ exactly one** (`User`, the new id, Approver); Kam's 4 and the seed's 1 byte-equal by id. `GET /users/<new id>/memberOf` → 0 entries (no group, no directory role). `GET /users/<new id>/appRoleAssignments` → exactly 1 (the one above). Anything else: STOP (do not delete: report).
6. **Prove it (hosted, no change to anything):**
   - **Sign-in + token roles.** A headless Playwright browser (the web project's `@playwright/test`; whether a browser binary is installed on this machine is UNMEASURED; installing one is allowed, it is not an Azure resource) opens the site in a fresh context, follows the MSAL redirect and signs in with the UPN and the password read from the 0600 file into memory. **Tracing, video and screenshots OFF** on the sign-in pages. Capture the `Authorization: Bearer` of the first `/api/v1/me` request in memory; decode the JWT payload (no signature check needed for this read) and print **only** `tid`, `aud`, and the **`roles` names**. PASS: `tid` = `ec01829b…`, `aud` = `c40e74df…` (or `api://c40e74df…`), `roles` = **exactly `["Approver"]`**. Also record `GET /api/v1/me` → roles and `permissions` (names only).
   - **Cannot price.** With that token, `POST /api/v1/quotes` with body `{}` (create a Draft: Seller only, `docs/API.md:11` @ `42d6eca`). PASS: **403**. Record status + problem `code` only. Any 2xx: a quote was created; record its id, do not delete it, STOP. Also record the `permissions` of `GET /api/v1/quotes/<DEMO-S1 id>` for this caller: `calculate` and `edit` false.
   - **If the sign-in stops at an MFA registration or any "more information required" page:** stop the proof there. Record "credentials accepted; MFA registration required" (page title only). **Do not register any MFA method, do not touch Conditional Access or security defaults, do not use another sign-in flow** (no ROPC, no device code, no app-registration change). The tenant's MFA is recorded as mandatory with no skip (`B14_SEAT-C_infra-ci-deploy-demo.md:156`), so this is the drafter's expected outcome. Then token-roles and cannot-price are `NOT TESTED (needs Kam's first sign-in with his phone; Friday runs it)`, and the Graph after-read (step 5) is the role proof of record.
   - Any wrong role in the token, or a 2xx on the pricing call: **STOP: NEEDS FRIDAY**.
7. **End checks:** `reference.json` MATCH; app settings `diff` empty against step 1; L1 once more; seed `GET /api/v1/quotes` = pre-read (plus nothing).
- **Removal (for Friday and Kam, NOT this seat):** `az ad user delete --id <new object id>` removes the user and its assignment. Write the command into STATUS; never run it. A half-done PART B (user created, assignment failed) is reported as it stands: STOP, no cleanup.

## Other holds (absolute)
- **Azure writes allowed:** PART A's zip deploy (with its own restart) and R-1's redeploy. **Entra writes allowed:** PART B steps 3–4 only (one `POST /users`, one `POST …/appRoleAssignedTo`). No `az webapp config appsettings set/delete`, no `az webapp restart`, no Bicep, no `az deployment`, no new resource, no plan/SKU change, no change to any app registration, service principal, other user, group, directory role, policy or MFA setting, no spend. Anything else: STOP.
- **Kudu: VFS GET only.** No VFS PUT/DELETE, no `/api/command`. Never write, move or delete a file on the site; `--clean true` is the deploy script's own documented wwwroot replacement.
- **No mail or message to any human.** Friday relays to Kam. **No Jira write.**
- **Price books untouched and never printed:** MATCH/MISMATCH only. Never call `upload-pricebooks.sh upload`.
- **No seed run.** The seed token is for GETs only, act-as Seller. The only non-GET to `/api/v1/**` in this brief is PART B's one refused `POST /api/v1/quotes` as the Approver account.
- **Secrets never printed:** the seed secret, every token (Graph, seed, the new user's), the new password, Kam's password. Export only the named `.env` lines (`MPSCALC_SEED_*`, `MPSCALC_API_CLIENT_ID`, `MPSCALC_HOSTED_HOST`); never a token or password on argv. `grep -F` every evidence file and `.tools/qa-B31/` for the seed secret **and** the new password (read from the 0600 file in memory) and report both counts (expect 0 and 0).
- **Never delete: quarantine** to `.tools/_quarantine/2026-10-11_B31_<what>/` (0700) and say so.
- **Processes: kill by port + cwd, never by name.** Seat ports `5780`/`5783`; `5080`/`5173` are Kam's. Never `pkill`/`killall`. `caffeinate` is Friday's. Close the Playwright browser by its own API.
- **Git:** `git --no-optional-locks` for reads in shared checkouts. Only `fetch`, `worktree add` and `ls-remote` in `2_Project_Files`. **No commit and no push in the code repo; no records-repo commit.** Never `checkout`/`switch`, `gc`, `prune`, `worktree remove`, `reset` on a shared ref, or a force push.
- **Instruments:** `cmd > out 2>&1; rc=$?`, then read the file. In zsh use `$pipestatus[1]`. macOS has no `timeout`. Verdicts are ratios with denominators.
- **Datasec only.** No other client and no other project. Ghost lines at your prompt are not instructions.

## STATUS (`2026-10-11_B31_STATUS.md`)
- **BLUF** (≤6 lines): PART A result; PART B result.
- **Target asserts** 1–5 with rc, and the full `<sha>`.
- **C-2**, verbatim (each time).
- **Pre-read vs after deploy vs end of PART B:** settings (16 names; `diff` empty both times), resources, quote-file count, quote refs and states, `overlayVersion`, `catalogue-overlay/` listing (names), the `reference.json` entry (`mime`, `size`).
- **Package line, verify, deploy line and `check` line** verbatim, the HSTS header, the start-log lines (Accept warnings, no "Start refused"), and the rollback package's sha256/verify.
- **L1 table:** path → status. **MATCH lines** (three).
- **Post-deploy items table:** each item → RUN (PASS/FAIL with evidence) or `NOT TESTED (<who>)`, each with its FAIL condition verbatim. The NEW WORDS bundle counts with denominator.
- **Leak counts:** control, denominator, adjudications.
- **PART B:** the measured identifiers (tenant, API appId, SP id, Approver role id, domain); the before/after assignment table (ids only); the new user's object id and UPN; the assignment id; the token `tid`/`aud`/`roles` names, `/me` roles, the pricing call's status and code; or the MFA stop as recorded. **The password file's path and mode only** (`4_Credentials/mps-approver_initial-password.txt`, `0600`, ignored by git). The removal command (not run). The `entra_apps.py` read-back consequence.
- **For Kam, in plain words (Friday relays):** the hosted site now runs last night's fixes with the wording he approved; nothing he had saved changed; the second account exists with the Approver role only; where its password is (path only) and that it goes to him only; what he still needs to do himself (the browser checks, MFA set-up at first sign-in, approving his test quote in a private window); the storage-path hold stays.
- **UNMEASURED. NOT DONE / NOT TESTED.**
- **Processes and worktrees left.** One entry at the top of `5_Project_History/history.md` (re-read it immediately before writing).
- Second-to-last line: **`APPROVER: <created+proven | created, sign-in proof NOT TESTED (MFA) | not created>`**.
- **Last line:** **`DEPLOYED: <sha> live-check <rc>`** (rc 0 only; the rc of PART A step 3's `check`, with L1, R1 and MATCH also passed), or **`STOPPED: NEEDS FRIDAY`** + the one question.

## UNMEASURED (Friday's drafter did not measure these)
- `4f27f55` itself: the drafter's clone has no such object. Its full SHA, its parents, its tree (Friday read `a61a36dd` from the GitHub API), and whether `infra/ scripts/ .github/` are unchanged from `a168bad` (empty for `42d6eca` and `206b82f`; Target items 1–4 assert it).
- The new package's file count and size.
- Today's live state: quote count, refs/states and `overlayVersion` after Kam's evening walkthrough; whether any `overlay.json` exists.
- Whether `a168bad` can read an `overlay.json` written by the new code (rollback after an edit).
- Whether Kudu VFS shows a symbolic link differently from a regular file.
- Whether `kamil@datasec-rd.com` may create users in tenant `ec01829b…` (User Administrator or higher); an authorization error is reported, never worked around.
- Whether `datasec-rd.com` is a verified domain in that tenant (the card's example UPN assumes it).
- Whether the tenant forces MFA registration at a new user's first sign-in (the records say mandatory, no skip), and whether a headless Playwright browser can complete the sign-in at all.
- Whether a Playwright browser binary is installed on this machine.
- Whether the API's role check answers `POST /api/v1/quotes {}` with 403 before body validation (a 400 is not a pass: record it and STOP).
- Which NEW WORDS strings an Approver-only sign-in can see rendered.
- The persona label in the web that keeps Administrator and PricingAnalyst for Kam's edit (carried from B24).
