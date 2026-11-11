# RE-COMMISSION — five-model A/B, Wednesday (07:5x relaunch seat), 2026-11-12 ~07:58 AEDT

Kam approved the relaunch plan at ~07:57 (live terminal: "good plan.  go ahead").

## Why this exists
The first operator (commissioned ~07:4x) DIED at ~07:49 when macOS restarted the Mac mini without approval. Nothing it held in memory survived. Read `commission.md` in this folder WHOLE: it is still the commission, unchanged. This file adds only what the dead operator left behind.

## What the dead operator left (measured by Wednesday 07:52-07:58; re-verify each before you rely on it)
- `serving_state_before.txt` (this folder): the Spark's serving state recorded 2026-11-11T20:44:53Z = 07:44 AEDT. The container was `deepseek-v4-flash-spark-deepseek-v4-flash-1`, the model `deepseek-v4-flash-0731`, port 8888, and the restore method is `docker start` (stop, never rm). **Re-record it yourself before any swap.** Do not trust a file written by a process that died.
- `2_Project_Files/local-model/spark-ab/ab.py` was EDITED in place by the dead operator (the commission said copy-and-mv). The backup is `ab.py.pre-1112-fivemodel`, the 10-27 version. Its diff adds the arms `mimohosted`, `nemotron`, `kolibri`, `lfm25` and `dsv41iq1s`, and threads `mk` through `assert_or_routing` / `post_hosted`. Read that diff whole and judge it. KEEP it only if `--model control` reproduces all 23 recorded verdicts with it. Otherwise restore from the backup by copy-and-mv and redo the arms yourself.
- `results_control_recheck1112.tsv` is PARTIAL: T01-T09 only, 07:46:57-07:48:10, cut off by the reboot. It is NOT a passed control. Re-run `--model control` in full.
- At 07:52 the Spark was serving `deepseek-v4-flash-0731` (`/v1/models` returned 200 through the tunnel, re-opened by Wednesday with `local-model/spark/tunnel.sh up`). spark_status showed queue 0, drainer not running, no round.
- **The Spark did NOT reboot, only the mini did.** Anything the dead operator started ON THE SPARK (an `hf download`, a `docker pull`, a nohup'd process, a partial weights folder) may still be running or half-written there. Before anything else, check the Spark's process list, docker ps -a, and any folder named for this test. Report what you find. Never delete one: a half-written download is quarantined or resumed, never removed.

## Kam's later words that bear on this (context only, not new scope)
- 07:45:29 (live): combining the 128 GB Spark and the 256 GB Studio. That needs the Studio, which is not here: OUT of this commission.
- 07:50:57 (live): "would v4.1 fit on 3 connected spark?" Wednesday answered him with arithmetic. It is not a test request: OUT of this commission.

Everything else (box discipline, the restore + T01 proof, the $10 OpenRouter cap, the privacy pins, the output, the constraints) is exactly as `commission.md` states.
