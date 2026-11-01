# B1063 ADDENDUM-1, from Tuesday: the answer to your Node question. Your commission otherwise stands unchanged.

Your question: run the web CI line locally on the machine's Node v26.8.1 with the difference stated, or wait for a Node 24?

**Answer: run it on v26.8.1. Do not wait.** This corrects the kit: its sentence "if `node` is not on PATH or is not Node 24, say so and STOP" was written without measuring the machine. Your STOP was right; the kit was wrong.

- `node --version` printing a version, and `npm ci` being able to run, remain the only REFUSE conditions on Node.
- State in STATUS, under MEASURED and NOT TESTED: local Node v26.8.1 and npm as read, CI pins Node 24, `engines` as read, and that the local run is therefore not the same runtime as the hosted web job.
- The hosted `web (npm ci, lint, test, production build)` job on the pull request is the judge on Node 24. Your READY line does not claim it.
- A red that appears locally and might come from the Node difference is still a STOP with the measurement, not a skip.

Your target READY and HARD STOP clocks run from your own Step-0 date as written; they do not move. Re-write your last line to `WORKING:` and carry on.
