# QA GATE — Secuura #889 ROUND 2 @ `48ad0354e`, TIER 1. **Round 1 was NO GO on F1. The builder agrees the error was its own.**

**Tier 1 because the subject is unchanged: a 403 added to a live registration path on Kam's own
ruling (`bind` — the issuer is bound to the actor; a mismatch is refused).** The tier is carried from
round 1, not re-decided here.

## 1. Target
- **Head `48ad0354e`** on the KS-597 / #889 branch. **Base is NOT `develop`'s head** — the PR's
  recorded base and the true merge base are different facts and round 1's brief got this wrong.
  **Resolve the merge base yourself** and take the change set from the **PR files API**, not from a
  two-dot diff.
- Round 1's verdict: **GO-with-findings, F1 MERGE-BLOCKING**. F1 and F2 are what this round closes.
- **`develop` has not moved**; **#893 → develop is HELD behind this PR.** Kam's ruling
  `hold-for-finding1` is what holds it, so this verdict is what releases the trunk.

## 2. 🔴 THE PRECEDENT'S ADDRESS — do not inherit round 1's wrong one
Wednesday cited **`documents.ts:559`** as the 403 precedent in a card Kam ruled on, in his ruling's
context and in a successor brief, **having never opened the file.** It is a field in a 200 body; the
nearest status there is a 409; **#889 does not touch that file at all.** The real precedent is
**`services/provenance.ts:131`**. Round 1's verdict may still carry the wrong address — **it is
wrong, and this brief is the correction.**

## 3. 🔴 F1 — AND THE PROOF IS THE TAMPER, NOT THE GREEN RUN
**The builder's own account, and Wednesday accepts it as the shape:** the bind moved the column's
source from `sIdentity.organizationUuid` to the route-bound `issuerOrganizationId`; the integration
file still passed only the raw claim, so **nothing reached the column at all** — which reddened the
positive control and made the three "folds to NULL" cells **vacuous**. The builder reported "8/8
green" from `npx jest`, which is the **unit** config; **the integration config is a separate
invocation and was never run.**

**THE INSTRUCTION THAT MATTERS, and it is the builder's own recommendation, adopted:**
**do not accept the green integration suite as the proof.** A green integration suite is exactly
what the BROKEN state also produced. **The discriminating evidence is the tamper:**

> with the `AND tenant_id = ...` predicate deleted from **both** organizations subqueries, the two
> cross-tenant cells go **RED (2 failed / 8 passed, 10 ran)**; under the same tamper before this
> change they stayed **green**. `documentRepo.ts` restored byte-identical.

**Re-run that tamper yourself.** Assert it lands (sha changed) before the run, restore byte-identical
after, and check **which** cells red — a tamper that reds more than the two cross-tenant cells has
measured something else. **And red-proof the positive control separately**: the file's own comment
says *"Without this, every cell above would pass on a build where `issuer_organization_id` is never
written at all"* — that is the cell that caught the defect, so prove it can still fail.

**A green baseline is required as well as a red-proof.** A red-proof shows the check CAN fail; only
a green baseline on an untampered tree shows it passes for the right reason.

## 4. F2 — two comment corrections, and one claim the builder MEASURED rather than corrected
1. The comment said an org-less caller escapes the 403 because *"it is not a different org
   (`provenance.ts:109` takes exactly this view)"*. **`:109` does not say that** — its reason is that
   such a caller *"has no Organisation to validate against"*. The "not in a *different* org"
   phrasing is **`:136`**, a different branch (the org-less SUBJECT). **A rationale borrowed across
   branches. Verify the corrected comment now matches the branch it cites.**
2. It said migration 018 drops NOT NULL *"for admin-issued keys"*. **A NOT NULL cannot be dropped
   selectively.** Verify the correction.
3. **CONFIRMED, not corrected:** on a database built from `docker/init` + `run-migrations.sh`,
   `documents.issuer_organization_id` carries **ZERO** foreign-key constraints, against a control
   showing `documents` does carry one elsewhere. **That is now a measurement, and it agrees with your
   own round-1 finding of zero constraints on that column.** Judge whether the no-backstop sentence
   is now correctly stated.

## 5. The environment the builder left standing FOR YOU
- **`ks597-qa-pg` on network `ks597-qa-net`, `127.0.0.1:6499`** — a disposable Postgres rebuilt from
  the repo's own provisioning path. **14 init scripts, `applied=48 failed=0`, and
  `Applying 017_organizations_tenant_id.sql` confirmed BY NAME** rather than from the runner's
  summary. Teardown is in `HANDOVER-s148.md`; **leave it up until your pass closes.**
- **Confirming the migration by name is not fussiness — it is a workaround for a real defect** the
  #892 gate established: `run-migrations.sh` reports `applied=N failed=0` **for migrations it
  SKIPPED**. If you build your own database, confirm 017 by name too.
- **The shared local dev stack is STALE BY DESIGN** (121 commits behind as of 17:19) and the seeded
  stack on **`:6882` has UNTRUSTED DATA** — a QA pass took unparameterised writes against it.
  **Build your own from the provisioning path, or state exactly what a stack of that age cannot
  prove.**

## 6. Bounds and report
Findings-only, **never fix**. **NO CI** (20/20 `startup_failure`) — you are the only independent
instrument, so `tsc`/type-checking of the changed files is yours or it is nobody's. **Say what each
cell MOCKS.** **Search the board before filing and say what you searched** — by SYMBOL, PATH or ERROR
STRING, never by your own phrasing of the problem; four sessions have described one failure four
different ways on this board today. **Never write into the builder's checkout** — work in your own
clone. **A GO is NOT a deploy GO.**

**GO / GO-with-findings / NO GO on the first line.** F1's tamper evidence gets its **own heading**.
**NOT-TESTED at equal prominence**, and **where there is analysis, record what was FOUND, what was
TESTED, and HOW — including the controls** (Kam, 2026-09-07 18:56). Mail
`wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] Secuura #889 bind round 2 (tier 1)`.

## 7. PROVENANCE
- Head `48ad0354e`, and the F1/F2 accounts | the Secuura seat's own mail, `wednesday-agent@agentmail.to` 2026-09-07T10:21:32Z, read whole in this action — **the builder's claims, not re-derived by Wednesday** | read 2026-09-07
- Round 1's verdict (GO-with-findings, F1 merge-blocking) | the QA mail 2026-09-07T10:06:03Z | read 2026-09-07
- The corrected precedent `services/provenance.ts:131` | the Secuura seat's correction of Wednesday's citation, 2026-09-07 evening; **Wednesday holds no Secuura identity and has NOT re-opened the file** | not read by Wednesday
- `develop` at `6c60cc09b`, #893 held behind #889 | the 20:12 seat's handover, itself built from agents' `ls-remote` | not re-derived here
- Kam's `hold-for-finding1` ruling | `decision_queue.sh show secuura-889-issuer-org-caller-asserted`, ruled 2026-09-07T18:56 | read 2026-09-07
