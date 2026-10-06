ANSWER (Seat D 12th): build-cache prune ALLOWED by Kam.

AUTHORITY: Kam ruled card `secuura-kintsugi-build-cache-prune-if-disk-guard-1006` = (a) on the live board, tap 23:05:25 AEDT (12:05:25Z), card stored ruled 23:06:18 AEDT. Option (a) text, verbatim: "Allow a build-cache-only prune if the guard trips" — detail: "Seat D 12th runs `docker builder prune` once (build cache only; no image, no rollback set, no volume), reads the free space, and resumes the build. Reported with before/after figures."

WEDNESDAY'S READING OF "IF THE GUARD TRIPS" (the 4,000 MB floor cannot see originate, per your 11:45Z finding): your ARMED CONTROLLED STOP before originate IS the trip this ruling covers, and so is a 4,000 MB floor refusal if one comes first. Whichever fires first is the one moment the prune runs.

RECEIVED: your 12:05Z correction (354 / 342 MB per image, steady; originate short by ~3,300-3,450 MB; the 188 taper withdrawn). The window diagnosis is right, and correcting it to Kam directly was right.

THE ORDER, at the stop and only there:
1. Build loop IDLE (no `docker build` process alive, checked by pid, never by basename). Never prune during a build.
2. Read BEFORE: `df` free MB + `docker system df` (build-cache line).
3. Run `docker builder prune -f` ONCE: the card's command, no `-a`, no `--filter`, no `image`/`system`/`volume` prune, no `rmi`. Paste its "Total reclaimed space" line verbatim.
4. Read AFTER, the same two readings. Assert every `:pre-20261006` rollback tag still resolves and the 21 built image IDs are unchanged (count before == after).
5. If free >= 8,600 MB: resume from your RESUME.md (only the remaining services, writing build.master.resume.log), originate first. If free is still < 8,600 MB: do NOT build originate, do NOT prune again or with `-a`. Mail the before/after figures and HOLD. Widening the prune is a new ruling, Kam's.
6. Report the before/after figures in your next STATUS. Wednesday relays them to Kam.

Everything else in the 11:12:34Z GO and the 11:45:58Z ANSWER stands. The swap STOPs, KS-535 and demo's STOP 1/STOP 2 are untouched by this mail.
