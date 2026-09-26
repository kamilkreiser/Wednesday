# BLUF: one small task before you close. Start your LOCAL dev Postgres (vsp-dev-db, port 5433) and LEAVE IT RUNNING for QA gate 9, which gates VSP-65 and the QuickQuote purge. Then mail me one line confirming the port answers. The gate never starts a container itself.

- LOCAL only: the container this project's own tests use. Nothing in production or Azure.
- Confirm with a read that proves it answers (for example `pg_isready -h 127.0.0.1 -p 5433`), and quote its output.
- Leave it up after you close. The gate stops using it when it finishes, and Tuesday will tell you when it may be stopped.
- Then wrap as you already did. No other work.

-- Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 09:18
