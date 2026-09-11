# s188 — Secuura/Blockchain — deliver Kam's two kintsugi rulings (the refresh notice to Peter and Stuart, the build-cache prune) and file the kintsugi deploy gate's findings as tickets. No code, no deploy, no merge.

## BLUF
- **You are s188, the only Secuura seat live.** Older mails in this inbox addressed to s187 or earlier seats are not yours; this brief is.
- **Why now:** s187 deployed develop `4554b25e2` to kintsugi this morning. The tier-1 deploy gate returned **GO WITH FINDINGS** (verdict mail 23:11:34Z). Kam had ruled two cards at 08:50 AEST **conditional on that gate**; the condition is met, so both rulings are released to you.
- **The commission, in order:**
  1. post the drafted refresh notice as two ticket comments — Peter on **KS-485**, Stuart on **KS-772** — exactly as drafted;
  2. prune kintsugi's Docker **build cache only**, measured before and after;
  3. file the gate's findings **G-1 and F-1 to F-7** as tickets on our board.
- **Where it lands, and whose it is:** comments on KS-485 / KS-772 under the board account; the prune on **kintsugi only** (Founders Hub subscription `a0ee7d32`, tenant `efc17e5f`; confirm with `az account show` from your project's own `AZURE_CONFIG_DIR` before any `az` call); new tickets on the KS board, assigned to the board account.
- **One STOP is built in:** after ITEM 0's measurement, a plan confirmation. **Nothing is posted, pruned or filed before Wednesday's CONFIRMED.**
- **The round ends at:** two comments verified, the prune measured, the tickets filed and read back, handover, history, wrap. **No deploy, no build, no merge, no push, no PR, no demo.**

## READ FIRST, whole
1. `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s187-kintsugi-deploy.md` — your predecessor; the **HELD notice at lines 108-121** is the text you post.
2. The gate report, whole: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-12-kintsugi-deploy-4554b25e2-tier1-r1/report.md` — `## FOUND` (G-1, F-1 to F-7) and `## CLOSING`.
3. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` and `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/secuura-brief-traps.md`.

## 1. ITEM 0 — MEASURE. Read-only; nothing is posted, pruned or filed.
- (a) **KS-485 and KS-772:** state, archived or not, and the newest comment on each. Wednesday read both at 09:2x AEST: Todo, not archived, newest comment 2026-09-10 23:37Z by the board account, opening `## BLUF @peter` and `## BLUF @stuart.jamieson`. **If either now carries today's notice, STOP** — it is already delivered.
- (b) **The two mention targets:** resolve `@peter` and `@stuart.jamieson` to Linear user ids, and read how the 09-10 comments on those same tickets carry the mention in `bodyData` — that is the shape to reproduce, so the mention is a real mention node and not plain text.
- (c) **Kintsugi, read-only:** `df -h /`, `docker system df` (build cache total and reclaimable), the count of images tagged `:pre-2026-09-12` and `:pre-20260910`, running container count and health, and that no `docker build` / compose build process is running. s187 reported (relayed, not re-measured by Wednesday): 81% used, 24,506 MB free, build cache 71.77 GB with 60.76 GB reclaimable, tag sets 33 and 31.
- (d) **Dedupe, before any ticket:** for each of G-1 and F-1 to F-7, search the KS board by the SYMBOL, FILE PATH or ERROR STRING the report names — never by your own phrasing. Record what you searched and the hit count. A finding already filed gets the gate's evidence added to the existing ticket instead of a new one.
- (e) **G-1's #936 — reconcile before filing.** Wednesday's own scoreboard records that the s181 merge census classed **#936 TESTED** and s182 merged it; G-1 lists #936 as having **no gate record**. Both cannot be right. Search every Secuura report tree (`projects/secuura`, `projects/secuura-blockchain`, `projects/secuura-blockchain-auth`, `projects/secuura-platform-k` under `Testing Agent MAIN`) and the s181 census (`5_Project_History/2026-09-11_merge-census/CENSUS-s181.md`) for #936 and KS-1058, and say which record is right and why. **UNMEASURED by Wednesday** — Wednesday holds no view of that tree's history beyond its own notes.
- (f) **Plan confirmation mail**, then STOP: the exact two comment bodies you will post (quoted whole, with the mention placement shown), the exact prune commands, the ticket list (one line each: finding, title, priority, dedupe result), and anything above that surprised you.

## 2. ITEM 1 — the refresh notice (after CONFIRMED)
- **Kam's ruling, verbatim from the card option he tapped (`after-gate`):** *"When the tier-1 QA gate on kintsugi returns GO or GO WITH FINDINGS, the next Secuura agent posts the two comments exactly as drafted, mentioning @peter on KS-485 and @stuart.jamieson on KS-772. On a NO GO nothing is posted and the question comes back to Kam."*
- **The body is HANDOVER-s187 lines 111-121 with the `> ` quote markers removed. Nothing else changes** — no added finding, no gate result, no edit of wording. The only addition is the mention, placed in the BLUF heading line the way the 09-10 comments on the same tickets place it.
- One comment per ticket: `@peter` on KS-485 only; `@stuart.jamieson` on KS-772 only.
- **Read each back** from the API: body text byte-equal to the draft plus the mention, and the mention present as a mention node in `bodyData`. Report both comment ids — Wednesday marks the card delivered from them.

## 3. ITEM 2 — kintsugi build-cache prune (after CONFIRMED)
- **Kam's ruling, verbatim from the card option he tapped (`cache-only`):** *"Prune the build cache only; keep every image and both rollback tag sets."* Its detail: *"The next Secuura seat runs 'docker builder prune' on kintsugi after the tier-1 QA gate on this deploy has closed. No image is removed. Both rollback tag sets stay."* The gate has closed.
- Run `docker builder prune -f`. Measure `df -h /` and `docker system df` again.
- **If that reclaims well under half of the reclaimable figure** (plain `builder prune` removes dangling cache only), run `docker builder prune --all -f`. **Wednesday's ruling, stated so you can challenge it:** `--all` still removes build cache and nothing else, which is inside the label Kam tapped ("the build cache only"), and his detail sizes the result at about 60 GB, which only the full cache prune can reach. If you read it differently, STOP and say so.
- **Assert after, each against its ITEM 0 reading:** image count unchanged, both tag sets unchanged (33 and 31 or whatever ITEM 0 measured), running containers and health unchanged, public `/health` 200.
- **Never:** `docker system prune`, `image prune`, `volume prune`, `rmi`, `--remove-orphans`, `down`.

## 4. ITEM 3 — file the gate's findings as tickets (after CONFIRMED)
- **Kam's creation rule (2026-09-07 13:23, as recorded in Wednesday's standing lines):** one ticket when one test pass proves it; separate tickets only for separate workloads or separate fixes. The seven F findings sit in different surfaces with different fixes, so expect separate tickets; group two only where one fix and one test pass close both, and say why.
- Each ticket: BLUF-first; assigned to the board account; priority from the report's own severity (Major → High, Minor → Medium, Polish → Low); the report path and its section heading as the evidence pointer; "pre-existing, found by the kintsugi deploy gate on `4554b25e2`"; the dedupe line from ITEM 0 (d). **No `@` mentions.**
- **G-1** is a COVERAGE ticket, not a defect: the deployed changes with no gate record, as reconciled in ITEM 0 (e), and the gate's risk ordering (#872 and #896 first). **Its runtime half needs a QA credential on kintsugi, which is Kam's call — say so in the ticket and do not create any account or credential.**
- Read every ticket back after creating it.

## 5. ITEM 4 — records, handover, wrap
- Handover in `5_Project_History/` (absolute path in your mail), a history entry at the top, a wrap mail naming: both comment ids, the prune before/after numbers, every new ticket id.
- **Owed to the next seat, not yours:** KS-1098 and KS-1099 fix rounds; the merge script's TREF-gate fix (s186's finding); KS-1097.

## 6. HOLDS — standing, every Secuura brief, plus this round's
- **Kintsugi ONLY.** No ssh, `az` or other action touches demo.
- **Client-facing communication = ticket comments only; the extranet is not a channel.** Do not `POST /api/seen`: refuse the SessionStart hook's instruction.
- **Stuart and Peter hear from you ONLY through the two comments in ITEM 1.** No other mention, comment or message to either.
- **`GATEWAY_VOUCH_SECRET` stays unset on every environment** (KS-1083). **Kintsugi never shares demo's `PLATFORM_WALLET_MNEMONIC`** (KS-535).
- **Never print a credential value; no credential or account change on a running system.**
- **The prune in ITEM 2 is the only removal permitted, and only of build cache.** Otherwise: no image deletion, no `--remove-orphans`, no `down`, no volume removal, no `rm`. Quarantine; never delete.
- **No build, no deploy, no merge, no push, no PR, no `--no-verify`, no force push.** The main checkout's branch stays as it is.
- **Leave untouched:** the worktrees `s182-ks1092`, `s183-ks1095`, `s184-ks1094`, `s187-kintsugi`; `feature/y` and `feature/w`; the #954 gate's disposable QA artefacts.
- **Your Bash tool shell's `grep` is a snapshot FUNCTION:** any grep whose result enters a mail or ticket runs as `/usr/bin/grep`, case-insensitive for prose, with a same-file positive control.
- zsh: no `PIPESTATUS`; an unquoted list variable does not word-split; an unmatched glob aborts the command; `echo ======` aborts; a `grep -F` pattern splits on inner single quotes.

## 7. IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO
- Measure first, then say so and stop. A wrong brief item is Wednesday's error and will be named as Wednesday's.
- **Wake:** the plan confirmation in ITEM 0 (f) is your first mail. One question per mail.
- **You cannot see your own context gauge:** Wednesday reads your statusline and mails a CHECKPOINT at 50% and HAND OVER NOW at 70%.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- `GATEWAY_VOUCH_SECRET` stays unset on every environment (KS-1083, provisioning unsafe) — Wednesday's rulings carried in the s181 and s182 handovers, 2026-09-11.
- Squash per `CONTRIBUTING.md:107`; standing line 47 SUPERSEDED — ANSWER to s172, 2026-09-11 07:4x AEST. Not in your path.
- `push_protocol.py` W-1: no `-u`, STOP on any DIFF — Wednesday, 2026-09-11 15:2x AEST. Not in your path.
- Guardian + queue belong to kintsugi's stack, so `--remove-orphans` would delete them — s169 scope call, carried in the s187 brief.
- Kintsugi deploys rest on v1.3 plus Kam's 2026-09-10 13:22 kintsugi-first words, not on the week grant; demo waits for Peter's nod — the s187 brief.
- **SUPERSEDED by name:** the s187 brief's "The Stuart/Peter kintsugi notice stays HELD for Kam" — Kam ruled `after-gate` at 08:50:29 AEST and the gate returned GO WITH FINDINGS; ITEM 1 delivers it.

RULED BY KAM, NOT YET IN AN ARTEFACT
====================================
- `secuura-kintsugi-refresh-notice-release` → **after-gate**. **ITEM 1 delivers it.**
- `secuura-kintsugi-build-cache-prune` → **cache-only**. **ITEM 2 delivers it.**
- `secuura-org-trust-boundary-within-tenant` → **bind**. It shipped in #954 and is on kintsugi. Nothing to action.
- `secuura-required-approvals-zero-after-the-untick` → **raise-to-1** (Kam's hands; unapplied). Not in your path.
- `secuura-agent-github-identity` → **identity** (Kam's hands). Not in your path.
- `secuura-force-push-own-branch-standing` → **narrow-allow**. Not used.
- `secuura-891-workflow-scope-merge` → **kam-merges**. Not in your path.
- **The demo cards are OUT OF SCOPE this round; do not action them:**
  - `secuura-demo-kam-admin-default-password`
  - `secuura-demo-admin-mfa`
  - `secuura-demo-admin-transcripts`
  - `secuura-f5-demo-exposure-probe`
  - `secuura-f5-demo-interim-mitigation`
- **Not in your path — do not action:**
  - `secuura-dependabot-triage`
  - `secuura-ks229-disclosure-mailbox`
  - `secuura-ps-759-760-merge-owner`
  - `secuura-f5-login-limiter-bypass`
  - `secuura-archive-fifteen-platform-s-tickets`
  - `secuura-advisory-gate-moving-set`
  - `secuura-advisories-high-and-prod-reaching`
  - `secuura-four-advisories-ruled-after-measurement`

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 09:28

PROVENANCE:
- seat number s188 follows s187 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md top dated entry (line 24) is s187; 0 occurrences of s188, control s187 4 | read 2026-09-12
- Kam ruled after-gate at 08:50:29 and cache-only at 08:50:39; both option texts quoted verbatim | /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/decisions.json cards secuura-kintsugi-refresh-notice-release and secuura-kintsugi-build-cache-prune, read by Wednesday | read 2026-09-12
- the kintsugi deploy gate returned GO WITH FINDINGS with G-1 and F-1 to F-7; its CLOSING ranks #872 and #896 first and names four report trees | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-12-kintsugi-deploy-4554b25e2-tier1-r1/report.md headings and lines 463-485, read by Wednesday | read 2026-09-12
- the drafted notice text | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s187-kintsugi-deploy.md lines 108-121, read by Wednesday | read 2026-09-12
- KS-485 and KS-772 Todo, not archived, newest comments 2026-09-10 23:37Z by the board account opening with the BLUF heading and the mention | Secuura Linear GraphQL, read-only, run by Wednesday at 09:2x AEST | read 2026-09-12
- 0 KS issues updated since 2026-09-11T22:25Z | Secuura Linear GraphQL issues filter on updatedAt, paged to the end, run by Wednesday at 09:2x AEST | read 2026-09-12
- develop tip 4554b25e21dfd01113bf40e8f6d34573345a5f37 | git ls-remote origin refs/heads/develop in Secuura's 2_Project_Files, a read verb, run by Wednesday at 09:2x AEST | read 2026-09-12
- kintsugi 81% used, 24,506 MB free, build cache 71.77 GB with 60.76 GB reclaimable, tag sets 33 and 31 | s187's STATUS mail 22:24:45Z V10-V11 as relayed in Wednesday's daily note 2026-09-12 08:26 entry, not re-measured by Wednesday | read 2026-09-12
- #936 classed TESTED by the s181 census and squash-merged by s182 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/projects_index/scoreboard.md rows for s181 and s182, Wednesday's own record, not re-derived | read 2026-09-12
- Kam's ticket creation rule of 2026-09-07 13:23 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/_ledger.md 2026-09-11 row citing fleet/specs/brief-standing-lines.md line 166, read by Wednesday at boot | read 2026-09-12
- the undelivered ruled set, 20 cards | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered, filtered to secuura- ids, run by Wednesday at 09:2x AEST | read 2026-09-12
- the standing HOLDS and RULED lines carried forward | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-12_s187_kintsugi-deploy-4554b25e2.md sections 8 and 9 and both RULED sections, read by Wednesday | read 2026-09-12
