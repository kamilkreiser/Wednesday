STARTABLE: YES (after the stamp: 8 four-underscore slot lines, and rulings on D-1 to D-5)

# B1039 drafter report: SEAT-R110, Composer demo pg_restore / psql version + db image digest read

**BLUF.** I drafted a read-only kit that copies the recorded route: identity check, then `az vm get-instance-view`, then ONE `az vm run-command invoke -g HPSM-DEV-RG -n hpsm-demo-vm --command-id RunShellScript` under the Composer project's own `AZURE_CONFIG_DIR` (tenant `d500ebad…`, subscription `0c57ab37…`). The script is 14 lines and pinned by sha256 `5f0a34c7…0046`. It checks the host, confirms the container `hpsm-demo-db-1` exists and is running, then runs `pg_restore --version`, `psql --version` and `docker inspect --format '{{.Config.Image}} {{.Image}}'`. Nothing else. The records already strongly suggest the answer is CLOSED. The db container was created on 2026-09-14 and was not recreated by B986. Its image id's first 12 hex characters `f1c3376c26f2` equal the compose pin's, and the pin has been unchanged since 2026-09-10. The kit still requires today's full reading.

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1039_SEAT-R110_composer-demo-pgrestore-version-read.md` (101 lines, sha256 `ba96de21…c82e`). The `.pre-stamp` copy beside it is byte-equal (cp -n, cmp equal, same sha256).

## Facts (instrument + control)
- **Authority.** `decision_queue.sh show composer-demo-pgrestore-version-read-1101`: status ruled, choice `a`, `ruled_ts` 2026-11-01T12:20:01.452328+11:00. The detail line is quoted verbatim in the kit. The card id is NOT written in the kit; slot 2 is for Tuesday.
- **B1039 unused.** `ls briefs | grep -i -c B1039` = 0 and the Composer `Briefs/` count = 0. Control: `B1038` = 3.
- **R110 unused.** The highest `SEAT-R` in briefs is R109 (B1033). `grep -r -l -i 'SEAT-R110|-R110'` over briefs and Tuesday daily notes found 0 files. Control: R109 found 2 files.
- **Route.** I found the route in the records and did not invent one. Sources: `Briefs/2026-10-16_B155_STATUS.md:55` (identity, VM, RG) and `:97` (the invoke), `B287_STATUS.md:20,52` (a read-only use, rc 0), `B986_STATUS.md:105` (Step 2 read, no SSH), `B986_evidence/identity_and_nsg_before.txt:3-5` (equal=YES on 10-31), and `CLARIFICATIONS.md:1408` (VM/RG).
- **Pin.** Local `git show d70edf70:compose.yaml` and `origin/main:compose.yaml` line 18 both read `postgres:16@sha256:f1c3376c…6f94`. `git log -S<digest>` gives 1 commit, 09622b62, dated 2026-09-10. `6e69886d` is MISSING from the local clone (it was not fetched, and I fetched nothing).
- **Overlay.** It does not override the db image: `B287_evidence/runs/R1-A3-vm-read.txt`, lines 14-15 of the printed overlay. `docker ps` showed `postgres:16` (`:48`).
- **Image store.** The VM reports `.Image` as the registry digest. Evidence: the objects image_id equals its RepoDigest (`R1-A3-vm-read.txt:54,56`).
- **Parser.** I tested it on 5 planted lines, including `16.9` resolving to REAL. The numeric compare was the trap, and it passes.
- **Script.** `sh -n` passes. I extracted the script from the kit with the kit's own awk line and its sha256 matched.

## D-decisions (in the kit; Tuesday rules in slot 6)
D-1: three reads (card names one). D-2: accept the run-command residue. D-3: identity is the user account (no Composer SP exists). D-4: the pin comes from the local repo, not a VM file. D-5: Opus on row C6 line 96, with Sonnet (B287 precedent) as the alternative.

## Q-questions (defaults)
- Q-1: Do `psql --version` and the image line stay inside the card's "one read-only command"? Default: yes, same single invoke.
- Q-2: Is the user identity acceptable given workspace rule line 25 (per-project principals)? Default: yes, as on 10-31.
- Q-3: Opus or Sonnet? Default: Opus.

## UNMEASURED
The versions; the full 64-hex `.Image`; whether the VM is running now; whether 16.x on the demo actually writes the key lines (this seat produces no restore script); and whether "16.10" is the true threshold (B1037-2 notes it is unsourced in-house).

## Outside the fences
None. I wrote 3 files under `briefs/`: the kit, its `.pre-stamp` and this report. Scratch copies stayed in the session scratchpad. The kit contains the account email `kreiser.org@me.com`, because the route's identity assertion needs it, as in every earlier kit. Strike it if the no-names rule covers it.
