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
architect** role Stuart suggested) coordinated by Wednesday. Personas: **Tron**
(master-control metaphor), **Allan** (reliable senior SWE agent), **Flynn**
(disruptive/creative agent). Commitment to formalize via a ticket. Stuart's
health note (BP from manually juggling 20–30 Claude tasks) is the human driver.
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
