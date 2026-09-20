# QA COMMISSION — RD-516, TIER 1 (round 1 of 2)

**Target:** branch `rd-516-ai-test-ssrf-s73` @ `f4264e5137eec3e348a29538ffe7b4ee7267c120` · **Base:** `60c76d7` (verified an ancestor by Tuesday)
**Tier:** **TIER 1** — an SSRF surface on an anonymously reachable route. Full weight.
**Report path (create it; it must not already exist):** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd516-f4264e5-tier1/report.md`
**Verdict mail:** to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-516 @ f4264e5 (tier 1)`

## 🔴 READ THIS FIRST — the technical material is IN THE REPO, not in this file
**`docs/rd516/RD-516-gate-brief.md`** on the branch under test (that is the IN-REPO path; the repo root IS `2_Project_Files`, so `git show <sha>:2_Project_Files/docs/...` returns "does not exist"). The builder accumulated it during the work rather than reconstructing it at the end. **It carries: what is ALREADY MEASURED so you do not redo it · the drivable surface · the mutation list with which cell each reddens · §5 the acceptance clause · §6 the named 27 seam-dependent cells · §7 the honest NOT-TESTED list.**

**This file is the commission. That file is the subject. Do not duplicate it here — read it there.**

## THE DRIVABLE SURFACE — a LOCAL run, NOT the demo
**RD-76 is real: the demo's `/login` has zero `<form>` and zero `<input>`, so no test account opens it.** Boot via `__tests__/helpers/rd395-server-harness.js` against a FRESH data directory; the suite's own boots show every env var the cells need. 🔴 **Say so in the verdict, so nobody later records a demo pass that did not happen.**

## WHAT I WANT FROM THIS GATE, in priority order
1. **Drive the refusal paths yourself, anonymously, in the open first-run window** — private, loopback, link-local, CGNAT, reserved and non-string targets — and confirm 400 with **zero dial attempts** and **no content echo**. **Pair every zero with a control that proves the instrument can see a dial** (the brief names four ways the dial counter's zero can lie; read that section before trusting any zero).
2. **Run the five owed mutations** in the brief's mutation list and confirm each reddens the cell it names, and only that cell.
3. **Check the audit reason taxonomy end to end** — a LITERAL IP must audit as its ADDRESS class, a NAME as the host-list reason. This was a real defect found during the work; confirm the fix holds on every class.
4. **Verify the ABSENCE clause**: RD-516 introduces no `dispatcher`, no `fetch:` option and no custom agent on the ai-test path, and `AOAI_FETCH_OPTIONS` still carries `redirect: 'error'` (RD-523's defence). **Mutation: delete the `fetchOptions` argument at `azureOpenAIAdapter.js:157` and rd523's cells must redden.**
5. **Report on the ACCEPTANCE CLAUSE (§5) as a finding, not a pass/fail of this branch**: are the 27 on main? They are not yet, by design. **Say so plainly so the verdict cannot be read as clearing the merge.**

## WHAT IS ALREADY KNOWN AND IS NOT A FINDING
**Do not spend a round rediscovering these — they are ticketed and in §7:** R7 fails for naming only (RD-585, containment green) · R8 fails on RD-541/C-106 (the limiter collapse belongs elsewhere) · R10(i) is skipped (RD-583, the scheme rule is unimplemented) · **R16 and R3 are NOT WRITTEN**, with reasons (R3's subject is the address pinning RD-584 holds, and **R3 must never be built on the interception seam** — that would test the harness against itself) · the timing channel is open (RD-581) · the Ollama branch is untouched (RD-478) · key exfiltration to an attacker's own AOAI resource is not closed by this ticket (RD-549).

## CREDENTIALS — ABSOLUTE PATHS, because "this project's" was wrong last time
🔴 **The AgentMail key is at `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (`AGENTMAIL_API_KEY`).** The QA project has **no** `4_Credentials` directory — a previous brief said "this project's `4_Credentials/.env`" and the gate had to work that out and report it as a finding. Do not look for one.

## BOUNDARIES
Findings only — **you never fix.** No merge, no deploy, no push to the branch. Anything irreversible, money, production or human-facing stops and comes to me. **Round 1 of 2 on this class; a third round is Kam's (C-62).**
