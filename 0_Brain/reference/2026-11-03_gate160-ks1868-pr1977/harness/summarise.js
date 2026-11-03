// G160: compare every cell's end state with base+ordinaryError for the same env/path/mode.
const fs=require('fs'),path=require('path');const W=path.resolve(__dirname,'..');
const rs=JSON.parse(fs.readFileSync(path.join(W,'logs','matrix_all.json')));
const S=['alive','initOutcome','emitReturned','flagAfter','initResult','ddlAttempts','getSession','createSession','passwordChange','passwordReset','denylistRevokedJ1','denylistFreshJ2','lockoutLockedVictim','health','wouldExit1'];
const sig=r=>{const x=r.result||{};return S.map(k=>k+'='+(r.result?x[k]:(k==='alive'?'DEAD':'-'))).join(' ');};
const ref={};for(const r of rs) if(r.version==='base'&&r.kind==='ordinaryError') ref[[r.env,r.path,r.mode]]=sig(r);
const out=[];const cnt={};
for(const r of rs){ if(r.path==='up')continue; const k=[r.env,r.path,r.mode].join('/')+'/'+r.version; cnt[k]=cnt[k]||{same:0,diff:[]};
 const s=sig(r); if(s===ref[[r.env,r.path,r.mode]]) cnt[k].same++; else cnt[k].diff.push(r.kind);}
for(const k of Object.keys(cnt).sort()) out.push(k+'\tsame='+cnt[k].same+'\tdiff='+cnt[k].diff.length+'\t'+cnt[k].diff.join(','));
out.push('','REFERENCE (base ordinaryError):');for(const k of Object.keys(ref).sort()) out.push(k+'\t'+ref[k]);
// any head cell more permissive than reference on security columns
const perm=[];for(const r of rs){if(r.version!=='head'||!r.result)continue;const x=r.result;
 if(x.getSession==='ACCEPTED'&&r.path!=='up')perm.push(r.env+'/'+r.path+'/'+r.kind+' session accepted');
 if(x.denylistRevokedJ1===false&&r.path!=='up')perm.push(r.env+'/'+r.path+'/'+r.kind+' revoked jti honoured');
 if(x.passwordChange==='proceeds-to-write'&&r.path!=='up')perm.push(r.env+'/'+r.path+'/'+r.kind+' pw change proceeds');}
out.push('','HEAD more-permissive cells (session accepted / revoked jti honoured / pw proceeds): '+perm.length, ...perm);
fs.writeFileSync(path.join(W,'logs','summary.txt'),out.join('\n')+'\n');console.log(out.join('\n'));
