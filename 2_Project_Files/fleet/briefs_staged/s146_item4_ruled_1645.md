## BLUF — ITEM 4 IS STOOD DOWN. Your measurement killed it and that is the measurement doing its job.
**Item 4 does NOT proceed as scoped, on your evidence, and it does not come back as a tail-end edit
to 12 files.** You were told to open with the measurement precisely so that a false premise would die
before code moved, and it did — **twice over, on two independent grounds.** That is the second time
today the measurement-first ordering has paid, and the first was your own F3 correction.

**One refinement to your §5, and it is the only thing I am changing.** You wrote that item 4 needs
*"a ruling on the SYSTEM_ADMIN gap."* **Most of that is measurable, not rulable — measure it first,
so that whatever is genuinely undecidable is small and clearly stated.** Detail in §2 below.

## 1. RATIFIED WITHOUT RESERVATION — and what makes the §1 evidence strong
Your zeros are real zeros because **you controlled them**: the same `git grep` over the same paths
finds `"test:unit"` in `playwright/package.json`, so the instrument fires. **An absence claim with a
positive control is a finding; without one it is a shrug.** You also enumerated the specific runners
that do *not* invoke provisioning — `global-setup.ts`, `auth.setup.ts` — by what they actually import,
rather than concluding it from the grep alone. **Two instruments, same answer.**

**So the fallbacks are the live path, not redundancy.** Removing them is precisely the F3 shape you
corrected this afternoon: taking out the harmless thing and leaving the one that detonates.

## 2. THE RULING ON §5.2 — MEASURE BEFORE ANYONE DECIDES
*"Do those sites need platform-admin reach, or is `orgAdmin` genuinely sufficient?"* — **for most of
the 12, that is a fact about the endpoints they exercise, not an opinion.**

**Do this instead of asking for a decision on all 12:** for each of the 12 sites, name the operation it
drives and read whether that route requires SYSTEM_ADMIN or is satisfied by ORG_ADMIN. **Then report
the SPLIT** — "N sites are satisfied by `orgAdmin`; M genuinely require SYSTEM_ADMIN, and here they
are." **The M is the real decision, and it will be far smaller than 12.**
This is the coordinator's job done at your seat: **turn "someone must decide" into "here is precisely
what is undecidable."** A decision put to Kam over 12 items he has to reconstruct is a decision he
cannot make quickly; the same decision over 2 named sites he rules in a sentence.

**If M turns out to be zero, item 4's second blocker dissolves entirely** and only the provisioning
prerequisite remains. **If M is non-zero, say so plainly** — the generated-actor path *cannot* serve
those sites, by the manifest module's own words, and that is a design fact, not a preference.

## 3. 🔴 THE THING IN YOUR §3 THAT IS BIGGER THAN ITEM 4 — raise it as its own item
**#888 is MERGED, so `getTestAdminPassword()` returns `''` on develop right now**, and the Playwright
`auth-setup` project therefore authenticates with an empty password unless `TEST_ADMIN_PASSWORD` is
set in the environment. **The direction is right and I am not second-guessing it.** What concerns me
is the discovery path:

**There is no CI on this repo** — you measured that yourself, 20 of 20 `startup_failure`. **So nothing
will fail loudly.** The next person to run that suite gets an authentication failure with no sentence
anywhere telling them which variable to set.

**Measure and report, in the same pass:** is `TEST_ADMIN_PASSWORD` actually documented as REQUIRED
anywhere a runner would look — `.env.example` (you confirmed `:133` is present but empty), the
Playwright README, `DEV-PROCESS`, the runbook? **If the variable is blank in the example and named
nowhere as required, that is a defect #888 introduced** — a correct security change with an
undocumented operational precondition. **Say so plainly if it is true; it does not diminish the fix.**

## 4. TICKET — ONE ticket, per Kam's 13:23 rule, not three
Kam, panel today, verbatim: *"if a single test is required, we should be creating one ticket with
multiple items inside it rather than multiple tickets. The only reason to create multiple tickets is
if they relate to separate workloads or separate fixes."*

**These are one logical path — the systemTest actor/credential story — so they are ONE ticket with
items:**
1. Wire actor provisioning into a pre-suite step so the manifest exists before anything reads it
   (its own test; not a tail-end edit).
2. The SYSTEM_ADMIN split from §2, with the M-sites named.
3. `TEST_ADMIN_PASSWORD` documented as required wherever a runner looks (if §3 confirms it is not).
4. Only then, the 12 sites.

**SEARCH BEFORE YOU FILE** — by SYMBOL (`getGeneratedActor`, `ADMIN_ACTOR_KEY`, `provision-actors`),
by PATH (`systemTest/fixtures/generated`), and by the error string. **Say in the ticket what you
searched and that you found nothing** — four sessions have worked this repo today and the same red is
in front of all of them. **Assign it to our account** (Kam 09-06: Platform K is ours; new and
unassigned items are ours — a ticket already on Peter or Stuart stays theirs).
**Then close KS-966 items 3 and 4 by comment**, pointing at the new ticket, so the next reader lands
on the reason rather than re-deriving it.

## 5. CREDIT — and your own formulation is going into the fleet's standing lines
**"A pass that skips a class cannot police that class, and I had built the skip into the instrument."**
That is the sharpest statement of this failure family anyone in the fleet has produced, and it is
being carried fleet-wide: **an enumeration's EXTENSION LIST is part of its claim, and an omitted
extension is a silent scope reduction that looks exactly like a complete answer.** Your `.py` omission
hid **six of the eight** executable files — the majority — and you found it yourself, before it
reached me, and led with it.

**Also credited:** the positive control on your zeros (§1), the two-instrument confirmation, and
separating "12 occurrences" from "8 executable files" from "3 example configs and 8 docs — those are
KS-965, not item 4." **Three different numbers that a careless pass would have merged into one.**

## 6. NEXT, AND YOUR BAND
Do §2 and §3 as measurements, file the ONE ticket, comment KS-966 items 3+4 closed against it.
**Then WRAP.** You were at ~60% before this turn and this was a heavy one. **Refresh
`HANDOVER-s146.md` with: the #888 merge, KS-968, the #891 workflow-scope block and its card, and this
item-4 stand-down with both blockers** — then hand over. **Do not start anything that will not fit.**
Both gates report to me, not to you; nothing is waiting on your seat.
