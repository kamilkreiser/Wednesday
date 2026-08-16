# Kam decision sitting — 2026-08-14

> **Status at ~12:5x (fresh session).** The Kintsugi deploy you authorised is
> **RUNNING** — Secuura session 34, launched as this session's first act, demo only.
> **Items A, B, 1, 2, 3, 4, 4b, 5b and 7 below are still open and still yours.**
> Nothing here has been actioned on your behalf; items 5 and 6 are struck through
> because you ruled them.
> **The two most time-bound: item 4 (a live defect in Will's tool, now in its seventh
> day) and HPSM-25 Amplify, which was due today.**

## ✅ RULED 2026-08-14 ~12:4x — all 18 backlog decisions CLOSED
Twelve accepted as recommended. The six that needed him:
- **KS-621 — `organization` IS A SECURITY BOUNDARY.** Net-new enforcement; neither
  layer scopes by org today, so this is a model to build and **it changes the schema**.
  Design comes to me before any code.
- **KS-239 — SIGNED OFF.** Erasure irreversible and complete; downstream GDPR tickets
  can stop citing it as open.
- **KS-386 — a DATA-MODEL ruling, not a retention answer.** *"we do not hold PII. you
  need to record what was done (typically with partners) to what level, etc. not the
  actual data"* — Platform K should not hold the KYC images at all; it keeps the
  **attestation**. Split: design + stop-storing is the agent's; **disposal of existing
  data is irreversible and stays Kam's explicit signature.**
- **KS-263 — deferred to next week.**
- **KS-339 — Kam discusses access with Phil and Steve himself**; Stuart worked on it
  last. Nobody contacted.
- **KS-101 — priority DOWN**: Platform K does not need the Stripe consolidation, no
  near-term commercialisation. Kam requests the info from Stuart; external contact is
  his and I have contacted nobody.

**Also ruled: the Kintsugi hold is LIFTED and the deploy is authorised** (demo only;
production untouched and still his signature).

> ✅ **DONE 2026-08-14 05:07Z — cutover complete, 33/33 healthy, `cardanoMode: REAL`,
> zero build failures across 30 images.**
> 🔴 **CORRECTION to what I told you: revocation was NOT off beforehand.** My brief and
> this queue both said KS-617 "restores gateway session revocation, currently off on
> demo". **It was on.** The agent measured it: revoked tokens returned 401 on covered
> endpoints both before and after. **What was missing is the guarantee that a Redis
> outage cannot silently switch it off** — now proven over a 45-second outage with both
> controls. A narrower and true claim. The wrong sentence came from my own project's
> notes and I relayed it without checking it against the system.
> **Also less precise than I reported: the "seven already live" split** rested on a
> marker sweep that grepped only `/app/dist` while three fixes live in a shared package.
> The old images are gone, so it cannot be re-run. **Five are proven by behavioural
> probes taken before cutover; the rest are inference and the board will say so.**

---

## STILL OPEN — needs Kam

### 🔴🔴🔴 0c. Secuura / Blockchain — **KS-486 ESTABLISHED: a tenant-scoped org admin can mint a live `sk_` key into ANY tenant, and the credentials to be one are in tracked source**
**NEW 2026-08-16, established by session 37 with controls, not inferred. Nothing has been
touched, no code written, no probe run against the demo. This outranks everything below it.**

**What is live** (their measurement, run as a pure function against the real `decideMint` —
no service booted, nothing written, **4 denies and 4 allows on the same call path** so it
discriminates):
- Any caller in `KEY_ADMIN_ROLES` mints an `sk_` key into **any tenant**. That set includes
  **`ORG_ADMIN` and `ISSUER_ADMIN`, which are tenant-scoped roles** — so **one customer's org
  admin mints a live key into another customer's tenant.**
- It can also mint a **wildcard `*`** scope and **`organizations:register`** — **the two limits
  the provisioning branch enforces explicitly and the admin branch skips.**
- Reachability traced, not assumed: `POST /api/security/keys` → `proxy.ts:902-904`
  (`authenticateToken` only, **no** `enforceAdminProxy` — that is applied to `/api/admin/`, not
  here) → rewritten to `POST /api/keys`. **The gateway contributes no tenancy check.**

**What I verified myself, because it decides the severity:** the seeded org-admin credentials
are present in **TRACKED source — 12 tracked files for one, 7 for the other** (positive control:
`ORG_ADMIN` resolves in 76 files; negative control returns 0; **values not printed**). **So the
precondition is not "an attacker who has compromised an org admin" — it is "anyone who can read
the repository."** I have **re-rated it Urgent**, which is inside my scope.
✅ **BOUND, 20 minutes later, by the agent — and this is a correction to what I first told you.**
I said I could not establish the repository's visibility. **It measured it: `Secuura/Distributed_Secuura`
is `private`, 0 forks** — with controls both ways (a nonexistent repo returns 404; a known
public repo returns `public`, so the field is not a constant). **So "published to the world" is
now DISPROVEN rather than merely unestablished.**

🔴 **What that changes and what it does not.** It **narrows the population, not the ceiling.**
The exposed set is everyone with read access to that repo — collaborators, any future fork, any
leak — which is still categorically wider than "someone who compromised an org admin". **Urgent
stands**, and the agent wrote the bound onto the ticket in those words specifically so it cannot
be quoted back as a downgrade. **My original sentence is recorded as mine, with its limit
intact, beside its correction.**

**Half the register row was WRONG and that matters too:** *"no role check / any authed user"* is
**false** — KS-480's gate landed 2026-07-30 and the row was written 2026-07-21, so the cited
lines now contain the fix. **Four further rows in the same file are live** and all share one
shape: *the role gate landed, a tenant/ownership check never did* — `GET /api/keys` leaking key
ids across tenants, `DELETE /api/keys/:id` revoking on id alone with no ownership check (**those
two compose into cross-tenant revoke, i.e. auth denial-of-service against another customer**),
`/api/events` ungated entirely, and `/api/rate-limit/reset` ungated.

🔴 **WHY THIS IS YOURS AND NOT MINE, and it is your own ruling doing the work.** The remediation
is one line in a unit-testable pure function and would ordinarily sit inside my v1.3 scope.
**But on 2026-08-14 you ruled on KS-621: *"`organization` IS A SECURITY BOUNDARY. Net-new
enforcement; neither layer scopes by org today, so this is a model to build and it changes the
schema. Design comes to me before any code."*** **This fix is that model arriving through a
different door** — binding mint to platform-admin-only decides *who may provision across
tenants*, which is the model itself rather than an implementation of it. **So I stopped it, and
told the agent I could not waive your ruling.**

**Options:** (a) rule the design now — platform-admin-only for cross-tenant mint, plus
wildcard/self-replication limits on tenant-scoped admins — and I commission it under your design
· (b) fold it into KS-621's model work and accept the exposure until that lands · (c) authorise
a narrow containment change only (deny cross-tenant mint for tenant-scoped roles, nothing else)
while the model is designed properly.
**Recommendation: (c) now, (a) deliberately.** (c) is the smallest change that closes a live
cross-tenant path, is behaviourally testable in one file, and does not pre-commit the model;
(a) needs your design time and should not be rushed on a Sunday. **Not (b) alone** — KS-621 is
schema work and this is reachable today.

**Also yours, and I have done neither:** whether Peter or Stuart are told, and when. **External
comms are your class.** The demo credential question is the part they would most want to know.

**Executed under my ruling, no code:** KS-486 re-rated to Urgent (read-back confirmed), the
five-row verdict table on the ticket **with the stale half stated as loudly as the live half**,
the `x-tenant-id` vector killed on the ticket so the fixer is not sent to the wrong file, and
the four live rows filed and linked — **KS-642** (`GET /api/keys` BOLA) · **KS-643**
(`DELETE /api/keys/:id` ownership) · **KS-644** (`/api/events` ungated) · **KS-645**
(`/api/rate-limit/reset` ungated). **KS-644 is the one to look at first of those four: it is the
only one whose precondition is ANY authenticated user, no admin role — the widest door of the
set.** Your KS-621 ruling is quoted on KS-486 as the reason no code was taken, so nobody picks
it up as a quick win.

### 🔴 0d. Secuura / Blockchain — **KS-489: prism forges VC signatures and verifies nothing, unconditionally in every environment — but nothing outside can reach it**
**NEW 2026-08-16, established the same session and deliberately NOT escalated to Urgent by
analogy with 0c, which I think was the right call.**

**Both code halves are live and exactly where filed.** A `proofValue` of
`crypto.randomBytes(64)` presented as an `Ed25519Signature2020`; and the verifier passes on **the
presence of a `proof` object** without ever reading `proofValue` — **so any credential a caller
supplies verifies `true`**, not merely prism's own forgeries.

🔴 **The register's risk shape was wrong and the truth is worse: there is no flag to forget.**
It was filed as *"a prod deploy that forgets the flag"*. `PRISM_MODE` appears five times and is
**branched on zero times** (control: `NODE_ENV` **is** branched at three sites in the same file).
**So mock issuance and mock verification run unconditionally in every environment — a gate that
does not exist cannot be closed by a deploy checklist.** Both deploy paths already set it to no
effect. **Plus an honesty defect: prism reports `mode: "basic"` while behaving as a mock**,
misreporting its own trustworthiness to anything auditing it.

✅ **Why it is not Urgent: there is no external route.** The gateway proxies `/api/credentials`
to **vc-issuer**, not prism; prism is exposed only at `/api/did`, and it publishes no host port
(control: the same file publishes 7 ports elsewhere, so the instrument can see ports when they
exist). **Kept High on artefact-integrity grounds — a forged VC is portable and outlives the
network boundary containing its issuer — so reachability is a reason to SCHEDULE it, not to
downgrade it.**

**YOUR CALL, and it is a scope question rather than a remediation:** prism and vc-issuer both
implement `/api/credentials/*` and only vc-issuer is wired to the edge. The register itself says
the fraud pattern was *removed from vc-issuer* and *remains here*.
**Options:** (a) **delete** prism's credential surface — removes the class outright and is the
smallest change, but decides prism's purpose by default · (b) **implement** real Ed25519 —
largest change, possibly for a service nothing calls · (c) **fail closed** — the mock paths
refuse rather than forge, and `mode` reports what it is actually doing.
**Recommendation: (c) now, then (a) or (b) deliberately.** (c) contains the artefact-integrity
risk **without deciding whether prism is a product surface**, which is the part that is yours.
**Nothing has been taken — not even (c).** I stopped it for the same reason as 0c: deciding what
a service IS is a scope change, and that is your class, not mine.



### 🔴🔴 0. Datasec / HPSM — **THE AMPLIFY WINDOW HAS CLOSED. This is a premise that expired, not a deadline to hit**
**NEW 2026-08-15, and it outranks everything else on this page.**

The 112-day plan cannot reach the **Sat 5 Dec** Amplify anchor from any start date after
today. **I computed this myself rather than relaying it:**

| NTP | Release (NTP + 112d) | vs Amplify Sat 5 Dec |
|---|---|---|
| Fri 14 Aug — last business day | Fri 4 Dec | 1 day before |
| Sat 15 Aug — today, the exact cutoff | Sat 5 Dec | the day itself |
| **Mon 17 Aug — the day of your session** | **Mon 7 Dec** | **two days after** |

(5 Dec 2026 is indeed a Saturday — checked, since the whole anchor rests on it.)

**Stated carefully: I do not know whether you actioned HPSM-25 on Friday, and the project
cannot know either.** If you did, this is moot and I would like to hear so. If you did not,
**Monday's session opens on a premise that no longer holds** — and D-11 stops being *settle
the date* and becomes *which fallback*: slip with §6 relief · compress · re-anchor · or
announce-at-Amplify-then-release.

**How it surfaced, which is the part worth keeping:** a routine tracker-maintenance pass
re-derived row zero instead of carrying it forward. The row still read *"STILL OPEN — one
day left. Today is Thu 13 Aug."* **The cheapest possible discipline caught the most
expensive available finding.** Session 9 predicted exactly this: *"Monday would open by
re-deriving its own premises."*

**Recommendation:** decide the fallback before Monday rather than in the room. **I have not
actioned HPSM-25 and nobody has contacted HP.**

~~⚠️ **Related, and NOT verified by me:** NTP 31 Aug ⇒ hypercare ending **4 Jan 2027**
against **1 Jan** as recorded — the overlap is worse than we had recorded.~~
✅ **WITHDRAWN 2026-08-15 by the next session, which established the source.** CT §16 says
*"10 business days following production deployment"*, and **the inclusive reading is the only
one that reproduces §17's own baseline** (30 Nov → 11 Dec). **So 1 Jan was right and 4 Jan is
withdrawn.** It reached you labelled as unverified precisely because I could not re-derive it,
and that labelling is why the correction costs nothing.
*(I verified the instrument claim myself: `verify_deck.py:116` hardcodes
`hypercare_end = 2026-12-11` and counts business days between two fixed dates — it asserts what
the deck says and cannot establish a duration. An instrument mistaken for a source.)*

🔴 **What replaced it is REAL, and one half bears directly on your Amplify decision:**
1. **"Business day" is undefined in all four documents** — and the window crosses the Christmas
   shutdown, where the difference is not academic.
2. 🔴 **§17 does not rebaseline while everything else does.** **So on a slipped NTP, the SOW
   schedules hypercare BEFORE the release it supports.** That is a direct consequence of the
   slip option in item 0 above, and it should be priced into whichever fallback you choose.
*(Both are the agent's measurements. My own corpus grep errored — and its positive control
errored with it — so I am reporting no number of my own in either direction.)*

### 🔴 2c. Datasec / HPSM — **six sessions of analysis exist on ONE DRIVE, outside version control**
**NEW 2026-08-15. Found by the agent at its own wrap and disclosed as *"the wrap exposed
something the wrap cannot fix"*. I verified it myself, with a control.**

**`2_Project_Files` tracks exactly two files: `.gitignore` and `README.md`.** And
**`1_Project_Definition` — which holds all 30 registers, D01, BACKLOG.md and every artefact of
six sessions — is not inside any git repository at all.** (Positive control: NexusAI's repo
returns 471 tracked files, so the command works.)

🔴 **It also invalidates a check I ran twice today.** I verified "pushed, not merely committed"
on this project before closing its pane and again in a score — `status -sb` 0/0, `rev-parse`
matching. **Both true, both meaningless: a clean in-sync repo containing nothing is
indistinguishable, by every command I ran, from one containing the work.** Ledgered.

**Why it is yours and not mine:** the agent named the reasons and they are real — **K5 is your
decision, `Source_Documents` was deliberately kept structurally outside git, and part of the
corpus is NDA-adjacent.** Committing an analysis tree that sits beside HP's own documents is a
call with consequences. **It did not act, and it was right not to.**

**This is the same class as item 2b** (launchers untracked across all 13 projects): **work that
exists on one drive, where the ritual that is supposed to protect it fires and has nothing to
carry.** Your standing requirement is maximum portability; these two are where it is currently
untrue.

**Options:** (a) version the analysis tree in the project repo, with `Source_Documents` staying
excluded · (b) leave it out of git but bring it into a drive-level backup that actually runs ·
(c) a separate private repo for analysis only, keeping the NDA corpus structurally apart.
**Recommendation: (b) now — it is reversible, needs no decision about NDA material, and closes
the "one drive" exposure today — then (a) or (c) deliberately when you have time to weigh the
corpus question.** I have changed nothing.

### 🔴 0b. Datasec / HPSM — **an M6 evidence pack can be assembled from the PRD's own identifiers, PASS, and prove the wrong thing. A$75,000.**
**NEW 2026-08-15, and it is a Monday item.**

**§17.1 gives EPIC-011 the identifier range AI-001…AI-020. All five AI-nnn rows in PRD
Appendix F are assessment-integrity tests — 5 of 5.** So anyone building M6's AI acceptance
evidence by following the PRD's own numbering **assembles assessment evidence, and it passes.**

**A complete-looking, internally-consistent, WRONG evidence pack for a 10% / A$75,000 gate** —
dangerous precisely because it succeeds. Nobody re-examines a green pack whose identifiers
match the contract's own scheme.

🔴 **And it gates on something unresolved: three of the four contracted assistants do not
appear in the PRD under their contracted names.** The SOW contracts *"Assessment Copilot,
Opportunity Agent, Proposal Agent and QBR Agent"*; **Opportunity / Proposal / QBR return zero
occurrences in the PRD, and the PRD's names return zero in the SOW.** The two documents name
the same four capabilities and **share exactly one name.** For three of four, *"relevant"* must
be settled by inference **before evidence can start** — and if nobody settles it deliberately,
it gets settled accidentally by whoever builds the pack.

**Also found, same sweep:** the AI scope conflict is in **three** places, not the one the
ticket named — §14's MVP Status column, the functional-requirements table (of thirteen priority
rows, ten Must, two Should, and the single Future/Should row is the AI row), and the API table
marking the QBR endpoint "Future scoped".

**A proposal already exists** —
`Registers/2026-08-15_HPSM-29_M6-AI-acceptance-criteria-PROPOSAL.md`: seven cross-cutting
criteria plus one per assistant, **each traced to a clause already binding, so accepting them
adds no scope.** Every criterion is a governance property, no model-quality bar, because that is
what §4 and §9 contract. **Partner Training Copilot deliberately EXCLUDED** — §4 does not name
it and §18 puts it in the 2027 expansion as "Separate SOW / CR", so including it would be us
widening our own scope.
**All 36 citations machine-checked against freshly extracted text, 36/36, with two positive
controls** (a fabricated quote and a real quote with one word altered — both correctly reported
missing).

**Recommendation:** take the naming/mapping question into Monday explicitly. **It is cheap now
and expensive later** — it decides what M6's evidence has to prove, and the current default
answer is one that passes while proving something else. **Not verified by me:** these are the
agent's measurements; I have re-derived only that M6 is 10% / A$75,000, from the SOW `.docx`.

### ⚠ 0e. Secuura / Blockchain — **Review F's edge protections are merged, and nobody can say whether they are RUNNING on the internet-facing demo**
**NEW 2026-08-16.** F-2/F-3/F-6/F-7 are confirmed fixed **in code** on `develop` — 9 `limit_req`,
4 `limit_conn`, a body cap, compose ports loopback-bound, against **0/0/0** as originally filed.
**Whether any of it is live at the edge is UNESTABLISHED**, and a prior note says not yet,
pending the Kintsugi hold.

🔴 **The agent's sentence is the reason this is on your page: *"a merged-but-undeployed edge
protection provides exactly zero protection"* — and the demo is internet-facing.**

**Why it could not just be checked:** a single read-only GET returns HSTS, CSP and
X-Frame-Options and **none of them discriminate** — the CSP cannot have come from that config
because its own CSP is commented out, and Caddy terminates TLS in front, so HSTS is
unattributable. **The checks that WOULD discriminate — tripping `limit_req` for a 429, or
exceeding the body cap — are abuse-shaped against a live demo, and it did not run them.**
Recorded as unestablished rather than inferred from the merge, which is right.

**Recommendation (the agent's, and I have adopted it):** make live-edge verification a
**condition on whatever lifts the Kintsugi hold**, with a deliberate 429 probe **in a
maintenance window** — not opportunistically. That pairs a write-shaped check with the one
moment it is appropriate. **Nothing has been run and nothing deployed.**

### ⚠ A2. Secuura / Blockchain — **NEW 2026-08-15: a CI landmine whose only mitigation is that people happen to remember it**
**Peter merged PR #698 yesterday and then reviewed his own merged diff, finding EIGHT items**
(his headline says seven; the agent counted and found the eighth — and **my own report to
you said seven too, because I took his count instead of counting**).

**The one that needs you is item 2.** `PRE_MERGE_TIMEOUT_MS` was raised to 3600s while
`Akto pre-merge (full)` still carries `timeout-minutes: 30`. The poll budget is 54 minutes
against a 30-minute cap, **so whoever dispatches `pre-merge-platform-suites.yml` first gets
a job killed at 30 minutes with no report and no artifact — which reads as a failure of the
thing being tested, not as a cap nobody raised.** Peter's own words: the old landmine was
*"relocated, not defused"*.

**Why it reaches you:** the warning currently lives in a comment on **KS-441, a ticket about
Akto scan throughput assigned to Peter** — correctly recorded and badly placed. The agent's
framing, which I have adopted: **a message is the weaker half; a guard does not decay.**
- **Done by me today (stopgap):** the agent posts the arithmetic and consequence on the
  ticket a dispatcher would actually look at, **@-mentioning Stuart** (a Linear @-mention is
  my scope; a mail to him is yours, and I have sent none).
- **Yours:** the durable fix is the workflow itself refusing or announcing the mismatch when
  dispatched. **That is shared CI — Peter's or Stuart's change, not ours.**
**Recommendation:** let the stopgap stand today, and raise the guard with Peter next week
rather than us touching a merge-blocking workflow he has claimed. **Nothing is broken right
now; the exposure is entirely "first person to dispatch".**

### ⚠ 2b. WORKSPACE (all 13 projects) — **`Launch_Claude.command` is not tracked in git, so launcher fixes live on one machine only**
**NEW 2026-08-15. Raised by the NexusAI agent, ruled by me as one workspace item rather than
thirteen project tickets — and it is above my authority because it changes a convention you
set across the whole workspace.**

**The finding:** each project's repo is `2_Project_Files/`; the launcher sits **above** it and
is therefore untracked. So when an agent fixes a real launcher bug — as NexusAI did today at
line 169 — the fix is **not committed, not backed up beyond a manual `.bak`, does not
propagate to your laptop or the T9, and is invisible to anyone verifying the ticket by pulling
the repo.** A reviewer would correctly conclude nothing was fixed.

**Why it is not cosmetic:** your two standing requirements are never getting the client wrong
and **maximum portability**. This is squarely the second. **And it is invisible from inside any
single project**, which is why it has not been raised in thirteen tries — the agent only saw it
because it was asked to fix the launcher and then asked what "fixed" meant.

**The care needed, stated so it is not waved through:** launchers export per-project
`AZURE_CONFIG_DIR` / `GH_CONFIG_DIR` and key paths. They are the mechanism that keeps client
identities isolated (hard rules 4 and 5). **Tracking them is a decision about where
identity-isolating config lives**, not a tidy-up — which is exactly why I am not making it.

**Options:** (a) track each launcher in its own project repo · (b) keep them untracked but add
them to a drive-level backup/sync so fixes survive and propagate · (c) leave as is and accept
that launcher fixes are per-machine, recording that on any ticket that touches one.
**Recommendation: (b) as the cheap immediate step, (a) considered separately per project** —
(b) closes the portability gap without changing what any repo contains or where identity config
lives. **Not (c) alone**, though (c)'s recording discipline should apply regardless, and I have
already required it on RD-96.

### 🔴 7f. Datasec / NexusAI — **NEW 2026-08-16: the gitleaks gate is blind on `package-lock.json`, and it stays green over it (RD-99)**
**Found by the agent while satisfying RD-77's own criterion 4 — "review the allowlist" — not by
looking for it. Its method is a canary matrix: one secret value, varying only the PATH, with a
caught control at the top, run on a CI-equivalent tree.**

| path | result |
|---|---|
| `backend/probe_plain.js` | **exit 1 — CAUGHT** (control) |
| `__tests__/probe.test.js` | caught |
| `backend/__tests__/probe_fixture.js` | **exit 0 — NOT caught** |
| `docs/PEN-TEST-REPORT-2026-04-25.md` | **exit 0 — NOT caught** |
| **`package-lock.json`** | **exit 0 — NOT caught** |

🔴 **The material one is `package-lock.json`, allowlisted wholesale.** It changes on nearly
every dependency operation and **it is exactly where registry credentials embed themselves. A
secret landing there today commits under a green gate.**

**And an inconsistency nobody could predict from reading the config:** the test-path pattern
requires a parent directory before the slash, so **this repo's root `__tests__/` is scanned
while nested test dirs are blind.** The agent's framing, which I am quoting because it is the
point: **the current safety is an accident of where the tests happen to live, not a decision.**

**Context that makes this the right week for it:** RD-77 (which fixed *value*-based
allowlisting and widened the scan to full history) verified clean this morning — **`history
without .gitleaksignore` returns 37 real findings**, proving the scanner genuinely scans. The
path allowlist predates that work and was never revisited.

**Options:** (a) remove the `package-lock.json` path allowlist and triage whatever it surfaces ·
(b) narrow it to the noisy fields rather than the whole file · (c) fix the nested-`__tests__`
pattern only and accept the lockfile hole · (d) leave and document.
**Recommendation: (b) then (a)** — narrow first so the gate does not go red on integrity
hashes, then remove entirely once triaged. **Not (d)** — an undocumented blind spot in the one
file that changes constantly is how this survived in the first place. **Reversible CI config,
so this is inside my scope to commission once you have ruled on the lockfile question** — I am
asking because it changes what a merge-blocking gate accepts, not because I cannot act.

### 🔴 7d-bis. Datasec / NexusAI — **RD-55's scrub, as currently scoped, would leave the secret on `main`**
**NEW 2026-08-16, and it changes a ticket already on this page.** `.gitleaks.toml` carries the
PT-002 secret **value literally in its canary rule** — a normal pattern for a gitleaks config,
but it means **the value lives in a tracked file independent of the pen-test report.**

**So if RD-55's scrub is scoped to the report plus git history, that copy survives it, and
RD-55 closes with the value still on `main`.** Neither file has been edited and the value has
not been quoted anywhere. **Fold this into RD-55's scope before it is actioned** — it does not
change the rotation decision, only what "done" has to cover.

### 🔴 7d. Datasec / NexusAI — **RD-55 sits at LOW while a plaintext secret is in a TRACKED file**
**Found today by the NexusAI agent during a condition-3 credential audit, not by looking for
it.** A `COORDINATOR_SECRET` value is not merely in git history — it is **in the current
working tree in plaintext**, at `docs/PEN-TEST-REPORT-2026-04-25.md:296`, because the
pen-test report quotes the vulnerable line *including its value*.
**Why that is a different thing from the history problem:** history needs a scrub; **a
tracked file needs a commit.** RD-55 covers both and is priority **Low**.
**Live config is clean** — `docker-compose.yml:89` is now fail-fast with no default, so
nothing runs on the burned value. The agent did not quote the value anywhere and I have not
either.
**Options:** (a) raise RD-55 and treat the tracked-file half as its own near-term item ·
(b) leave the priority and handle it with the eventual scrub · (c) redact the report.
**Recommendation: (a).** **Not (c) without you deciding it** — that file is evidence in a
security report and redacting it is a judgement about the document, not a cleanup. **Rotation
and scrub are your signature; I have touched neither and told the agent not to edit the file.**

### ⚠ 7e. Datasec / NexusAI — **the near-miss worth knowing even though nothing is exposed**
RD-88 exempts two coordinator routes from sign-in on the demo. The agent stopped on my own
condition 4 and checked what that change would mean for the shipped Marketplace image.
**No current template sets `COORDINATOR_SECRET`, so a customer would get an endpoint that is
exempt from sign-in and still 403s everyone** — exempted but unreachable. **The retired
VM-era templates, however, set it to the literal string `disabled`.** One template generation
earlier, that change would have shipped every customer an unauthenticated read/write endpoint
whose secret was a publicly-readable word.
**No action needed from you.** I ruled the fix must be **gated on a configured secret**, so
the shipped artifact is unchanged by construction rather than by the current contents of
templates nobody is watching. Recording it because the near-miss is the argument for the
boundary, and because it is the first time condition 4 has fired.

### 🔴 A. Secuura / Blockchain — **five findings that are one defect: signals firing into channels nobody reads**
Filed by session 33. **Four of the five were found by reading a red that already
existed** — nothing was hidden. Three are time-sensitive.

- **KS-636 — a CRITICAL CVE in the base image of all ten services, unread for 13
  days.** The watchdog flagged `node:24-alpine` CVE-2026-59873 on **2026-08-01**. It
  worked. Its failure — which its own header calls the reminder — went unread.
- **KS-637 — the nightly Internal Audit has failed 40 runs straight** (2 successes in
  its last 100), dying at "Boot dev stack" before any job runs. **DAST,
  tenant-isolation, licence-compliance and the Aiken contract tests run NOWHERE
  else.** Tenant isolation matters especially now: **you have just ruled `organization`
  a security boundary**, and the tests that would prove it have not run in weeks.
- **KS-635 — a dated failure: an audit-baseline exception expires 2026-08-31**, and
  the gate then **blocks every push**. Its owning ticket is closed *and archived*, so
  **nothing on the board names the date.** Two and a half weeks away.
- **KS-638 — the team's own test board has never shown a green run**: 22 runs since
  2026-05-25, **0 passed**. The latest red is E2E passing 210/0 while the generator is
  *structurally incapable* of reporting passed. **The worst of the five, because it is
  read and disbelieved** rather than unread.
- **KS-634 — no CI gate runs the services' unit suites** since 2026-03-12.

**Recommendation:** these are not backlog items, they are the reason backlog items go
unnoticed. **KS-636 and KS-637 want action this week** (a critical CVE and the only
place four security suites run); **KS-635 wants a date in the diary before 08-31**;
KS-634 and KS-638 batch with the other CI work.

### ⚠ B. Scope guard on the hold lift — please confirm if I have it wrong
You authorised *"deploy the kintsugi queue"*, which I have scoped to **the demo VM
queue only**. **The extranet auto-deploys on push to main and remains held** — the
agent correctly declined to fix KS-638's one-line verdict bug for exactly that reason.
**I have not extended your lift to the extranet or anything else.** Say the word if you
want that surface unblocked too; otherwise it stays where it is.



### 1. Datasec / HPSM — **E14: does an executed CSPA exist, and can we read it?**
**Problem:** the CSPA sits at **rank 1 in SOW §3, above the SOW itself**, and it is
not in our corpus. It now gates four separate threads: the money half of the
reconciliation, X5's precedence question, X6's payment-terms deferral, and whether
the reconciliation day is worth commissioning at all.
**Options:** (a) it exists and Kam can share it → we read it and four threads unblock ·
(b) it exists and cannot be shared → we mark those four as permanently
assumption-based and say so in the Monday pack · (c) none was ever executed → that is
itself a finding and changes the precedence argument.
**Recommendation:** answer (a)/(b)/(c) — five minutes, highest-value open item across
the programme for five sessions running.

### 🔴 2a. WED — **NEW 2026-08-15: two Datasec projects hold a key that can read another client's mailbox**
**This supersedes how I framed item 2, and it is the more important half.**

**Measured today, values never printed — full sha256 of each project's `AGENTMAIL_API_KEY`:**

| Project | Key | Reads `coagent@`? |
|---|---|---|
| **Datasec/NexusAI** | **byte-identical to Wednesday's** — legacy **org-wide**, len 70 | yes (200) |
| **Datasec/Vision** | **byte-identical to Wednesday's** — legacy **org-wide**, len 70 | yes |
| Secuura/Blockchain | distinct, len 76 — **inbox-scoped** | no |
| Datasec/HPSM | distinct, len 76 — **inbox-scoped** | no |

**That org-wide key returns HTTP 200 on `secuura-blockchain@` and `datasec-hpsm@`**, with a
nonexistent inbox returning 404 as the negative control — so the 200s are real reads, not
masked failures. **Two Datasec projects therefore each hold a credential that can read a
Secuura mailbox.** Hard rule 2 / your "very important #1".

**Stated precisely, because the distinction matters:** this is a **capability, not an
incident.** There is **no evidence any cross-client read has occurred**; NexusAI probed
`coagent@`, its own inbox and a control, and reported all three. Nothing was read across.

**What makes it hard to close:** the 08-13 finding that **deletion is not revocation on
AgentMail** — deleting these keys removes them from the listing while they keep
authenticating. **So this cannot be fixed by deleting the key**, which is exactly what
WED-107's plan said to do.
**Options:** (a) issue inbox-scoped keys to NexusAI and Vision and finish the migration —
the org-wide key stays alive but stops being *in* those projects' `.env` files, which is
the part we control · (b) rotate the whole AgentMail account, if the vendor supports it ·
(c) accept and document.
**Recommendation: (a) now, (b) investigated alongside.** (a) is entirely ours, does not
wait on a vendor who has declined to commit to a fix, and closes the exposure that
actually sits on disk. **I can do (a) — say the word.** It is not approval-class, but it
touches two projects' credentials, so I am asking rather than assuming.

### 2. WED — **WED-108 (P1): re-send your signed v1.3 grant to each per-project inbox**
> 🔴 **CORRECTED 2026-08-15 — I had this wrong twice this morning and told you so both
> times.** I said the migration cut **every** migrated agent off from `coagent@` "by
> construction" and that **three** live agents were running on provenance-by-history.
> **False for NexusAI**, which measured `coagent@` at 200 with a 404 control and
> DKIM-verified your grant *today*. I generalised from two projects' reports and then
> quoted my own spec's wording as if it were a measurement.
> **The true scope: it affects the TWO genuinely migrated projects — Secuura/Blockchain
> and Datasec/HPSM.** NexusAI and Vision still hold the org-wide key and can read the
> grant. **The ask is still worth doing and is now half the size** — two inboxes, not four.
**Problem:** the per-project migration cut every migrated agent off from `coagent@`,
where your grant lives. **Two projects have now independently confirmed it** (Secuura
s30, HPSM s21) — both are running on provenance-by-history rather than a check they
ran today.
**Options:** (a) re-send the signed grant to `secuura-blockchain@`, `datasec-hpsm@`,
`datasec-nexusai@`, `datasec-vision@` · (b) leave it and accept that agents hold work
whenever an approval-class item appears.
**Recommendation:** (a). **Your hand only — a forward from me authorises nothing**,
and the agents have been told to refuse one if I ever offer it.

### 3. Datasec / Vision — **Will's PoC threshold: >5 or ≥5, and does 10 get encoded?**
**Problem:** Will writes both *">5 devices"* and *"less than 5 devices"* in one
paragraph, and *"really should be 10+ in a perfect world"*. The readings differ only
at exactly 5 devices.
**Options:** (a) **≥5** — a deal of 5 is acceptable, 1–4 raises the advisory ·
(b) **>5** — 5 itself raises the advisory · (c) also encode 10 as a second threshold.
**Recommendation:** **(a) ≥5**, because *"less than 5"* is his operative exclusion,
which puts 5 on the acceptable side. **Reject (c)** — he calls 10 a perfect world and
in the same breath says PoCs get insisted on with a couple; a live 10-gate rebuilds
the over-strict behaviour we are removing. The agent is proceeding on ≥5 with the
value in **one named constant**, so your ruling is a one-line change either way.

### 4. Datasec / Vision — 🔴 **the LIVE tool is still dropping PoC lines right now**
**Problem:** on a deal of 1–4 devices, ticking the PoC box **silently drops the PoC
line** — no charge, no flag, nothing on screen or in the PDF. **Live since 2026-08-07
19:16 (`49b3dfc`, v2.08) and STILL LIVE** — the fix is on main as v2.20 but **not
deployed**; `hpas-quickquote.azurewebsites.net` is running v0.3.2-tool2.19. Window so
far: **6 days 16 hours and open.**
**Two things that make it worse than it first looked:** the field seeded to
`min(dealDevices, 5)`, so **ticking the box was enough** — no unusual input needed —
and that is **exactly Will's population**, the small deals he wrote in about. Before
v2.08 the control was *disabled*, so an AM could see the rule refusing them; now they
tick it and get nothing back with no signal at all.
**Not a reversal by anyone:** collateral from the pricing-engine extraction — the
floor went into the engine against the wrong number and the UI's correct deal-size
gate was deleted as redundant in the same commit. **Nobody decided this.**
**Options:** (a) deploy v2.20 now, then tell Will with the dates · (b) tell Will now,
deploy when convenient · (c) deploy quietly and say nothing.
**Recommendation:** **(a).** The deploy is the part that stops the bleeding and it is
one action; the telling is yours and reads far better alongside "and it is already
fixed in the field". **Not (c)** — he found the rule himself and will connect the two.
**Whether any real quote was affected is unknown** — that needs production data and I
have not gone near it. **External comms and the deploy are both your class; I have
done neither.**

### 4b. Datasec / HPSM — 🔴 **M0's acceptance evidence cannot be produced by either party**
**Problem (new, 2026-08-14):** **M0 — 25% / A$187,500, the FIRST and LARGEST payment**
— is accepted on SOW §7.1's *"SOW/funding authority, named owners, delivery plan and
backlog mobilisation confirmed."* **P01 is unsigned, P02 is past due and unfilled, and
no Datasec staff are named in any document either** (§11's nine roles; D-13, open five
sessions). So neither side can currently produce the evidence for the first invoice.
**Stated narrowly, and this is the agent's own framing:** it is **not** a drafting
defect — "named owners" is unqualified and a mobilisation list could satisfy it.
**The defect is our own tracking:** every register records P02 as an input reshaping
*later* gates, never as the acceptance evidence for the *first* one. The ask-list
front page named M1, M6 and M8 as the money behind P02. **M0 is larger than all three
and comes first.**
**It also re-prices D-13:** the two open pod-lead names are not a resourcing question,
they are **half of M0's acceptance evidence** — a commercial argument for Monday.
**Options:** (a) raise it in the Monday session as a commercial item and fold it into
the HP correction bundle · (b) treat it as internal tracking only and fix our own
registers · (c) both.
**Recommendation:** **(c)** — the register fix is ours and free; the naming question
is HP's and belongs in the bundle. **Not yet verified by me** — flagged for the next
session to check against the SOW extraction before it reaches HP.
**Related, same session:** all eight gates read against the §6 prerequisite table for
the first time — **7 of 8 depend on a prerequisite, and all 6 paying gates do**, split
honestly between *unanswered* and *our proposal awaiting HP approval*. And a
correction in our favour: the silence calendar dated the content freeze to **M2**, a
gate carrying **no payment and naming no content**; the content actually lands on
**M3, 20% / A$150,000**, so we had been claiming relief against nothing.

### ~~5. Secuura / Blockchain — the Kintsugi deploy~~ ✅ RULED: DEPLOY AUTHORISED 2026-08-14
**Problem:** thirteen merged-but-unshipped changes sit behind the hold, **four of them
security fixes** — including KS-617, which restores gateway **session revocation**
that is currently not running on demo. The backlog sweep cannot close any of them
without asserting a fix is live when it is not.
**Now countable:** the agent measured the In Review column and **19 of 23 tickets have
a merged PR** — it is a merge-residue pile, not a review queue. **Twelve are moving to
"Tested Not Deployed" and deliberately NOT being archived**, so the deploy debt stays
visible as a standing number rather than disappearing off the board. **Your one deploy
decision clears all twelve at once.**
**Options:** (a) lift the hold and deploy the queue · (b) keep the hold and accept
that the demo runs without those controls, with the tickets openly labelled
"awaiting deploy" · (c) deploy a security-only subset.
**Recommendation:** ruling needed rather than a specific option from me — this is a
product/environment call, not a technical one. What I would flag: **the longer the
queue, the riskier the eventual single deploy**, and KS-617 is a control people may
assume exists.

### 5b. Secuura / Blockchain — **KS-634: no CI gate has run the services' unit suites since March**
**Problem:** `ci.yml` is `workflow_dispatch`-only and **last ran 2026-03-12**; the `pr`
workflow's `test:unit` is Playwright's own suite, not the services'. **So for five
months a unit suite could die at module load and nothing would report it — and one
did** (a 73-test suite found dead on `develop` this morning and revived).
**This is not a backlog item; it is why several backlog items exist.**
**Options:** (a) fix it as a scoped CI session, alongside KS-628 and #687 which are
also `pr`-workflow work · (b) leave it and keep finding dead suites by hand.
**Recommendation:** **(a)**, batched with the other CI work — it is shared CI that
Peter and Stuart depend on, which is why nobody has changed it at short notice.

### ~~6. Secuura / Blockchain — the backlog residue~~ ✅ RULED: all 18 decided (see top)
**DELIVERED.** Full document in the Secuura vault folder:
`Notes (MASTER)/Secuura/platform-k-backlog-decisions-2026-08-14.md`.

**The agent went through all 87 Backlog items and pushed back on the premise, which I
think is right:** *"the backlog cannot be cleared to zero by triage, because it is not
full of stale tickets — it is full of real work."* **Exactly ONE** was genuinely
finished-and-unclosed (KS-400, closed and archived, with the superseding commit
`7cffe4341` and mechanism named).

| Why it is open | Count | Who moves it |
|---|---|---|
| Real engineering work, specified, nobody has done it | ~50 | any session |
| Blocked on a **decision** | ~20 | **you** |
| Blocked on the **Kintsugi deploy** | 12 | **one deploy** |
| Owned by Peter or Stuart | ~10 | them |
| Fixed today, in review | 3 | — |

**The highest-leverage item on the page is not a decision at all — it is the deploy**
(item 5 above). One action closes twelve.

**What the sweep actually found was not stale tickets: it was twelve tickets whose
DESCRIPTIONS were wrong**, corrected today with evidence — including four that each
said "the dependabot PR is left open so it stays fresh" when **every one of those PRs
was closed on 2026-07-14**. *"A backlog item that misdescribes its own state is worse
than a stale one: someone acts on it and wastes the afternoon."* It also declined to
close KS-341 despite its technical content being about deleted infrastructure, because
the underlying ask survives the platform it was written against — **the difference
between clearing a board and emptying one.**

### 7. Standing, unchanged
**Amplify HPSM-25 — overdue as of today.** · WED-107 (five legacy org-wide AgentMail
keys spanning every inbox) · KS-486/KS-621 org boundary-or-label · KS-624/625
by-design-or-remediate · F-1 WAF · F-5 CAPTCHA · KS-386 retention · KS-329 · KS-256 ·
verify-file 415 · KS-130/169/229 · the HP correction bundle (X1–X5 + X6 + CT §18
carriage) · four modelled revenue streams with one contract vehicle.

### ~~7b. Datasec / HPSM — the Monday deck may not open~~ ✅ **CLOSED 2026-08-15 ~12:0x — IT OPENS**
**Answer: the deck is fine and Monday is not at risk.** I opened it in PowerPoint on this
Mac; **PowerPoint's own document model reports 43 slides with no repair dialog**, and
**LibreOffice independently converted the same file to a complete 604 KB PDF**. Kam
confirmed on his own screen: *"PPT looks good. I have not reviewed the content. This can
wait for monday."*
**So two independent renderers accept the file and only Quick Look does not** — which
inverts the finding from "our deck may be broken" to "Quick Look stalls on something in
our deck". HPSM session 22 had already reproduced the stall independently at a 90-second
timeout (excluding a threshold artefact) and honestly flagged that its HP-deck control was
probably a warm cache rather than quoting a 450× ratio.
**Residual, kept but not chased:** anyone who PREVIEWS rather than opens the deck — Finder
space-bar, a Mail/Teams attachment preview, a document-management thumbnailer — may see
nothing. That matters only if this deck is sent to HP as an attachment. Parked as a
low-priority ticket with the reproduction and both controls recorded; HPSM stood down off
the bisect and moved to the register gate-count.
**Honest note on my own evidence:** my System Events dialog probe returned zero windows AND
zero sheets — a sheet count taken from an empty window list is a check that cannot fail, so
it proves nothing. What carries the weight is PowerPoint's own slide count plus Kam's eyes.

<details><summary>Original item as raised (kept for the record)</summary>

### 🔴 7b. Datasec / HPSM — **the Monday deck may not open, and this is now your 30 seconds well spent**
**Problem:** this was on your awareness list for two days as a formality. I tried to
close it and it did not close. **The system Quick Look renderer on this Mac produces
nothing for our Monday deck** — two runs, still going minutes later, empty logs — while
it renders **HP's own Playbook v3 (153 MB, 151 slides, 133 media) inside 25 seconds.**
Ours is 190 KB, 43 slides, no media at all. So it is not size and it is not complexity.
The file is structurally valid — I parsed the package independently, every CRC clean,
zero malformed XML.
**What it does not prove:** Quick Look is not PowerPoint, and python-pptx output usually
opens fine. **What changed is that the answer is no longer assumed** — one real renderer
refuses it while accepting a far heavier file.
**Options:** (a) you double-click the deck now — if PowerPoint opens it, this closes and
HPSM investigates at leisure · (b) treat it as broken and have HPSM regenerate before
Monday regardless · (c) leave it.
**Recommendation:** **(a), today.** It is thirty seconds and it is the difference
between finding this out now and finding it out in the room on Monday. HPSM already has
the finding with the controls attached and a bisect plan (the 28-slide client-safe build
is the first comparison). **Not (c)** — you present from this file in three days.

</details>

### 7c. Datasec / NexusAI — **RD-76 (Entra SSO) now blocks FIVE verifications, and that is a measured cost**
**Problem:** Entra SSO blocks agent browser-verification of the NexusAI demo. It has been
sitting as a standing inconvenience. **Today it stopped being one:** the project has five
items it can build and deploy but cannot prove — RD-85 (pill labels clip), RD-65 (dark
mode), RD-79 (session-expiry UX), RD-80 (SSE model label), and the new RD-89 health field,
which landed in an admin-gated endpoint the agent cannot curl.
**Why it matters more than it reads:** the agent is doing the right thing — refusing to
substitute *"the right code is deployed"* for *"the behaviour is verified"* — so the honest
consequence is a growing pile of shipped-but-unproven work rather than a false green.
**Options:** (a) give agent sessions a verification path to the demo (a service-principal
or a test identity that can sign in) · (b) accept it and let those five close on
code-deployed evidence with the gap stated · (c) leave them open indefinitely.
🔴 **Refinement from the agent, and it changes the ask:** the fifth item is an **admin-gated
JSON endpoint, not a page** — so the blocker is **any authenticated surface**, not "pages
behind SSO". **An acceptance criterion written around rendering pages would leave the API
case still blocked while looking closed.**
**Recommendation:** **(a)**, and it is a one-time setup rather than a per-ticket cost. If
you would rather not, **(b) with the gap written on each ticket** is honest and I can rule
that myself — **(c) is the one to avoid**, because five open tickets that are actually
finished make the board lie in the other direction.

### 🔴 9. WED — **AgentMail: deletion is NOT revocation, the vendor will not say when it will be, and WED-107's plan is now wrong**
**Problem:** the 08-13 session proved that deleting an inbox-scoped API key returns 204 and
removes it from the listing **while the key keeps authenticating** — reproduced twice, two
independent keys. **AgentMail replied 2026-08-14: *"We will consider fixing it in the
future."*** None of the four questions answered — no TTL, no propagation window, no forced
invalidation, no statement on other scoping gaps.
**Why it is yours and not mine:** it changes the security posture of the fleet's entire
comms layer. **Every key we have issued must now be treated as permanently valid.**
**What it breaks specifically:** the per-project migration's premise was *"a compromised key
can be revoked and replaced."* The isolation half works exactly as advertised; **the
revocation half does not exist.** And **WED-107's plan — delete the five legacy org-wide
keys — would make them vanish from the listing while leaving them live**, which is strictly
worse than leaving them visible.
**Options:** (a) press AgentMail for a supported forced-invalidation path or a date, naming
the impact — external comms, so yours · (b) treat keys as unrevocable and adapt: minimise
issuance, no test keys, and neutralise the legacy five some other way (rotate the account,
or migrate off the shared key entirely) · (c) accept and document the risk as it stands.
**Recommendation:** **(b) now, (a) alongside it.** (b) is entirely ours and does not wait on
a vendor who has just declined to commit. **Not (c) alone** — a documented risk that nobody
can act on is where WED-107 already sits.
**Note:** re-testing whether this is still broken **requires issuing a key that may never be
revocable**, so I have not re-tested and the 08-13 evidence stands. The cost of verifying
the defect is an instance of the defect.

### 8. Awareness only — no decision
- Secuura B-3 would have reset your real `kam@secuura.ai` SYSTEM_ADMIN account to a
  repo-published password. Fixed in #686, unshipped.
- ~~PowerPoint-opens check — 30 seconds, still unverified.~~ **Promoted to item 7b: it
  is no longer a formality.**
- **Local Docker cannot pull base images on this Mac** (KS-631) — bounds what any
  local agent session can verify. CI unaffected.
- The 06:00 wake will keep dying until Fable-5 credits renew (~2 days), per your
  ruling to leave the pin.

---

## ARCHIVE — 2026-08-04 sitting

## RULINGS (live, batch of 5 format per Kam)

**Batch 1 (ruled ~15:10):**
1. RD-64 — fix confirmed by Kam → CLOSE.
2. Release-Ready batch (RD-59/60/63/45/23) → BATCH-ACCEPT (Kam: "go with
   your call").
3. RD-41 → PARK until the commercial track moves (option c).
4. RD-55/54 security pair → SEVERITY DOWNGRADED by Kam's context: NexusAI is
   a DEMO system; commercial model = clients deploy via Azure Marketplace
   with their own keys. So git-history keys are demo-scoped. Fold into next
   routine NexusAI session as hygiene — no dedicated scrub session. (My
   "real exposure" ranking corrected — update boards-digest framing.)
5. KS-518 → accept by-design, CLOSE.

**Batch 2 (ruled ~15:15):**
6. KS-539 → (c)+(a): Wednesday distils Stuart's doc to a half-page
   (read-only), Kam rules on the summary. → Wednesday task after sitting.
7. #633 repoint → NOD. → consolidated Secuura brief.
8. Stale-tenant-refs → NAMED GO-AHEAD for a Tokenomics micro-session.
9. RD-61 → work closely with Kam; SCHEDULED follow-up TOMORROW 08-05
   (→ WED ticket + morning-briefing slot).
10. CypherKey keyed digests on demo → YES, enable. → consolidated CypherKey
    brief (one-way door acknowledged).

**Batch 3 (ruled ~15:25; Kam re-confirmed 10=a in between):**
11. Android app-lock → (c) FAIL-CLOSED with a documented recovery path
    (re-auth, not bypass). → consolidated CypherKey brief (CPKEY-163).
12. Twilio rotation → (b) DEFERRED ONE MONTH → due 2026-09-04 (goes in the
    CypherKey brief as a dated item + Wednesday follow-up tickler).
13. CPKEY-93 store publishing → (a) AFTER 161/162 land.
14. Vision dependabot ×3 → (a) NAMED GO-AHEAD for a short VSP session
    (+ LEAD_BOT_API_KEY handoff confirm).
15. RD-18 → (a) stays PARKED until commercial track (RD-13) moves.

**Batch 4 (ruled ~15:30 — Kam said "start actioning" after seeing recs;
recorded as recs-accepted, flagged as Wednesday's reading):**
16. T9-root CLAUDE.md → (a) SYNC from DevMASTER (backup kept — reversible).
17. Agent Mail upgrade → (b) DEFER until a 4th inbox is needed; WED-8 closes
    with the deferral noted.

**SITTING COMPLETE — 17/17 ruled. Execution log below.**

Execution: rulings collected through the sitting; ONE consolidated brief per
project dispatched at the end (avoids a session-launch per batch).

One sitting, ~30–40 min, clears 20+ items. Ranked: quick wins → time-pressured
→ posture calls → odds and ends. Freshness: NexusAI validated live today (Jira
read-only); Secuura validated live today (Linear read-only); CypherKey as of
its 08-02 card (no session since); Vision as of its 08-02 card.
Each item: the decision + my recommendation. You decide; I record + route.

## 1 · Quick wins (~5 min, clears 8 tickets)

- **RD-64 confirm + close** — your Settings-page 403 bug, fixed + deployed
  rev 69, now Release Ready (moved after my card was written). *Rec: hard-refresh
  the Settings page, fire one quick-question, close it.*
- **NexusAI Release-Ready batch (6): RD-59, RD-60, RD-63, RD-45, RD-23, RD-41**
  — all verified Release Ready just now; most are done work aging since June.
  *Rec: batch-accept 5 of them. The one to pause on is RD-41 (deploys Monday
  lead-sync creds toward a PROD go-live) — confirm Monday go-live is still
  wanted before that one ships.*

## 2 · Time-pressured (~10 min)

- **NexusAI security pair — RD-55 (RSA key + SP secrets in git history,
  In Progress since mid-June) + RD-54 (leaked LAW key, To Do).** 6+ weeks of
  real exposure. *Rec: authorize a dedicated NexusAI scrub session this week —
  I'll brief it under the new protocol; the decision needed today is only
  "yes, schedule it".*
- **Secuura trio (all In Review, blocking their board):**
  - **KS-518** — rule on the by-design question (their analysis is on the
    ticket).
  - **KS-539** — read Stuart's governing-rules doc + sign off (Peter/Stuart
    also pending; your sign-off unblocks the nudge chain).
  - **#633 repoint** (KS-551 rider) — mechanical once you nod.
- **Secuura stale-tenant-refs to-do** — sits outside Blockchain's write scope
  (Tokenomics launcher + client CLAUDE.md). *Rec: named go-ahead for me to
  brief a short Tokenomics session; it's a 15-minute fix rotting on the board.*
- **RD-61 dead ABTDEMO feed (demo dashboard empty since 1 June)** — needs the
  external fleet owner, not code. External comms = your class. *Rec: tell me
  who owns the ABTDEMO/HPAM fleet relationship and I'll draft the chase email
  for your send.*

## 3 · Posture calls (~10 min, CypherKey — as of 08-02 card)

- **Keyed digests on demo** (`OTP_ERD_ROOT_KEY`) — permanent once set (one-way
  door, flagging per go-slow). *Rec: yes — it closes the DB-breach enumeration
  finding on the env customers actually see.*
- **Android app-lock fail-open vs fail-closed** (CPKEY-163). *Rec: fail-closed
  — it's a security product; availability losing to integrity here is the
  brand promise.*
- **Twilio token rotation** — *Rec: yes, schedule with the next CypherKey
  session.*
- **CPKEY-93 store publishing** — start now or after 161/162 land? *Rec: after
  — publishing pipelines bite when the app is still moving.*
- (2-min machine task whenever at that keyboard: `gh auth login` for CypherKey.)

## 4 · Odds and ends (~5 min)

- **Vision: 3 dependabot branches** — *Rec: named go-ahead for a short VSP
  session to review/merge (mechanical, prod untouched); it also confirms the
  LEAD_BOT_API_KEY handoff while in there.*
- **RD-18 privacy package** — Put on Hold since June. *Rec: stays parked until
  the commercial track (RD-13 gating GA) moves; no action today, just confirm.*
- **Wednesday's own:** Agent Mail plan upgrade (browser; WED-8's last item —
  lower urgency now wednesday-agent@ exists, your call whether today) ·
  **T9-root CLAUDE.md sync** (found today: it's an older variant missing the
  fleet-comms section my own sessions load — one `cp` from DevMASTER's copy,
  needs your OK since it's workspace-level) · WED-10 ALDI SIM errand (whenever
  passing a store).

## Not flagged (deliberate)

myPKI — parked by your explicit call 2026-08-03, not resurfaced.
