# WED-102 — Verification of the HPSM structure proposal against the PPT and SOW

**For: Kam · the 2026-08-13 flesh-out sitting.**
**Method:** I read the proposal (C2, 264 lines) in full, then judged every load-bearing
claim against verbatim extracts of the SOURCES — PRD §7.2/§9, SOW-01 §3/§4/§14,
GTM §3.1, deck slides 41/48/66 full-text + 87–146 titles, template inventory —
pulled raw by an extraction agent and evaluated by me. Not against the proposal's
own citations. (Coverage caveat: deck checked at full text for 3 slides + titles
for 60; not all 151.)

## BLUF

**The proposal survives verification.** Every factual claim I checked is accurate
against the sources, both defects are real, and the eight-module spine is
genuinely corroborated (GTM §3.1 + templates + the deck's own commercial anchors).
**But I found one gap the proposal does not name, and it is the first thing HP
will push on: the spine has no Compliance section — and "compliance" is one of
only three section names the SOW explicitly contracts.** Fixable in tomorrow's
discussion; should not go to HP as-tabled.

## Claims verified ✅ (all confirmed verbatim)

1. **PRD §7.2 wizard sections** = Business | Fleet | Firmware | Authentication |
   Monitoring | Compliance — exact.
2. **PRD §9** = six domains, 20/20/15/15/15/15, sum 100%; Data Protection 15% +
   Hardening 15% have no matching wizard section; Business + Fleet score nothing.
   **Defect 1's arithmetic is right.**
3. **SOW §4 Musts**: "Versioned deterministic scoring" ✓ · "finding-to-service
   opportunity mapping" ✓ · Assessment Engine "business/fleet/compliance
   sections" ✓ (so Defect 3 — SOW names 3 sections vs the PRD's 6 — is real).
4. **SOW §3 precedence**: PRD is priority 3 = the acceptance baseline ✓; the
   Playbook v3 deck itself is priority 6 (so the deck is IN the contract stack).
5. **GTM §3.1** = the eight modules with the stated prices, including both
   US$2,500 entry modules ✓. Datasec_01–08 template filenames track the eight
   modules 1:1 ✓.
6. **The deck fixes nothing that contradicts a ten-section wizard** (within my
   coverage): s48 contracts only "'Good' web-based MFE / white-labeled MVP";
   the s87–146 content block is phase/commercial structure, not assessment
   domains. The spine aligns WITH the deck's own eight-anchor service structure.
7. **Independent corroborations landed en route:** the extractor (blind to the
   findings) flagged the §14 payment-table arithmetic itself (M8: 5% ≠ A$75k;
   rows sum past the A$750k baseline) — third independent confirmation. s48's
   "$650,000 for Web Playbook MVP" confirmed verbatim → the FX-gap finding
   stands. s41 confirms "Partner portal MFE" sits under Channel Licensing
   capabilities — the scope-ambiguity finding stands.

## What I'd sharpen (2 items)

**A. Defect 1 is real but should be stated one notch softer.** PRD §7.2 is a
*low-fidelity wireframe* — its Sections line is inside a mock-up, and the
question set itself is HP-owned and unsupplied (P05). HP can answer "the six
sections are navigation; the question set will cover all six scored domains."
The defensible form: **the mapping from collected inputs to 30% of the score is
UNDEFINED in the acceptance baseline** — still signature-blocking (deterministic
score Must + undefined input mapping = acceptance dispute), but framed as a
clarity defect, not "the engine cannot score." Same conclusion, harder to argue
with.

**B. The gap the proposal misses — Compliance loses its home under the spine.**
The ten proposed sections contain no Compliance section. PRD §9 gives
Compliance Readiness 15% (policy evidence, audit trails, regulatory alignment);
the proposal's own mapping table grades its nearest module ("Security Operating
Model – Governance & Cadence") as *"partial — governance ≠ compliance
evidence."* And SOW §4 contracts "business/fleet/**compliance** sections" by
name — the spine keeps business and fleet as context sections and silently
drops the third. For an SMB product whose own deck leads with ePHI/HR/financial
documents (s41), losing the compliance domain is a product regression HP may
rightly reject.
**Fix options for tomorrow** (either keeps the spine's two dissolutions intact):
  (i) rename/extend section 5 to "Operating Model, Governance & Compliance
  Readiness" and move PRD §9's compliance example-inputs into it explicitly; or
  (ii) a ninth scored section "Compliance Readiness" mapping to a bundled
  service offer (costs the clean 8=8 identity mapping but keeps the domain
  first-class). I lean (i) — it preserves the identity mapping and the SOW
  line-fix covers the naming.

## Also surfaced by extraction (ops, not structure)

- The on-disk template extraction is **missing Datasec_10/11/12** (L2/L3/L4
  level templates) relative to its own source zip — HPSM-16's level analysis
  used Datasec_00's matrix so its conclusion stands, but re-extract before the
  refinement session.

## Net for tomorrow

Adopt-with-amendments is my recommendation: the spine's two dissolutions are
real and the corroboration is strong, but it goes to HP only after (1) the
Compliance home is decided, (2) Defect 1 is reframed as the undefined-mapping
clarity defect, and (3) it rides the single PRD-reopening conversation with the
A2.4/A2.2 items as the proposal already suggests.
