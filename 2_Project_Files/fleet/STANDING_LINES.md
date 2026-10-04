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

- **TRUE DUPLICATES ARE OURS TO CLOSE (Kam, terminal 2026-09-14 08:55, verbatim: "if these are truly duplicates, no need for external review or comment, let's just close them and archive them ourselves. This should be a standing rule going forward."):** a board pass that proves at SOURCE that ticket B asks for the same defect/work as A marks B `Duplicate of A`, closes and archives it with ONE facts-only comment naming A and the read — no proposal, no card, no Peter/Stuart ruling. Overlapping-but-distinct tickets are NOT duplicates and stay untouched; a client human's ticket is closed only when it is the SURVIVOR's duplicate of ours, never theirs into ours. Lesson: `0_Brain/learnings/2026-09-14_true-duplicates-are-closed-and-archived-by-us-no-external-review.md`.

- **A WORKTREE PATH IN A BRIEF IS ABSOLUTE, AND NEVER UNDER THE CLONE (found by Datasec/NexusAI S66, 2026-09-18, and it corrected this coordinator):** every gate or builder brief that tells an agent to create a git worktree gives the path as an ABSOLUTE path outside the project's checkout. A relative `qa-worktrees/<name>` resolves against whatever directory `git worktree add` is invoked from, and invoked from inside the clone it writes into the tree every seat treats as read-only — so the defect belongs to the INSTRUCTION, not to the agent obeying it. S66 hit it and its evidence suggests a second seat's gate agent did too, eight hours apart, from the same brief wording. **Test by its handle: if the worktree path in a brief does not start with `/`, the brief is wrong.** Two seats independently reaching the same wrong place from one sentence is a template defect; it is fixed here rather than in each agent's memory. Origin: S66's correction mail, 2026-09-18 00:12:57Z, DKIM verified; family `0_Brain/learnings/2026-08-09_an-enforcement-you-must-arm-is-not-one.md` (in-path, not remembered).

- **A MULTI-CLAUSE GUARD IS RED-PROVED BY FLIPPING EACH CONJUNCT SEPARATELY (Datasec/NexusAI S65, 2026-09-18, adopted verbatim):** *"a conjunction whose terms are never individually falsified is untested."* Where a guard's condition is `A && B && C`, a single red arm that trips all three at once has measured the PAIR and learned nothing about the PARTS — the same defect as a multi-clause guard red-proofed with a fixture that trips every clause (`0_Brain/learnings/2026-08-07_a-check-that-cannot-fail.md`, the Datasec/NexusAI S31 case). **Every brief for a multi-clause guard requires one red arm PER CONJUNCT, each flipping exactly one term with the others held true**, and the report names which term each arm falsified. Origin: S65's R16, red-proving the RD-516 trusted-stored triple (`endpointSource === 'stored'` AND `signInConfigured` AND `callerIsAuthenticated`) by flipping each of the three separately.

- **AN EXPLANATION OF WHY A FIX WORKS IS A CLAIM, NOT COMMENTARY — and its author is the last person who can catch it (Datasec/NexusAI S66, 2026-09-18, self-diagnosed after its THIRD confidently-wrong sentence in one day; adopted verbatim):** *"when I explain WHY a fix works, I reach for a tidy absolute and state it as measured. The countermeasure that has actually worked each time is someone else red-proofing my explanation, not my re-reading it."* **The shapes to distrust are the tidy absolutes:** *"exactly one call site"* (measured false — eleven handlers), *"this proves the eval reached that far"* (false — top-level function declarations hoist), *"stored means admin-configured"* (**Tuesday's own, and load-bearing for a security relaxation — falsified by an agent's measurement, not by re-reading**). **The rule: every sentence explaining why a fix works gets a red proof, or it is marked UNVERIFIED in the artefact.** A gate brief aimed at the author's own explanation is worth more than one aimed at the code, because the code has other readers and the explanation has none. This binds the coordinator's rulings exactly as it binds a builder's commit messages.

- **"MAIN MOVED" AND "MAIN MOVED IN A WAY THAT REACHES MY CELLS" ARE DIFFERENT FACTS — and only the second one costs anything (Datasec/NexusAI S66, 2026-09-18, adopted verbatim):** when the trunk moves under a gated or in-flight branch, **do not re-run anything until you have read WHAT moved.** `git diff --stat <old>..<new>` against the paths your cells actually exercise settles it in one command. S66's case: `e0ea198..d881f95` was one line of `DEPLOYMENT_GUIDE.md`, nothing under `static/` or `backend/`, so under C-68 there was no affected cell and the movement was a non-event — it checked rather than assumed, and said so. **This is the crispest statement of C-68's real content and it cuts exactly the gate duplication Kam ruled against (2026-09-18 09:22):** a seat that treats every trunk movement as a re-run trigger spends sessions proving nothing, and a seat that ignores trunk movement misses the one that matters. **The discriminator is the diff, not the SHA.** Corollary from the same seat: a clean merge preview is NOT evidence the counts are right — regenerate them on the merged tree regardless.

## 2026-09-22 — after `git apply` in a worktree, RESTORE DISK MODES FROM THE INDEX before any push (Secuura Seat C 19th, #1189 pushed ungated)
⚠ **CORRECTION 2026-09-29 (Secuura Seat B 43rd, measured): do NOT use `git checkout-index -a -f` for this.** It restores file CONTENT from the index, not only modes, so it silently REVERTS a patch applied with `git apply` (the apply printed "applied", the tree read clean, and the change was gone). Restore the exec bit on the specific file instead (`chmod +x <file>` after checking `git ls-files -s <file>` shows 100755), then verify with `git diff` that your change is still present. The rule below stands; the command it suggests does not.
`core.filemode=false` + `git apply` onto an existing 100755 file rewrites the working-tree copy WITHOUT the exec bit (index and HEAD keep 100755); if that file is the pre-push hook, git skips it with only a `hint:` line and the push rc stays 0. Every raise brief carries: after every `git apply`, `git ls-files -s | awk '$1=="100755"{print $4}' | xargs chmod +x` (or `git checkout-index -f -a`), then `test -x .githooks/pre-push` asserted before the push — in the series tool, with a control (an applied hunk onto a 100755 file leaves the disk bit set). A hook is judged by its DISK copy.

## Seat-owned tools copied from a predecessor: re-key the PROSE, not only the namespace (2026-09-25, Seat B 27th)
When a successor copies a predecessor's merge/push/lock script, grep the copy for the PREDECESSOR'S SEAT NAME as prose (e.g. `Seat B 26th`) as well as its namespace tokens (`s-b26-`). `merge22.py:186` hard-coded "Merged by Seat B 26th" into every squash body; a namespace-only re-key would have written a false author line onto develop permanently. Proof of the re-key = read the body the tool WOULD write: own seat name present, predecessor's absent. Better: the seat name is a required argument with no default.

## A parser fix is tested against CAPTURED real output, never against the ticket's example line (2026-09-25, tier-2d gate on #1241)
KS-1226's example `Tests  1 failed | 1 skipped | 243 passed (245)` had been COMPOSED by a 09-17 gate probe; real vitest 4.1.11 prints `skipped` AFTER `passed`. The PR matched the ticket's words, passed its own cells, and returned NULL on every real summary. Any brief for a regex/parser/format change requires: capture the real tool's output first (fixture outside the package, the same reporter/flags the consumer uses), paste it verbatim into the cells, and name the tool version. An example line in a ticket is a representation until it is reproduced.

## A close withheld by §5f carries the CANONICAL handle, lowercase, verbatim (2026-09-26, Seat M1)
When `secuura-test-discipline` §5f withholds Done on a runtime change, the ticket gets ONE comment in exactly this shape (KS-1165 / KS-932 precedent): `Merged <sha> (PR #n, <file>); offline gates green; NOT Done per secuura-test-discipline §5f — live sweep owed (torn-down rebuilt stack, all containers verified up), unverified: <what>`. The search handle is the phrase `live sweep owed`, lowercase. On 2026-09-26 two tickets carried a capitalised `Live sweep owed` and a case-sensitive search for the established form missed exactly those two. `live sweep` alone over-collects (32 vs 14); `§5f` alone returns 99. The sweep list is built from this phrase, so a variant spelling silently drops a ticket from a list that reads complete.

## A missing gate is not a passing gate — quote only the gate lines your push actually printed (2026-09-26, Seat B 31st)
The pre-push hook filters by PATH: a push touching no `Blockchain/Dev/` path runs only the format-gate, and the platform preflight (the fleet STOP counts) never runs. **A PR body or READY carries only the gate lines that appear in THAT push's log** — never the fleet counts as boilerplate. If the platform preflight did not run, say `fleet STOP: NOT APPLICABLE (format gate only)`. Found by B 31st on #1291 when its own parser returned None for all three figures.

## A search token that contains your own worktree name matches every path you own (2026-09-26, Seat B 31st)
Worktrees are named after their work (`s-b31-ks1341b`), so `grep -c '<ticket-slug>'` over lint/tsc output counts EVERY absolute path in that worktree, not the file you care about (B 31st: 14/14 lint lines, 622/622 tsc lines). **Search on the real FILENAME, and run the same pattern over a baseline run that predates the file as the control** — the control must read 0 (or the pre-existing count) before the number is believed.

## A hyphenated foreign key ATTACHES in a PR title, body or commit message — in a Linear COMMENT it only cross-references (2026-09-26, Seat B 31st; Wednesday agrees)
The un-hyphenation rule binds the squash subject, the squash body and commit messages (Linear/GitHub attach tickets from those). A ticket COMMENT that points at a follow-up it just filed may name it hyphenated, because there the cross-reference is the intent. The key scanner flags both; the author reads which surface it is before acting.

## A re-key checker classifies prose by SYNTAX, never by how a line reads (2026-09-26, Seat B 32nd)
Guessing "this is a comment" from a line's first words ("The ", "Reads", "⚠") is blind both ways: real docstring lines read as live code, and any live line that opens with "The " reads as prose. Classify with the language's own tokenizer (Python `tokenize`: prose iff every token on the line is a COMMENT or STRING; a file that will not tokenize is REPORTED, never assumed clean). In a proof driver, naming the predecessor script is the POINT: a token is a defect there only when the line INVOKES the predecessor, and the matcher must allow `VAR=… bash "<pred>"` call shapes (CONTROL D caught that miss).

## A control that runs the real guard runs its side effects too (2026-09-26, Seat B 32nd)
An arm that drives the REAL release/lock/push writes the real cool-off stamps, markers and logs, and the NEXT arm then reads them. Assert where every side effect landed and clear it inside the arm, or a later arm reports a false defect. B 32nd's A7 printed "STILL WAITS FOREVER" because A11's real release had written a real 90 s cool-off.

## A handover names WHICH develop it measured (2026-09-26, Seat B 32nd)
`origin's develop (ls-remote)` and `refs/remotes/origin/develop` (the local tracking ref, which moves only on a fetch) are different facts, and both can be true at once. Every handover or brief line naming "develop" says which of the two it read, and with what instrument.

## A re-key checks EVERY predecessor generation a file names, not only the immediate one (2026-09-27, Seat B 32nd)
Inherited tools accrete stale tokens across several hand-offs (`merge28.py:160` still printed `.push-lock-25`, two generations back, in a LIVE refusal message). A re-key checker's token list is built from every generation present in the file (grep for the family pattern, e.g. `push-lock-[0-9]+`, `b[0-9]+(st|nd|rd|th)`), never from "the seat before me".

## A merge seat MAY refresh the shared checkout's tracking ref when a signed GO cannot be executed without it (2026-09-27, Wednesday ruling)
One `git fetch origin develop` under the push lock, measured (exactly one ref value moved; HEAD, local develop, untracked set and `.git/config` unchanged) and disclosed in the MERGED mail. Instrumental to a GO already signed, so no ASK is needed. Anything beyond a tracking-ref refresh is still an ASK.

## A red set quoted in a PR body names the row DESCRIPTIVELY when the test title embeds a foreign key (2026-09-27, Wednesday ruling on Seat B 32nd's question)
Write `A1 GET /` or `C3 SOURCE`, and add "the cells' titles carry the ticket key as file content", instead of pasting `RED KS-1341 A1 …` verbatim into a PR title, body or commit message, where a hyphenated key ATTACHES the ticket. Inside a ticket COMMENT the verbatim title is fine (it only cross-references). This is the form B 32nd already used on #1293, #1294 and #1296.

## A proof script cleans up ONLY its own scratch directory; it never deletes a live artefact in the seat record folder (2026-09-27, Seat B 33rd, defect found in B 31st's and B 32nd's `pushproof`/`ffproof`)
Both proofs ran `rm "$R/.my-last-release"` with `$R` = the script's own directory, i.e. the seat's record folder. That deleted the LIVE rule-B cool-off stamp that a real lock release had written, and silently voided the 90-second wait. Every delete in a proof is scoped to the proof's own `$W` scratch. After a proof runs, check the live artefact it sits beside: a real stamp must survive a proof with its value unchanged.

## A copied tool is re-keyed for PATHS and ENVIRONMENT-VARIABLE NAMES as well as seat names (2026-09-27, Seat B 33rd)
`arms28.py` set `MERGE27_SCRATCH` while `merge28.py` read `MERGE28_SCRATCH`, so the per-arm scratch isolation never took effect. Its refusal arms did not depend on scratch, and every merge that followed was verified by Wednesday at source (PR API + END tree), so no merge result is in question. Two tools also carried a dead session's absolute scratchpad path as a live default. The re-key token list includes every env-var prefix and every absolute path that names a predecessor, with a set-equals-read assertion for each env var.

## A diff-line comparator tests `l and l[0] in '+-'`, never `l[:1] in '+-'` (2026-09-27, Wednesday AND Seat B 33rd, the same trap twice in one day)
In Python, the empty string is "in" every string, so `'' in '+-'` is True. A comparator written the short way counts the diff's trailing empty line as a change, and reports "NOT identical" (59 vs 60, 53 vs 52) on patches that are byte-identical. Both seats caught it from the off-by-one. Every such comparator carries a control: a known-identical pair must print IDENTICAL, and a one-token mutation must print DIFFER.

## A namespace check greps EVERY spelling of the seat token (2026-09-27, Seat B 33rd)
B 33rd's guard grepped the branch segment `-b33-` and nearly missed a ref it had created itself, `refs/seatb33/pr1301`, which has no hyphens. A seat's namespace check lists every form its token takes: the branch segment, the worktree prefix, a ref namespace, and argv tags. Each form carries a control that fires on a planted instance of that spelling.

## A stacked PR's squash leaves a no-op file in its three-dot set (2026-09-27, Wednesday ruling on Seat B 33rd's Q-1301)
After the base PR squashes and the stacked PR is retargeted to develop, the stacked PR's merge-base is still the OLD develop. Its three-dot file set therefore still includes the base PR's files, byte-identical to develop now. The GO for a stacked PR declares those files as extra equality targets (blob == develop's, mode checked), marked NO-OP, so the merge tool's "file set == declared targets" check passes on a true assertion instead of refusing.

## `git rev-parse <sha>:<path>` on an object you have not fetched is neither a blob nor an error (2026-09-27, Seat B 33rd)
When the commit is not in the local object store, the command can hand back the argument string itself, and an equality check against a real sha then reads as "different". A remote blob is read through the contents API (`GET /repos/…/contents/<path>?ref=<sha>` → `sha`), or the commit is fetched first under the lock. A STOP driven by a blob comparison is re-checked by the other instrument before it is believed.

## A declared squash subject NEVER carries the `(#n)` suffix, and its length is checked as it will LAND (2026-09-27, Seat B 33rd's disclosure + Wednesday's ledger row)
GitHub's squash merge appends ` (#n)` to the subject it is given. gate31's addendum declared subjects already ending in `(#n)`, and three doubled subjects landed on develop permanently (#1300's at 95 chars, over the 92 rule). Gate drafters write addendum subjects WITHOUT the suffix. Merge tools refuse a declared subject matching `\(#\d+\)$`, and measure MG-11 as `len(declared) + len(" (#n)") <= 92`. The GO's key scan also runs this length check.

## A no-op path and an overlap path are different declarations (2026-09-27, Seat B 33rd on Wednesday's Q-1301 ruling)
`merged_blob_paths` declares a genuine OVERLAP: the merge resolves a file to a blob DIFFERENT from the PR head's. A squash-stack NO-OP (head == merged == develop) is declared under its own key, `noop_paths`. Using the overlap key for a no-op trips the overlap check correctly. Every exception is proven by an undeclared-path arm and a one-digit wrong-blob arm before it is relied on.

## A tool that can be pointed at an alternative input proves the bytes it VERIFIED are the bytes it USED (2026-09-27, Seat B 34th, a defect in raise28/29)
`raise2x.py --patch` reassigned only the PATH. The string it split and applied stayed the READY's, so the `cmp`-vs-golden check ran on one file while another was raised. Re-reading the path is not enough. Assert content equality at the point of use (`split-source CONFIRMED == <file> (<bytes>, sha256)`), and drive both arms on a real subject. **Fixed in `5_Project_History/2026-09-27_seatB-34th/raise/raise30.py`; copy forward from THAT file, never from raise28/raise29.**

## `patch -F0` is not `git apply --check` (2026-09-27, Seat B 34th, on Wednesday's KS-1108 verification)
GNU `patch` accepts a hunk whose old-side count is wrong, and `git apply` refuses it. A brief or addendum that verifies a recounted or regenerated diff with `patch -F0 --dry-run` has not verified it for a seat that applies with `git apply`. Verify with the tool the seat will use (`git apply --check` in a scratch repo seeded by `git show <tip>:<path>`), or run both.

## A tool copied forward is keyed to its AUTHOR's position, not its function; and a re-key tool must be in its own token map (2026-09-28, Seat B 35th's ITEM 0)
Seat B 35th found four inherited LIVE defects in B 34th's `*30` tools, each correct for B 34th and wrong for its successor, and none of them would have failed loudly: the inbox matcher's pane constants (the `-B` lane's, inverted), which tagged 8 of B 34th's own mails as the new seat's; the re-key checker's INVOKE regex (`2[0-9]`), blind to the `*30` generation it existed to catch; that checker's THEIRS folder and label, one generation stale; a lock proof's "stamp leaked" arm that tested EXISTENCE, so a real earlier release read as a leak. Also: `rekey30.py` had no entry for itself in its own map, so it survived its own pass. **Rule for every copied tool:** before it guards anything, re-derive every seat-, pane-, generation-, folder- and path-keyed constant from the NEW seat's position, add the re-key tool to its own token map, and prove each constant with a control that goes the other way on the real subject (the real inbox, the real predecessor folder), not with a synthetic fixture.

## A seat's "other seats" lists name EVERY predecessor that shared its pane, and a GO is acted on only when it names THIS seat's number (2026-09-28, Seat B 36th's ITEM 0, Q4)
Seat B 36th measured that the re-key maps predecessor -> self on live lines, so the inbox matcher's OTHER_SEATS list turned the predecessor's token into the seat's OWN token each generation, and never added the real predecessor. Result, on real subjects: B 35th's `GO (Seat B 35th): merge 1311 … 1315` classified FOR ME in B 36th's inbox, a stale five-merge authorisation read as its own. The same mechanism hollowed out `namecheck`'s FOREIGN list and inverted its control. **Rule for every seat that copies tools forward:** (1) after re-keying, ADD the immediate predecessor's and the one before's seat tokens (e.g. `b 35th`, `b 34th`) to OTHER_SEATS/FOREIGN, and prove it on a real predecessor subject still in the inbox (it must read FOREIGN) with your own subject as the control (it must read FOR ME); (2) a GO, RELEASE or merge instruction is acted on only when its subject names THIS seat's number, whatever the matcher says; (3) this binds both lanes (unsuffixed and `-B`). Evidence: one seat, measured on real mail with controls both ways (w=1, pilot). Built against a stale authorisation being read as live; says nothing about mail with no seat number (that is a QUESTION to Wednesday, not a guess).

## A checker's verdict prints how many items it CHECKED, and "0 checked" is never CLEAN (2026-09-28, Seat B 37th's ITEM 0)
Seat B 37th measured it on identical trees with only one constant changed: the inherited `bannercheck` carried `GEN = "32"`, a value the re-key could not rewrite (no bare `"32"` key in the SELF map, by design). It printed **VERDICT CLEAN with 0 lines checked and both controls PASS**, because the controls hardcoded their own generations and never guarded the parameter the subject depends on. The fixed value checked 16 lines. **Rule for every seat that writes or copies a checker:** (1) the verdict line states the population checked (`N checked`), and `0 checked` is a FAIL, never CLEAN; (2) at least one control must run THROUGH the same parameter the subject run uses (here `GEN`), so a stale parameter reds the control too; (3) any per-generation constant in a copied tool is found by grepping for the predecessor's number as a bare string, not only through the re-key's map. Evidence: one seat, isolated A/B measurement on identical trees (w=1, pilot). Family: a check that cannot fail; a false absence is usually my own instrument.

## Never end a turn on a "next up" line with nothing running: a stated next step is not a wake (2026-09-28, the third instance)
Three seats (B 25th on 09-25; B 36th and B 38th on 09-28) ended a turn by writing their next step ("Next up: ITEM 2 …") with no background job and no pending mail, then sat idle until Wednesday's watcher noticed. A turn that ends stops everything; the harness re-invokes a seat only when a background job EXITS or a message arrives. **Rule:** before ending any turn while queued work remains, EITHER keep working (start the next item in the same turn) OR leave a real wake: a background job that exits when done, or a QUESTION mail to Wednesday. A "next up" sentence with nothing running is a stall, whatever it says. Evidence: three seats, three watcher catches, all zero cost only because the watcher fired.

**Fourth instance, 2026-09-29 04:21 (Seat B 41st), WITH this line in its brief:** it ended on "I'll keep going unless you want the order changed" with no job running. The written line does not fire at the moment of ending a turn. **What catches it today is `wake_watch`'s idle leg (about 3 min) plus a Wednesday CONTINUE.** Enforcement candidate: a Stop-hook in the Secuura seat's launcher that refuses to end a turn whose last line matches `next up|I'll keep going|continuing with` while no background job is live. It is shared tooling in another project's launcher, so it is proposed to Kam, not built.

## Read a repo file from a SHA, never from the Secuura MAIN checkout's working tree (2026-09-29, Seat B 44th's CORRECTION + QUESTION)
The project's main checkout (`!CODING/Secuura/Blockchain/2_Project_Files`) is read-only to seats and sits far behind develop: at 3bad652d1 it was **176 commits behind** 8af6ab82 (Seat B 44th, `git rev-list --count`). Twice (B 36th on 09-27, B 44th on 09-29) a seat read `audit-baseline.json` from that working tree and reported a row (GHSA-jjmj, removed by #1214) as live at the fuse. B 44th had measured the lag at boot and still read the file an hour later. **Standing line for every Secuura brief:** read any repo file as `git show <sha>:<path>` at the sha you mean (or from your own worktree after checking its HEAD), and name the sha beside the claim. A file read from `2_Project_Files`'s working tree is a claim about 3bad652, not about develop.

## After a rebase, `cmp` of the pre/post diffs is the proof; `patch-id` is corroboration only (2026-09-29, Seat B 44th's control)
Seat B 44th drove `git patch-id --stable` against four mutations of a real diff: it caught added-line text, context-line text and a removed hunk, and MISSED a whitespace-only change (a trailing newline returned the SAME id), because patch-id normalises whitespace by design. `cmp` caught all four. **Standing line for every rebase-and-repush:** store the pre-rebase diff, then `cmp` it against the post-rebase diff (rc 0 is the proof). Report patch-id equality only beside it, never instead of it.

## An audit-baseline re-date carries a FROZEN-CLOCK red proof, run by the gate itself (2026-09-29, gate42b's recommendation, adopted)
A baseline re-date is a security control, even when its change is a config file graded Tier 2. Its gate re-runs legs 6-7 with the clock frozen just past the old expiry (base must red on the named rows, head green) and at a control date past the new expiry (head must red), using a preload proven to move the clock (positive arm) and to refuse when unset. The author's own proof is corroboration, never the verdict. Measured on #1340: develop rc 1 on frvp at 2026-09-30T00:01Z, head rc 0, 2026-10-10 control rc 1.

## A correction comment to a client is HELD until its PR's gate has read it, and every sentence carries its instrument or "unmeasured" (2026-09-29, KS-1374: three client-facing texts in one day, each with an unmeasured claim)
Posting a correction "with the PR" puts it on the client's screen BEFORE the gate that would catch it. Draft it, put it in the READY, let the gate check every factual line against the head, THEN post. Reassurances ("unchanged", "only local", "limit 2000") are the claims most likely to be wrong. If an earlier comment is wrong, EDIT it to be true rather than stacking another. Lesson: `0_Brain/learnings/2026-09-29_a-correction-to-a-client-is-a-new-claim-gate-it-like-code.md`.

## `git apply` can drop a file's DISK exec bit while the index still says 100755 (2026-09-30, Seat B 47th)
With `core.filemode=false`, `git apply` on a tree-100755 script left it `-rw-r--r--` on disk; git reported nothing (porcelain showed only the content change, the index still read `100755`). The ks1054 suite then read 29/11, every failure "predicate missing or not executable" — **a mode defect wearing the costume of 11 product defects.** Control that isolated it: six untouched 100755 scripts in the same directory kept `-rwxr-xr-x`, and a `git archive` of the same base blob came out executable. **After applying any patch to a 100755 file, check `[ -x <file> ]` on disk before the first test run; restore with `chmod 755` (bytes unchanged, `cmp` rc 0) and read the COMMITTED mode from the tree, never from `stat`.** Evidence basis: one instance, measured with the controls above.

## Two live seats on one inbox: every mail names the seat AND uses that seat's own row tag, and each seat's matcher is proved against the OTHER seat's real subjects on BOTH tags (2026-09-30, Seat B 49th)
With Seat B 49th live on `Secuura/Blockchain` and Seat D 1st briefed for `Secuura/Blockchain-B`, B 49th drove real subject shapes through its own matcher: an UNSUFFIXED `[Wednesday -> Secuura/Blockchain] GO (Seat D 1st): …` classified **FOR ME**, so a GO meant for the co-tenant would have read as B 49th's. The `-B` form was safe only by accident (an old OTHER_SEATS entry). **Rules:** (1) Wednesday addresses every mail to a parallel seat on that seat's own row tag AND names the seat in the subject; (2) every co-tenant brief makes its seat add the other seat's name and token to OTHER_SEATS/FOREIGN, with controls going both ways on the other seat's REAL subjects, on BOTH the suffixed and unsuffixed tags; (3) short tokens (`d1`, `m1`) match on word boundaries only, with a hex-run control (`45a105d11745` holds `d1`; CORRECTED 2026-10-01: the earlier example `52dadb07f70d` holds no `d1`, found by the B 51st drafter, and a control that cannot fire is not a control). Evidence basis: one instance, measured with controls in `5_Project_History/2026-09-30_seatB-49th/raise/seatD-cotenant-proof.txt` (Secuura project).

## A background watcher dies at its harness timeout with NO signal to the seat; arm it at the maximum and re-arm before it lapses (2026-09-30, Seat B 49th)
Seat B 49th armed its inbox watcher with a one-hour background timeout; the harness killed it at exactly one hour (07:09:26Z), its log just stopped, and for a window the seat held NO wake while believing one was live. **Rules:** (1) arm every watcher or waiter with the maximum background timeout (7200000 ms); (2) note the re-arm deadline and re-arm before it, while still holding; (3) a claim that a watcher is RUNNING is a `ps` reading taken in the same action as the sentence. Evidence basis: one instance, verified by the seat against the inbox by API (nothing was missed).

## A token census states whether it is RAW substring or WORD-BOUNDED; the two disagree inside hex and base64 runs (2026-10-01, Seat B 51st)
The B 51st brief recorded "`b50` 0 hits" over B 49th's folder. Seat B 51st counted **2** raw hits: one inside a git sha (`…31db501cd…`) and one inside a base64 page token. Under a word-boundary rule `(^|[^0-9a-z])b50([^0-9a-z]|$)` both files read **0**. Both readings were right, and a successor could not tell which one was meant. **Rule:** every token count in a brief, receipt or handover names its predicate, either `raw` or `bounded` with the regex, e.g. "`b50`: 2 raw / 0 bounded". A seat-token decision uses the bounded count, and the raw count is kept as the hex-trap control. Evidence basis: one instance, measured both ways by the seat.

## One "no new mail" poll at the same second as a message's timestamp proves nothing; only the NEXT poll settles it (2026-10-01, Seat B 51st)
Seat B 51st's inbox watcher polled at 20:54:42Z, the same second Wednesday's ANSWER was timestamped, and printed `no new Wednesday mail FOR ME`. The API listing had not yet indexed the message. The next poll fired correctly, so nothing was lost. **Rule:** a seat never reads a single clean poll as "no answer yet". An absence is established by a poll that STARTS after the latest timestamp in question. The same seat noted a second trap: leg 7's reproduction hint counts `git ls-files '*package-lock.json'` from the REPO ROOT (45), not from `Blockchain/Dev` (40). Evidence basis: one instance each, measured by the seat.

## A merge tool must not ADD attribution the GO forbids; check the SENT body, not the input (2026-10-01, Seat B 53rd)
B 52nd's `merge47.py:391` appended `Co-Authored-By: Claude …` to every squash body that lacked one, so a GO saying "no attribution" landed a trailer anyway. B 52nd then wrongly blamed a GitHub harvest, and Wednesday adopted that claim without reading the tool. Seat B 53rd measured it (input 0, SENT body 1) and fixed `merge48.py`: the GO's `NO TRAILER` clause drives `no_trailer`, the composed body is asserted trailer-free before the API call, and a control proves the un-suppressed path still appends. #1367 and #1368 landed with 0 trailers. **Standing line for every merge seat:** carry the suppression forward in each re-key; check the body you SEND (not the file you built it from); keep branch commits trailer-free too, so the claim holds whatever GitHub does.

## `push<N>.sh` takes `.push-lock-<N>` ITSELF; never wrap it in your own take (2026-10-01, Seat B 53rd)
Seat B 53rd took the lock in a wrapper shell, then called `push48.sh`, which takes the same lock at `:121`; it waited 221 s on its own holder ("held by other" naming its own seat). It cost nothing because the wait comes before the push. **Brief wording:** say "push with `push<N>.sh` (it takes and releases the lock)", never "push under lock-N". Only bare git verbs (a ruled fetch, a merge tool that does not lock) are wrapped by hand.

## `npm ci --ignore-scripts` leaves `@secuura/shared` UNRESOLVABLE until `packages/shared` is built; build it BEFORE the first test, not only before the push (2026-10-01, Seat B 53rd)
The workspace symlink exists, so a directory listing reads "installed", but `main` is `dist/index.js` and `--ignore-scripts` builds nothing. `require.resolve` and a real import both threw MODULE_NOT_FOUND. Prove resolution by action from inside each touched service after `npm run build --workspace=packages/shared`.

## `require.resolve('<pkg>/package.json')` throws ERR_PACKAGE_PATH_NOT_EXPORTED when the package's `exports` map hides it; resolve the MAIN entry and walk up to the owning dir (2026-10-01, Seat B 54th)
Wednesday's B 54th brief prescribed `require.resolve('@hono/node-server/package.json', { paths: [...] })` to read a resolved version. It cannot run: `@hono/node-server`'s `exports` does not expose `./package.json`. **The working shape:** `require.resolve('<pkg>', { paths: [<dir>] })`, walk up to the directory whose `package.json` has that `name`, and read `version` off disk. Use a nonexistent module as the MODULE_NOT_FOUND control. **Also from the same seat:** when removing a baseline row, key the proof on the row KEY (parse both blobs' key sets), never a substring grep for the id. Other rows' reason text can quote it (frvp appears in the two react-router rows' reasons at :97 and :104).

## On git 2.51, `git push --dry-run` RUNS the pre-push hook; it is not a side-effect-free identity probe (2026-10-02, Seat B 54th)
Wednesday's B 54th brief said the dry run does not fire the hook. Seat B 54th proved the opposite in a sandbox repo: a real-push control printed the hook marker and created the ref; the dry run printed the marker and created no ref. In the shared checkout this runs the 287-line `.githooks/pre-push`, and a stale local develop inflates its range (KS-991). **Prove push identity with an SSH auth probe instead** (`ssh -T git@github.com` under the repo's own key; "Hi <repo>!", with a refused-key control), plus `ls-remote` rc 0. The real push via `push<N>.sh` from the seat's own worktree proves the write path.

## An npm `overrides` entry is INERT against a complete lock; `npm update/install --package-lock-only` leave it byte-identical (2026-10-02, Seat B 54th)
npm applies overrides when it BUILDS a tree. Against an already-complete lock it never re-evaluates an exactly pinned nested dependency, so both verbs print "up to date" and change nothing. The route that worked (Wednesday-ruled for #1369): prune the ONE stale nested entry, re-run in the ruled toolchain (node:24-alpine, npm 11.19.0), and prove the result equals an INDEPENDENT from-scratch resolve with the override (with the counterfactual without it). The key-by-key diff must show only that entry. **Also:** a lock-only re-run re-checks ROOT edges only (gate53 proved it with a deep-deletion control), so idempotence is not validation of deep entries; `npm ci` exercises the full tree. Prefer `^x.y.z` over `>=` in an override when a major is published (2.1.3 was).

## A JSON value-level comparison is not a byte-level one: report BOTH (2026-10-02, Seat B 54th)
Rewriting audit-baseline.json with `json.dumps` re-escaped em-dashes in 7 unrelated rows: the parsed comparison passed while the bytes changed. Only the text diff caught it. **When editing a tracked JSON file, prove the parsed delta AND that the text diff touches only the intended object** (keep the file's own formatting).

## A seat token is not always two digits (2026-10-04, Seat C 21st found it at ITEM 0)
- The re-keyed seat tools assumed a NUMERIC generation (`int(GEN)`, `range(20, int(GEN))`, `\d\d` stems, a `(4[0-9])` parked-file predicate). A lettered token like `c21` (or `50`, past 49) broke four sites: bannercheck int(), its banner regex matching `21` INSIDE `lockproofc21` (put the current generation FIRST in an alternation, longest-first, case-folded), stems() returning a VACUOUS CLEAN (0 checked; caught only by 0-checked-is-a-FAIL), and rekey_check failing in both directions. Every brief that re-keys a tool generation names this: grep the copied tools for `int(`, `\d\d`, `[0-9]{2}` and `4[0-9]` on the generation before the first run, and fix the predicate, not the map.
