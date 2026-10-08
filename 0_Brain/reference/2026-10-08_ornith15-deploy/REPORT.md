---
date: 2026-10-08
type: reference
source: Ornith-1.5 deploy builder (background agent), text saved by Wednesday because the agent's own write was refused; headline facts re-verified by Wednesday at source 18:4x
---
# Ornith 1.5 deployed as the night runner's default (Kam 18:12 ruling)

## BLUF
- `night/night_run.sh` defaults to `NIGHT_BACKEND=omlx` and `NIGHT_MODEL=Ornith-1.5-35B-A3B-MLX-8bit` (`:71-73`, read by Wednesday). Ornith 1.0 stays the explicit fallback (`NIGHT_BACKEND=ollama`, `ornith:35b`). It never switches by itself.
- New tracked files: `local-model/omlx_serve.sh` (start/stop/status/clear-trip; port 47780 only; memory guard; generic via `OMLX_MODEL`/`OMLX_MODEL_SRC`), `local-model/lib/omlx_call.py`, `local-model/omlx/settings.template.json` (memory tier `balanced`; no secrets: every key is null or empty, checked by Wednesday).
- Changed files: `night_run.sh`, `local_model_task.sh`, `doctor.sh`, `PORTABILITY.md` (item 23), `.gitignore` (`local-model/omlx/state/`), `local-model/README.md`. Each has a `.pre-1008-ornith15` backup beside it.
- **Proofs (builder's outputs):**
  - **Fire:** KS-1110 r2 through the runner's own path on 1.5 gave `RESULT: PASS (7/7)` twice, once with the runner auto-starting the server; the output was byte-identical to the A/B.
  - **Fallback:** `NIGHT_BACKEND=ollama` refused loudly with Ollama down.
  - **Refusal:** three cases (autostart off, a guard trip on record, the wrong model on omlx), each `END rc=3`, with no silent switch.
- **Found:** the A/B's 65536 context cap was never in effect, because oMLX 0.7.0 also needs `sampling.max_context_window_policy`. It is now set, and oMLX reports 65536. The model loads at the first request, so `start` preloads it. Its memory shows as WIRED, not RSS. `~/.omlx/bin/omlx-cluster-python` is a 4-line shell script, not a symlink; PORTABILITY describes it correctly.
- **OWED (outside the builder's brief):** `night/hold_ready.py` labels READY files `ornith35b-q4` unless `--model-tag` is passed, and `night/retry_when_load_allows.sh` calls `local_model_task.sh` without `LM_BACKEND`, so it would run 1.0.
- **End state:** oMLX STOPPED (port 47780 free; Wednesday's lsof showed 0 listeners); swap 922.06M; memory_pressure 92% free. The real `night/queue.md` and `done.md` were untouched (Wednesday's `git diff --stat`: empty). The proofs ran in an isolated `omlx/state/proof/`.
- **NOT TESTED:** a real 1.0 run through the new code (Ollama down); a real guard trip or HTTP 507 (simulated only); long runs and SSD-cache growth; prompts over 28K tokens on the capped server; the 23:30 and 15-minute jobs with no seats live. The 15-minute launchd loop already runs the new code: its 18:36:49 fire refused at G2 because Secuura panes are live.
