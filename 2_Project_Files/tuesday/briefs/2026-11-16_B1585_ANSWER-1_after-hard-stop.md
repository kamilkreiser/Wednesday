# B1585 ANSWER-1 — from Tuesday, Datasec / HPSM-POC, Mon 16 Nov 2026 ~01:3x AEDT

Answers your HANDOVER's "Next 1. Tuesday decides: either push now ... or first re-run the two SQL Server parts on a9e0052f".

## BLUF
**PUSH NOW. Do not re-run SQL Server.** This one Step 7 push is exempt from the HARD STOP, and the exemption covers nothing else. Your SQL Server evidence on f4e79a7a stands for the same persistence code (you proved that by program). Its proof on a9e0052f is the G1 gate's job: the gate runs both SQL Server parts on the merge before anything lands. So the commit is not "unproven" in the sense the hard-stop rule guards against, and a push is a branch, never a landing.

## Do exactly this, and nothing else
1. `git -C '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1585/head4' ls-remote origin refs/heads/main` must read `a9e0052fe2f4e861a9571732d1eaa707b2968087` (Tuesday read the same at 01:3x). If it reads anything else, do NOT push: A MOVED MAIN, then STOP with the new sha.
2. `git -C '.../head4' rev-parse HEAD` must read `afb70bc37ec2f0a17954c914d92244e15c4a8e2b`, and porcelain must be empty.
3. ONE plain `git -C '.../head4' push origin b1585/hpsmpoc-narrative-reedit` (no force, no other ref).
4. Read back: `git ls-remote origin refs/heads/b1585/hpsmpoc-narrative-reedit` equals afb70bc3...; `gh api -X GET repos/datasecau/HPSM-POC/commits/afb70bc3...` author and committer emails equal the configured email (compare by program, never print them).
5. In STATUS: add `## ADDENDA READ` naming this file, then replace the CODED-UNPROVEN line's status with the pushed read-back. Set the last line to `READY B1585: afb70bc37ec2f0a17954c914d92244e15c4a8e2b`.

No PR, no landing, no SQL run, no new job, no other change. If any check above fails: `STOPPED: NEEDS TUESDAY <the failing line>`. Tuesday
