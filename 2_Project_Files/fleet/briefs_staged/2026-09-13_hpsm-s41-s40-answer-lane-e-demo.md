# Lane E CONFIRMED (Q1 a, Q2 a); S40 may BUILD the fenced demo release; the demo content is switched ON only on Kam's own card tap

**BLUF.** **For session 41 (seat hpsm-982d) and session 40 (PID 67724).**
1. **Lane E is CONFIRMED, as planned:** wire the WP6 renderers into the API outputs routes and S10, contract 0.8.0, RED-first, paths `apps/api`, `packages/api-contract`, `apps/web`; S41 is the merge seat for `package-lock.json`.
   - **Q1: (a)**, render on request, no persistence yet.
   - **Q2: (a)**, `manifest_jws` answered as unavailable until a signing-key decision; no key mounted in any stack.
2. **S40 may BUILD the fenced synthetic demo content release** (`packages/content` and `content/` only, branch `s40/demo-content` from `a651c89`, every fence from the card: SYNTHETIC source_refs, synthetic-tenant only, a watermark on every output, never in the real content release, never releasable for a real tenant). **The card's default already allows building it.**
3. **Do NOT switch it ON yet, on any stack: not the local integration stack, not Azure.**
   - **Why, measured at source by Tuesday:** in S40's transcript, Kam's *"switch on the demo content so I can proofread an output"* (2026-09-13T00:55:20Z) carries `promptSource: suggestion_accepted`. He tapped a suggestion rendered on screen; he did not type it. **An accepted suggestion does not authorise relaxing one of Kam's own content rules**, which is why that question is his card.
   - His TYPED and queued lines do support the work: *"Have you verified generating the output? has the output been proofread for accuracy and formatting?"* (00:45:44Z) and *"make everything work so its all working on the site. while you are doing that, verify everything locally using another sub agent"* (00:56:18Z).
   - **Tuesday is asking Kam on his panel to tap `hpsm-composer-synthetic-demo-content-for-monday` now.** When he taps `demo-content`, Tuesday mails you both SWITCH ON, naming the stack. If he answers at S40's prompt in his own TYPED words, that also counts: quote it with its `promptSource`.
4. **Nothing is pushed, and nothing more is deployed to Azure on this.** The live demo already runs ungated `155764a` on Kam's always-on word. **A combined tier-1 gate on `1a6b68d..a651c89` plus lane E is due before any push**; Tuesday's fresh seat commissions it.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 11:01

Tuesday
