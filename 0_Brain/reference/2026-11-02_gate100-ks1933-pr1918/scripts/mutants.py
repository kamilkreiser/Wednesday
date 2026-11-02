# Gate 100 mutants: product files only, tests untouched, sha256 restored after every run.
import hashlib, json, subprocess, re, sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate100-ks1933-pr1918'
A=G+'/repo/Blockchain/Dev/services/billing/src/'
CG=A+'creditGrants.ts'; WH=A+'routes/webhooks.ts'
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
ORIG={p:(open(p).read(),sha(p)) for p in (CG,WH)}
M=[
 ('M1 lost claim ignored (always credit)', CG, "if ((claim.rowCount ?? claim.rows.length) === 0) {", "if (false) {"),
 ('M2 claim error swallowed as already-granted', CG, "  const claim = await query<{ payment_key: string }>(CLAIM_GRANT_SQL, [\n    req.paymentKey, req.customerId, req.credits, req.eventId, req.eventType,\n  ]);", "  let claim: any;\n  try { claim = await query<{ payment_key: string }>(CLAIM_GRANT_SQL, [\n    req.paymentKey, req.customerId, req.credits, req.eventId, req.eventType,\n  ]); } catch { return null; }"),
 ('M3 claim error swallowed as won', CG, "  const claim = await query<{ payment_key: string }>(CLAIM_GRANT_SQL, [\n    req.paymentKey, req.customerId, req.credits, req.eventId, req.eventType,\n  ]);", "  let claim: any;\n  try { claim = await query<{ payment_key: string }>(CLAIM_GRANT_SQL, [\n    req.paymentKey, req.customerId, req.credits, req.eventId, req.eventType,\n  ]); } catch { claim = { rowCount: 1, rows: [{}] }; }"),
 ('M4 impossible empty claim -> silent skip', CG, "      throw new Error('Credit grant claim returned no row and no existing row');", "      return null;"),
 ('M5 READ failure swallowed -> skip', CG, "    const prior = await query<{ status: string; age_seconds: number }>(READ_GRANT_SQL, [req.paymentKey]);", "    let prior: any; try { prior = await query<{ status: string; age_seconds: number }>(READ_GRANT_SQL, [req.paymentKey]); } catch { return null; }"),
 ('M6 mark-failed removed', CG, "      await query(MARK_FAILED_SQL, [req.paymentKey]);", "      void MARK_FAILED_SQL;"),
 ('M7 credit failure swallowed (no rethrow)', CG, "    throw error;\n  }\n\n  try {", "    return null;\n  }\n\n  try {"),
 ('M8 mark-granted removed', CG, "    await query(MARK_GRANTED_SQL, [req.paymentKey]);", "    void MARK_GRANTED_SQL;"),
 ('M9 mark-granted failure rethrown', CG, "      ...describeThrown(markErr),\n    });\n  }\n  return newBalance;", "      ...describeThrown(markErr),\n    });\n    throw markErr;\n  }\n  return newBalance;"),
 ('M10 checkout key always cs:', CG, "return piId ? `pi:${piId}` : `cs:${session.id}`;", "return `cs:${session.id}`;"),
 ('M11 checkout key ignores expanded object', CG, "const piId = typeof pi === 'string' ? pi : (pi && typeof pi === 'object' && typeof (pi as { id?: unknown }).id === 'string' ? (pi as { id: string }).id : null);", "const piId = typeof pi === 'string' ? pi : null;"),
 ('M12 describeThrown adds message value', CG, "return { errorType: name, errorFields: fields };", "return { errorType: name, errorFields: fields, message: (value as any).message } as any;"),
 ('M13 describeThrown rethrows when unreadable', CG, "    return { errorType: 'unreadable thrown value', errorFields: [] };", "    throw value;"),
 ('M14 PI handler bypasses the ledger', WH, "      const newBalance = await grantCreditsOnce(\n        { paymentKey: `pi:${paymentIntent.id}`, customerId, credits: certifications, eventId: event.id, eventType: event.type },\n        (c, n) => stripeService.addCertificationCredits(c, n),\n      );", "      const newBalance: number | null = await stripeService.addCertificationCredits(customerId, certifications);"),
 ('M15 PI handler keys on event id', WH, "paymentKey: `pi:${paymentIntent.id}`", "paymentKey: `pi:${event.id}`"),
 ('M16 checkout reports credits when skipped', WH, "    if (newBalance === null) {\n      return 0;\n    }\n    creditsAdded = certifications;\n\n    logger.info('Certification credits added'", "    creditsAdded = certifications;\n\n    logger.info('Certification credits added'"),
 ('M17 finalise catch rethrows', WH, "    logger.error('Failed to finalise webhook event', { eventId, ...describeThrown(err) });", "    logger.error('Failed to finalise webhook event', { eventId, ...describeThrown(err) });\n    throw err;"),
 ('M18 release catch reads message', WH, "      eventId,\n      ...describeThrown(err),\n    });", "      eventId,\n      error: (err as any)?.message,\n    });"),
]
out=open(G+'/logs/mutants_table.jsonl','w')
for name,path,old,new in M:
    src=ORIG[path][0]
    n=src.count(old)
    if n!=1: print(name,'ANCHOR COUNT',n); out.write(json.dumps({'mutant':name,'anchor':n})+'\n'); continue
    open(path,'w').write(src.replace(old,new))
    tag=re.sub(r'[^A-Za-z0-9]+','_',name.split(' ')[0])
    log=f'{G}/logs/mut_{tag}.log'
    rc=subprocess.run(['bash',G+'/scripts/vt.sh',log,'ks1933-billing-one-purchase','ks1868-billing-webhook-stripe','ks488-c4']).returncode
    open(path,'w').write(ORIG[path][0]); ok=sha(path)==ORIG[path][1]
    txt=open(log).read()
    failed=sorted(set(re.findall(r'^\s+× (\S+)',txt,re.M)))
    m=re.search(r'Tests\s+(.*)',txt)
    nonassert=len(re.findall(r'(SyntaxError|TransformError|ReferenceError|Transform failed)',txt))
    row={'mutant':name,'rc':rc,'tests':m.group(1) if m else None,'killed_by':failed,'assertionErrors':txt.count('AssertionError'),'nonAssertionSignals':nonassert,'restore':ok}
    print(json.dumps(row)); out.write(json.dumps(row)+'\n'); out.flush()
print('final', {p.split('/')[-1]:sha(p)==ORIG[p][1] for p in ORIG})
