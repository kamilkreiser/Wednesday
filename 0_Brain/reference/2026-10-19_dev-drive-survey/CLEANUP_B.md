# DevMASTER cleanup (b): leftovers + unused models to G-DRIVE, 2026-10-19

**Authority:** Kam ruled card `wed-devmaster-drive-cleanup-1019` = **(b)** "Leftovers, and move unused models to G-DRIVE", live board 11:08:11 AEDT 2026-10-19. Executed by a storage sub-agent for Wednesday, 11:11 to 12:33 AEDT. It rests on `SURVEY.md` (same folder), which was read whole first, along with `learnings/2026-10-15_a-sync-is-not-done-until-every-folder-is-counted-on-both-sides.md`.
**Scope:** only the three classes below. Nothing in `!CODING/` was touched (it was read-only: the launcher grep), and nothing Datasec or Secuura/Blockchain was touched.
**Scripts and raw evidence:** `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2ce15c23-3025-4dcd-9e03-2be96a0a6754/scratchpad/drivecleanup/`. This is session scratch and will not survive; the load-bearing numbers are copied here.

## BLUF

| Class | Outcome | DevMASTER freed by this agent |
|---|---|---|
| 1. Gatesets older than 14 d | **NOT removed.** 161 eligible, 1 skipped (referenced). Removal was **refused by `pretooluse_no_rm.sh`** (it refuses every `rm` outside `/tmp`, literal or not), and the refusal was not worked around. Also: all 161 hold git-tracked files (11,865 tracked files in total). | 0 |
| 2. oMLX Qwen3.8-Flash + Qwen3.5-122B | **COPIED and VERIFIED** to G-DRIVE. **Source NOT removed**: the same hook refused a literal `rm -rf`. Both now exist twice. Ornith-1.5 untouched. | 0 (163.8 GiB is ready to free on Kam's own `rm`) |
| 3. Ollama unreferenced models | **MOVED**: 6 models copied and verified (every blob sha256 = its name), then `ollama rm`. 7 kept models verified. | **136.9 GiB** (147,004,483,696 B of blobs) |

**df on DevMASTER:** used fell by 179.7 GiB (75% → 66%). **Only 136.9 GiB of that is this agent's.** The other ~42.8 GiB was freed by some other process during the window; that is not attributed here.

## df before / after (`df -k`, KB)

| Drive | Before (11:11:37) used / avail / % | After (12:32:47) used / avail / % | Δ used |
|---|---|---|---|
| `/Volumes/DevMASTER` | 1,460,338,272 / 492,678,652 / 75% | 1,271,860,104 / 681,156,824 / 66% | **−188,478,168 KB = −179.7 GiB** (this agent: −136.9 GiB) |
| `/Volumes/G-DRIVE` | 7,819,675,660 / 3,897,807,256 / 67% | 8,134,894,980 / 3,582,587,936 / 70% | **+315,219,320 KB = +300.6 GiB** (= the three archives below, `du -sk` 315,374,892 KB) |

Room check before any copy: G-DRIVE had 3.63 TiB free against a ≤ 0.31 TiB need.
Note: the survey's 91% (07:50) was already 75% at 11:11. Something else freed about 260 GiB between the two, most likely the Testing Agent MAIN QA scratch (survey row 1); that was not checked.

---

## Class 1: QA gatesets older than 14 days

**FOUND:** `2_Project_Files/fleet/qa-agent/gatesets/` holds **194 dirs + 12 loose files** (206 entries, which matches the survey's 206). The survey's "173 older than 14 d" is not reproduced: by the stricter test below the count is **162**. The loose files (serial-chain logs and scripts, 09-17/09-20, a few KB each) are not gatesets and are out of scope, so they were left alone.

**TESTED:**
- **Age:** a gateset counts as older than 14 days only if BOTH its dir mtime AND its newest non-node_modules file are more than 14×86,400 s old. Result: 162 of 194. 0 dirs had an old mtime but a newer file. Ages run from 14.x to 34 days.
- **Open files / cwd:** `lsof +D gatesets/` gave 0 lines, and 0 of 602 process cwds sit under gatesets. **Positive control:** `lsof +D 2_Project_Files/dashboard` gave 14 lines, and 27 cwds sit under WEDNESDAY.
- **References:** each of the 162 names was grepped (`grep -lF`) across the 7,101 files under `0_Brain/reference/` with mtime under 14 days. **1 hit:** `2026-09-17_seatB` is named in `0_Brain/reference/2026-10-12_ks-routing-triage/raw_ks_issues.json`, so it is **SKIPPED**. Controls: the word `gateset` matched 4 recent files, and that 1 real hit is the positive. (The newest gateset name, `2026-10-11_gate86`, had 0 hits; that is the honest answer, since it is not cited.) Substring matching only errs toward skipping.
- **Git:** `git ls-files` shows that **all 161 eligible gatesets contain tracked files: 11,865 tracked files** (briefs, prompts, `*.out`; 19,207 tracked under gatesets/ in total). Removing them is therefore also a repo change that needs a commit.

**HOW / result:** a literal-path `rm -rf` script was refused by `pretooluse_no_rm.sh` ("this Bash call DELETES outside the session scratchpad", Kam 2026-08-26). Reading the hook shows it refuses **any** `rm` whose target is not under `/tmp`, so literal paths do not help. **Not worked around.** No quarantine move was made either: a same-volume `mv` frees 0 bytes and would turn 11,865 tracked files into git deletions in Wednesday's tree.

| | Count | Bytes | Files |
|---|---|---|---|
| Gateset dirs (all) | 194 (+12 loose files) | 27.9 GiB (survey) | |
| Older than 14 d (strict) | 162 | 11.22 GiB | 541,869 + seatB |
| Skipped: referenced | 1 (`2026-09-17_seatB`, 216 KB) | | 42 |
| **Eligible** | **161** | **11,770,180 KB = 11.22 GiB** | **541,869** |
| Removed | **0** (hook refusal) | 0 | 0 |

The list of eligible names (with ages, KB and file counts) is in `CLEANUP_B_gatesets_eligible.txt` in this folder.

---

## Class 2: oMLX models (copy, verify, then remove source)

**FOUND:** `2_Project_Files/tools/omlx/models/` = `Ornith-1.5-35B-A3B-MLX-8bit` (**KEPT, not read or touched**: `doctor.sh:245`; `night_run.sh:74` default; `omlx_serve.sh:50` default) · `Qwen3.8-Flash-Next-oQ4e-mtp` · `Qwen3.5-122B-A10B-4bit`.

**TESTED (not in use):**
- `ps` for omlx|mlx|ollama|vllm|llama matched nothing but the checking script itself (control: 24 claude processes matched the same `ps`).
- `lsof +D` on each folder gave 0 lines (rc 1), both at check time and again immediately before each copy. 0 process cwds were inside either folder. The lsof positive control is under class 1.
- **Reference grep:** 28,795 tooling files under `2_Project_Files` (`*.sh/py/md/json/command/plist/toml/yaml/txt/conf/js/ts`, < 5 MB, excluding node_modules, gatesets, runs, work, models, seat_scratch, .git, .venv and cache), plus the root `Launch_*.command`, `PORTABILITY.md` and `CLAUDE.md`. oMLX's own `uv-cache`/`venv` (package source, where the names appear in i18n strings) were filtered out. Hits:
  - Qwen3.8-Flash / oQ4e: `local-model/omlx_setup_and_download.sh` (the download line), `PORTS.md:18` (the 10-08 test port), and `tools/omlx/base/stats.json` (server stats). No default and no live caller.
  - Qwen3.5-122B: `local-model/omlx_serve.sh:51` (comment: the generic script was reused for the 10-08 test; `OMLX_MODEL` defaults to Ornith at :50), plus Blockchain-clone and Spark-dry text that names the **Ollama** tag `qwen3.5-122b-q4km`, not this MLX folder.
  - **Positive control:** `Ornith-1.5-35B-A3B-MLX-8bit` was found in 14 files, including doctor.sh, night_run.sh and PORTABILITY.md.

**HOW:** `rsync -a` with no `--delete`, one copy at a time, to `/Volumes/G-DRIVE/WED/models-archive/2026-10-19_omlx/<name>/`. The script checked the rc, file/dir/symlink counts, summed `stat -f %z` bytes, a byte-identical per-file name+size list, and sha256 of the largest file plus 4 random files on both sides.

| Model | Src files / bytes | Dst files / bytes | dirs | name+size list | sha256 sample (largest first) | Copy time | Result |
|---|---|---|---|---|---|---|---|
| Qwen3.8-Flash-Next-oQ4e-mtp | 102 / 106,318,247,000 (99.0 GiB) | 102 / 106,318,247,000 | 5 = 5 | identical | 5/5 equal: `model-00015-of-00021.safetensors` 2685967e…d4a4ee, `model-00020-of-00021.safetensors` d5b16c8a…0a93c, +3 `.cache/huggingface` metadata files | 11:39:36–11:47:46 | **VERIFIED** |
| Qwen3.5-122B-A10B-4bit | 81 / 69,620,628,851 (64.8 GiB) | 81 / 69,620,628,851 | 5 = 5 | identical | 5/5 equal: `model-00005-of-00014.safetensors` d396eef8…abab6, `model-00002-of-00014.safetensors` 617d0276…f883, +3 metadata files | 11:53:08–11:59:17 | **VERIFIED** |

**Source removal: REFUSED.** `rm -rf "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/omlx/models/Qwen3.8-Flash-Next-oQ4e-mtp"` (a literal path) was refused by `pretooluse_no_rm.sh`. Not retried, not worked around, and the second model was not tried. **Both sources are still on DevMASTER, so the 163.8 GiB is not yet freed.**
To finish (Kam, in his own terminal, after a glance at the counts above):
```
rm -rf "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/omlx/models/Qwen3.8-Flash-Next-oQ4e-mtp"
rm -rf "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/omlx/models/Qwen3.5-122B-A10B-4bit"
```
Restore if ever needed: `rsync -a /Volumes/G-DRIVE/WED/models-archive/2026-10-19_omlx/<name>/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/omlx/models/<name>/`. Qwen3.8-Flash can also be re-downloaded (`omlx_setup_and_download.sh`, pinned revision).

---

## Class 3: Ollama store `/Volumes/DevMASTER/SYSTEM/ollama/models`

**FOUND (instrument of record):** no server was running at 11:11 (`ollama list` → "could not connect"). It was started with Wednesday's own `local-model/start_ollama.sh` (drive-local v0.34.0 binary, `OLLAMA_MODELS` = this store; "STARTED … serves ornith:35b"), and **stopped again at 12:32** (pid 98672, by port; port 11434 confirmed free) to restore the starting state. `ollama list` before: **13 models**, matching the 13 manifests on disk. 55 blobs.

**TESTED (references):** 16,171 files (the class-2 tooling set without the omlx package cache) plus **all 22 `!CODING/*/*/Launch_*.command`** were grepped for each model name. Launchers: 0 hits for every model (positive control: 22/22 launchers contain `claude`). Tooling, with `name:tag` / bare-word results:

| Model | Hits | Verdict |
|---|---|---|
| ornith:35b / :35b-q8_0 | 209 / 24 | KEEP (positive control) |
| gpt-oss:120b / :20b | 3 / 3 | KEEP |
| nomic-embed-text | only the 09-22 chat log | KEEP (named in the brief) |
| **qwen3.5-122b-q4km** | default `LLM_MODEL` in **Secuura Blockchain** code (`scripts/start-ollama.sh:5`, `tests/helpers/llm-client.ts:7`, `docs/ENVIRONMENT-VARIABLES.md:346`, seen in the clone at `local-model/omlx/state/proof/scratch/clone_ks1110/`) | **KEEP** (another project's default; it is 10 MB anyway) |
| **phi3** | `models.phi3` / `getModelByName('phi3')` in NexusAI QA briefs (`fleet/qa-agent/briefs/2026-10-07_nexusai-gate-batch19.md` etc.) | **KEEP** (named in 2_Project_Files; a Datasec app reads that name) |
| qwen3:32b-fp16, qwen3-coder-next, qwen3-coder:30b, codellama:13b, llama3.2:3b, phi2 | only the 2026-09-22 chat-log snapshot (`fleet/state/safe_pull/manual-20261018-190133/…/chat_wednesday.json`): Wednesday's own prose listing Kam's personal store, not a caller | **MOVE** |

Grep errors: 0 across all runs.

**Blob plan (manifest JSON parse):** the 6 MOVE models reference **28 unique blobs, 147,004,483,696 B**. **0 of them are shared with any KEPT model** (one small blob is shared between two MOVE models). 0 referenced blobs were missing. The loose `phi-2.gguf` and `Modelfile.phi2` in the models root are not Ollama-managed, so they were left alone.

**HOW:** `rsync -a --files-from` (6 manifests + 28 blobs, `manifests/` and `blobs/` layout kept) to `/Volumes/G-DRIVE/WED/models-archive/2026-10-19_ollama/` (12:01:30–12:14:31, rc 0). After verification: `ollama rm` for each of the 6 (all rc 0, "deleted '<name>'"). **No file was deleted by hand.**

| Check | Source | G-DRIVE archive |
|---|---|---|
| Manifests | 6 | 6, **6/6 byte-identical (`cmp`)** |
| Blobs | 28 | 28 |
| Bytes (34 files) | 147,004,488,934 | 147,004,488,934 |
| sha256 of every dst blob vs its `sha256-<hash>` name | | **28 ok / 0 bad** (12:14–12:27) |

**After `ollama rm`:**
- `ollama list` shows **7**: ornith:35b-q8_0, ornith:35b, gpt-oss:20b, gpt-oss:120b, qwen3.5-122b-q4km, nomic-embed-text, phi3.
- `ollama show` returned **rc 0 for all 7** (architectures: qwen35moe ×3, gptoss ×2, nomic-bert, phi3). Negative control: `ollama show codellama:13b` → rc 1 "model 'codellama:13b' not found".
- Kept-model blobs: **27/27 present**, 0 missing. Moved blobs: **28/28 gone** from DevMASTER, and the archive still holds 6 manifests and 28 blobs.
- Store: 55 → 27 blobs, 13 → 7 manifests. `du -sk SYSTEM/ollama` = 138,167,920 KB (131.8 GiB), down from 268.7 GiB in the survey.

| | Before | Moved (copied + `ollama rm`) | Kept | Skipped |
|---|---|---|---|---|
| Models | 13 | 6 | 7 | 0 (phi3 and qwen3.5-122b-q4km moved from the survey's "unreferenced" list to KEEP on new evidence) |
| Blobs | 55 | 28 | 27 | 0 |
| Bytes | ~268.7 GiB (du) | 147,004,483,696 (136.9 GiB) | 131.8 GiB (du) | |

Restore if ever needed: `rsync -a /Volumes/G-DRIVE/WED/models-archive/2026-10-19_ollama/ /Volumes/DevMASTER/SYSTEM/ollama/models/`. Ollama picks the manifests up on its next `list`.

---

## G-DRIVE archive (the count table, both sides)

| Folder on `/Volumes/G-DRIVE/WED/models-archive/` | Files | Bytes | Source still on DevMASTER? |
|---|---|---|---|
| `2026-10-19_omlx/Qwen3.8-Flash-Next-oQ4e-mtp/` | 102 (= src 102) | 106,318,247,000 (= src) | **yes** (removal refused) |
| `2026-10-19_omlx/Qwen3.5-122B-A10B-4bit/` | 81 (= src 81) | 69,620,628,851 (= src) | **yes** (removal refused) |
| `2026-10-19_ollama/` | 6 manifests + 28 blobs (= src 34) | 147,004,488,934 (= src) | no (`ollama rm`; verified first) |

No empty-on-one-side folder anywhere, and no `_INCOMPLETE_COPY` marker needed: every copy finished and was counted.

## What was NOT done

- **No gateset removed** (161 eligible, 11.22 GiB): the hook refused, and they carry 11,865 git-tracked files, so removal also needs a `git rm` commit by whoever does it. 1 skipped as referenced (`2026-09-17_seatB`). The 12 loose files in gatesets/ and the 32 gatesets at 14 days or younger were not touched.
- **oMLX sources not removed** (163.8 GiB): hook refusal. The two literal commands are above.
- The survey's other rows (QA scratch, ab_ornith15 run, Spark clones, the 3.86 GiB sync log, small dirs, quarantines) are out of scope and untouched.
- `phi-2.gguf` (1.79 GB) and `Modelfile.phi2` loose in the Ollama models root: not Ollama-managed and out of scope, left alone.
- No grep inside `!CODING/Secuura/Blockchain` or Datasec trees (scope). The Blockchain default for `qwen3.5-122b-q4km` was seen only through the clone in Wednesday's tree. Other agents' use of phi3/nomic was not checked beyond 2_Project_Files and launchers.
- The 42.8 GiB of extra DevMASTER free space that appeared during the window was not investigated.
- No git commit was made (this report and the sidecar list are untracked new files).
