# REPORT: Datasec offload, DevMASTER to G-DRIVE (2026-10-19)

## BLUF

- **TUESDAY (step 6, added after Kam's 20:45:07 ruling):** copied and verified all EQUAL (15,826 files, 828 dirs, 1,372,683,081 bytes; sha 365/365; 1 repo equal). `ignore = Path TUESDAY` was added at `devnas.prf:147`. Removal was **refused by the same hook (STOP)**. See the STEP 6 section at the end.

- **Copy: DONE and VERIFIED.** The copy of `/Volumes/DevMASTER/!CODING/Datasec` is at `/Volumes/G-DRIVE/DEVELOPMENT WORK/DevMASTER-Datasec-offload_2026-10-19/Datasec`. Main tree plus `_case_twins/` equals the source exactly: 2,534,516 files, 335,109 dirs, 11,867 symlinks and 98,927,910,226 bytes. All 24 top-level entries are EQUAL (23 visible entries plus `.DS_Store`). The sha256 check covered 99,681 files: 99,681 PASS and 0 FAIL, with controls OK. Of the 158 repos, 155 are equal on every field. The other 3 differ only in the `status --porcelain` count, and that is caused by case-folding (section 3.5): their index, objects, refs and HEAD are identical.
- **Case twins: 35** (25 file pairs, 10 directory pairs). All are in `_case_twins/`, with `MAP.txt` holding both-side sha256 values (35/35 match).
- **Sync profile:** `devnas.prf:139` = `ignore = Path !CODING/Datasec`. It was re-verified at 22:10 with positive and negative controls.
- **Removal: NOT DONE (STOP).** The never-delete hook `pathguard.py` refused `rm -rf "/Volumes/DevMASTER/!CODING/Datasec"`. Its message is quoted verbatim in section 4. I did not work around it: no `WED_ALLOW_CROSS_TREE=1` and no quarantine move. **Datasec is still fully present on DevMASTER, and no space has been freed.**
- **Read this before re-authorising removal:** 117 of the 134 linked-worktree `.git` files in the copy hold absolute `gitdir:` pointers back into `/Volumes/DevMASTER/!CODING/Datasec/...` (section 3.6). Once the source is gone, those 117 worktrees on G-DRIVE would no longer open as git repos until their pointers are repaired. The data itself is all on G-DRIVE.

## 0. Preflight

| check | 18:33 (first agent) | 20:36 (resume) | 22:10 (pre-removal) |
|---|---|---|---|
| `pgrep` unison / devnas-sync | none | none (see note) | none |
| `lsof +D` source | rc=1, nothing open | rc=1, nothing open | rc=1, nothing open |
| rsync running | n/a | none (`pgrep -x rsync` rc=1) | none |

Note: at 20:36, `pgrep -fl unison` matched one Wednesday zsh (pid 71308) whose command line contained the string `~/.unison`. It was not a sync. `pgrep -x unison` returned rc=1, and `pgrep -fl devnas-sync` returned rc=1.

### df (1K blocks)

| when | DevMASTER used / avail | G-DRIVE used / avail |
|---|---|---|
| 18:33 before | 1,002,597,408 / 950,419,516 (52%) | 8,134,894,912 / 3,582,588,004 (70%) |
| 22:10 after (no removal) | 1,008,088,056 / 944,928,868 (52%) | 8,241,767,284 / 3,475,715,628 (71%) |

DevMASTER did not shrink because the removal was refused. Its +5.5 GB comes from other sessions' activity; Datasec was not modified. G-DRIVE grew by about 107 GB, which is the copy.

## 1. Sync profile (done by the first agent at 18:35; re-verified, not re-edited)

- Backup: `/Volumes/DevMASTER/!SYNC FILES/devnas.prf.pre-1019-no-datasec`.
- `devnas-sync.sh` line 52 has `PROFILE_SRC="$SCRIPT_DIR/devnas.prf"`, and it copies that file into `~/.unison/` on every run (lines 123-125). `Sync All Drives.command` calls `devnas-sync.sh`, so `devnas.prf` is the profile the engine actually uses.
- 22:10 re-verify: target `139:ignore = Path !CODING/Datasec` (rc=0); positive control `129:ignore = Name qa-worktrees*` (rc=0); negative control `ignore = Path !CODING/NoSuchClient` (rc=1).
- Diff against the backup:

```
129a130,139
>
> # 2026-10-19 (Kam, live board 18:22:11 AEDT, view=wednesday, verbatim): "It looks like we are
> # starting to run out of space on a more regular basis. From now on, this drive will not hold any
> # Datasec files. Keep the efficiency rules alive and offload anything old / unnecessary to G drive
> # or clear but do not sync or keep any Datasec files on this drive. Remove Datasec from this drive"
> # Datasec was copied to /Volumes/G-DRIVE/DEVELOPMENT WORK/DevMASTER-Datasec-offload_2026-10-19/Datasec
> # and removed from DevMASTER. This ignore MUST stay: without it the next sync would either propagate
> # the deletion to the NAS / T9 / laptop, or copy Datasec back onto this drive. Previous profile is
> # beside this file as devnas.prf.pre-1019-no-datasec.
> ignore = Path !CODING/Datasec
```

Caveat: the comment says "and removed from DevMASTER", but the removal was refused, so that is not yet true. I did not edit the profile again (the instruction was not to). The ignore is in force, so Datasec on DevMASTER is no longer synced in either direction.

## 2. Copy

- First run, 18:35-20:25: `/opt/homebrew/bin/rsync -aHX --info=progress2`. It was killed by SIGTERM at 99% (75.1 GB). Logs: `logs/step2_rsync.*`.
- Resume, 20:37:19-21:15:22: same command, same source (trailing slash) and same destination. **rc=0, stderr 0 bytes, final `to-chk=0/2881493`** (96,862 files transferred, 23.8 GB). Logs: `logs/step2b_rsync.log/.out/.err`.
- Case twins: copied by Python `shutil.copy2` into `_case_twins/twin_NNN/<original relative path>`, one numbered folder per twin, so no two twins can collide. 35 written: 25 files with sha256 equal on both sides (25/25), and 10 directory placeholders. 12 of the 25 file twins are byte-identical to their winner. Log: `logs/step2c_twins.out` (rc=0, stderr empty).
- `MANIFEST.txt` (2,534,516 file rows: size, relative path, and `main` or `case_twin`) and `README.txt` are in the destination parent.

## 3. Verification

Method: Python `os.scandir` walks of both trees (no symlink following), recording names, types, sizes and link targets only. Logs: `logs/step3_walk_*.err`, both 0 errors (source 2,881,492 entries, destination 2,881,457 entries). Then a casefold-keyed comparison (`logs/step3_compare.out`, rc=0, `problems: []`). For every non-colliding key it checks type, size (files) and link target (symlinks). For every collision group it matches the destination file's sha256 against each source twin to find the winner.

### 3.0 Controls (run before trusting the results)
- Compare control: a copy of the destination manifest with one file dropped and one size changed by 1 byte. The compare reported MISSING, SIZE differs and PER-FOLDER mismatch, rc=1 as expected (`logs/step3_compare_control.out`).
- sha control: a known-different pair read UNEQUAL, and a missing file was detected.
- git control: ATTIO's source HEAD compared with CypherKey/2_Project_Files' destination HEAD read UNEQUAL.

### 3.1 Totals

| | source | destination main tree | case twins | main + twins = source? |
|---|---|---|---|---|
| regular files | 2,534,516 | 2,534,491 | 25 | yes |
| directories | 335,109 | 335,099 | 10 | yes |
| symlinks | 11,867 | 11,867 | 0 | yes |
| other | 0 | 0 | 0 | yes |
| bytes (regular files) | 98,927,910,226 | 98,927,755,048 | 155,178 | yes |
| distinct casefold keys | 2,881,457 | 2,881,457 | | yes; no missing, no extra |

The main tree is short by exactly 35 entries, which is the twin count. `_case_twins/` makes up the difference.

### 3.2 Per-folder table (24 top-level entries: `ls` shows 23, plus hidden `.DS_Store`)

| top-level entry | files src / dst + twins | dirs src / dst + twins | symlinks src / dst | bytes src / dst + twins | EQUAL |
|---|---|---|---|---|---|
| .DS_Store | 1 / 1 + 0 | 0 / 0 + 0 | 0 / 0 | 24,580 / 24,580 + 0 | yes |
| _archive | 12,828 / 12,828 + 0 | 1,927 / 1,927 + 0 | 32 / 32 | 3,301,287,222 / 3,301,287,222 + 0 | yes |
| _quarantine_2026-09-28_HPSM-drive-sync-copy | 12,170 / 12,169 + 1 | 3,038 / 3,033 + 5 | 0 / 0 | 15,723,083,359 / 15,723,078,756 + 4,603 | yes |
| ATTIO | 1,352 / 1,352 + 0 | 410 / 410 + 0 | 1 / 1 | 4,642,557 / 4,642,557 + 0 | yes |
| b118 | 0 / 0 + 0 | 3 / 3 + 0 | 0 / 0 | 0 / 0 + 0 | yes |
| CLAUDE.md | 1 / 1 + 0 | 0 / 0 + 0 | 0 / 0 | 2,820 / 2,820 + 0 | yes |
| Commercial Readiness | 6 / 6 + 0 | 1 / 1 + 0 | 0 / 0 | 332,954 / 332,954 + 0 | yes |
| CypherKey | 32,778 / 32,778 + 0 | 7,171 / 7,171 + 0 | 0 / 0 | 2,093,226,696 / 2,093,226,696 + 0 | yes |
| Datasec MPS Commercial Calculator | 2,016 / 2,016 + 0 | 457 / 457 + 0 | 0 / 0 | 216,374,590 / 216,374,590 + 0 | yes |
| Datasec Security Composer | 78,246 / 78,246 + 0 | 17,781 / 17,781 + 0 | 0 / 0 | 26,435,655,095 / 26,435,655,095 + 0 | yes |
| Datasec-Sales-Tools | 5 / 5 + 0 | 3 / 3 + 0 | 0 / 0 | 838,892 / 838,892 + 0 | yes |
| Feedback_System | 37 / 37 + 0 | 20 / 20 + 0 | 0 / 0 | 171,064 / 171,064 + 0 | yes |
| HPAM | 5 / 5 + 0 | 2 / 2 + 0 | 0 / 0 | 4,440,884 / 4,440,884 + 0 | yes |
| HPSM | 34,280 / 34,268 + 12 | 6,465 / 6,460 + 5 | 35 / 35 | 16,349,407,647 / 16,349,308,290 + 99,357 | yes |
| HPSM-POC | 12,596 / 12,584 + 12 | 1,749 / 1,749 + 0 | 0 / 0 | 2,877,291,708 / 2,877,240,490 + 51,218 | yes |
| Lead_Bot | 45 / 45 + 0 | 14 / 14 + 0 | 0 / 0 | 288,659 / 288,659 + 0 | yes |
| Marketing_Collateral | 6 / 6 + 0 | 9 / 9 + 0 | 0 / 0 | 52,685,427 / 52,685,427 + 0 | yes |
| myPKI | 59,676 / 59,676 + 0 | 18,522 / 18,522 + 0 | 36 / 36 | 4,288,255,949 / 4,288,255,949 + 0 | yes |
| NexusAI | 2,251,585 / 2,251,585 + 0 | 271,991 / 271,991 + 0 | 11,742 / 11,742 | 25,770,448,243 / 25,770,448,243 + 0 | yes |
| RESEARCH | 0 / 0 + 0 | 1 / 1 + 0 | 0 / 0 | 0 / 0 + 0 | yes |
| Security Review | 13,688 / 13,688 + 0 | 2,735 / 2,735 + 0 | 0 / 0 | 1,129,077,650 / 1,129,077,650 + 0 | yes |
| Task_Dispatcher | 105 / 105 + 0 | 73 / 73 + 0 | 0 / 0 | 383,897 / 383,897 + 0 | yes |
| Vision_Sales_Portal | 23,088 / 23,088 + 0 | 2,731 / 2,731 + 0 | 21 / 21 | 679,976,250 / 679,976,250 + 0 | yes |
| Websites | 2 / 2 + 0 | 6 / 6 + 0 | 0 / 0 | 14,083 / 14,083 + 0 | yes |

The twins sit only in `HPSM` (12 files, 5 dirs), `_quarantine_2026-09-28_HPSM-drive-sync-copy` (1 file, 5 dirs) and `HPSM-POC` (12 files). Every row reads EQUAL when it is computed as source = destination + twins.

### 3.3 Case twins (35)
- 25 file pairs and 10 directory pairs. Every group has exactly 2 members, and no group mixes a file with a directory. A Unicode NFD-normalisation collision check found 0.
- The twins are in `qa-wp3r2/m1..m5` vs `M1..M5` under HPSM's `1_Project_Definition/Architecture/2026-09-10_policy-composer/` (in both HPSM and its 09-28 quarantine copy), and in `B62-QA_evidence/.../api-logs/claim1|claim2` log names under HPSM-POC.
- Map: `/Volumes/G-DRIVE/DEVELOPMENT WORK/DevMASTER-Datasec-offload_2026-10-19/_case_twins/MAP.txt`.
- Name lists from the first agent: `logs/step2_case_collisions.txt` and `logs/step2_case_collisions_detail.txt`.

### 3.4 Content sha256
- Random sample of 300 files (seed 20261019), PLUS every file under 1 MB whose name contains `.env`, `key` or `cred` (case-insensitive; 99,392 files, mostly `node_modules` matches on "key"). That makes 99,681 unique files.
- **PASS 99,681 / FAIL 0.** Collision members were excluded here because section 3.1 verified them by sha. Log: `logs/step3_sha.out`.

### 3.5 Git repos (158)
- Read-only throughout: `git -c safe.directory=* --no-optional-locks` with `rev-parse HEAD`, `status --porcelain | count`, `stash list | count` and sha256 of `for-each-ref`. Log: `logs/step3_git.out`.
- **155 of 158 EQUAL on all four fields.** 17 of those 155 are linked worktrees whose `.git` file points at a gitdir on another volume (16 on `KK_T9_External_HDD`, 1 on `Laptop-DEV`). They return the same "not a git repository" error on both sides, so those rows compare error with error. They were already broken on the source.
- **3 UNEQUAL, on the porcelain count only. HEAD, stash and refs are equal:**
  - `HPSM`: dirty 53 vs 47
  - `HPSM/_quarantine_2026-09-25_added-pre-rewrite/_extracted_2026-09-23/HPSM`: 49 vs 38
  - `_quarantine_2026-09-28_HPSM-drive-sync-copy/HPSM`: 63 vs 65
- Diagnosis (`logs/step3_git_diag.out`, `logs/step3_git_diag2.out`):
  - **All 27 differing porcelain lines lie inside the `qa-wp3r2/m1..m5` / `M1..M5` case-collision directories.** All 27 resolve case-insensitively to a source entry.
  - In all 3 repos, `.git/index` sha256, `ls-files -s`, `count-objects -v` and refs are identical on both sides. `fsck --connectivity-only` returned rc=0 on both sides.
  - The difference is git's own `lstat` on a case-insensitive volume. A path such as `M1/x.log` that is deleted or untracked on the case-sensitive source resolves to `m1/x.log` on G-DRIVE.
  - I classified these as twin-accounted, not as an OTHER difference.
  - Verbs beyond the brief's four, all read-only: `ls-files -s`, `count-objects -v`, `fsck --connectivity-only`, `config --get`.

<details><summary>Repo table (158 rows)</summary>

| repo (under Datasec/) | HEAD | dirty src/dst | stash src/dst | refs sha equal | equal |
|---|---|---|---|---|---|
| ATTIO | fae239bb6eb8 | 0/0 | 0/0 | yes | yes |
| CypherKey/2_Project_Files | 76395e4feece | 0/0 | 1/1 | yes | yes |
| Datasec MPS Commercial Calculator | 95dcd9667162 | 5/5 | 0/0 | yes | yes |
| Datasec MPS Commercial Calculator/2_Project_Files | 7f6ca4c08d9f | 0/0 | 0/0 | yes | yes |
| Datasec Security Composer | 66d54ab2ef52 | 722/722 | 0/0 | yes | yes |
| Datasec Security Composer/2_Project_Files | 0b2fca43db2e | 0/0 | 0/0 | yes | yes |
| Datasec Security Composer/_quarantine_2026-10-03_B47_mock-end-without-tiles | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/2_Project_Files/.git/worktree/ERR:fatal: not a git repository: /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/2_Project_Files/.git/worktree | ERR:fatal: not a git repository: /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/2_Project_Files/.git/worktree/ERR:fatal: not a git repository: /Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/2_Project_Files/.git/worktree | yes | yes |
| HPSM | 0c3c2ec8e2d7 | 53/47 | 0/0 | yes | NO (twin-caused, see 3.5) |
| HPSM-POC | 76bb8ba426db | 561/561 | 0/0 | yes | yes |
| HPSM-POC/2_Project_Files | 8869b1a943bd | 0/0 | 0/0 | yes | yes |
| HPSM/2_Project_Files | 580d7a21bc8c | 0/0 | 0/0 | yes | yes |
| HPSM/6_Policy_Composer | 7a477400f9b3 | 0/0 | 0/0 | yes | yes |
| HPSM/_quarantine_2026-09-25_6_Policy_Composer-pre-rewrite/6_Policy_Composer | 7a477400f9b3 | 0/0 | 0/0 | yes | yes |
| HPSM/_quarantine_2026-09-25_added-pre-rewrite/_extracted_2026-09-23/HPSM | 110efb54f91c | 49/38 | 0/0 | yes | NO (twin-caused, see 3.5) |
| HPSM/_quarantine_2026-09-25_added-pre-rewrite/_extracted_2026-09-23/HPSM/2_Project_Files | 580d7a21bc8c | 0/0 | 0/0 | yes | yes |
| HPSM/_quarantine_2026-09-25_added-pre-rewrite/_extracted_2026-09-23/HPSM/6_Policy_Composer | 7a477400f9b3 | 0/0 | 0/0 | yes | yes |
| HPSM/_quarantine_2026-10-02_composer-separation/6_Policy_Composer | 7855f10a1fdd | 0/0 | 0/0 | yes | yes |
| NexusAI/2_Project_Files | a9a8cb6e3fc6 | 267/267 | 0/0 | yes | yes |
| NexusAI/deploy-worktrees/48e092c | 48e092cfd15f | 0/0 | 0/0 | yes | yes |
| NexusAI/deploy-worktrees/9520b8c | 9520b8cca76e | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees-s37-2b2734a | 2b2734a7194b | 3/3 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/06858d7 | 06858d7cfa1b | 4/4 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/095ea0c | 095ea0cd3bb7 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/0ef10d9 | 0ef10d9ffc32 | 4/4 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/149e358 | 149e358e3f99 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/19fde0c | 19fde0cc2f3a | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/1f41edc | 1f41edcb702e | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/1faa88f | 1faa88f88498 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/1faa88f-tamper | 1faa88f88498 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/234c30b-s38qa | 234c30b15244 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/24112a3 | 24112a355775 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/24d472e-rd338parent | 24d472e010d2 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/29ea1c0 | 29ea1c0223ad | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/2b014bc | 2b014bcaae9f | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/2b2734a | 2b2734a7194b | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/2bc7ef7 | 2bc7ef78601d | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/2cd51a5 | 2cd51a571515 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/34c3e53 | 34c3e53eee12 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/36bb08b | 36bb08bbd70d | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/3b39ed1 | 3b39ed1c0b1d | 2/2 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/4322af1 | 4322af1cf9e5 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/460d264 | 460d264e01cd | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/4611a20 | 4611a207b233 | 3/3 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/463f03d | 463f03dbc73e | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/4835d59 | 4835d593c0e2 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/48e092c | 48e092cfd15f | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/48e092cfd15fca33d14ad6a293044e5f5c96b87d | 48e092cfd15f | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/4ab4182 | 4ab4182278c1 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/4e0ada2 | 4e0ada2c201b | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/4e4a630 | 4e4a630aa2ee | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/58184aa | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/58184aa/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/58184aa | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/58184aa/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/58184aa | yes | yes |
| NexusAI/qa-worktrees/5f3b0bf | 5f3b0bf36b0a | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/60a225f | 60a225f94b1b | 5/5 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/61cf342 | 61cf3428cf5e | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/6339847 | 633984761494 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/6454326 | 6454326850a0 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/6a30fcf | 6a30fcfa8766 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/6b78315 | 6b78315c5b43 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/6bb36f6-parent-s38qa | 6bb36f6297ca | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/6dc400a | 6dc400a43eb1 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/70df9fd | 70df9fdac6ed | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/7147a4a | 7147a4a8f6de | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/71adf47 | 71adf4757009 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/7568302 | 75683022f0e9 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/7a76fe3 | 7a76fe3ab307 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/7cce776 | 7cce7763b0d6 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/7df675b | 7df675bf61fe | 5/5 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/7e5faa9 | 7e5faa940c05 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/8fc919b | 8fc919b0c5d7 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/93cbdc4 | 93cbdc429aba | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/9671040 | 9671040c163a | 3/3 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/9dd3837 | 9dd383719303 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/9e4d6f4 | 9e4d6f44fa27 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/a554e52 | a554e52f7222 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/abf3986 | abf3986c283c | 5/5 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/b1cafaf | b1cafaf738dc | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/b303b1d | b303b1d15b8a | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/b446436-rd338qa | b4464361261a | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/b6cec2f | b6cec2f66b23 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/b77feea | b77feea28f4e | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/b8b72f7 | b8b72f770657 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/b982f3b | b982f3bab67b | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/badff5f | badff5f4613e | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/be2159f | be2159f84867 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/c1fe9ea | c1fe9eab8813 | 5/5 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/c342236 | c342236d3100 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/c930672 | c9306723e8c8 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/c9947dd | c9947ddd90cb | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/ca98a55 | ca98a55f4a85 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/caf1fe7 | caf1fe78ab07 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/db0c65a | db0c65a6435a | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/db0d1d6 | db0d1d67e01c | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/deploy-149e358 | 149e358e3f99 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/e6c3fca | e6c3fcaa8e9f | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/e952f3b | e952f3b945df | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/ea6378d | ea6378d94772 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/ec8506a | ec8506adc9f3 | 5/5 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/ee3c4c1 | ee3c4c1e3628 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/f876732 | f87673221636 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/fc8e779 | fc8e779b022d | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/fe4eed3 | fe4eed367b24 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/qa-worktrees/a554e52 | a554e52f7222 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/regate8-base-2b2734a | 2b2734a7194b | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s36-n63-redproof-61cf342 | 61cf3428cf5e | 3/3 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s38qa-48e092c | 48e092cfd15f | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s38qa-69e837b | 69e837bac0b3 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-ec8506a | ec8506adc9f3 | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-f618f64 | f618f64e4f6f | 1/1 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-rd333-24d472e | 24d472e010d2 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-rd333-faae2d6 | faae2d6d48ea | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-rd333-tamper | faae2d6d48ea | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-rd336-3bdf20d | 3bdf20dad67f | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-rd336-3bdf20d-tamper | 3bdf20dad67f | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-rd336-5197780 | 5197780504c3 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-rd336-70d401c | 70d401c8325a | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-t1-router-revert | f618f64e4f6f | 2/2 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-t2-serverjs-literals | f618f64e4f6f | 2/2 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-t3-vocab-widen | f618f64e4f6f | 2/2 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s39qa-t4-fallback-declassified | f618f64e4f6f | 2/2 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s40qa-rd340-05606f5 | 05606f5a22bc | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s40qa-rd340-260832c | 260832c0c80a | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s40qa-rd340-47b1a71 | 47b1a710bd93 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s40qa-rd340-9401f6f | 9401f6f03de6 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s40qa-rd340-tamper | 47b1a710bd93 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s40qa-rd340-tamper-260832c | 260832c0c80a | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s40qa-rd340-tamper-9401f6f | 9401f6f03de6 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s41qa-rd180251-7def418 | 7def4188020d | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s41qa-rd180251-9c8e63a | 9c8e63afbdbc | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s41qa-rd341-9c8e63a | 9c8e63afbdbc | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s41qa-rd341-cbc8812 | cbc8812c4f54 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s41qa-rd341-tamper | cbc8812c4f54 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s41qa-rd341-tamper2 | cbc8812c4f54 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s42qa-rd341-2b21385 | 2b21385afbf5 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s42qa-rd341-tamper | 2b21385afbf5 | 0/0 | 0/0 | yes | yes |
| NexusAI/qa-worktrees/s46qa-5e6077e | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/s46qa-5e/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/s46qa-5e | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/s46qa-5e/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/s46qa-5e | yes | yes |
| NexusAI/qa-worktrees/s46qa-731aa6e | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/s46qa-73/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/s46qa-73 | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/s46qa-73/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/s46qa-73 | yes | yes |
| NexusAI/wt-rd304 | 69e837bac0b3 | 1/1 | 0/0 | yes | yes |
| NexusAI/wt-rd306 | 000b9a0f0b9a | 1/1 | 0/0 | yes | yes |
| NexusAI/wt-s46-g2 | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-g/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-g | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-g/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-g | yes | yes |
| NexusAI/wt-s46-hist | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-h/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-h | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-h/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-h | yes | yes |
| NexusAI/wt-s46-rd323 | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-r | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s46-r | yes | yes |
| NexusAI/wt-s47-r2 | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | yes | yes |
| NexusAI/wt-s47-rd369 | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | yes | yes |
| NexusAI/wt-s47-rd376 | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | yes | yes |
| NexusAI/wt-s47-rd377 | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | yes | yes |
| NexusAI/wt-s47-rd381 | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s47-r | yes | yes |
| NexusAI/wt-s48-mkt | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s48-m/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s48-m | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s48-m/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s48-m | yes | yes |
| NexusAI/wt-s49 | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s49/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s49 | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s49/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s49 | yes | yes |
| NexusAI/wt-s49-rd363 | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s49-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s49-r | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s49-r/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s49-r | yes | yes |
| NexusAI/wt-s50-mktreview | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s50-m/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s50-m | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s50-m/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s50-m | yes | yes |
| NexusAI/wt-s51-mktremed | ERR:fatal: n | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s51-m/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s51-m | ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s51-m/ERR:fatal: not a git repository: /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/.git/worktrees/wt-s51-m | yes | yes |
| Task_Dispatcher/2_Project_Files | 8cde6c7a159f | 0/0 | 0/0 | yes | yes |
| Vision_Sales_Portal/2_Project_Files | ef5a9c0b942c | 26/26 | 0/0 | yes | yes |
| Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool | 47eb53303410 | 30/30 | 0/0 | yes | yes |
| _quarantine_2026-09-28_HPSM-drive-sync-copy/HPSM | f9fd75bedfb7 | 63/65 | 0/0 | yes | NO (twin-caused, see 3.5) |
| _quarantine_2026-09-28_HPSM-drive-sync-copy/HPSM/2_Project_Files | 580d7a21bc8c | 0/0 | 0/0 | yes | yes |
| _quarantine_2026-09-28_HPSM-drive-sync-copy/HPSM/6_Policy_Composer | 7a477400f9b3 | 0/0 | 0/0 | yes | yes |
| myPKI/2_Project_Files | 42240664a455 | 32/32 | 0/0 | yes | yes |

control: {'a': 'ATTIO', 'b': 'CypherKey/2_Project_Files', 'unequal_detected': True}

</details>

### 3.6 Worktree pointers (finding that matters for removal)
- 134 repos in the tree are linked worktrees, so `.git` is a file holding a `gitdir:` line. I checked the targets by prefix only, printing nothing:
  - **117 point to an absolute path under `/Volumes/DevMASTER/!CODING/Datasec/`** (the main repos' `.git/worktrees/<name>`, e.g. NexusAI qa-worktrees)
  - 16 point to `KK_T9_External_HDD`
  - 1 points to `Laptop-DEV`
- Consequence 1: on G-DRIVE today, those 117 worktrees resolve their git metadata through the DevMASTER source, so their destination-side HEAD and refs comparison was partly reading the source. Their working-tree files are verified independently by sections 3.1 and 3.4, and their gitdirs exist on G-DRIVE inside the copied main repos.
- Consequence 2: after the source is removed, those 117 worktrees on G-DRIVE stop being openable as git worktrees until the pointers are rewritten (`git worktree repair` from the copied main repo, or rewriting each `gitdir:` line). No data is lost, but anyone restoring them should know.

## 4. Removal: STOP (hook refusal)

Pre-removal checks at 22:10 were all clean (step 1 re-verified, no unison, devnas-sync or rsync running, `lsof` rc=1). Log: `logs/step4_preflight.log`. I then issued `rm -rf "/Volumes/DevMASTER/!CODING/Datasec"`. The PreToolUse hook refused it before execution, so nothing was removed. The source still has 23 entries, confirmed after the refusal. Verbatim:

```
PreToolUse:Bash hook error: [bash "$CLAUDE_PROJECT_DIR/2_Project_Files/fleet/hooks/pretooluse_no_cd.sh"]: REFUSED by pathguard.py: `rm` WRITES to
  /Volumes/DevMASTER/!CODING/Datasec
which belongs to another client or to the other agent's tree. This seat's root is
/Volumes/DevMASTER/WEDNESDAY.

Hard rule 1 (stay in the project folder) and rule 2 (no cross-client contamination).
Coordinators manage; the project's own agent executes. One writer per tree is the design,
not a precaution — it is why the claims files have never once conflicted.

READS are fine and are NOT gated: cat, grep, ls, git log/show/diff.
To change another project: brief its agent. To change the sister tree: it is hers.
If this is a deliberate provisioning run that Kam asked for, re-issue it with
WED_ALLOW_CROSS_TREE=1 and say so in the session note — an override used silently is an
override that stops being one.
```

I did **not** re-issue the command with `WED_ALLOW_CROSS_TREE=1`. The binding addendum says not to work around a refusal. Whether Kam's 18:22:11 instruction counts as "a deliberate provisioning run that Kam asked for" is for Kam or Wednesday to rule on. If the answer is yes, the removal is one command with the override, followed by the post-removal checks: the path is gone and the destination counts are unchanged (re-walk and expect 2,881,457 entries in the main tree).

## 5. What I did NOT do
- Did not remove the source (hook refusal above). I also did not move it to a quarantine, which is not authorised.
- Did not use the `WED_ALLOW_CROSS_TREE=1` override.
- Did not edit `devnas.prf` again. Its comment line "and removed from DevMASTER" is premature until removal happens.
- Did not repair the 117 worktree pointers on G-DRIVE (section 3.6).
- Did not compare xattrs, permissions or mtimes beyond what `rsync -aHX` itself guarantees.
- Did not run any git write verb, and did not print any Datasec file's contents. Only names, counts, sizes and hashes appear here and in the logs. The worktree-pointer check printed prefix counts only.
- Did not touch Notes (MASTER), anything under WEDNESDAY other than this folder, other `!CODING` clients, or anything on G-DRIVE outside `DevMASTER-Datasec-offload_2026-10-19/`.

---

# STEP 6: TUESDAY (Kam ruling 2026-10-19 20:45:07 AEDT, card `wed-devmaster-datasec-leftovers-1019` = a, relayed by Wednesday)

Verbatim ruling: *"Move the TUESDAY folder to G-DRIVE; leave the vault and repo files"*. Source: `/Volumes/DevMASTER/TUESDAY`. Destination: `/Volumes/G-DRIVE/DEVELOPMENT WORK/DevMASTER-Datasec-offload_2026-10-19/TUESDAY`. I started this only after the Datasec steps 2-5 above were finished and reported.

**BLUF: copy DONE and all checks EQUAL. Profile ignore added and verified. Removal REFUSED by the same `pathguard.py` hook (STOP). TUESDAY is still on DevMASTER, and from now on it is not synced.**

- **Preflight (22:00 and 22:14):**
  - du 1,378,664 KB; 35 top-level entries; 0 entries modified since 2026-10-01 (excluding `.git/`).
  - `lsof +D` rc=1; no unison, devnas-sync or rsync running. Log: `logs/step6_preflight*.log`.
- **Profile:** `devnas.prf` syncs from the drive root, and before this only `TUESDAY/2_Project_Files/local-model/models` was ignored. So TUESDAY was synced.
  - Backed up with `cp -p` to `devnas.prf.pre-1019-no-tuesday`, then appended the dated comment and `ignore = Path TUESDAY`.
  - Verified: target `147:ignore = Path TUESDAY` (rc=0); positive control `139:ignore = Path !CODING/Datasec` (rc=0); negative control (rc=1). Log: `logs/step6_profile.log`. Diff:

```
139a140,147
>
> # 2026-10-19 (Kam, live board 20:45:07 AEDT, card wed-devmaster-datasec-leftovers-1019 = a, verbatim):
> # "Move the TUESDAY folder to G-DRIVE; leave the vault and repo files". TUESDAY is being copied to
> # /Volumes/G-DRIVE/DEVELOPMENT WORK/DevMASTER-Datasec-offload_2026-10-19/TUESDAY and is to be removed from
> # DevMASTER. This ignore MUST stay: without it the next sync would either propagate the removal to the
> # NAS / T9 / laptop, or copy TUESDAY back onto this drive. Previous profile is beside this file as
> # devnas.prf.pre-1019-no-tuesday.
> ignore = Path TUESDAY
```

- **Copy:** `/opt/homebrew/bin/rsync -aHX --info=progress2`, 22:15:15-22:16:01. rc=0, stderr 0 bytes, `to-chk=0/16655`, 1,372,683,081 bytes. Log: `logs/step6_rsync.*`.
- **Controls:** the compare control (one file dropped and one size +1) gave rc=1 with 4 problems, as expected. The sha known-different pair read UNEQUAL and the missing file was detected. The git control compared TUESDAY's source HEAD with Datasec/ATTIO's destination HEAD and read UNEQUAL. TUESDAY has only 1 repo, so the in-tree control was not possible.

| | source | destination | EQUAL |
|---|---|---|---|
| regular files | 15,826 | 15,826 | yes |
| directories | 828 | 828 | yes |
| symlinks | 0 | 0 | yes |
| bytes | 1,372,683,081 | 1,372,683,081 | yes |
| case twins | 0 | | n/a |
| sha256 (300 random + 67 `.env`/`key`/`cred` files under 1 MB; 365 unique) | | PASS 365 / FAIL 0 | yes |

| repo | HEAD | dirty src/dst | stash src/dst | refs sha equal | equal |
|---|---|---|---|---|---|
| TUESDAY (root; `.git` is a directory) | 05262d342bd0 | 2701/2701 | 1/1 | yes | yes |

- **Removal: STOP.** At 22:16:54 the pre-removal checks were clean (ignore present, no sync, `lsof` rc=1). `rm -rf /Volumes/DevMASTER/TUESDAY` was refused before execution, and the source is intact (35 entries). The hook message is verbatim identical to section 4 except for the path line, which reads `  /Volumes/DevMASTER/TUESDAY`. As with Datasec, I did not use `WED_ALLOW_CROSS_TREE=1` and did not quarantine.
- **Not done:** removal; any change to Notes (MASTER) or WEDNESDAY. `MANIFEST.txt` covers Datasec only. The README has a TUESDAY paragraph.
