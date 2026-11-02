const D='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968/repo/Blockchain/Dev/services/vc-issuer';
const t=process.hrtime.bigint(); try{ require(require.resolve('@secuura/shared',{paths:[D]})); }catch(e){console.log('err',String(e).slice(0,100));}
console.log('require @secuura/shared ms', Number(process.hrtime.bigint()-t)/1e6); console.log(require('os').loadavg());
