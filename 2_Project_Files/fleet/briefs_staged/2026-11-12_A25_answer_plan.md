Seat A 25th

ANSWER: plan confirmation (Seat A 25th)

CONFIRMED as written. KS-1466 under Kam's ruling a: the in-repo caller census and the SEED_DOCUMENT_TYPES read at develop first (local); then R1 and R2 on BOTH boxes; the build only if the measurement clears on both and you are under 55 when it starts; A2 carried (PR 2191 OPEN); fix rounds by ADDENDUM only. Your 10(a) precision is right (enforcement.ts:101 is the typeRefRaw line; the untyped return is 117 at develop): quote 117 in your BLUF and PR.

GRANTED, exactly as your item 6 describes, on kintsugi AND demo:
- R1 (catalogue): ssh as secuura with the project's own key files (3_Access_Keys/vm_secuura02_kintsugi, vm_secuura02_demo; names only, never a value), `docker compose ps` in the stack directory (kintsugi's directory UNMEASURED: if not found, STOP and say so), then redis-cli inside the compose redis container with commands on STDIN only. ALLOW-LIST, nothing else: AUTH (password read by the remote shell from the box's own Dev/.env, never in argv, never printed), KEYS secuura:gateway:doctype:* (the gateway's own read), GET of each returned key. No SET, DEL, EXPIRE, CONFIG, FLUSH, SAVE, or any other command; your recorder enforces the allow-list in code and its evidence lists every command it sent.
- R2 (callers): `docker compose logs --since 168h api-gateway` read and counted on the box (report the window the log actually covers); Postgres SELECT only inside BEGIN TRANSACTION READ ONLY ... ROLLBACK via `docker compose exec -T postgres psql` on stdin, table/column names read from the migrations first; if psql asks for a password, stop (none is passed).
- NOT granted: any other docker compose verb (up, restart, pull, exec of anything but redis-cli and psql as above), any HTTP call to either box, GET /api/admin/document-types (forbidden as stamped), the public GET /api/document-types (your own reasoning for not proposing it is accepted), any file write on a box, any az command (these are ssh-only reads; confirm each host is the Secuura VM named in the project CLAUDE.md / runbook before the first command: hard rule 4).
- Demo stays FROZEN for writes; these reads are inside that freeze. If R1 or R2 is refused on either box, or a box is down: STOP and QUESTION (topic KS-1466 measurement), as stamped; demo UNMEASURED is never a default.

Board: the KS-1466 BLUF comment carrying Kam's ruling is released now, through lin.py, once; your daily-note Priorities block too. Your item 12 fault (a subshell cd and a find) is accepted as declared; the replacement is right.

STOP RULE reminder (Kam's): if enforcing would refuse ANY current caller on either box, change nothing and QUESTION with the numbers per box (stored entry's fields, empty/missing state, each refused caller and its volume). Rows are an upper bound, as you say: say which numbers are logs and which are rows.

FLOOR at this answer (tmux list-panes, 11:3x AEDT): you %36 (build), Seat R 105th %27 (raise; KS-2169 push running), Seat B 148th %30 (merge; PR 2199), Seat S 66th %33 (board), Seat T 24th %39 (build; KS-1398 step one lane L1: the fifth session on the project your item 1 saw). None is yours. Your rung-6 launch proof is this plan mail.

Wednesday
