# Brief — NexusAI: Kam's four marketplace remediations, plus what else blocks submission

**Commissioned by Kam, 2026-09-10 ~16:5x, answering the marketplace review's five carriers. He is
preparing containers TOMORROW.** This round CHANGES CODE. Nothing merges, deploys or submits.

## HIS WORDS, ITEM BY ITEM — and item 1 is a CHECK, not an action

> **1)** please check the code, but my recollection is that these passwords are a legacy. And the
> current operational structure of the system is to have no authentication until the first run
> process is completed at which point the entra setup configuration kicks in and takes over.
> Confirm that this is the case, and if so, these passwords can be removed and as they are not
> relevant.
> **2)** we need to capture the identifiers in the first run setup. However, once they are entered,
> hash the values out except for the last six digits.
> **3)** the description names being sent through is an acceptable problem, and as this deployment
> will be within the client's tenant, it should not cause any issues with PII.
> **4)** for the screenshots, blur out the surnames of the actual names and review whether there's
> new screenshots that should be added. Those screenshots are quite old, so I think it would be
> better if we created a new series of screenshots for the listing.
> Plus: **if there's anything else necessary ahead of the marketplace submission, tell me.**

---

## ITEM 1 — CONFIRM BEFORE YOU DELETE. The confirmation IS the deliverable.

`docs/Authorized_Users.md` holds two named individuals, work addresses and **plaintext passwords**,
marked Administrator/Active, and it ships inside the customer image.

**Kam asked you to check, not to trust him. So the answer may be "no" and that is a valid outcome.**

**Tuesday's first pass, to be RE-DERIVED and not taken on trust:**
- `grep -rl Authorized_Users` over `*.js|*.ts|*.json|*.html` returns exactly ONE hit:
  `__tests__/image-content-exposure.test.js` — the security test asserting it does not ship. **No
  production reader found.**
- The mechanism he describes exists: `isAuthEnforced` (`backend/server.js:2209`), `authGateDecision`
  (`:2349-2350`), `getFirstRunStatus`/`firstRunComplete` (`:758`).

**What you must establish, each with a control that fires:**
1. **Does ANY runtime path read that file, those usernames, or those passwords?** Search the values'
   variable names and the usernames, not just the filename — and search every language and asset
   type in the tree, not only `*.js`. State the frame you searched.
2. **Is the pre-first-run state genuinely unauthenticated, and does Entra take over after?** Read
   `authGateDecision` and `isAuthEnforced` and say what each returns in each state. **This is
   already a filed Critical (RD-01 / 13B Critical 11 / RD-361): "requireAuth fails open … serves
   every route unauthenticated before first-run setup, and reverts to that state on any storage
   error."** That corroborates his recollection — **it does not discharge your check**, and note
   the second clause: it also reverts on a storage error, which is not the same as "before
   first-run only".
3. **Only if 1 returns nothing and 2 confirms the described structure: remove the file**, quarantine
   a copy per the project's convention, and state in your wrap exactly what you established.
   **If either fails, remove NOTHING and report.**

## ITEM 2 — MASK ENTERED IDENTIFIERS, LAST SIX VISIBLE

Read `static/first-run-setup.html` and its handler before choosing a shape. **Decide from the code,
and say which you chose and why:**
- **Display masking** — the value is still stored and usable, and the UI shows `••••••••••ab12cd`.
- **Stored hashed** — the value cannot be read back, which **breaks anything that later needs it**.

**The wizard must still work.** If those identifiers are used after entry to call Entra or write
config, hashing at rest is the wrong reading of "hash the values out" and display masking is the
right one. **Establish that from the code, do not guess, and tell Kam which and why.**

## 🔴 ITEM 2b — A GAP IN HIS INSTRUCTION THAT TUESDAY IS RAISING, NOT SILENTLY FIXING

Item 2 covers the **customer's** identifiers after entry. It does **not** cover the review's actual
finding, which is different: **our OWN real identifiers are shipped as the EXAMPLE text a customer
types over** — a real tenant GUID at `static/first-run-setup.html:325` and `:980`, the Datasec dev
tenant at `:1231`, and a real service-principal application id at `:1239`.

**Masking what the customer types does nothing about those.** They are in the shipped HTML whether
or not anyone runs the wizard.

**Do this: replace them with obviously-synthetic placeholders** (the all-zeros GUID form already
used at `static/js/entra-provisioning-ui.js:254` is the in-repo precedent). **Then tell Kam plainly
that you did it and that it was not in his four items** — he can reverse it in one line, and he
should know the difference between what he asked for and what shipped.

## ITEM 3 — NO ACTION

He has accepted `backend/llm/tools.js:135` and the demo-tenant usernames at `backend/server.js:11151`
on the grounds that deployment is inside the client's tenant. **Do not change them. Do not re-raise
it.** Record that it was ruled, not overlooked.

## ITEM 4 — SCREENSHOTS

`docs/marketing/screenshots/`, 8 PNGs, which ship in the image AND are the RD-15/RD-23 listing assets.
- **Blur the surnames** on every real name. At least `rd15-03` and `rd23-08` carry one; **check all
  eight rather than the two already named** — the review verified two by eye and did not claim the
  rest were clean.
- **Assess whether the set should be re-shot.** He suspects they are too old to represent the
  product. Report what they show versus what the app looks like now, and recommend — **do not shoot
  a new series in this round without saying so first**; that is a listing asset and a bigger job.

## AND THE PART HE ASKED FOR LAST: WHAT ELSE BLOCKS SUBMISSION

**Two hard preconditions from the review are NOT in his four items and remain open. Lead your wrap
with them:**
1. 🔴 **The build LOCATION.** Building from `2_Project_Files` ships an untracked RSA private key plus
   24 extra files, because that tree's `.dockerignore` is the 26-April version (1042 B) against
   main's 4074 B. **He builds tomorrow.** Say plainly which tree he must build from.
2. 🔴 **`.dockerignore` key/env rules are root-anchored** — `*.pem`, `*.key`, `.env` match only at
   root, proven by planted canaries. The clean image is clean by luck. **One line per rule
   (`**/*.pem` etc.).** Fix it, red-proof it with a nested canary, remove the canary.

Then: **anything else you find that would embarrass a public listing.** You have the review at
`evidence-s50-marketplace-review/` — re-derive rather than inherit.

## HOLDS

- **Work in your OWN worktree.** `2_Project_Files` is Kam-ruled `investigate`/keep-as-is — **do not
  restore, sync or tidy it**, even though this brief names its `.dockerignore` as a hazard.
- **No merges, no deploys, nothing to Partner Center.** Submission is Kam's signature class.
- **Read-only on Jira** — do not file; report what should be filed.
- **Never reproduce a secret value, prefix or length** in any output, including when reporting what
  you removed.
- **Nothing is deleted without a quarantined copy.**
- Do not email Kam. Mail **`tuesday-agent@agentmail.to`**.

## REPORT

Lead with the two hard preconditions, then item by item: what you established for item 1 and whether
removal happened; which masking shape you chose for item 2 and why; item 2b stated as your own
addition; item 4's per-image findings and your re-shoot recommendation; and anything else you found.
**Every negative claim carries a control that fires. State what you did NOT examine.**
