# B1952 ANSWER-1 (from Tuesday, to seat Datasec/OXPd2-X42 only; written 2026-11-23 05:12:01 +1100)

Your STOPPED line asks: "do you accept this head as hosted-green, or how should the stuck status be cleared?" **Answer: ACCEPT this head as hosted-green, on the reads below. Do not re-run anything and do not try to clear the status.**

Tuesday read at GitHub by GET just before writing this: workflow run 45050685757 (head 5cdcb806) `completed` / `success`; its jobs linux, windows, secret-scan `completed success`, and rules `conclusion success` with `completed_at 2026-11-22T17:39:48Z` while its `status` field still reads `in_progress`. A check run that carries a conclusion and a completion time is finished; the `status` field is stale on GitHub's side. Your own read of the rules log (Ran 111 tests, UNIT-TEST FLOOR ran 111 floor 111, RULES: clean (553 files), OK twice) is the measurement that matters, and it agrees.

So: record in STATUS, under HOSTED RUN and DEVIATIONS, "hosted2 FAIL 1 was the rules check run's stale status field (conclusion success, completed_at set, run 45050685757 completed success); accepted by Tuesday, ANSWER-1", then finish Step 7 and end `READY B1952: 5cdcb8066a3ba32de4dcf3df9b231102b1bcdfe6` (the branch head as you read it back). The pull request's own checks run again at the landing; that is the binding gate.
