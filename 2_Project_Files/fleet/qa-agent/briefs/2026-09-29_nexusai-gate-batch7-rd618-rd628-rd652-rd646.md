# QA Agent Invocation Brief — Datasec/NexusAI, ONE batched gate "batch 7": RD-618 (TIER 1) + RD-628 (TIER 2, through-code) + RD-652 (TIER 2) + RD-646+RD-647 (TIER 1) (lane 1) + RD-686 ROUND 2 OF 2 (TIER 2, words; lane 4) — five verdicts, one report

**ROUND CAP — RD-686 is at ROUND 2 OF 2 for its class. A NO GO on RD-686 here goes to KAM, not to a round 3** (Tuesday's commission, 2026-09-29).

**Drafted for Tuesday 2026-09-29 ~00:05–~00:50 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.** (RD-686 round 2 was added by
Tuesday's mid-draft message at ~00:30 AEST.)
Commissioned on Tuesday's batch 7 commission (2026-09-29) and six READY mails on disk, each read WHOLE (members A-D are NexusAI lane 1, built by
**NexusAI-M (S86M)**, which is also the lane-1 merge author after the verdict; member E is lane 4, built by **NexusAI-P (S86P)**, its merge author):
- **A — RD-618** @ `4334b96d91132d933bc30b6b8dbd63e2031552cc` (branch `rd-618-csp-intake-residue-s86m`) — the new-head READY
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_nexusai-rd618-r2-READY-mail.txt` ("supersedes 7e4cd2e … Everything
  else in that READY stands") and the first READY `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_nexusai-rd618-READY-mail.txt` (for `7e4cd2e`).
- **B — RD-628** @ `a5799f3ba444fba82b8f8f34529b5493751a9b48` (branch `rd-628-two-machine-id-derivations-s86m`) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_nexusai-rd628-READY-mail.txt`
- **C — RD-652** @ `09e2e6accf172f574dec22bdaedc47e104076edd` (branch `rd-652-node-env-unset-warn-s86m`) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_nexusai-rd652-READY-mail.txt`
- **D — RD-646 + RD-647** @ `608a1cd99adcc69f6d2cdc552f170e89710adb02` (branch `rd-646-647-redis-fail-closed-recovers-s86m`) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_nexusai-rd646-647-READY-mail.txt`
- **E — RD-686 round 2 of 2** @ `ab1272678fe40e23cff86ff749601572dc8cb64b` (branch `rd-686-694-brand-wording-s85p`; one commit on the batch-6-gated
  `8962a14`) — `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-29_nexusai-rd686-r2-READY-mail.txt`

**Batched under the 2026-09-18 batch-gates rule, as batches #1-#6.** E is words only and disjoint from A-D (no shared path, no executable change; §1
TARGET E). Unlike batch 5b, **three of the four lane-1 members change the server entry point**
(`backend/server.js`: A, C and D), and **A and D interact at run time on `POST /api/csp-report`** — the reason A-D are gated together (THE
CROSS-CHANGE CELL, §8). Every pair merges counts-only by merge-tree (MEASURED by the drafter, §1); **merge-tree cannot see the interaction; only a run can.**
**Every head is re-read by `git ls-remote` in the launcher, which refuses on a mismatch.**

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 00:46
Self-check note: Tuesday read the header, the rulings, §§4-9 and §11-13 whole and the drafter's WRONG list, and ADDED ruling (h) at stamp: the stale-parent ids (image-content-exposure pair) are accounted under C-133 on blobs, which SUPERSEDES "predicted missing 0". Tiers are Tuesday's; the RD-686 round cap goes to Kam.

## TUESDAY'S RULINGS (the commission; carried verbatim in substance — the gate applies them, it does not re-rule them)
- **Tiers.** **RD-618 is TIER 1** (Tuesday's ruling: the CSP report intake is an unauthenticated input surface; the builder also suggested tier 1, READY
  :5). **RD-628 is TIER 2, through-code** (comments-only in `backend/encryptionService.js` plus golden-blob cells — **verify the comments-only claim AT
  SOURCE**; if it changes ANY executable line, that is a finding and a WRONG item). **RD-652 is TIER 2.** **RD-646 + RD-647 is TIER 1** (a boot-behaviour
  change: with Redis configured and down, a boot at main EXITS; at `608a1cd` it stays up and answers 503).
- **(a) THE CROSS-CHANGE CELL — the reason A-D are gated together.** RD-618's narrowed CSP error handler and RD-646/647's census interact on
  `POST /api/csp-report`. **On a merged tree holding BOTH `4334b96` and `608a1cd`, RD-646's census (CENSUS-B and CENSUS-M) must see the named 503 on
  `POST /api/csp-report` with Redis down.** The builder's script `session-tools/s86m/mx618x646.sh` exists (read it; the gate may run a copy of its logic
  or its own — §8 says why not the script itself). **And at `7e4cd2e` (RD-618's OLD head) merged with `608a1cd`, that cell must go RED** — the positive
  control that the interaction is real. **Merge-tree cannot see this; only a run can.**
- **(b) Main is now `40b7eae`, not the heads' base (`1904765`). Main WILL MOVE during the gate:** NexusAI-M is merging batch 5a/5b (RD-681, RD-627b,
  RD-682, RD-705, RD-695, RD-413, then C-170, RD-696, RD-594) and NexusAI-P is merging batch 6. **Pin M0 at your start by `git ls-remote` and say so;
  re-read main at start, mid and end, as the 5b gate did.** Never re-base mid-gate.
- **(c) C-57 on the merged tree of the members (E joins as "docs, no test ids"):** predict the id set; **any missing id is named with its file's blob history (C-133's mechanical test),
  never assumed.**
- **(d) RD-652 KEEPS the `NODE_ENV` default** (Tuesday ruled it, C-173; the READY cites it). **Check it keeps the default and only adds a WARN.**
- **(e) The gate NEVER merges and never pushes. Findings only.** Merges exist ONLY inside your own scratch clones, as the merged-tree measurement (§9);
  nothing is merged into anything the fleet can see, and nothing leaves your clones.
- **(f) STANDING (a hung jest held the NexusAI lock for 4.5 h on 2026-09-28): every jest run inside a hold gets `--forceExit` AND a hard deadline, and
  every mutated file is restored in a `trap … EXIT`.** This brief makes it H-20 and H-21 (§3a). A run that hits its deadline is ABORTED and reported,
  its restore proven by hash, and the lock released by your own wrapper's exit — never waited on.
- **(g) RD-686 round 2 of 2 (Tuesday's mid-draft message): TIER 2, through-code, WORDS ONLY** — `docs/BRAND.md` +15/−7 over the gated `8962a14`.
  **The question: are the three rewritten claims (F-E1, F-E2, E8 from the batch-6 gate) now TRUE of the gate code they describe** —
  `__tests__/helpers/css-colors.js` :202/:204, `__tests__/brand-token-conformance.test.js` :116/:140/:149/:265, `scripts/derive-brand-tokens.js`
  `LIGHT`'s 20 values? **Re-read each cited line AT THE HEAD, never from the READY.** **ROUND CAP: a NO GO goes to Kam, not to a round 3.** In the
  merged-tree C-57/C-68 step it joins **only as "docs, no test ids"**; its C-68 set is **the 10 `BRAND.md`/`css-colors.js` readers** the READY names.
- **(h) ADDED AT STAMP by Tuesday — SUPERSEDES "predicted missing 0" in the C-133 bullet (THE CLARIFICATIONS) and in §9.6.** Every member branches from `1904765`, and main has since RENAMED test ids those heads still carry at their old titles. **Predicted missing at M0 = `40b7eae`: at least the two `__tests__/image-content-exposure.test.js` titles RD-418 renamed on main (`8de8e5c`; blob `94e6e4c` at `1904765` and at the heads, `9ede5fd` on main).** NexusAI-N hit exactly this pair on batch-3 merges 1 and 2 (2026-09-28), and Tuesday confirmed the accounting at source: the C-133 mechanical test holds on blobs (only main changed the file since the base; merged = main's blob). **Ruling: a missing id is ACCOUNTED (not a STOP) when C-133's blob test holds AND the new id is present and green on the merged tree; any missing id that fails either condition is a STOP.** If M0 has moved further (the 5a/5b merges), compute the same test for every missing id. List every one, id by id, with blobs and history.
- **Launch order:** as gate slots free; the launcher re-pins heads at launch and reads main as it finds it.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did
not build these changes and you owe no builder anything. **Every line below that reports what a builder says is a CLAIM, never evidence.** Explore a
branch that narrows and extends the ANONYMOUS CSP report intake (A), a comments-plus-golden-blob change beside the storage encryption (B), a boot WARN
(C) and a fail-closed rate-limit store with self-recovery (D), looking for any state in which **an anonymous caller gets something into the log or the
ring buffer it should not (a forged URL's userinfo or token, the raw body), one request floods the violation ring, a limiter error is reported as the
wrong thing, a Redis outage lets a rate-limited `/api` route through or kills the process, the app fails to recover when Redis returns, a comment
change hides an executable change, a stored secret stops decrypting, the development default silently moves, or a "guarding" cell stays green while
the thing it is named for is broken.**

- **RD-618 is TIER 1** (the anonymous intake). Verdict: **GO / GO WITH FINDINGS / NO GO at `4334b96`**, plus its merged-tree result.
- **RD-628 is TIER 2 (through-code)** (comments + cells; the property pinned is security-relevant: existing secrets keep decrypting). Verdict at **`a5799f3`**, plus merged-tree result.
- **RD-652 is TIER 2** (one boot WARN, default kept). Verdict at **`09e2e6a`**, plus merged-tree result.
- **RD-646 + RD-647 is TIER 1** (boot behaviour with Redis configured and down: exit → stay up and 503). Verdict at **`608a1cd`**, plus merged-tree result.
- **RD-686 is TIER 2 (words, round 2 of 2)** (a doc that states what the brand gates read). Verdict at **`ab12726`**, plus merged-tree result. **ROUND
  CAP: NO GO → Kam.**
- **One verdict PER ticket, one report, one mail.** A finding on one ticket never becomes another's verdict. **A finding that exists only in a
  COMPOSITION (above all §8) is graded on the merged tree and named against BOTH tickets' merged-tree lines.**
- **TIER 1 AT FULL WEIGHT, FINDINGS-ONLY:** no fixes, no pushes, no deploys, nothing to Partner Center, the demo or production (§12).

## THE CLARIFICATIONS THAT BIND THIS GATE (opened by the drafter at source, ~00:28–~00:30 AEST)
File: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md` (330,055 bytes, 1917 lines, mtime 2026-09-28 16:16;
the last numbered entry by `grep -n` is C-186 at :1911 — re-read line numbers, the file grows during the day). **The drafter opened ONLY these:**
- **C-57** (:416) — *"A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control. Any
  other conflicting file still stops."* Control: *"The merged set must be a superset of the union of the parents' sets … Any missing id stops the merge."*
- **C-68** (:663) — a verdict holds only at its head; when product code a cell reads changes before merge, the condition is RE-RUNNING THE AFFECTED
  CELLS by name; *"a clean merge-tree and a changed measured surface are not in tension, and the clean result is what makes the change invisible."*
  **§8 is exactly this case.**
- **C-89** (:833) — after a merge commit: `git diff --quiet HEAD` holds and `git show HEAD:scripts/verify-expected-counts.json` equals the regenerated numbers.
- **C-133** (:1432) — base-aware accounting: a missing id is ACCOUNTED only when *"(1) the merged blob is byte-identical to one parent's blob; (2) since
  the merge base, ONLY that parent changed the file, and the other parent's blob equals the base blob"*; the C-112 control beside it; **"Not covered: …
  short-lived branches (plain C-57 applies unchanged)"**; and its **ADDENDUM** (an authorised rename, old->new named, new id present and green). **These
  five are short-lived branches: plain C-57 applies — predicted missing 0 (§9.6); any missing id is a STOP, named with C-133's blob test anyway (ruling c).**
- **C-141** (:1486) a builder's proof ticket YIELDS to a `qa-*` ticket; ADDENDUM (a MERGE hold is gate-class); ADDENDUM 2 (once per waiting gate
  ticket); ADDENDUM 3 (self-applied); **ADDENDUM 4** (a yield re-queues directly behind with `--after`).
- **C-173** (:1775) — *"**RD-652:** KEEP the default (unset NODE_ENV means development). Add a loud boot WARN only (tier 2). Changing the default is out of scope."*
- **C-179** (:1854) — RULED BY KAM: *"Decision nexusai-redis-down-revisit-after-resubmission: a — Fail closed, fix the log line and the never-recovers bug (recommended)"*;
  build: keep failing closed; the startup log no longer says "falls back to in-memory"; recovery without restart. *"Red proof: a real
  Redis stopped and started (docker, through the docker lock), plus a control that the Marketplace configuration, which has no Redis, is unaffected."*
  *"Not covered: multi-replica behaviour (`maxReplicas` is pinned to 1, C-58), and RD-650's SCIM limiter store (its own ticket)."*
- **C-184** (:1895) THE MERGE-TURN RULE (one merge author at a time; read the queue for `merge` tags before a forward merge) — **why main moves in
  steps during your gate.** **C-185** (:1904) main's CI known-failing set is `{rd638-export-always-ends E2}` BY NAME until RD-723 merges; any OTHER
  failing cell is a STOP. **C-186** (:1911) after a push, the next merge ticket waits for that push's CI Build; turn order **O, P, M, N**.
- **Not opened by the drafter, so not cited:** every other C-number. Where the 5b brief's standing rules (C-102 early returns, C-104 never census an
  unresolved merge, C-110 floor rule, C-112 declared limits, C-122 source text vs behaviour, C-125 foreign-server counter, C-150 blobs decide, C-174
  never kill by pattern) are carried into §3a/§3b/§11 below, **they are carried from that brief, not re-read here — open them yourself before relying on
  their wording.**

## PRIOR ROUND
PRIOR ROUND (RD-618): the **gate 2** gated RD-495 (+RD-498) at `179bf603cf563013ac9f89dbc7b1e216e8a9d385`, verdict **GO** with open findings F-A1..F-A7.
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-gate2-rd495-rd525-rd575/report.md`
(summary :16; F-A1 :152; F-A2 :179; F-A3 :183; F-A5 :196; F-A4 :217; table :356-361). Findings carried forward and their disposition:
- **F-A2** (Polish, MEASURED there): Reporting-API reports stored as EMPTY entries; *"noise in a 500-entry ring that an anonymous caller can refill at
  60/min per address"* → RD-618 claims PARSED (and empty ones REFUSED 400). **Measure the ring-refill question again under the new parse (row s6).**
- **F-A3** (Minor): the stripper cut only at a literal `?`/`#` and kept userinfo → RD-618 claims userinfo dropped, `%3F`/`%23` cut, `blob:` inner URL stripped.
- **F-A4** (Polish, READ ONLY): stale "registered above requireAuth" comment → RD-618 marks it HISTORY.
- **F-A5** (Polish, PROBED in bare node): V8's parse message echoes ≤ ~10 leading body characters into the error log → RD-618 claims a fixed log line.
- **F-A1** (Minor): the readout refuses everyone in setup-open states — **left out by Tuesday's ruling** (READY :5 "F-A1 is left out by your ruling
  (C-178 addendum)"; the drafter did NOT open C-178 for this brief — RELAYED). Not re-opened.

PRIOR ROUND (RD-646 / RD-647 / RD-652): the **gate 7 round 2** named all three as **known, ruled residuals** (not exercised).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-23-gate7r2-rd645-rd641/report.md`
(:86 "An UNSET `NODE_ENV` gets 50 — deliberately not asserted (C-147, residual RD-652)"; :126 "Redis-down behaviours (RD-646 / RD-647) are known, ruled
residuals"; :242 "Redis-down behaviour of the auth limiter | NOT RUN"; :246; :271). Nothing to carry but the context: **RD-645's auth limiter is one of the
limiters RD-646 now fails closed** — its cell file `__tests__/rd645-auth-limiter-mounted.test.js` joins D's C-68 set.
PRIOR ROUND (RD-628): the **gate 5** raised **F-B2** (the machine-id source and how guessable it is, Major for the affected deployment shapes, READ ONLY
plus one PROBED line; *"owner: encryption/key management, the RD-628 / F-05 area"*).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/report.md` (:320).
RD-628 does NOT claim to address F-B2 (it corrects a false comment and pins the two derivations) — **say whether anything in `a5799f3` bears on F-B2;
do not re-grade F-B2.**
PRIOR ROUND (RD-686, round 1 of 2): the **batch 6 gate** gated RD-686 (+ RD-694 items 1-3) at `8962a149798531b61eddd22361dec1261a372f4e`, verdict
**NO GO** ("words only; three phrases to correct").
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch6/report.md`
(verdict :13; why NO GO :18; F-E1/F-E2 :21; §7 RD-686 :150-163 — the E1..E8 + e9 claim table; recommendation 1 :213). Its brief:
`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-gate-batch6-rd693-rd286-rd204-rd197-rd686-rd692.md`
(U7 :383-386 — the 10 readers). Findings carried forward and their disposition:
- **F-E1 (Major, unsafe direction):** "`dark-mode.css`: every colour" — MEASURED false: an off-token SECOND `rgba()` in a declaration (E1A) and a NAMED
  colour `fuchsia` (E1C) both pass 24/24 → round 2 rewrites the words (the gates are unchanged; RD-722 holds the gate-side fix). **Re-run E1A and E1C
  and show the NEW words predict both greens.**
- **F-E2 (Major, unsafe direction):** "pins how often each TOKEN value occurs" — `#00719f` (brand-chrome, 48 light uses) has no pinned count, +1 passes
  (E2A) while +1 `#0096d6` fails (E2B) → round 2 says "each MEASURED token value (the 20 values in `LIGHT`)". **Re-run E2A/E2B.**
- **E8** (the closing sentence overclaimed, part of F-E1/F-E2) → round 2 narrows it.
- **E3-E7 and e9 were TRUE** at round 1 and round 2 does not touch them (READY :20 "section 6 … kept byte-for-byte") — confirm by the diff, do not re-measure.
- **Reuse its probe BY COPY:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch6/evidence/qa-b6-686-probe.js`
  and its `e-probes.txt` (named in its §7).

PRIOR ROUND (method): the **batch 5b gate** is the most recent lane-1 gate and the source of the instruments.
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch5b/report.md`
(verdicts §0; H-rules §2; full verifies §11 — each **~18 min** on this machine, through the lock, SESSION_SECRET UNSET, a fresh short TMPDIR each; floor
§14 — one hold, 2 h 55 min, 175 HB lines, max gap 61 s; self-corrections §15 S-1..S-9). Its C-F1 matters here: **K2's source-regex population is blind
to routes on the `afterAuthGate` router, indented, double-quoted or split routes** — RD-646's census uses the same kind of regex (row r7).
**Reuse its instruments BY COPY** from `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch5b/evidence/`:
`qa-floorlib.sh` (**its `ROOT`/`NEG` defaults are STALE again — correct BOTH**), `qa-floorcount.py`, `qa-to.sh` (the per-step deadline: `perl alarm`, rc
142 = fired; **macOS has no `timeout` binary** — 5b §15 hit that), `qa-holdlib.sh`, `qa-jestwrap.sh`, `qa-runj.sh`, `qa-mutate.py`, `qa-merge.sh`,
`qa-c57-id-superset.sh`, `q-merged-identity.py`, `qa-ssprint.sh`, `qa-h1-selftest.sh`, `qa-h1-scan.py`, `qa-netbelt.sb`, `qa-netbelt-ctl.js`,
`qa-srvlib.js`, `qa-k-population.js`, `qa-lockcheck.js`. The original counter is gate 7's
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`.
- **Concurrent gates/merges, read for context, NOT re-run:** batch 5a (`2026-09-27-gate-batch5a`) and 5b are GATED and MERGING; batch 6 is MERGING
  (NexusAI-P's `s86p-merge-1-rd286` was in the jest queue at 00:20:30 AEST (`ps`), pid 24342, base `40b7eae`). Any of them may move main during your gate.

## 1. Targets — verified at drafting from the object store (00:18–~00:34 AEST)
**origin by `git ls-remote` at 2026-09-29 00:18:41 AEST (call ended 00:18:44):** `main` **`40b7eaeac70016f734b54f49c62e3be8398d4245`** ·
`rd-618-csp-intake-residue-s86m` **`4334b96d91132d933bc30b6b8dbd63e2031552cc`** · `rd-628-two-machine-id-derivations-s86m` **`a5799f3ba444fba82b8f8f34529b5493751a9b48`** ·
`rd-652-node-env-unset-warn-s86m` **`09e2e6accf172f574dec22bdaedc47e104076edd`** · `rd-646-647-redis-fail-closed-recovers-s86m` **`608a1cd99adcc69f6d2cdc552f170e89710adb02`**
(each = Tuesday's commission). **Re-read at 00:31:38–00:31:41 AEST** for member E: `rd-686-694-brand-wording-s85p`
**`ab1272678fe40e23cff86ff749601572dc8cb64b`** (= Tuesday's message), main still `40b7eae`. Also at origin then (NOT members): 5a's `rd-705-no-store-authenticated-pages-s86m` `e164d1a`, `rd-681-clear-undecryptable-s84m`
`4209299`, `rd-627b-sigterm-flush-s84m` `c82aa92`, `rd-682-clear-partial-audited-s84m` `f15fed6`, `rd-695-stats-trend-undated-s84m` `ad97d12`,
`rd-413-truthful-mail-secret-storage-s84m` `f70594a`; 5b's `rd-460-pkg-into-main-s84m` `be0fe37`, `rd-696-listen-remedy-cells-s84m` `2c221fa`,
`rd-594-kv-identity-open-window-s86m` `c7fbf33`; lane 2's `rd-424-backup-after-write-s84n` `2ce26eb`. **None of them was an ancestor of `40b7eae`**
(`merge-base --is-ancestor`, rc 1 each). Every sha is a commit in the local object store (`cat-file -t`).
**Other pinned shas, in full:** the heads' base `1904765007e9447ac6c980f9840c0689a02abe6c` (1904765) · RD-618's OLD head `7e4cd2efd7f4f2ff28bbf6fb9cd07be02789240d`
(7e4cd2e; parent `1904765`; `4334b96`'s only parent).
**Re-read at your start, mid and end. A moved TICKET head is a finding and a reason to stop, never a typo to fix.**

**Main may move during your gate (ruling b).** Call main at your start **M0**. (1) M0 must be `40b7eae` or a DESCENDANT of it (the launcher refuses
otherwise); (2) `git diff --name-only 1904765 M0` must share NO path with any member's delta **except `scripts/verify-expected-counts.json` and
`backend/server.js`** — the 5a merges ALL change the server entry point (MEASURED: each of the six 5a heads differs from its merge-base with main in it),
so the launcher does NOT refuse on it; instead it re-measures merge-tree M0 × each member in a scratch object dir (guard 80b) and refuses on anything but
counts-only. **Re-measure it yourself.** (3) Your merged tree is **M0 + A + B + C + D**, predicted counts **counts(M0) + 26 tests / + 4 suites
(4217/256 at M0 = `40b7eae`, which is 4191/252)**; (4) **if M0 moved and changed the server entry point, BOTH populations change** — K2's (RD-594's, if
its cell file is in M0) and RD-646's census — **measure both on M0 and on the merged tree and name any new route**; (5) if main moves AGAIN during your
gate, your verdict names M0 and says what moved (C-68). **Never re-base mid-gate.**
**Main's movement `1904765..40b7eae` (MEASURED, 14 paths):** `.dockerignore`, `Dockerfile`, `__tests__/helpers/image-manifest.js`,
`__tests__/helpers/rd703-parked-NOT-RUN/rd699-be-run-glue.test.js`, `__tests__/image-content-exposure.test.js`, `__tests__/rd324-ledger-guard-union.test.js`,
`__tests__/rd327-build-digest-on-public-health.test.js`, `__tests__/rd385-shipped-root-markdown-identifiers.test.js`, `__tests__/rd418-dockerignore-round3.test.js`,
`__tests__/rd684-redrive-keeps-surviving-target.test.js`, `__tests__/rd698-mixed-encoding-file.test.js`, `__tests__/rd699-decode-branches-behaviour.test.js`,
`backend/dataErasure.js`, the counts file. **∩ every member delta = the counts file only; the server entry point is blob `bc099b2` at both `1904765` and
`40b7eae`** (so at M0 = `40b7eae` the members apply to exactly the server source they were built on).

### TARGET A — RD-618 (TIER 1) @ `4334b96`
- **Chain (MEASURED):** TWO commits over `1904765`: `7e4cd2e` (parent `1904765`, 2026-09-28 12:54:33 +1000, "RD-618 F-A2..F-A5: the anonymous CSP intake
  stores only real reports and never logs what a forged report carries") → `4334b96` (parent `7e4cd2e` only, 23:01:59 +1000, "RD-618: the CSP intake's
  error handler answers only body-parser's own entity.* errors; anything else keeps its own status (Tuesday 2026-09-28T11:17:37Z)"). `merge-base(4334b96,
  40b7eae) = 1904765`.
- **Delta over `1904765`: 4 files, +219/−17** — `A __tests__/rd618-csp-intake-residue.test.js`, `M backend/server.js`, `M backend/services/cspReport.js`,
  `M scripts/verify-expected-counts.json`. **`7e4cd2e..4334b96`: 3 files, +21/−4** (the handler, the cell file (R5 added), counts). Blobs: server
  `bc099b2` → `20309de` (7e4cd2e) → **`c5bd870`**; `cspReport.js` `f102d26` → **`fa868ea`** (both commits). Counts **4133/247 → 4141/248 (7e4cd2e) →
  4142/248** (+9/+1).
- **What changed (READ at `4334b96`):** the intake route (server entry point, registered ABOVE `app.use('/api/', generalLimiter)`; its own limiter
  `cspReportLimiter` runs BEFORE the JSON parser) now parses `application/reports+json`, stores one entry per `csp-violation` report in an array, answers
  **400** and stores nothing when no entry has any violation field, and still answers 204 when `buildCspEntries` throws. A route-level error handler
  `app.use(CSP_REPORT_URI, (err, req, res, next) => …)` answers ONLY `err.type` starting `entity.` (413 for `entity.too.large`, else 400, one fixed log
  line) and passes everything else on with `next(err)` to the GLOBAL handler, which answers `error.statusCode || error.status || 500` (READ, merged file
  :22513). At `7e4cd2e` the same handler answered EVERY error: `(err.status || err.statusCode) === 413 ? 413 : 400`. `stripQueryAndFragment` rebuilds a
  PARSEABLE URL as protocol + host + path (userinfo, search, hash dropped), cuts the path at `%3F`/`%23` (either case), recurses into `blob:`; a value
  that does NOT parse as a URL keeps the old literal cut plus the encoded cut. The RD-495 comment near the readout is marked HISTORY (F-A4).
- **Cells (READ):** S1-S4 (the stripper, S4 a control on the RD-495 shapes), R1-R5 (one booted server via `helpers/rd395-server-harness`, `RATE_LIMIT_MAX`
  20000, `jest.setTimeout(240000)`); R5: an unsupported charset → body-parser `charset.unsupported` (415, NOT `entity.*`) → 415, no "not valid JSON", nothing stored.
- **Builder's claims (RELAYED):** red at base 6/8 (S1 S2 S3 R1 R2 R3); green 8/8; M-A3 → S2, S3; M-A2 → R1; M-A5 → R3 (`session-tools/s86m/rd618-h4.log`);
  then R5 red with `7e4cd2e`'s server source, 9/9 green, M-R5 (the entity guard removed) → R5 red (`session-tools/s86m/rd618b-hold.log`, `rd618b-hold.sh`);
  verify **4142/4142 across 248**; merge-tree counts-only vs main and the lane-1 heads.
- **NOT TESTED — VERBATIM (first READY :33-36; the new READY says "Everything else in that READY stands"):**
  *"- A real browser sending a Reporting-API report. The cells POST the documented shape."* ·
  *"- The 16 KB cap boundary exactly (unchanged; the gate recorded it as not bracketed)."* ·
  *"- The demo."*
  → **L-A1** (a real browser's Reporting-API report) · **L-A2** (the 16 KB cap boundary — bracket it if cheap, row s8) · **L-A3** (the demo).

### TARGET B — RD-628 (TIER 2, through-code) @ `a5799f3`
- **Chain (MEASURED):** ONE commit, parent `1904765` only, 2026-09-28 14:23:18 +1000, "RD-628: encryptionService's machine-id key is NOT jsonStorage's;
  say so, and pin a golden blob from each". **Delta: 3 files, +105/−12** — `A __tests__/rd628-two-machine-id-derivations.test.js`, `M
  backend/encryptionService.js` (`31fd8a4` → `e449589`), `M scripts/verify-expected-counts.json`. Counts **4133/247 → 4136/248**.
- **The comments-only claim — MEASURED by the drafter, twice:** (1) `git diff -U0 1904765 a5799f3 -- backend/encryptionService.js`: **0** changed lines
  that are not comment lines (every `+`/`−` line starts with `*`, `//` or `/**`); (2) node, both blobs with block and line comments stripped and whitespace
  collapsed: **code-equal = true**; control in the same run (a one-identifier edit to the base) **= false**. **So the executable text is unchanged — re-prove
  it with your own instrument AND with a stronger one (an AST/token comparison, e.g. `node --check` plus a tokenizer, or the module's exported function
  bodies compared via `Function.prototype.toString` after comment strip), with its own control.**
- **What the comments now say (READ; verify each against the code):** encryptionService salts PBKDF2 with the literal `'nexusai-storage-encryption-salt'`
  (`:56` `const SALT = …`, used `:120`); `jsonStorage.deriveKeyFromMachineId` salts with `sha256('printer-dashboard-salt-v1')` (`backend/jsonStorage.js`
  `:60-62` at `a5799f3`); "in KV mode jsonStorage takes this module's DEK (getDek)" — READ at `jsonStorage.js :85-97` (`enc.getDek()` then machine-id
  fallback); "in env-key mode both read STORAGE_ENCRYPTION_KEY" — **verify at source, not by the comment** (C-122's point).
- **Cells (READ at `a5799f3`):** G1 (encryptionService.decryptValue reads a golden blob), G2 (JsonStorage.getSetting on a real store whose `.machine-id`
  holds the synthetic id), CTRL (each refuses the other's blob). The ENV scrub deletes `STORAGE_ENCRYPTION_KEY`, `LEGACY_STORAGE_ENCRYPTION_KEYS`,
  `KEYVAULT_NAME`, `KEYVAULT_KEY_NAME` — **but NOT `LEGACY_MACHINE_IDS`**, which `jsonStorage.getEncryptionKeyCandidates` reads (`:150-158`) — row g5.
- **Builder's claims (RELAYED):** 3/3; M1 (encryptionService uses jsonStorage's salt) → G1 + CTRL red; M2 (the reverse, in `jsonStorage.js` transiently)
  → G2 + CTRL red (`session-tools/s86m/rd628-h4.log`); verify **4136/4136 across 248**. C-68: *"When rd-424 (backup after write) merges, G2 is re-run by
  name on that tree."* — **MEASURED: `rd-424-backup-after-write-s84n` @ `2ce26eb` DOES change `backend/jsonStorage.js`** over its merge-base with main.
- **NOT TESTED — VERBATIM (READY :35):** *"NOT TESTED: Key Vault mode (getDek), and a real pre-RD-616 volume. Neither is what these cells pin."*
  → **L-B1** (Key Vault mode / getDek) · **L-B2** (a real pre-RD-616 volume).

### TARGET C — RD-652 (TIER 2) @ `09e2e6a`
- **Chain (MEASURED):** ONE commit, parent `1904765` only, 2026-09-28 20:58:02 +1000, "RD-652: warn loudly at boot when NODE_ENV is unset (the development
  default is kept, C-173)". **Delta: 3 files, +73/−3** — `A __tests__/rd652-node-env-unset-warns.test.js` (60 lines), `M backend/server.js` (**+10/−0**,
  `bc099b2` → `c2e645a`), `M scripts/verify-expected-counts.json`. Counts **4133/247 → 4136/248**.
- **Ruling (d), MEASURED by the drafter:** the server-source diff is ONE insertion block of 10 lines directly after `require('dotenv').config();` (6
  comment lines, a 3-line `if (!process.env.NODE_ENV) { logger.warn('⚠️  NODE_ENV is not set, so this server runs in DEVELOPMENT mode …'); }`, one
  blank) and **nothing else**; the default line `process.env.NODE_ENV = process.env.NODE_ENV || 'development';` is present **byte-identical** at `1904765`
  (:973) and `09e2e6a` (:983) under the comment "Set NODE_ENV to development if not set". `logger` is required at :41, before the WARN. **Re-prove it
  (w1-w3).** No `.env` is tracked at `09e2e6a` (only `.env.example`, blob `b3dd6ee`).
- **Cells (READ):** W1 (`NODE_ENV` EMPTY → the WARN and the fix named), CTRL-DEV (explicit `development` → no WARN), CTRL-PROD (`production` → no WARN);
  three boots through the harness, `jest.setTimeout(420000)`. **Declared limit (READY :21):** *"the harness always passes a NODE_ENV, so 'unset' is
  exercised as EMPTY."* — row w4 drives a TRULY unset one.
- **Builder's claims (RELAYED):** red at base (W1 red, controls green); 3/3; M1 (warn on every boot) reddens both controls (`rd652-h4.log`); the pre-commit
  gitleaks hook refused a literal SESSION_SECRET; re-run on the EXACT committed tree 3/3, verify **4136/4136 across 248** (`rd652-rerun.log`); a push
  briefly created the branch at `1904765` (disclosed).
- **NOT TESTED — VERBATIM (READY :32):** *"NOT TESTED: a real .env file setting NODE_ENV (the ordering is read, not driven); Windows."*
  → **L-C1** (a real `.env` setting NODE_ENV — drive it once in your extract if cheap, row w5) · **L-C2** (Windows).

### TARGET D — RD-646 + RD-647 (TIER 1) @ `608a1cd`
- **Chain (MEASURED):** ONE commit, parent `1904765` only, 2026-09-28 21:15:25 +1000, "RD-646 + RD-647 (Kam, C-179): with Redis configured, rate
  limiting fails CLOSED while Redis is unreachable, says so truthfully, and recovers by itself". **Delta: 4 files, +474/−24** — `A
  __tests__/helpers/rd647-restartable-proxy.js`, `A __tests__/rd646-647-redis-fail-closed-recovers.test.js` (299 lines), `M backend/server.js` (`bc099b2` →
  `4ddf75f`; two hunks, both in and just above `setupRateLimitStore`), `M scripts/verify-expected-counts.json`. Counts **4133/247 → 4144/248** (+11/+1; the
  helper is not a suite).
- **What changed (READ):** a named error `rateLimitStoreUnavailable()` — `statusCode 503`, `code 'RATE_LIMIT_STORE_UNAVAILABLE'`, `userMessage` naming Redis
  and `REDIS_URL / REDIS_HOST` — and **no `.type`**; a per-limiter wrapper store that throws it while `!client.isReady`, builds the real `RedisStore` only once
  ready, swallows the constructor's SCRIPT LOAD rejections, never throws from `decrement`/`resetKey`; `reconnectStrategy` backoff (250 ms … 5 s),
  `disableOfflineQueue: true`; one error line per outage; a client library that cannot load fails closed too. **No Redis configured is unchanged
  (in-memory).** The global handler returns `userMessage` only in production; in development it returns `message` and `code` (READ, `sanitizeErrorForClient`).
- **Cells (READ):** B1, CTRL-LIVE, CENSUS-B, B2 (Redis DOWN at boot); M1, M2, CENSUS-M, M3, FAITHFUL (drop mid-run and return); M4 (a command cut
  mid-flight); CTRL-MEM (no Redis). Servers spawned `NODE_ENV=production`, fresh DATA_DIR/HOME, `RATE_LIMIT_MAX 20000`; the fake Redis is RD-607's
  (`__tests__/helpers/rd607-fake-redis.js`) behind the new restartable proxy. `jest.setTimeout(300000)`; `afterAll` TERMs then KILLs its children.
- **THE CENSUS (READ, the cell's own code):** population = every `^app\.(get|post|put|delete|patch)\('(\/api\/[^']*)'` literal in the server entry point
  (`:params` → `rd646x`, `*` routes skipped) **plus six**: `PROBE_PATHS.live`, `PROBE_PATHS.ready` (from `bootPreflight`'s export), `POST /api/csp-report`,
  and the router mounts `/api/feedback`, `/api/setup/entra-provisioning`, `/api/sustainability/kpis`. **Drafter's reproduction: 153 literals, 152 unique
  method+path, + 6 = 158** (= READY's "158 routes"), **unchanged at `1904765`, `40b7eae`, every member head, every 5a head, and the `4334b96` × `608a1cd`
  merge-tree result.** Each route is driven once, anonymously, non-GET with `Content-Type: application/json` and body `'{}'`, 10 s abort; **an offender
  is any status `!== 503` not on ALLOW** (ALLOW = `GET /api/live` only). **The census checks the STATUS, not that the 503 is the NAMED one** — only the
  LIMITED route (`/api/health`) is checked for the named message (B1, M2). **§8 requires the name on `POST /api/csp-report` too.**
- **Builder's claims (RELAYED):** red at `1904765`: B1, B2, CTRL-LIVE (boot exits), M2 (500), M3 (500); M1, FAITHFUL, CTRL-MEM green; green 11/11; MA
  (no reconnect) → B2, M3, M4; MC (raw errors) → M4; MD (the false log line) → B1 (`session-tools/s86m/rd646-h6.log`); **real Redis (docker
  `redis:7.4-alpine`)**: main mid-run 500 no recovery, boot exits; fix: named 503, 200 ~2 s after return, boot stays up (`rd646-real-redis.sh`); re-run on
  the exact committed tree 11/11, verify **4144/4144 across 248** (`rd646-rerun.log`); h4/h5 VOID (disclosed). Outside the census, stated: static HTML pages,
  and the SCIM limiter (no Redis store at all, RD-650).
- **NOT TESTED — VERBATIM (READY :48):** *"NOT TESTED: multi-replica (maxReplicas is 1, C-58); Linux/CI (no PR); a real container runtime's restart policy; Redis with TLS or AUTH; the SCIM limiter (RD-650)."*
  → **L-D1** (multi-replica) · **L-D2** (Linux/CI) · **L-D3** (a real container runtime's restart policy — and its HEALTHCHECK, row r9) · **L-D4** (Redis
  TLS/AUTH) · **L-D5** (the SCIM limiter, RD-650) · **L-D6** (drafter's addition, C-179's red proof: a REAL Redis — this gate runs **no docker** and the
  drafter found **no `redis-server` binary** on this machine (`command -v` → none); the real-Redis rows stay RELAYED unless one exists without installing
  anything).

### TARGET E — RD-686 round 2 of 2 (TIER 2, words) @ `ab12726` — ROUND CAP: a NO GO goes to Kam
- **Chain (MEASURED):** TWO commits over `1904765`: `8962a14` (round 1, parent `1904765`, 2026-09-27 02:05:52 +1000, "RD-686 + RD-694 (lane-4 parts):
  BRAND.md rule 3 and the css-colors.js header state what the brand gates actually read" — **gated NO GO by batch 6**) → `ab12726` (parent `8962a14`
  only, 2026-09-28 07:53:57 +1000, "RD-686 round 2 of 2: correct the three phrases the batch-6 gate measured false (F-E1, F-E2, E8), words only").
  `merge-base(ab12726, 40b7eae) = 1904765`; `8962a14` is NOT on main (RD-686 was held out of batch 6's merges, READY :28).
- **Round-2 delta `8962a14..ab12726`: 1 file, `docs/BRAND.md`, +15/−7** (= Tuesday's `--stat`). **What MERGES is both commits — delta over `1904765`:
  2 files, +62/−25: `M __tests__/helpers/css-colors.js` (round 1; blob `78bb004` → `bdb5ca3`, unchanged by round 2) and `M docs/BRAND.md`.** **The
  helper change is COMMENT-ONLY — re-proved by the drafter** (node comment-strip: code-equal = true; control false; batch 6's e9 found the same with the
  repo's own stripper). **No counts change** (the counts file is not in E's delta: 4133/247 at `8962a14` and `ab12726`); **no test id added or removed**;
  `brand-token-conformance.test.js` (`9cf6993`) and `scripts/derive-brand-tokens.js` (`d94423a`) are the SAME blobs at `1904765` and `ab12726` —
  **the gates did not change.**
- **The round-2 claims, re-read by the drafter AT THE HEAD (`ab12726`):**
  - `css-colors.js` :202 `if (FUNCTIONAL.exec(value)) functional.push(site);` — ONE functional site per declaration (`FUNCTIONAL` :53 is
    `/\b(rgba?|hsla?)\(\s*([^)]*)\)/gi`, `lastIndex` reset before one `exec`); :203 tests `NAMED` and :204 pushes to `named` (the READY says ":204
    collects named colours separately" — :203-204).
  - `brand-token-conformance.test.js` :116 `RGB_TRIPLE = /\b(rgba?)\(\s*(\d+)\s*[,\s]\s*(\d+)\s*[,\s]\s*(\d+)/i` — no `g` flag: the FIRST integer
    triple in the site's value; :149 `RGB_TRIPLE.exec(site.value)`; :153-154 `else if (/hsla?\(/i.test(site.value))` records `hsl()` UNCONVERTED —
    **only when the declaration holds NO rgb integer triple**; :140 `RGB_PROP_DECL` (`g`) reads every `--*-rgb` declaration; :265 asserts them; the
    file reads `.named` **0** times (control: `.functional` 1); :70-79 the light counts come from `generator.LIGHT`.
  - `scripts/derive-brand-tokens.js` `LIGHT` (the object literal from :69, evaluated in node from `git show`, nothing required): **20 entries, 20
    distinct values; `#00719f` NOT among them; control `#0096d6` present (`brand-blue`, count 54)** — the READY's probe VERIFIED.
- **The drafter's READ of where the NEW words may still overclaim (rows e4, e5 — measure; do not take this READ as a verdict):** (i) the new text keeps
  "an `hsl()` is recorded UNCONVERTED and fails by name" — READ at :149-154 that holds only for a declaration with no rgb triple: a declaration holding
  an off-token `hsl()` AND an on-token integer `rgba()` records the rgba and never the hsl; (ii) "the FIRST `rgb()`/`rgba()` of each declaration" —
  `RGB_TRIPLE` needs three INTEGERS, so a first `rgb()` written with percentages, decimals or `var()` is skipped and the next integer triple (or none) is
  read. **If either plant passes the real gate green and the words do not say so, the words are still not TRUE of the code — and at round 2 of 2
  that NO GO goes to Kam.**
- **Builder's claims (RELAYED):** each claim re-read at source on the head (READY :13-16); verify **4133/4133 across 247** (`session-tools/s86p/rd686r2-verify.log`,
  14:11:39Z-14:28:23Z; `--update-counts` changed only `_updated`, file restored, nothing committed); RD-199/RD-200 histories and §6 kept byte-for-byte.
  **Named on purpose, NOT changed (READY :22-24):** the test TITLE at `brand-token-conformance.test.js` :244 *"every rgba()/hsl() colour in
  dark-mode.css resolves to a token"* carries the same overclaim (renaming changes a test id, C-57/C-133) — listed on RD-722, which holds the gate-side
  fix (E1A/E1C/E2A as red-first cells). **Say whether a doc that is now true beside a test title that is not is a finding against RD-686 (words-only
  ruling) or only RD-722's; severity yours, disposition Tuesday's/Kam's.**
- **NOT TESTED — VERBATIM (READY :26):** *"NOT TESTED: the gate's E1A/E1C/E2A plants were not re-run by me (words-only round; the gates are unchanged,
  so their results cannot have moved). No browser leg (docs only). CI not run on the branch (no PR)."*
  → **L-E1** (E1A/E1C/E2A not re-run by the author — YOU re-run them, e1-e3) · **L-E2** (no browser leg) · **L-E3** (CI, no PR).
- **C-68 set (the READY :28 and batch 6's U7, READ):** the 10 `BRAND.md`/`css-colors.js` readers — `brand-chrome-contrast`, `brand-chrome-gradient-stops`,
  `brand-md-accent-count`, `brand-token-conformance`, `costs-header-solid`, `css-colors-stripper`, `light-active-tab-chrome`, `muted-4-16-attribution`,
  `primary-button-chrome`, `rd200-js-colour-corpus`. **Re-derive them** (`git grep -l -E 'BRAND\.md|css-colors' -- __tests__` in your clone, positive
  control `brand-token-conformance`). **If M0 carries batch 6's RD-286 (`1645c69`, it changes `static/css/dark-mode.css`), the brand readers measure a
  different sheet — run the 10 on M0 + E and say what moved.**

### File overlap and MERGE-TREES — MEASURED by the drafter in a scratch object dir (NexusAI's store as a read-only alternate), ~00:19–~00:33 AEST
Name sets over `1904765`: A (4), B (3), C (3), D (4). **`comm`: A∩C = A∩D = C∩D = {`backend/server.js`, counts}; A∩B = B∩C = B∩D = {counts}.**
**`git merge-tree --write-tree --name-only`** (objects in the drafter's own `mktemp -d` under its scratchpad): **all six member pairs, `7e4cd2e` × `608a1cd`,
and `40b7eae` × each member → exactly ONE conflicting path each, `scripts/verify-expected-counts.json`** (rc 1; `backend/server.js` "Auto-merging" clean for
A×C, A×D, C×D and `7e4cd2e`×D). **Each member vs every 5a head (rd-705, rd-681, rd-627b, rd-682, rd-695, rd-413), every 5b head (be0fe37, 2c221fa,
c7fbf33) and rd-424 → counts-only; vs rd-286 (`1645c69`, batch 6) → no conflict at all.** **E (`ab12726`, 00:32 AEST) shares NO path with any
member; merge-tree E × `40b7eae`, × each of A-D and × each batch-6 head (`ddf1b75`, `1645c69`, `fe47bb4`, `43e729c`, `4580829`) → rc 0, no conflict at
all** (E carries no counts file). Result trees (drafter's scratch only): `4334b96`×`608a1cd` =
`27c70ef999a5081234c565ea0d6d58a4e342c18d` (its server source `node --check` rc 0; `startsWith('entity.')` 1, `RATE_LIMIT_STORE_UNAVAILABLE` 4, the old
`=== 413` catch-all 0); `7e4cd2e`×`608a1cd` = `f0ee623a6986dd62efb1029bf8906ae497e59237` (parses; guard 0, catch-all 1). **The launcher's guard 80
re-measures every pair in a FRESH scratch object dir; re-measure them yourself (§9 Q1).**

### MERGE ORDER — the drafter's proposal, with its predicted end state and the C-68 re-run set per merge
**Proposed order: 1. RD-628 (B) → 2. RD-652 (C) → 3. RD-618 (A) → 4. RD-646+RD-647 (D) → 5. RD-686 (E, docs, no test ids).** (E is lane 4's and
merged by NexusAI-P, so in the fleet it merges in P's turn (C-186), not M's; in YOUR clone it goes last because it is independent of everything.)
Why: B touches no server source (cheapest, independent); C is a 10-line insertion far from the other hunks; A before D so that **the tree D lands on
already carries A's narrowed handler — the cross-change cell (§8) is then GREEN at D's merge rather than at some later one**; **D LAST, because its census
enumerates the whole `/api` population from the server source at run time — measure it on the tree that holds everything (C-68), exactly as 5b put RD-594
last.** The order is file-independent (every pair = counts, server source auto-merges), so **order independence is the control (§9.4), not an
assumption. Challenge it if any row says otherwise.** **Never merge `7e4cd2e`** — it is a positive-control tree only (§8).

| step | merge | predicted conflicts | predicted counts after (M0 = `40b7eae`) | C-68 re-run set BY NAME (on the tree after that step) |
|---|---|---|---|---|
| 1 | M0 + B | counts only | **4194/253** | rd628 + every suite that loads `backend/encryptionService.js` or `backend/jsonStorage.js`'s key path: `rd616-617-mail-secrets-at-rest-and-export-shapes`, `rd518-keyvault-identity-and-loud-fallback`, `marketplace-keyvault-durability` (if in M0), `rd150-falsy-settings-round-trip`, `rd407-concurrent-settings-writers` — **re-derive with git grep** |
| 2 | + C | counts only | **4197/254** | rd652 + every suite that asserts on the boot log or on `NODE_ENV` defaults: `rd408-r2-misconfigured-explains`, `rd408-r3-probe-endpoints`, `rate-limit-allowance`, `setup-rate-limit-allowance`, `rd645-auth-limiter-mounted` — **re-derive** |
| 3 | + A | counts only | **4206/255** | rd618 + `rd495-admin-routes-behind-the-gate` (A4-A7) + `rd607-redis-limiters-keep-their-own-counts` (R4) + every suite that POSTs to the CSP URI or reads `cspReport` — **re-derive** |
| 4 | + D | counts only | **4217/256** | rd646-647 (CENSUS-B/M on the MERGED population) + rd618 + rd495 + rd607 + rd645 + rd641 + `rate-limit-allowance` + `setup-rate-limit-allowance` + rd408-r3 (the probes) + **rd594 if its cell file is in M0** (K2, Tuesday's 5b ruling) — the builder's own C-68 names are rd607, rd645, rd495, rd594, rd641 (READY :46) |
| 5 | + E | **none** (E has no counts file; merge-tree rc 0 against M0 and every member) | **4217/256 (unchanged: docs, no test ids)** | the 10 `BRAND.md`/`css-colors.js` readers (TARGET E) |

**End state predicted: 4217/256 = 4191 + 3 + 3 + 9 + 11 + 0 / 252 + 1 + 1 + 1 + 1 + 0 at M0 = `40b7eae` — ARITHMETIC; re-base it on YOUR M0 (5b had to: main had
moved before its start); C-68 says the measurement decides.** **Re-derive every set in YOUR clone with a positive control** (the ticket's own cell file must
be found): `git grep -l -E 'encryptionService|deriveKeyFromMachineId|getEncryptionKeyCandidates|STORAGE_ENCRYPTION_KEY'`, `git grep -l -E
'NODE_ENV|dotenv'`, `git grep -l -E 'csp-report|CSP_REPORT|cspReport|reports\+json'`, `git grep -l -i -E 'REDIS|rd607-fake-redis|RATE_LIMIT|generalLimiter|429|503'`
over `__tests__` in your clone at M0; add what the table misses and say which.

### How to build your trees
- **No worktree is created in the NexusAI repo, and you never work in its `2_Project_Files` checkout.** In that repo use ONLY read verbs: `show`,
  `log`, `diff`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `grep`, `ls-remote`, `archive`, `count-objects`. Never `fetch`, `pull`, `push`,
  `checkout`, `worktree`, `commit`, `stash`, `gc`, `clean`, or `merge-tree --write-tree` without a scratch `GIT_OBJECT_DIRECTORY` of your own.
- **Head trees:** `git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/qa-trees/batch7.XXXXXX/>`, git-indexed where a full verify or a cell needs it.
- **The merged trees:** §9 and §8, in **your OWN scratch clones** (`git clone --shared --no-checkout <repo> <your own dir>`): `clone-1` (proposed order),
  `clone-2` (reverse order), `clone-x7e4` (M0 + `7e4cd2e` + `608a1cd`, the positive control — never anything else).
- **Each tree is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree for a clean arm; `batch7`-prefixed
  directories only. Earlier gates' trees are their evidence — copy from, never run in.
- `node_modules`: an APFS clone (`cp -c -R`) of the newest gate tree you trust, **after proving** `package-lock.json` is blob `9064763` there too (it is
  `906476350431e2ecb3c21070a25c64b1702c1aa8` at `1904765`, `40b7eae`, `7e4cd2e`, `4334b96`, `a5799f3`, `09e2e6a`, `608a1cd` — MEASURED); a real
  directory, never a symlink. **D's cells need the `redis` and `rate-limit-redis` packages from that `node_modules` (`package.json`: `redis ^4.7.0`,
  `rate-limit-redis ^4.2.0`, `express-rate-limit ^7.1.5`, `express ^5.1.0`) — prove they resolve before the first D run.**

## 2. Why these tiers, and who is waiting
- **RD-618 TIER 1:** anonymous, rate-limited at 60/min per address, reachable before sign-in. **Anything an anonymous caller can put into the log or the
  ring that RD-618 says it strips (userinfo, a query/fragment token, the raw body) is a Blocker on the product; one request that floods the 500-entry
  ring is a Major (F-A2's own concern); a limiter/store error reported as "not valid JSON" or as 400 is a Major (Tuesday's narrowing); a cell green
  while its named behaviour is broken is a Major (C-40, carried from the 5b brief).**
- **RD-628 TIER 2 (through-code):** **any executable change in `backend/encryptionService.js` is a Major AND a WRONG item** (the commission's condition);
  a golden blob that does NOT redden under the unification it exists to catch is a Major; a comment that states something false about the code is a Minor.
- **RD-652 TIER 2:** **the default moving (in value, place or condition) is a Major against ruling (d)/C-173**; a WARN that fires in a shipped
  configuration (production) or fails to fire when NODE_ENV is truly unset is a Minor; wording is Polish.
- **RD-646+647 TIER 1:** with Redis configured and unreachable, **any rate-limited `/api` route that answers anything but 503 (above all a 200 that
  serves data) is a Blocker; a process that dies (at boot or mid-run) is a Blocker; no recovery once Redis returns is a Major; a 503 that is not the
  named one, a log line that lies, or a leak of the library's message is a Minor; any change to the NO-Redis path (the Marketplace configuration) is a
  Blocker.** The boot change is by Kam's ruling (C-179) — **a compose healthcheck consequence is a note for Tuesday to relay, not a defect (row r9).**
- **The composition (§8):** **the census red on `POST /api/csp-report` on the merged tree is a Blocker for whichever of A and D merges second** — it is
  the exact semantic collision the builder named (RD-646 READY :46).
- **RD-686 TIER 2 (words, ROUND 2 OF 2):** **any rewritten claim that the real gate contradicts in the unsafe direction (the doc says a shape is
  caught and the gate passes it) is a Major and a NO GO — and at the round cap that NO GO goes to Kam, not to a round 3**; a claim true but imprecise
  in the SAFE direction is Polish; any executable change in `css-colors.js` is a Major (the words-only ruling).
- **Who is waiting:** the merge author for A-D is **NexusAI-M (S86M)** (pane `%19`, claude `62649` at 00:24 AEST), after batch 5a/5b under C-184/C-186's
  turn order; for E it is **NexusAI-P (S86P)** (pane `%22`, claude `20317`), after batch 6.

## 2a. LEGITIMATE SHAPES — required measurements, row by row (the checkers here are RD-646's census, RD-618's R-cells, RD-628's golden blobs and RD-652's controls)
**Columns: the head, the base it is measured against (M = `1904765`'s product, the heads' base; say also what M0 does where it differs), and the MERGED
tree. Every server row: your own extract, under the network belt, a fresh DATA_DIR, killed in a `finally` by pid.**

**X — the cross-change cell (A × D). THE REASON FOR THIS GATE. §8 has the method.**

| row | shape | expected | predicted-by |
|---|---|---|---|
| x1 | clone: M0 + `4334b96` + `608a1cd` (and the full merged tree of §9); rd646's CENSUS-B and CENSUS-M | **green; `seen['POST /api/csp-report'] === 503`**, 0 offenders | Tuesday (ruling a) + builder READING (r2 READY :23 "That is a reading, not a run") |
| x2 | the same, the 503 BODY on `POST /api/csp-report` (your own probe, same boot state as CENSUS-B and CENSUS-M) | production mode: JSON whose `message` names Redis AND `REDIS_URL`/`REDIS_HOST` (the named 503, `namesRedisAndFix`); **not** "not valid JSON" in the log; the global handler's `Server error:` log line carries `path /api/csp-report` | drafter (READ `sanitizeErrorForClient`) |
| x3 | **POSITIVE CONTROL: clone M0 + `7e4cd2e` + `608a1cd`** (the OLD handler); CENSUS-B and CENSUS-M | **RED, each with EXACTLY ONE offender `POST /api/csp-report -> 400`**, every other rd646 cell green; the log carries "CSP report refused (400): body is not valid JSON" for a request whose body was valid | builder (D's READY :46) + Tuesday (ruling a) |
| x4 | mutant on the x1 tree: the `entity.` guard line removed (M-R5's shape, one anchor) | CENSUS-B/M red exactly as x3 AND rd618's R5 red; everything else green | drafter (M-X4) |
| x5 | mutant on the x1 tree: the named error given a `type: 'entity.parse.failed'` (a copy of D's `rateLimitStoreUnavailable`) | CENSUS-B/M red on `POST /api/csp-report -> 400` — **proves the guard's discriminator is `.type` and nothing else** | drafter (M-X5) |
| x6 | x1 tree, Redis UP (M1's state): `POST /api/csp-report` with a valid report-uri body, a Reporting-API array, `{}`, and invalid JSON | 204, 204, 400 (no fields), 400 + the fixed log line — **D changes nothing about A's intake when Redis answers** | drafter |
| x7 | x1 tree, **no Redis configured** (the Marketplace configuration): the same four bodies | identical to x6 (in-memory limiter) — **CTRL-MEM for A** | drafter (C-179's control, applied to A) |

**S — RD-618's intake (A). At `4334b96`, at M, and on the merged tree.**

| row | shape | expected at `4334b96` | at M | predicted-by |
|---|---|---|---|---|
| s1 | the 9 cells, clean | 9/9 green | 3/9 green (S4, R4 and R5? — **measure; the builder's 6/8 red predates R5**) | builder |
| s2 | M-A3 / M-A2 / M-A5 / M-R5 re-derived independently | S2+S3 / R1 / R3 / R5 red, nothing else | — | builder |
| s3 | **userinfo in an UNPARSEABLE URL** (`https://user:pw@host:99999/x`, a space in the host, a `%zz` in the host): `new URL` throws → the literal-cut fallback | **the drafter READS the fallback keeping `user:pw@`** (`cutAt(cutAt(s,/[?#]/), ENCODED)`) — measure what reaches the log and the ring; if userinfo survives, F-A3 is only partly closed | drafter (READ) |
| s4 | **double-encoded** `?`: `https://h/p%253Ftoken=SECRET` | the `%3F` regex does not match `%253F` — predicted the token SURVIVES as `%253Ftoken=SECRET`; say whether that is a leak (it decodes once to `%3F…`) | drafter (READ) |
| s5 | `blob:` nesting: `blob:blob:https://u:p@h/p?q` and a deep nest near the 16 KB cap | stripped at every level; recursion bounded; no stack error, no 500 | drafter |
| s6 | **ring refill (F-A2's concern) under the new parse:** ONE `application/reports+json` array of N `csp-violation` reports just under 16 KB | **how many entries ONE request pushes** (predicted ≈ N, dozens) vs the 500-entry ring and 60 req/min — **the refill rate of the ring per minute before and after RD-618; a one-request flush is a Major** | drafter (READ `buildCspEntries`: no per-request cap) |
| s7 | a body-parser error that is NOT `entity.*` (`charset.unsupported`, `encoding.unsupported`, `request.aborted`) → the global handler | its status kept; **list what the global handler's `Server error:` log line carries — an attacker-chosen charset/encoding string?** (F-A5's shape moved elsewhere?) | drafter (READ: the global handler logs `error.message`) |
| s8 | the 16 KB cap: bodies of 16 383 / 16 384 / 16 385 bytes (L-A2) | 204/400 then 413 at the boundary the limit names | drafter (optional; say if bracketed) |
| s9 | R3's "raw body never reaches the log" — plant a body whose first 10 characters are a unique marker, invalid JSON | 0 occurrences of the marker anywhere in the server output (H-1-style scan with a planted-DIFFERENT-marker control) | builder + drafter |

**G — RD-628's golden blobs (B). Through-code; no server boot needed.**

| row | shape | expected at `a5799f3` | at M | predicted-by |
|---|---|---|---|---|
| g1 | the comments-only claim (ruling) | **0 executable changes**, by two independent instruments each with a control that fires | — | drafter (MEASURED) |
| g2 | the 3 cells, clean, and the cell file against M's product (tests only in effect) | 3/3 both | 3/3 | builder |
| g3 | M1 (unification one way) / M2 (the other way) re-derived | G1+CTRL / G2+CTRL red | — | builder |
| g4 | **a unification on BOTH sides at once** (both salts set to the same new value) | G1 AND G2 red (the golden blobs catch what fresh round-trips cannot) — **the cell's WHY, measured** | drafter |
| g5 | `LEGACY_MACHINE_IDS` and `LEGACY_STORAGE_ENCRYPTION_KEYS` exported in the runner's environment (the scrub omits the first) | cells unchanged? CTRL still refuses? — say whether the cell depends on the runner's env | drafter (READ) |
| g6 | the comment's "in env-key mode both read STORAGE_ENCRYPTION_KEY": with it set to a 64-hex throwaway, a blob made by one path decrypts through the other | **measure it** (C-122: a comment is source text, not behaviour) | drafter |
| g7 | G2's path at the rd-424 head (`2ce26eb`, NOT a member): the cell file on M0 + `2ce26eb` in a separate clone | **optional, only if cheap; say which** — the builder's own C-68 note; otherwise name it for the merge author | builder (C-68 note) |

**W — RD-652's WARN (C). At `09e2e6a`, at M, and on the merged tree.**

| row | shape | expected at `09e2e6a` | at M | predicted-by |
|---|---|---|---|---|
| w1 | ruling (d): the server-source diff | ONE 10-line insertion after `require('dotenv').config();`; the default line byte-identical and still under "Set NODE_ENV to development if not set"; no other `NODE_ENV` line changed | — | drafter (MEASURED) |
| w2 | the 3 cells, clean | 3/3 | W1 red, controls green | builder |
| w3 | M1 (warn always) → both controls red; **M-W2: the default line moved ABOVE the WARN** (so NODE_ENV is never empty at the check) | M1: controls red; **M-W2: W1 red** — proves W1 guards the ORDER | builder + drafter |
| w4 | **NODE_ENV truly UNSET** (deleted from the child env, not empty) — boot once by hand | the WARN once; mode = development (the default) | drafter (the declared limit) |
| w5 | a `.env` in the extract's cwd setting `NODE_ENV=production`, the env unset (L-C1) | no WARN (dotenv loaded first) — **say which cwd dotenv reads** | drafter (optional) |
| w6 | the shipped paths: `Dockerfile` (`ENV NODE_ENV=production`, READ :122), `docker-compose.yml` (`NODE_ENV=production`, :37), the Marketplace template | no WARN in any (READ ONLY is enough; say so) | builder (READY :13) |

**R — RD-646/647's fail-closed store (D). At `608a1cd`, at M, and on the merged tree; the fake Redis behind the proxy, never a real one unless one exists (L-D6).**

| row | shape | expected at `608a1cd` | at M | predicted-by |
|---|---|---|---|---|
| r1 | the 11 cells, clean | 11/11 | B1, B2, CTRL-LIVE, M2, M3 red; M1, FAITHFUL, CTRL-MEM green (M4? CENSUS-B/M? — **measure; the READY does not say**) | builder |
| r2 | MA / MC / MD re-derived | B2+M3+M4 / M4 / B1 red | — | builder |
| r3 | **M-R3: the `!client.isReady` check removed** (the store built on a dead client — RD-646's crash shape) | B1 red (process dies or 500) — the cells can see the ORIGINAL bug come back | drafter |
| r4 | **M-R4: `decrement` made to THROW after the response** | an unhandled rejection? a crash? — measure whether any cell notices | drafter |
| r5 | **the census's 503-only assertion**: a mutant where the CSP limiter (or one other route) answers a 503 that is NOT the named one (e.g. a plain `res.status(503)`) | **census GREEN (predicted)** — the census cannot tell a named 503 from any 503; say which cell (if any) does; x2 is where this gate checks the name | drafter (READ `census()`) |
| r6 | **every census 503's BODY** in one CENSUS-B-state boot (your own driver, production mode) | each body the named message; **count and name any 503 that is not** | drafter |
| r7 | **the population's blind shapes** (5b C-F1): routes on the `afterAuthGate` router, the 12 `app.use('/api…')` mounts (the census adds 3), indented/double-quoted/split `app.<method>(` literals, `*` routes | drive the router and afterAuthGate GETs once anonymously with Redis down — all 503 predicted (`app.use('/api/', generalLimiter)` sits in front of every `/api` path, READ :1423 on the merged file); **a 200 that serves data is a Blocker** | drafter (5b C-F1) |
| r8 | SCIM routes with Redis down (L-D5, RD-650) | served (not refused) — the builder's stated exception; **measure that it is exactly SCIM and nothing else** | builder |
| r9 | the compose/Docker HEALTHCHECK consequence (READ ONLY): `docker-compose.yml` :91-92 and `Dockerfile` :152-153 curl `/api/health`; `restart: unless-stopped` (:90) | at M, Redis down at boot → process exits → restart loop; at `608a1cd` → stays up, `/api/health` 503 → container UNHEALTHY, not restarted by compose; the Marketplace template probes `/api/live` (:573) and sets no Redis. **A note for Tuesday's relay to Kam (C-179 "Tuesday tells Kam about the boot change"), not a defect** | drafter (READ) |
| r10 | recovery timing: Redis returns → first 200 | within the backoff ceiling (≤ 5 s + one request); measure the gap | builder ("about 2 s") |
| r11 | CTRL-MEM on the MERGED tree (no Redis configured) | 200 everywhere the limiter allows; the log says in-memory; **nothing** mentions Redis | builder (C-179's control) |
| r12 | a leak census after every D run: no fake Redis, proxy or server child left, no port held (the READY disclosed a leaked pid 89570 in an earlier run) | none left, by pid from your own ancestry | drafter (C-174 via 5b) |

**E — RD-686 round 2's words against the REAL gate (E). At `ab12726` (the words) and on the merged tree (the gate the words will sit beside); the plants
go into COPIES of `static/css/dark-mode.css` / a light sheet in YOUR extract, run through the real `brand-token-conformance` file (24 cells at batch 6).**

| row | shape | expected at `ab12726` (what the NEW words say) | predicted-by |
|---|---|---|---|
| e1 | **E1A**: an off-token SECOND `rgba()` in one declaration of `dark-mode.css` | the gate GREEN (24/24), **and the new words SAY so** ("does NOT read a second or later `rgb()`/`rgba()` in the same declaration … passes") → claim TRUE | batch 6 (E1A) + READY |
| e2 | **E1C**: a named colour (`fuchsia`) in `dark-mode.css` | gate GREEN; words say "does NOT read named colours (`fuchsia`, `white`) … passes" → TRUE | batch 6 (E1C) + READY |
| e3 | **E2A / E2B**: +1 `#00719f` / +1 `#0096d6` in a light sheet | E2A GREEN, E2B RED; words say "each MEASURED token value (the 20 values in … `LIGHT`) … `#00719f` has no pinned count, so one more use of it … passes" → TRUE | batch 6 (E2A/E2B) + READY |
| e4 | **an off-token `hsl()` in a declaration that ALSO holds an on-token integer `rgba()`** | **drafter READ: gate GREEN** (`:149` finds the rgba, `:153`'s `else if` never records the hsl) — while the new words still say "an `hsl()` is recorded UNCONVERTED and fails by name" → **if GREEN, a claim NOT true of the code (unsafe direction)** | drafter (READ :149-154) |
| e5 | **an off-token FIRST `rgb()` written with percentages, decimals or `var()`** (e.g. `rgb(10%, 20%, 30%)`, `rgba(12.5, 0, 0, .5)`), alone and before an on-token integer `rgba()` | **drafter READ: gate GREEN** (`RGB_TRIPLE` needs three integers) — the new words say "the FIRST `rgb()`/`rgba()` of each declaration … Each must resolve" → **if GREEN, NOT true as worded**; say whether `var(--…-rgb)` forms are covered by the `--*-rgb` clause instead (then SAFE) | drafter (READ :116) |
| e6 | the positive controls in the same run: an off-token FIRST integer `rgba()` → RED; an lone off-token `hsl()` → RED "UNCONVERTED"; an off-token `--x-rgb` triple → RED; an off-token hex → RED | all RED (the gate CAN fail on each shape the words say it reads) | batch 6 + drafter |
| e7 | every OTHER sentence round 2 changed (the diff's `+` lines) and every sentence it did not (§6, RD-199/RD-200 histories) | the changed ones each tested by e1-e6 or READ against the cited line; the unchanged ones byte-identical to `8962a14` (`git diff 8962a14 ab12726` shows one hunk region, §8 rule 3) | READY :20 |
| e8 | the 10 readers (C-68) at `ab12726` and on the merged tree | all green; per-file counts (batch 6: 113/113 at its step 1) | READY :28 + batch 6 U7 |
| e9 | the test TITLE :244 ("every rgba()/hsl() colour … resolves to a token") beside the now-narrower doc | report it (READY names it, RD-722); a severity against RD-686 only if the words-only ruling covers titles — say which reading you took | READY :23 |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.**

## 3. THE QUESTIONS ALL TARGETS ANSWER FIRST
0. **SESSION_SECRET UNSET, EVERY RUN** — §3a H-1's ONE permitted printer. Positive control once per target with a server: its own cell file with a
   throwaway random 64-hex secret exported (never printed, never written) — identical results, or say what differed.
1. **Re-pin everything yourself:** `git ls-remote` at start, mid and end (three timestamped readings, branch name beside each sha): main, the five member
   branches, and the 5a/5b/6 heads §1 names (they tell you what main is about to become). M0 and the "Main may move" rule re-proved; chains and exact
   parents (`git log --format='%H %P'`); deltas (`git diff --name-status`); counts at `1904765`, M0, `7e4cd2e`, `4334b96`, `a5799f3`, `09e2e6a`, `608a1cd`,
   `8962a14`, `ab12726`.
2. **POSITIVE CONTROL FIRST — re-derive every red and every mutant INDEPENDENTLY** — your own scripts, never the builders' `hold.sh` files or
   `mx618x646.sh` (read them for method). **Before each mutant arm, prove it still parses — `node --check` on every mutated JS file, exit 0, quoted — and
   that it LANDED (the exact mutated text present, the original absent once the new text is removed; `qa-mutate.py <arm> <mid> --verify` with its negative
   control). A red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.** Quote the failing assertion of every red.
3. **Name every behaviour guarded by no cell, and every one guarded only by source text.**
4. **Full verify of each head and of the merged tree**, `npm run verify -- --maxWorkers=2 --forceExit` (prove `--forceExit` reached jest — the verify
   script passes unknown args through, READ `scripts/verify-suite.sh` :117 — or say it did not and rely on the deadline), through the lock, on a
   git-indexed tree, SESSION_SECRET UNSET, a fresh SHORT TMPDIR each (5b B-F1: a long TMPDIR reddens rd696 cell 5 — if rd696 is in M0). **Predicted:
   `4334b96` 4142/248 · `a5799f3` 4136/248 · `09e2e6a` 4136/248 · `608a1cd` 4144/248 · `ab12726` 4133/247 · M0 = `40b7eae` 4191/252 · merged
   (M0 + A + B + C + D + E) counts(M0) + 26 / + 4 = 4217/256 at M0 = `40b7eae`** (predictions; the measurement decides). Every failure by NAME; **`rd638-export-always-ends E2` is
   C-185's known CI failure — if it fails LOCALLY, report it by name, it is not excused locally.** Re-run until green is not an acceptance gate.

## 3a. INSTRUMENT RULES — H-1..H-19 (carried from the batch 5b brief, which carried batches #1-#4, rd579-rd639 and pkg221) and H-20..H-21 (ruling f)
- **H-1 (rd579-rd639 S-1: a SET/UNSET idiom printed the secret's VALUE).** The ONLY permitted printer, verbatim:
  `if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi`.
  **FORBIDDEN anywhere in your scripts:** `${SESSION_SECRET-…}`, `${SESSION_SECRET:-…}`, `${SESSION_SECRET+$SESSION_SECRET}`, `echo
  $SESSION_SECRET`, `printenv`, `env | grep`, `set | grep`, and **echoing an env array that could hold it (`${envs[*]}`)**.
  **Self-test it BEFORE the first hold (a control that can fail):** run the printer once with a throwaway exported and once unset, capture both, assert
  the throwaway's value is ABSENT from both (compare in-process; never print it). **After every hold, scan that hold's logs for the throwaway value** and
  report the count (0); **the scan's own positive control plants a DIFFERENT random marker, never the throwaway.** Print any needle only as
  `<first4>…<last4>`, and **mask GUIDs with or without hyphens**. (5b §2: export the throwaway INSIDE the run's subshell, never in argv.)
- **H-2.** Never construct a product storage object on a DATA_DIR you are measuring AFTER its server booted. Seed BEFORE; read logs RAW.
- **H-3.** Every hook you rely on (a preload, a stubbed store, a planted route, a mutated rule) gets a **LANDING CONTROL** before the measured run: prove it
  fired once on a known input. An arm whose instrument failed is VOID, is re-run, and is reported as a self-correction.
- **H-4.** The heartbeat is a **separate child** process started by the hold wrapper (`while sleep 60; do echo "HB $(date -u +%FT%TZ) <step> <pid>
  <elapsed>"; done`), killed in the wrapper's `trap … EXIT`; **the wrapper ABORTS the hold if no HB line appears within 90 s of the grant**, and after
  every hold you compute and REPORT the **max gap** between HB lines (must be ≤ 120 s). Keep the HB child's output unfiltered (a `grep -v` BUFFERED it once).
- **H-5.** Restore your own perturbations (mutated files, planted routes, held ports, sockets, env files) before any hash, and hash the restore.
- **H-6.** Every extractor and census gets a POSITIVE CONTROL. **Every path is quoted** — `!CODING` and `Testing Agent MAIN` contain `!` and spaces.
  **Every server you boot runs under the network belt (`qa-netbelt.sb`) with its landing control (EPERM for TEST-NET-1, 200 for loopback).** D's fake Redis
  and proxy listen on loopback — prove the belt lets THEM through (a loopback connect succeeds) before trusting any "Redis down" state.
- **H-7.** Mutants are built and verified ONLY by a quoted tool with a negative control (an unmutated tree → VOID rc ≠ 0). A mutant check that prints an
  empty count is a VOID arm, never a pass.
- **H-8.** The landing rule is "the exact mutated text is present AND the original text is absent once the new text is removed" — never "the anchor is absent".
- **H-9.** Byte-level plants (a golden blob one hex off, a salt one byte off, a body at the 16 KB boundary) are written with `Buffer` and verified by
  `xxd -l 16` BEFORE use; never with `echo`, `printf`, a heredoc or `JSON.stringify` where the bytes matter.
- **H-10.** Prove every phenomenon reachable before measuring its absence: for "Redis down" prove the proxy REFUSES a connect; for "Redis up" prove a
  PING answers through it; for s3/s4 prove the forged URL reached the stripper (the log line exists) before reading what it kept.
- **H-11.** Every script runs under `/bin/bash` explicitly, and every `<sha>:<path>` is written `"${sha}:${path}"`. **Never `set -- $x` or `declare -A`
  in the default shell** (macOS bash 3.2 has no associative arrays — the drafter hit it today: a hex key like `2c221fa` is read as an arithmetic
  subscript and fails "value too great for base").
- **H-12.** Before the C-57 control, list every `__tests__` file any head MODIFIES or DELETES (`git diff --name-status <its base> <head> -- __tests__`).
  **Predicted this time: ONE, a helper** — A, B, C and D only ADD (`rd618-…`, `rd628-…`, `rd652-…`, `rd646-647-…`, `helpers/rd647-restartable-proxy.js`);
  E MODIFIES `__tests__/helpers/css-colors.js` (round 1, comment-only, `78bb004` → `bdb5ca3`; a helper holds no test ids). Nothing deleted.
- **H-13.** Every tree census is NUL-safe (`ls-tree -z`), with a positive control on a path containing a space.
- **H-14.** Every driver ends with an explicit END record; a run with no END record is VOID, whatever its exit code.
- **H-15.** Pass preloads as `-r "<path>"` in argv, never through `NODE_OPTIONS`.
- **H-16.** A plant is checked to be what the product will treat it as before it is used (the forged URL is in a field the stripper reads; the proxy port
  is the one the server's `REDIS_URL` names).
- **H-17.** Absolute tool paths only; every arm asserts the thing actually STARTED (the server's first log line, jest's first suite line) before its rc is read.
- **H-18.** zsh consumes `:s`/`:a` in `$var:path` as history modifiers; `/bin/bash`, braces, and **reject any sha256 equal to `e3b0c442…` as a VOID read**.
- **H-19.** gitleaks canaries (if you run gitleaks over the deltas) are planted as real keys, not JSON-escaped inside strings.
- **H-20 (ruling f — a hung jest held the NexusAI lock 4.5 h on 2026-09-28).** **EVERY jest invocation inside a hold carries `--forceExit` AND runs under
  a per-step hard DEADLINE** (`qa-to.sh <seconds> …`, rc 142 = fired): targeted cell runs 600 s, the C-68 union 2,400 s, a full verify 2,700 s (5b measured
  ~18 min each). A deadline that fires ABORTS that step (reported by name, never retried silently), the wrapper's EXIT trap runs, and the lock releases
  through the wrapper's own exit. **`--forceExit` hides open handles, so the leak census (r12, §11) runs after every jest regardless.**
- **H-21 (ruling f).** **Every file you mutate is restored in a `trap … EXIT` installed BEFORE the first mutation** (restore by `git show
  "${sha}:${path}" > file` or from a pre-mutation copy, then hash-compare to the pinned blob); the trap also covers INT and TERM; after every hold, assert
  every mutated path's hash equals its pinned blob and report it. **A mutant tree left mutated after a deadline is a self-correction to report, and that
  tree is quarantined, never reused.**

## 3b. THE NEGATIVE-ASSERTION SWEEP (C-102, carried from the 5b brief) — REQUIRED, scoped to what these members change
**A adds EARLY RETURNS to the intake** (`return res.status(204).end()` in the catch; `return res.status(400).end()` when no entries) **and a `return
next(err)` to the error handler; D adds throws BEFORE the limiter's count.** A negative-asserting cell that stays GREEN because it is now stopped EARLIER
is invisible to every verify.
1. **Enumerate the new early exits (READ, quote each):** `git diff 1904765 <head> -- <the server entry point> backend/services/cspReport.js` for A and D;
   every new `return`, `throw`, `next(err)` before the handler's last line.
2. **Enumerate the callers' cells** at the merged tree: every cell that POSTs to the CSP URI (positive control: `rd618-csp-intake-residue` must be found),
   and every cell that asserts a limiter status (429/503/200) (positive control: `rd607-redis-limiters-keep-their-own-counts`). Classify each NEGATIVE
   (asserts a refusal, an absence, a status code other than 2xx, "not logged") or POSITIVE.
3. **For each NEGATIVE cell: does it still reach the check it is NAMED for?** E.g. rd495's A5/A6 (the 413 cap, "referrer never stored") must still be
   answered by the parser/cap and the stripper, not by A's new 400 "no violation fields"; rd618's R2 (400 no fields) must be the empty-entry branch, not the
   parser; rd607's refusals must be the COUNT, not D's store error; CENSUS-B's 503s must be D's named error, not a crash page. **A negative cell whose red
   (or green) now comes from a different, earlier line is DISARMED** — name it with the line. Prove it with the log line each branch writes, or coverage
   (`--coverage --collectCoverageFrom=<the file>`).
4. **Self-test first or ABORT:** a positive control (a cell you know reaches its named check — e.g. R3's fixed log line is written by the entity branch), a
   negative control (a POSITIVE cell), and a non-empty population.
5. **Report per ticket:** population, negative cells, still reaching, disarmed. B and C: population = their own cells (CTRL, CTRL-DEV, CTRL-PROD are the
   negative cells — prove each is reached by the branch it names).

## 4. TARGET A — RD-618 (TIER 1). Answer each with a measurement.
1. **Scope:** `git diff --name-status 1904765 4334b96` = the four files; `7e4cd2e..4334b96` = the three; nothing in `static/`.
2. **POSITIVE CONTROL FIRST:** the cell file against `1904765`'s product (s1 — which cells are red, by name) and against `7e4cd2e`'s product (R5 red,
   the other 8 green — the builder's claim), then at `4334b96` 9/9.
3. **Every row s1-s9 of §2a** — s3, s4, s6 and s7 first (they are the drafter's reads of residual shapes the cells do not pin).
4. **The narrowing (Tuesday's ANSWER 2026-09-28T11:17:37Z, RELAYED in the r2 READY):** enumerate body-parser's error `type`s (READ its source in your
   `node_modules`, quote the list) and, for each, which branch answers it at `4334b96` and at `7e4cd2e`. Say whether any `entity.*` type is one the
   intake should NOT answer as 400/413, and whether any non-`entity.*` parser error now leaks attacker text through the global handler's log (s7).
5. **C-68 set for A** (MERGE ORDER step 3) on `4334b96` and the merged tree.
6. **PRIOR WORK:** gate 2's F-A2..F-A5 (PRIOR ROUND) — say which are CLOSED by measurement, which partly (s3/s4), which unchanged; F-A1 stays out (ruled).

## 5. TARGET B — RD-628 (TIER 2, through-code). Answer each with a measurement.
1. **The comments-only claim (ruling), g1:** two independent instruments, each with a control that fires. **If ANY executable line changed, it goes in
   your WRONG list (commission condition) and is a Major.**
2. **POSITIVE CONTROL FIRST:** 3/3 at `a5799f3` and against `1904765`'s product; then M1, M2 (g3) and g4.
3. **Every comment sentence the commit adds, checked against the code it describes** (READ + g6 for the env-key sentence). A false one is a Minor.
4. **g5, g7.** And whether anything in `a5799f3` bears on gate 5's F-B2 (PRIOR ROUND) — say, do not re-grade.
5. **C-68 set for B** (MERGE ORDER step 1). **Name for the merge author:** rd-424 (`2ce26eb`) changes `backend/jsonStorage.js`; when it merges, G2 re-runs
   by name on that tree (the builder's own note; C-68).

## 6. TARGET C — RD-652 (TIER 2). Answer each with a measurement.
1. **Ruling (d), w1:** the default kept, only a WARN added — quote the diff hunk and the default line at both shas.
2. **POSITIVE CONTROL FIRST:** W1 red / controls green against `1904765`'s product; 3/3 at `09e2e6a`; M1 and M-W2 (w3).
3. **w4 (truly unset), w5 if cheap, w6 (READ).**
4. **C-68 set for C** (MERGE ORDER step 2). **RD-705 is the lane-1 head whose hunk the READY says sits "directly above" the default line** — measure the
   merge-tree `09e2e6a` × `e164d1a` yourself (drafter: counts-only) and, if RD-705 is in M0, say where the WARN and the default sit on the merged tree.

## 7. TARGET D — RD-646 + RD-647 (TIER 1). Answer each with a measurement.
1. **Scope:** the four files; the server-source hunks are only the named error and `setupRateLimitStore` (READ: two hunks). Nothing in `static/`.
2. **POSITIVE CONTROL FIRST:** the cell file against `1904765`'s product (r1 — which cells red, by name; the boot EXITS), then 11/11 at `608a1cd`.
   **H-10 first: prove the proxy's down state refuses and its up state answers.**
3. **Every row r1-r12 of §2a** — r3, r5, r6 and r7 first.
4. **The census population:** reproduce it independently (158 predicted: 152 unique literals + 6) on `608a1cd`, on M0 and on the merged tree; name every
   route added or removed by M0's movement (if the 5a merges added routes, the census must drive them — C-68).
5. **The boot change (C-179, TIER 1):** at `1904765` with Redis configured and down, the boot EXITS (measure the exit code and the last log line); at
   `608a1cd` it stays up and `/api/live` answers 200 while every limited route answers the named 503; the startup log never says "falls back to in-memory".
6. **C-68 set for D** (MERGE ORDER step 4), on `608a1cd` and the merged tree. **Name for the merge author:** every later lane-1 merge that changes the
   server source changes the census population; CENSUS-B/M re-run by name at each (the same rule Tuesday ruled binding for RD-594's K2 in 5b).

## 7a. TARGET E — RD-686 ROUND 2 OF 2 (TIER 2, words). Answer each with a measurement. ROUND CAP: a NO GO goes to Kam.
1. **Scope:** `git diff --stat 8962a14 ab12726` = `docs/BRAND.md` only, +15/−7; over `1904765`, `css-colors.js` + `BRAND.md`; `css-colors.js` code
   unchanged (your own comment-strip with a control, plus `node --check`); the three gate files the words describe are the SAME blobs at `1904765`,
   M0 and `ab12726` (if M0 changed any of them, the words describe a different gate — say so and re-read at M0).
2. **Re-read every cited line AT THE HEAD** (css-colors.js :202-204, :53; brand-token-conformance :116, :140, :149, :153-154, :265, :70-79; `LIGHT`)
   and quote it. **Never from the READY.**
3. **POSITIVE CONTROL FIRST (e6), then e1-e5** through the REAL gate file in your extract, one plant per copy (H-9 for byte plants; H-3 landing: the plant
   is in the sheet the gate reads). **For each rewritten claim, one line: the words, the gate's measured behaviour, TRUE / NOT TRUE, which direction.**
4. **e7, e8, e9.** The 10 readers at the head and on the merged tree, per-file counts.
5. **Verify at `ab12726`** (4133/247 predicted; the READY's own verify changed only `_updated`) — or, if the queue is long, say why the 10 readers plus
   the merged-tree verify stand in for it (E changes no executable line), and label it.
6. **PRIOR WORK:** batch 6 §7's E1-E8/e9 table — say which rows round 2 moved (E1, E2, E8) and that the rest are byte-unchanged.
7. **The verdict line carries the round cap:** *"RD-686 round 2 of 2: <GO|GO WITH FINDINGS|NO GO> @ ab12726"* — and a NO GO names, for Kam, each
   claim still untrue with its plant.

## 8. THE CROSS-CHANGE CELL (ruling a) — rows x1-x7. The reason for this gate.
1. **Why here, and why not the builder's script as-is:** `session-tools/s86m/mx618x646.sh` (READ, 18 lines) builds the merge IN A NEXUSAI WORKTREE
   (`git merge --no-ff --no-commit origin/rd-646-…`), runs `npx jest` on four files **with no `--forceExit` and no deadline**, and aborts the merge only on
   its LAST line with no trap — **so a hung jest leaves a NexusAI worktree mid-merge (H-20/H-21).** Its log `session-tools/s86m/mx618x646.log` (mtime
   2026-09-29 00:15:47 AEST) holds only `[nexusai-lock] waiting …` lines — **0 result lines (drafter `grep -c 'csp-report ->'` = 0): it NEVER RAN**, which
   matches the r2 READY :19-21 ("UNMEASURED BY ME … yielded … not re-queued"). **Use its FILE LIST (rd646, rd618, rd495, rd607) and its two anchors
   (`startsWith('entity.')`, `RATE_LIMIT_STORE_UNAVAILABLE`); build the merges in YOUR clones.**
2. **x3 FIRST (the positive control):** `clone-x7e4` = M0 + `7e4cd2e` + `608a1cd` (counts placeholder, C-104: resolved and staged before any run).
   Predicted: `rd646-647-…` CENSUS-B and CENSUS-M RED, each with exactly ONE offender, `POST /api/csp-report -> 400`; every other rd646 cell green;
   `rd618-…` (the `7e4cd2e` file, 8 cells, no R5) 8/8. **If x3 is NOT red, the interaction is not what everyone read — STOP and report it; x1's green then
   proves nothing.**
3. **x1 then x2** on `clone-1` after step 4 (and on a two-member clone M0 + `4334b96` + `608a1cd` if the full merge is not yet built): green, and the
   `POST /api/csp-report` 503's body is the named one (x2).
4. **x4 and x5** (mutants on the x1 tree): the census re-reddens on exactly that route. **x6 and x7:** A's intake unchanged by D when Redis answers and
   when it is not configured.
5. **Report it as a COMPOSITION finding if anything but the prediction happens, graded on the merged tree and named against both RD-618's and
   RD-646+647's merged-tree lines.** State for the merge author: whichever of A and D merges second re-runs rd646 and rd618 by name (D's READY :46), and
   `7e4cd2e` must never reach main.

## 9. THE MERGED TREE (C-68, C-57, C-89, C-104, C-133). No verdict is complete without it.
1. **Build it in YOUR OWN scratch clone** under `projects/nexusai/qa-trees/batch7.*/clone-1`: `git clone --shared --no-checkout <repo> <dir>`; in the clone
   only: remove `origin`, set a local `user.name`/`user.email`, `gc.auto 0`, `core.fsmonitor false`; `git checkout -b gate <M0>`; then `git merge --no-ff`
   in the PROPOSED ORDER: **`a5799f3`**, **`09e2e6a`**, **`4334b96`**, **`608a1cd`**, **`ab12726`**. **Write your prediction for each merge BEFORE it**
   (the MERGE ORDER table); **anything other than the counts file conflicting STOPS (C-57).** Re-measure all ten member pairs by `merge-tree` in a
   scratch object dir first (E pairs predicted conflict-free).
   **C-104: resolve and stage before any census or run.**
2. **Resolve the counts file by REGENERATION, never by hand:** take a side (a placeholder) to complete each merge commit, then `npm run verify --
   --maxWorkers=2 --forceExit --update-counts` ONCE on the tree after ALL merges, through the lock, SESSION_SECRET UNSET, under its deadline; commit the
   regenerated file in the clone. **Predicted 4217/256 at M0 = `40b7eae`.** Then a plain verify of the committed head.
3. **The server source on the merged tree:** `node --check` rc 0; A's `startsWith('entity.')` present once; D's `RATE_LIMIT_STORE_UNAVAILABLE` present
   (4 occurrences at the drafter's A×D merge-tree); C's WARN block present once and ABOVE the default line; the old `=== 413` catch-all absent.
4. **Order independence (a control that can fail):** clone-2 in REVERSE (`ab12726`, `608a1cd`, `4334b96`, `09e2e6a`, `a5799f3`). **The two `HEAD^{tree}` must be
   identical apart from the counts file** — quote both tree ids and the `git diff --name-only`. **The server source auto-merges in three places — say
   whether both orders give the same BLOB for it** (they must).
5. **Blob identities and C-112's condition (carried from 5b), stated beside the conclusion:** every member path at the merged tree == its head's blob
   (`cspReport.js` `fa868ea`, `encryptionService.js` `e449589`, the four new cell files and the helper; E's `css-colors.js` `bdb5ca3` and `docs/BRAND.md`
   `f614781`), the server source == neither parent (a 3-way auto-merge — say so, and show every hunk of each member is present); `package-lock.json`
   `9064763`. **`__tests__`: 300 files predicted at M0 = `40b7eae` (295 + 4 cell files + 1 helper; E modifies one helper and adds none), every one
   byte-identical to at least one parent, 0 identical to none, 0 absent (NUL-safe, H-13).**
6. **id-superset control (C-57) — ruling (c): PREDICT, then measure.** merged test ids ⊇ ids(M0) ∪ ids(`4334b96`) ∪ ids(`a5799f3`) ∪ ids(`09e2e6a`) ∪
   ids(`608a1cd`) ∪ ids(`ab12726`)? **Predicted: YES, missing 0** — no member modifies or deletes an existing `__tests__` CELL file (H-12: E's one
   modified file is a helper, comment-only), and each of A-D's ids are only its own new file's; **E joins this step only as "docs, no test ids"**
   (ids(`ab12726`) = ids(`1904765`), predicted; measure it, or say you used `1904765`'s set as its stand-in and why). **Predicted new ids: 9 (rd618) + 3 (rd628) + 3 (rd652) + 11 (rd646-647) = 26, = the counts delta.** Use a COPY of the 5b gate's
   `qa-c57-id-superset.sh` (reads the jest JSON of YOUR OWN verifies; keeps the lock-holder refusal; proven first to STOP on a planted missing id), five
   parents. **Any missing id: name it, its file, the file's blob at M0, at each head and on the merged tree, and its `git log --format='%h %s'
   1904765..<each parent> -- <file>` history, and say whether C-133's mechanical test holds on blobs** — and it is still a STOP (these are short-lived
   branches: C-133 "Not covered … short-lived branches (plain C-57 applies unchanged)"). **Never assume an id's absence is benign.**
7. **The semantic overlaps git cannot see (C-68), on the merged tree, one hold:** every C-68 set of the MERGE ORDER table BY NAME (per-file counts); rows
   x1-x7 (§8), s1, s6, s9, g2, w2, w4, r1, r5-r7, r11; then the full verify. Then ONE mutant per ticket on the merged tree: **M-A5** (rd618 R3 red), **M1-B**
   (rd628 G1 + CTRL red), **M1-C** (rd652 controls red), **MA** (rd646 B2, M3, M4 red) — each must still hold through the other changes; and for E the
   plants e1 and e6 through the merged tree's gate (still GREEN / still RED, i.e. the words still describe the gate main will carry). Rows e8 (the 10
   readers) join the C-68 union.
8. **C-89 on your clone:** `git diff --quiet HEAD` holds; `git show HEAD:scripts/verify-expected-counts.json` equals the regenerated counts.
9. **Nothing leaves your clone.** No push, no remote, no ref written in NexusAI. **Count `<repo>/.git/objects` files before and after your whole session
   and account for any delta by mtime** (live seats commit there; 5b S-9: `--shared` clones and merge-tree freshen mtimes of existing objects — say so).

## 10. CI (C-142 as amended by C-185) — NOT RUN AT ANY BRANCH HEAD unless a PR exists
- **Unverified by the drafter** (no `gh` run). Check with `gh pr list --head <branch> --state all` (READ ONLY, NexusAI's own `GH_CONFIG_DIR`) for all
  five branches; M0's CI Build with `gh run list --commit <M0>` READ ONLY, labelled, and its failing set against C-185's known set `{rd638 E2}`.
  **`gh` never merges, approves, comments, reviews, labels, re-runs, dispatches, sets a variable or opens a PR.**
- **What the merge push would start** (READ the workflow `on:` filters at the merged tree, as 5b §7 did): 5b measured that a push to main starts
  `deploy-demo.yml` with its `build`/`deploy` jobs SKIPPED because `CI_DEPLOY_ENABLED` is unset (and no `demo` environment exists, 5b D-O1). **Re-read the
  variable READ ONLY (`gh variable list`) or say UNMEASURED** — the members change no workflow, so this is context for the merge author, not a member finding.

## 11. Floor discipline — THE FOUR CLAUSES, plus THE DEADLINE RULE (carried from the 5b brief)
1. **Every jest run, every server you boot goes through `session-tools/nexusai-lock.sh`, tagged `qa-b7-…`** (e.g. `qa-b7-H1-cells`, `qa-b7-H2-cross`,
   `qa-b7-H3-heads-verify`, `qa-b7-H4-merged`) — C-141: gate-class; under ADDENDUM 2/3 every NEW `qa-*` ticket earns a fresh, self-applied yield from the
   builders. **When a MERGE ticket (gate-class, C-141 ADDENDUM) is already queued when you file, file yours with `--after <that merge ticket's tag>`
   (ADDENDUM 4's tool) so you sit directly behind it; never ahead of it.** **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit another seat's
   process, lock directory, owner file or ticket, even if it looks stuck; if a holder looks stuck, mail a QUESTION (§13) and keep waiting. **Expect a
   busy queue: at 00:20 AEST the queue held `s86p-rd686-verify`, `s86p-merge-1-rd286`, `s86o-rd466-proof` and `s86n-ready3-verify`.** Pure reads, the
   comment-strip comparison and merge-trees may run outside the lock — say which did.
2. **Hold the lock ONCE per multi-run measurement.** Every hold is a TRACKED CHILD of your seat, never detached (`nohup … &`).
3. **Count foreign servers the C-125 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND the server entry point anywhere in the
   remaining argv; "ours" = the ancestor chain CONTAINS your own claude pid. **Record the foreign count BESIDE EVERY RESULT.**
   **NEGATIVE controls, all in the same run, all must classify FOREIGN:** NexusAI-M `62649` (%19), NexusAI-N `9959` (%21), NexusAI-P `20317` (%22), NexusAI-O `38362` (%29), Tuesday `24942` (%0; the parent of Tuesday's own shell) — re-read by Tuesday at stamp 2026-09-29 00:46 (Tuesday re-reads the seats at stamp from `tmux list-panes -a -F
   '#{pane_id} #{@cockpit_name} #{pane_pid}'` + `pgrep -P` + `ps`; the drafter's reading at 00:24 AEST, for reference only: NexusAI-M claude `62649`
   (`%19`), NexusAI-N `9959` (`%21`), NexusAI-P `20317` (`%22`), NexusAI-O `38362` (`%29`); Tuesday's pane `%0` pid `23911` had NO child process, and
   two other live `claude` processes (`24942`, `84139`) could not be tied to a pane by the drafter — **Tuesday names her own pid at stamp**). Re-read them
   at start; if one has exited, say so and use the others; **a hold with NO live negative control aborts.** Reuse the 5b gate's instrument BY COPY with
   YOUR pid as `ROOT` and these as `NEG`:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch5b/evidence/qa-floorlib.sh`
   (**its defaults are STALE — correct `ROOT` and `NEG` before any hold**) and `…/qa-floorcount.py`; the original counter is gate 7's
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`.
   **D's cells spawn servers with `spawn(process.execPath, [<the server entry point>])` — your counter must see them (a control server spawned that way
   reads 1, then 0 after reap).**
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, "0 offenders" (x3 is its control), "0 executable
   changes" (g1's control), "no leak" (r12), "missing 0" (the planted-missing-id control), "0 raw-body marker" (s9's different-marker control).

**5. THE DEADLINE RULE — every real-server probe and every network request has a per-step DEADLINE, a HEARTBEAT, and kills its server in a `finally`.**
Every HTTP request carries a client timeout; each step (boot 120 s, request 30 s, a census 400 s, targeted jest 600 s, C-68 union 2,400 s, full verify
2,700 s, exit 20 s) has a written DEADLINE (`qa-to.sh`); a step past it is ABORTED and reported, never waited on. **Log a HEARTBEAT line at least every
2 minutes during any hold (H-4: a separate child, ≤ 120 s max gap, aborted if absent at 90 s); a step with no heartbeat for 5 minutes is aborted and
reported,** and a hold that is not progressing releases the lock. Every server, fake Redis and proxy you start is killed in a `finally` (SIGTERM, then
SIGKILL after a grace) **by pid from your own ancestry, never by pattern (C-174)**, and the reap is confirmed by your floor counter. **H-20 and H-21 apply
to every jest.**

## 12. HELD
- **LOCAL RUN, NOT THE DEMO:** every server request goes to a server YOU booted on 127.0.0.1 from YOUR tree, under the network belt (H-6).
- **External hosts you MAY contact, and nothing else:** `git ls-remote origin` (pins); `api.github.com` via `gh` READ ONLY (§10); `api.agentmail.to` (your
  verdict mail and any QUESTION). **No Azure, no registry, no demo, no customer-test tenant, no Partner Center, no docker** (L-D6).
- **TIER 1 AT FULL WEIGHT — FINDINGS-ONLY (ruling e):** no fix, **no merge outside your own clones, no push, never push — not to main, not to ANY author's
  branch**, no deploy, **nothing to Partner Center, the demo or production**, no money, no external comms, no mail to any human. **No `az` at all.**
- **Never write into** the builders' `session-tools/` (copy, then hash at start and end) or any `worktrees/` directory; **never run
  `session-tools/s86m/mx618x646.sh` (§8.1).**
- **Symlinks, chmod, sockets, held ports, env files and scratch git repos live ONLY under your own mktemp dirs.**
- **Findings-only:** do not commit (outside your clones), move any branch, file a ticket, or write anything inside the NexusAI project (`2_Project_Files`,
  `session-tools/`, `worktrees/`, `1_Project_Definition/`, `qa-reports/`). **NEVER `rm`** — quarantine, per the template §5.

## 13. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch7/report.md` — ONE report covering every
member; evidence in `./evidence/` beside it.

**Questions:** your routing name is **`QA/NexusAI-batch7`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by) and **PROCEED ON THE SAFEST READING without waiting**;
Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning `[Tuesday -> QA/NexusAI-batch7] ANSWER`. Approval-class items (anything
touching the demo, Azure, Partner Center, money, or a human) are NOT RUN and named. Record every question, reading and answer.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 7: RD-618 · RD-628 · RD-652 · RD-646+RD-647 · RD-686 r2`
Lead the body with ONE line per ticket in this form — `RD-618: <GO|GO WITH FINDINGS|NO GO> @ 4334b96` · `RD-628: … @ a5799f3` · `RD-652: … @ 09e2e6a` ·
`RD-646+RD-647: … @ 608a1cd` · `RD-686 round 2 of 2: … @ ab12726` (a NO GO there says "→ Kam (round cap)") — then one line naming M0, the merge order you recommend, the merged counts you measured, **the cross-change cell's result
(x1 green? x3 red with exactly `POST /api/csp-report -> 400`?)**, and the census population on the merged tree. Never `wednesday-agent@`. AgentMail key:
`AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute: the QA project has none). Never put the key, a token or any
secret in a mail or the report.

Verdict format:
- **RD-618** naming `4334b96d91132d933bc30b6b8dbd63e2031552cc`: the positive control at base and at `7e4cd2e`; the four relayed mutants re-derived; rows
  s1-s9 (s3/s4/s6/s7 answered); the parser-error table (§4.4); F-A2..F-A5 disposition.
- **RD-628** naming `a5799f3ba444fba82b8f8f34529b5493751a9b48`: the comments-only verdict with both instruments and their controls; g2-g7; every added
  comment sentence checked.
- **RD-652** naming `09e2e6accf172f574dec22bdaedc47e104076edd`: ruling (d) verified; w2-w6; the truly-unset boot.
- **RD-646+RD-647** naming `608a1cd99adcc69f6d2cdc552f170e89710adb02`: the boot exit at base and stay-up at head; r1-r12; the census population (158
  predicted) at head, M0 and merged; every 503 body named or not.
- **RD-686 round 2 of 2** naming `ab1272678fe40e23cff86ff749601572dc8cb64b`: every cited line quoted at the head; e1-e9 with the TRUE / NOT TRUE line per
  rewritten claim; the 10 readers; **the round cap stated in the verdict line.**
- **The cross-change cell (§8):** x1-x7, x3 FIRST.
- **The merged tree (§9):** M0; both orders; counts regenerated once (measured vs 4217/256 re-based on M0); the id-superset result with every missing id
  (predicted none) and its blob history; C-112's condition; the C-68 sets by name; one mutant per ticket; C-89; the object-count accounting; **your
  recommended merge order.**
- **The §3b sweep:** per ticket, population / negative cells / still reaching / disarmed.
- Each of **L-A1..L-A3, L-B1..L-B2, L-C1..L-C2, L-D1..L-D6 and L-E1..L-E3** answered: discharged with a measurement, or left standing and named.
- All refs as **three timestamped readings (start / mid / end)**, each with its branch name.
- **§3a H-1..H-21:** for each, that it was followed, with the self-test outputs (H-1), landing controls (H-3, H-10), max HB gap per hold (H-4), byte checks
  (H-9), every deadline that fired (H-20) and every restore hash (H-21).
- Every action recommendation carries its evidence class: **MEASURED AT RUNTIME / PROBED / READ ONLY**. Severity is yours; priority is Tuesday's.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, a real Redis server (no docker), Redis with TLS or AUTH, multi-replica, a real container runtime's restart or healthcheck, a real browser's Reporting-API report, Key Vault mode and a real Key Vault success path, any deploy, real Azure, Partner Center, the demo, and Windows.

## WRONG OR UNVERIFIED IN THE COMMISSION AND THE READYS — carried so the gate inherits the corrections
1. **Ruling (a)'s "the census must see the NAMED 503 on POST /api/csp-report" — the census cannot see a name.** RD-646's `census()` (READ at `608a1cd`)
   records an offender when `status !== 503` and checks nothing else; only `/api/health` is checked for the named message (B1, M2). **A green CENSUS-B/M
   proves "a 503", not "the named 503"** — this brief adds x2 and r5/r6 to measure the name. The r2 READY :23 says only "the census should see 503"
   (accurate).
2. **RD-628 "comments only in backend/encryptionService.js" — VERIFIED at source (not wrong):** 0 non-comment changed lines by `git diff -U0`; code-equal
   after comment strip = true, with a control that reads false on a one-identifier edit. The gate re-proves it (g1).
3. **RD-652 "9 lines right after require('dotenv').config()" — the insertion is 10 lines** (`git diff --stat`: server.js `10 +++++`: 6 comment lines, a 3-line
   `if`, one blank). **Its quoted WARN text omits the `⚠️  ` prefix** the code carries. Cosmetic; the cell's regex matches either. **Ruling (d) VERIFIED:**
   the default line is byte-identical at `1904765` :973 and `09e2e6a` :983; nothing else in the file changed.
4. **RD-618 r2 READY :19-21 "C-68 WITH RD-646/647: UNMEASURED BY ME … yielded … not re-queued" — VERIFIED:** `mx618x646.log` holds lock-wait lines only
   (last write 00:15:47 AEST, 2026-09-29; 0 `csp-report ->` lines); no `mx618x646` process at 00:20. **Its "Read at source … the global handler, which
   answers its statusCode, 503" — VERIFIED READ ONLY** (merged file :22513 `error.statusCode || error.status || 500`; D's error has no `.type`, so the
   narrowed handler's `return next(err)` passes it on; only two error middlewares exist in the merged server source, :902 and :22513).
5. **The builder's script is not gate-safe** (§8.1): a NexusAI worktree merge, no `--forceExit`, no deadline, no trap — exactly ruling (f)'s failure shape.
6. **"Main is now 40b7eae" (ruling b) — VERIFIED** at 00:18:41 AEST; it is a DESCENDANT of the heads' base `1904765`; its 14-path movement touches no
   member file but the counts file; the server source is unchanged by it (`bc099b2` at both). **"M is merging batch 5a/5b … P is merging batch 6" — at
   00:18 none of the 5a/5b heads was yet an ancestor of main**, and `s86p-merge-1-rd286` (base `40b7eae`) was queued. Every 5a head changes the server
   source; merge-tree of each member vs each 5a/5b head = counts-only (MEASURED).
7. **RD-646 READY "census 158 routes" — VERIFIED arithmetic** (153 literals, 152 unique + 6). **But "every /api route" is the census's OWN population:**
   the 5b gate measured 12 `app.use('/api…')` mounts and 8 parameter-free GETs on the `afterAuthGate` router in the same server source; the census adds 3
   mounts (row r7). Not a false statement — the READY names its population — a limit the gate measures.
8. **RD-646 READY "Real Redis (docker redis:7.4-alpine …)"** — C-179's red proof; **this gate runs no docker and the drafter found no local `redis-server`
   (`command -v` → none)** — RELAYED (L-D6).
9. **RD-646 READY "/api/health answers 503 while Redis is down" + compose healthcheck — a CONSEQUENCE the READY does not state (READ ONLY):**
   `docker-compose.yml` :91-92 and `Dockerfile` :152-153 probe `/api/health`; `restart: unless-stopped` :90. At main a Redis-down boot exits (restart loop);
   at `608a1cd` the container stays up and reports UNHEALTHY. The READY says "Tuesday tells Kam about the boot change (C-179)" — **this is part of what she
   tells him** (row r9).
10. **RD-628's cell scrubs four env vars but not `LEGACY_MACHINE_IDS`** (READ; `jsonStorage.getEncryptionKeyCandidates` reads it). Possibly harmless (a
    same-id legacy candidate dedupes) — row g5 measures.
11. **RD-628 READY's C-68 note — VERIFIED that rd-424 (`2ce26eb`) changes `backend/jsonStorage.js`**; RD-413 (`f70594a`, "the mail path") changes none of
    `jsonStorage.js`, `encryptionService.js`, `backend/emailService.js` over its merge-base (MEASURED, named-file diff) — so the READY's "rd-413 (the mail
    path)" merge-tree is counts-only and carries no G-cell re-run of its own.
12. **The 4.5 h hung-jest incident (ruling f) — RELAYED:** the drafter did not find it in the batch 5a or batch 6 reports (`grep -i 'hung|4.5 h|forceExit'`
    → no match on it); it is Tuesday's account and is applied as a standing rule regardless (H-20/H-21).
13. **RD-618 first READY "F-A1 is left out by your ruling (C-178 addendum)" — NOT verified:** the drafter did not open C-178 for this brief (commission
    list). RELAYED.
14. **RD-618 READY :22 "RED on the base files … 6/8 red" predates R5** — at `1904765` the R5 cell's expectation (415 kept) is untested by the builder;
    s1 measures all nine against the base product.
15. **Drafter's own slips, disclosed:** (H-11) a first multi-head merge-tree loop used `declare -A` under `/bin/bash` 3.2 and mislabelled rows ("value too
    great for base" on `2c221fa`); re-run with plain pairs — §1's results are from the re-run. (H-18) one zsh read of `$H:scripts/…` failed "bad
    substitution"; re-run under `/bin/bash` with braces. (Provenance) the first draft of this brief carried minute stamps in PROVENANCE that were
    estimates, some later than the clock; replaced below — only the `date`-stamped readings are exact.
16. **Tuesday's mid-draft message "one file, docs/BRAND.md (+15/-7 over the gated 8962a14)" — TRUE for round 2, but what MERGES is both commits:** over
    the base `1904765` the branch changes **2 files, +62/−25**, including **`__tests__/helpers/css-colors.js`** (round 1's header, COMMENT-ONLY — re-proved:
    code-equal true, control false; blob `78bb004` → `bdb5ca3`). So "disjoint from the lane-1 four" holds (no shared path) and "no test ids" holds (a
    helper), but "docs only" is not literally the merged delta — H-12 and §9.5 carry the helper.
17. **Tuesday's "the C-68 set is the 10 BRAND.md/css-colors readers the READY names" — the READY :28 does not NAME them;** it says "the gate's step-1 set
    (the 10 BRAND.md/css-colors readers)". The names come from the batch-6 brief U7 (:383-386: nine `BRAND.md` readers + four `css-colors.js` readers,
    three in both = 10), listed in TARGET E; the gate re-derives them.
18. **RD-686 READY :14 ":204 collects named colours separately" — :203 tests `NAMED`, :204 pushes.** Cosmetic. **:116 no `g` flag, :140, :149, :265,
    `.named` read 0 times, `LIGHT` 20 values, `#00719f` absent, `#0096d6` count 54 — all VERIFIED at the head.**
19. **RD-686's new words — two places the drafter READS a residual overclaim (e4, e5; NOT run):** "an `hsl()` is recorded UNCONVERTED and fails by name"
    holds only for a declaration with no integer rgb triple (:149-154); "the FIRST `rgb()`/`rgba()` of each declaration" is the first INTEGER triple
    (:116). If the real gate passes those plants, the round-2 text is still not true of the code — at round 2 of 2, a Kam item.
20. **"The batch-6 gate report … the 2026-09-27 or 2026-09-28 batch-6 directory"** — it is `reports/2026-09-27-gate-batch6/report.md` (the gate ran
    2026-09-27/28; RD-686 section §7 :150).

## PROVENANCE (drafter, 2026-09-29 ~00:05–~00:50 AEST, read-only; EXACT times only where a `date` call stamped them, the rest "~")
- origin heads (main, A-D, the 5a/5b heads, rd-424, rd-627a) | `git ls-remote origin` (one call) | **00:18:41–00:18:44** (date-stamped)
- origin `rd-686-694-brand-wording-s85p` and main | `git ls-remote origin` | **00:31:38–00:31:41** (date-stamped)
- every pinned sha a commit; chains, parents, dates, messages; merge-bases; name-status; shortstats; counts at `1904765`, `40b7eae`, `7e4cd2e`, A-D,
  `8962a14`, `ab12726`; main's `1904765..40b7eae` path list | `git cat-file -t`, `git log --format='%H %P %ci %an | %s'`, `git merge-base
  [--is-ancestor]`, `git diff --name-status|--shortstat|--stat`, `git show "${s}:scripts/verify-expected-counts.json"` | ~00:19 and ~00:32
- blobs: server source, `cspReport.js`, `encryptionService.js`, `package-lock.json`, `css-colors.js`, `brand-token-conformance.test.js`,
  `derive-brand-tokens.js` | `git rev-parse` | ~00:19, ~00:33
- merge-trees: A-D pairs, `7e4cd2e`×D, `40b7eae`×each member, each of A-D × 11 lane heads, E × main / A-D / five batch-6 heads | `merge-tree --write-tree
  --name-only` with `GIT_OBJECT_DIRECTORY` = the drafter's own `mktemp -d` under its scratchpad, NexusAI's objects as alternate | ~00:19–~00:33
- RD-628: the diff; non-comment changed lines (0); comment-strip code-equality with control (node over `git show` of both blobs); `SALT` lines;
  `jsonStorage.js` :60-62, :85-97, :150-158; the cell file whole | `git diff -U0`, `node -e`, `git show` | ~00:20
- RD-652: the diff; every `NODE_ENV` line at the head; `logger` at :41; the default line at both shas; `.env` not tracked | `git diff`, `git show | grep -n` | ~00:21
- RD-618: both server-source diffs, the `cspReport.js` diff, the cell names | `git diff`, `git show | grep -n` | ~00:21–~00:27
- RD-646: the server-source diff; the global handler and `sanitizeErrorForClient`; the cell file :56-160 (boot, ALLOW, census); `package.json`
  versions; compose/Docker healthchecks; the template's `/api/live` probe | `git diff`, `git show | sed -n`, `grep -n` | ~00:22–~00:28
- census and K2 populations at 13 shas and the A×D merged tree; the merged files' anchors and error middlewares | python over `git show`,
  `node --check`, `grep -c` | ~00:23–~00:28
- `session-tools/s86m/` listing; `mx618x646.sh` whole; `mx618x646.log` head/tail and `grep -c` | `ls -la`, `cat -n`, `head`, `tail`, `grep -c` | ~00:20
- live processes: the jest queue and no `mx618x646` process | `ps -axo` | **00:20:30** (date-stamped); seats | `tmux list-panes`, `pgrep -P`, `ps` | **00:24:20** (date-stamped)
- RD-686: the READY whole; chain; both diffs; cited lines at the head (css-colors.js :185-212, :51-53; brand-token-conformance :110-118, :138-160,
  :240-270, `.named`/`.functional` counts, :70-79 by grep); `LIGHT` evaluated from the object literal in node (nothing required); css-colors.js
  comment-strip with control; the batch-6 report :13, :18, :21, :150-163, :213 and refs table; the batch-6 brief U7 :383-386 | `cat -n`, `git
  show|diff`, `node`, `sed -n`, `grep -n` | ~00:31–~00:34
- CLARIFICATIONS: size/mtime/lines; C-57 :416, C-68 :663, C-89 :833, C-133 :1432 + ADDENDUM, C-141 :1486 + ADDENDA, C-173 :1775, C-179 :1854,
  C-184 :1895, C-185 :1904, C-186 :1911 (read); last entry C-186 | `grep -n -o`, `sed -n` on that one file | ~00:28–~00:30
- prior reports: gate 2 F-A lines; gate 7r2 RD-646/647/652 lines; gate 5 F-B2; the 5b report §0-§2 and §10-§18; 5b evidence listing; 5a/6 report grep |
  `grep -n`, `sed -n`, `ls` | ~00:12–~00:26
- the 5b brief and launcher (the pattern) whole; BRIEF_TEMPLATE whole; the charter's headings; the five lane-1 READYs whole | `Read`, `cat -n` | ~00:05–~00:15
- `command -v timeout gtimeout redis-server redis-cli docker` → only docker present | ~00:30
- routing: **no `QA/NexusAI-batch7` line in `fleet/inbox_routing.conf`** (batch5b :130 exists) — Tuesday adds it; the launcher's guard 40 refuses until
  then | `grep -n -i batch` | ~00:26
- report dir `2026-09-29-gate-batch7` absent | `ls -d` | ~00:29

## FILL AT STAMP — Tuesday, before launch (the launcher refuses until the starred items are done)
- ★ both STAMP placeholders at the top (the SELF-CHECK line and the Self-check note) — LAST, by hand, no placeholder token in the note.
- ★ the routing line `QA/NexusAI-batch7|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf` — added 2026-09-29 00:46 by Tuesday.
- ★ the negative-control seats in §11 (replace the stamp placeholder there with the pids, each in backticks) AND the launcher's `NEG_SEATS` — Tuesday's own pid included.
- If a member head MOVES before launch: the launcher's guard 18 refuses — re-pin that head in the launcher and every occurrence in this brief, re-read its
  READY, never `sed` a sha blindly.
