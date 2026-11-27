# Proposal 1: the Wednesday seat's boot prompt reads the wake pack

TARGET: `Launch_Wednesday.command`
DIFF: `01_launcher_boot_prompt.diff` (unified, 115 added lines, 0 removed; regenerate with `python3 2_Project_Files/wake/proposed/build_launcher_diff.py --write`)

## Reason

The prompt mandates whole reads that today measure about 1.25 MB for the Wednesday seat (census re-run in `STATUS.md`). The diff adds two blocks. Hunk A, after the rules-card step and before doctor, builds `0_Brain/wake/WAKE-wednesday.md` with `wake_pack.py`. Hunk B, after the `INITIAL_PROMPT` assignment, replaces steps 1 to 4 of the read list with: the two rules files, the pack, Kam's rulings for the day, the week instruction. Steps 5 to 11 and the whole STANDING BEHAVIOUR block are reused from the existing prompt by slicing, so there is no second copy of that text to drift. The two daily notes stay a whole read (Kam's 2026-08-06 rule in `CLAUDE.md`). **That choice is one line:** in hunk B, `WAKE_NOTES="whole"`. Changing it to `WAKE_NOTES="ondemand"` replaces step 5 with "create today's note; earlier notes on demand" and reuses the legacy text from step 6; nothing else changes. Mandated reads are then about 21K estimated tokens instead of about 40K (the census prints both). Both settings are tested (P03 and P12). If Kam rules for on demand, the same answer also changes item 5 of proposal 3's list and step 4 of the session-start section in root `CLAUDE.md` ("read the last TWO daily notes in full"), which this round does not touch. The new step 2 also tells the seat that the handover is written only through `handover.sh`.

**A failed pack is loud (round 3, the checker's M3 and m2).** The build counts as done only when `wake_pack.py` exits 0 AND the pack file exists and is not empty. If it cannot be built, is over budget, is missing, or a slice marker is no longer found, the seat boots on the existing read list, whole and unchanged, and the FIRST lines of its prompt (directly after the `ultrathink` line) say: that the wake pack failed at this launch, why (the build's last line, which always starts `wake_pack: FAILED`), that this boot is on the legacy reads, and that the seat's first act is to tell Kam on the panel, write it in the boot note, and fix or ticket it. An `echo` is still printed for whoever watches the terminal, but the prompt is the channel. A seat never boots on a stale or partial pack, and `wake_pack.py` itself now fails the build rather than writing a part as a one-line placeholder (a missing or empty rules card, a card without its "Most reinforced" section, a grants file whose table cannot be read, a missing ledger).

**Round 4.** The prompt's two sentences about grants changed with the pack: it now says the register is in the pack in full, every row verbatim, that the pack does not judge which rows are live, and that nothing more is fetched for grants. The build also fails (and the fallback is loud) on a STATE file that `handover.sh check` would refuse. The suite now holds the two cases the second checker found untested: the build fails while an OLDER pack is on disk (P21), and the build exits 0 leaving an EMPTY pack (P22); both give the loud fallback.

**What else moves to on demand for this seat** (so the coordinator knows the whole change): `TASKS.md` (a pointer in the pack, as the brief asked), `INDEX.md` and `entries/`, the other coordinator's ledger headlines, and the scoreboard head. The last two were partial reads in the old step 3 and are not in the brief's list; the new step 2 names them as on demand.

## How the diff guarantees the other seats' text is byte-identical

1. **Additive only.** The diff has zero removed lines; `build_launcher_diff.py` refuses to write one that has any. The existing `INITIAL_PROMPT` assignment is not edited.
2. **One guard per hunk.** Each hunk is a single `if [ "$AGENT" = "wednesday" ]; then ... fi` block; the loud-fallback branch is inside hunk B's. Outside the guards the only added statement is `WAKE_PACK_OK=0; WAKE_PACK=""; WAKE_SUMMARY=""; WAKE_FAIL=""`, four assignments of names the launcher did not use before (needed because the launcher runs under `set -u`).
3. **Measured, not argued.** `tests/run.sh --groups P` extracts the real prompt region from the launcher, evaluates it for `tuesday` and for `friday` with and without the hunks, and compares the two prompts byte for byte (checks P01, P02; P01b and P02b confirm the added code prints nothing and builds no pack for those seats). The mutant "launcher change not confined to wednesday" turns those checks red.

## What a checker can run

```
python3 2_Project_Files/wake/proposed/build_launcher_diff.py | diff - 2_Project_Files/wake/proposed/01_launcher_boot_prompt.diff   # stored diff is current
bash 2_Project_Files/wake/tests/run.sh --groups P                                                                                # P00 to P16
```

## Not covered

No real launch was made: the launcher starts a seat. The prompt was evaluated in a harness that stubs the launcher's variables; the diff was applied to a scratch copy, which passes `bash -n`.

ROLLBACK: `patch -R Launch_Wednesday.command < 2_Project_Files/wake/proposed/01_launcher_boot_prompt.diff` (or `git revert` of the commit). The next launch is the legacy prompt again; the pack and STATE files are then unread and harmless.
