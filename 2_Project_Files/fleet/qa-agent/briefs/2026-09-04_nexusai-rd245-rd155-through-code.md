# QA Agent Invocation Brief — Datasec / NexusAI, RD-245 + RD-155 through-code pass

**R0 (client isolation):** this brief carries exactly one client's content — Datasec / NexusAI. Do not name or reference any other client, in the report or anywhere else.

## Charter (read first, in full)

`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

Read it end-to-end before running anything. This brief supplies only WHAT and WHERE.

## 1. Target
- **Client / Project:** Datasec / NexusAI
- **Source tree (read-only, for root-causing):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files`
- **Branch under test:** `rd-136-nga-defaults-s12` at **`b8068485cc2ade013912818c8366449ea74bec14`** — verified as that branch's head at origin by Wednesday with `git ls-remote origin` in the same action as writing this line.
- **Running target:** the project's local dev stack. **Environment identity: LOCAL DEV, non-production.** Nothing in this pass touches the Azure demo or any deployed revision.
- **Production?** NO. This is a local branch that has not been deployed. **If any step would reach a deployed surface, stop and mail Wednesday.**

## 2. Spec / DoD being tested against

**These are the BUILDER'S CLAIMS, taken from its STATUS mails to Wednesday at 03:30:35Z (RD-155) and 03:51:01Z (RD-245). They are inputs to FALSIFY, not evidence.** Wednesday has ratified the SHAPE of both reports and has explicitly NOT ratified their correctness — that is this pass's question.

### RD-245 — backup rotation lost a generation
1. `backupFile()` compares live to the newest backup by sha256 and **returns when identical**, so an unchanged file consumes no rotation slot. The claim is that this single check makes the 04:35:15 boot a no-op, and that the no-op boot **is the whole of the data loss**.
2. **The THIRD boot is the test.** The claim is that after a mutation and ONE boot the good copy still sits in `prev` under the OLD code too, so the defect only appears on the boot after that — i.e. **a test that booted once would have passed against the code that lost the data.** Check this reasoning holds, and check the committed test actually reaches the third boot.
3. A criterion-3 warning naming both files if a rotation would ever leave no differing copy — kept deliberately even though the identity check should make it unreachable.
4. `writeEmergencyCopy()` was hoisted to an idempotent helper on BOTH paths, because the early return would otherwise have skipped the emergency copy (a copy of LIVE, not a generation). Claim: a deployment whose settings stopped changing after the emergency directory appeared would never have received a last-resort copy.
5. **`backupFile` is the SOLE writer of those slots** — the claim is that the three other sites are restore paths copying backup → live.
6. Red-proof, second attempt: **2 fail / 2 pass**, the two passing being the genuine-change rotation and the harness control.

### RD-155 — settings-elsewhere warning silent for numbers and booleans
1. The predicate now counts numbers and booleans, **including `0` and `false`** — "only absence is absence"; a naive `if (value)` would silently reintroduce both.
2. Four named-key branches were **removed as subsumed** by the general rule.
3. 23 table-driven tests; against the OLD predicate **exactly 5 fail** (NUMBER · BOOLEAN true · ZERO · FALSE · a numeric key beside a null), and `'true for authEnforced as a boolean'` **PASSES** on the old code via its named branch.
4. All 8 negative cases and both controls **pass on the old code too** — so the table is claimed not to assert the new behaviour into existence.
5. The predicate is now **exported**; previously reachable only through `resolveDataDir`'s side effects.
6. `jsonStorage.js` restored **byte-identically** after the tamper.

**Gate claim, both tickets:** `VERDICT: PASS — 1504/1504 across 88`.

## 3. Scope

**Charter:** a through-code pass on RD-245 and RD-155, hunting for the classes this fleet keeps paying for — a guard whose corpus is narrower than its claim, a control that cannot fail, a fix that closes the named cause while the symptom survives, and a sibling surface the fix did not reach.

**In scope:** the RD-245 and RD-155 diffs at `b8068485cc`; the backup/rotation machinery and every writer of those slots; the settings-elsewhere predicate and every caller; the committed tests for both, read as well as run; the gate's own count.

**Specifically worth your attention, because Wednesday cannot check them from outside:**
- **Claim 5 of RD-245 is a REACH claim** ("sole writer") and this fleet has been wrong about exactly that shape repeatedly. Enumerate the writers yourself; do not accept the enumeration.
- **RD-245's fix introduced a hole its author found and closed in the same commit.** Ask what ELSE the early return skips — an early return is a control-flow change, and one skipped side effect being found does not bound the set.
- **RD-155 removed four branches as "subsumed".** Subsumption is a claim about a predicate's extension. Find an input the four branches caught that the general rule does not.
- **Both red-proofs are the builder's own.** Re-derive at least one of them independently rather than re-running theirs.

**Out of scope / do NOT touch:**
- **RD-296** — its BUILD is HELD with Kam. Do not test it, do not touch it, do not recommend starting it.
- **RD-281 is IN PROGRESS on a live surface** — `tests/e2e/ground.js` and the sustainability contrast specs. Read them if you must, change nothing, and do not report churn there as a finding of this pass.
- Anything deployed. Anything in another client's tree.

## 4. Credentials (POINTER ONLY — never values)
- `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/4_Credentials/.env` — source it, never echo a value, never copy one into a report.
- No persona/role exercise is required for this pass; it is through-code plus local test execution.

## 5. State-mutation & cleanup
- **Pattern for this pass: exclude-and-report-only.** Do not provision accounts, do not mutate any shared state.
- **NEVER `rm`, in your scratchpad or anywhere else — STANDING, all projects (Kam's rule: cleanup means quarantine, not removal).** Build each attempt in its own `mktemp -d` and abandon the old one; a scratchpad is disposable, so nothing needs deleting. If a path genuinely must be cleared, move it into a dated `_quarantine_YYYY-MM-DD/` beside it and say so. Guard every expansion — `"${DIR:?unset}/${SUB:?unset}/…"` — so an empty variable ABORTS rather than widening. **If a cleanup is costing you real budget, stop building the fixture and report the affected checks as NOT RUN with the blocker named.**
- **Restore any file you tamper with byte-identically and prove it with a hash.** RD-245's subject is a file-rotation mechanism; a tamper you do not restore is indistinguishable from the defect.

## 6. Output boundary (fixed — not a choice)
**Findings, reports and recommendations ONLY.** Make NO changes of any kind — no code, no tests, no fixtures, no tickets, no config. Describe the fix-shape and the regression test the owner should add, in prose. The project's own agent authors and commits everything. (Kam ruling 2026-08-11, absolute.)

## 6a. EVIDENCE CLASS ON EVERY FINDING THAT RECOMMENDS AN ACTION (mandatory)

**Any finding that recommends an ACTION — fix this, wire this, delete this, prioritise this — carries its evidence class inline, in these words:**
- **`MEASURED AT RUNTIME`** — the behaviour was driven and observed. Name the probe.
- **`PROBED`** — an adjacent call was made; say which, and what it does NOT cover.
- **`READ ONLY`** — established from source, spec, config or docs, **not executed.**

**A recommendation with no evidence class is incomplete.** This rule exists because a QA recommendation of this fleet's own, right about VALUE and silent about FEASIBILITY, was overturned by a live probe one commit before it shipped — the report presented a static read with the same confidence as its measurements.

**The corollary, and it bites directly on this pass:** a repo's own gate passing is not evidence that the behaviour is right. **`1504/1504 across 88` is a claim about a suite, not about a backup that survives three boots.**

## 7. Known-fragile / known-changed areas

**Known-fragile — hunt the class here first:**
- The **jsdom instrument cluster (RD-163 / RD-201 / RD-199)** is a known open gap: RD-163 is recorded as potentially invalidating *"every contrast number this engagement has measured."* If anything you touch depends on a jsdom-measured value, treat it as unreliable and say so; do not re-derive the cluster, it is not this pass.
- This project's guards have repeatedly been red-proofed in the shape of the defect that motivated them and shipped over a corpus of a different shape.

**Recent changes — do NOT flag as new regressions:** RD-291, RD-294, RD-299, RD-300 (Declined), RD-301, RD-302 all moved today; several are record/ticket corrections rather than code. RD-282 (layout, page-level guard) and RD-155 also landed today. **Their board states are the builder's read from its 03:51:01Z STATUS mail, not re-derived by Wednesday.**

**Known open gap, carried so it is not rediscovered:** the QA project still has no launcher entry, no inbox and no wrap hook — Wednesday runs this hop by hand and reads your report from your own project tree.

## 8. Logistics
- **Session time-box:** one bounded pass over the two tickets. If you reach a context boundary, stop at it and write what you have with the untested areas named — an honest partial pass is worth more than a rushed complete-looking one.
- **Report location:** under your own project tree (`projects/<product>/reports/`), as the charter specifies. Tell Wednesday the path.
- **Untested areas are first-class output.** Lead the NOT-TESTED list with what you did not execute.
- **Escalation path:** back through Wednesday at `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] QUESTION: <topic>`. Approval-class items (prod/demo-affecting, money, external comms, anything irreversible) ALWAYS pause for Kam. **Priority on any finding is the humans' call, never yours.**

---

PROVENANCE:
- Branch head `b8068485cc2ade013912818c8366449ea74bec14` on `rd-136-nga-defaults-s12` | `git ls-remote origin` run from Wednesday's seat, read-only | read 2026-09-04
- RD-245's six claims and the 2-fail/2-pass red-proof | the builder's STATUS mail `[Datasec/NexusAI -> Wednesday] RD-245 FIXED @ b806848`, 2026-09-04T03:51:01Z, at wednesday-agent@agentmail.to | read 2026-09-04
- RD-155's six claims and the exactly-5-fail red-proof | the builder's STATUS mail `[Datasec/NexusAI -> Wednesday] RD-155 FIXED @ b56fa37`, 2026-09-04T03:30:35Z, at wednesday-agent@agentmail.to | read 2026-09-04
- The gate claim 1504/1504 across 88, and the ticket states listed as recent changes | the same 03:51:01Z STATUS mail — the builder's read, NOT re-derived by Wednesday | read 2026-09-04
- RD-296's BUILD is HELD with Kam, and RD-281 is In Progress on ground.js | Wednesday's daily note 2026-09-04, 12:30 and 13:37 blocks, Wednesday's project not yours | read 2026-09-04
- The jsdom cluster RD-163/201/199 as a known-fragile open gap | the builder's 03:51:01Z STATUS mail, its budget-judgement section | read 2026-09-04

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 13:53
Wednesday's own limits, stated so this pass is not calibrated against false confidence: Wednesday has verified ONLY the branch head at origin. Every claim in section 2 is the builder's, unverified by Wednesday, and is listed to be falsified rather than confirmed. The ticket states in section 7 are the builder's read and Wednesday did not re-derive them from the board. Where this brief and the tree disagree, the TREE governs — say so and continue.
