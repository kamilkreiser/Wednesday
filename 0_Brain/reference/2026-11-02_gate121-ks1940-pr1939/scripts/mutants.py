import subprocess,hashlib,json,os
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate121-ks1940-pr1939'
G=W+'/repo/Blockchain/Dev/services/governance'
SVC=G+'/src/services/governanceService.ts'; RT=G+'/src/routes/governance.ts'
NEW=G+'/src/__tests__/ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts'
orig={f:open(f).read() for f in (SVC,RT)}; sha={f:hashlib.sha256(orig[f].encode()).hexdigest() for f in orig}
TH="    throw new ServiceUnavailableError('Governance participant store');\n"
ID_LOG="    logger.error('DB get participant failed', { id, error: reason });\n"
AD_LOG="    logger.error('DB get participant by address failed', { walletAddress, error: reason });\n"
def once(s,a,b):
  assert s.count(a)==1,(a,s.count(a)); return s.replace(a,b)
def nth(s,a,b,n):  # replace n-th (0-based) occurrence
  i=-1
  for _ in range(n+1): i=s.index(a,i+1)
  return s[:i]+b+s[i+len(a):]
S=orig[SVC]; R=orig[RT]
assert S.count(TH)==2
M={
 'M1_swallow_restored_byId':        (SVC, once(S,ID_LOG+TH,ID_LOG)),
 'M2_swallow_restored_byAddress':   (SVC, once(S,AD_LOG+TH,AD_LOG)),
 'M3a_route_503_becomes_200':       (RT,  once(R,"  } catch (error) {\n    next(error);\n  }\n});","  } catch (error) {\n    void error; void next; res.status(200).json({ success: true, data: null });\n  }\n});")),
 'M3b_helpers_throw_409_not_503':   (SVC, S.replace(TH,"    throw new ConflictError('Governance participant store');\n")+"\nexport const g121KeepImport = ServiceUnavailableError;\n"),
 'M4a_route_guard_dropped':         (RT,  once(R,"  } catch (error) {\n    next(error);\n  }\n});","  } catch (error) {\n    void error; void next; return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Participant not found' } });\n  }\n});")),
 'M4b_createProposal_guard_dropped':(SVC, once(S,"let proposer = await dbGetParticipant(proposerId);","let proposer = await dbGetParticipant(proposerId).catch(() => undefined);")),
 'M4c_register_guard_dropped':      (SVC, once(S,"const existing = await dbGetParticipantByAddress(walletAddress);","const existing = await dbGetParticipantByAddress(walletAddress).catch(() => undefined);")),
 'M4d_getParticipant_T8_hides':     (SVC, once(S,"const byId = await dbGetParticipant(idOrAddress);","const byId = await dbGetParticipant(idOrAddress).catch(() => undefined);")),
 'M4e_castVote_guard_dropped':      (SVC, once(S,"const voter = await dbGetParticipant(voterId);","const voter = await dbGetParticipant(voterId).catch(() => undefined);")),
 'M4f_cancel_guard_dropped':        (SVC, once(S,"const canceller = await dbGetParticipant(cancellerId);","const canceller = await dbGetParticipant(cancellerId).catch(() => undefined);")),
 'M4g_delegate_second_dropped':     (SVC, once(S,"const delegate = await dbGetParticipant(delegateId);","const delegate = await dbGetParticipant(delegateId).catch(() => undefined);")),
 'M5_fallback_reads_value_byId':    (SVC, nth(S,"      reason = 'unreadable thrown value';\n","      reason = String(err);\n",[i for i in range(S.count("      reason = 'unreadable thrown value';\n")) if True][0]) if False else None),
 'M6_swallow_only_unreadable_byId': (SVC, once(S,ID_LOG+TH,"    if (reason === 'unreadable thrown value') return undefined;\n"+ID_LOG+TH)),
 'M7_log_dropped_byId':             (SVC, once(S,ID_LOG+TH,'    void reason;\n'+TH)),
 'M8_always_constant_byId':         (SVC, once(S,"    logger.error('DB get participant failed', { id, error: reason });","    logger.error('DB get participant failed', { id, error: 'unreadable thrown value' }); void reason;")),
 'M9_string_branch_x_byId':         None,
}
# M5 / M9: locate the guard block that precedes ID_LOG
blk_i=S.index(ID_LOG); g0=S.rindex("    let reason: string;\n",0,blk_i); blk=S[g0:blk_i]
M['M5_fallback_reads_value_byId']=(SVC, S[:g0]+blk.replace("reason = 'unreadable thrown value';","reason = String(err);")+S[blk_i:])
M['M9_string_branch_x_byId']=(SVC, S[:g0]+blk.replace(": String(err);",": 'x';")+S[blk_i:])
blk_a=S.index(AD_LOG); a0=S.rindex("    let reason: string;\n",0,blk_a); blka=S[a0:blk_a]
M['M5b_fallback_reads_value_byAddr']=(SVC, S[:a0]+blka.replace("reason = 'unreadable thrown value';","reason = String(err);")+S[blk_a:])
out=[]
for name,(f,new) in M.items():
  assert new!=orig[f], name
  open(f,'w').write(new)
  j=f'{W}/logs/mut_{name}.json'
  p=subprocess.run([G+'/node_modules/.bin/jest','--config',G+'/jest.config.js','--rootDir',G,'--runTestsByPath',NEW,'--json','--outputFile',j,'--forceExit'],capture_output=True,text=True,env={**os.environ,'TMPDIR':W+'/tmp'})
  open(f,'w').write(orig[f])
  assert hashlib.sha256(open(f).read().encode()).hexdigest()==sha[f]
  try:
    d=json.load(open(j)); res=d['testResults'][0]; a=res['assertionResults']
    red=[x['title'].split(' ')[2] for x in a if x['status']!='passed']
    if not a: red=['SUITE_FAILED:'+res['message'][:150].replace('\n',' ')]
  except Exception as e: red=['NOJSON '+str(e)]
  out.append(f"{name:34} rc {p.returncode} {'KILLED' if red else 'SURVIVED'} red={sorted(set(red))}")
  print(out[-1],flush=True)
print('RESTORE_OK',{os.path.basename(k):v[:12] for k,v in sha.items()})
