// prints a compact base-vs-head table from two jsonl files; marks head MORE permissive than base
const fs=require('fs');const rd=f=>fs.readFileSync(f,'utf8').trim().split('\n').map(JSON.parse);
const [b,h]=[rd(process.argv[2]),rd(process.argv[3])];
const c=x=>x.s==='resolved'?(Array.isArray(x.v?.attributed)?'['+x.v.len+(x.v.len?':'+x.v.attributed.join(','):'')+']':String(x.v)):x.s==='rejected'?'REJ('+x.type+(x.code?' '+x.code:'')+')':'PENDING';
const perm=x=>x.s==='resolved'?(x.v===true?2:(x.v?.len??0)):0; // higher = more permissive
let more=0,cells=0;
for(let i=0;i<b.length;i++){const B=b[i],H=h[i];if(B.kind!==H.kind||B.strict!==H.strict)throw new Error('misaligned '+i);
 const keys=['trustedForeign','trustedGenuine','filter','load'];let flag=[];
 for(const k of keys){cells++;if(k!=='load'&&perm(H[k])>perm(B[k])){more++;flag.push(k)}}
 console.log(`${B.strict?'STRICT':'nonstr'} ${B.kind.padEnd(36)} | base tF=${c(B.trustedForeign)} tG=${c(B.trustedGenuine)} f=${c(B.filter)} load=${c(B.load)} | head tF=${c(H.trustedForeign)} tG=${c(H.trustedGenuine)} f=${c(H.filter)} load=${c(H.load)}${H.afterRelease?' | afterRelease b='+c(B.afterRelease)+' h='+c(H.afterRelease)+' ('+H.afterRelease.ms+'ms)':''}${flag.length?'  <<< HEAD MORE PERMISSIVE: '+flag:''}`);}
console.log(`cells ${cells}, head more permissive than base: ${more}`);
