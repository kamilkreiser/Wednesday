# No-golden test + two-machine model check — report (2026-11-11 ~22:0x AEDT)
Written by Wednesday from the test agent's returned text (the harness refused the sub-agent's own write). Commission: commission.md in this folder.

## BLUF
1. **The test did NOT run: no OpenRouter key on this machine.** `4_Credentials/.env` holds only a comment: the key was "removed 2026-10-27 after the V4.1 hosted trial … Kam told to revoke it". No key in the Secuura .env or the vault either. Spend US$0.00; nothing was sent anywhere.
2. **Everything up to the send is built and tested:** 20 tickets screened (15 at rungs 4-6, 5 Opus-tier per Kam 21:38:45), inputs built with NO golden (a `no_golden_proof()` guard refuses golden-shaped input), `hosted/noground.py` (new; replay.py and check.sh unchanged), `tests/test_noground.py` 14/14 OK including three real checker controls (positive PASS 7/7; product hunk removed -> FAIL A3; red marker removed -> FAIL A4). Dry run of all 20 x 3 models: zero network calls. **Projected cost: about US$0.26 typical, US$0.74 worst for round 1 across three models; at most ~US$1.5 with round 2.**
3. **Models (all on OpenRouter's zero-retention list, read 21:42):** DeepSeek V4.1-Flash-1017 (DeepInfra fp8, $0.098/$0.294 per M), GLM-5.3-Flash (Z.ai fp8), MiMo-V2.6-Flash (DeepInfra fp8; endpoint status -2 degraded at read).
4. **Part A — 384 GB pooled does NOT open a clearly better model than 256 GB alone.** The strongest open coding model that runs locally is **DeepSeek V4.1-Flash-1017 (552B/16B active): it fits a 256 alone as a 3.0 bpw MLX pack (~209 GB, KLD 0.096); one M5 Ultra measured 103 tok/s @33K, 84 @131K; DeepSWE 74.2/77.0 vendor-reported (not independent).** Pooling buys only a higher-precision pack of it (288 GB) plus weaker models (Nemotron 3 Ultra, MiniMax M3.1 Flash, Beam; Inkling 2 Small weights unreleased). GLM-5.3 (69±3 independent), Kimi K3/K3.1, V4 Pro, MiMo-Pro do not fit 384 GB usably. **CORRECTION to research.md:** its table said V4.1-Flash needs 512 GB at Q4 and runs 14-29 tok/s; the 3.0 bpw pack fits 256 GB. V4.1-Flash, not MiMo or GLM-Flash, is what a 256 would run.
5. **Claude-minutes bar:** a Sonnet raise seat spends ~34.8 min per raised PR (scoreboard rows R 92nd, T 21st, T 16th, T 15th, U 21st: 871 min / 25 PRs); one third = **11.6 min per accepted local item**. Measured selection + prompting tonight ~0.45 min/ticket (+15 min one-off tooling); judging unmeasured.

## To run (once OPENROUTER_API_KEY is in 4_Credentials/.env; one model at a time; ~3-6 min per check, 3-6 h for all 60; load1 < 8)
    python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/noground.py run --model v41
    python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/noground.py run --model mimo
    python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/noground.py run --model glm
    python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/noground.py run --model <m> --round2
Then a Claude reads each PASS against the ticket: ACCEPT / WRONG-FIX / PARTIAL, timing the read (that is the Claude-minutes measurement).

## The 20 tickets (noground_tasks.json)
Rungs 4-6: KS-2163, 2046, 1982, 1908, 1896, 1880, 1826, 1806, 1743, 1222, 1112, 954, 1191, 1934, 683. **Opus tier:** KS-1946 (transaction design), KS-1921 (audit write inside the status change), KS-1870 (reconciler rule R7), KS-1935 (billing compare-and-set: money code, local test only), KS-1945 (three originate files). Weak picks flagged: KS-1743 (cause unverified), KS-1982 (fix may be in the Dockerfile), KS-1806 and KS-683 (bundled). B2 (agentic Sonnet-seat tasks) SKIPPED: needs the key and a provably git-free tool loop.

## Unmeasured
Every Part B verdict, ACCEPT rate, cost and judging minute; MiMo endpoint availability at run time; any two-Mac run of V4.1-Flash; independent DeepSWE for V4.1-Flash, MiniMax M3.1, Nemotron 3 Ultra, Inkling 2; quality loss of the 3.0 bpw pack on agentic work; the 256's real wired limit.

## Side finding
`hosted/tests/test_replay.py` has a PRE-EXISTING error: DryRun hits a relative run dir in spark/done.md (`0_Brain/reference/2026-10-28_spark-op6/r1_ks1415/round.json`, not found), plus one untraced failure. replay.py itself unchanged.
