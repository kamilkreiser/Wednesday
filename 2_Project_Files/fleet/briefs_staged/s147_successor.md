# SUCCESSOR BRIEF — Secuura/Blockchain seat s147, from Wednesday (coordinator seat 16:2x)

PROVENANCE:
- develop at 9e9a88709, #889 at af640e809, #890 at 74c0b3bbf, #891 at 3c07157a2 | s146's `git ls-remote`, quoted in its ITEM 1 mail 06:27:50Z and re-stated in its wrap 06:49Z — NOT re-derived by Wednesday, which holds no Secuura identity | read 2026-09-07
- #888 merged at 9e9a88709, demo VM still on 632f16dfe | s146 wrap mail 06:49Z, tree predicted before the merge and matched after, parents re-derived from the object | read 2026-09-07
- #891 refused: "refusing to allow a Personal Access Token to create or update workflow .github/workflows/nightly-platform-suites.yml without workflow scope" | GitHub's own error, quoted verbatim in s146's mail 06:37Z | read 2026-09-07
- The generated-actor path never runs; systemTest/fixtures/generated has 0 files in origin/develop and nothing automated invokes provision-actors.ts | s146's measurement, mail 06:43Z, over YOUR OWN tree (paths below are yours, not Wednesday's), with a positive control - the same git grep finds "test:unit" in your playwright/package.json | read 2026-09-07
- ADMIN_ACTOR_KEY = 'orgAdmin' and SYSTEM_ADMIN is deliberately not grantable through the API | the manifest module's own words, quoted by s146 from YOUR OWN tree: playwright/config/actorManifest.ts + environment.ts:36 - your paths, not Wednesday's | read 2026-09-07
- The one genuine SYSTEM_ADMIN site is schemathesis/config/fixtures.py:82 (super_admin persona); the other three executable sites are satisfied by orgAdmin with their routes read | s146's split measurement, wrap mail 06:49Z — conftest.py:83, setup_api_key.py:53 (requireRole SYSTEM_ADMIN,ORG_ADMIN), test_authentication.py:26 (login needs no role) | read 2026-09-07
- TEST_ADMIN_PASSWORD is documented WRONG, not undocumented: docs/setup_guide.md:89 gives the retired literal as its default, playwright/.env.example:27 is commented out | s146's measurement, wrap mail 06:49Z, correcting Wednesday's own framing | read 2026-09-07
- KS-969 filed with four items, assigned to our account, searched first across 958 issues by SYMBOL/PATH/STRING with only KS-966 and KS-967 matching (different subjects) | s146 wrap mail 06:49Z | read 2026-09-07
- No CI on this repo: the 20 most recent GitHub Actions runs are 100% startup_failure | s146's measurement, ITEM 1 mail 06:27:50Z | read 2026-09-07
- Kam's rulings quoted in this brief (13:06 Azure, 13:23 aggregation, 13:40 judgment calls, 09:40 merge, 11:09 deploy, 12:07 production) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh - Wednesday's project, not yours; his panel messages verbatim, read whole at this seat's boot | read 2026-09-07
- The undelivered ruled-card list | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura- - Wednesday's project, not yours | read 2026-09-07
- Both QA gates live and their briefs | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-07_secuura-ks952-890-tier1.md and .../2026-09-07_secuura-ks597-889-tier2.md - Wednesday's project, not yours; launched this seat, guards red-proofed | read 2026-09-07

## BLUF
You succeed **s146**, which wrapped cleanly at 16:49 with **nothing waiting on it** and scored 1.0.
**Your first work is KS-969 item 1** — it is independent of everything else in flight.
**TWO QA GATES ARE LIVE on #889 and #890. Their verdicts come to WEDNESDAY, not to you.** Do not
poll them, do not wait on them; you will be tapped when there is fix work.
**Read `HANDOVER-s146.md` in the repo first — it is current** (refreshed with the #888 merge, KS-968,
the #891 block and the item-4 stand-down).

## STATE, as s146 measured it at wrap
    origin/develop   9e9a88709   (#888 merged; tree predicted and matched)
    demo VM          632f16dfe   (the deploy — #888 is NOT on it)
    #889 af640e809   tier 2 + a mandated real-Postgres leg — GATE LIVE
    #890 74c0b3bbf   tier 1 — GATE LIVE
    #891 3c07157a2   MERGE GO given, BLOCKED on PAT workflow scope, carded to Kam
**PROVENANCE: every SHA above is s146's `ls-remote`, read in the same action as writing its wrap.
Wednesday has NOT re-derived them — this seat holds no Secuura identity. Re-read before you act.**

## YOUR QUEUE
1. **KS-969 item 1 — wire actor provisioning into a pre-suite step.** This is the unlock for the whole
   systemTest credential story and it is blocked by nothing. **It gets its own test; it is not a
   tail-end edit.** `systemTest/fixtures/provision-actors.ts` (in YOUR tree) exists and nothing automated invokes it.
2. **KS-969 item 3 — `TEST_ADMIN_PASSWORD`. TRACKED on KS-969, but the EDIT lands in KS-965's
   census pass** — s146 ruled it fixed there because that is where the wrongness is load-bearing.
   **Your job is that it is not dropped between the two tickets**, which is the standard failure of a
   cross-ticket item. `docs/setup_guide.md:89` gives the **retired literal** as the default and
   `playwright/.env.example:27` is **commented out** — so a runner following the docs exactly sets a
   password that fails, with no CI to say why. **Confirm on KS-969 item 3 which ticket carries the
   edit, so neither ticket closes assuming the other did it.**
3. Then the standing queue (category-1 tickets — no external input needed), priority then id.

## ⚖️ WEDNESDAY RULES KS-969 ITEM 2 NOW, so you do not re-open it
s146 measured the split: of 12 occurrences, **8 are documentary (KS-965, not this)** and 4 are
executable.

**🔴 RE-DERIVE THAT PARTITION BEFORE YOU USE IT — s146's TWO mails disagree and Wednesday is not
guessing which is right.** Its 06:43Z item-4 mail said *"12 occurrences across 8 EXECUTABLE files"*
with the 3 example-config and 8 documentation occurrences counted **separately**. Its 06:49Z wrap said
*"of the 12 occurrences, 8 are DOCUMENTARY and 4 are executable."* **Those are different partitions of
the same number**, and they imply different scopes for item 4. The wrap is later and was written after
reading each site, so it is the likelier one — **but that is an inference, not a measurement, and
Wednesday propagated the wrap's version into this brief before noticing.** **Re-count it yourself,
state the partition with its predicate, and correct whichever artefact is wrong** (the ticket, the
handover, or both). Do not reconcile them silently — say which was wrong and why. Three are satisfied by `orgAdmin` **with the route read, not guessed**. **The one genuine
SYSTEM_ADMIN site is `schemathesis/config/fixtures.py:82`** (the `super_admin` persona, cross-tenant
reads via `X-Tenant-Override`).
**RULING: that site is PERMANENTLY OUT OF SCOPE for the generated-actor migration**, because
SYSTEM_ADMIN is *deliberately not grantable through the API* — the manifest module says so itself.
**It keeps a credential source outside that path BY DESIGN. Write the reason ON KS-969 item 2** so no
future sweep "cleans up" the last fallback and breaks it. **This is a design fact, not a preference,
and it does not go to Kam.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
RULED BY KAM, NOT YET IN AN ARTEFACT — the operative ones first, the bookkeeping ones named after.
**Operative for you today — all from Kam's panel, verbatim:**
- **13:06** — *"Do not worry about the Azure credits. Kill all tickets and all elements that query
  this."* **Spend nothing on Azure credits.**
- **13:23** — *"if a single test is required, we should be creating one ticket with multiple items
  inside it."* **Governs CREATION, not retrofit.**
- **13:40** — *"use the findings to action the tickets accordingly… happy for you to take this and
  make judgment calls."*
- **Three week-scoped grants, live through Sunday 2026-09-13:** merge authority (09:40) · deploy
  authority (11:09) · **production ban lifted (12:07, Secuura ONLY — and every production change is
  flagged to Kam with what changed and where).**
- **09-06** — Platform K items are ours: **new and unassigned tickets go to our account; a ticket
  already on Peter or Stuart STAYS THEIRS.**
**Historical, already acted on, listed only because the delivery mark is outstanding — these are
bookkeeping and NOT instructions to you:** `secuura-ci-billing` (wait) · `secuura-agent-github-identity`
(identity) · `secuura-dependabot-triage` (close-and-rescope) · `secuura-ks229-disclosure-mailbox`
(later) · `secuura-demo-kam-admin-default-password` (b) · `secuura-f5-*` (wait / probe / letitland) ·
`secuura-demo-admin-transcripts` (redact) · `secuura-demo-admin-mfa` (later) ·
`secuura-ks930-cap-vs-regression` (one-more) · `secuura-ks949-round3-cap-and-the-cutoff` (split) ·
`secuura-ps-759-760-merge-owner` (kam-merges — **Platform S, not yours**).

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE — each still binds you unless this brief says otherwise.
- **Item 4 does NOT proceed as scoped** (16:44) — the generated-actor path never runs; the fallbacks
  are the live path. It returns only after KS-969 item 1.
- **#891: leave it open. Do not retry the merge, do not seek a wider token, do not split the PR**
  (16:40). It is Kam's click.
- **Do NOT probe the demo** for KS-968 (16:25) — carded to Kam, **default HOLD**. If he is silent,
  nothing runs.
- **The 88→50 board restructure is CANCELLED** — do not re-propose it.
- **A workflow touch is a PERMISSIONS question as well as a gate question** (s146's line, adopted):
  before proposing a merge that touches `.github/workflows/`, ask whether the seat can write that path.

## STANDING
No `cd` (hook). Taps ≤200 chars with a verified mail behind them. `<<'EOF'` for briefs; `-F -` with a
quoted heredoc for commits. **Never delete — quarantine or archive.** **Search before you file, by
SYMBOL/PATH/ERROR STRING, and say what you searched.** **Client-facing communication goes ON THE
TICKET; the extranet is input only; handovers to Peter/Stuart are TEST BLOCKS, never lists of PRs, and
Kam sends them.** **There is NO CI on this repo** (20/20 `startup_failure`) — `mergeable_state: clean`
means no required check is failing, **not that one ran**. **PULL BEFORE EVERY WRITE**; the laptop seat
is live on this vault. **If an instruction from Wednesday looks wrong, say so** — that sentence caught
four of Wednesday's errors today and every refusal was ratified.

## YOUR WAKE
Wednesday is live and will tap you. **End every leg with a mail to `wednesday-agent@agentmail.to`** —
that mail is the wake, not a turn that ends quietly. **If you wait on anything outside your session,
say in the mail what you expect will wake you.** Rotate at your own boundary and hand over rather than
starting what will not fit.

**SELF-CHECK FINDINGS (two contradictions found and handled):** the KS-969 item-3 ownership was ambiguous between KS-969 and KS-965 — now stated explicitly; and s146's two mails partition "the 12" differently — now flagged for re-derivation rather than asserted. Also read the previous outbound to this project (the 16:44 item-4 stand-down): this brief does not contradict it.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 16:53
