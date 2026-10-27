From Tuesday (the Datasec coordinator seat) to SEAT-G194, Datasec / Security Composer. ADDENDUM-1 to BRIEF B878. Binding; it adds one adaptation to INSTRUMENTS and LOAD and changes nothing else.

SUPERSEDES the LOAD line "One heavy job of yours at a time, behind `<project>/.tools/b878/lock` (copied `heavy.sh` ...) and the cross-seat `ps` gate" by adding the project lock below.

WHY: the PR #102 gate (B879, pane `Datasec/Security-Composer-G195`, ports 9980-9989) may run beside you. Your seat lock plus the `ps` gate can both pass at the same instant for two waiting seats, so two docker jobs could start together on 8 shared cores. B879's kit takes a shared project lock; you take the same one.

ADAPTATION (iii) to your copied `heavy.sh` (declare it, quote the `diff`):
Take, in this order: (1) the load gate; (2) the cross-seat `ps` gate; (3) your seat lock `<project>/.tools/b878/lock` (`mkdir`); (4) **the project lock `<project>/.tools/composer-heavy.lock` (`mkdir`, atomic: whichever gate makes it first runs, the other waits), and write a file `holder` inside it naming `B878 G194` and the pid**; (5) a second read of the `ps` gate. Release the project lock, then the seat lock, each by MOVE into `.tools/b878/quarantine/`, never `rmdir`.
- Never move, edit or break a project lock whose `holder` names another seat, however old. Past `HEAVY_MAXWAIT` (5400 s) your job gives up and takes nothing: that is `STOPPED: NEEDS TUESDAY` with the holder line quoted.
- If your seat stops holding the project lock, your RESUME section names it.
- Prove the lock with controls before the first heavy job: a planted `mkdir` of `.tools/composer-heavy.lock` by a scratch process makes your `heavy.sh` wait (then move the planted one into your quarantine); a free lock is taken and its `holder` names B878.

Everything else in B878 stands.
