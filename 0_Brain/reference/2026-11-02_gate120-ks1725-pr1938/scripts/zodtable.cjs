const {z}=require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate120-ks1725-pr1938/repo/Blockchain/Dev/node_modules/zod');
// identity of errors/issues
const r=z.object({a:z.string(),b:z.number()}).safeParse({a:1});
console.log('same array:',r.error.errors===r.error.issues,'JSON eq:',JSON.stringify(r.error.errors)===JSON.stringify(r.error.issues),'n=',r.error.issues.length);
const e2=new z.ZodError([]); e2.addIssue({code:'custom',path:[],message:'x'}); console.log('after addIssue same:',e2.errors===e2.issues);
// record table: base one-arg vs head two-arg, per value schema
const vals={string:z.string(),unknown:z.unknown()};
const inputs=[{},{a:'x'},{a:1},{'1':'x'},{'':'x'},{__proto__x:'p'},JSON.parse('{"__proto__":"x"}'),Object.create({inh:'x'}),[], ['x'],null,'s',42,undefined,new Map(),Object.assign(Object.create(null),{k:'v'}),{a:undefined},{[Symbol('s')]:'x'},new Date()];
let diffs=0,tot=0;
for(const [vn,v] of Object.entries(vals)){
  const base=z.record(v), head=z.record(z.string(),v);
  for(const i of inputs){ tot++;
    const a=base.safeParse(i), b=head.safeParse(i);
    const sa=JSON.stringify([a.success,a.success?a.data:a.error.issues]), sb=JSON.stringify([b.success,b.success?b.data:b.error.issues]);
    const lab=(()=>{try{return JSON.stringify(i)}catch{return String(i)}})();
    console.log(vn.padEnd(8),String(lab).slice(0,30).padEnd(32),a.success?'ok':'REJ',b.success?'ok':'REJ',sa===sb?'same':'DIFF');
    if(sa!==sb)diffs++;
  }
}
console.log('cells',tot,'diffs',diffs);
// shape equality of schema: _def
const s1=z.record(z.string()), s2=z.record(z.string(),z.string());
console.log('keyType kind base:',s1._def.keyType._def.typeName,'head:',s2._def.keyType._def.typeName);
// ZodError ordering/object-level multi issue message
const sch=z.object({x:z.string(),y:z.record(z.string(),z.string()),z:z.number().min(3)});
const rr=sch.safeParse({x:1,y:{a:2},z:1});console.log(JSON.stringify(rr.error.errors)===JSON.stringify(rr.error.issues),rr.error.issues.length);
