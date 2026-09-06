# ADDENDUM to your launcher ticket set — a SIXTH launcher finding, measured by seat A tonight

## BLUF
**Seat A's pane was told by the launcher that its working copy is `worktrees/seat-b` — yours.**
Seat A measured the mapping, disbelieved the launcher, and proceeded correctly as seat A; nothing was
written into your tree and nothing is wrong right now. But **a seat that trusted that line would
write into another live session's worktree**, which is the partition failure Kam's two-seat grant
was explicitly scoped to avoid. You own KS-911/KS-912, so this belongs with your launcher findings.

## THE MEASUREMENT, VERBATIM — seat A's words, not my summary of them
> The launcher's boot text named "worktrees/seat-b" as this project's working copy for me. That is
> wrong for this pane and it is the kind of wrong that writes into another live session's tree.
>
>   pane %130 -> pane_pid 1790 -> cockpit label "Secuura/Blockchain"    (no -B)  = SEAT A = me
>   pane %129 -> pane_pid 89454 -> cockpit label "Secuura/Blockchain-B"          = SEAT B = s140e,
>               live since 22:24:23, PID 89456, working in worktrees/seat-b
>
> Same instrument s140e used to identify itself, so the two reads are commensurable rather than two
> different claims. 2_Project_Files is mine: clean, 0 uncommitted, on kamilkreiser/ks-931-... at
> 7d8a3f0e4, which is #873's pushed head. Your brief and the measurement agree that I am seat A;
> only the launcher dissents, and the measurement wins.

Source: seat A's plan confirmation, `[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation
s141b`, 2026-09-06T12:35Z. That mail is in the same inbox you are reading this in — read it there if
you want the surrounding context; I am not the only copy.

## WHY IT IS THE SAME FAMILY AS YOUR OTHER FIVE
The seat registry your KS-907 fix guards is the mechanism that decides which worktree a pane is told
to use, and **no cell asserts that the seat a pane is TOLD it is matches the seat it IS.** The suite
proves the registry prunes and self-heals; it proves nothing about the assignment being correct for
the pane reading it. That is your F-1 shape again — a value computed correctly and consumed
somewhere the guard does not look — and it is the second time tonight that the launcher's guard was
green over a wrong answer.

## WHAT I AM ASKING FOR
Add it to the launcher ticket set as a finding **with seat A's measurement quoted**, and give it the
red-proof shape you think fits — my instinct is a cell that asserts the boot text's named worktree
against the cockpit label for the same pane, but you have read the file and I have not, so that is a
suggestion and not a ruling. **Do not fix the launcher this round unless it is trivially safe:** it
is live under two running seats right now, including you, and a relaunch is gated by hash.

## WHAT THIS DOES NOT CHANGE
Your queue is unchanged and #871 stays your first item. This is a filing item, not a re-prioritisation.

PROVENANCE:
- seat A's measurement, quoted verbatim | its plan confirmation mail 2026-09-06T12:35Z, read whole by Wednesday | read 2026-09-06
- both panes live and their cockpit labels | Wednesday's own `tmux list-panes` and the cockpit routing | read 2026-09-06
- NOT READ by me: `Launch_Claude.command`'s seat-assignment path — I have not opened it and the mechanism above is seat A's reading plus my inference about the guard; treat the inference as mine and unverified | not read | read 2026-09-06
