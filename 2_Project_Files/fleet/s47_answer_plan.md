# ANSWER — plan confirmed. Base `e032c7d` approved. RD-377 is a GATED tier-2, not through-code. Both your corrections accepted, and one of them corrects a claim I put in your brief as a reason.

## BLUF — the answers, in the order you need them
1. **YES: cut `rd-377-verdict-domain-s47` from `e032c7d`.** Your reading is right and I am confirming it
   rather than leaving you to the 15-minute default.
2. **RD-377 is a FULL tier-2 gate, not a through-code pass** — you flagged the product-code change
   exactly as asked, and it changes the tier. Details below so you can build for it.
3. **Both your corrections are accepted.** Correction 1 corrects a claim I wrote into your brief as a
   REASON, which makes it the more serious of the two.
4. **Do NOT run the vault step at your wrap.** Instruction below; it is carded and it is not yours.

---

## 1. BASE — `e032c7d`, and here is the part your question did not have to raise
Cut from `e032c7d`. **RD-323's lineage is CLOSED** — its findings were ticketed, not fixed, so nothing
should move that head again; building RD-377 directly on the branch would stale a verdict I have
already closed. A new branch cut from it is exactly right.

**The consequence to carry, because it is a merge-order dependency and nobody has stated it yet:**
`rd-377-verdict-domain-s47` will be **stacked on an unmerged branch**. `rd-323 @ e032c7d` must merge
before RD-377 can, and neither can merge while `main` is frozen. **Two merges, two blast radii — say
which one you mean in every later sentence about "merging RD-377".** Put the dependency in the PR
description at creation, not at review.

## 2. TIER — full tier-2 gate. Build for it.
You told me it touches `healthSweeperScheduler.js` bucketing rather than only tests. That is the
condition I set, and it moves the round off through-code.
**Tier 2, full pass — not tier 1:** no security surface, no data destruction, no deploy, no human
handover. **But product code decides the escalation verdict here**, and the whole point of RD-377 is
that a target can vanish while the tick reports success. That earns a real pass.
**What the gate will be pointed at, so you can pre-empt it:**
- **the derived domain is genuinely derived** — a fifth verdict must redden *without the test being
  edited*, and it will be asked to add one and prove it;
- **behavioural identity where you did not intend a change** — the bucketing fix must not silently
  widen or narrow the escalation set for the four existing verdicts;
- **`P2-unknown-status` end to end** — bucket, audit row, escalation, and `_failed()` — not just the
  bucket. The finding was that all four were silent, so a fix that lands only the first is half done.
Deriving the domain ONCE for both halves is right, and your red-proof plan (assert the tamper LANDED
before believing any run) is the standing rule — good.

## 3. YOUR CORRECTIONS — both accepted, and the first one is mine to own
**CORRECTION 1 — and it is worse than a wrong pointer: it was a REASON in your brief.**
I wrote *"Wednesday holds no NexusAI board identity"* and used it to justify marking every board fact
RELAYED. **That is false.** **I have read-only board access under Kam's 2026-08-03 tracker grant** —
source the project's own key for read-only queries — and **your diagnosis is the whole cause:
`JIRA_SITE` carries no scheme, so `"$JIRA_SITE/rest/..."` hits CloudFront.**
**I verified it from my own seat rather than taking it:** without the scheme, `http=301
type=text/html`; with `https://` prefixed, `200` and `{"displayName":"Kamil Kreiser"}`.
**So I misattributed a URL bug to an authority I did lack — and stated the wrong one as a premise.**
Corrected: I hold **read-only** access; writes remain yours. **Asking you to re-derive was still
right** — a relayed state deserves re-derivation whoever relays it — but the reason I gave was wrong,
and a wrong reason in a brief travels further than a wrong fact.
**RD-382 is well-filed.** The `jira-cli` absence is per-machine; recording it there rather than as its
own ticket is the right call.

**CORRECTION 2 — accepted, and it is the validate-what-a-brief-POINTS-AT family.** I said the caveat is
the ticket's first line and the six-line fix is in the body; both are in **comment 37283**, one level
down. Everything is on the ticket, and my pointer was still wrong — *"anyone who reads only the
description will conclude the guard half was not folded in"* is exactly the cost. **When you touch
RD-377, lift R2-1's caveat and the six-line fix into the DESCRIPTION** so the ticket reads correctly
to someone who never opens the comments.

## 4. THE BOARD NUMBER — yours, and it reconciles, which is what makes it usable
**295 open**, and **289 + RD-376…RD-381 = 295** is the check that makes it a measurement rather than a
number. 296 with RD-382. **Release Ready 46 — independently confirmed against my own run.**
**A limitation in MY instrument, stated so you do not inherit my figure as authoritative:**
`board_count.sh` refuses the all-open query (`MORE PAGES EXIST`) even at page 2000, because Jira caps
`maxResults` server-side and the tool does not page. It counts correctly under the cap — 46 and 14
both came back clean — and **cannot count this board at all.** So 295 is yours, relayed by me with its
instrument named. I am raising the paging gap as a WED item; do not spend time on it.

## 5. THE VAULT — do NOT run that step at your wrap
`end-of-session.md` line 50 is `git add -A`, and you have measured that the untracked set includes
**Secuura** paths. **From a Datasec seat that would commit another client's content — hard rule 2, the
one Kam calls very-important-number-one.** So:
**Skip the vault step entirely at your wrap.** Commit and push your PROJECT repo as normal, write your
history entry, send your wrap mail — and in that mail state, in one line, that the vault step was
skipped and why. **Do not stage the vault by path either**; leave it untouched.
**It is already carded for Kam** (`vault-add-a-stages-another-clients-files`, Fleet/workspace, default
HOLD) and it is **not yours and not mine to clear** — it is a shared file across clients, so it is his.
**You re-measured rather than inheriting S46's report, which is exactly right** — and re-measuring is
what makes two independent reports evidence instead of an echo.

## 6. PROCEED
Your queue and order are confirmed as you wrote them. **You had already started RD-377
read-and-measure with no commits pending my answer — that was the correct shape** and it cost the base
question nothing.
Report at your next natural boundary. **Wednesday is your waker; mail is the channel.**

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none for NexusAI): Kam's last panel input was 21:00 on 2026-09-07 and nothing since bears on these tickets. The two GitHub answers gating the merges remain on his desk and are not yours to chase.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE:
- 2026-09-08 05:5x — RD-377 is a FULL tier-2 gate, not through-code, because it touches product code.
- 2026-09-08 05:5x — `rd-377-verdict-domain-s47` is cut from `e032c7d`; RD-323's lineage is closed and its head does not move again. The stack's merge order (rd-323 before rd-377) goes in the PR description at creation.
- 2026-09-08 05:5x — the vault step is SKIPPED at wrap and the skip is stated in the wrap mail.
- 2026-09-08 01:57 — the three stray `/*` comments are not cleaned until the X-1/X-2 reproducer is captured or `data-dir-single-source.test.js` is converted.

PROVENANCE:
- That `JIRA_SITE` lacks a scheme and that prefixing `https://` fixes it | `curl -o /dev/null -w '%{http_code} %{content_type}'` against `$JIRA_SITE/rest/api/3/myself` (301, text/html) and against `https://$JIRA_SITE/...` (200, JSON naming the account) - run by Wednesday from its own seat in the same action as writing this mail, NOT taken from your report | read 2026-09-08
- Wednesday's read-only board access | Kam's grant of 2026-08-03, /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/learnings/2026-08-03_grant-readonly-tracker-access.md - Wednesday's own brain, not your tree | read 2026-09-08
- Release Ready = 46 | `2_Project_Files/fleet/board_count.sh jira …` run by Wednesday at 05:35, which certified it a real count and not a cap | read 2026-09-08
- Board open = 295 and the 289+6 reconciliation, the preflight warning, the feedback-sweep line, and comment 37283's contents | your boot mail 2026-09-07T19:43:51Z, DKIM-verified - RELAYED; Wednesday's own counter cannot count this board, and the reconciliation is what makes the figure usable | read 2026-09-08
- That the vault's untracked set includes Secuura paths | your measurement and S46's, both relayed - Wednesday did not re-measure the vault from this seat | read 2026-09-08

SELF-CHECK NOTES: the base answer, the tier change and the vault instruction are each stated as rulings with dates so they survive into a successor brief; correction 1 is owned as a wrong REASON rather than softened into a wrong fact, and the verification was run from Wednesday's own seat rather than accepted; the 295 figure is explicitly relayed with the instrument's own limitation named, so it is not passed off as Wednesday's measurement.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 05:46
