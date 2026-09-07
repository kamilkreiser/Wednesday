# QA GATE — Datasec/NexusAI RD-363 / SEC-07 (`rd-363-keyvault-purge-protection-s43` @ `b0dec96`). **TIER 1, round 1 of 2.**

**Charter first, in full:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/CLAUDE.md`
(T9 seat — DevMASTER is not mounted. Every path here is a T9 path.)

## 🔴 TIER: UPGRADED FROM 2 TO 1 BY WEDNESDAY, AND THE REASON IS THE WHOLE BRIEF
The previous coordinator seat queued this as **tier 2** (a small, well-tested config change — 3 files,
+118/−5). **Wednesday read the diff and disagrees.** The tier rule's own words give full weight to
*data destruction* and *deploys*; this change is both, and it adds a third property neither of those
names:

**`enablePurgeProtection: true` CANNOT BE UNSET.** Azure permits enabling it and provides no path to
disable it. `softDeleteRetentionInDays` likewise cannot be **reduced** after vault creation. This
template runs **in the customer's own subscription**, on every Marketplace deployment that takes the
`not(parameters('useExistingKeyVault'))` path.

**So a wrong value here is not a bug we fix in the next release — it is a permanent property of a
resource in someone else's tenant that neither they nor we can reverse.** That is the strictest gate
we have, and it is round 1 of 2 under Kam's cap.

**None of this is a criticism of the change.** Wednesday's reading is that it is very likely correct
and well-argued. The tier is about what a mistake would cost, not how likely one is.

## 1. Target — four SHAs, four different facts
- **Branch:** `rd-363-keyvault-purge-protection-s43`
- **Head:** `b0dec96fc1f498b309cee692b6441ed9e9b0b043`
- **Its parent (the red-proof baseline the builder used):** `9546da5f5585eb6e215d935c4cae2a55c339104b`
- **`origin/main` head:** `a9a8cb6e3fc62b8c08e1f3aadecb08519f1f6ddc`
- **🔴 THE BRANCH IS 248 COMMITS AHEAD OF `main`.** Diffed against `main` this change reads as
  **254 files / +59,000 lines**. Diffed against its own parent it is **3 files / +118 / −5**.
  **The second is the change under test. Do NOT diff against `main`** — you would be reading 248
  commits of other people's work as if it were this PR.
  (Wednesday has asked the builder what NexusAI's real integration branch is; the answer is not in
  yet and this gate does not depend on it.)
- **Files:** `azure-marketplace/combined/mainTemplate.json`,
  `__tests__/marketplace-keyvault-durability.test.js`, `scripts/verify-expected-counts.json`
- **Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files` — **read-only to
  you.** Work in your own worktree/clone.
- **NON-PROD. NO DEPLOY. NO `az` COMMAND AGAINST ANY TENANT, AT ANY POINT.** Kam's 2026-09-07
  production lift is **Secuura only** (his 12:10: *"Only secure"*). Datasec production is entirely out
  of scope. **You may read ARM schema documentation; you may not touch an Azure resource.**

## 2. What the change actually does
    -  "softDeleteRetentionInDays": 7
    +  "softDeleteRetentionInDays": 90,
    +  "enablePurgeProtection": true
on the `Microsoft.KeyVault/vaults` resource, apiVersion `2023-07-01`, condition
`[not(parameters('useExistingKeyVault'))]`. Plus a long `comments` field stating the rationale, and a
112-line durability test.

**Why it matters (the builder's stated case, for you to verify not assume):** this vault holds
`nexusai-wrapping-key`, the RSA-2048 key wrapping the DEK that protects the customer's persisted
configuration (`backend/encryptionService.js`). **There is no backup of the wrapping key.** Without
purge protection, any principal with `Microsoft.KeyVault/locations/deletedVaults/purge/action`
(Contributor and above) can permanently destroy it after the soft-delete window.

## 3. 🔴 THE QUESTION WEDNESDAY MOST WANTS ANSWERED — the UPGRADE path, not the fresh deploy
Everything in the builder's rationale is about a **new** deployment. **Ask what happens to an
EXISTING customer who redeploys this template over a vault they created under the old values.**

    existing vault:  softDeleteRetentionInDays = 7,   enablePurgeProtection absent
    new template:    softDeleteRetentionInDays = 90,  enablePurgeProtection = true

- **`softDeleteRetentionInDays` cannot be changed after vault creation.** Does an ARM redeploy with a
  different value **fail the whole deployment**, silently no-op, or succeed? Establish this from the
  ARM/Key Vault resource documentation and from the template's own idempotency, and say which source
  answered it.
- If it fails: **every existing Marketplace customer's next upgrade breaks**, and the failure arrives
  as an ARM error in their subscription, not ours. That is a Major and it is exactly the class a
  fresh-deploy-only rationale cannot see.
- Is there a `condition`, an existing-vault branch, or an upgrade note anywhere that handles this?
  **If not, is that a defect in this change or a pre-existing property of the template?** Say which —
  and if pre-existing, **search the board by symbol/path/error-string before concluding it is
  unfiled**, and report what you searched.

## 4. THE COVERAGE GAP THAT MAY BE THE REAL ONE
The KV resource is conditioned on `not(useExistingKeyVault)`. The builder's own inherited comment
says vault creation **only fires in the legacy "pass-secrets-as-securestrings" path**, and that when
`useExistingKeyVault=true` the customer pre-creates the vault out-of-band.

**So: which path do real customers take?** If the common path is `useExistingKeyVault=true`, this
change protects **the path fewer customers use**, and the wrapping key in the majority case sits in a
customer-created vault with no purge protection and nothing telling them to enable it.
**That is not a reason to reject the change — it is a question about whether the ticket is closed by
it.** Report it as: what this closes, what it leaves open, and whether SEC-07's own wording is
satisfied.

## 5. THE DELIBERATE OMISSION — verify the REASON, do not "fix" the thing
The comment states that a `networkAcls` block with `defaultAction: Deny` was **deliberately not
added**, because the Container App resolves every secret through `secrets[].keyVaultUrl` using the
user-assigned identity — at deploy time **and on each revision** — so a vault firewall with no private
endpoint and no `ipRules` would **brick the deployment**.

**Do not add it. Do not recommend adding it.** Your job is narrower:
1. **Is the stated reason true?** Does the Container App really resolve secrets that way, on each
   revision, in this template? Read it.
2. **Is the reason pinned somewhere that fails loudly** if someone reaches for the obvious fix, or only
   in a comment? (The builder says a test cell pins it — verify the cell actually asserts the absence
   *and* the reason, and that it would fail if `networkAcls Deny` were added.)
3. **Is the residue tracked?** The comment says "Tracked on RD-363", and SEC-08 and SEC-11 are said to
   remain open on that same ticket. Confirm.

## 6. THE RED-PROOF — the builder's own claim, which is unusually good, so check it hard
Verbatim: *"Red-proofed at the base `9546da5`: 4 red, and the CONTROL is among them because with no
`enablePurgeProtection` to delete the tamper does not happen, so it refuses to pass vacuously."*

- **Re-run the red-proof yourself at `9546da5`.** Confirm 4 red and that the control is one of them
  for the reason stated.
- **Then prove the GREEN BASELINE at `b0dec96`** — a red-proof shows a check *can* fail; only a green
  baseline shows it passes for the right reason.
- **If any cell has more than one clause, red-proof each clause individually.** A multi-clause guard
  tripped by a fixture that breaks every clause has measured the pair and learned nothing about the
  parts.
- **A test that asserts on a JSON template is asserting on text.** Say what it can and cannot prove:
  it cannot prove Azure honours the property, only that the template requests it. Name that boundary
  rather than letting the cell imply deployment-level assurance.

## 7. The counts file
`scripts/verify-expected-counts.json` moves 2154/112 → 2161/113. That file **is** the CI gate's
expectation. Confirm the delta matches the cells actually added (+7 tests, +1 suite) — a counts bump
larger than the cells added is how a skipped suite hides.
**And note for your report:** the sibling repo learned today that its CI secret-scanning workflows pin
`actions/checkout@v7`, a major that does not exist, so those workflows fail before the scanner runs.
**If you can cheaply establish whether NexusAI's own CI actually runs this counts gate, do — a gate
that never executes is the same as no gate.** If you cannot establish it cheaply, say so and stop;
do not go down that road at the cost of this one.

## 8. Evidence rules — mandatory
1. **Every cell you count: say what it MOCKS and therefore what it cannot prove.**
2. **A zero, an empty result and a silent success are suspects, not evidence.** Distinguish "nothing is
   wrong" from "the check never ran" before reporting either.
3. **Capture `rc` on its own line** for any bounded command.
4. **An enumeration's file set and extension list are part of its claim** — an omitted path is a silent
   scope reduction that looks like a complete answer. Say what your sweep covered.
5. **Never delete.** Cleanup means quarantine.
6. **Findings-only. You never fix.**

## 9. Verdict
**GO** · **GO-with-findings** (mark each Major vs advisory) · **NO GO**. Severity is yours; priority is
Wednesday's. **Round 1 of 2** — a second NO GO ships what is closed and tickets the residue.

Report by mail to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Datasec RD-363 / SEC-07 (@ b0dec96, tier 1)`.

PROVENANCE:
- branch head `b0dec96fc1f498b309cee692b6441ed9e9b0b043` | `git ls-remote origin refs/heads/rd-36*` run by Wednesday in the same action as writing this | read 2026-09-07
- parent `9546da5f5585eb6e215d935c4cae2a55c339104b`, 3 files +118/−5 | `git show --stat b0dec96` | read 2026-09-07
- 248 commits ahead of `origin/main` `a9a8cb6e…`; 254 files/+59,000 when diffed against main | `git rev-list --count`, `git diff --stat` | read 2026-09-07
- the template hunk (`softDeleteRetentionInDays` 7→90, `enablePurgeProtection` added, apiVersion `2023-07-01`, condition `not(useExistingKeyVault)`) and the `comments` rationale | `git show b0dec96 -- azure-marketplace/combined/mainTemplate.json`, quoted from the diff | read 2026-09-07
- counts 2154/112 → 2161/113 | `git show b0dec96 -- scripts/verify-expected-counts.json` | read 2026-09-07
- the red-proof claim (4 red at 9546da5, control among them) | the builder's own commit message on `b0dec96` | read 2026-09-07
- "do not fix the networkAcls omission — it would brick every customer deployment" | the laptop seat handover `0_Brain/tasks/NEXT-PICKUP-DATASEC-LAPTOP.md` **and** independently the `comments` field in the diff above | read 2026-09-07
- tier cap of two NO GO rounds | Kam, 2026-09-05 20:19 | read 2026-09-07
- production lift is Secuura-only | Kam, panel 2026-09-07 12:07 + 12:10 *"Only secure"* | read 2026-09-07
- **UNMEASURED, stated as such:** whether ARM fails or no-ops on a `softDeleteRetentionInDays` change at redeploy; which `useExistingKeyVault` path real customers take; whether NexusAI's CI runs the counts gate. These are the gate's questions, not Wednesday's findings.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 17:39
