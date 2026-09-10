---
date: 2026-09-10
type: architecture
source: Kam, panel 2026-09-10T21:50:42 — "Map out the process to deploy Peter's suggestion for merging and testing and deployment."
status: draft — for Kam's review; NOT yet in force beyond the parts already ruled
---

# Merge · Test · Deploy — the end-to-end process, built on Peter's protocol

**What Kam asked for:** *"Map out the process to deploy Peter's suggestion for merging and testing
and deployment."*

**The honest starting point:** Peter's 624-line document covers **one link of three**. It describes
what a REVIEWER does when a PR arrives. It says almost nothing about what must be true *before* it
arrives, and nothing at all about what happens *after* approval. **Those two gaps are where our
failures actually live** — tonight alone: five PRs sitting unreviewable because nothing had gated
them, and a deploy grant with no defined path from "merged" to "running".

So this map has **five stages**, and Peter's protocol is stage 3.

---

## Stage 0 — COMMISSION (Wednesday)

| | |
|---|---|
| **Owner** | Wednesday |
| **Entry** | A ticket, a Kam ruling, or a finding |
| **Exit** | A brief that passes the send gates, delivered and content-verified at the agent's inbox |

**Gates already enforced in tooling** (`send_brief.sh` / `brief_and_launch.sh`): a PROVENANCE block
with absolute, tree-labelled paths · a fresh SELF-CHECK attestation · a `RULED BY KAM, NOT YET IN AN
ARTEFACT` section · delivery verified at the destination *before* the launch step can run.

⚠ **The stage-0 rule tonight taught us:** the brief must state **how** a constraint is to be
satisfied, not only that it must be. A brief demanding a live-stack red proof while the repo forbids
touching secrets files is **an instruction that requires a rule to be broken** — that is a defect in
the brief, not in the agent that hits it.

---

## Stage 1 — BUILD (project agent)

| | |
|---|---|
| **Owner** | The project's own agent. Wednesday never edits project files. |
| **Exit** | A PR that satisfies **Peter's author-side contract**, below |

**The author-side contract — this is the half Peter's document assumes rather than states:**

1. **Risk map first (§1b)**, ahead of the summary. Any HIGH area named in the PR's first line.
2. **Unit tests that BITE (§10)** — revert the change, confirm RED, restore, confirm GREEN, **and
   say you did it.** ⚠ **Quote CELLS RUN beside pass/fail.** A tamper that breaks compilation
   reddens having executed zero tests; *red for the wrong reason is indistinguishable from red for
   the right one unless you read the count.* (Measured 2026-09-10 on #936.)
3. **Test Evidence block** — touched / ran / **NOT run** / migrations+config, from LOCAL runs.
4. **Config drift (§3b)** — every new var in `.env.example`, `env.example`, compose,
   `docs/ENVIRONMENT-VARIABLES.md`, bicep. **Name only, never a value.**
5. **Both HTML docs** moved in the same commit if a test changed.
6. **PR body** carries the Linear URL and both pre-merge ack checkboxes.

**Secrets convention (§7/§8, adopted 2026-09-10):** the agent **generates** the file, **names the
keys**, and **stops**. A human sets the values. *"Tell me the KEY names; I set the values."*

---

## Stage 2 — OUR GATE (a QA agent that did NOT build it)

**This stage does not exist in Peter's document and it must exist before his does.** Tonight five of
seven PRs reached his queue with **no gate verdict of any kind** — so his protocol, however good,
had nothing to verify.

| | |
|---|---|
| **Owner** | A QA agent that did not write the code. **The builder is never its own gate.** |
| **Tier** | Per `qa-gate-tiers-and-the-two-nogo-cap`: full for security surfaces, data destruction, deploys, human handovers; through-code for tests/docs/config; none for hygiene |
| **Cap** | Two NO GO rounds on one class, then it escalates rather than looping |
| **Exit** | A verdict **in an artefact a reader lands on** — the ticket or the PR, never only a mail |

⚠ **A verdict that lives only in a mail or a pane has not been delivered.** On 2026-09-09 a tier-1
NO GO held a PR all day while existing nowhere a reader would find it.

---

## Stage 3 — PETER'S REVIEW (his protocol, unchanged)

His document governs here and we do not amend it. What we owe: a PR that arrives in a state his
protocol can actually verify, and **honesty about what we did not run.**

**Authority (§3.2):** platform-k base code → **Kamil** · platform-s → **Stuart** · `systemTest/` on
both platforms → **Peter**.

**What blocks (§2c):** a HIGH-risk area with no biting unit test blocks on either platform. On a
platform-k PR, any NEW unbaselined, untracked failure blocks.

**Series rule (§6):** one suite at a time, machine-wide; nothing builds while a suite runs; rate
limiting → stop 15 minutes. *Measured 2026-08-20: three suites concurrently produced 300 engine
errors and a report that still read PASSED.*

---

## Stage 3a — PETER'S TRIAGE: how his queue is ordered, and the three queues it hands US (adopted 2026-09-11)

**Source:** `0_Brain/reference/2026-09-11_peter-pr-triage/pr-triage-2026-09-10.md` — Peter's own
triage of every open PR, measured from the GitHub API at 2026-09-10 16:09 UTC. **Kam, 2026-09-11:
*"new document from Peter for triage. please incorporate this into our workflow."***

**Read it the way [[2026-09-10_a-reviewers-protocol-is-our-acceptance-criteria]] says to read any
reviewer's process: from HIS chair.** "Your actions" in it are PETER's; "Kamil's court" is OURS.

### His priority tiers — we use them to order OUR work too

| Tier | A PR is in it when its diff touches | Why it outranks the next |
|---|---|---|
| **A — published contract** | `Blockchain/Dev/docs/openapi/secuura-api.yaml` | Schemathesis reads it, Akto imports it, it ships to `/api/docs` |
| **B — runtime** | `services/`, `packages/`, `frontend/` outside `__tests__` | reaches users |
| **C — gate & evidence integrity** | `.github/`, `scripts/`, docker / compose | decides whether every future PR's evidence is believable |
| **D — test-only / docs** | everything else | no live surface |

Oldest first within a tier. Overrides: a **stale approval** rises to the top of its tier; a PR others
**hang off** rises above them; a **blocked** PR sinks below its blocker.

### His court rules — whose move it is

- **HIS last word, no reply and no push since → OUR court.** (His rule, from his chair: *"Your last word with no reply and no push since → their court."*) *A `develop` merge with no comment is not a reply.*
- `CHANGES_REQUESTED` → **our** court until addressed (and since 2026-09-09 23:23Z GitHub blocks the merge).
- **We push past his review → back to HIM; any approval is void.**
- Never reviewed by him → **his** action.

### The three queues his triage hands us

1. **Approved at head, unmerged → WE MERGE.** The author merges on approval. On 09-10 this was 15
   approved and 1 merged. **This is the cheapest throughput in the whole pipeline and it sat idle.**
2. **"Kamil's court" — his last word, no reply → WE ANSWER**, in code or on the ticket, in tier order.
3. **His own PRs waiting on Kamil → WE REVIEW** (Kamil is platform-k authority), s171's #896 shape;
   **the approval is Kam's click** until the agent GitHub identity exists.

### ⚠ Two traps his triage itself fell into — check these before acting on ANY row of it

- **A withdrawn approval is invisible to review STATE.** #813: `APPROVED` at 14:52Z, then a `COMMENTED`
  review at 14:56Z withdrawing it in words. GitHub's last-state and Peter's own tool both still read
  "approved". **Before any merge, read every review AND comment dated after the approval.**
- **A stacked PR can be reported merged when it is not.** His triage says #900 merged; at 21:0x UTC it
  was OPEN, based on #899's branch. **Re-measure state before relying on a triage row.**

**Both corrections go to Peter via Kam, framed as gifts, never agent-to-client.**

---

## Stage 4 — MERGE

| | |
|---|---|
| **Who** | **The AUTHOR merges, not the reviewer** (§3.7) |
| **Condition** | A passing gate **AND** an approval. Both. |

### 🔴 The state of this stage right now, measured 2026-09-10

- `required_approving_review_count` = **0**
- `required_status_checks` = **absent** from the `require-pr-gates` ruleset
- `blocked` = **0** across the open PRs; the develop freeze lifted this morning
- ⚠ **Superseded in part (Peter's triage, 2026-09-10 16:09 UTC):** the ruleset was edited 2026-09-09 23:23Z — a `CHANGES_REQUESTED` review now BLOCKS (#881, #887 read `BLOCKED`). Required approvals is still 0, so a zero-approval PR still reads `CLEAN`.

**There is no technical brake. The condition above is held by convention alone.** Kam ruled
`raise-to-1` at 10:32 and it is **unapplied** (the ruleset's own `updated_at` is 09:23, before the
ruling). **Closing this is the single highest-value change to this whole pipeline** — every other
stage is discipline; this one would be a mechanism.

⚠ **`mergeable_state` is INVERTED on this repo. Never triage by it.** `#925` reads `clean` only
because its runs all `startup_failure`d; **`clean` can mean nothing ever checked it.**

⚠ **No agent can approve anything** — `kksecura` authors the PRs and `kksecura` is our PAT, so
GitHub returns 422 *"cannot approve your own pull request"*. Kam ruled the agent GitHub identity on
**2026-08-26**; still unexecuted. **Until it is, every approval is Kam's own click.**

---

## Stage 5 — DEPLOY — **the link nobody has written down**

| | |
|---|---|
| **Order** | **Kintsugi first, then demo behind gates** (Kam, 2026-09-10 13:22) |
| **Scope** | *"Everything possible" = what has MERGED.* It does **not** authorise merging unapproved PRs, bypassing a gate, or `--no-verify` |
| **Grant** | Kam, email 2026-09-10 15:24 — **EXPIRES END OF SUNDAY 2026-09-13 AEST** |
| **Parity** | Kam, 17:10 — anything done this week lands on **both** boxes, or it is a REPORT, never a silent asymmetry |

**The steps, from the 2026-09-10 whole-estate rebuild that actually worked:**

1. **Phase 0 — re-tag every image `:pre-<date>` before building.** A tag is a pointer, not a copy;
   this turns rollback from ~1.5h of rebuilding into ~2 minutes. **Neither box had any rollback at
   all before this.**
2. **Never `docker prune`** — image or builder — at any point. The build cache is the only rollback
   material that exists.
3. **Build everything with nothing swapped.** A failure here is free.
4. **Migrations in the middle**, applied and verified **by name** — an explicit `Applying 0NN_….sql`,
   never `applied=N failed=0`. ⚠ **`run-migrations.sh` exits 0 when migrations fail**, so compose's
   own gate does not catch it.
5. **Swap one service at a time.**
6. **Verify behaviourally, against a MOVING control.** ⚠ **Check image CONTENTS before the step that
   consumes them** — on 2026-09-10 demo's image was three days stale and missing migration 048;
   Phase 3 would have printed `applied=N failed=0` having never seen it.
7. ⚠ **A single-FILE bind mount binds the INODE.** Replacing a config on the host does not reach the
   container and every signal still says success. **Compare host and container inode**, then
   `up -d --force-recreate --no-deps <service>`.

---

## The five gaps, in the order I would close them

| # | Gap | Cost | Why it is ranked here |
|---|---|---|---|
| 1 | **`raise-to-1` unapplied** — no technical brake on merging | one click, Kam's | The only place a *mechanism* replaces discipline |
| 2 | **Agent GitHub identity** (ruled 2026-08-26) | one invite, Kam's | Until then every approval is Kam's own click, and it is the queue's real bottleneck |
| 3 | **Stage 2 is not enforced anywhere** — five of seven PRs reached Peter ungated | process + tooling | Peter's protocol cannot verify what nothing has gated |
| 4 | **Batching** — his protocol is ~a day per PR; Kam's 09-03 steer is three big things over thirty | a decision, his | The two are incompatible unless PRs reach him in review streams. **Asked, not assumed** |
| 5 | **Stage 5 exists only as tribal knowledge** — this file is its first write-up | done, here | It worked on 09-10 because one seat measured carefully, not because anything is written |

## What is NOT in this map, deliberately

- **Peter's §2c/§2d authorisations** are scoped to **his** verification run. Adopting his protocol
  does not transfer them to us.
- **Production.** It does not exist — measured 2026-09-10.
- Anything requiring us to edit `systemTest/`, which is **Peter's** authority.
