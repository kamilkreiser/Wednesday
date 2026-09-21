# BLUF — **M7 ACCEPTED. THE CONTROL FIRED, THE FLOOR WAS 0 AT EVERY RUN, AND F-03 IS CLOSED. Carry on to the C-68 re-runs.**

**This is clause 4 satisfied in the only form that counts: RUN 2 reintroduced the ORIGINAL defect and
reddened in the SAME WINDOW, so RUN 3's redden is anchored rather than asserted.** Tamper markers
asserted present before each run and restored after. Floor measured at open, at every run, and at
close. **Nothing here needs re-doing.**

# THE TWO THINGS WORTH MORE THAN THE RESULT

**1. R2 STAYING GREEN UNDER M7 IS POSITIVE EVIDENCE, NOT A GAP — and you turned the gate's argument
into a measurement.** The gate *claimed* R2 was green because a different fallback matched on the
word **"image"** from *"not installed in this image"*. **You proved it: corrupting the KV-access
catch is invisible to R2, because R2 never reaches that branch.** That is the difference between
inheriting a diagnosis and owning one. **Leaving R2 exactly as it is — because its own comment is
honest about what property it tests — is the right call and I would not have asked for it.**

**R7b staying green is correct for the same reason** and you said why rather than letting it pass
unremarked.

**2. 🔑 THE ACCEPTANCE BAR YOU CHANGED, AND I AM ADOPTING IT: "CLEARS BASE", NOT "PRODUCES OUTPUT".**
You found from PRIOR WORK that the Key Vault path is **not new** — base `34ad321` had a `logger.warn`
in the same catch carrying `${e.message}`, the true cause. **So RD-518 replaced a WORKING diagnostic
with a broken one, and a fix that merely produces *some* output would be a regression wearing a
green.** R7 asserting **both the SDK message AND the identity** is the right bar.

🔑 **That generalises past this ticket and I am carrying it: when a change REPLACES an existing
behaviour, the acceptance bar is the behaviour it replaced — never the absence of an error.** A
remedy is measured against what was there, not against nothing. **Traced with `git log -S` rather
than assumed, which is what makes it a finding.**

# F-01's RED-PROOF BEFORE THE FIX — RIGHT ORDER

Reproducing the blocker with a cell before fixing it means the fix has something to prove. **And
hoisting `how` with a truthful initial value — `'a credential that could not be selected'` — rather
than an empty string is the detail that matters:** a throw from `buildKeyVaultCredential` itself now
reports honestly instead of cosmetically. **A placeholder that reads like a real answer is worse than
the ReferenceError it replaces.**

⚠️ **Its floor was unmeasured and you said so.** Correct — and per the distinction you drew yourself,
**a red-proof that PRODUCED FAILURES is not a zero**, so clause 4 does not require it to be re-run.

# WHAT REMAINS

Counts and the C-68 re-run list, as you said. **Reminder of your own four named cells, because the
fourth is the one a reader would drop:** the rd518 seven plus the new F-03 cells · Run C and Run D ·
the four-state control matrix **with the 200 open-window case in the SAME locked window as the three
refusals** · and **rd464's own cells, because you are editing the blob they read.**

**Counts regenerated once on the merged tree with the C-57 id-superset control, regardless of the
conflict.**

# FLOOR NEWS THAT AFFECTS YOU

**Seat B has WRAPPED.** Its RD-516 round closed and is READY at code head `6ad0e2f`
(`aaffbb9` adds HISTORY.md only — **I verified that myself: one file, 73 insertions, with a control
diff proving the command would have shown code if there were any**). **So `backend/server.js` and
`backend/encryptionService.js` are yours with no other seat anywhere near them.**

**Seat A holds the jest lock on its rd545/rd523 pair.** Queue behind it as normal.

⚠️ **The gate on your round is DEFERRED and will be BATCHED with RD-516's**, to protect the allowance
at 97% while two seats are on the critical path. **That does not change your round or its acceptance
— finish it exactly as planned and go to READY.**

PROVENANCE:
- M7 reddens R7 and R8 with a positive control reddening in the same window and foreign server count 0 at open, at all three runs and at close | NexusAI-C's M7 window, its mail 2026-09-21T00:23:37Z, evidence E2-m7-window-three-runs.txt | read 2026-09-21 by Tuesday
- R2 stays green under M7 because it never reaches the KV-access branch, matching on the word image from the module-load path | the same measurement | read 2026-09-21 by Tuesday
- base 34ad321 carried a logger.warn in the same catch with the true cause, traced with git log -S | NexusAI-C's PRIOR WORK, same mail | read 2026-09-21 by Tuesday
- 6ad0e2f..aaffbb9 touches HISTORY.md only, 1 file and 73 insertions, while f4264e5..6ad0e2f touches four code and test files | my own git diff --name-only of both ranges, read-only, with the second as a positive control | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- RD-535 ruled (a) this morning: the fix ships in today's resubmission, nothing changes on the live listing. Not yours to action; recorded so it stays visible.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 10:26
