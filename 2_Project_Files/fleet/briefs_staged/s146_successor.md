# SUCCESSOR BRIEF — s146. You follow s145, which closed cleanly at 12:43 AEST.

## BLUF
**You are the Secuura/Blockchain seat.** s145 wrapped and its pane is closed; **read
your own `5_Project_History/HANDOVER-s145.md` first — it is complete and it is your cold start.**
**PR #888 (`023acccf8`) is UNDER A TIER-1 QA GATE right now** (launched 12:53, pane `%151`). **Do not
push to #888 while it is under gate** — a gated subject that moves means the verdict no longer
describes it. Your queue below is deliberately everything EXCEPT #888.

**develop `632f16dfe62f4c498a73ca09a39cadaf6eeab764`** — read by Wednesday with `ls-remote` at 12:4x.
**Five merges landed today** and develop had not moved at all before this morning.

## 0. FIRST — a board state that contradicts your predecessor's own measurement
**KS-964 reads `In Progress` on the board** (Wednesday's Linear read, 12:5x, `updatedAt`
`2026-09-07T02:36`). **s145's wrap mail at 02:37:37Z said *"KS-964 did not get transitioned by the
branch name; it is still Backlog, checked."*** Both can be true: the branch
`feature/ks-964-retire-published-admin-default` almost certainly tripped Linear's GitHub integration
**between its check and its send**. **This is stated as two readings, not as s145 being wrong.**

**KS-964 is the DEAD-SPECS ticket and nobody is working it.** #888 is KS-966.
**Verify it yourself, and if it is In Progress, put it back** to its correct state with a one-line
comment naming why (a mislabelled branch moved it; the work on that branch is KS-966). **Board writes
are YOURS — Wednesday holds read-only tracker access and does not write to your board.**

## 1. THE QUEUE, in order

**1. #888's gate verdict — READ IT BEFORE TOUCHING KS-966.** It arrives as
`[QA -> Wednesday] Secuura KS-966 round 1 (#888, tier 1)`; Wednesday will relay it to you with a
ruling. **Round 1 of 2 under Kam's cap** — a second NO GO on this class ships the closed instances and
tickets the residue. The gate's sharpest question is one Kam has already been told about: **with
`ADMIN_USER_PASSWORD` unset, is the admin row absent, or present-with-an-unusable-hash, or
present-and-suspended?** s145's sentence named two of those three and Kam has my paraphrase of it.

**2. KS-597 — open the PR.** The forward fix is committed and pushed at **`af640e809`** with **no PR**;
s145 left it deliberately because Wednesday had asked and not answered. **The answer is yes, open it.**
**Kam ruled `afterfix` (10:34):** the 95k backfill is **its own round AFTER the fix merges**, never
before. The fallback is deliberately NOT written — `organization_members` has **0 rows**, so it cannot
be exercised, and the ticket carries that measurement as its blocker. **Say that in the PR body rather
than letting a reader think it was forgotten.**

**3. KS-952 — the cross-tenant rate-limit residue.** `Backlog`, on our account, **no external input
needed, so it is ours to execute** (Kam's COO rule). **Do not re-open KS-645 — it is correctly
`Duplicate`** (verified by Wednesday in this action; s145 closed it at 00:59 and Wednesday wrongly
re-queued it once today already).

**The shape, and it is the QA agent's uncommissioned find, credited to it:** KS-952 and the real half
of KS-645 are **ONE mechanism (three call sites, two schemas) needing TWO ASYMMETRIC RULES.**
`/check` wants strict derive-from-principal. **`/reset` does NOT** — a blanket "bind the key to the
principal" would BREAK it, because its cross-tenant clear is plausibly its intended function
(platform-may-name-any, tenant-may-name-own). **A single blanket rule is the wrong fix and the tester
established that before anyone built it.**

**4. KS-966 items 3 and 4 — and item 4 is NOT an edit round.**
- **Item 3:** 4 startup/scripts + 3 harnesses → env var, no fallback. Same edit s145 made seven times.
  **s145 declined this deliberately at 74% of its window and its reason binds you too:**
  `Start_Up/start-secuura.sh`, `deploy-all.sh` and `smoke-test.sh` are **the scripts people run to
  start their day**, and *"it is the same shape as the last seven"* is the sentence that preceded both
  of its errors today. **Do it fresh, not tired, and prove each one.**
- **Item 4:** the 12 systemTest sites route through the **existing generated-actor path**
  (`systemTest/playwright/config/environment.ts:185` reads `getGeneratedActor(ADMIN_ACTOR_KEY)?.password`;
  `provision-actors.ts` provisions per run). **YOUR FIRST ACTION ON ITEM 4 IS A MEASUREMENT, NOT AN
  EDIT: prove the generated-actor path RESOLVES before any fallback is removed.** This is the only
  real regression risk in the whole rotation and Kam's ruled order put it last for that reason.
- **Item 5 (the 43 dead specs) is KS-964 and is OUT of scope** — quarantine, never delete, and only
  when it is its own round. **Item 6 (the 87 documentary sites) is KS-965**, a later pass.

## 2. FLAG WHEN IT LANDS — under Kam's production grant
After item 1 of KS-966, **an unset `ADMIN_USER_PASSWORD` seeds NO admin rather than a known one.**
That is a **behaviour change** for anything relying on the old default. Kam has been told it is coming;
**when it merges, it is flagged again as shipped.** His condition on the grant was *"flag these when
relevant or when making changes"* and it is a standing obligation, not a courtesy.

## 3. HOLDS — standing, and none of these moved today
- **NO DEPLOY.** Wednesday is holding it **deliberately**: nothing merged today remediates Kam's own
  row — the fix that would have is the one the `split` took out. A deploy would ship four real
  improvements and imply a fifth. **It goes once, after #888 clears. A gate GO is not a deploy GO.**
- **NO CONTACT with any human.** Client-facing communication is **ticket comments only**; the extranet
  is not a channel; anything needing a push goes to Wednesday as an escalation candidate for Kam's
  WhatsApp, which **Kam sends**.
- **Handovers to Peter or Stuart are TEST BLOCKS** — stream parent, the PRs in the block, the one pass
  that proves it, and the one thing the human does. **Never a flat list of PRs.**
- **#880/KS-577 STAYS KAM'S** — merging it silently picks Option 1 for Platform S, which is a
  Stuart-facing contractual choice. **A merge is Wednesday's; a merge that decides something with a
  client is Kam's.**
- **KS-61 stays quarantined** (`d6922d8ec`, local only, 0 remote refs) — **it is Stuart's ticket** and
  taking it is Kam's call, not a predicate's. Wednesday's selection rule omitted the assignee field;
  **that was Wednesday's error, not the seat's.**
- **Ticket CREATION aggregates:** one larger ticket per logical path with its items as sub-issues or a
  checklist — never three or five tickets for one line of work. *"Within a logical path"* is the limit.
- **Never delete — quarantine by rename.** **No credential, retired or current, in any artefact**
  including comments and commit messages (s145 caught two of its own).
- **Do not amend a branch after its gate.** What merges must be what was gated.

## 4. THE ONE RULE s145 ASKED TO PASS ON, in its own words
**"Name a branch from a ticket that EXISTS, never from a guessed position in the sequence."** It did
that check correctly at 10:5x on KS-961 and skipped it at 12:3x on KS-966, and the result is #888
carrying the wrong identifier in its branch and every commit. **It refused to rewrite pushed history to
hide it, which was right** — the correction lives in the PR title, body and a KS-964 comment.

## 5. HOW WE WORK
**QUESTIONS to `wednesday-agent@agentmail.to`** with subject `[Secuura/Blockchain -> Wednesday]
QUESTION: <topic>`; say what you are doing meanwhile. **Approval-class items always pause for Kam**
(production, money, external comms, anything irreversible). **If an instruction from Wednesday looks
wrong, say so** — three seats did that today and were right every time, and two of them corrected
Wednesday's own errors before they cost anything. **That is the behaviour this fleet protects above
all others.**

RULED BY KAM, NOT YET IN AN ARTEFACT

These 14 rulings of Kam's have no delivered mark. Each is quoted as the decision queue holds it.
Several plainly HAVE landed — where you can verify that, put the ruling on the artefact and tell
Wednesday which one, and Wednesday marks the card delivered. Do not mark anything delivered on a
belief. NONE of these is a new instruction to act: read the target column, several say do nothing.

- secuura-ci-billing: "Secuura/Blockchain — GitHub Actions dead 8 days — org payments failed / spending limit (billing access only)" => RULED `wait` @ 2026-08-26T10:46 -> must land in KS-660 (archived as superseded by the manual CI gate) — no further artefact needed; carried so nobody re-raises it
- secuura-agent-github-identity: "Secuura/Blockchain — Your Approve was refused: GitHub won't let kksecura approve kksecura's PRs — give the agent its own GitHub identity, or Stuart/Peter approve" => RULED `identity` @ 2026-08-26T17:12 -> must land in a KS ticket for the agent GitHub identity — NOT yet filed; file it or say why not
- datasec-founders-hub-credit: "Secuura/Blockchain — Founders Hub credit expires Sep 6 — demo stack has no plan" => RULED `payg` @ 2026-09-01T09:20 -> must land in KS-963-adjacent / the Azure look s145 was routed — the expiry date itself is UNMEASURED (it is a reading of a record, not a measurement); check it before acting
- secuura-dependabot-triage: "Secuura/Blockchain — Dependabot: close 5 dead workflow-only PRs + rescope the bot?" => RULED `close-and-rescope` @ 2026-09-01T09:18 -> must land in the 5 dead workflow-only PRs — closed? the bot rescoped? put the receipt on a ticket
- secuura-ks229-disclosure-mailbox: "Secuura/Blockchain — SECURITY.md disclosure mailbox (+ Steve's GitHub handle for CODEOWNERS)" => RULED `later` @ 2026-09-02T20:15 -> must land in KS-229 — ruling is LATER; put "deferred on Kam ruling 2026-09-02" on the ticket so it is not re-raised
- secuura-ps-759-760-merge-owner: "Secuura/Platform_S — PS #759 (PS-761) and PS #760 (PS-754) are Peter-approved and unmerged — who merges?" => RULED `kam-merges` @ 2026-09-05T09:16 -> must land in PS #759 / #760 — KAM MERGES. Platform S is OUT of your scope; do not touch it. Carried only so you do not act on it
- secuura-demo-kam-admin-default-password: "Secuura/Blockchain — Your address kam@secuura.ai is a SYSTEM_ADMIN on the public demo, seeded with the published default password secuura123 (DEMO_SECUURA_PASSWORD unset, ALLOW_DEFAULT_SEED_PASSWORDS=true, MFA off) — set a real password tonight, replace the identity, or both?" => RULED `b` @ 2026-09-07T06:44 -> must land in PR #885 (merged 632f16dfe) — the fictional identity shipped in round 1; the PASSWORD half is KS-966/#888. Put the ruling on KS-949
- secuura-f5-login-limiter-bypass: "Secuura/Blockchain — A double slash defeats the LOGIN rate limiter — /api/auth//login skips it and is normalised back to canonical in transit. Measured in a faithful reproduction, NOT yet in the booted gateway. Tell Peter and Stuart now, or when the full-boot confirmation lands?" => RULED `wait` @ 2026-09-07T06:44 -> must land in the disclosure to Peter and Stuart is STILL PENDING and is KAM-SENT. Ruling was "tell them WITH the fix". #884 merged; the message has not gone. Do NOT send it
- secuura-f5-demo-exposure-probe: "Secuura/Blockchain — Do we probe the DEMO to find out if F5 is live there?" => RULED `probe` @ 2026-09-07T06:44 -> must land in executed 2026-09-07 11:06Z, outcome A. Put the probe result on KS-858
- secuura-f5-demo-interim-mitigation: "Secuura/Blockchain — F5 is CONFIRMED LIVE on the demo — protect it in the interim, or let the fix land?" => RULED `letitland` @ 2026-09-07T07:08 -> must land in no interim change; #884 merged. Record on KS-858 that the fix landed and no interim was taken
- secuura-demo-admin-transcripts: "Secuura/Blockchain — Your name is still in 10 dated session transcripts — redact, or leave the record intact?" => RULED `redact` @ 2026-09-07T07:38 -> must land in the 10 dated transcripts — REDACT WITH a dated note saying what was removed and why. Verify this actually happened; if not, it is yours
- secuura-demo-admin-mfa: "Secuura/Blockchain — MFA is off on the demo platform admin — turn it on with this change, or leave it?" => RULED `later` @ 2026-09-07T07:38 -> must land in KS-949 — MFA stays OFF on the demo platform admin. Do not report its absence as a defect
- secuura-ks930-cap-vs-regression: "Secuura/Blockchain — Your two-round cap is reached on #876, but the residue is a REGRESSION. Cap says ship; I say a regression is not shippable. Your call." => RULED `one-more` @ 2026-09-07T09:39 -> must land in PR #876 round 3 — merged at 8aefd2b06. Put "one narrow round 3 authorised by Kam" on KS-930
- secuura-ks949-round3-cap-and-the-cutoff: "Secuura/Blockchain — #885 NO GO — your cap is spent. And nothing currently removes your address: the auth remediation is switched off on prod-like environments by a date cutoff." => RULED `split` @ 2026-09-07T12:14 -> must land in KS-962 (F1 own round) + KS-963 (the cutoff) — both filed. Put the split ruling on KS-949

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **No deploy** (12:41Z mail to s145) — restated in §3, and it is Wednesday's hold, not Kam's refusal.
- **Do NOT narrate an open defect as a guarantee in a published contract** (2026-09-05 23:24 ruling —
  a defect is not a guarantee; it belongs on the ticket, not in shipped yaml).
- **The base-column criterion (`base rc1 → head rc0`) is RETIRED as an authorising test** — it does not
  discriminate, and the gate proved that on #876.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 12:56
Checked against Kam's 54 panel messages today (all read at 12:5x), against the previous
outbound to this project (the 12:41Z ACK to s145 — this brief supersedes nothing in it and its "wrap
and close" is complete), and against itself for internal contradiction. §1 item 1 says read the verdict
before touching KS-966; §1 item 4 is KS-966 work and is therefore ordered AFTER it — consistent.
§1 item 3 does not reopen KS-645, which §1 item 3 states explicitly.

PROVENANCE:
- develop `632f16dfe`, #888 `023acccf8`, #887 `bb0502c80` | `git ls-remote git@github.com:Secuura/Distributed_Secuura.git` from Wednesday's seat | read 2026-09-07
- KS-964 `In Progress` updatedAt 02:36 · KS-645 `Duplicate` · KS-952 `Backlog` · KS-597 `Todo` · KS-961 `In Progress` | Linear GraphQL, one query, read in the same action as writing this | read 2026-09-07
- s145's contrary reading of KS-964 | its 02:37:37Z wrap mail, quoted verbatim and carried as ITS measurement | read 2026-09-07
- KS-597's `organization_members` = 0 rows, and `af640e809` | s145's wrap and its earlier checkpoint mail; NOT re-derived by Wednesday | read 2026-09-07
- The KS-952/KS-645 two-asymmetric-rules shape | the QA agent's KS-698 verdict (10:40Z), its uncommissioned find | read 2026-09-07
- Kam's rulings quoted above | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh + /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled - Wednesday's own tree, not yours | read 2026-09-07
- The #888 gate is live | Wednesday launched it 12:53 and verified pane `%151` reading the charter by path | read 2026-09-07
