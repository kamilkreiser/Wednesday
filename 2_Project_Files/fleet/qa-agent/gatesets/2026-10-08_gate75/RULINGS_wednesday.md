# gate75 — RULINGS for Wednesday (drafted 2026-10-08 ~12:28–13:15 AEDT, NOT launched)

Every OPEN question carries the drafter's recommendation and a DEFAULT. The default is what the kit and the R 17th brief DRAFT already assume, so ruling "as recommended" changes no file. **None of them blocks the launch** (the dry run reached rc 0 with every one at its default). Q-KEYS75 and Q-BUILDER75 bind the merge seat, not the gate.

## CARRIED (binding on the gate, written into the prompt)

- **R1 TIER.** #1426 is T2, a guard change. The red-proof is the heart of it: every arm R 16th ran is re-driven at the head, plus the commission's new arms, by `c3_guard_gate75.py`.
- **R2 ACTIONS.** The three classes, SUBSET (never equality), PENDING never a pass, a 0-runs comparator re-read. The comparator is `base`. **base == develop == ddea005553bf at draft, so develop / base / union are ONE sha** and no comparator ruling is owed while develop is unmoved.
- **R3 PRE-EXISTING MISMATCH.** The three files are base-state (gate73 R3). c1 P13 confirms them byte-identical at base, head and develop.
- **R4 PLATFORM SUITES.** Schemathesis, Akto, Playwright and Performance (k6) are UNMEASURED locally (stack down). They are never counted as passing.
- **R5 MERGE SEAT.** The next R seat: `kit.json merge_seat = Secuura/Blockchain-R`, ordinal `Seat R 17th`. It is never the author (Seat R 16th), and the launcher refuses the author by name.
- **R6 CONTROLS.** Every control must be able to fail. A zero gets a positive control. Every arm is read by one parser.
- **R7 RESTORE TO THE HEAD STATE.** This is R 16th's fault, made a rule. Saved bytes are written back and re-asserted equal to the HEAD blob. Planted files are quarantined. `checkout`, `restore`, `reset` and `clean` are never used.
- **R8 A5 = THE RULED NAMED LIMITATION** (your ANSWER_A5, ruling (i)). A bare marker inside a quoted value reads GREEN. KS-1451 owns it. The gate reports it as the limitation, never as a pass.
- **R9 LEG 14 / no `--no-verify`.** A landing that needs a push is a STOP.

## OPEN QUESTIONS

**Q-SEAT75 — confirm the ordinal.**
- `merge_seat_ordinal` = `Seat R 17th`. The rendered GO string is `GO (Seat R 17th): merge 1426 on gate75`.
- *Rec / default:* confirm. If another seat boots, change kit.json and re-run the repin. It re-renders the string, and the launcher checks it.

**Q-TRAILER75 — the BRANCH commit carries `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.**
- Measured: c1 P5/P6 read 55 raw trailer bytes and 1 Co-Authored-By line. The reader is non-blind: control `bf277eead268` reads 55 B too.
- This breaks STANDING_LINES :371 ("keep branch commits trailer-free too, so the claim holds whatever GitHub does"). R 16th made no claim either way.
- Fixing the branch commit needs a rewrite and a force-push. Both are forbidden.
- *Rec / default:* **non-blocking (Minor).** What lands is the squash. The merge seat sends an explicit body, asserts it trailer-free BEFORE the API call (`mergera1.py` / builder), and X-7 asserts the LANDED commit has 0 trailers with the non-blind reader.
- Also put a line in R 17th's handover: raise seats keep branch commits trailer-free. R 16th's commit tooling added one.

**Q-KEYS75 — which keys does the landing hyphenate? It binds the merge seat (mergera1 requires `own_keys` == the live PR body's `Refs` set; the builder requires the subject to open with exactly the own keys).**
- Live PR body: `Refs KS-1450 · Refs KS-1451`. It also hyphenates KS-1386 (Peter's, Done) and KS-1401 (#1383's). Per STANDING_LINES :278, they ATTACH from a PR body.
- **(a)** own = {KS-1450}. R 17th PATCHes our own PR's body ONCE to the staged DRAFT `merge_inputs/1426.pr_body_keys_dehyphenated.DRAFT.txt`:
  - 10,094 B, sha256 `a36e00f5265b49f62f6121207e2cddeb6f019d3c3af280d2c7bc4cde435bb07a`;
  - four mechanical edits, each count asserted: `Refs KS-1450 · Refs KS-1451` → `Refs KS-1450`, and KS-1451 / KS-1386 / KS-1401 de-hyphenated;
  - after them the hyphenated set is {KS-1450}, with 0 closing words, 0 `Merged by` and 0 Co-Authored-By.
  - R 17th reads it back by sha256 and uses it VERBATIM as the squash body. This is the Q-1422-REFS precedent (R 15th, one PATCH).
- **(b)** own = {KS-1450, KS-1451}, with no PATCH. The subject must then open `KS-1450, KS-1451: …`, which reads as if KS-1451 were addressed. It is not. KS-1386 and KS-1401 would still need de-hyphenating in a separate squash-body file.
- *Rec / default:* **(a).** It is one GitHub write on our own PR, and it also stops the live PR from attaching Peter's KS-1386.

**Q-SUBJ75 — the squash subject.**
- The PR title is 101 chars and the head subject is 73 chars. Both are NON-ASCII (U+2014), so neither can be the squash subject.
- *Rec / default:* `KS-1450: unblock preflight leg 14 - mark baseline reasons, exempt provenance run ids`.
  - It is 84 chars, ASCII, carries no `(#`, and opens with the own-key list then `: `.
  - It is true of the diff, which also adds a membership cell and two doc clauses (a subject summarises). The gate may re-declare it; its wording wins.

**Q-BUILDER75 — R 15th's builder cannot express this landing as copied. The tool wins; this needs your spec.**
- `build_addendumra15_gate74.py` is sha256/16 `95087d4c791e221c`, 328 lines (R 15th's `merge/`, re-hashed by the drafter). It knows `RA15_LANDING=behind|on-develop|merge-in`, so `on-develop` fits: PARENTS == [D].
- Its `RA15_DOCS` is `merged|none`, and neither fits #1426:
  - **`merged` REFUSES**, because it asserts head doc blob != the GO's merged blob (:207). Here develop never touched the docs, so merged == head (c4 M2: `576a4687c995` / `3481baae3dd9`).
  - **`none` REFUSES**, because the PR touches both docs (:216).
- The builder also hard-codes the GO-clause regex to `Seat R 15th` (:126), and its predecessor tuple (:262-264) ends at `Seat R 14th` and asserts `Seat R 15th` ABSENT (:266).
- *Rec / default:* R 17th writes a NEW COPY, `build_addendumra17_gate75.py`, and never edits R 15th's. The copy:
  - keeps every inherited assert;
  - re-keys `RA15_*` → `RA17_*`;
  - re-keys the GO-clause regex to `Seat R 17th`;
  - extends the predecessor tuple with `Seat R 15th` (it merged #1422/#1423, so its claims sit in develop's history) and `Seat R 16th` (it AUTHORED #1426, so a `Merged by Seat R 16th` would be false);
  - ADDS `RA17_DOCS=head`. This asserts that the GO carries `flow`/`cheat` lines equal to the HEAD blobs, that each target == head blob == the blob in T', and `merged_blob_paths == []`.
- Arms, each of which must REFUSE: `head` with a GO blob != the head blob; `merged` on this PR (the inherited refusal); `none` on this PR; a GO clause naming R 15th; a body planted with `Merged by Seat R 16th`; `RA17_LANDING=behind` on this PR (its parent is D, not an older B).
- Then the chain: builder → `mergera1.py --dry` → READ the `.DRY` body.

**Q-GAP75 — two GREEN arms that are not the ruled A5: the exemption is wider in two ways than its words say.**
- **A4v:** a REAL `from_runs` VALUE copied into a new array of the baseline is exempted SILENTLY. The membership check is `index($v)` on the value, not the element's position.
- **N4v:** a NEW file at another root whose path ENDS in `/schemathesis/config/schemathesis-baseline.json`, holding a real `from_runs` value, is exempted SILENTLY. `PROVENANCE_LINE_RE`'s path part is an unanchored SUFFIX.
- What escapes either way is an already-recorded run id, not a typed target. The novel-value forms are caught (A4, N2, N4, all RED on MEMB only).
- Three texts state more than the code does:
  - the guard comment :48-56 ("in THAT ONE FILE");
  - the PR body ("in that one file", "every line the exemption drops really is a from_runs member");
  - both doc clauses ("exempt in that one file", "a guard cell asserts every exempted line really is a `from_runs` member").
- *Rec / default:* **Minor, non-blocking.** Correct the WORDING in the KS-1450 comment before it is posted (client-facing correction rule). Record the docs/comment overstatement as a named follow-up of OURS. The natural home is KS-1451's change, which already edits this guard's marker test: anchor the path at the scan base and bound membership by position, after which the doc clause becomes literally true. No new ticket without your word.
- If you rule it Major, the fix is a new commit on the branch (a new head) and a re-gate.

**Q-COMMENT75 — R 16th's DRAFT KS-1450 comment cannot be posted as written. The drafter's reading follows; the gate re-reads it sentence by sentence.**
- **(a) DOES NOT HOLD:** "only in `schemathesis/config/schemathesis-baseline.json`". The filter matches a path SUFFIX (N4/N4v).
- **(b) DOES NOT HOLD:** "every line the exemption drops really is a `from_runs` member". It is VALUE membership (A4v).
- **(c) DOES NOT HOLD as worded:** "all red with their own reason, each reading one failed cell". The drafter's A8 (jq shim exit 127) reads 9p+2f, because the non-vacuity control also needs jq. R 16th's own shim may have differed; the gate decides.
- **(d) DOES NOT HOLD:** "Full preflight run by hand (this push is systemTest + docs only, so the hook does not run it)". R 16th's OWN READY mail, PR body and handover lesson 4 say the hook DID run it in-hook (340 s): a first push of a new branch has no computable base, and `.githooks/pre-push` fails safe. The sentence is a leftover from the brief's wrong premise.
- **(e) DOES NOT HOLD:** "the same `\s*\S` shape is in at least four other harness guards, whose own bare-marker controls pass only because each plants into a comment at end-of-line". The drafter found:
  - the literal shape in the akto and playwright guards only;
  - a `.split(...)[1].strip()` test in the schemathesis guard (the same class);
  - in the performance guard, `line.includes(MARKER)` with NO reason test, so a BARE marker exempts even a `.ts` comment line. This was probed on the predicate in isolation, not on the suite. That guard also has no bare-marker control.
- **(f) HOLDS:** "exactly 2 existing marker lines repo-wide", under the predicate `slot-literal-ok:[[:space:]]*[",]` (2 at head, 2 at develop).
- *Rec / default:* the gate writes the CORRECTED text. R 17th posts that text, re-read against the MERGED head, as its ONLY board write. Peter is told, not asked (your 10:45 rule).

**Q-CLAUDEMD75 — `systemTest/CLAUDE.md:1166-1169` describes this guard with ONE exception mechanism (the marker), and this PR adds a second.**
- That paragraph is unchanged (c1 P10: `systemTest/CLAUDE.md` byte-identical base == head). Skill §5e routes systemTest docs to that file.
- *Rec / default:* **Minor, non-blocking.** Fold it into KS-1451's change, which must edit :1169's "a bare marker exempts nothing" anyway. The gate rules whether §4/§5e makes it owed in THIS commit.

**Q-5D75 — §5d: the six JSON `reason` lines carry no WHY + ticket comment (JSON has none).**
- *Rec / default:* polish. The marker text is the WHY, and the guard's comment block names KS-1450.

**Q-KS1451-SCOPE — not the gate's question, and it needs a Linear read (the drafter has none).**
- If KS-1451's body says the `\s*\S` shape is in all five guards, (e) above shows that is inaccurate. The performance guard's gap is wider: no reason test at all.
- *Rec:* you read KS-1451 at send time and, if needed, correct it with one comment. That is OUR ticket, so the correction is ours. It is NOT R 17th's work.

**Q-PREFLIGHT-BUDGET75.**
- While develop is unmoved, the SIM tree IS the head tree. The gate builds the SIM commit, asserts tree equality, and runs ONE preflight (head, ~6 min, ~1.6 GB of installs). A develop-side preflight is optional, because develop's figures are on record and CI corroborates them.
- *Rec / default:* accept.

**Q-USAGE75.**
- The gauge read **96%** at the drafter's dry run (`usage_gate.sh --check` at `WED_USAGE_STOP=100`, rc 0).
- The repin passes `WED_USAGE_STOP=100` ONLY after reading `0_Brain/learnings/2026-10-08_use-to-100pct-raise-gate-merge-seats-only.md`. It requires `status: live`, card `secuura-usage-89pct-raise-backlog-1008` and the gate clause, and refuses rc 12 otherwise.
- The grant ends at the weekly renewal (~Sun 11 Oct): an EVENT, never inferred.
- *Rec / default:* as wired.

**Q-BASELINE-NOTE (no ruling; named).**
- The baseline's `$generated.note` says "Regenerate by re-running this union … do not hand-edit". The PR hand-edits six `reason` strings and leaves `$generated` untouched (c1 P15: `from_runs` equal as parsed JSON).
- The drafter reads the note as being about the run union, not the triage prose. Named so the gate can disagree.

## WEDNESDAY'S RULINGS — (to be written by Wednesday)

Ruled by Wednesday, 13:06 AEDT, after reading KIT_REPORT.md (226 lines) and this file WHOLE:
- **Q-SEAT75:** confirmed, `Seat R 17th`.
- **Q-TRAILER75:** as recommended, non-blocking. The merge seat asserts the sent body and the landed squash carry 0 trailers; a line in R 17th's handover says raise seats keep branch commits trailer-free.
- **Q-KEYS75:** (a). Own = {KS-1450}; one PATCH of our own PR body to the staged draft, read back by sha256.
- **Q-SUBJ75:** as recommended; the gate may re-declare it, and its wording wins.
- **Q-BUILDER75:** as recommended. R 17th writes a new copy `build_addendumra17_gate75.py` with `RA17_DOCS=head` and the six refusal arms; R 15th's builder is never edited.
- **Q-GAP75:** Minor, non-blocking for THIS merge. The gate confirms or overturns. The KS-1450 comment's wording is corrected before posting. Under Kam's 10:45 rule ("we fix our own problems"), the two gaps (value membership, path suffix) plus the doc and guard-comment overstatement are OUR follow-up: they go into KS-1451's change, which already edits this guard. If the gate rules them Major, that stands: a new commit and a re-gate.
- **Q-COMMENT75:** as recommended. The gate writes the corrected text; R 17th posts it after the verified merge, as its only board write. Peter is told, not asked.
- **Q-CLAUDEMD75:** Minor; it folds into KS-1451. The gate rules whether §4/§5e make it owed in this commit.
- **Q-5D75:** polish.
- **Q-KS1451-SCOPE:** Wednesday reads KS-1451 at R 17th's send.
- **Q-PREFLIGHT-BUDGET75:** accepted, one preflight at the head.
- **Q-USAGE75:** as wired. Authority: Kam's 09:17 grant (gate class).
- **Q-BASELINE-NOTE:** noted; the gate may disagree.
