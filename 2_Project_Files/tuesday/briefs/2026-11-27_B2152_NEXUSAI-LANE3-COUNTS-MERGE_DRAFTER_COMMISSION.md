# B2152 DRAFTER COMMISSION (in-session, READ-ONLY, Sonnet) -- Datasec/NexusAI: a short BUILD kit for seat N185: merge main into b2143/lane3-kit1 and regenerate the counts (gate B2150's landing step 0b)

Commissioned by Tuesday (s333). `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` binds whole.

**Model:** Sonnet seat (spelled-out edit, no design), launch line with `CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude` inside the quotes.

**Form:** read whole, and copy the lock wrapper, the dot-free trees, the clone and identity steps and the push rules from:
- kit `2026-11-27_B2143_SEAT-N184_nexusai-lane3-kit1.md` (the branch's own kit) with its ADDENDUM-1;
- kit `2026-11-27_B2142_SEAT-N183_nexusai-lane2-kit2-round2.md` (a fast-forward push of an existing pushed branch).

**Write only:**
- the kit `2026-11-27_B2152_SEAT-N185_nexusai-lane3-counts-merge.md` and its `.measured`;
- `2026-11-27_B2152_DRAFTER-REPORT.md`;
- scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/d2152/`.

**Return:** 10 lines, `STARTABLE: YES|NO` first, then Questions with defaults.

## The job: gate B2150's landing.txt step 0b, token for token
Source: `tuesday/briefs/2026-11-27_B2150_verify/landing.txt` lines 10-36. Read the whole file.
- **Branch:** `b2143/lane3-kit1` at K `895da3f4630e170e038a1b5b2c78008ae7633b93`, three commits on BASE `279b2235`.
- **Main:** now `de39619cac31e475fe46350e29bdb3047b86e046`, the PR 267 merge. Tuesday read it after landing; re-read it.
- **The merge:** in the seat's own clone, `git merge --no-ff --no-commit <main sha>`. Expect exactly one conflict, in `scripts/verify-expected-counts.json`. Any other conflicted path is a STOP.
- **The counts:** resolved only by the project's own command, `npm run verify -- --maxWorkers=2 --update-counts`, in a dot-free tree inside the NexusAI jest lock.
- **The pair:** must be 6634 / 419 (6606 + 28, 417 + 2; PREDICTED). Any other pair is a STOP naming both.
- **Commit message:** "RD-1016 RD-1015: merge main; suite counts 6634 tests in 419 suites, written by the project's own command".
- **Push:** a plain verify at the merge commit, then ONE fast-forward push of the branch (never force).
- **Landing:** no PR. Tuesday opens it from B2150's texts, with the body line its landing.txt line 51 names.

## Draft and dry-read, measuring what you can
- **No jest lock is held now:** no NexusAI seat is live. If the lock base shows no holder, you MAY prove the merge's conflict set in a scratch clone (git only; no jest run).
- **Measure the merge result's file list:** compare BASE...merge. Exactly B2143's six paths should differ from main once merged, plus the two counts lines.
- **Name what the gate's reads still cover** after the pin moves from K to the merge commit: the gate read K's tree, and the merge adds only main's files and the counts. Write it as landing.txt does.
- **Questions:**
  - The seat commits the merge (default yes).
  - Sonnet seat (default).
  - Hard stop: about 90 minutes predicted (clone and npm ci, one update run, one plain verify; each whole-suite run about 22 minutes).
