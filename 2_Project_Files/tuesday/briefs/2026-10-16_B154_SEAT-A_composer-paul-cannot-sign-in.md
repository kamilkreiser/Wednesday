From Tuesday (Kam's Datasec coordinator seat; Friday handed this project to Tuesday on 2026-10-15). Datasec / Security Composer. Questions to tuesday-agent@agentmail.to; your STATUS file is the wrap.
# BRIEF B154 · SEAT-A: Paul cannot sign in to the Security Composer demo. Find out why, fix it, prove he can sign in.

**BLUF.** Kam, Tuesday's terminal 2026-10-16 ~12:0x AEDT, verbatim: *"Also, Paul mentioned he cannot login into the Security Composer.  Please check why and resolve.  Tell me once he can log in again"*. Diagnose read-only first, then make the SMALLEST fix that restores Paul's sign-in, then prove it. Report in `1_Project_Definition/Briefs/2026-10-16_B154_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK). Last line exactly `DONE: B154 Paul can sign in (proved <how>)` or `STOPPED: NEEDS TUESDAY` with ONE question.

**Step 0:** copy this file unchanged into your `1_Project_Definition/Briefs/` (sha256 both copies equal; this copy is in Tuesday's tree, read-only to you).

## MEASURED BY TUESDAY (2026-10-16 ~12:0x AEDT, read-only, from outside)
- The demo host named by `COMPOSER_DEMO_URL` in your `4_Credentials/.env` answers: `HTTP/2 401`, `server: Caddy`, `www-authenticate: Basic realm="restricted"` (curl -D, root and /health). So the box is up and a Caddy basic-auth gate sits in front of the app. Tuesday did not get past it and did not use any credential.
- Demo = `ef916ce2` per Friday's handover (UNMEASURED today). main is now `230f9fab` (PR #79 merged by Tuesday 2026-10-16; parent 45591406, tree = the gated tree). **Do NOT deploy #79 or main in this brief:** Kam's card `composer-l05-setup-card-too-1014` is untapped and holds the demo on ef916ce2.
- Lead, unverified: CLARIFICATIONS COMP-16 (line ~1311) mentions "a drafted note for Paul's user guide about the changed sign-in page", ruled (a) hold. So a release may have changed how Paul signs in while his guide (`1_Project_Definition/User_Guide/2026-10-09_Paul_v1_5`) still describes the old way. Check it; it is a lead, not a finding.

## WHAT TO DO
1. Read `CLAUDE.md`, `1_Project_Definition/CLARIFICATIONS.md` (sign-in, accounts, Caddy, Paul, guest, Entra), `README.md`, Friday's demo deploy doc `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/friday/composer_demo_deploy.md` (read-only), and the newest history entries. Find how Paul is MEANT to sign in (basic-auth layer + app sign-in; which account; which identity provider).
2. Measure each layer separately, naming the instrument: (a) the Caddy basic-auth gate: which users it accepts and whether Paul's is among them (read the Caddyfile on the box, read-only); (b) the app sign-in for Paul's account (does it exist, is it enabled/locked, expired password, MFA, guest invite not redeemed, role); (c) what changed since the guide v1_5 (git log of the sign-in path, the deploys since 2026-10-09). Use the demo's documented access route only; any temporary access (key, NSG rule) is added for this job, named, and REMOVED and proven removed before you finish, as B133 did.
3. Fix the cause with the smallest change. In scope (Kam said "resolve"): re-adding/unlocking Paul's account, resetting the basic-auth entry he needs, re-issuing an invite, restarting a stuck service. If the fix needs a NEW password or link that Paul must receive, set it, put it ONLY in your project's `4_Credentials/` (chmod 600, never in STATUS, a commit or a mail), and say in STATUS where it is: Kam sends it to Paul, never you. OUT of scope, STOP and ask: deploying a new build, changing the sign-in design, deleting any account or data, anything touching other users.
4. Prove it: sign in as Paul's account (or the exact path Paul uses) end to end in a real browser, read only, and record what screen he lands on. If his credential is unknown to you, prove every layer up to it and say exactly what Paul must enter.
5. Tell Tuesday what Kam should tell Paul, in one or two plain sentences (Kam sends it).

## HOLDS
- Nothing to Paul or any human: Kam sends. Paul's user guide is updated only when Kam asks.
- The demo site is Kam's: change only what step 3 allows, with a backup of any file you edit (Caddyfile etc.) kept beside it, dated.
- Work only in a `_wt_b154*` worktree for anything git; the root `2_Project_Files` takes read-only verbs only.
- Never delete (quarantine). Secrets stay in 4_Credentials/ and 3_Access_Keys/. No HP marks or HP-NDA material.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 12:0x
