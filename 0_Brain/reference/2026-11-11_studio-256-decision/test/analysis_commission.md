# Analysis commission: Kam's hosted no-golden test, by Wednesday, 2026-11-12 ~00:1x AEDT

## Why
Kam is deciding whether to buy a 256 GB Mac Studio for local models. His bar (live board 2026-11-11 21:22, verbatim): "the question is whether local LLMs are useful (and to what extent) in our workflow. more ram gives us mimo and others but that is only of value if it takes 30% or so off the plate from the cloud models". He asked for this test at 21:36 and said "lets wait for the test" at 21:47. Commission: `commission.md` in this folder; the test's design and Part A (what fits in 256 GB or 384 GB) are in `report.md` here.

## Wait first
The run is still going: a bash loop (pid 79866) runs `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/noground.py run --model <m>` for v41, then mimo, then glm. Log: `run_2026-11-11.log` in this folder (lines `NOGROUND <model> <ticket>_r1 [...]: PASS|FAIL — ...` and `== <model> start|rc=`). Wait until `ps -p 79866` reports it gone and the log has `== glm rc=`, polling every 2 minutes with a background loop that EXITS when done. Do not stop or touch the run. If it is still running after 2.5 hours, report what is there and say it was incomplete.

## Then, in order
1. **Read the harness before judging any FAIL.** `noground.py`, the checker it calls, and what the legs A1, A2a, A3, A4 test. Many rows read `checker=PASS (7/7)` but FAIL on `A2a rc=1`, and some stop at `A1 (sampler loop)`. For EACH of the 60 rows, classify the cause: MODEL (wrong or partial fix), HARNESS (a check that refused a correct fix, or a run that never reached the model's real answer), or INPUT (the ticket or its input was not answerable). Read the actual diff and the checker output for every A2a refusal, and say what A2a refused and whether that refusal is right. Every classification names the file and lines it rests on. **A2a is the crux:** if it is wrongly refusing correct fixes, the headline pass rate is understated, and the report must say by how much, with each case shown.
2. **Score each PASS against its ticket**, and every A2a-refused checker-pass too: ACCEPT (fixes what the ticket asks), WRONG-FIX, or PARTIAL. Time each read, because that time is the Claude-minutes measurement. The test's own bar is in report.md: about 11.6 Claude-minutes saved per accepted local item.
3. **Answer Kam's question with numbers.** Per model: rows, PASS, ACCEPT, the share of the 20 tickets (and of the 5 Opus-tier tickets separately) a local model would take off the cloud, the dollar cost spent, and the wall-clock. Then state plainly whether any model reaches his 30%, and how far the answer moves if the harness defects are fixed (show both numbers). Name what is UNMEASURED, for example the 3.0 bpw quality loss on a 256 GB Studio, or that this is hosted inference, not the local box.

## Output
Write `analysis.md` in this folder. Its first section is a BLUF of at most five lines that Wednesday can give to Kam directly, with no jargon (do not say A2a or rungs; say what they mean). Then a per-row table (ticket, model, verdict, cause, the evidence path), the per-model numbers, and the method with its controls. Return the BLUF and the per-model numbers in your final message.

## Constraints
Read-only on everything except `analysis.md` and a `scratch/` folder in this directory. No network calls to OpenRouter (the key is in `4_Credentials/.env` and you do not need it; never print it). No `cd`, no rm, absolute paths, quoted heredocs. Read-only git verbs only on any Secuura checkout.
