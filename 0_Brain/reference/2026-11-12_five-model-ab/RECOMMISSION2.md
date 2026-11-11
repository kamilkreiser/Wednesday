# RE-COMMISSION 2: five-model A/B, HOSTED ARMS + the Spark T01 proof. Wednesday, 2026-11-12 ~09:1x AEDT

Read WHOLE first: `commission.md` and `RECOMMISSION.md` in this folder (the commission and its constraints all stand), then the previous operator's final report. That report was returned to Wednesday, not written to disk because the drive dropped; its facts are summarised here.

## State from operator 2 (died at the 08:40 DevMASTER drop; the drive was back at 08:56 and again at 09:07)
- ab.py is FINAL and committed. It has the five arms, `--nm-source`, and per-model provider pins: MiMo is pinned to Cohere fp8 because DeepInfra's MiMo endpoint was down, with the same privacy pins (data_collection deny, zdr, no fallbacks).
- The checker fix: run with `--nm-source 2_Project_Files/local-model/spark-ab/work/nm_src_1112`. Without it every task fails to build (zod 4 deps).
- Control reproduced 23/23 twice (results_control_recheck1112b.tsv, ...c.tsv).
- MiMo hosted: T01-T12 ALL PASS in results_mimohosted.tsv. T13-T23 are NOT run.
- Budget file `runs/fivemodel1112_budget.json`, cap $10. Spent at T12: $0.0551.
- The Spark: DeepSeek V4 Flash restored and healthy at 08:45:55. **The T01 PASS proof is NOT run.**
- On the Spark, left in `/home/datasec-rd/five-model-ab-1112/`: Nemotron, Kolibri and LFM2.5 weights, all verified. A V4.1 UD-IQ1_S download (233 GB, unsloth) and a llama.cpp image re-pull were still running at 08:55. LFM2.5 failed on the NVIDIA vLLM 0.29 image (no sm_121 FlashAttention-2 kernel).

## THIS commission, in order
1. **T01 proof on the Spark first:** `ab.py --model deepseek --only T01 --label restore1112 --nm-source …/work/nm_src_1112`. It must PASS. If it does not, STOP and report.
2. **MiMo hosted T13-T23** (resume, same pins, same budget file).
3. **V4.1 hosted, full 23** (the second run Kam asked for, to measure the noise of the 10-27 single run).
4. Write report.md in this folder:
   - hosted totals out of 23 (MiMo: T01-T12 from the existing tsv plus your T13-T23);
   - the V4.1 run-to-run comparison against 10-27, task by task;
   - cost;
   - the same "what it does NOT measure" section as before.
5. **Do NOT start any local Spark model swap** (Nemotron, Kolibri, LFM2.5, V4.1-local) in this session. The DevMASTER drive has dropped three times today: an hour-long swap mid-drop is what cost the last run. Local arms are a later commission.
6. The two Spark background jobs (the V4.1 download, the llama.cpp re-pull): report their state (running, done or failed) by a read-only ps/ls. Leave them alone.

Drive drops: if `/Volumes/DevMASTER` vanishes, stop, wait for it, re-read everything you wrote in the last minutes, then resume. Hosted calls are idempotent per task with the budget file reserving before each call: re-read the budget after any drop before calling again.

Constraints: exactly `commission.md`'s (no cd, no rm, no push, no mail, no board, $10 cap, privacy pins, never print a key).
