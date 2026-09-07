# QA GATE — Datasec/NexusAI RD-362 (SEC-04 + SEC-03), `rd-362-pentest-report-exposure-s43` @ `920e067`. **TIER 1, round 1 of 2.**

**Charter first, in full:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/CLAUDE.md`
(T9 seat — DevMASTER is not mounted. Every path here is a T9 path.)

**TIER 1, ruled by Wednesday.** The change decides **what ships inside the customer image**. It is a
containment control on a document that carries an SSH-key recovery commit and a blob path, and
containment controls are the class that fails silently: the artefact looks right, the thing you meant
to remove travels in a carrier you did not check. The previous coordinator seat had this at tier 2 on
size (4 files, +155/−6); size is not the tier.

## 1. Target — the SHAs, and they are four different facts
- **Branch:** `rd-362-pentest-report-exposure-s43`
- **Head:** `920e067dc32f21cfb11e23701ee10ac210bee4d0`
- **Its parent (the red-proof baseline):** `9546da5f5585eb6e215d935c4cae2a55c339104b`
- **`origin/main` head:** `a9a8cb6e3fc62b8c08e1f3aadecb08519f1f6ddc`
- 🔴 **The branch is 248 commits AHEAD of `main`. DIFF AGAINST THE PARENT, NOT AGAINST `main`.**
  Against main this reads as tens of thousands of lines of other people's merged work. **The change
  under test is 4 files, +155 / −6:** `.dockerignore`, `__tests__/image-content-exposure.test.js`,
  `docs/PEN-TEST-REPORT-2026-04-25.md`, `scripts/verify-expected-counts.json`.
  (Standing line, from the builder and now in every NexusAI brief: *base every NexusAI gate on
  `parent..head` of the branch under test, never on `main`. main is the integration branch but is
  ~247 commits behind the work.* Tracked as RD-367; this gate does not depend on its resolution.)
- **Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files` — **read-only to
  you.** Work in your own worktree or clone.
- **NON-PROD. NO DEPLOY. NO `az` COMMAND, against any tenant, at any point.** Kam's 2026-09-07
  production lift is **Secuura only** (his 12:10: *"Only secure"*). Datasec production is out of scope
  entirely. **Do not build or run the image against any registry.**
- 🔴 **NEVER REPRODUCE A SECRET, A COMMIT HASH OR A BLOB PATH FROM THE PEN-TEST DOCUMENT IN YOUR
  REPORT.** Describe structurally — file, line, what class of thing it is, its length. The whole
  point of this change is that those strings stop travelling; a report that quotes them defeats it.

## 2. 🔴 THE CENTRAL QUESTION — this is a CONTAINMENT control, so inspect the OUTPUT, never the source
SEC-04's claim is that the pen-test report **stops shipping inside the customer image**. The mechanism
is `.dockerignore`. **A containment control that has never been exercised is a claim, not a control.**

1. **Build the ignore-set the way Docker would and enumerate what the build context actually
   contains** — do not read `.dockerignore` and infer. If you can produce the context listing without
   building or pushing an image (`docker build --no-cache` is NOT authorised; a context enumeration or
   a faithful re-implementation of Docker's ignore semantics is), do that and say which method you
   used and what it cannot prove.
2. **Docker's ignore semantics are not gitignore's.** Precedence is last-match-wins, `!` re-includes,
   and a directory exclusion cannot be undone by a later file re-include beneath it. **Check the
   ordering in the file, not just the presence of the patterns.**
3. **The builder found the ORIGINAL defect was a missed carrier:** the `.docx` and `.pdf` were
   excluded and **the `.md` original was not** — and `Dockerfile:37` and `:79` both `COPY docs/`, so it
   shipped twice over. **Ask the same question of the new state: what OTHER carrier could hold this
   content?** Other copies of the report under different names or paths, an archive, a build artefact,
   a `docs/` symlink, something `COPY`'d by a second stage, or the same text quoted inside another
   tracked file. **Enumerate the carriers; an omitted extension or path is a silent scope reduction.**

## 3. 🔴 THE TRAP THE BUILDER ALREADY HIT — and the guard it built
**The obvious fix is a blanket `*.md` exclusion and it 500s two live routes.** `PRIVACY.md` and
`TERMS_OF_SERVICE.md` are **read at runtime** and served by `backend/server.js:1367` and `:1374`.
The builder found this before excluding anything and pinned the reason in a **control cell** asserting
both that they are NOT excluded and that the server really reads them.

**Your job: verify that cell actually discriminates.** Would it fail if someone added a blanket
`*.md`? Prove it by tampering a copy — and assert the tamper landed before asserting the failure.
**A control that cannot fail is the thing this whole engagement keeps finding.**

## 4. SEC-03 — the redaction, and the claim it deliberately does NOT make
The builder redacted two commit hashes plus blob paths at `:183`, the reproduction line at `:190`, and
**a third instance at `:553` that its own grep missed and the TEST found** (its pattern did not allow a
leading backtick).

**Carry this framing into your verdict — it is the builder's own and Wednesday has ratified it:**
> **The redaction removes the RECIPE. It does not remove the EXPOSURE.** The blobs stay reachable in
> git history until the rotate-and-scrub lands (**RD-55**, dev-tenant admin, category 2).
> *Redacting the map is not removing the territory.*

1. **Verify the redaction is complete** — sweep the document for every remaining instance of the
   *class* (hash-shaped strings, blob paths, reproduction commands), with your own pattern, **and say
   what your pattern would miss**. The `:553` miss happened because a pattern did not allow one
   leading character.
2. **Verify the "does not read as closure" cell exists and actually asserts it.** A redaction that
   reads like a fix is worse than the recipe, because it stops anyone doing RD-55.
3. **Do NOT treat SEC-03 as closed** and do not let the ticket's language imply it. Report what
   shipped and what did not, separately.
4. **SEC-02 is explicitly NOT in this change** — the live Entra client secret republished as the body
   of the `pt002` gitleaks rule, deliberately deferred because changing that rule interacts with
   `scripts/gitleaks-canary.sh`, which asserts **by RuleID** that every custom rule still detects the
   syntax it claims. **Do not test it, do not recommend fixing it here.** Confirm only that it is
   untouched and still tracked.

## 5. The counts file
`scripts/verify-expected-counts.json` moves by +6/−6 lines. **Confirm the test-count delta matches the
cells actually added** — a counts bump larger than the cells added is how a skipped suite hides.
**Note for context, do not chase it:** the builder established that NexusAI's `gitleaks.yml` pins
`actions/checkout@v7`, which **exists** (v7.0.1, 2026-07-20) and has run across 104 pushes — an
earlier fleet claim that it was a nonexistent major has been **retracted**. Do not act on that claim
if you meet it anywhere.

## 6. Evidence rules — mandatory
1. **Every cell: say what it MOCKS and therefore what it cannot prove.** A cell asserting on
   `.dockerignore` text proves the file's contents, never the build context's.
2. **Carry BOTH controls.** A positive control that your instrument fires, **and a negative control —
   an impossible pattern returning a zero you can vouch for.** (That second one comes from the
   builder's own RD-368 search and it is now standing practice; a zero without it is not evidence.)
3. **Red-proof per clause**, and prove the green baseline too.
4. **Capture `rc` on its own line** for any bounded command; a `0` from a killed command is not a zero.
5. **Never delete.** Cleanup means quarantine.
6. **Findings-only. You never fix.**

## 7. Verdict
**GO** · **GO-with-findings** (mark Majors vs advisory) · **NO GO**. Severity is yours; priority is
Wednesday's. **Round 1 of 2** under Kam's cap — a second NO GO ships what is closed and tickets the
residue, so if you go NO GO, name which instances could ship and what the residue's ticket should say.

Report by mail to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Datasec RD-362 (SEC-04 + SEC-03) @ 920e067, tier 1`.

PROVENANCE:
- head `920e067dc32f21cfb11e23701ee10ac210bee4d0`, parent `9546da5f…`, 4 files +155/−6 | `git ls-remote` and `git show --stat`, run by Wednesday in the same action as writing this | read 2026-09-07
- 248 commits ahead of `origin/main` `a9a8cb6e…` | `git rev-list --count` | read 2026-09-07
- the `.md`-carrier defect, `Dockerfile:37`/`:79` both `COPY docs/`, the `PRIVACY.md`/`TERMS_OF_SERVICE.md` runtime reads at `server.js:1367`/`:1374`, the `:553` grep miss, the SEC-02 deferral and its `gitleaks-canary.sh` RuleID interaction | the builder's mail `[Datasec/NexusAI -> Wednesday] RD-362 in-repo half SHIPPED @ 920e067`, 2026-09-07T07:15:14Z, re-read from the inbox in this action | read 2026-09-07
- "the redaction removes the recipe, not the exposure; blobs reachable until RD-55" | same mail; ratified by Wednesday and required in the verdict | read 2026-09-07
- `checkout@v7` exists (v7.0.1, 2026-07-20) and the "nonexistent major" claim is retracted | GitHub API read by Wednesday + 104 pushes on the pin, from the builder's repo-history check | read 2026-09-07
- production lift is Secuura-only | Kam, panel 2026-09-07 12:07 + 12:10 | read 2026-09-07
- **UNMEASURED, stated as such:** whether any carrier other than `docs/` holds the report's content; whether the runtime-read control cell would fail on a blanket `*.md`. Those are this gate's questions.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 18:00
