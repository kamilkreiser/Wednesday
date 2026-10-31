#!/usr/bin/env python3
import subprocess, os, json, shutil, hashlib, re, sys
D = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate69-ks1911-1883"
B = os.environ.get("BILLING", f"{D}/repo/Blockchain/Dev/services/billing")
ROUTE = f"{B}/src/routes/billing.ts"
VITEST = f"{B}/../../node_modules/.bin/vitest"
T = "src/__tests__/ks1888-billing-routes-bound-to-the-customer-owner.test.ts"
G62 = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate62-ks1888-1871/scripts/mutants.py"
lines = open(G62).read().split("\n")
blk = "\n".join(lines[73:76])  # file lines 74-76
import ast
tup = ast.literal_eval(blk.strip().rstrip(",").replace(", ROUTE,", ", \"ROUTE\","))
assert tup[0].startswith("G62-M18"), tup[0]
_, _, old18, new18 = tup
CK = "(await stripeService.listCustomersByEmail(email)).find((c) => mayActOnCustomer((req as any).user, c))"
M = [
 ("G62-M18 byte for byte from mutants.py:74-76", old18, new18),
 ("O1 by-email: owner check dropped, first match returned", "const customer = " + CK + ";", "const customer = (await stripeService.listCustomersByEmail(email))[0];"),
 ("O2 by-email: owner check inverted", CK, "(await stripeService.listCustomersByEmail(email)).find((c) => !mayActOnCustomer((req as any).user, c))"),
 ("O3 by-email: check applied to first match only, others admitted (leak)", CK, "(await stripeService.listCustomersByEmail(email)).find((c, i) => i === 0 ? mayActOnCustomer((req as any).user, c) : true)"),
 ("O4 by-email: owner check admits last match unchecked (leak)", CK, "(await stripeService.listCustomersByEmail(email)).find((c, i, a) => i === a.length - 1 || mayActOnCustomer((req as any).user, c))"),
]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
o = sha(ROUTE); res = []
for name, old, new in M:
    src = open(ROUTE).read(); n = src.count(old)
    if n != 1: res.append({"mutant": name, "error": f"anchor {n}"}); print(res[-1], flush=True); continue
    shutil.copy(ROUTE, f"{D}/evidence/route.bak")
    try:
        open(ROUTE, "w").write(src.replace(old, new))
        out = f"{D}/evidence/mut_{name.split()[0]}.json"
        p = subprocess.run(["nice","-n","10",VITEST,"run","--root",B,"--maxWorkers=3","--reporter=json",f"--outputFile={out}",T],capture_output=True,text=True)
    finally:
        shutil.copy(f"{D}/evidence/route.bak", ROUTE)
    assert sha(ROUTE) == o, "restore failed"
    d = json.load(open(out)); cells = [a for f in d['testResults'] for a in f['assertionResults']]
    red = [a['title'] for a in cells if a['status'] != 'passed']
    skipped = [a['title'] for a in cells if a['status'] in ('skipped','pending','todo')]
    r = {"mutant": name, "rc": p.returncode, "cells": len(cells), "red": len(red), "skipped": len(skipped), "red_titles": [t[:70] for t in red]}
    res.append(r); print(json.dumps(r), flush=True)
json.dump(res, open(f"{D}/evidence/mutants.json", "w"), indent=1)
print("route sha restored:", sha(ROUTE) == o)
