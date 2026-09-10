# Brief — NexusAI: full review ahead of preparing the containers for Azure Marketplace

**Commissioned by Kam, 2026-09-10, on the Tuesday panel: *"spin up a Nexus agent to review the
Nexus project in full ahead of what I would like to do tomorrow, which is prepare all the
containers for Nexus to be submitted to the usual marketplace."***

**This is a REVIEW. You find and report; you do not fix, merge, deploy or submit.** The deadline
is that Kam prepares containers TOMORROW, so the deliverable is a readiness verdict he can act
on in the morning, not a backlog.

## WHY THE ORDER OF THIS BRIEF IS WHAT IT IS

A marketplace submission is **effectively irreversible**: what goes into a published image can be
pulled by anyone and cannot be recalled. So this review leads with **what is inside the images**,
not with code quality. Everything else is secondary to that.

---

## 🔴 ITEM 1 — WHAT SHIPS INSIDE THE CONTAINER IMAGES

**Start from a known instance, then widen. Re-derive it; do not trust this brief.**

This morning's tier-1 QA gate on RD-369 established, by `docker export` of the built image
rather than by reading source, that **`DEPLOYMENT_GUIDE.md` ships inside the customer image and
carries a real Azure subscription GUID and two real email addresses.** Tuesday independently
confirmed the file's content and that it contains **zero** standalone `ID` tokens.

**That matters tomorrow in a way it did not matter yesterday.** It is a pre-existing exposure,
not a regression — and it is in the artefact about to be published.

**The detector that should have caught it cannot see it.** `LABEL_ID = /\b(id|ids)\b/i` requires a
standalone `ID` token. The shipped source is full of camelCase identifiers that can never match —
Tuesday measured `tenantId` 142, `clientId` 135, `subscriptionId` 71 in `*.js`/`*.ts` under
`wt-s49` (**a Tuesday measurement in a stated frame — re-derive it in yours**).

**Your job is NOT to fix the detector.** RD-369 is at a cap: Kam authorised one round 3 and there
is no round 4 without him. **Your job is to enumerate what is actually in the images.**

1. **Build the image and enumerate its contents** — `docker export`/`docker save`, not a reading
   of the `Dockerfile`. Ask of the file list: *what is in here that a customer should never get?*
2. **Sweep the exported filesystem for carriers**, and pick the patterns from what identifiers
   actually look like in THIS codebase, not from a generic list: GUID-shaped strings, email
   addresses, tenant/subscription/client identifiers in any casing, internal hostnames, staging
   URLs, personal names, `.env`-class files, `.git` directories, test fixtures, source maps.
3. **Every negative claim gets a positive control** — plant or locate a known instance and prove
   the search finds it. A clean sweep whose instrument cannot fire is worse than no sweep.
4. **🔴 NEVER REPRODUCE A SECRET VALUE, prefix or length** in your report. Location, variable name
   and credential class only. That hold applies to your report exactly as it applies to the register.
5. Report each carrier as: what it is · which layer/path puts it there · whether it is needed at
   runtime · what removing it would cost.

## ITEM 2 — THE SUBMISSION PACKAGE ITSELF

`AZURE_MARKETPLACE_SUBMISSION_PACKAGE.md`, the `azure-marketplace/` directory, `Dockerfile`,
`docker-compose.yml`, `deployment/`, `bicep/`.

- Does the package describe what the repo actually builds today? Where it does not, say so per item.
- Are the marketplace's technical requirements for a container offer met — image tagging, required
  labels, licensing metadata, the ARM/bicep template, and whatever the package itself claims is
  required? **Read Microsoft's current requirements rather than trusting the package's summary of
  them**, and cite what you read.
- Is the build reproducible from a clean checkout? Try it.

## ITEM 3 — THE REST OF THE PROJECT, BOUNDED

Kam said "in full", and the deadline bounds it. Cover, in this order, stopping when a category
yields nothing: open RD tickets that would block or embarrass a submission · third-party licences
shipped in the image · anything the repo documents as unfinished · anything that authenticates.

**Say plainly what you did NOT examine.** An honest gap beats a silent one, and a review that
claims completeness it does not have is worse than a narrow one.

---

## RULED BY KAM, NOT YET IN AN ARTEFACT — read before you touch anything

**`nexusai-main-tree-is-a-stale-snapshot`, ruled `investigate` at 2026-09-10 11:48:**
*"Keep the tree as-is until the mechanism is explained, then restore."*

`2_Project_Files` sits at `cd2b543` while `wt-s49` is at `7cd0907`, with mtimes older than the
commits above them and no explanation. **You do not restore it, sync it, or tidy it.** If your
review happens to explain the mechanism, that is a finding Kam wants — report it, change nothing.

## HOLDS

- **Work in your OWN git worktree.** Do not work in `2_Project_Files` and do not touch another
  seat's worktree.
- **No merges, no deploys, no pushes to main, and nothing to Partner Center.** Submission is Kam's
  and is a signature-class action.
- **Read-only on Jira.** A separate Jira round is running today on the Datasec product register;
  do not create or transition tickets, or you will collide with it. Report what should be filed.
- **Read-only on `Source_Code/`-style material you are only citing.**
- Do not email Kam.

## WHAT TO REPORT

Mail **`tuesday-agent@agentmail.to`**. Lead with a **GO / GO-WITH-CONDITIONS / NOT READY** verdict
for tomorrow's container preparation, then:

- the image-contents enumeration and every carrier found, with its controls;
- what is required before submission versus what merely should be improved — Kam needs that line
  drawn sharply, because tomorrow he acts on it;
- what you did not examine;
- every instrument that failed you, including your own.

**RAISE, do not fix.** If something is a one-line change and obviously right, say so and leave it.
