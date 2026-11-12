# B1534 ANSWER-1 (Tuesday s271, 2026-11-12, to SEAT-C94) — option (1), widened narrowly and proved by program

**Your question:** the pinned npm 10.9.8 rewrites main's lock on a no-change install (`"peer": true` added to 27 optional platform entries, blob 53305eb4 -> 03f17b45). Widen the property, find the npm that wrote main's lock, or something else?

**Answer: (1).** The pinned image's npm is the project's own toolchain (Dockerfile line 3); a lock it writes is the lock its `npm ci` agrees with. Guessing which other npm once wrote main's lock is not a measurement. Your control did exactly what it was for: it found the difference before the update was mixed into it.

**The property is widened by exactly this, and nothing else:**
1. Run the no-change install first and keep its output as the **normalised base** (`03f17b45`). Print, by program (python `-I -B`, JSON parse of both locks), that base -> normalised differs ONLY by an added `"peer": true` key on exactly those 27 entries: same key set, every other field of every entry byte-equal (version, resolved, integrity, dev, optional, os, cpu, engines, dependencies), no entry added or removed. Print the 27 entry names. Control: a planted version change in a copy of the normalised lock must be reported.
2. Then apply the update ON TOP of the normalised base exactly as your kit's Step 3b says, and run the Step 3c comparison against the **normalised base**, not main's blob: the changed-entry set must still equal the 34 of FACTS (by name), with the bots' versions.
3. The committed lock therefore differs from main by the 34 update entries PLUS the 27 flag-only lines. State both sets in STATUS, in the commit body (one sentence: "the lockfile is regenerated with the project's pinned npm 10.9.8, which also adds a peer flag to 27 optional platform entries; no version changes") and in `pr-body.txt`.
4. Every other check of your kit stands unchanged (install proof by `npm ci` in the pinned image, whole suite equal to main, builds, alerts, scans, identity, one commit, plain push).

Your Hard stop (15:00) is unchanged. **Last line on finish:** `READY B1534: <sha40> lockfile blob <sha40> paths 3`, or `STOPPED: NEEDS TUESDAY <one question>`.
