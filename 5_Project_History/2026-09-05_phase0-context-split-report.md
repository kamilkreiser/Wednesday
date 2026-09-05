---
date: 2026-09-05
type: report
source: WED-145 Phase 0, executed by a Wednesday-assistant seat on branch `phase0-context-split` (worktree `2_Project_Files/worktrees/phase0`), on Kam's 20:28 approval of `1_Project_Definition/Architecture/2026-09-05_learning-tiers-context-split-plan.md`
status: live
---

# WED-145 Phase 0 — measure and tag: what the three-tier split would take out of Wednesday's boot

## BLUF
**The boot path drops from 543,399 B to 427,895 B — 21.3%.** Scaled linearly against the
27% this brain load measured today, that is an **estimated ~21% boot (about 6 points back). It is an
ESTIMATE, not a measurement** — the real number is the statusline at the next boot that reads the
by-tier digest. **Nothing was deleted, merged or rewritten.** Every ledger row still exists, byte for
byte; every lesson file still holds every word of its cases; the default digest is unchanged. All of it
sits on `phase0-context-split` for Wednesday and Kam to rule on.

## The numbers

| Thing | Before | After | Δ |
|---|---:|---:|---:|
| `_ledger.md` (read whole at every boot) | 288,517 B · 135 rows | 199,169 B · 93 rows | **-89,348 B (-31.0%)** |
| `_ledger_fleet_insights.md` (new, read on demand) | — | 90,296 B · 42 rows | +90,296 B |
| Boot digest | 254,882 B (`_boot_digest.md`) | 228,726 B (`_boot_digest_by_tier.md`) | **-26,156 B (-10.3%)** |
| **What a boot reads (digest + ledger)** | **543,399 B** | **427,895 B** | **-115,504 B (-21.3%)** |
| Boot ctx% (statusline) | 27% (measured, every seat since 09-02) | **~21% (ESTIMATED, linear)** | ~−6 points |

**Conservation.** The 42 moved rows are byte-identical to their source lines and the row SET is equal:
HEAD's 135 rows == 93 (ledger) + 42 (new file), no duplicates, original order preserved in both. Ledger
bytes on disk went 288,517 → 289,465 across the two files — **+948 B**, which is the new file's own
heading prose, its table header, and the one pointer line added to `_ledger.md`. No row was edited.

**Where the digest's 26,156 B comes from:** 25,183 B is the 28 project CASE sections becoming one-line
handles; 973 B is the section index dropped from the 24 M files. The P sections are **73,445 B in the
lesson files** but only 25,183 B in the digest — the digest already carried their rules and headings, not
their evidence. Do not add those two figures together: 73,445 B is what would travel to the agents in
Phase 1; 25,183 B is what leaves Wednesday's boot.

## The tiers, as tagged

98 lesson files, 464,832 B, every one now carrying `tier:` in its frontmatter.

| Tier | Files | Bytes |
|---|---:|---:|
| W — Kam, the coordination method, the boundaries, Wednesday's own failure modes | 69 | 260,648 |
| M — fleet method, client-neutral | 24 | 85,237 |
| MIXED — a W/M lesson carrying project CASE sections | 5 | 119,913 |
| P — a project's own cases, as a whole file | 0 | 0 |

**The W/M split is a first pass and nothing yet depends on it** — in the digest, M differs from W only by
dropping the section index (973 B across 24 files). It matters in Phase 2, when the M tier is what
travels to every agent. Wednesday should read the tier column of `_tier_census.md` as a proposal.

## The section list — every P section that would leave the boot

| Project | Case sections | Bytes in the lesson files |
|---|---:|---:|
| P-Datasec/NexusAI | 14 | 42,660 |
| P-Secuura/Blockchain | 14 | 30,785 |
| **total** | **28** | **73,445** |

24 of the 28 sit in `2026-08-07_a-check-that-cannot-fail.md` (71,660 B — 15% of all lesson bytes, and
the single largest file in the brain). The other four are one section each in
`headline-must-match-the-operative-case`, `i-read-representations-they-read-sources`,
`a-recorded-blocker-is-not-a-boundary` and `an-overstated-record-gets-discounted-wholesale`.

Full list, verbatim from `0_Brain/learnings/_tier_census.md`:

| File | Project | Section | Bytes | Note |
|---|---|---|---:|---|
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The concrete remedy, added 2026-08-13 (Secuura/Blockchain s28) | 2,226 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A failure-only log going quiet is not recovery (2026-08-22, Secuura s61) | 1,441 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The third member: a check that MISREPORTS what it saw (2026-08-14, same agent) | 1,756 | heading says 'same agent'; body names PR #646 (= KS-559, Secuura) and 'a Secuura session caught it' |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A test that cannot CLEAN UP starts asserting against live data (2026-08-15, Secuura s35) | 2,538 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A positive control proves the suite it RAN IN, and nothing about its neighbour (2026-08-15, Secuura s35) | 1,494 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | The inverse: a REPRODUCTION that cannot reproduce (2026-08-15, Datasec/NexusAI) | 2,467 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The refinement that makes the positive-control rule actually work (2026-08-16, Secuura s37) | 1,849 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | An indicator that can MISS its own event (2026-08-24, Datasec/NexusAI) | 1,221 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | The control needs its own control (2026-08-23, Datasec/NexusAI) | 3,030 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The condition we had not stated: on a side-effecting system, the positive control IS an action (2026-08-14, Secuura s34) | 2,051 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The mirror: an ABSENCE claim needs a positive control too (2026-08-14) | 2,689 | heading carries no project; body: 'A Secuura session flagged…' |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | Three "cannot see" members from one micro-session (2026-08-25, Datasec/NexusAI s5) — and a derivation lesson from its neighbour | 1,977 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A test's NAME is not its coverage (2026-09-03, Secuura s119 — the member that let an AUTH BYPASS survive a suite that appears to test it) | 3,287 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | A census, a writer and a verifier that descend from ONE parse are one view rendered three times (2026-09-04, Datasec/NexusAI S29 — its own diagnosis,  | 3,563 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | THE ALL-FAIL RED-PROOF: a tamper that destroys the SUBJECT, so the failure set stops discriminating (2026-09-04, Datasec/NexusAI — self-caught and sel | 2,244 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | A FIXTURE THAT CANNOT REACH THE PRODUCT'S PATH — the entry-point member (2026-09-04, Datasec/NexusAI RD-245; a BLOCKER found under a green suite the t | 3,734 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | CORRECTED the same session, by the same agent, and the correction is the better lesson | 5,210 | sub-section continuing the Datasec/NexusAI S29 census case (L486), filed out of order after the L606 shell section |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A red-proof proves a check CAN fail; only a GREEN BASELINE proves it can pass for the right reason (2026-09-04, Secuura s120 — a guard defeated by its | 3,367 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | The AXIS a guard is blind on is not the axis it was designed for (2026-09-04, Datasec/NexusAI — a perfectly-implemented guard, green on a defect it co | 2,898 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | THE OTHER END OF IT: a red-proof on a subject that did not COMPILE is not a red-proof (2026-09-04, Secuura s121 — the pair to the green-baseline rule  | 3,073 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | A MULTI-CLAUSE guard red-proofed with a fixture that trips BOTH clauses has measured the pair and learned nothing about the parts (2026-09-04, Datasec | 3,475 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | THE SECOND HALF, added hours later by the TESTER that verified the fix (2026-09-04, QA re-gate on `aad37da`) | 2,903 | sub-section of the L831 Datasec/NexusAI multi-clause-guard case (the tester's second half) |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | AN ELIMINATION SET THAT IS EXHAUSTIVE WITHIN ONE CATEGORY AND SILENT ABOUT THE OTHERS (2026-09-04, Datasec/NexusAI S32 — it disproved its OWN filed fi | 3,523 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A TEST HELPER THAT REIMPLEMENTS THE PRODUCT IS A MOCK THE MOMENT THE PRODUCT MOVES (2026-09-05, Secuura s128 — found by its own red-proof, not by read | 2,047 |  |
| `2026-08-13_headline-must-match-the-operative-case.md` | P-Secuura/Blockchain | The tooling costume (2026-08-17, Secuura s43): a check whose MESSAGE rots while its measurement stays correct | 1,857 |  |
| `2026-08-14_i-read-representations-they-read-sources.md` | P-Datasec/NexusAI | The fourth switch (2026-08-25, Datasec/NexusAI s4): the option you can VERIFY WITHOUT EFFORT | 1,422 |  |
| `2026-08-16_a-recorded-blocker-is-not-a-boundary.md` | P-Secuura/Blockchain | The third member (2026-08-27, Secuura s73; consolidated 2026-08-30): a DEFERRAL recorded only in code, pointing at a ticket | 1,110 |  |
| `2026-08-16_an-overstated-record-gets-discounted-wholesale.md` | P-Datasec/NexusAI | THE ROT HAS A MECHANISM, and the NexusAI agent (S32) named it better than I had (2026-09-04, after its THIRD stale ticket in one day) | 4,993 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | MIXED | M | 71,660 | Datasec/NexusAI 12 sec / 36,245 B · Secuura/Blockchain 12 sec / 27,818 B |
| `2026-08-16_an-overstated-record-gets-discounted-wholesale.md` | MIXED | M | 9,448 | Datasec/NexusAI 1 sec / 4,993 B |
| `2026-08-13_headline-must-match-the-operative-case.md` | MIXED | W | 5,623 | Secuura/Blockchain 1 sec / 1,857 B |
| `2026-08-14_i-read-representations-they-read-sources.md` | MIXED | W | 25,262 | Datasec/NexusAI 1 sec / 1,422 B |
| `2026-08-16_a-recorded-blocker-is-not-a-boundary.md` | MIXED | M | 7,920 | Secuura/Blockchain 1 sec / 1,110 B |
| `2026-08-06_ghost-suggestions-in-panes.md` | W | — | 17,636 | — |
| `2026-09-01_qa-gate-before-my-verification.md` | W | — | 11,810 | — |
| `2026-09-02_coo-actionable-tickets-never-wait-for-kam.md` | W | — | 9,758 | — |
| `2026-08-28_contemplation-mistakes-and-the-fixed-will.md` | W | — | 9,270 | — |
| `2026-08-15_a-cap-is-never-neutral.md` | M | — | 7,463 | — |
| `2026-09-05_three-tier-learnings-wednesday-management-agents-project.md` | W | — | 7,018 | — |
| `2026-09-02_the-statusline-is-the-context-instrument.md` | W | — | 6,854 | — |
| `2026-09-03_a-pane-close-is-a-session-kill.md` | W | — | 6,770 | — |
| `2026-09-03_a-ratified-design-has-two-halves.md` | W | — | 5,945 | — |
| `2026-09-04_decisions-held-narration-drifted.md` | W | — | 5,683 | — |
| `2026-08-07_ask-for-what-you-need.md` | W | — | 5,427 | — |
| `2026-08-16_classification-is-the-field-that-grants-authority.md` | W | — | 5,409 | — |
| `2026-09-02_style-guides-never-mixed.md` | M | — | 5,395 | — |
| `2026-08-25_travel-drive-stale-pointers.md` | W | — | 5,172 | — |
| `2026-09-02_coo-actionable-tickets-never-wait-for-kam (conflict_on_2026-09-04).md` | W | — | 5,159 | — |
| `2026-08-06_artifact-presence-is-not-execution.md` | M | — | 5,048 | — |
| `2026-08-09_an-enforcement-you-must-arm-is-not-one.md` | M | — | 4,779 | — |
| `2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md` | W | — | 4,700 | — |
| `2026-08-26_a-sync-that-cannot-refuse-a-deletion.md` | M | — | 4,653 | — |
| `2026-09-01_a-tap-is-a-pointer-not-a-message.md` | W | — | 4,650 | — |
| `2026-08-07_protocol-v1.3-signed-delegation.md` | W | — | 4,617 | — |
| `2026-09-05_tickets-are-the-channel-whatsapp-via-kam-is-the-escalation.md` | W | — | 4,601 | — |
| `2026-08-07_valid-is-not-delivered.md` | M | — | 4,572 | — |
| `2026-08-10_a-ritual-nothing-triggers-is-not-a-ritual.md` | W | — | 4,500 | — |
| `2026-08-13_establish-authority-before-reconciling.md` | M | — | 4,461 | — |
| `2026-08-16_an-ask-without-a-default-is-an-indefinite-hold.md` | W | — | 4,428 | — |
| `2026-09-05_handovers-to-peter-and-stuart-are-test-blocks.md` | W | — | 4,372 | — |
| `2026-08-07_we-each-have-strengths.md` | W | — | 4,356 | — |
| `2026-08-13_containment-never-run-is-a-claim.md` | M | — | 4,333 | — |
| `2026-08-21_challenge-me-when-you-think-im-wrong.md` | W | — | 4,329 | — |
| `2026-08-29_unquoted-heredoc-executes-backticks.md` | M | — | 4,168 | — |
| `2026-08-07_a-promise-is-not-a-mechanism.md` | M | — | 4,149 | — |
| `2026-08-13_shared-bus-tag-filter-or-leak.md` | W | — | 4,070 | — |
| `2026-08-06_brief-provenance-enforcement.md` | W | — | 4,061 | — |
| `2026-08-04_validate-brief-pointers.md` | W | — | 3,983 | — |
| `2026-08-07_ghost-text-can-fool-the-human-too.md` | W | — | 3,819 | — |
| `2026-08-17_conversation-needs-a-stable-panel.md` | W | — | 3,753 | — |
| `2026-09-02_rotate-in-the-70-80-band-conditionally.md` | W | — | 3,624 | — |
| `2026-08-15_a-gui-open-is-a-write.md` | M | — | 3,535 | — |
| `2026-08-03_context-loading-split.md` | W | — | 3,463 | — |
| `2026-08-07_autonomy-grant-ship-decisions.md` | W | — | 3,461 | — |
| `2026-08-11_coordinator-not-carrier.md` | W | — | 3,445 | — |
| `2026-08-05_kam-types-into-panes.md` | W | — | 3,393 | — |
| `2026-08-26_never-delete-cleanup-means-quarantine.md` | M | — | 3,391 | — |
| `2026-09-05_root-folder-holds-only-rules-and-launchers.md` | W | — | 3,364 | — |
| `2026-08-07_enumerate-every-surface-before-done.md` | M | — | 3,325 | — |
| `2026-08-07_authorship-is-checkable-dkim.md` | M | — | 3,292 | — |
| `2026-09-03_names-not-pronouns-in-notes-and-actions.md` | W | — | 3,090 | — |
| `2026-08-04_never-blanket-markseen-mid-monitoring.md` | M | — | 3,006 | — |
| `2026-08-06_ask-format-client-project-options-rec.md` | W | — | 2,989 | — |
| `2026-08-06_local-proof-is-not-target-evidence.md` | M | — | 2,889 | — |
| `2026-08-21_decision-queue-and-rotation-rhythm.md` | W | — | 2,868 | — |
| `2026-08-25_one-drive-devmaster-is-master.md` | W | — | 2,868 | — |
| `2026-08-06_bluf-write-for-the-reader.md` | W | — | 2,806 | — |
| `2026-08-28_overnight-is-working-time.md` | W | — | 2,783 | — |
| `2026-08-05_identities-float-verify-always.md` | W | — | 2,757 | — |
| `2026-08-21_auto-rotate-at-70pct.md` | W | — | 2,698 | — |
| `2026-08-04_delegation-v2-observability.md` | W | — | 2,666 | — |
| `2026-08-22_vendor-asks-scale-to-leverage.md` | W | — | 2,665 | — |
| `2026-08-06_exercise-mechanisms-before-arming.md` | M | — | 2,593 | — |
| `2026-08-06_never-discard-stderr.md` | M | — | 2,585 | — |
| `2026-08-20_dashboard-shows-only-live-work.md` | W | — | 2,576 | — |
| `2026-08-03_contemplation-the-cockroach.md` | W | — | 2,567 | — |
| `2026-08-04_gitignore-artifacts-at-creation.md` | W | — | 2,507 | — |
| `2026-08-05_life-os-commission-principles.md` | W | — | 2,479 | — |
| `2026-08-19_a-pagination-default-is-a-selector.md` | M | — | 2,445 | — |
| `2026-08-05_wed-work-threshold-delegation.md` | W | — | 2,387 | — |
| `2026-08-12_morning-ticket-sweep-autostart.md` | W | — | 2,337 | — |
| `2026-08-12_hpsm-continuous-readiness-grant.md` | W | — | 2,335 | — |
| `2026-08-03_mental-model-not-source-of-truth.md` | W | — | 2,273 | — |
| `2026-08-26_mirror-reports-state-not-intent.md` | W | — | 2,245 | — |
| `2026-08-26_zsh-has-no-pipestatus.md` | M | — | 2,164 | — |
| `2026-08-10_own-the-spec-not-just-the-escalation.md` | W | — | 2,026 | — |
| `2026-08-10_kam-agent-conversations-are-my-surface.md` | W | — | 2,009 | — |
| `2026-08-03_context-discipline-close-before-full.md` | W | — | 1,997 | — |
| `2026-08-06_selector-discipline-in-ui-verification.md` | M | — | 1,851 | — |
| `2026-08-03_role-beyond-code-three-priorities.md` | W | — | 1,847 | — |
| `2026-08-21_deliver-whole-or-say-wait.md` | W | — | 1,834 | — |
| `2026-08-17_check-the-refusal-before-the-kill.md` | M | — | 1,824 | — |
| `2026-08-05_browser-extension-islocal-untrustworthy.md` | M | — | 1,816 | — |
| `2026-08-06_morning-shift-change.md` | W | — | 1,790 | — |
| `2026-08-03_workflow-systemisation-duty.md` | W | — | 1,733 | — |
| `2026-08-21_steps-get-line-breaks.md` | W | — | 1,722 | — |
| `2026-08-03_go-slow-earn-autonomy.md` | W | — | 1,680 | — |
| `2026-07-31_fully-portable-drive.md` | W | — | 1,641 | — |
| `2026-07-31_parent-child-learning-model.md` | W | — | 1,631 | — |
| `2026-08-05_verify-the-chain-not-the-legs.md` | M | — | 1,500 | — |
| `2026-08-03_frequency-weighted-reinforcement.md` | W | — | 1,438 | — |
| `2026-08-03_grant-readonly-tracker-access.md` | W | — | 1,391 | — |
| `2026-07-31_manage-dont-do.md` | W | — | 1,389 | — |
| `2026-08-03_daily-rhythm-6-to-23.md` | W | — | 1,339 | — |
| `2026-08-12_no-cc-kam-on-agent-mail.md` | W | — | 1,276 | — |
| `2026-07-31_one-question-at-a-time.md` | W | — | 1,109 | — |

**Four of the 28 name no project in their heading**; their client was resolved from the case body and
each carries the reasoning in the Note column. Those four are the ones to check before any transfer —
a case that travels to the wrong client's agent is an R0 breach, and a heading is the only thing a
future reader will look at.

## What was NOT done, deliberately
- **Nothing merged.** Everything is on `phase0-context-split`; `main` was never touched.
- **Nothing deleted.** No row, no section, no file. The moves are moves.
- **No Phase 1 transfers, no M-tier shared home, no lesson text changed** — out of Phase 0's scope.
- **Five ledger rows were NOT moved** although their type says fleet-insight: their subject is
  Wednesday's own hands or her own tooling, and the brief says an ambiguous row stays and gets listed.
  They are in the STATUS mail and in the commit for step 1.
- **The boot has not been re-measured.** The ~21% is arithmetic on bytes. Nothing reads
  `_boot_digest_by_tier.md` yet — the launcher still loads `_boot_digest.md`, and switching it is
  Wednesday's call, not this seat's.

## How the default digest was proven unchanged
1. **The code change is inert.** The pre-change script and the post-change script, both run over the
   pre-tag lesson files with a frozen timestamp: `cmp` byte-identical, 254,882 B — and identical to the
   digest captured before any edit in this session.
2. **The whole of Phase 0 is inert on it.** That same baseline against the new script run over the
   tagged files: the only differing line is the header's own source-bytes measurement
   (464,044 → 464,832 B — the 96 `tier:` lines). Digest bytes identical at 254,882.
   `boot_digest.py --check`: 98 files, 0 misses, 0 stale.
3. **Red-proof of the flag.** A fixture lesson tagged `tier: P-Test/Fixture` emits exactly one line and
   no case prose; delete the tag and it falls back to the default shape and is named UNTAGGED
   (2,236 B → 2,615 B).

The `<!-- tier: P-… -->` markers are stripped in `parse_text`, so neither digest ever carries one.

## Provenance
- Plan and tiers | `1_Project_Definition/Architecture/2026-09-05_learning-tiers-context-split-plan.md` + `0_Brain/learnings/2026-09-05_three-tier-learnings-wednesday-management-agents-project.md` | read 2026-09-05 by this seat
- Kam's approval | panel 20:28, "Let's go ahead with the proposed plan" | quoted in the brief
- The 27% baseline | the brief's measured figure for digest + ledger today | not re-measured here
- Every other number above | measured from the files in this worktree at the commit each step names
