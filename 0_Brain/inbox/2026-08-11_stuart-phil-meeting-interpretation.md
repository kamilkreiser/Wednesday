# Secuura Technical Weekly — 2026-08-11 11:30 AEST (Stuart, Phil, Kam)
## Wednesday's interpretation + clarifications + task breakdown

Source: Gemini meeting notes, `~/Downloads/Technical Weekly Catch up – 2026_08_11…`,
handed to Wednesday by Kam. This is Wednesday's reading — **claims attributed to
a named person are theirs; anything marked (inference) is Wednesday's reading, not
what they said.** To be shared with the Secuura/Blockchain (=Blockchain Manager)
agent AFTER Kam answers the open questions at the foot.

---

## A. Load-bearing project CLARIFICATIONS (these change how the platform is described and built)

1. **Certification is now an UMBRELLA term, not an action.**
   Certification = **attestation + signing + (optional) watermarking**. Agreed by
   Phil + Stuart + Kam. Attestation = a user attesting a document is correct
   (stored on-chain via the system, distinct from the file). Signing relates to
   integrity/authenticity. Watermarking is a **distinct, optional** third element.

2. **Any modification — including watermarking — creates a NEW document version
   that REQUIRES RE-CERTIFICATION.** Tracked through document lineage as distinct
   version updates. This is a hard rule now, and it bears directly on verify/
   certify logic and on KS-584/P3 territory (which row/version is "the" certified
   one).

3. **Verification is a CONFIGURABLE WORKFLOW, not a fixed function.** Kam's
   position, agreed: the platform stays flexible ("buffet-style"), clients
   configure verification workflows **via smart contracts**; Secuura does NOT
   prescribe regulatory rules — clients define and enforce their own compliance
   (e.g. required identity-verification steps). The recruiter-verifying-a-
   university-document scenario is answered by the workflows feature: track and
   **display the specific verification steps** (identity checks, domain matching)
   for the verifier to inspect.

4. **Blockchain recording logic (directly relevant to PS-556):** the **workflow
   path must be verified against the smart contract** and recorded; **simple
   interactions like document VIEWING must NOT be recorded on-chain** — explicitly
   to avoid "noise." (This is Kam + Stuart, in the meeting. See PS-556 note.)

5. **End-user sees a simple binary "verified"; audit/legal sees the full rigor.**
   The system supports complex, theoretically rigorous processes for audit and
   legal purposes, but the end-user primarily sees a simple binary status.

6. **Environment separation — the instability we saw today is explained.** Kam:
   recent platform instability came from MERGING the demo and dev systems, which
   were previously separate. Decision: **separate them again.** Legacy UAT stays
   standalone; a **NEW dev VM** (connected to Cardano) is spun up for development
   and breaking changes; the current stable system remains for demos. Kam creates
   the dev VM.

7. **Naming convention change (PENDING Kam's adoption decision — see Q1).** The
   team agreed to STOP using "Platform S" and "Platform K" and adopt the temporary
   names **"Legacy UAT"** (= the .NET document platform, Stuart's side, PS team) and
   **"Blockchain Manager"** (= the Cardano anchoring platform, Kam's side, KS team),
   until the architecture is formally updated.

8. **Terminology for external comms needs defining** — "signing" is ambiguous
   (lawyers vs admins). The group will define clear distinctions between
   certification, verification, signing, watermarking for stakeholders and
   lawyers; Phil researches external-facing labels (replacing "signing" for
   hashing/integrity tracing).

---

## B. CORROBORATION of work already in flight (no new action, but confirms our reads)

- **KS-584 = "the critical error affecting the verification process."** Kam told
  the meeting it is "resolved with a quick fix" (our interim) and that the
  **permanent multi-day fix (P3) will be implemented once the new dev environment
  is operational, to avoid breaking existing systems.** → This adds a real
  dependency to P3 the agent does not yet know (see Q2).
- **PS-552 confirmed live** — "uncertified documents were incorrectly flagged as
  certified in the Outlook plugin." Matches Stuart's PS-552; the Outlook-plugin
  context is new detail.
- **Security items corroborate my earlier flags** — restrict UAT signup to
  specific emails (≈ the QuickQuote allowlist debate, and my PS-438/439 flag:
  UAT MFA off + hardcoded dev password), admin 2FA, health-info behind VPN/IP.

---

## C. TASK BREAKDOWN (drafted; NOT yet created — Linear cap is a hard block, see Q3)

### For the Blockchain Manager (KS / Secuura-agent) side
- **BM-1 Certification model:** implement certification as attestation + signing +
  optional watermarking (umbrella), with watermark/modification → new version →
  mandatory re-certification, tracked via lineage. (Big; likely multi-ticket.)
- **BM-2 Verification-as-workflow:** verification steps defined/enforced via smart
  contract; record the workflow path on-chain, do NOT record casual views.
  Display inspectable verification steps to a third-party verifier.
- **BM-3 P3 permanent verify fix** — build now, **land in the NEW dev env** once it
  exists (Q2). Already scoped: versioned verify-list + caller-independent
  service-to-service anchor truth + stale-status reconciliation.
- **BM-4 New dev VM bring-up** (Kam-led; agent may assist with the Blockchain
  Manager service deploy onto it). Separate from stable demo.
- **BM-5 System-details ticket for Peter & Stuart** (Kam's "document system
  details" next-step) — the agent likely drafts the technical content.

### Kam's own (tracked, not the agent's to execute)
- Create dev VM · document system details ticket · create Tron/Flynn persona
  ticket (agent-infra formalization) · review BRD when Phil shares · set up a
  ticket "once a Japanese name is confirmed" (unclear — see Q4).

### Stuart's (Legacy UAT / PS — context for the agent, not its work)
- Differential analysis (current platform vs BRD) using Claude · UI filters to
  de-clutter power-user views · restrict UAT signup to specific emails · admin
  2FA · finalize identity system · configure org-wide SSO (Google + GitHub) ·
  deliver 3 items to Kam.

### Phil's (context)
- Upload + share BRD · update certification definitions doc · research external
  terminology · distribute finalized definitions · discuss sandbox strategy with
  Ven (Swipe Task API integration).

### Group
- Define terminology (certification/verification/signing/watermarking) for
  stakeholders + lawyers.

---

## D. AGENT-INFRASTRUCTURE note (this is about Wednesday's own model)
Kam described **Wednesday** to Stuart and Phil — coordinator over specialized
per-company agents (QA, security), iTerm sub-terminals, shift from reading all
output to managing rules/gates. They're **adopting the model**: a matrix of
subject-matter agents (engineers per company, a privacy-act expert, a **system
architect** role Stuart suggested) coordinated by Wednesday. Personas
(CORRECTED per Kam 2026-08-11): **Tron = Wednesday** — Stuart referred to
Wednesday using *Tron* (the film) references, i.e. Tron is the coordinator/
master-control figure, which is Wednesday's role. **Allan** = reliable senior
SWE agent · **Flynn** = disruptive/creative agent. (My earlier reading listed
Tron as a separate master-control persona — wrong; Tron IS Wednesday.)
Commitment to formalize via a ticket. Stuart's health note (BP from manually
juggling 20–30 Claude tasks) is the human driver.
→ This validates today's coordinator-not-carrier + QA/security-agent commission.
Worth a WED-side note; may inform WED-41/43/44 (QA + security + a new architect agent).

---

## E. PS-556 debate — what this meeting CONTRIBUTES (do NOT resolve; for Kam's debate)
The meeting speaks almost directly to my open PS-556 question. Folded into the
parked debate note. Headline: Kam-in-the-meeting already drew my core line —
*"simple interactions like document viewing should not be recorded on-chain
(noise); the workflow path must be verified against the smart contract"* — which
is my "reads are private/noise; opt-in workflow-defined verification is recorded"
position, in his own words. The recruiter scenario → inspectable workflow steps is
close to my "receipt" concept. **This likely reframes PS-556 from "does K record
verification acts?" to "the client's smart-contract WORKFLOW defines what is
recorded; casual verification is not."** Bringing to the debate, not deciding.

---

## OPEN QUESTIONS FOR KAM (must answer before Wednesday shares with the agent)
See the message to Kam. Q1 naming adoption · Q2 P3/dev-VM dependency · Q3 Linear
cap vs new tickets · Q4 minor ambiguities (Japanese-name ticket; scope of share).

---

## KAM'S ANSWERS (2026-08-11, decisions RESOLVED)

- **Q1 naming → DO NOT change anything internal.** External-facing names (Legacy
  UAT / Blockchain Manager) are noted for context only; internally Kam and Stuart
  still say S and K. Keep KS/PS, cockpit name, launchers, INDEX unchanged.
- **Q2 P3 → (a).** Build P3 now; **deploy into the new dev server once it exists.**
- **Q3 Linear cap → cull first**, then create the meeting tickets in the same
  session (Kam agreed the recommendation).
- **Q4 → the "Japanese name" is KINSUGI** (Kintsugi — the art of mending broken
  things with gold, which highlights the break and makes the thing better for it).
  **Kintsugi is the name of the NEW Platform K DEVELOPMENT server.** Kam asked for a
  clarification ticket (drafted below). NB this is a SERVER hostname, additive —
  not a platform rename, so no conflict with Q1.

## DRAFTED TICKET — for the Secuura/Blockchain agent to CREATE after the cull
(Wednesday cannot create it: read-only tracker grant + Linear cap hard-blocks
creation until the cull. Content is ready so the agent creates it verbatim.)

**Title:** [Infra] New Platform K dev server "Kintsugi" — restore dev/demo split;
promote to demo+staging only on Kam+Peter+Stuart sign-off

**## BLUF**
A new Platform K server named **Kintsugi** becomes the DEVELOPMENT server. The
current Platform K server becomes **DEMO + STAGING** (stable). Restore the prior
workflow: develop and test against **Kintsugi**, and promote to the current
(demo/staging) server ONLY once **Kam, Peter and Stuart** give the go-ahead.
Decided at the 2026-08-11 technical weekly; directly fixes the instability caused
by merging dev and demo into one system.

**## Recommendation / actions**
- Stand up **Kintsugi** (new VM, Cardano-connected) as the dev environment
  (Kam-led; the Blockchain Manager agent assists with the service deploy).
- Current Platform K server → **demo + staging only**; no development against it.
- **Promotion gate:** no push Kintsugi → current server without explicit
  Kam + Peter + Stuart sign-off.
- **P3 dependency:** the permanent verify-by-hash fix (KS-584 P3) is BUILT now and
  DEPLOYS into Kintsugi once it is operational — never against the demo/staging box
  mid-development (Kam's "avoid breaking existing systems").

**## Detail**
Name rationale (worth keeping): *Kintsugi/Kintsugi* mends a break with gold so the
mended object is stronger for the break — fitting for the server where breaking
changes are made, healed and proven before promotion. [SPELLING CONFIRMED by Kam 2026-08-11: canonical = **Kintsugi** (with the t).]

## FRESH-SESSION EXECUTION PLAN (hand-off; Wednesday hit her 50% checkpoint)
Do these in a fresh Wednesday session, in order:
1. Relaunch Secuura/Blockchain fresh for P3 — brief: build P3 now (legs 1+2),
   **deploy target = Kintsugi once it exists** (Q2a), hold at ready-to-land for
   Kam's cutover word (versioned, ruling (a)).
2. Have the agent run the **Linear cull FIRST** (archive already-actioned tickets;
   never close anything live; ambiguous → list for Kam; report before/after
   active count).
3. Then the agent creates: the **Kintsugi ticket** (verbatim above, once Kam
   confirms spelling) + the meeting task set (BM-1 certification model, BM-2
   verification-as-workflow, BM-5 system-details for Peter/Stuart) — BLUF format,
   in the KS team.
4. Share the meeting INTERPRETATION (sections A/B/C/D, NOT section E / PS-556) with
   the agent as context for BM-1/BM-2.
5. Carry the certification-redefinition + verification-as-workflow clarifications
   into the P3/architecture context (they bear on what "certified" means).
6. Leave PS-556 (section E) OUT — it is Kam's open debate.
