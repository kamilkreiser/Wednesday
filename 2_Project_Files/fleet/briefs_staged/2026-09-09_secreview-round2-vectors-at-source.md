# BRIEF — Security Review ROUND 2 of 2: re-derive the vectors AT SOURCE, then score

**From:** Tuesday (s2). **Round 2 of 2 under the cap.** A third round is Kam's, not mine and not yours.
**Predecessor:** `_Working/2026-09-09_VERIFY96_REPORT.md` — read it first; this brief builds on it and
does not repeat it.

## BLUF

**Your own strongest recommendation is now the commission. Re-derive each finding's CVSS vector from
the source code, and only then compute the score. Do not adopt the computed column from round 1.**

You proved why in round 1 and I am not asking you to re-argue it: `H-D1`'s vector was itself wrong, and
correcting one metric from source moved the row **down**, not up. `I-D2` looks like the same failure
inverted. **A score computed from an unchecked vector is not a verification, it is a second unverified
number wearing better clothes.**

## WHAT ROUND 1 SETTLED, so you do not re-derive it

`H-D1` → **High 8.6**, applied and verified in the rendered `.docx`; estate **23C / 82H / 339 total**.
The pending set is **97** (SPDF-D1 is the 97th). The 338-vs-339 typo, the PARKED row's arithmetic, and
the stray tally line are all corrected. The XXE question **closed negative** — `Directory.Build.props:3`
is `net10.0-windows`, nothing to file. **6 rows are re-derived at source; 91 are not.**

## THE QUEUE

**1. The two rows that need no judgement at all — do these first, they are transcription fixes.**
Restore the bucketing qualifiers on **`D-04`** and **`D-05`** (HPAuthenticationManager). Your round-1
finding is accepted in full: the reviewer was right, the register lost the qualifier, and a bare
"Medium | 9.1" reads as an error when it is a documented decision. **Restore the reason on the row so
the next reader cannot mistake it for a defect** — and so no future pass "fixes" it.

**2. The four declared-band-vs-printed-number contradictions** you found with no stated reason:
`NEW-2` (License-Services), `NEW-6`, `NEW-9` (License-Services), `NEW-9` (LicenseServer). You read three
of the four as one reviewer's systematic band habit rather than four slips. **Establish which it is from
the delta files, then correct the band or the number — whichever the source supports — and say which.**

**3. THE MAIN WORK: the 91 rows, vectors re-derived at source, Highs first.** Per row: read the code the
finding names, derive each CVSS metric from what the code actually does, record the vector, compute, and
state the band. **Where the re-derived vector differs from the filed one, the difference is the finding**
— say which metric moved and what in the source moved it. `H-D1`'s `AV:N`→`AV:L` is the template.

**4. The 16 band-crossers from round 1's table are a PRIORITY ORDER, not a verdict.** Do them first
inside the Highs, because they are where a wrong band is most likely and most costly. **The three that
would move High → Critical (`I-D2`, `I-D1`, `D-01`) come first of all** — an under-scored Critical is
the expensive direction.

## WHAT IS EXPLICITLY NOT IN THIS ROUND

🔴 **JUNE IS OUT.** `F-07`, `F-10`, `F-22` and the rest of the June baseline are **carded with Kam**
(`secreview-estate-wide-scoring-pass-including-june`, recommendation `extend`, default HOLD) because
extending into a signed-off deliverable is a scope change and his signature class. **Do not touch June
rows even if a current row's error traces into one** — where it does, name the June row and stop there.
That naming is useful; the edit is not yours.

## HOW THIS ROUND IS JUDGED

- **FOUND · TESTED · HOW · NOT TESTED** on every row whose band moves, per Kam's standing instruction.
- **Controls, and round 1 set the bar:** you validated your CVSS implementation against twelve published
  reference vectors before trusting it. Keep that. **A pass in which no row moves needs its instrument
  checked, not a clean bill.**
- **Do not file what you have not tested.** Round 1's named-but-unfiled items stay named — the PFX
  co-location and the generator-vs-artefact mismatch — until the tracing is done.
- **Depth stated plainly at the end**, as you did: how many re-derived at source, how many got
  mechanical treatment, and the register describing itself honestly either way.

## HOLDS — unchanged, every one

No live pass of any kind; the `fc05dcdd` vs `0c57ab37` tenant question is still unresolved and Kam's.
`Source_Code/` read-only. No secret value, prefix or redacted head. No client-facing comms, no Jira
writes. Never delete — quarantine. **Round 2 of 2: a NO GO or an unfinished tail at the end of this
round ships what is closed and tickets the residue. There is no round 3 without Kam.**

## THE CHANNEL, and one thing round 1 got right that I want repeated

No fleet inbox; your report on disk is the deliverable. **And say where you disagree with me.** Round 1's
fourth disagreement — that I scoped the commission one level too low, because the largest defect was in
the scoring instrument rather than in any of the 96 claims — was correct, is accepted, and is the reason
this round exists in this shape. **That is the single most valuable thing you produced.**
