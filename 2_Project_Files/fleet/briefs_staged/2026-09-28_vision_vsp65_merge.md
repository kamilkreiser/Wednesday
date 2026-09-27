# BLUF — MERGE VSP-65 to portal main (gate 10 GO at 0d992e0, 16:46Z), merge QuickQuote's BACKLOG branch, file gate 10's tickets, then WRAP. NO DEPLOY: putting VSP-65 on the live portal is Kam's word, and Tuesday cards him after your MERGED.

**Addressed to the cockpit seat `Datasec/Vision_Sales_Portal`.** Read the gate report WHOLE first: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2/report.md` (VERDICT, FINDINGS INDEX, THE QUEUE, NOT TESTED).

## AUTHORITY
Merges of gated work are Tuesday's GO (v1.3 signed delegation; the gate is the condition). This mail is that GO for the two merges below. Deploying the portal is PRODUCTION and stays Kam's.

## 1. MERGE VSP-65 — portal `fix/vsp-65-pool-query-timeout-2026-09-27` @ `0d992e09ebe0830dbe414aa73ca9a17a1be6c480`
- Main at origin = `eaf024a` (Tuesday's ls-remote at this brief). The gate measured main as the merge-base, so this is a FAST-FORWARD: the pushed tree is the gated tree `30798eef…`, byte for byte.
- Conditions, in the same action as the push: ls-remote main still `eaf024a` (if it moved: STOP and mail); `merge-base --is-ancestor eaf024a 0d992e0` rc 0; head exactly `0d992e0`. Push `0d992e0:refs/heads/main`, no merge commit, no force.
- No lock hold needed: the gate already ran unit 105/105 and test:db 78 as sets on exactly this tree (report §N.6); re-running an unchanged tree is duplication (Kam, 2026-09-18).
- After the push: read that `test.yml` and `gitleaks.yml` are the only workflows on main and neither deploys (Tuesday READ: both are `on: push` to main, test + scan only). CI is UNMEASURED from this machine (gh not logged in; Kam's hands) — say so in the MERGED mail. The gate names CI's Node 22 coverage gate and `e2e:pro` (the first CI boot of the new schema.sql) as the first things to read once CI can be read.

## 2. MERGE QuickQuote `backlog/qq-purge-deployed-2026-09-27` @ `e4089041d6213d460e74992ddf775a909ffe03eb` (your own BACKLOG-only commit)
Hygiene tier (BACKLOG.md only; no gate). QuickQuote main at origin = `986f7b8` (read at this brief). Fast-forward if main is its parent, else merge forward; check the diff is BACKLOG.md only before pushing. QuickQuote's workflow runs tests only, no deploy (your 09-27 MERGED read).

## 3. TICKETS (Jira VSP, BLUF-first; search by symbol/path first; one per fix that one pass proves)
- **VSP65-R2-O1 (Minor):** with `IDX_session_expire` missing, the guarded CREATE INDEX (`server/schema.sql:281-285`) can fail a boot main passed (42501 as a non-owner; DB_QUERY_TIMEOUT at 30 s behind a held write). Fix shape and regression cells are in the report. Reachable via a backup-db dump restore.
- **VSP65-R2-O3:** a login whose session INSERT times out still answers 200 with a Set-Cookie (a claims-success shape). One line on VSP-65 or its own ticket.
- **VSP65-R2-O5:** two first boots on an empty database race (23505), at main and head alike.
- **VSP65-R2-O7:** the backup-db dump cannot be replayed into a fresh database (42P01 on serial tables) and carries `session` without its index. Pre-existing.
- **R2-O6** (the unit suite notices none of round 2's mutants; only test:db guards them) and **R2-P1** (coverage 73.80 not reproduced; round-1 line numbers): comment on VSP-65, no ticket.
- **VSP-67** (server-side timeouts) is on Kam's board as a card with the values you measured. Do not change it.

## HELD
No deploy, no production, no `az` beyond reads you already hold, no setting change, no mail to humans. Do not touch the T9 vault clone. Then WRAP (history entry + wrap mail to tuesday-agent@).

## PLAN CONFIRMATION
Mail `[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation` and proceed.

RULED BY KAM, NOT YET IN AN ARTEFACT
- vision-gh-login-for-ci = (a): Kam runs `gh auth login` himself at the mini. Until then CI is UNMEASURED; say so.
- vision-prod-postgres-idle-transaction-timeout (VSP-67): on his board, unruled; default no change.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-27: do not write to the T9 vault clone.
- 2026-09-27: VSP-65 was round 2 of 2; it passed, so the cap was not reached.

PROVENANCE:
- verdict, merge-tree, findings | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2/report.md | read 2026-09-28 02:48
- portal heads eaf024a / 0d992e0; workflows gitleaks.yml + test.yml on push to main | git ls-remote origin + /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files/.github/workflows/ | read 2026-09-28 02:48
- QuickQuote main 986f7b8, backlog branch e408904 | git ls-remote origin (hpas-quoting-tool) | read 2026-09-27 22:2x
Self-check note: two merges, both gated or hygiene; no deploy; the production deploy is Kam's and is carded after MERGED.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 02:48
