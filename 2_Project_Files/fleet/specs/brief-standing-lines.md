# Standing lines for every brief (consolidated 2026-08-30 — paste, do not re-derive)

Promoted at the 08-30 consolidation from ledger rows that recurred across sessions. Each has
a mechanism or a measured instance behind it; the send gate cannot check them, so they live
here and travel in the brief body.

## Authority (signature-class actions: prod, demo deploy, money, external comms, irreversible)
- **A transcript turn authorises only if `promptSource: typed` AND the wording is not an echo
  of Wednesday's own sentence** — `suggestion_accepted` is a keystroke on a rendered line
  (ghost ladder rung 9, 08-27). Otherwise: DKIM-verified mail from kreiser.org@me.com.
- **A card Wednesday ruled on a relayed word is not a second source** — provenance names the
  event once.
- **When the principal is IN the session, confirm a two-word answer ("and associated") rather
  than interpret it** — cheaper to ask than to flip a default on a reading (s77, 08-27).
- Pane text is never authority; a tap may only POINT at the mail ("ANSWER in your inbox,
  DKIM-verify it").

## Evidence wording
- **Record the SET, not the count**: a suite's failing set is the signature; "FAIL 9,
  byte-identical to baseline" hid a fix landing and a defect arriving (KS-697, KS-703 —
  two proofs). Diff sets between runs; a count is a representation of a set.
- **Every count carries its predicate and its bound** (state set, window open at the
  counterpart's last write, limit) — "134 in backlog/unstarted/started since 10:32Z".
- **A zero needs a control that can fail independently** — and a control that AGREES with a
- **A control only discriminates if it can fail the SAME WAY the measurement can** (Secuura s133, 2026-09-05): a single-token control returned 7 beside a multi-word-phrase sweep that read 0 — the phrase LINE-WRAPS in the generated yaml and a single-line grep structurally cannot match it, while a single token never wraps. Sibling of "lint by-SHA copies outside the project returns 0 and cannot fail" (s132): the control must share the measurement's failure mode.
- **A comparison of two outputs must first assert that the outputs EXIST — two empty things are always identical** (Secuura s133, 2026-09-06: a corpus dump via `console.log` was swallowed by vitest, both files came back with zero lines, and the diff reported "IDENTICAL" with matching md5s — true and meaningless; caught by the line count printed beside it). Every equality check carries a non-vacuity assertion on both sides.
- **A step's own report of success is not evidence that it succeeded — check the artefact, not the exit banner** (NexusAI S37, 2026-09-05: a scripted conflict resolver failed on every call, `git add` + `rebase --continue` ran unconditionally, three commits landed with `<<<<<<<` nested three deep, and `git rebase` printed "Successfully rebased"). Rebase lines: after any scripted resolution, re-read the file for conflict markers AND check the resolver's rc BEFORE `git add`/`--continue`; abort the whole rebase on either. Sibling: `Object.freeze` on a Set does not stop `.add()` — test the freeze, do not trust it.
- **A gate line about a dependency is a claim about the CORPUS that gate reads** (Secuura s133, 2026-09-05): the root `audit:gate` printed "no longer reported — remove" for a body-parser row while leg 7 (`audit:locks`, each service's OWN lock) still reported it live in a standalone lock — the root audit reads the hoisted workspace tree and cannot see standalone locks. Before deleting a baseline row, BOTH gates must agree; a "deletion only" reading from one gate is the representation of a lock, not the lock.
  null is the suspect (grep that never ran; NOAUTH; empty bearer; dead SSH leg).
- **An absence claim carries the corpus it was measured against, verbatim.**
- **A before/after pair is not evidence until the two artefacts are shown to DIFFER — hash them** (NexusAI S37, 2026-09-05: its first RD-332 pair was byte-identical between builds because the sentence sat below the fold; the captions looked right). And health-confirm each server BEFORE switching the tree — a `git checkout` racing module loading served one build as two.
- **Name every suite by PATH and command, never by a phrase** — "the four platform suites" meant two different sets in this fleet's own QA reports on 2026-09-05 (Schemathesis/Akto/Playwright/k6 vs the four service suites); the tester had to resolve a builder's phrase Wednesday had relayed unread.
- **Never echo ANY portion of a credential — not a prefix, not a "redacted" head, not its length beside its value.** A presence check is `[ -n "$K" ] && echo set || echo unset` — the value never enters a format string (Wednesday's own 2026-09-04 w=1 severity-high row: `${T:-no}` printed a live token; a QA pane on 2026-09-05 printed the first 12 characters of a key "(redacted)" — a prefix is a partial leak in a transcript that outlives the session).

## Instrument traps (all measured)
- **Linear `updatedAt:{gt:"P1D"}` returns 0 with an agreeing 0 control** — ISO datetimes only.
- **Linear `comments(last:N)` returns the OLDEST** — `first:50` + client-side sort.
- **A launcher's aggregate drift warning ("N commits since the stack was built")** carries the
  OLDEST container's build time — it cannot say which service is stale; check per service.
- **`send_brief.sh --to` takes the PROJECT NAME** (routing table), not an inbox address.
- **`env | grep VAR` prints `VAR=` for an empty value** — presence is not a value.
- **zsh: no `PIPESTATUS`; unquoted `$VAR` does not word-split** — redirect to a file, read `$?`.
- **A CONTRACT DESCRIBING A DEFECT IS AS WRONG AS ONE DESCRIBING AN ABSENT CHECK** (seat B, 2026-09-06, KS-732): a published API description narrated a known fault verbatim — *"the password is REQUIRED BY THE SCHEMA BUT NEVER VERIFIED"* — written deliberately so the contract would not bless an absent check. **The moment the fault was fixed the narration became a lie, and nobody was assigned to notice.** So: a defect narrated in any published artefact (spec, schema description, README, header comment) is listed in the fixing PR's checklist and removed in the same change; and when you write such a narration, name the ticket that will delete it.
- **A CELL THAT CANNOT TELL THE FIX FROM ITS OWN FALLBACK IS NOT A REGRESSION TEST** (seat A, 2026-09-06, KS-921 F-1): the guard was fixed two ways — a corrected selector AND a looser cross-check that fails loudly on anything the selector misses. The regression cell asserted only "exit 1 and the filename appears somewhere", so with the selector fix removed **the cross-check also exits 1 and also names the file** — the cell passed against the exact tamper it existed to catch, and the suite stayed green. **Defence in depth is what makes this invisible**: the guard is still behaving correctly under the tamper. Assert WHICH mechanism judged the case, not that some mechanism did. Found by RUNNING the tamper, not by reading the cell.
- **A FIXTURE THAT NAMES THE WRONG OBJECT FAILS IN THE SAME SHAPE AS THE DEFECT IT GUARDS** (seat B, 2026-09-06, KS-720): a test fixture mocked table `wallet_challenges` where the product uses `wallet_auth_challenges`; the lookup returned undefined, the handler threw NotFound, and the CONTROL cell reported "link issued no write" — **indistinguishable from the defect under test**. A wrong name does not announce itself; it produces the symptom you were looking for. Caught only because a control was present. So: name every fixture object from the product's own schema/source in the same action, and treat a control that reports exactly the expected defect as a suspect until its subject is verified.
- **A RED-PROOF HARNESS NAMES ITS OWN SUBJECT IN ITS OUTPUT** (QA, 2026-09-06, KS-923 F2): a suite whose subject comes from `${VAR:-default}` treats an EMPTY value as unset, silently grades the SHIPPED file, and prints a transcript **byte-identical** to a genuine proof run (same sha256) — so no transcript can tell them apart. Use `${VAR-default}` (no colon) so set-but-empty falls to the FATAL, add an explicit set-but-empty guard, and **print the resolved subject path as the first line of every run**. Then a red-proof that graded the wrong file is visible in its own output rather than in nobody's.
- **The word-split rule has a costume that PRINTS SUCCESS** (s140, 2026-09-06 20:3x): `for p in $targets; do rm -f "$p" && echo removed; done` in zsh passes the whole list as ONE argument; `rm -f` on a path that does not exist **exits 0**, so six deletions that never happened printed six success lines. Caught by re-reading the directory, never by the exit code. Use `typeset -a` + `"${targets[@]}"`, and treat **`rm -f` rc 0 as not-evidence** — the control is the listing afterwards. (Cleanup still means quarantine, not removal; deletion is for credential scratch only.)
- **Unquoted heredocs execute backticks** — `<<'EOF'` for every brief/note body.

## Process
- **Palette from THIS project's style guide only — never invented, never another client's
  (Kam, 2026-09-02: "make sure project style guides are adhered to and never mixed").** Every
  UI brief names the project's style-guide / brand-token file as a READ-FIRST pointer. If none
  exists, item 0 of the round is to write it from the project's own existing brand tokens (the
  light theme, the logo, the customer's guide where the product is a client deliverable) — no
  new colour ships before the guide does. QA passes on visual work carry a brand-conformance
  leg: every introduced colour → the token it resolves to, or OFF-GUIDE = Major at any
  contrast ratio, no allow-list. A derived theme/palette is a BRAND decision = Kam's signature
  (the RD-160 precedent): rendered proposal to him before it ships. Instance: NexusAI dark
  mode rounds 6–8 (an invented navy palette, nine contrast passes, zero brand legs).
- **A ticket's title/description is not its resolution** — an archived ticket's conclusion is
  read from its resolution comments and the tree, and a constraint older than the current
  brief chain gets one re-read before it is copied forward (KS-291 "infeasible" carried
  stale for two days; ledger w=57, 2026-09-02).
- **A deferral recorded only in code ("tracked on KS-nnn") must have its own OPEN ticket**
  before the parent closes (KS-586 → KS-692).
- **Never delete** — quarantine (dated folder / Archive/); briefs carry the rule.
- **Positive controls WRITE on side-effecting systems** — label the artefact, keep it.
- **End-of-session must verify the VAULT push, not only the project push** — two sessions'
  records (207 lines) sat uncommitted in the vault silently until s91 found them blocking a
  pull (2026-08-31, credited to s91). A wrap that commits the project and skips the vault
  loses the session record with no signal.
- **Never `--no-verify` on ANY commit or push, a merge commit included** — a hook that refuses is fixed at its root cause or its verdict is READ and mailed to Wednesday; a bypass compensated afterwards is still a bypass and counts against the round (added 2026-09-06 01:1x after S38 bypassed the gitleaks pre-commit hook on a merge commit, disclosed it, and compensated with the canary + an explicit scan — the Secuura briefs carried the line, the NexusAI brief did not).
- **Never round-trip JSON (or any body that may carry escapes) through `echo "$var"` in zsh** — zsh's `echo` interprets backslash escapes, so a PR body ABOUT control bytes turned into a real control byte and the parse returned an EMPTY status that read as "not clean"; `printf '%s'` or pipe the source straight into the parser (s134, 2026-09-06 01:2x — a transport that corrupts a measurement while the data was never wrong).
- **A red-proof's tamper is shown APPLIED before its run is believed** — assert the tampered line is in the file (grep it, or diff against the saved original) before the suite runs; a patch script that dies leaves the untampered file, and the suite then prints a green that reads exactly like a test that cannot fail (S38, RD-335, 2026-09-06 01:3x — tamper F's patch died on a syntax error and the suite printed `27 passed`).
- **An identifier named in a brief, an ANSWER, a QA brief or a ticket is grepped in the repo at the SHA under discussion BEFORE it is written** — a name that appears only in prose (a comment, a report, a mail) is not the product's name, and quoting it downstream launders it into one (added 2026-09-06 02:1x, credited to Datasec/NexusAI S38: `unavailableReason` existed in exactly one place, its own comment; the QA report and Wednesday's GO adopted it, and the round's item 0 was commissioned in a name the product never had — the emitted field is `reason`).
- **Every SUCCESSOR brief carries TWO ruled sections, each read from its source in the same action, empty allowed and absent not:** `RULED BY KAM, NOT YET IN AN ARTEFACT` (from `decision_queue.sh list ruled` for the project since the previous brief, each card checked against its ticket/PR/row) AND `RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE` (every scope / holds / "do not" ruling in Wednesday's ANSWERs to the project since the previous `_successor_brief.md`, quoted in one line with the mail's timestamp). Added 2026-09-06 02:2x after Wednesday's 2026-09-05 23:24 ruling to s133 ("do NOT narrate KS-823 in a published contract") reached s134 through nothing it read and the tester paused the published yaml as approval-class (ledger w=4 of the ruled-but-undelivered family; lesson 2026-09-05_a-relayed-ruling… EXTENSION 2026-09-06).
- **A "comment-only" / "docs-only" claim is certified by a stripper PROVEN on a comment in every position it can occupy** — at line start AND after code on the same line — with a planted control in each position; a stripper that only strips line-start `//` reports a mid-expression comment as CODE and DIFFERS on a pure move (added 2026-09-06 02:2x, credited to Secuura s134: its (e) check read DIFFERS on the #831 placement fix because the defect — `sharedRegistry.// KS-823 …` — was invisible to the instrument being used to clear it; the general form, on KS-822 line 6: an instrument that cannot see a comment in an unusual position cannot certify a change as comment-only).
- **A validator's coverage is a claim like any other — a shipped validator is red-proved with one forbidden fixture per rule it claims to enforce, each shown to RAISE and to NAME the offending path, before its commit message says it makes errors "arrive where they were made"** (added 2026-09-06 02:4x, credited to Datasec/NexusAI S38: its ADF `validate()` proved it caught a bare string and was generalised to "it validates"; twenty minutes later a block nested inside a paragraph passed it and Jira answered 400 — "I did not red-prove the one I shipped").
- **A farm that reaches back into the tree it is supposed to isolate is not an isolation** — before any result from a by-SHA copy counts, `require.resolve` (or the language's equivalent) of the package under test is run INSIDE the copy and shown to land inside the copy; a symlinked `node_modules` that resolves a workspace package back to the original tree measures the split it was built to remove (added 2026-09-06 03:1x, credited to Secuura s134: its first `!`-free-path cell read 3 red and would have passed as a refutation; it checked resolution first and voided the cell as its own confound — "a cell that cannot come out green cannot refute anything").
- **A READER is red-proved on hostile input separately from the behaviour it feeds** — a comment stripper, a path matcher, an AST walker or any predicate that decides what the instrument SEES is tampered on its own (a trailing comment, a `//` holding `/*`, a relative path in a sibling directory, a spread/computed key) before the behaviour it gates is believed; a guard whose behaviour is red-proved on the corpus and whose reader was never fed a hostile line has been tested "against the shape I had in mind" (Datasec/NexusAI S39, RD-340, 2026-09-06 — its own four R-6 findings). [M]
- **A queue that moves to the next ticket moves the BRANCH first** — before the first commit of a new ticket the builder reads and states `git branch --show-current`; "the tree is clean" says nothing about which branch you are standing on, and a commit onto a branch held under a gate voids the gate the moment it is pushed (Secuura s135, KS-818, 2026-09-06 — caught before the push, cherry-picked off, the held ref verified unmoved). [M]
- **"No conflict markers" is not "resolved" — PARSE the result** — a conflict hunk can exclude lines COMMON to both sides, so keeping both sides drops them; a marker sweep and a block count both pass on a file that does not compile, and only the language's own parser (`tsc` on the file direct, a `node --check`, a `python -m py_compile`) discriminates; every hand-resolved conflict is followed by a parse of the resolved file before the counts are believed (added 2026-09-06 05:2x, credited to Secuura s135: the #834 rebase's first resolution left the ACCEPTANCE describe unclosed with a marker sweep at 0 and a plausible describe count; `TS1005 '}' expected` was the only signal). [M]
- **A log message, an error string or any emitted sentence is an INTERFACE to whatever asserts on it — a change to one runs the FULL gate, never the touched file alone, before READY** — an isolated run of the new suite is green over the sibling assertion that pins the old sentence; the full gate is what catches it (added 2026-09-06 05:4x, credited to Datasec/NexusAI S39: RD-338 changed the cap notice's wording and RD-337's own test pinned the old sentence; the isolated run could not see it, the full gate did, and the assertion was updated rather than loosened). [M]
- **A Jira `comment ~ "<hyphenated-slug>"` search is not a search for that slug** — the text index splits on hyphens and ORs the parts, so it returns the union and reports it as a match; ownership of a decision card by a ticket is established by READING the ticket's comments, never by that search, and a seat that greps by slug and reports "no owning ticket" is reporting the index, not the board (added 2026-09-06 06:2x, credited to Datasec/NexusAI S40: `comment ~ "nexusai-restore-path"` returned 20 tickets including three that mention nothing; every one of thirteen owners was confirmed by reading). [M]
- **One proof covers one shape — a claim about WHO IS AT RISK is red-proved separately from the mechanism it rests on** — a scratch-repo proof that a hook does not fire on a clean auto-merge says nothing about the hand-resolved merge, and a ticket that measures the mechanism then REASONS its way to the exposed population has filed a paragraph about a shape the proof never touched; both shapes are driven, with a counter, before the exposure sentence is written (added 2026-09-06 06:5x, credited to Datasec/NexusAI S40: RD-342's exposure paragraph was exactly backwards — the clean auto-merge, nearly every merge, is the unscanned case — and it measured both cases in one run and corrected the ticket ten minutes after filing it). [M]
- **A hand-maintained claim drifts fastest when the same author changes the behaviour it describes** — a prose sentence in a contract, a header, or a comment that describes a behaviour is re-read and rewritten in the SAME COMMIT that changes that behaviour, and the READY names every such sentence it touched; the test comment for a case being updated while the published description of the same case is not is the exact shape (added 2026-09-06 07:3x, credited to Secuura s136: KS-822's F-4 prose "filtered out, not refused" left standing two commits after F-5 made that case a refusal, in the artefact F-8 exists to protect, by F-8's own author). [M]
- **A finite, checkable set is enumerated into the corpus one case per member — and the enumeration is of the SHAPES, never of the instances in front of you** — a filter written from the two members in hand is the reader's recurring class (the RD-340 import-guard reader, fourth generation: `MemberExpression.property` and `Property.key` excluded, `MethodDefinition.key`, `PropertyDefinition.key` and labels forgotten); and a count of the instances in hand (118 of 118 files parsing under both modes) is a true measurement that answers a question nobody asked — the SHAPES (`with`, octal escapes, ESM) decided the parse order. Credited to Datasec/NexusAI S40, 2026-09-06 07:4x.
- **A control must not mutate its subject — and when the treatment and the control agree EXACTLY, suspect the harness before believing the result** — `git stash` / `git checkout` are disqualified as controls in a repo you are also building from, because the thing being measured moves under the measurement (a stashed build measured a post-prune tree, so the fix was compared against itself and read as a no-op); extract the comparison revision to a path OUTSIDE the working tree (`git show <ref>:<path> > <scratch>` and build from there); two variants that differ by a real change and produce byte-identical numbers are an instrument failure, not a finding — the same shape as a zero-result grep with no positive control (Secuura/Blockchain s138, 2026-09-06, KS-490 (2) / PR #851 — self-caught before the report; adopted by Wednesday 12:4x).
- **`ps` is not a liveness test for a sibling seat** — a Claude session spawns a shell only DURING a tool call, so a seat idle between calls is invisible to the process table; liveness is read from the daily note, the inbox and the pane, never from `ps` (Secuura/Blockchain s139b, 2026-09-06 — caught before it reached a decision; adopted by Wednesday 13:5x).
- **A secret-scan canary must be shown to FIRE before its clean means anything** — a canary built from a vendor's documentation example key pair reported "no leaks found" on a non-empty range; only a canary that produces a hit proves the scanner is reading the corpus, and the real scan's clean is unmeasured until then (QA agent, Secuura #847 re-check, 2026-09-06 — recorded, not quietly replaced; adopted by Wednesday 13:5x).
47. **A server-side PR merge pins the HEAD, not the BASE — with two seats live, merge by a LOCAL `--no-ff` onto the tip re-read and `git push origin HEAD:develop` (no force, no lease): a moved base makes the push REFUSE; the receipt names `first parent` beside `asserted` every time, and a gate's predicted merge-tree oid is a prediction against ONE base (a differing first parent invalidates the prediction, not the merge).** (Secuura seat A s139, 2026-09-06 04:30:42Z — #852 landed on #848's merge nine seconds after the assertion held; ruled by Wednesday 14:3x.)
- **A control proves the INSTRUMENT RUNS; it does not prove the QUERY CAN MATCH — those are two different failures and most controls guard only the first.** A sweep for which routes a suite pins searched for `wallet/status` and `wallet/authenticate`, returned 0 hits for both, and read as confirmation of a finding; the cells mount a router and call RELATIVE paths (`/status/${WALLET}`, `/challenge`), so **the search term could never have appeared**. The positive control (`describe`) proved grep ran — and therefore agreed with the null result for the wrong reason, making a false reading look verified. **The second control is a PLANT: write the thing you are searching for into the corpus and find it with the same command.** It surfaced only because 0 hits for `/status` CONTRADICTED the verdict's own claim that CONTROL 1 pins it, and the contradiction was chased instead of the agreement being banked. Corollary worth keeping: **an agreement between your result and the story is the moment to look for the instrument's blind spot, not the moment to stop.** (Secuura/Blockchain seat B s140e, 2026-09-06 12:49Z — self-caught, and it nearly reversed a finding; adopted by Wednesday 22:5x.) [M]
- **A MEASUREMENT travels; an EXPLANATION of it does not.** One green result (a tamper leaving a suite at 595/595) carried THREE successive mechanisms across three agents and every one was wrong — "pinned by nothing" (the route IS exercised), "the cell cannot tell two causes apart" (there is no second cause), and finally the measured truth (the suite `vi.mock`s the middleware to a passthrough, so the gate is deleted before any cell runs). **So a relay carries the RUNS and the LINE NUMBERS and no conclusion**, and the receiving agent re-measures before building on it. Corollary that cost the most here: **a fix-shape derived from a wrong mechanism can be a second check that cannot fail** — "assert a non-401 without a bearer" is green on the GATED route too when the gate is mocked away. (Secuura/Blockchain seat A s141b, 2026-09-06 12:55Z, in its own words; adopted by Wednesday 22:5x after making the same relay error twice on one finding in four minutes.) [M]
- **A RED that proves nothing is as blind as a green that proves nothing — and it is more dangerous, because red is the colour you were hoping for.** A tamper written as `authenticate` where the product uses `authenticate()` handed Express a FACTORY where middleware belongs; `next()` was never called, the request hung, and the suite went red on a 5000 ms timeout. It reddened for a reason unrelated to the hypothesis and was nearly banked as confirmation. **Every red-proof states WHICH assertion it trips and why, and a red that arrives by timeout, crash, syntax error or setup failure is NOT a red-proof** — it is the run failing to happen. The whole positive-control discipline has an unwritten second half and this is it. (Secuura/Blockchain seat A s141b, 2026-09-06 — self-caught; adopted by Wednesday 22:5x.) [M]
- **A WITHDRAWAL names the measurement it rests on and the SCOPE that measurement covered, inside the sentence that withdraws.** Twice in ten minutes on 2026-09-06 Wednesday retracted more than had been refuted — once removing a live finding (an unasserted `exec` premise, refuted only for a different claim), once removing a WORKING fix (a cell shape useless under `ks796`'s passthrough mock and valid under `ks720`'s gating stand-in). Both went out in an URGENT relay, which is the condition: speed is when a rule in memory does not fire, so the rule goes in the sentence. *"X measured this in ks796; I withdraw it for ks796 and do not know about ks720"* is one clause longer and preserves the fix. **An over-withdrawal replaces a precise useful statement with a vague safe one, and the vague one is what the next reader implements.** [W]
- **THREE WAYS A SEARCH LIES, and each needs a different defence — a positive control catches only the first.** (1) the command NEVER RAN (an unquoted `--include=*.ts` tripping zsh `nomatch`) → a true zero that is not a measurement; (2) the TERM COULD NOT MATCH the way the code is written (`wallet/status` against cells that call relative paths) → a real zero read as confirmation; (3) **the command ran, the term could match, and the OUTPUT WAS TRUNCATED** — `head -8` over eleven `vi.mock` calls hid the one at line 130 that carried the whole finding. A positive control catches (1). Checking the query against the data's shape catches (2). **NEITHER catches (3): COUNT FIRST (`grep -c`), or do not truncate a list you are about to call complete.** And the author's own closing line, kept because it is the point: **"naming a lesson does not install it"** — it had written (1) and (2) up itself earlier the same session. (Secuura/Blockchain seat B s140e, 2026-09-06 13:01Z; adopted by Wednesday 23:0x.) [M]
- **A hash proves the BYTES; only a RUN proves the file still works.** After restoring a tampered source by inverse edit and verifying sha256 back to the pre-tamper value, re-run the suite that file belongs to before calling the tree clean — a byte-identical restore of a file that was never valid, or a restore that silently landed in the wrong copy, both pass a hash check. (Secuura/Blockchain seat B s140e, 2026-09-06 — it re-ran ks720's seven cells green after the hash matched; adopted by Wednesday 23:0x.) [M]
- **A red-proof must EARN the cell, not merely exercise it.** A tamper that reds the new cell alongside its neighbours proves nothing about what the new cell adds: at one SHA all three readability cells red together, so that run could not show CELL 13 catches what CELLS 10 and 11 miss. The run that earns it breaks ONLY the guard the cell is for (12 passed, 1 failed, only CELL 13 red), and the INVERSE tamper (CELL 13 green) shows it is not merely sensitive to any break in the area. **Every gate brief asks for both from here.** (Secuura/Blockchain seat B s140e, KS-936 / PR #875, 2026-09-06 — it added both runs unasked because the ticket's requested run did not earn the cell; adopted by Wednesday 23:0x.) [M]
- **EMPTY OUTPUT IS NOT A RESULT — it is an ABSENCE, and an absence has at least two causes. Read the command's EXIT STATUS, not the shape of its output.** This is the ONE defence that catches all three ways a search lies (see the taxonomy below): the command never ran, the term could not match, and the output was truncated. Fourth instance the same session: `--reporter=basic` is not a valid vitest 4 reporter, so the runs exited with a STARTUP ERROR and produced nothing — read twice as "no output" and once misattributed to `console.log` suppression, in a mail to the coordinator. **The runs had not happened at all.** Wednesday's own instance minutes later, the same family from the other side: a `sed` whose delimiter appeared inside its pattern failed and wrote a ZERO-BYTE script, and `bash -n` on an empty file returns 0 — a syntax check that could not fail, caught only by grepping the content instead of trusting the status. **Capture `rc=$?` on its own line; never branch on the presence or absence of output.** (Secuura/Blockchain seat B s140e, 2026-09-06 13:13Z, in its own words; adopted by Wednesday 23:1x.) [M]
- **A CLAIM THAT DRIFTED FROM ITS GUARD IS FIXED BY NAMING THE GUARD, never by deleting the claim and never by leaving it** — and a fix that leaves it unlinked reproduces the defect in the act of fixing it. `wallet.ts` carried the comment *"A cell pins that the four stay open"* while no such cell existed for `/authenticate`; the remedy added the cell AND rewrote the comment to name the file that makes it true and to say why the cell cannot live in the suite that mocks its own subject away. **Watch the REMEDY specifically: this class hides there now** — twice on 2026-09-06 a fix nearly reproduced its own defect (a ratified fix-shape that would have added a second cell that cannot fail, and this comment). (Secuura/Blockchain seat B s140e, KS-942 / PR #878, 2026-09-06 13:22Z, in its own words; adopted by Wednesday 23:2x.) [M]
- **BOUND A READ BY THE STRUCTURE, NEVER BY A LINE NUMBER YOU GUESSED — the fourth way a search lies: you started reading in the MIDDLE of the thing you were measuring.** `sed -n '48,75p'` over an allowlist then a grep for `'/api/auth'` returned 0 hits, which would have supported "the prefix is not even declared public" — **the key was at line 47, one line above the slice**, and the string that did match was its REASON. The command ran, the term could match, the output was not truncated. Read from the structure's opening brace (`awk` between delimiters), not from an offset. **And the thing that actually caught it is the defence that works when all the mechanical ones pass: the zero CONTRADICTED something already known about the system** — a prefix allowlist with no `/api/auth` entry makes no sense against a gateway that proxies `/api/auth` wholesale. **Disbelieve a zero that disagrees with the architecture.** (Secuura/Blockchain seat B s140e, 2026-09-06 13:27Z; adopted by Wednesday 23:2x.) [M]
- **DEFENCE IN DEPTH CAN BE THE CONCEALMENT MECHANISM, not merely a complication — two reasonable guards can be WORSE than one, because one guard has a visible edge and two have an UNOWNED SEAM.** The gateway's auth gate reads the SPEC, so four routes are public at the edge only because their operations declare `security: []`; **one line of yaml closes a public route and THREE suites stay green** — one mounts the service router with the gateway out of the path, one works at MOUNT granularity with the whole prefix allowlisted once, and one never involves the gateway. Each is individually reasonable; the decision lives in a third place none of them reads, and their combined presence is what makes the gap look covered. **When two guards cover a surface, ask which one owns the DECISION — if the answer is neither, that is the finding.** (Secuura/Blockchain seat B s140e, KS-944, 2026-09-06; adopted by Wednesday 23:2x and relayed into the KS-926 campaign.) [M]
- **A GATE'S SUBJECT IS A SHA. While a PR is under an active gate, new work goes on a NEW BRANCH — or the coordinator stops the gate and relaunches it.** Twice on 2026-09-06 a builder pushed to a branch mid-gate and the verdict that arrived described a head the branch had moved past (#874 `fe5225f31 → bea418b02`, #876 `af954c691 → ff7704135`); the second cost a tier-1 pass on a superseded head. **The coordinator holds the only view of which panes are gating what, so any instruction that could cause a push NAMES the gates currently running against that branch** — the builder cannot weigh what it is not told. And a verdict is a receipt about a SHA, never about a PR: re-read the verdict's own target line against `ls-remote` before merging on it. (Wednesday's own failure, 2026-09-06 23:3x, self-caught after the fact and after the same shape had already been reported by the #874 tester an hour earlier.) [W]
- **A REPRODUCTION BUILT FROM THE MOUNT LIST IS SYSTEMATICALLY MORE PERMISSIVE THAN THE PRODUCT — build it from the ROUTE REGISTRATION.** The agent's own words after the third instance in one session: **"I left out the middleware that would have said no."** Its reproduction of the gateway omitted `authenticateToken(true)` at `proxy.ts:327`, which made an MFA bypass look reachable unauthenticated when the real gateway 401s it — it corrected its own finding DOWNWARD, unprompted, in the same mail that confirmed the bigger half. **And the paired rule: a harness that answers 200 for the row you want must be shown to answer NO for something** — four refusals in the same batch (an unmounted route, an unmounted route with the same odd spelling, a wrong prefix, and the canonical spelling under an exhausted limiter) are what make one 200 a finding rather than the instrument's default. **That control also CHANGED the finding's shape**: a double slash on its own produced nothing, so the defect is the interaction between an extra slash and a real mounted prefix whose strip normalises it AFTER the guard — not "double slashes are magic" — which rules out the obvious platform-wide fix. (Secuura/Blockchain seat B s140e, KS-946, 2026-09-06; adopted by Wednesday 23:5x.) [M]
- **A PRE-STATED CONDITION IS AN INSTRUMENT AND IT CAN BE BROKEN — so REPORT THE RAW VALUES, ALWAYS, whatever bucket your own condition puts them in.** Stating a FAIL condition before running is right and stays required; **it is not sufficient**, because the condition is written before you know what the system can do. A demo probe pre-declared *"NULL RESULT — not live — BOTH spellings carry the headers"*; both spellings DID carry headers, so read literally the condition said CLEAN — and the truth was the opposite, because a DIFFERENT limiter answered for the missed mount and supplied headers of its own. Presence was the wrong discriminator; the header's VALUE was the right one. **The only thing that saved it was the brief's separate requirement to print the raw result either way** — the values were on screen and they contradicted the agent's own bucket, and it said so rather than re-filing quietly. **So: every probe reports the RAW MEASUREMENT beside its verdict, and a verdict that disagrees with its own raw values is a finding about the instrument, not a result about the system.** (Secuura/Blockchain seat s143, the authorised demo probe, 2026-09-07 06:5x — self-disclosed; adopted by Wednesday the same action.) [M]
- **A SAFETY TIE-BREAKER PROTECTS ONE DIRECTION AND BIASES THE OTHER — put a control on the SAFE side too.** When a criterion says *"if you cannot measure it, take the safer option"*, it is armoured against a false GO and wide open to a **false NO-GO**, and nothing in it points at contamination. A builder's first before/after baseline was polluted by an earlier probe's exhausted limiters; it would have shown six changed rows and produced a confident NO-GO on a correct fix. It took a FRESH boot for each side instead and said why. **A baseline is inherited state until proven otherwise: for any before/after comparison, take a fresh baseline per side and name which run each number came from.** (Secuura/Blockchain seat s143, 2026-09-07 06:4x — its catch, on a criterion Wednesday wrote; adopted the same action.) [W/M]
- **WHEN A GUARD KEEPS FAILING IN THE SAME PLACE, READ ITS OWN COMMENT AGAINST ITS CODE BEFORE PROPOSING A FIFTH FIX — the recurring bug is usually the gap between what the file SAYS it does and what it does.** `check-shared-relink.sh` took FOUR gate rounds, each closing a false clean and leaving another. Its exemption arm's own comment said the exemption is *"granted on POSITIVE readings, never on the absence of a parse match, because absence is exactly what an unreadable write looks like"* — and the implementation was four DENY arms with a catch-all `else` that GRANTED. **All four rounds were bugs in that one doc-vs-code gap.** Inverting was not a fifth change of direction; it was the first time the code did what the file already claimed. **The general rule for choosing between narrowing and inverting: both need a list, and the question is only WHICH WAY AN INCOMPLETE LIST FAILS.** An incomplete DENY-list of spellings ships the artefact you did not enumerate, green — here `${REGISTRY_PREFIX}node:24-alpine`, **56 of 79 FROM lines in the repo**. An incomplete ALLOW-list gives the author a red naming their image, and they add it in a reviewed change. **That asymmetry is the whole argument.** **And a path/file ALLOW-LIST is the wrong instrument for an artefact property** — Wednesday recommended one and was refuted with evidence: an ACL over paths goes stale as files move or are copied, it is the same species as the hand-maintained census this very file's banner forbids (and which had drifted, 5/20 stated vs 4/21 derived), and it answers the wrong question — the risk is *does this image ship a JS runtime*, not *where does this file live*. **Ask what property actually carries the risk, and put the list on THAT.** **Finally: inverting is only safe once you have measured who reaches the arm.** The exemption had ZERO consumers on the real tree (all 25 class files write node_modules, so none reaches it), proved by byte-identical guard output across all 25 before and after. (Secuura/Blockchain seat s143, 2026-09-07 — its answer to Wednesday's breadth question, correcting Wednesday's own lean; adopted verbatim, and it supersedes Wednesday's weaker "an exemption on a blocking clause is a hole by construction" line written the same morning.) [M]
- **AN INSERT THAT DISPLACES AN ANNOUNCED "NEXT" NAMES WHAT IT DISPLACES AND WHEN IT RETURNS — and the coordinator re-reads the displaced item's STATE before writing it into a handover as in-flight.** A seat announced *"#882 round 1 next"* in two separate mails and never started it; Wednesday inserted higher-priority work four times, listed #882 as in-flight in a handover a successor would have trusted, and discovered it was **untouched — zero commits, branch unmoved** — only by asking rather than assuming. **A queue item is a record of what was SAID, not of what was STARTED**, and the state is one `ls-remote` away. The agent's own framing is the rule: *"the net effect is that the thing I twice announced as next has never been started, and that is worth saying plainly rather than letting 'next' keep meaning 'not yet'."* **Related and not a coincidence: an announced next is also where the turn-end stall lands** — both of that morning's stalls happened immediately after the seat named its next item. (Wednesday's own failure, 2026-09-07 07:47, self-caught by asking; the seat's attribution — that every displacement was the coordinator's insert and none was its own reordering — verified and accepted.) [W]
- **AN APPROVAL THAT WILL PRODUCE A PUSH NAMES THE REPOSITORY IT LANDS IN — the destination is a fact the coordinator holds and the principal does not.** Kam approved an Attio schema change on its merits (one attribute, the cap lifted by exactly one) and was later surprised that the resulting commits went into the **Datasec** GitHub organisation. His words: *"I approved ATO push, but did not realize that this was going to the Datasec repository. This cannot happen in the future."* **Every artefact in the chain described WHAT changed and none named WHERE it would land** — not the card, not the brief, not the dry-run review, not the GO. **Rule: any card, brief or GO whose consequence is a commit states the remote (`git@github.com:org/repo.git`) and the branch, in the BLUF, before the approval is given.** The same applies to a deploy (which environment, which subscription) and to a ticket (which board). **The principal cannot object to a destination nobody showed them**, and "it followed the existing arrangement" is not consent — it is precisely the thing an approval is supposed to interrogate. (Kam, 2026-09-07 09:04, on the ATTIO push; the arrangement was 17 days and 51 commits old and matched every other Datasec project, which is context and not a defence.) [W]


- **WIDENED THE SAME DAY (w=2, 10:2x) — THE RULE ABOVE IS ONE COSTUME. THE CLASS IS: ANYTHING WEDNESDAY COMMISSIONS NAMES THE FIELD THAT DECIDES WHOSE IT IS, NOT ONLY WHAT WILL CHANGE.** Hours after the ATTIO line was written, Wednesday delegated ticket SELECTION to the Secuura seat (s145) with a five-clause rule — priority, no client-human INPUT needed, no file under gate, not already In Review, closable in a session — and **never named the ASSIGNEE field.** The seat applied the rule correctly and committed to **KS-61, which is assigned to Stuart.** Kam had already ruled this exact point on 2026-09-06 10:24: *"once something is assigned to someone it belongs to them. the ruling was only to new or unassigned items."* Caught by Wednesday reading the seat's pane minutes in; stopped before any push, comment or reassignment, and the seat's derivation work quarantined rather than reverted. **Why the ATTIO line did not fire: it says "whose consequence is a COMMIT" and names "the remote and branch". A selection rule's consequence is not a commit — it is taking someone's ticket — so the promoted line was scoped to one costume and this was another.** That is [[2026-08-13_headline-must-match-the-operative-case]] operating on an enforcement line: the handle said *commit* and the field was *assignee*.
  **THE RULE, IN ITS GENERAL FORM — this supersedes nothing above, it contains it:** every card, brief, GO or delegated RULE states, in its BLUF, the field that decides **whose the thing is and where it lands**, for whatever it commissions:
  - a **commit** → the remote and the branch;
  - a **deploy** → the environment and the subscription;
  - a **ticket** → the board **and the assignee**;
  - a **selection rule handed to an agent** → the **ownership predicate** ("unassigned, or on Kam's account; never Peter's or Stuart's"), because a rule that filters on *difficulty* while omitting *ownership* will find the borderline item on its own;
  - a **message to a human** → who sends it (Kam) and on which channel.
  **Test by its handle:** read only what the artefact says will change. If a reader could not answer *"and whose is it?"*, the field is missing. [W]

## TICKET CREATION — the unit of a ticket is the TEST PASS (Kam, 2026-09-07 13:23, verbatim)

> *"if a single test is required, we should be creating one ticket with multiple items inside it
> rather than multiple tickets. The only reason to create multiple tickets is if they relate to
> separate workloads or separate fixes."*

**The predicate, stated so it can be applied without judgement:** **if ONE test pass proves the
whole thing, it is ONE ticket** — its items as a checklist or sub-issues inside it. **Split only on
a separate WORKLOAD or a separate FIX**, never because findings arrived separately, were found by
different passes, or sit in different files.

**This SHARPENS his 2026-09-06 09:42 aggregation ruling** (*"rather than creating three or five
separate tickets, create one larger ticket… within a logical path"*) by naming what "a logical path"
actually is: **the test pass**. It is the same criterion he already set for the REVIEW side
(handovers to Peter and Stuart are TEST BLOCKS, cut by what one pass proves), so **creation and
review now use one predicate** — which is why a stream built this way needs no re-grouping later.

**Standing line for every brief that may create tickets:**
> *"Ticket creation aggregates on the TEST PASS: if one test proves it, it is one ticket with its
> items inside. Separate tickets only for separate workloads or separate fixes — never because the
> findings arrived separately."*

**The check before filing N tickets:** *could one pass prove all N?* If yes, it is one ticket and you
are about to make the reviewer read N times. If no, name the distinct workload or fix per ticket in
its first line.

## FILING A FINDING — a control proving "not mine" does not prove "not filed" (2026-09-07)

**Found by a board catalogue pass:** one guard failure filed **four times across 31 hours**. Every
session ran a control and correctly proved the red pre-dated its own work. **None searched the board
first.** Five findings, fourteen tickets, on one board.

**Standing line for every brief:**
> *"Before filing any finding, search the board for it BY SYMBOL, FILE PATH OR ERROR STRING — never
> by your own phrasing, which is what differs between sessions describing one failure. State the
> search in the ticket ('searched `<symbol>`, 0 open hits'). A control proving a red is PRE-EXISTING
> is half the check; the other half is that it is UNFILED. If it is already filed, add your evidence
> to that ticket rather than opening a second one — two independent proofs of one red are stronger
> than two tickets."*

**Why it belongs in the path and not in an agent's memory:** a duplicate is only visible from OUTSIDE
the session that files it. Inside one session the loop is flawless — red → control → not mine → file.
Nothing in that loop can surface the other three.

## BRANCH NAMING — the rule has TWO directions (2026-09-07, both learned in one day)

**Direction 1 (morning, from a real mislabel):** *name a branch from a ticket that EXISTS, never from
a guessed position in the sequence.* A seat guessed the next id, named the branch, and #888 now
carries `ks-964` while meaning `ks-966` — corrected in the PR title and body, history NOT rewritten.

**Direction 2 (afternoon, and it is the one nobody would think of):** **sometimes the ticket id must
be LEFT OUT of the branch name on purpose.** A seat fixing the KS-418 documentation defect named its
branch `docs/nightly-schedule-true-reason` **specifically because `ks-418` in the branch name would
have transitioned PETER'S ticket** through Linear's GitHub integration — the same integration that
silently moved KS-964 to `In Progress` that morning.

**The rule, stated once so both directions follow from it:**
> **A branch name is an INSTRUCTION TO THE BOARD, not a label.** Linear's integration reads it and
> moves the ticket. So: name it from a ticket that exists AND that you are entitled to move. **If the
> ticket belongs to a client human — Peter, Stuart — keep its id OUT of the branch entirely and put
> the reference in the PR body instead**, where it links without transitioning.

**Test by its handle:** *"if this branch name moves a ticket, is that ticket mine to move?"* If no,
the id does not go in the name.

## CLEANUP DURING A DEPLOY — a just-built artefact reads as UNUSED until the thing that uses it restarts (2026-09-07)

**Found by a seat mid-deploy, unprompted, and it is the reason a disk-space guard must never delete:**

> *"Do not prune images to make room — the freshly built ones read as unused until `up -d` recreates
> the containers, so a prune deletes this deploy's own output."*

**The general shape:** cleanup tooling decides liveness from REFERENCES, and **a deploy is precisely
the window in which the references have not caught up yet.** A freshly built image, a new layer, a
staged artefact, an unadopted volume — all of them look like garbage to a reaper until the consumer
is restarted to point at them. **So the moment you most need space is the moment automated cleanup is
most likely to destroy the thing you just made.**

**Standing lines for any brief involving a build, a deploy or a disk constraint:**
> *"NEVER free space on a live box on your own judgement — a stalled deploy is recoverable, a box you
> cleaned up is not. A disk guard STOPS the build and escalates; it does not delete. And specifically:
> do NOT prune images or build cache during a deploy — the artefacts you just built read as unused
> until the consumer restarts, so the prune eats your own output."*

**Also standing, from the same handover:** **`docker compose up -d --remove-orphans` is a destructive
flag on any host running profile-gated services** — containers outside the active profile read as
orphans and are removed. Name the forbidden flag in the brief; do not rely on it not occurring to
anyone.

## WAKERS AND WATCHERS — two rules an agent found in its own monitor, 2026-09-07

**RULE 1 — a waker must be able to observe the FAILURE it exists for.**
A seat built a waker that exited on the build's `=== DONE` marker. **Its disk guard stops the build
with `pkill`, which never writes that marker** — so **the one event it most needed to hear about
would have left it asleep indefinitely.** Its own words:

> *"A watcher that cannot observe the failure it exists for is a check that cannot fail, wearing a
> monitor's clothes."*

**The corrected shape, and it is the general one — wake on THREE classes, not one:**
1. the **success** marker;
2. the **explicit failure** marker (the guard's own stop file);
3. **the watched process DISAPPEARING without either** — *"because the first two are both things that
   WRITE something; a process that dies writes nothing."*

**Test by its handle:** *if the thing I am afraid of happens, does this waker fire?* If the only
answer is "it would write a marker", ask what happens when it cannot.

**RULE 2 — a backgrounded task that backgrounds again is ORPHANED, and it reports success.**
The seat's first fix wrapped the harness's background mode around a command that itself ended in `&`.
**The outer shell exited immediately, the harness marked the task COMPLETE, and the loop kept polling
with nothing left to wake.** *"It reported 'started' and was inert."*

**It caught this by DURATION: the task completed in under a minute, which is not what a 90-minute
watcher does.** **Standing check: after starting any long-lived background task, verify it is still
running at a time when it should be** — a task that finishes far too fast has not finished, it has
detached from you. Never `&` inside a tracked background task; let the loop be the foreground of it.

**RULE 3, from the same seat and worth as much as the other two:** **when a waker fires on a
condition that requires a JUDGEMENT, it prints the instruction alongside the alert.** Its
`GUARD_STOPPED` branch prints *"mail Wednesday, do not clean up the box"* — *"I did not want that
decision resting on my memory at the moment it fires."* **The moment an alert fires is the worst
moment to be recalling policy.**

---

## SEARCHING THE BOARD BEFORE YOU FILE — run BOTH search kinds, and the noisy one earns its keep
*(Secuura/Blockchain seat, 2026-09-07 20:29, in its own terms; sharpens the M-tier rule filed the
same morning in `2026-09-07_a-control-proving-it-is-not-yours-does-not-say-who-filed-it`.)*

That morning's rule said: **search by SYMBOL, PATH or ERROR STRING — never by your own phrasing of
the problem**, because the phrasing is exactly what differs between four sessions describing one
failure. **True, and it implied the fuzzy multi-word search is the weak one to avoid. It is the weak
one to RUN ANYWAY.**

Measured on Linear's `searchIssues`: **symbol searches DISCRIMINATE** (`scopeField` and
`boundedByCodePoints` → 0; `rateLimitScope` / `explicitScope` / `principalScope` / `maxLength` →
KS-970 only, with a `KS-970` control returning non-zero to prove the search itself works). **Phrase
searches return noise** — `"Caller has no tenant"` and `run-migrations.sh` each returned ~20 loosely
related hits.

**And the noise is what caught the duplicate.** **KS-808** — already open, in Backlog, carrying the
defect **verbatim in its own title** — was found through the noisy `run-migrations.sh` result, not
through any exact search.

**The rule:**
1. **Run the exact searches to DECIDE (symbol, path, error string) and the fuzzy one to DISCOVER.**
   They have different failure modes; an exact search cannot find a ticket that named the thing
   differently, which is the whole reason duplicates exist.
2. **Run a control that returns non-zero**, so a clean zero is one you can vouch for.
3. **State in the ticket what you searched and what each search returned** — that line is cheap and
   it makes the absence checkable.
4. **A match your "0 open hits" did not predict gets OPENED, not waved past.** The same seat checked
   a `checkRateLimitSchema` hit on KS-645 that looked like a match and established it was a closed
   Duplicate about a different route.
5. **If it IS already filed, add your evidence to that ticket and write the reason ON it** — never a
   second ticket, and never the reason only in a reply, or the next sweep re-derives the same wrong
   disposition from the same title.

## A FIX SPECIFIED BY A STRING IS SCOPED BY THAT STRING — count the sites before you name the fix
*(same seat, same mail, and it is an implementation hazard the gate did not name.)*

The finding said a refusal message *"names the wrong thing"* at two sites. **The string
`"Caller has no tenant"` occurs at FOUR**, and **two of them are CORRECT**: `index.ts:665` and `:716`
guard `if (!isPlatformRole(...) && !callerTenantId)` — they test the tenant claim **directly**, so
the message is literally true there. Only `:1267` and `:1377` sit behind `if (scope === null)`, which
is null for three different reasons.

**The rule:** before accepting or writing a fix described by a STRING, a message, a symbol or a
pattern, **count its occurrences and classify each one** — a `grep`-shaped fix has a `grep`-shaped
blast radius, and a finding that names two instances has said nothing about the others. **Pin the
sites that must NOT change with a regression cell**, so the boundary is a property of the suite
rather than of whoever writes the fix.
