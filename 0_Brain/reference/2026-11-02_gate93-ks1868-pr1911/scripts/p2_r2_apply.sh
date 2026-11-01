#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911; S=$W/c1scratch; F=Blockchain/Dev/services/auth/src/routes/auth.ts
RU=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_
cp $W/logs/base_auth.ts $S/$F
git -C $S apply -p1 ${RU}p3_auth_reset_password_revoke_unreadable_throw/out.md.checker/section_1.diff; echo "p3 rc=$?"
git -C $S apply -C1 -p1 ${RU}p1_auth_register_publish_event_unreadable_throw/out.md.checker/section_1.diff; echo "p1 rc=$?"
git -C $S apply --check -p1 ${RU}p2_auth_login_publish_event_unreadable_throw-r2/out.md.checker/section_1.diff; echo "p2-r2 plain check rc=$?"
git -C $S apply -C1 -p1 ${RU}p2_auth_login_publish_event_unreadable_throw-r2/out.md.checker/section_1.diff; echo "p2-r2 -C1 rc=$?"
cmp $S/$F $W/logs/head_auth.ts && echo "applied(P3,P1,P2-r2) == HEAD auth.ts: IDENTICAL"
