# Datasec/NexusAI — S49 brief

## BLUF

**Three of Kam's rulings on this project were undelivered when this brief was started. ONE of them is your first queue item; one turned out to be already done; one is Kam's own to close.** Everything below is inside work he has already ruled or inside the marketplace readiness set S48 measured. **Nothing here is a deploy.**

**Boot from a CLEAN WORKTREE at `origin/main`, not from `2_Project_Files/`.** That tree is a stale snapshot — S48 measured 33 tracked files on disk not matching `cd2b543`, the diff being a reversion of `+248 / −1230`. The card `nexusai-main-tree-is-a-stale-snapshot` is OPEN with Kam's default standing: *the stale tree stays, the agent works from its own worktree, the mechanism stays unexplained.* **Do not "fix" that tree. Do not commit from it.**

---

## RULED BY KAM, NOT YET IN AN ARTEFACT

Built from `decision_queue.sh list ruled --undelivered` for this project, read at the timestamp in SELF-CHECK. **Three cards. Each ruling is quoted; each names the artefact it must land in.**

**1. `nexusai-rd369-round3-or-ship-at-the-cap` → `round3`, ruled 2026-09-09T12:09:48+10:00.** His words as the option reads: *"Authorise ONE round 3, narrow — the window and the certifying cell only. Remove the window from BOTH paths and make the certifying cell able to fail."*
→ **Lands in:** the RD-369 guard code and its test, plus a comment on RD-369 naming this as the authorised round 3.
🔴 **He was offered `wider` — round 3 PLUS removing the RD-385 files from the image — and he did NOT take it.** So **removing those files is OUT OF SCOPE for this session.** Detecting them is in scope; deleting them is not. If you think that is wrong, say so and stop — do not act on the reading.

**2. `nexusai-three-lineages-in-scope-or-parked` → `close-superseded`, ruled 2026-09-08T10:07:29+10:00 — ✅ ALREADY DELIVERED, and this is stated because Wednesday nearly commissioned it again.**
**PROVENANCE:** RD-163, RD-201, RD-304, RD-306 — all four read **`[Done]`** live over the Jira REST API from Wednesday's seat, **2026-09-10 09:2x**, resolved **2026-09-08T10:08-10:09**, one minute after the ruling. **The board write happened two days ago; only the CARD was never marked.** Wednesday marked it delivered at 09:23 today.
🔴 **Wednesday had this in the queue as work for you.** The `send_brief` freshness gate refused the brief and made Wednesday read the tickets. **Do not close them again. Nothing is owed here.**

**3. `rd104-gh-identity-acceptance-false-premise` → `youcheck`, ruled 2026-09-07T19:58:59+10:00.** Kam took the option to read two GitHub settings pages himself (`environments`, and `variables/actions` for `CI_DEPLOY_ENABLED`) because the project's `gh` identity cannot reach the `datasecau` org at all.
→ **UNMEASURED BY WEDNESDAY: whether he has answered.** Wednesday holds no GitHub identity for this org and cannot check. **The instrument that closes it is Kam.** Until those two answers exist, **the deploy question stays open — which costs you nothing this session, because nothing here deploys.**

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- **The QA gate precedes every score and every merge** (Kam, 2026-09-01; tiered 2026-09-05). Items 1 and 2 touch security surfaces → **tier 1**. Item 3 is a docs correction → **through-code only**.
- **A GO names a HEAD.** If you push after a gate verdict, that verdict is stale and the re-gate is part of accepting the fix, not a surprise afterwards.
- **Client-facing communication is ticket comments only.** Nobody messages a human outside the team.
- **Cleanup means quarantine, never deletion.**

---

## QUEUE — in this order. Each item carries its ticket's own scope sentence.

### 1. RD-369 round 3 — the guard, narrow (Kam-authorised above)
PROVENANCE:
- RD-369 state (**`Release Ready`**, 1 comment, last comment **2026-09-08T10:24**, updated 2026-09-08T11:53) | Jira ticket RD-369 | read 2026-09-10
- RD-369 has no comment after Kam's 2026-09-09T12:09 ruling, so no seat has acted on round 3 | Jira ticket RD-369 comments endpoint | read 2026-09-10
- Only `rd-369-round2-s47` @ c96837df931af020bd700b53fd3719f47f27cb22 and `rd-369-recut-s47` @ 117931ef4a5b8da635d4c4d2207227136c483138 exist at origin; there is no round-3 branch | git ls-remote origin | read 2026-09-10
**Ticket scope, quoted:** the exposure itself is CLOSED and proven against a real built image (288 derived vs 288 admitted, all four carrier paths 404 from a running container). **This round is about the GUARD that prevents recurrence, and nothing else.**
The gate's finding: the builder found a distance window that made the instrument answer clean, **removed it from one code path and left it on the other, while the docblock says there is no window.** Proven consequence: a **purely cosmetic reflow** — one line broken after its colon, every value preserved — flips **three of four** true RD-385 files from carrier to CLEAN. And the certifying cell asserts only *greater than zero* over 284 files, so mutation-killing either detection path leaves it GREEN.
**Do:** remove the window from **both** paths; make the certifying cell **able to fail** (red-proof it by mutation, with a green baseline either side).
**This is the last round either way** — Kam's cap. No round 4 without him.

### 2. RD-363 — merge the Key Vault purge-protection branch
PROVENANCE:
- RD-363 state (**`Testing`**, High, labels `blocker, horizon-1, security`, updated **2026-09-07T17:50**) | Jira ticket RD-363 | read 2026-09-10
- Branch `rd-363-keyvault-purge-protection-s43` @ `b0dec96fc1f498b309cee692b6441ed9e9b0b043` | `git ls-remote`, read 2026-09-10
🔴 **THE TICKET IS WIDER THAN THIS MERGE AND THIS IS A NARROWING, stated so the ticket does not close on a fraction.**
**Ticket scope, quoted verbatim:** *"SEC-07/08/11 — Marketplace deployment template hardening: Key Vault has no purge protection while holding the DEK wrapping key, storage has no network ACL and uses shared-key access, and the image is built with `npm install` rather than `npm ci`."* **Three legs.** [Testing], High, labels `blocker, horizon-1, security`.
The branch `origin/rd-363-keyvault-purge-protection-s43` at **`b0dec96fc1f498b309cee692b6441ed9e9b0b043`** (confirmed at origin by `ls-remote` from Wednesday's seat, 1 commit, template + one new test) closes **the Key Vault leg only.**
**Why it matters:** `main`'s `azure-marketplace/combined/mainTemplate.json:386-387` today has `enableSoftDelete: true`, `softDeleteRetentionInDays: 7` and **no `enablePurgeProtection`** — so the zip built from `main` ships a Key Vault holding the RSA key that wraps the customer's DEK, **destroyable permanently by any Contributor after 7 days, with no backup.**
**Do:** forward-merge (the branch is based on an older main — **not** a fast-forward), tier-1 gate, then merge on Wednesday's GO. **Then say explicitly which of the three legs remain open and either sub-issue them or leave RD-363 open — do not close it on one leg.**

### 3. `PRIVACY.md:21` — stop declaring another company's privacy policy
**Measured by S48 at `cd2b543`:** the published privacy URL in the repo is `https://help.hpauthsuite.com/support/solutions/articles/47001217571-hp-privacy-statement` — **HP's privacy statement, for a different product** — while four lines above, the same document names **Datasec Solutions Pty Ltd** as the data controller. `privacy.datasec.com.au/nexusai` is **NXDOMAIN**; `datasec.com.au/privacy` is **404**.
**Do:** remove the HP URL. **Do NOT invent a replacement URL** — standing up the domain and the page is Kam's, and a listing field pointing at a host that does not resolve is not an improvement on one that resolves wrongly. **Leave it explicitly marked as pending with a ticket reference, and say in your wrap what the replacement needs.**

---

## HOLDS

1. **No deploy. No `az` write of any kind.** Nothing in this queue deploys, and the deploy precondition (RD-104's two GitHub settings) is still unanswered by the only person who can see it.
2. **No removal of the RD-385 files** — Kam was offered that and chose the narrower option. Detection only.
3. **Do not touch `2_Project_Files/` as a working tree.** Clean worktree from `origin/main`, and say in your first mail which path you cut and at which SHA.
4. **Signature classes unchanged:** production, money, external communication to any human, anything irreversible. **A production change would be flagged to Kam before or immediately after — but there is none in this queue.**
5. **`docker` is installed on this machine and the daemon was DOWN at brief time** (Docker Desktop launch was requested at 09:2x, unverified). **If an item needs a built image, measure the daemon first and say so — do not report an ignore-file read as an image-level fact.** That distinction is RD-369's entire finding.
6. **Quarantine, never delete.** Nothing is `rm`'d.

## WHAT WEDNESDAY HAS NOT MEASURED, AND THE INSTRUMENT THAT CLOSES EACH

- **Whether Kam has answered RD-104's two pages.** Instrument: Kam. Not you, not Wednesday — the project `gh` identity 404s on the org itself.
- **Whether RD-367 ("247 commits have never reached main") still holds.** It was filed 2026-09-07; the trunk was unfrozen 2026-09-08 and `main` is now `cd2b543` with `HEAD == origin/main` and **zero commits ahead** (read from the repo by Wednesday, read-only, at brief time). **It looks stale. It is NOT in your queue — but if you have a spare cycle, re-derive it and comment, rather than leaving a High ticket asserting something that has probably resolved.**
- **The three RD-363 legs other than Key Vault.** Instrument: the branch diff and the template. Yours to read.

## PROVENANCE: every fact above, and where it came from

- Board facts (RD-363 `[Testing] High labels=[blocker,horizon-1,security]`, RD-385 `[To Do] High`, RD-367 `[To Do] High`, RD-372 `[To Do] High`, RD To Do = **117 paged to `isLast`, not a cap**): **read live over the Jira REST API from Wednesday's seat at brief time**, under Kam's 2026-08-03 read-only tracker grant.
- `b0dec96fc1f498b309cee692b6441ed9e9b0b043`: **`git ls-remote origin 'refs/heads/rd-363*'`, read verb, run at brief time.**
- `main = cd2b543`, `HEAD == origin/main`, 0 commits ahead, and the worktree list: **`git log` / `rev-list` / `worktree list` — read verbs only, no write verb was run in your checkout.**
- Template line numbers, the HP privacy URL, the `Dockerfile:79` COPY and the four `docs/` files: **quoted from `NexusAI/MARKETPLACE-READINESS-2026-09-09.md` (S48, measured in worktree `wt-s48-mkt` at `cd2b543`) — S48's read, NOT re-derived by Wednesday.** Treat them as relayed and re-derive before acting.
- The three rulings: **`decision_queue.sh show <id>`, quoted from the card, at brief time.**
- 🔴 **Wednesday holds no GitHub identity for `datasecau` and no Docker daemon reading. Every claim about the org's settings or about image CONTENTS in this brief is second-hand or absent, and is labelled as such above.**

## SELF-CHECK: re-read end-to-end for contradictions | 2026-09-10 09:25

- Read against Kam's rulings for today: **`kam_rulings_today.sh` returned 0 messages for 2026-09-10** — and Wednesday has separately measured that his 08:58 message never entered the store the tool reads, so **that zero is a known-weak instrument, not a clean absence.** No ruling of his from today is in this brief because none is visible; if he ruled on NexusAI today it is not here.
- Read against the previous outbound to this project: **the S48 commission (analysis only, no changes).** This brief SUPERSEDES nothing in it — S48 was read-only by design and this is the first brief that commissions changes from its findings.
- Every ticket id in the QUEUE was read live in the same action as writing this brief.
- **Narrowings stated:** RD-363 (one leg of three) · RD-369 (guard only, not the exposure, not the file removal).
- 🔴 **A queue item was REMOVED after the gate refused this brief.** The first draft commissioned closing RD-163/201/RD-304/RD-306. **They have been `Done` since 2026-09-08.** Wednesday had read the RULING and not the TICKETS. The gate caught it; recording it here so you can see what the brief nearly cost you.
