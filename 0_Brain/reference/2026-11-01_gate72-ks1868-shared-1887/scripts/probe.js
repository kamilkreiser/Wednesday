const {createUnhandledRejectionHandler:c}=require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate72-ks1868-shared-1887/repo/Blockchain/Dev/packages/shared/dist/utils/gracefulShutdown.js');
const mk=(mode,r)=>{const o={logs:[],sd:[],threw:false};const h=c({serviceName:'s',mode,logger:m=>o.logs.push(m),shutdown:s=>o.sd.push(s)});try{h(r)}catch(e){o.threw=String(e)}return o};
const p=Proxy.revocable({}, {});p.revoke();
const stackThrow=Object.create(Error.prototype,{message:{value:'m'},stack:{get(){throw new Error('s')}}});
const symMsg=Object.create(Error.prototype,{message:{value:Symbol('x')}});
const strThrow={toString(){throw new Error('t')}};
const nullp=Object.create(null);
for (const [n,r] of [['revoked',p.proxy],['stackGetterThrows',stackThrow],['symbolMessage',symMsg],['toStringThrows',strThrow],['nullProto',nullp],['plain Error',new Error('ok')]]) for (const m of ['survive','exit']) console.log(n,m,JSON.stringify(mk(m,r)).slice(0,200));
