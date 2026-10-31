#!/usr/bin/env python3
"""Gate 62 own mutants: one unique-anchor replacement each, run the PR's two ks1888 files + gate 62's probe, restore, verify sha256."""
import subprocess, os, json, shutil, hashlib
G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate62-ks1888-1871"
B = f"{G}/repo/Blockchain/Dev/services/billing"
ROUTE = f"{B}/src/routes/billing.ts"; SVC = f"{B}/src/services/stripeService.ts"
VITEST = f"{G}/repo/Blockchain/Dev/node_modules/.bin/vitest"
TESTS = ["src/__tests__/ks1888-billing-routes-bound-to-the-customer-owner.test.ts",
         "src/__tests__/ks1888-stripe-service-lookups.test.ts",
         "src/__tests__/gate62-probe.test.ts"]
if os.environ.get("PR_ONLY") == "1": TESTS = TESTS[:2]
OUTJ = "own_mutants_pr_tests_only.json" if os.environ.get("PR_ONLY") == "1" else "own_mutants.json"
CUS_CHECK = "    // KS-1888: a customer the caller may not act on reads exactly like an unknown one.\n    if (!mayActOnCustomer((req as any).user, customer)) {"
SETUP = """    if (!mayActOnCustomer((req as any).user, await stripeService.findCustomer(req.params.customerId))) {
      sendNotFound(res, 'Customer not found');
      return;
    }
    const setupIntent = await stripeService.createSetupIntent(req.params.customerId);
"""
M = [
 ("G62-M1 check dropped on GET /customers/:id (existence only)", ROUTE, CUS_CHECK,
  "    // KS-1888: a customer the caller may not act on reads exactly like an unknown one.\n    if (!customer) {"),
 ("G62-M2 check dropped on POST /credits/use", ROUTE,
  "    if (!mayActOnCustomer((req as any).user, await stripeService.findCustomer(data.customerId))) {",
  "    if (!(await stripeService.findCustomer(data.customerId))) {"),
 ("G62-M3 check dropped on DELETE /payment-methods/:id (existence only)", ROUTE,
  "if (!paymentMethod || !(await mayActOnAttachedTo((req as any).user, paymentMethod.customer, (id) => stripeService.findCustomer(id)))) {",
  "if (!paymentMethod) {"),
 ("G62-M4 POST /customers trusts the body userId (owner from request input)", ROUTE,
  "const ownCustomer = callerId !== undefined && data.userId === callerId;",
  "const ownCustomer = data.userId !== '';"),
 ("G62-M5 platform-admin check inverted in mayActOnCustomer", ROUTE,
  "  if (isPlatformRole(caller.role as string | undefined)) return true;\n  const owner",
  "  if (!isPlatformRole(caller.role as string | undefined)) return true;\n  const owner"),
 ("G62-M6 setup-intent: Stripe write BEFORE the check", ROUTE, SETUP,
  """    const setupIntent = await stripeService.createSetupIntent(req.params.customerId);
    if (!mayActOnCustomer((req as any).user, await stripeService.findCustomer(req.params.customerId))) {
      sendNotFound(res, 'Customer not found');
      return;
    }
"""),
 ("G62-M7 tenant conjunct dropped (owner userId alone admits)", ROUTE,
  "  return typeof recordedTenant !== 'string' || recordedTenant === '' || recordedTenant === caller.tenantId;",
  "  return true;"),
 ("G62-M8 GET /invoices/:id refused gets a different 404 message", ROUTE,
  "if (!invoice || !(await mayActOnAttachedTo((req as any).user, invoice.customer, (id) => stripeService.getCustomer(id)))) {\n      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Invoice not found' } });",
  "if (!invoice) { res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Invoice not found' } }); return; }\n    if (!(await mayActOnAttachedTo((req as any).user, invoice.customer, (id) => stripeService.getCustomer(id)))) {\n      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Invoice not accessible' } });"),
 ("G62-M9 ORG_ADMIN same-tenant bypass in mayActOnCustomer", ROUTE,
  "  if (isPlatformRole(caller.role as string | undefined)) return true;\n  const owner",
  "  if (isPlatformRole(caller.role as string | undefined)) return true;\n  if (caller.role === 'ORG_ADMIN' && customer.metadata?.tenantId === caller.tenantId) return true;\n  const owner"),
 ("G62-M10 POST /customers existing-by-email returns first match unfiltered", ROUTE,
  "(await stripeService.listCustomersByEmail(data.email)).find((c) => mayActOnCustomer(user, c));",
  "(await stripeService.listCustomersByEmail(data.email)).find(() => true);"),
 ("G62-M11 PUT reserved-metadata refine removed", ROUTE,
  ".refine((m) => !RESERVED_CUSTOMER_METADATA.some((key) => Object.prototype.hasOwnProperty.call(m, key)), {",
  ".refine(() => true, {"),
 ("G62-M12 GET /customers/:id logs caller+id before the check", ROUTE, CUS_CHECK,
  "    logger.info('[Billing] customer lookup', { id: req.params.id, user: (req as any).user?.userId });\n" + CUS_CHECK),
 ("G62-M13 invoice/pm with no customer admitted for anyone", ROUTE,
  "  if (!customerId) return false;\n  return mayActOnCustomer(user, await lookup(customerId));",
  "  if (!customerId) return true;\n  return mayActOnCustomer(user, await lookup(customerId));"),
 ("G62-M14 DELETE pm owner taken from request query, not the stored pm", ROUTE,
  "mayActOnAttachedTo((req as any).user, paymentMethod.customer, (id) => stripeService.findCustomer(id))",
  "mayActOnAttachedTo((req as any).user, (req.query.customer as string) ?? null, (id) => stripeService.findCustomer(id))"),
 ("G62-M15 credits/use lookup swallows outage (getCustomer): outage -> 404", ROUTE,
  "    if (!mayActOnCustomer((req as any).user, await stripeService.findCustomer(data.customerId))) {",
  "    if (!mayActOnCustomer((req as any).user, await stripeService.getCustomer(data.customerId))) {"),
 ("G62-M16 isMissingResource always true (provider failure reads as missing)", SVC,
  "  return e.code === 'resource_missing' || e.statusCode === 404 || /No such/i.test(String(e.message ?? ''));",
  "  return true;"),
 ("G62-M17 empty-userId guard removed (no userId == no owner admits)", ROUTE,
  "  if (typeof caller.userId !== 'string' || caller.userId === '' || typeof owner !== 'string' || owner === '') return false;\n  if (owner !== caller.userId) return false;",
  "  if (String(owner) !== String(caller.userId)) return false;"),
 ("G62-M18 by-email uses Stripe's first match then checks it (old findCustomerByEmail)", ROUTE,
  "const customer = (await stripeService.listCustomersByEmail(email)).find((c) => mayActOnCustomer((req as any).user, c));",
  "const first = await stripeService.findCustomerByEmail(email); const customer = first && mayActOnCustomer((req as any).user, first) ? first : undefined;"),
]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
orig = {p: sha(p) for p in (ROUTE, SVC)}
env = dict(os.environ, TMPDIR=f"{G}/tmp")
results = []
for name, path, old, new in M:
    src = open(path).read()
    n = src.count(old)
    if n != 1:
        results.append({"mutant": name, "error": f"anchor count {n}"}); print(json.dumps(results[-1]), flush=True); continue
    bak = f"{G}/tmp/mut.bak"; shutil.copy(path, bak)
    try:
        open(path, "w").write(src.replace(old, new))
        p = subprocess.run(["nice", "-n", "10", VITEST, "run", "--root", B, "--maxWorkers=2", *TESTS], capture_output=True, text=True, env=env)
        out = p.stdout + p.stderr
        line = [l for l in out.splitlines() if "Tests " in l]
        fails = sorted({l.strip()[:160] for l in out.splitlines() if l.strip().startswith(("×", "FAIL"))})[:6]
        results.append({"mutant": name, "rc": p.returncode, "killed": p.returncode != 0, "tests": line[-1].strip() if line else out[-400:], "sample_failures": fails})
    finally:
        shutil.copy(bak, path)
    assert sha(path) == orig[path], f"RESTORE FAILED for {path}"
    results[-1]["restored_sha256_ok"] = True
    print(json.dumps(results[-1]), flush=True)
final = {p: sha(p) for p in (ROUTE, SVC)}
json.dump({"results": results, "sha256_before": orig, "sha256_after": final, "restored": final == orig}, open(f"{G}/evidence/{OUTJ}", "w"), indent=1)
print("RESTORED", final == orig)
