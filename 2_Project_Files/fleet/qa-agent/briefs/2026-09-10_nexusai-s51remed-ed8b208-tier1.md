# QA GATE — TIER 1 — Datasec/NexusAI, the Marketplace remediation branch

**Head under test:** `s51-marketplace-remediation` @ `ed8b208dccccb74d449227e3b968eab1b30bd0f5`, based on `cd2b543` (origin `main`).
**🔴 LOCAL ONLY — NOT PUSHED.** The branch lives in the worktree `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed`.
**Diff:** 6 commits, 16 files, +442/−33 — `.dockerignore`; `static/js/identifier-mask.js` (new), `static/first-run-setup.html`, `static/js/first-run-setup.js`; `backend/server.js` (one line); three test files; `scripts/verify-expected-counts.json`; 7 of the 8 PNGs in `docs/marketing/screenshots/`.
**Round:** 1 of 2 under the cap for this class. S52's verification was the builder's own check, not a gate.

## WHY TIER 1

`.dockerignore` is the control that decides whether key and env files enter the **customer image**. The masking change sits on the first-run page that handles **Entra identifiers**. The screenshots are **public listing assets** that carried real surnames. **Kam builds the Azure Marketplace containers from this head TOMORROW (2026-09-11).** Security surface plus a human handover.

## WHAT KAM COMMISSIONED — his words (2026-09-10, 16:5x)

> **2)** we need to capture the identifiers in the first run setup. However, once they are entered, hash the values out except for the last six digits.
> **3)** the description names being sent through is an acceptable problem, and as this deployment will be within the client's tenant, it should not cause any issues with PII.
> **4)** for the screenshots, blur out the surnames of the actual names and review whether there's new screenshots that should be added.

Item 1 (the `docs/Authorized_Users.md` check) is **not this gate's subject** — it is reported and sits with Kam as a card.

## THE BUILDERS' CLAIMS — verify each, relay none (S51 built, S52 verified: `REPORT-S52.md` §2)

1. **`26ca78a` — `.dockerignore` key/env rules match at any depth.** S52: from a `git archive` extract with real Docker, the old rules let **10/10** nested canaries (`.pem .key .env .env.production .pfx .p12`, `3_Access_Keys/`, `4_Credentials/`, `ssl/`) into the build context; the new rules block **0/10 in the context and 0/10 in the product image**; root canaries were blocked both times; nested positive controls were present.
2. **`ec7a3ad` — masking, last six visible.** S52, real browser: 9/9 inputs attached; an unfocused field shows bullets plus the last six; page code and server both hold the full value; Save & Validate, Validate and Enforce worked server-side. **Runtime-added data-source boxes were NOT driven.**
3. **`e70d949` — NOT one of Kam's four:** all 9 wizard placeholders are the all-zeros GUID, replacing real publisher identifiers.
4. **`58184aa` + `ed8b208` — surnames blurred** on 7 images, illegible at 4x; a 12 px patch on `rd15-04`'s rotated axis label.
5. **`96b17e3` — suite:** `npm run verify` VERDICT PASS, 2300/2300 across 119 suites.
6. **Item 3 untouched:** `backend/llm/tools.js` 0 changed lines; the `backend/server.js` change is one line near `:13975`.

## 🔴 WHAT TO ATTACK FIRST — nobody has checked the other direction

1. **OVER-EXCLUSION.** S52 proved the new rules keep secrets OUT. **Nobody proved they keep nothing the product NEEDS.** Build `--target production` at **both** `cd2b543` and `ed8b208`, enumerate each image's files, and diff: **every file that disappears must be one the rules were meant to exclude.** Then run the `ed8b208` image and prove `/api/health`, `/login` and the first-run page still load. A fix that strips a runtime file ships a broken container tomorrow.
2. **MASKING THAT IS ONLY COSMETIC.** Is a full identifier value recoverable anywhere a user or an observer reaches **without typing it** — the rendered DOM, page source, a network response, browser storage, a server log, an error message? Are **all** identifier fields covered, including the runtime-added data-source boxes S52 did not drive?
3. **BLURS THAT DID NOT REMOVE THE NAME.** Any legible real name or surname at any zoom? Any image **metadata or embedded thumbnail** still carrying the original? Any other personal text left (addresses, tenant names)?

## HOW TO DRIVE IT

- **Never write into the NexusAI checkout or its `.git`** — no `fetch`, no `worktree add`, no `checkout` there. Clone into your OWN `mktemp -d`: `git clone --no-hardlinks '/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed' "$T/repo"`, then check out `ed8b208dccccb74d449227e3b968eab1b30bd0f5` (and `cd2b543` for the comparison) **in your clone**.
- `npm ci && npm run verify` — **read the VERDICT line, not the exit code.**
- **Docker 29.7.2 is up on this machine** (measured 19:3x). Remove only images YOU built, and say so.
- **Browser:** a local server of THIS commit on a fresh data directory. **If you drive Chrome through an extension, fingerprint it against this Mac first** (`navigator.hardwareConcurrency` and screen size against `sysctl -n hw.ncpu`) — the extension can drive a different Mac's Chrome and report it as local. Prefer a headless driver that is provably on this machine.
- **`2_Project_Files/` in the NexusAI project is a Kam-ruled keep-as-is stale snapshot.** Do not build from it, touch it or "fix" it.

## KNOWN — do NOT report as new

- **First-run completion leaves the dashboard open without Entra** until Enforce runs (REPORT-S52 §1.2). Pre-existing, already reported to Kam, likely in the RD-361 / SEC-01 area.
- **The Enforce step shows an error after it succeeds**, and `checkEntraStatus` throws on opening User Access (§1.4.1–2). Pre-existing at `cd2b543`, to be ticketed.
- **`docs/Authorized_Users.md` and all 8 PNGs still ship** (`COPY docs/`). Measured by S52; Kam holds the removal and re-shoot cards. **Do not remove or re-shoot anything.**
- **RD-369 round 3** (`rd-369-round3-s49` @ `7cd0907`, on origin, unmerged) pins `docs/Authorized_Users.md` and the two first-run files as carriers in cell G1. **You MAY run that G1 cell against this head to MEASURE the merge hazard** (S52 reasoned it from the test text and did not run it). Report it; do not resolve it.
- **Item 3 is Kam-ACCEPTED** — do not re-raise the names in `tools.js` or the demo usernames.

## WHAT WOULD MAKE THIS A NO GO FOR TOMORROW'S BUILD

- Any nested secret-class file still enters the build context or the image.
- The `ed8b208` production image lacks a file the running product needs, and health, login or the first-run page fails where `cd2b543` works.
- A full identifier value is recoverable on a path a user reaches without typing it.
- A legible real name remains in any listing image or its metadata.
- `npm run verify` does not report PASS.

## CONTROLS THIS GATE OWES ITSELF

**Every zero gets a control that would have produced a non-zero, run in the same action.** If an instrument cannot reach the case it names, mark the cell **NOT TESTED** with the blocker, never a pass. Every finding that recommends an action carries its evidence class: **MEASURED AT RUNTIME · PROBED · READ ONLY.** **Never `rm`** — build each attempt in its own `mktemp -d`.

## YOU ARE FINDINGS-ONLY

**Never fix.** Report. Grade Blocker / Major / Minor. Qualify your own greens.

## 🔴 MAIL YOUR VERDICT

**Send it to `tuesday-agent@agentmail.to`**, subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — Marketplace remediation @ ed8b208 (tier 1)`. **Lead with GO or NO GO for tomorrow's build.** **NOT `wednesday-agent@`** — Datasec's coordinator is Tuesday. **You have no inbox, so a verdict you do not mail is lost.**

PROVENANCE:
head ed8b208dccccb74d449227e3b968eab1b30bd0f5 at local refs/heads/s51-marketplace-remediation, absent from origin | git rev-parse and git ls-remote in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed | read 2026-09-10
6 commits, 16 files, +442/-33 from cd2b543; origin main is cd2b543 | git log, git diff --stat and git ls-remote in that worktree | read 2026-09-10
builders' claims 1-6 and the KNOWN items | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/evidence-s52-marketplace-verification/REPORT-S52.md sections 1.2, 1.4, 2, 4 | read 2026-09-10
Kam's items 2-4 verbatim | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-10_nexusai-marketplace-remediation.md | read 2026-09-10
rd-369-round3-s49 at 7cd0907 on origin | git ls-remote origin in the worktree | read 2026-09-10
Docker server 29.7.2 responding | docker info on Kamils-Mac-mini | read 2026-09-10

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-10 19:34
