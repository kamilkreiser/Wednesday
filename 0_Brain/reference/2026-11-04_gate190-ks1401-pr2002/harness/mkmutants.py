#!/usr/bin/env python3
"""Gate 190: write mutant copies of the committed 058 into mut/<ID>/058_ks1401_tenant_isolation_after_039.sql.
Each mutant must change the file (asserted) and is applied by the same harness as the real file."""
import os, sys, re
WD = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002'
NAME = '058_ks1401_tenant_isolation_after_039.sql'
src = open(f'{WD}/scratch/real/{NAME}').read()

def sub(s, old, new, count=1):
    n = s.count(old)
    assert n > 0 and (count == 'all' or n >= count), (old, n)
    return s.replace(old, new) if count == 'all' else s.replace(old, new, count)

M = {}
M['M1'] = sub(src, "SET tenant_id = $1 WHERE tenant_id IS NULL'", "SET tenant_id = $1'")
M['M2'] = sub(src, "    EXECUTE format('ALTER TABLE public.%I FORCE ROW LEVEL SECURITY', t);\n", "")
M['M3'] = sub(src, "    EXECUTE format('DROP POLICY IF EXISTS tenant_isolation ON public.%I', t);\n", "")
M['M4'] = sub(src, "default_tid  CONSTANT UUID := 'a0000000-0000-4000-8000-000000000001'", "default_tid  CONSTANT UUID := 'a0000000-0000-4000-8000-000000000002'")
M['M5'] = sub(src, "  PERFORM set_config('app.tenant_scope_bypass', 'platform_admin', true);\n", "")
upd = "    EXECUTE format('UPDATE public.%I SET tenant_id = $1 WHERE tenant_id IS NULL', t)\n      USING default_tid;\n    GET DIAGNOSTICS filled = ROW_COUNT;\n"
m6 = sub(src, upd, "")
M['M6'] = sub(m6, "    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', t);\n", upd + "    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', t);\n")
M['M7'] = sub(src, "  PERFORM set_config('lock_timeout', '5s', true);\n", "")
M['M8'] = re.sub(r"      RAISE EXCEPTION\n        'KS-1401: table public\.% is absent;[^\n]*\n", "      CONTINUE;\n", src)
M['MC1'] = sub(src, "current_setting('app.current_tenant_id', true) IS NOT NULL\n            AND ", "", 'all')
M['MC2'] = sub(src, "            AND current_setting('app.current_tenant_id', true) <> ''\n", "", 'all')
M['MC3'] = sub(src, "            AND tenant_id::text = current_setting('app.current_tenant_id', true)\n", "", 'all')
M['MC4'] = sub(src, "          OR current_setting('app.tenant_scope_bypass', true) = 'platform_admin'\n", "", 'all')
# gate-own mutants (not in the seat's series)
M['G1_noAddColumn'] = re.sub(r"      EXECUTE format\('ALTER TABLE public\.%I ADD COLUMN tenant_id UUID', t\);\n", "", src)
M['G2_noWithCheck'] = re.sub(r"\n        WITH CHECK \(\n.*?\n        \)\n    \$p\$", "\n    $p$", src, flags=re.S)
M['G3_tableListDropsCert'] = sub(src, "'charge_events', 'certifications', 'oauth_apps', 'svc_webhooks'", "'charge_events', 'oauth_apps', 'svc_webhooks'")
M['G4_restrictive'] = sub(src, "CREATE POLICY tenant_isolation ON %I\n", "CREATE POLICY tenant_isolation ON %I AS RESTRICTIVE\n")
for k, v in M.items():
    assert v != src, k
    d = f'{WD}/mut/{k}'; os.makedirs(d, exist_ok=True)
    open(f'{d}/{NAME}', 'w').write(v)
print(' '.join(M.keys()))
