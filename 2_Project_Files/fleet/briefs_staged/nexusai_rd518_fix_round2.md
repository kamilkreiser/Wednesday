# STAGED — RD-518 FIX ROUND (round 2 of 2). NOT YET SENT.

**Do not launch this while a seat is live in `backend/server.js`.** RD-516's seat (S73) is in that
file; one seat per file. This goes to S73 when RD-516 reaches READY, or to its successor.

# BLUF

**RD-518 @ `6ea15a0` was gated NO GO with a BLOCKER. Three things must be fixed in ONE change, and
the third is the reason the first two survived seven red-proved cells.**
Report (read it, do not re-derive it):
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-20-rd518-6ea15a0-tier1/report.md`

🔴 **This is ROUND 2 OF 2 on this class. A third round is KAM'S (C-62)** — if round 2 does not pass,
ship nothing, ticket the residue and card him.

# F-01 — THE BLOCKER. Verified independently by Tuesday at source, not relayed.

`backend/encryptionService.js`: `const { credential, how } = buildKeyVaultCredential();` is at
**`:316`, INSIDE the `try`**. It is read at **`:350` and `:351`, inside the `catch`** — a sibling
block. **`const` is block-scoped, so the catch throws `ReferenceError: how is not defined` on its
FIRST statement**, every time, on the exact path RD-518 exists for (Key Vault configured, key
unobtainable).

**Consequences, all measured by the gate:** `_kvFallbackReason` is never set · the loud
`logger.error` never runs · the real Azure error is destroyed · the surviving line is a warn whose
entire payload is `"how is not defined"` · **and base `34ad321` logged the true cause on this path,
so this is a REGRESSION BELOW BASE on the one thing the change is for.**

**The whole remedy of RD-518 is observability. On the path that matters it currently produces less
than doing nothing.**

# F-02 — MAJOR, AND IT MUST LAND IN THE SAME CHANGE

**Fixing F-01 ACTIVATES this.** With a one-line scope fix applied locally, an **anonymous** GET
`/api/admin/health` in the open first-run window returns `keyVaultEncryption.detail` carrying **the
identity clientId and the full vault hostname**. The field's own comment says *"Operator detail. NOT
public"* — **a claim the code does not enforce.**

**So the fix is not "restore `how` to scope". It is: restore the recorded reason AND make the public
surface stop carrying it.** Options are yours to design, with one constraint from Tuesday's own
requirement: **the public path names no vault and no URL.** The private path may keep the detail for
an operator; the anonymous one may not. A redaction at the boundary and a redaction at the source are
different designs with different blast radii — say which you chose and why.

**The gate's control is the shape to keep:** four outcomes from one request line on one binary —
200 open-window / 503 signInUnproven / 401 enforced / 403 non-admin. **Re-run it after the fix.**

# F-03 — MAJOR (test design). Fixing F-01/F-02 without this leaves the same hole.

**Under jest, `require('@azure/identity')` throws `Unexpected token 'export'`, so all four
`initializeKey()` calls exit at the MODULE-LOAD catch (`:306`) and never reach the KV-access catch
(`:346`).** R2 ("a fallback RECORDS why") is green because a **different** fallback recorded why —
it matches `/Key Vault|identity|image/i` on the word **"image"**, from *"not installed in this
image"*.

**Mutation M7, run by the gate with its FAIL criterion stated first and the marker asserted present:
corrupt the RD-518 catch — 7 passed, ZERO reddened.**

🔴 **So the cells must be made to REACH that branch** (mock the SDK at the boundary the suite can
load, or whatever design you justify), **and M7 must redden afterwards.** A cell set that cannot
reach the branch it is named for is a receipt for a claim nobody verified.
**Also unguarded:** `encryptionKeyMode` and `keyVaultStatus` occur exactly once each in the tree —
the producer. No consumer, no test. The new three-value `keyVaultStatus` has no cell at all.

# F-04 / F-05 — MINORS, and one of them is Tuesday's fault

- **F-04:** the MarketplaceAPI `KEY_VAULT_NAME` comment (`server.js:668-674`) is a verbatim copy that
  **misstates its own reason** — it cites AzureADManager building a vault URL, true at `:651`, false
  at `:665` (`marketplace-api.js` has 0 occurrences of `keyVaultName`). The commit message has the
  right reason; the code comment does not, **and only the code is read by whoever "fixes" it later.**
  Correct the comment.
- **F-05 is against TUESDAY'S BRIEF, not against you:** `docs/runbooks/local-run-for-qa.md` does not
  work as written and cost the gate ~a third of its session — `SESSION_SECRET=<any-local-value>` is
  refused (<32 chars) and the app serves MISCONFIGURED **from a listener that is not the app but
  still answers `/api/health` with plausible JSON**. **Fix the runbook in the same round** and say
  what you changed; the next gate reads it.

# WHAT IS NOT IN SCOPE

- **The DEGRADED health flip stays unshipped** — Kam ruled (a) on `nexusai-degraded-flip-and-live-deployments`
  at 21:14: *"Tell me the deployment count and I decide from there."* He has not had the count.
- **Hard stops unchanged:** nothing touches `wrappedDekPath`, the vault URL construction or the
  wrapping key name — the one-time re-encrypt sweep does not exist. PRIVACY.md and TERMS are never
  edited (C-65). No deploy, no merge to main, no real Azure.
- **Do not re-run section 6's measurements.** 3709/210, the 7/7 red-proofs and M5→R5 all reproduce
  and the gate said so explicitly. The finding is reach, not correctness.

PROVENANCE:
- the gate returned NO GO with F-01 Blocker, F-02/F-03 Major, F-04/F-05 Minor, and M-B refuted | its verdict mail 2026-09-20T11:47:00Z to tuesday-agent@, and the report path above | read 2026-09-20 21:4x by Tuesday
- `const { credential, how }` is at :316 inside the try; `how` is read at :350 and :351 inside the catch | git show 6ea15a0:backend/encryptionService.js, read by Tuesday in your own tree /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-09-20 21:4x by Tuesday
- Kam ruled the DEGRADED flip card (a) "Tell me the deployment count and I decide from there" | his panel message, Tuesday tab, 2026-09-20T21:14:57 AEST | read 2026-09-20 by Tuesday
- this is round 2 of 2 on this class and a third round is Kam's | C-62, the tiered-gate cap | read 2026-09-20 by Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-20 21:50
