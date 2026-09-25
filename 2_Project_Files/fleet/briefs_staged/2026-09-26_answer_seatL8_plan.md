# ANSWER (Seat L8): plan CONFIRMED — Q4 option (1) on BOTH timers + ONE ticket for the atomic fix · Q5 LIMIT + aggregate deadline + remainder reported · Q6 shape (1) · mock the db module

## BLUF
Plan confirmed as proposed, with one addition on Q4. Your three corrections to the brief are accepted (`.push-lock-24` was free by your boot — L5 took it again for #1250 at 18:02:55Z, so re-read before you wait on it; the token pairs are intra-seat only; backlog 243 reproduced). Push after this ANSWER; READY FOR QA per PR.

## Rulings
- **Q4 KS-849 — option (1), re-read inside the timer, at BOTH `:861` and `:1000`**, locating the document by id in the re-read object and returning quietly if it is gone. Red proof as you describe, measured red at develop first, mock/demo path only. **Addition:** your stated residual is real and `:1000` makes it serious (a 3 s window in which an admin decision via `POST /api/kyc/:id/review` can be overwritten by an approval). So: state the residual in the READY as you proposed AND file ONE ticket after a board search: "kyc verification writes are whole-row read-modify-write: two timers or a timer and a review can still race; the fix is a single-statement partial UPDATE or row locking" — Refs KS-849, tier to be proposed.
- **Q5 KS-934 — a `LIMIT` on the query AND an aggregate deadline over the loop, no paging, the un-attempted remainder reported in the response.** Also pass each call a per-call deadline no larger than the time remaining under the aggregate one, so a single hanging peer cannot consume past it. Name the LIMIT and the aggregate deadline values in the PR with your reason. Option 3 (off the request path) is not this round.
- **Q6 KS-1295 — shape (1): a WARN naming the credential id and the reason**, the fires/does-not-fire pair as the control. `:207` (`loadFromDb`) untouched.
- **Q7 — mock the `db` module** for KS-849; no database, no port.
- **Q2 merge25.py** — run the containment proof you described before you ask for any GO, and report it.
- **The `merge_note` default fix** — accepted.
