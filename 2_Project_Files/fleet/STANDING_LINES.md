# Standing lines for every builder brief

**What this is.** The HOLDS and definitions that belong in *every* brief Wednesday sends to
a project agent, in one place, so they stop being reconstructed from memory each time.

**What this is NOT, stated plainly: a mechanism.** Nothing forces a brief to carry these.
Pasting them is still a habit, and habits skip
([[../../0_Brain/learnings/2026-08-10_a-ritual-nothing-triggers-is-not-a-ritual]]). The
in-path version — `send_brief.sh --kind brief` refusing a body with no `HOLDS` section — is
the promotion candidate **at the next instance of a brief going out without them**. It is
deliberately not built today: the gate in this same file was changed hours ago, and a rule
is at its most dangerous in the hour it is adopted
([[../../0_Brain/learnings/2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]]).

---

## READY FOR QA — what it means as an ARTEFACT

**Why this exists.** On 2026-09-09 a seat did real work on KS-926, pushed `ed954f09e` to
origin with 14/14 preflight, and reported it. **There was no pull request. There never had
been.** Nothing was wrong with the work and nothing was wrong with the report — **no brief
in this fleet has ever said what READY means as a thing that exists**, so "READY" meant
"I have finished", and finishing and being reviewable are different states. A healthy
branch is the quietest form of work-done-and-the-board-not-saying-so, because there is no
stale record to notice — there is no record. That family is at w=13.

**READY FOR QA means all five of these EXIST and are named by identifier in the mail:**

1. **A PULL REQUEST — not a branch.** A branch is where work lives; a PR is what a reviewer
   can reach. `ls-remote` proves a branch exists and proves nothing about reviewability.
   **If the sentence names a SHA and no PR number, it is not ready.**
2. **Its HEAD SHA, read from origin in the same action as writing the sentence** — never
   carried forward from an earlier message.
3. **The TICKET, with a comment on it naming the PR.** The ticket is where the next reader
   lands; a PR nobody linked is findable only by whoever already knew.
4. **The TEST EVIDENCE block the repo requires, in the PR body, written by whoever RAN the
   tests.** Not by the coordinator. A body composed by someone who did not run them is the
   shape this fleet keeps catching.
5. **What was NOT done or NOT covered**, in the same mail. "Unit-proven; the click path
   could not be exercised" is a complete report; a bare green tick is not.

**THE EXCEPTION, written now rather than waited for.** Work with no reviewable surface of
its own: a fix inside a PR that already exists, or work explicitly commissioned to stop at
a branch for a later stacked PR. **Those are ready without a PR of their own — and they say
so, and they name the PR that will carry them.** If you cannot name that PR, the exception
does not apply.

---

## INSTRUMENTS — bound the OUTPUT, never the STREAM you are diagnosing from

**Why this is here.** On 2026-09-09 one seat lost three commands to this family in a single
session and named it better than the coordinator had. **Every one made a null result look like
a real one**, and each was the pipe or a missing binary rather than the subject:

1. `timeout 90 git fetch | tail` — **macOS has no `timeout`.** git never ran; the pipeline
   still exited 0. **First command of the session.**
2. A push through `| tail -50` — hid legs 1–3, so the real cause (`DEPS MISSING` on a worktree
   that had never had `npm ci`) looked unattributable.
3. `pgrep -qf 'npm test -w services/security'` — **matched the seat's own wrapper's command
   line**, so a test that had never started read as running.

**The rule:** redirect to a file and read the file — `cmd > out 2>&1; rc=$?` — then **the exit
code and the head both survive**. Bound the *output you display*, never the *stream you are
diagnosing from*.

**And the three specifics, because each is a repeat offender:**
- **`timeout` does not exist on macOS.** Neither does `realpath` on older ones. Assume the
  oldest shell on the drive's targets: bash 3.2, no `declare -A`.
- **A `pgrep -f` pattern matches YOUR OWN command line**, including the wrapper that ran it.
  Exclude your own pid, or match on something only the target emits.
- **In zsh there is no `PIPESTATUS`** — it is `$pipestatus[1]`, and the Bash tool here is zsh.
  `${PIPESTATUS[0]}` expands to empty, so the guard around a refusable step reads nothing and
  looks fine.

## HOLDS that go in every brief

- **Signature classes pause for Kam, always:** production · money · external communication
  to any human · anything irreversible.
- **Client-facing communication is TICKET COMMENTS only.** The extranet is INPUT ONLY —
  read it, never post there. Anything needing a push comes to Wednesday as an escalation
  candidate for Kam's WhatsApp; **nobody else messages Peter or Stuart.**
- **Handovers to Peter/Stuart are TEST BLOCKS, never a list of PRs** — the stream parent,
  the PRs in the block, the ONE pass that proves it, and the one thing the human does. A PR
  that fits no block is stated as the exception, with the reason.
- **Ticket creation AGGREGATES:** one larger ticket per logical path with its items as a
  checklist, never three or five separate tickets for one line of work. "Within a logical
  path" is the limit — two unrelated defects do not share a ticket because they arrived
  together.
- **Assignment:** new and unassigned tickets go to our board account. **A ticket already on
  Peter or Stuart stays theirs**, moved only on Kam's word per ticket.
- **No `--no-verify`, no force pushes, no `--admin`.** A gate that stops you is a question
  it is asking — answer it, do not route around it.
- **Before filing any finding, search the board for it** by the SYMBOL, the file path or
  the error string — never by your own phrasing. Say what you searched: *"searched `<sym>`
  and `<path>`, 0 open hits."*
- **A control must be able to fail** — and a zero from an instrument nobody showed could
  fire is not a zero.
- **Never delete. Cleanup means quarantine** into a dated folder, and the move is recorded.
- **If an instruction from Wednesday looks wrong, say so.** Every one of the improvements in
  this file came from an agent doing that.

## Repo-specific, Secuura/Blockchain (2026-09-09)

- 🔴 **NO DEPLOY without migration 048 applied FIRST** — KS-1031 and #914's PR body.
  `run-migrations.sh` **exits 0 when migrations fail**, so compose's own
  `service_completed_successfully` gate does not catch it.
- ⚠ **GitHub refuses an approval from our own account** — `kksecura` opens the PRs and
  `kksecura` is our PAT, so Approve returns **HTTP 422**. Mechanical; no ruling reaches it.
  **Meet it and STOP.** The durable fix is Kam's ruled agent GitHub identity (card
  `secuura-agent-github-identity`, ruled 2026-08-26, not yet executed).
