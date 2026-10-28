# op6 task 1 (KS-1415 item 2): count cells beside each grep -m1 status-URI pin in prometheus_targets.test.sh. Tier test_only via gen/mk_testonly.py.
PROD='observability/.env.example'
TEST='Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh'
A1='    "$(grep -m1 \'SECUURA_NGINX_STATUS_URI=\' "$DEV_ROOT/../../observability/config/alerting.env.example")"\n'
N1=A1+'''
# KS-1415: the cell above reads only the FIRST status-URI line, so a later ACTIVE :6882 line could hide below it. A count is blind to position.
# Comments are stripped first, as prom_live is above: the example's own prose may name 6882.
expect "observability/config/alerting.env.example carries no active nginx-gateway:6882 line" "0" \\
    "$(sed 's/#.*//' "$DEV_ROOT/../../observability/config/alerting.env.example" | grep -c 'nginx-gateway:6882')"
'''
A2='    "$(grep -m1 \'SECUURA_NGINX_STATUS_URI=\' "$DEV_ROOT/../../observability/.env.example")"\n'
N2=A2+'''
# KS-1415: same blind spot as the alerting.env.example cell: a count of active :6882 lines, whatever their position.
expect "observability/.env.example carries no active nginx-gateway:6882 line" "0" \\
    "$(sed 's/#.*//' "$DEV_ROOT/../../observability/.env.example" | grep -c 'nginx-gateway:6882')"
'''
T=dict(dir='ks_1415_p2_count',ticket='KS-1415',
 title='prometheus_targets.test.sh: the status-URI cells pin only the FIRST line of each env example; add a count cell for each that no ACTIVE nginx-gateway:6882 line exists (RUNG 3, TEST-ONLY bash: two in-place hunks, planted tamper in one example file)',
 intro="DRAFT by a Spark operator (op6) for Wednesday, 2026-10-28 AEDT (never-keep-the-Spark-idle). Secuura only. A local PASS is a candidate, never a merge. Test-only bash change. Item 1 of KS-1415 (the two HTML documents) is NOT this brief.",
 product=PROD, test=TEST, ref='Blockchain/Dev/scripts/__tests__/smoke_test_counters_survive_errexit.test.sh',
 tamper_line=49, tamper_from="# SECUURA_KAFKA_BROKER=secuura-kafka:9092", tamper_to="SECUURA_NGINX_STATUS_URI=http://secuura-nginx-gateway:6882/stub_status",
 statement_ok="line 49 is the last line of the file, one complete commented example; the tamper replaces it with an ACTIVE (uncommented) second status-URI line naming :6882, AFTER the first occurrence, so the existing first-line pin (grep -m1) still reads the correct line and stays green",
 edit=[(A1,N1),(A2,N2)],
 nh_txt='2 hunks, one count cell added after each existing grep -m1 pin', nh_word='TWO hunks', nh_head='TWO EDITS in the TEST file (two hunks)',
 red=['observability/.env.example carries no active nginx-gateway:6882 line'],
 runner='bash` (`bash Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh` from the repo root',
 rung='3 (test-only mode: a planted tamper must be reddened by the cell; both hunks byte-exact)',
 what_wrong="`prometheus_targets.test.sh` pins the gateway status URI in `observability/config/alerting.env.example` and `observability/.env.example` with `grep -m1 'SECUURA_NGINX_STATUS_URI='`, which reads only the FIRST such line. A file whose first line is right but which carries a LATER ACTIVE (uncommented) `nginx-gateway:6882` line passes. 6882 is the gateway's published host port, unreachable from the exporter's network. Add, directly after each pin, a count cell: the number of ACTIVE (comment-stripped) lines naming `nginx-gateway:6882` in that file must be 0. Keep the existing pins.",
 where="- `Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh:90` - (correct, STAYS) the `grep -m1` pin of `alerting.env.example`; the first hunk adds its count cell right after it.\n- `...prometheus_targets.test.sh:121` - (correct, STAYS) the `grep -m1` pin of `observability/.env.example`; the second hunk adds its count cell right after it.\n- `observability/.env.example:49` - the product-side line the checker tampers; not modified by you.",
 cells="- RED under the tamper: the `.env.example` count cell prints FAIL (count 1, wanted 0); the tamper adds an active `:6882` line AFTER the first status-URI line, so the existing pin stays green.\n- GREEN at the untouched tip: both count cells read 0 (the files carry `6882` only inside comments, and none names `nginx-gateway:6882`).\n- The `alerting.env.example` cell is the twin; it is not tampered by the checker.",
 unmeasured="- Nothing was run by the drafter beyond reading both files and running the suite green at the tip (6 passed).\n- The label says `active` and the count strips comments (`sed 's/#.*//'`), the same idiom the file already uses for `prom_live`; the ticket's literal `grep -c` without the strip gives the same 0 at the tip.\n- Whether this tier's checker can run a bash suite at all is not known to the drafter.",
 scope="**KS-1415 item 2 only.** Refs KS-1415, never a close-word.",
)
