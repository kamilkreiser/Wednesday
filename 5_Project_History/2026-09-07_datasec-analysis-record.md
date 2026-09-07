# Datasec analysis record — 2026-09-07 evening (laptop seat)

**Written on Kam's instruction, panel 18:56:36:** *"where there is analysis, make notes of what was
found, what was tested, and how."* Every item below carries **FOUND · TESTED · HOW · NOT TESTED**.
Scope: the Datasec side only (Secuura is the Studio seat's, recorded separately).

---

## 1. RD-361 — auth gate fail-closed, round 2 (tier 1) → **NO GO, one Blocker**

**FOUND.** An interrupted first run **permanently bricks a fresh deployment.** The boot sentinel is
written on boot 1; `authEnforced` is written only by `POST /api/auth/enforce` (`server.js:3349`) or
the disable path (`:15426`). Between first boot and the admin completing setup the volume has a
sentinel and no `authEnforced`, which `authStateUnestablished()` reads as loss → UNKNOWN → deny.
**The deadlock is closed:** `/api/auth/enforce` sits in `setupOnlyPaths`, not `alwaysPublicPaths`, so
`requireAuth` denies the one route that could write the key. Only exit: hand-editing `settings.json`
on the customer's volume.
Also **F-B (Major):** the case-D fix is unguarded — flipping its sole producer leaves the suite green.

**TESTED.** The builder's four-scenario table re-derived on **both heads** (`e4d9147` and `1149d1c`);
the flag enumeration walked exhaustively including the HMAC-mismatch return and the outer catch;
eleven mutations, each clause individually; the six-site claim swept across the whole tree; the 503 +
`Retry-After` header; the full suite (2174/2174, matching the committed expectation).

**HOW.** Real `JsonStorage` over **real directories** — case D driven by a genuinely `chmod 0500`
directory, not a hand-set flag. Wire measurements against a booted server with a real CSRF token.
**Controls:** an empty volume serves `/first-run-setup` 200 and `/api/setup/status` 200 (so "round 2
denies everything" is excluded); the untampered head green. **F-B proved by red-proof M10** —
`jsonStorage.js:847` `= true` → `= false`, then `auth-gate-fail-closed.test.js` returns **20/20,
rc=0, blind**, while the gate's own cell goes red.

**NOT TESTED.** That the audit row *arrives* at `/api/admin/audit-log/export` — reaching it needs an
authenticated admin session and the state under test denies every route. Stated by the gate, not
discovered afterwards.

**Instrument errors the gate reported on itself:** a first `/api/auth/enforce` POST returned 403 — that
was CSRF, not the auth gate; re-run with a real token → 503. A first wiped-volume health check missed
`volumeWiped` because the body was truncated to 400 chars before matching.

---

## 2. RD-363 / SEC-07 — Key Vault purge protection (tier 1, raised from tier 2) → **GO-with-findings**

**FOUND.** The change is sound (`enablePurgeProtection: true`, retention 7 → 90). **Hard block on
publishing any offer version** until the redeploy-over-an-existing-vault path is settled, because
`enablePurgeProtection` **cannot be unset** and `softDeleteRetentionInDays` cannot be reduced after
creation — in a template that runs in the **customer's own subscription**.
It also **refuted a standing fleet claim**: `actions/checkout@v7` exists.

**TESTED.** The template hunk against the ARM resource semantics; the red-proof at the parent
`9546da5`; the deliberate `networkAcls` omission and whether its reason is pinned; the counts delta;
the `useExistingKeyVault` coverage question.

**HOW.** GitHub API `repos/actions/checkout/releases/latest` → `v7.0.1`, published 2026-07-20.
**Independently re-derived by Wednesday** in the same session: same endpoint, plus
`repos/actions/checkout/tags` showing majors v1–v7 with `v4` as the control; and
`grep -rn 'actions/checkout@'` over NexusAI's workflows → **4 × v4, 1 × v7, the v7 being
`gitleaks.yml`**. **Third, strongest corroboration from the builder — repo history:** the pin entered
`gitleaks.yml` 2026-06-30 (`cf50237`), main froze 2026-09-01, **104 commits landed in between, each a
gitleaks trigger.** Had the major not existed, all 104 would have failed at `Set up job`.

**NOT TESTED.** The sibling repo — the gate verified this for NexusAI and the action itself and said
so explicitly. Whatever is failing there is still open.

---

## 3. RD-362 — pen-test report exposure (tier 1) → **GO-with-findings; must NOT close as "containment achieved"**

**FOUND.** The report does leave the build context — **and SEC-03 redacted 1 of 5 carriers.** Four
unredacted copies remain tracked, one under a different name in `Final Documents/Working Documents/`
inside the build context. **`docs/runbooks/git-history-scrub.md` SHIPS INSIDE THE CUSTOMER IMAGE
carrying the recovery pointer in pasteable `<commit>:<path>` form** — SEC-04 excludes the report and
ships the map. **F4 (Major):** a short-form hash survives ~8 lines above the redaction and the key
directory is named ~12 below; the test's pattern only matches 40-hex preceded by `git show`.

**TESTED.** Build-context membership; `.dockerignore` ordering and precedence; carrier enumeration
across names and paths; the runtime-read control cell; the counts delta; whether SEC-02 is untouched.

**HOW.** A validated ignore matcher computing "routes break" **independently of the test**, rather
than inferring it. The commit hash **dereferenced to a live blob — type and size only, never content.**
The control cell tampered **five ways**, each tamper asserted to have LANDED first, base re-run green
afterwards: `*.md` → 1 FAILED (fires); `**/*.md`, `*.[Mm][Dd]`, `*.m?`, `PRIVACY.*` → **8 passed each
(silent)**, all four breaking the two live routes. A **leak gate with both controls** run over its own
outbound report so no secret, hash or blob path appears in it.

**NOT TESTED.** Anything requiring a built or pushed image — explicitly out of scope.

**Instrument error it reported:** a first tamper matrix returned **rc=1 on all five variants** and
looked like a clean red-proof. It was a jest config error and **the runs never executed.**
*"A 1 from a crashed command is no more evidence than a 0 from a killed one."*

---

## 4. RD-329 — public `/api/health` allow-list (tier 2) → **GO-with-findings; real but narrow**

**FOUND.** **6 tamper classes caught, 10 missed.** The guard holds the two spellings the builder
designed for, not the property its name asserts. **F-2 is the general one: the "belt-and-braces"
deny-list is NOT a second layer — it shares the allow-list's parser.** On tamper E, `nodeVersion` is
explicitly ON the deny-list, went out on the wire, and **both cells stayed green.** *Two layers that
fail together are one layer*, and the commit message presents them as independent. **F-3:** the
GUID-scrub cell asserts three character sequences exist in the file — scrub commented out with its
spelling left in place, and a raw GUID rides out on `degradedReason`.

**TESTED.** 16 tamper classes; the parent baseline; the counts delta; whether the repo actually
enforces the counts gate.

**HOW.** Each tamper `node --check` clean, and **each miss read off the wire from a booted server** —
not inferred. Misses include a `...full` spread leaking **+16 fields incl. `persistence.dataDir`**
(an absolute path), bracket notation, `Object.assign`, re-nesting under an allowed key, an alias
variable, **two keys on one physical line** (the regex is line-anchored), and an **allowed KEY with a
sensitive VALUE**. **Controls:** untampered tree GREEN, comment-only edit GREEN, positive tampers RED
— so the greens are vouchable. Parent measured independently at 2154/112; delta exactly +5 tests /
+1 suite.

**NOT TESTED / honest limits it named of BOTH instruments:** an allowed key carrying a sensitive value
defeats any key-based allow-list, source or behavioural; the commented-scrub case is the RD-362
pattern exactly.

**🔴 The most actionable line in the verdict:** the builder called source-reading *"the strongest
instrument available without booting the app"* — true as worded, **but this repo already boots the
app** (`__tests__/erasure-health-branches.test.js:97-143` spawns the real `server.js` on a reserved
port). Rebuilt on that existing pattern, the same allow-list **caught 7 of the 10 misses.**

---

## 5. RD-148 — SCIM revoke UI (tier 1, raised from the queue tail) → IN FLIGHT

Raised because it adds a **REVOKE control** — a destructive action on a security surface — with +103
lines of new product JS. Its three questions: whether the request names the row the admin is looking
at (bound at render vs re-read at click); whether the UI reports success from an HTTP 200 or from the
revocation; and whether the **server route** is guarded. **A constraint was stated to it up front
rather than discovered:** there is no drivable browser surface (builder wrapped, `localhost:3001` has
no listener — verified by `lsof`, deployed hosts out of scope), so it must either stand the app up
locally from that commit **and say it is a local run of the same commit**, or say plainly it could not
and name what a code/DOM pass cannot prove.

---

## 6. Security review, step 1 — ten components read by the coordinator

**FOUND.** Across ten components, **zero findings refuted.** From the six Wednesday read tonight:
**CONFIRMED 87 · REFUTED 0 · DOWNGRADED 8 · UPGRADED 3 · UNVERIFIABLE 1**, on top of the earlier
four's 62-re-derived / 0-refuted.
**Two new highs not in the seed:** `V-OXPD-A` — unauthenticated device-code minting on a LAN port
using the organisation's own tenant and client secret, depositing a completing user's access **and
refresh** tokens into the attacker's session; and `V-01` (Reporting Dashboard) — the pen-test report
quotes three former signing secrets in cleartext **with `.gitleaksignore` working-tree fingerprints
suppressing exactly those lines** while the file's own header claims the tree scans clean.

**TESTED.** Each verifier re-derived the finder's mechanism at source — current `file:line`, quoted
code read by them, CVSS components checked against what the code does, compensating controls hunted
deliberately, and the class hunted beyond the listed instances.

**HOW.** The verdict set is five values with mandatory evidence per value, and a **REFUTED requires a
positive control proving the search could have found the thing.** Method visible in the downgrades:
`OXPD-02` High→Low because the only caller of the vulnerable function **has zero callers**;
`OTP-31` High→Low because the portal's gate is a server-issued bearer, not ASP.NET middleware;
`OTP-32` H→M because a finder item was simply wrong (`minReplicas: 1`, not 2); `MYPKI-01` Critical→High
because **the finder's own control grep had been mis-run** — it reported 0 hits for a KDF, the re-run
returns 7.

**NOT TESTED.** Anything live — the engagement is static and read-only by rule. Each file names the
exact live check that would settle its UNVERIFIABLE rows.

**Why the zero is credible:** the same passes moved severity *down* eight times and refuted an
estate-wide escalation. A register whose rows get knocked down is one whose surviving rows carry weight.

---

## 7. Wednesday's own measurements this evening

| Claim | How it was established | Control |
|---|---|---|
| No RD-361 gate was running despite the handover saying so | `tmux list-panes`, `find '*rd361*'`, `grep -rl RD-361 briefs/`, `alerts.log` | each with a positive control (`find '*ks930*'` → 3 hits; `grep -rl KS-930` → hits) |
| `actions/checkout@v7` exists | GitHub API releases/latest + tags | control major `v4` present |
| The residue has no ticket | Jira REST `text ~ "authConfigs"` (2), `"SEC-01"` (3) | control `"Key Vault"` → 15 hits; all under the 20 limit, so untruncated |
| RD-363 is SEC-07/08/11, not SEC-01 rem 3 | Jira REST `issue/RD-363` and `issue/RD-361` | both resolved, so the reader works |
| 7 project repos hold stale ssh pointers; the vault's is healthy | `git config -f <cfg> core.sshCommand` per repo | quoted-form extraction; a forced missing spaced path still warns |
| No launcher heals the vault pointer | `grep sshCommand Launch_Wednesday.command` → 0 | control: `Notes (MASTER)` → 1 hit, so the launcher does reference the vault |
| `kam_rulings_today.sh` returned a stale answer | it printed 65 messages ending 13:40 at 18:13; the same script now prints 70 | the five missing messages appeared after a `pull` |
| I never told Kam he had been quiet | grepped this seat's own six panel messages, sentence by sentence | first grep too loose (bare "quiet" matched six unrelated sentences); narrowed before it answered |

**Fixes shipped, each with both branches exercised:** `chat_reply.sh` self-heal (recovers 1630 entries
where the old logic silently dropped 6 including the two newest) · `doctor.sh` travel-pointer sweep now
covers the shared vault (fire path 7 warnings, quiet path silent **and proven swept**) ·
`kam_rulings_today.sh` freshness line (quiet / fire / disabled).

---

**Evidence paths.** QA reports live under the QA project's own
`projects/nexusai/reports/2026-09-07-*` directories, named in each verdict mail. Verification files:
`!CODING/Datasec/Security Review/_Working/verification-2026-09/`. Gate briefs:
`WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-07_nexusai-*`. Launchers:
`WEDNESDAY/2_Project_Files/fleet/state/launch_qa_nexusai_*.sh`.
