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
- **Ticket creation — the unit is the TEST PASS (Kam, 2026-09-07 13:23, verbatim):** *"if a single
  test is required, we should be creating one ticket with multiple items inside it rather than
  multiple tickets. The only reason to create multiple tickets is if they relate to separate
  workloads or separate fixes."* Full predicate and the brief line: `fleet/specs/brief-standing-lines.md:166`.
  ⚠ The older 2026-09-06 09:42 wording (*"one larger ticket per logical path"*) was withdrawn by
  Kam at 09:45 and is NOT the rule — cite the 09-07 test-pass rule, never the 09-06 wording.
  (Corrected 2026-09-11 14:04: an earlier edit the same day struck the whole line as withdrawn,
  which was wider than the withdrawal.)
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

---

## A VERDICT LINE IS A CLAIM ABOUT WHAT RAN — print the ratio, never "all"

**Why this exists.** On 2026-09-09 a Secuura seat, sweeping for guards that skip a member and still
exit 0, found the class one level above the guards: **`PREFLIGHT PASSED.` printed identically whether
13 legs ran or 10.** Proven by control on one tree at one commit, changing only the gateway URL —
gateway up: 0 skipped, `PREFLIGHT PASSED.`, exit 0; gateway closed: **3 legs SKIPPED**, `PREFLIGHT
PASSED.`, exit 0. The two runs are indistinguishable from their verdict line, and the three legs that
vanish include the two closest to a security assertion. **That line is what gets quoted into PR Test
Evidence blocks that a client human reads.**

**The class is not "guards with skip lists". It is A VERDICT COMPOSED SEPARATELY FROM THE WORK** —
and it reproduces anywhere a summary is written by different code than the thing it summarises: test
runners, deploy scripts, migration gates, audit passes, health checks, batch jobs, a wrap mail.

**The rules:**

1. **A pass line carries a RATIO, never a quantifier.** `13/13 legs ran` beats `all legs passed`;
   `23 / 23 services` beats `all services`. **A quantifier is a claim about a denominator the reader
   cannot see.**
2. **A skip is not a pass.** Zero failures and ten of thirteen legs is not the same event as zero
   failures and thirteen of thirteen. If a run could not execute part of itself, its verdict says
   INCOMPLETE and its exit code is non-zero — or, where a skip is genuinely legitimate, the count is
   printed and the reader decides.
3. **Ask of any summariser: what would this print if half the work never ran?** If the answer is "the
   same thing", the verdict is decoration and every claim resting on it is unfalsifiable from its own
   output.
4. **Prove it with a control, in both directions.** Force the skip condition and show the verdict
   changes; run it clean and show it still passes. A guard that can only fail is as useless as one
   that can only pass.
5. **When you discover your own already-shipped evidence rests on such a line, strengthen the shipped
   instance immediately** — re-read the leg-by-leg output and post the provenance on the artefact —
   rather than only fixing the future. The 2026-09-09 seat did exactly this on PR #924.

**Precedent to copy rather than reinvent** (both already in the Secuura corpus, which is why the fix
shape was settled rather than open): `run-shell-suites.sh` refuses the vacuous pass in terms — *"'all
0 are reached' is not a pass: there is nothing being gated"* — and `check-production-guard.sh` prints
`23 / 23 services`.

---

## "WHAT DID MY BRANCH CHANGE" IS A THREE-DOT QUESTION — `other..HEAD` on a branch you are BEHIND shows their commits as yours

**Why this exists.** On 2026-09-09 a Secuura seat asked whether its branch touched a lockfile. It ran
`git diff --name-only origin/develop..HEAD`, got **12 lockfiles**, and was one step from reporting the
mainline as broken repo-wide. The branch was **9 commits behind develop** and had touched **two files,
neither a dependency file** — `git diff --name-only $(git merge-base origin/develop HEAD)..HEAD`.

**The mechanism:** a two-dot diff `A..B` compares the two ENDPOINTS. If B is behind A, everything A
gained since the fork shows up as though B changed it — **in the direction that makes your own branch
look guilty of someone else's commits.** So the natural next sentence is an alarm, and the alarm is
about the wrong repository state entirely.

**The rules:**

1. **To ask what YOUR branch changed, diff from the MERGE BASE** — `git diff $(git merge-base X HEAD)..HEAD`,
   or `git diff X...HEAD` (three dots, which does it for you). **Never `X..HEAD`.**
2. **The same trap sits in `log`**: `git log X..HEAD` is correct for "my commits" and
   `git log X...HEAD` is not — the two commands want opposite dot counts, which is exactly why this
   is worth writing down rather than remembering.
3. **If a "what did I change" answer surprises you by its SIZE, check how far BEHIND you are before
   you check what you touched.** `git rev-list --left-right --count X...HEAD` costs nothing and tells
   you whether the number is about your work or about the gap.
4. **A gate refusing your push is a claim about YOUR TREE, not about the repository.** Before
   reporting a repo-wide blocker, establish whether the failure follows the branch or the trunk — the
   cheapest test is whether merging the trunk in makes it go away.
5. **This is a FALSE MEASUREMENT, not a false absence** — the command ran, succeeded, and answered a
   different question than the one asked. It belongs beside the census rules: *complete over what?*
   Here: *changed relative to what?*

---

## A TAMPER'S RESTORE NEEDS A UNIQUE ANCHOR — "the line I just changed" is not automatically one

**Why this exists.** On 2026-09-09 a Secuura seat red-proofed a guard by reverting `auth.ts:826` to
`await userRepo.updateUser(user.id, { passwordHash: newHash });`. **That exact string already exists
verbatim at `auth.ts:539`** — the opportunistic login rehash. Its restore asserted `count == 1`, the
assertion **failed**, and it restored by line number with the content checked first, verifying 539
untouched.

**What a silent wrong-occurrence restore would have done:** left the tamper in a DIFFERENT function,
in a file the seat believed it had restored, **and passed every test in the run** — because the tests
were pointed at the line it meant to tamper, not the one it actually left broken.

**The rules:**

1. **Before tampering, prove your anchor is unique** — `grep -c` the exact string in the file. If the
   count is not 1, tamper by line number with the surrounding content asserted, or pick a longer
   anchor that is unique.
2. **Assert the restore, do not perform it.** `count == 1` on the way back, plus a **sha256 of the
   whole file compared to the pre-tamper hash**. A restore you did not verify is a claim.
3. **`git checkout` is not the answer here** — it reverts more than your tamper if anything else in
   the tree moved, which is why this fleet restores by content and hash instead.
4. **The failure is silent by construction:** the tests you then run are aimed at the line you MEANT
   to change, so a tamper left in a sibling function produces a green run and a corrupted file. **The
   uniqueness check is the only thing between you and that.**
5. **Generalises past tampers** to any scripted edit-then-revert: sed on a config, a stubbed
   credential, a temporarily disabled guard, a patched fixture.

- **An exit status read through a pipe is the pipe's, not the command's — and this is about PIPES, not about pushes.** (Secuura seat s164, 2026-09-10, in its own words: *"The requirement is not about pushes; it is about pipes."*) Wednesday had written this standing line as *"push unpiped and paste the exit line"* because every recorded instance had been a `git push`; the seat then made it on a lockfile regen loop minutes after quoting the rule back, and `exit=0` was `tail`'s. **Redirect to a file and read `$?` on its own line** (`cmd > out 2>&1; rc=$?`), then read the file. In zsh `${PIPESTATUS[0]}` is empty — the equivalent is `$pipestatus[1]` — so branching on a piped status is a check that cannot fail. **A rule written from the instances it was found in is complete over those instances and silent about the class.**

- **The half the pipes line was still missing, added 2026-09-10 after it bit the seat that improved it:** `${PIPESTATUS[0]}` is **bash**. The Claude Code Bash tool runs **zsh**, where it expands to the EMPTY STRING — so `rc=${PIPESTATUS[0]}` assigns nothing, `[ "" = 0 ]` is false, and the guard reads as a silent failure that is indistinguishable from a real one. zsh's equivalent is `$pipestatus[1]` (lower-case, 1-indexed). **The shape that needs neither, and the one to write by default: `cmd > out 2>&1; rc=$?` — then read the file.** The rc is real and the output survives. (Wednesday's own ledger held this trap twice and it was not in the brief; a rule you improve is not a rule you have finished.)

---

## TOUCHING A FILE THAT WAS REPAIRED IN THE LAST DAY

**Why this exists.** On 2026-09-10 two agent-blind defects in `wake_watch.sh` were fixed in the
morning under Kam's `parameterise` ruling (`a66e3793`, card marked **delivered**). **Four hours later
Wednesday proposed a change to that same file carrying a third hardcoded, seat-specific path** — a
re-introduction of the family that had just been closed, into a file everyone now believed was clean,
past a card that had already been told the job was done. It was caught by the OTHER coordinator, not
by the author, and not by any gate.

**The rule, for any agent about to change a recently-repaired file:**

1. **Ask when this file was last fixed, and what the fix CHANGED** — `git log -p` the repair, not
   just a read of the current text. **The constraint a fix introduces is invisible in the final
   file**; the diff is the only place it is stated.
2. **A card marked "delivered" is the guard standing down, not the guard confirming your change is
   safe.** It says an earlier defect was closed. It says nothing about yours.
3. **Being the person who repaired it is not protection.** It is what makes you fast and confident
   enough to break it — which is the actual mechanism of this failure, observed on its author.
4. **If the repair had a family** (agent-blindness, hardcoded paths, unquoted variables), **grep the
   file for that family before adding anything**, including in the code you are about to write.

**Same clock as [[../../0_Brain/learnings/2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]],
different object:** a rule is least tested in the hour it is adopted; a file is least defended in the
hours after it is repaired, because the repair consumes the attention that would have noticed the
next change. Framing named by the Datasec coordinator, 2026-09-10.
