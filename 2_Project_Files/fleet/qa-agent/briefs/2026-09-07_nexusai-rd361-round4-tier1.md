# QA GATE — Datasec/NexusAI RD-361 **ROUND 4**, `rd-361-round4-s45` @ `400718f`. **TIER 1.**

## Why this round exists, and what that means for your bar
Rounds 1, 2 and 3 all NO GO'd on the same Blocker. **Kam capped this class at two rounds, bent his
own cap for round 3, and then authorised round 4 explicitly.** Round 3 failed because its
discriminator (`firstRunComplete`) has **three FRONTEND writers unrelated to auth** — the previous
gate's own first-hand finding. **A NO GO here does not open a round 5. It goes to Kam.** So the bar
is: be right, and be right about what you did *not* establish.

**This round changed shape mid-flight.** Wednesday told the builder that no content discriminator
could work and instructed it to try to falsify that first. **It did, and Wednesday was wrong** — the
builder found `authEnforced_updated_at`, a companion key stamped by `setSetting`
(`backend/jsonStorage.js:1865`) on the same write, which survives deletion of `authEnforced` itself.
The planned `/api/auth/enforce` carve-out was withdrawn. **Wednesday ratified the SHAPE of that
reasoning and explicitly did NOT ratify its correctness in the product. That is your question.**

## 1. Target — the SHAs, and what each one is for
    400718f   rd-361-round4-s45   THE SUBJECT. Parent 2f4896d, single commit, pushed.
                                  Verified by Wednesday with `ls-remote`: 400718fecf0b2b7d…
    2f4896d   rd-361-round3-s44   ROUND 3's tip = the base. The Blocker is LIVE here.
    1149d1c   round 2             the older Blocker state, if you want a second before-column.
    main                          251 behind. NOT a diff base. Base everything on `2f4896d..400718f`.
                                  Diffing against main reads other people's merged work as this change.

3 files, +225/−94: `backend/services/authEnforcement.js`,
`__tests__/auth-gate-fail-closed.test.js`, `scripts/verify-expected-counts.json`.
Builder's claim: **PASS 2182/2182 across 113 suites**, 2177 → 2182 reconciling as 7 cells added and
2 replaced, counts regenerated with `--update-counts` rather than hand-picked.

## 2. 🔴 THE CENTRAL QUESTION — does the Blocker actually close, on the wizard's ordinary path?
The fix relaxes only when a readable settings OBJECT carries **neither `authEnforced` nor
`authEnforced_updated_at`**. `firstRunStillInProgress` is renamed `authEnforcedNeverWritten`.

**Reproduce, do not reason.** Real server, real `npm start`, real `DATA_DIR`, boot → interrupt →
boot on the SAME directory, on BOTH heads:

    state I   Log Analytics connected, then restart   2f4896d: DENY 503  ->  400718f: must SERVE
    state I2  "don't show again" ticked, then restart 2f4896d: DENY 503  ->  400718f: must SERVE
    state F   fresh, recycled before setup            both: serve
    state C2  authEnforced KEY alone removed          both: must DENY (the stamp survives)
    state E   enforced and intact                     both: require-session — NO REGRESSION
    state L1  settings emptied, backups intact        both: require-session via restore — NO REGRESSION
    state RST admin reset                             both: allow-open-mode — NO REGRESSION

**The deadlock is the thing to confirm gone:** at `2f4896d`, `POST /api/auth/enforce` itself returns
503 with a VALID CSRF token, so the one route that could repair the deployment is refused. **Drive it
with a real token on both heads.** E, L1 and RST are the regression column — the builder states the
predicate is never consulted there because the branch is guarded on the key being ABSENT
(`authEnforcement.js:215`). **Verify that guard rather than accepting it**, because a predicate that
silently starts being consulted is how a fix reaches states it was never reasoned about.

## 3. 🔴 THE COMPLETENESS CLAIM — the builder named this as its own weakest point, and it is right
**"`authEnforced` has exactly two writers across all 678 git-tracked files"** is the load-bearing
sentence, and it is **the same SHAPE of claim that killed round 3** — a census correct over a frame
smaller than the question. The builder widened past `backend/` and stated its frame. **A frame someone
states is still a frame they chose.**

1. **Re-run the census yourself, over a frame you choose**, and say what yours was. Every extension,
   no filter, dotfiles included, and check the language boundary that killed round 3 (`.js` vs `.ts`
   vs the frontend under `static/`, and any template or generated caller).
2. **Both writers must go through `setSetting`** — that is what makes the stamp unconditional. If any
   path writes `authEnforced` some other way (a direct file write, a bulk `saveSettings`, a
   migration, a restore, a seed, a test helper that ships), **the stamp can be absent while the key
   is present**, and the fix is wrong in the dangerous direction.
3. **Can the stamp be absent on a real customer deployment by a route nobody modelled?** The builder
   checked two — nothing strips it (the one `delete settings[…_updated_at]` at `jsonStorage.js:2073`
   is `LEGACY_AI_LOG_KEY`, a different key), and it is not newer than the write (`git log -S` puts
   both in `8eb94ce`, 2026-04-18). **Look for a third. The builder says a third would sink this.**
   Migrations, backup/restore round-trips, and anything that rewrites settings wholesale are where to
   look.

## 4. VERIFY THE RED-PROOF — do not trust it, re-run it, and M0 is the one that matters
The builder red-proofed **per clause**, asserting each mutation PRESENT before reading its result:

    M1  key clause deleted        1 red — clause 2 only
    M2  stamp clause deleted      3 red — cell C, the discriminator, clause 3
    M3  type guard weakened       1 red — clause 1 only
    M4  blanket deny              4 red — both Blocker cells + the relax control
    M0  round-3 logic restored    4 red — including the Blocker's second form

**M0 is the discriminating one**: it proves the new cells fail against round 3's ACTUAL shipped
implementation rather than a strawman. **Re-run M0 yourself.** A multi-clause guard red-proofed with
a fixture that trips more than one clause has measured the pair and learned nothing about the parts —
so check that M1 and M3 really do isolate single clauses.

**M4 exists so the fix cannot degenerate into round 2's blanket deny under a green suite.** Confirm it
still discriminates.

## 5. THE BUILDER'S OWN TEST DEFECT — confirm the fix, and look for its siblings
Cell C originally used a `storeWith()` helper that hand-writes `settings.json` and **therefore cannot
produce a stamp**; it went red on its own precondition rather than passing on a fixture. It now drives
the real `setSetting`. **A test helper that reimplements the product is a mock the moment the product
moves.** Check whether any OTHER cell in that file still hand-writes settings where it should be
driving the product — that is the same defect wearing a different cell number.

## 6. 🔴 WHAT THIS ROUND DOES **NOT** CLOSE — do not credit it, and check it did not get worse
**F-2 / state L4** — settings emptied with `backups/` AND `.emergency-backup/` both gone — **still
resolves to `allow-open-mode`, exactly as under round 3.** The stamp dies with the file. This is
measured undecidable from inside the volume and its durable fix is the platform layer (**RD-368**,
where the builder added the measurement as comment 37267).

**Your job on this: confirm L4 is UNCHANGED, not improved and not worsened.** If round 4 has made L4
reachable in any state it was not reachable in before, that is a finding and it outranks everything
else in this brief. **And if any artefact you read — the docblock, the commit message, RD-361, RD-370
— reads as though L4 is closed, say so.** The builder says it wrote the exclusion in its own words in
all four; verify that rather than taking it.

## 7. ITEM 3 — the inverted cell, and whether the inversion traded one wrong assertion for another
Round 3's suite asserted `DENY_UNKNOWN` for `{entraTenantId:'x', firstRunComplete:true}` and labelled
it `lost` — **the surviving Blocker asserted as intended behaviour inside the suite meant to catch
it.** It has been inverted: that state must now SERVE. **The builder flagged this as its own third
worry.** Ask whether the new assertion is right for the right reason, or merely the opposite of a
wrong one.

## 8. THE DRIVABLE SURFACE — and the honest limit, carried from round 3
**A LOCAL RUN AT THIS COMMIT against a fresh data directory. NOT the demo.** RD-76 is real: the demo's
`/login` carries zero `<form>` and zero `<input>`, so no test account opens it. Say *"same commit, not
the demo image"* — never imply the demo was tested. The predicate is exported and the whole state
space is reproducible by constructing a real `JsonStorage` twice over one directory, so **no browser
is required for the subject.** No screen changed; **do not manufacture screenshots**, and record that
as correct rather than as missing coverage.

**🔴 The shared local dev stack is STALE BY DESIGN.** Build your own from the repo's provisioning
path, or state plainly what a stack built on an older date cannot prove. The seeded stack on `:6882`
has also taken unparameterised writes from a previous pass — **treat its DATA as untrusted.**

**Neutralise the live-demo probe, as the round-3 gate did:** `healthSweeperScheduler.js:31` hardcodes
the demo URL as its default sweep target. Set `HEALTH_SWEEP_URLS=" "` on every boot. **No `az`, no
registry, no contact with `nexusai-staging` or the demo.** The builder's checkout is READ-ONLY —
work in your own clone or worktrees and restore them clean.

## 9. Evidence rules — mandatory
- **Positive control on the instrument** (something that proves a 503 is a gate decision and not a
  dead server) and a **negative control that flips with the subject**. A zero with no control is not
  a measurement.
- **Every tamper asserted to have LANDED before its effect is read.** Discard any run whose tamper did
  not land; do not report it.
- **Read every hit before counting it.** Quote `file:line`.
- **Name the frame** in every sentence claiming completeness — the failure family that killed round 3
  and nearly killed the builder's own item 1 (its first harness gave each state a fresh temp
  directory and manufactured two differences that looked exactly like findings).
- **Every analysis record carries FOUND / TESTED / HOW, with the controls named under HOW** — Kam's
  standing instruction of 2026-09-07 18:56:36.
- **State what you did NOT test**, in the same breath as what you did.

## 10. Verdict
**GO · GO-with-findings · NO GO**, with severities. A guard that is real but narrow is
**GO-with-findings**, not NO GO. **A NO GO here goes to Kam as a decision, not to a round 5** — so if
you NO GO, say what you would do next and what it would cost.

Report to **Wednesday**, not to the builder. Write the report and evidence under
`projects/nexusai/reports/2026-09-07-rd361-round4-tier1/` and name the path in your mail.

PROVENANCE:
- Head 400718f and its parent | `git -C <NexusAI>/2_Project_Files ls-remote origin refs/heads/rd-361-round4-s45` run by Wednesday - Wednesday's read, not yours | read 2026-09-07
- The fix, the red-proof table, the cell-C defect, RD-370, the L4 exclusion | the builder's READY mail 2026-09-07T11:47:48Z, DKIM-verified - relayed, not re-measured by Wednesday | read 2026-09-07
- The three frontend writers and the tab order | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round3-tier1/report.md section 2 — the ROUND 3 GATE's own first-hand finding | read 2026-09-07
- main 251 behind; RD-76 demo login unusable; the stale shared stack | same round-3 report, sections 1 and 8, plus Wednesday's handover - Wednesday's tree, not yours | read 2026-09-07
- Kam's cap, his round-3 bend and his round-4 authorisation | /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/dashboard/data/decisions.json cards `nexusai-rd361-blocker-vs-nogo-cap` and `nexusai-rd361-round3-blocker-survives` - Wednesday's tree, not yours | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 21:52
