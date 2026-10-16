# B156 drafter report · MPS hosted deploy of main 0f8ad97 (seat K)
Drafted 2026-10-16 ~13:50 AEDT. Brief: `2026-10-16_B156_SEAT-K_mps-hosted-deploy-0f8ad97.md` (this folder). Nothing launched, sent or written outside these two files. Read-only git (no fetch), `gh api` GETs only (project GH_CONFIG_DIR), no az, no HTTP to the site.

## Measured
- main = `0f8ad97…` (API 02:43Z); tree `424daeeb…`; parent chain 0f8ad97 → 7af91dec → e2990622 → b9a3d769. Compare b9a3d769...0f8ad97: ahead 3, behind 0, 24 files, +2,071/−82. Nothing changed under infra/ scripts/ .github/ tools/; appsettings 0; `migrat` 0; MpsCalc: keys 13 = 13 (14 = 14 in the wider form).
- Check-runs on 0f8ad97: 8/8 success (ci 38840260381, CodeQL 38840260021, 4 languages). Open code-scanning alerts on main: 0. The CI package artifact exists (2,866,388 B, not expired).
- Live = b9a3d769 per B92 STATUS:188. Briefs from 10-14 to 10-16 and history.md record no deploy after it. B99 read hosted feedback today (Kudu GET only): 4 items, two with screenshots.
- Rollback package: B92's `.tools/wt-B92-release/…/mpscalc.zip` re-hashed = `2e62263f…`, 2,859,845 B, 48 files, worktree clean at b9a3d769.
- Words: B97's approved strings sit at `rental.ts:52,53,56,147` at 0f8ad97. B92's 10 strings are all still in source. B94 retired `For purchase quotes only: …`.

## Adaptations from B92 (deliberate)
1. **Preferred package = the CI artifact** (`deploy-from-ci.sh fetch`, run 38840260381). The seat now has a gh login, and B92 built locally only because it had none. This also avoids a heavy dotnet+npm build at load ~195. If `fetch` fails, the seat falls back to B92's local package.sh.
2. **No 48-file expectation.** B98 FOUND 4 adds 2 Pkcs dlls. The seat diffs the file list against the rollback zip and STOPs on any other non-wwwroot add or remove.
3. **Rollback target = b9a3d769** (B92's package). B92's E-2 one-way warning does not apply, because no store code changed in the range. The precondition is still kept.
4. **The words check covers the bundle only.** A rendered rental proposal is UNMEASURED by design: rendering one needs a proposal GET, which writes an event (a B38 HOLD).
5. **MPS-LANES ADDENDUM-3 holds were added** because ten lanes share the .git and the process table.

## Traps for Tuesday before launch
- **The `.tools/` paths are the PROJECT ROOT's** (`<project>/.tools/wt-B92-release`, `qa-B92`, `backup-B92`), not `2_Project_Files/.tools/`. The latter holds only the lanes' worktrees. The brief says this, but a seat that guesses wrong will "find" no rollback package.
- **Main may move during the lanes' work.** If lane PRs merge before the seat reads assert 1, the brief STOPs; it never deploys a newer sha. Merge nothing on MPS main until B156's last line.
- **Kam's K-20 rename** ("Rental (monthly)" → "Finance (monthly)", ADDENDUM-1) is NOT in 0f8ad97. The hosted site will still show the old quote-type names.
- **The CI artifact expires 7 days after 02:30Z today.** Launch well before then, or the seat falls back to a local build.
- The hosted feedback now holds Paul's screenshots, which go into the backup zip. The brief forbids opening or printing them, and the backup sits in a git-ignored folder (`check-ignore` rc 0, `.gitignore:29`).
- **The `/2` feedback rollback condition:** any new feedback or quote after the backup turns a needed rollback into STOP: NEEDS TUESDAY. That is conservative but intended.

## UNMEASURED by the drafter
Hosted store counts, served bundle today, new package's size/sha/file count, hosted ASP.NET runtime version, the rendered book.
