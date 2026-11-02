// Gate 140: gate 135's driver.cjs (REAL shared validateBody -> errorHandler 422, and validation.validateBody 400),
// with F4 cases built the way each tree's request sites build them (base z.nativeEnum, head zod3NativeEnum),
// plus the delta cases (F1 on every type, F2 trim, F2xF3 in a union, nested F3, F4 NaN/Infinity/strings).
// usage: node driver140.cjs <DevDir> <base|head> <outJson>
const path=require('path'); const DEV=process.argv[2], side=process.argv[3]; const {createRequire}=require('module'); const req=createRequire(path.join(DEV,'package.json'));
const compat = side==='head' ? require(path.join(DEV,'packages/shared/dist/validation/zod3-compat.js')) : null;
const shared=require(path.join(DEV,'packages/shared/dist/index.js'));
const mw=require(path.join(DEV,'packages/shared/dist/middleware/index.js'));
const val=require(path.join(DEV,'packages/shared/dist/validation/index.js'));
const {z}=req('zod');
const NE = (e) => side==='head' && !process.env.G140_RAWNE ? compat.zod3NativeEnum(e) : z.nativeEnum(e);
const DT = (o) => side==='head' ? compat.zod3Datetime(o) : z.string().datetime(o);
const Tier={BASIC:'basic',STANDARD:'standard',PREMIUM:'premium'}; const Num={A:0,B:1}; const Mixed={A:'a',B:2};
const cases={
  control_missing:[z.object({name:z.string()}),{}],
  F1_iso_missing:[z.object({d:shared.isoDateTimeSchema}),{}],
  F1_iso_null:[z.object({startDate:shared.isoDateTimeSchema.optional()}),{startDate:null}],
  F1_iso_number:[z.object({startDate:shared.isoDateTimeSchema.optional()}),{startDate:20261102}],
  F1_iso_bool:[z.object({d:shared.isoDateTimeSchema}),{d:true}],
  F1_iso_array:[z.object({d:shared.isoDateTimeSchema}),{d:[]}],
  F1_iso_object:[z.object({d:shared.isoDateTimeSchema}),{d:{}}],
  F1_iso_badformat:[z.object({d:shared.isoDateTimeSchema}),{d:'not-a-date'}],
  F1_iso_empty:[z.object({d:shared.isoDateTimeSchema}),{d:''}],
  F1_iso_ok:[z.object({d:shared.isoDateTimeSchema}),{d:'2026-11-02T10:00:00+10:00'}],
  F1_iso_nooffset_seconds_less:[z.object({d:shared.isoDateTimeSchema}),{d:'2026-11-02T10:00Z'}],
  F1_dt_msg_null:[z.object({d:DT({message:'M'})}),{d:null}],
  F1_dt_nomsg_null:[z.object({d:DT({})}),{d:null}],
  F1_dt_nomsg_bad:[z.object({d:DT({})}),{d:'x'}],
  F2_array_into_min_string:[z.object({title:z.string().trim().min(3).max(200)}),{title:['a','b','c','d']}],
  F2_trim_min_given_empty_array:[z.object({title:z.string().trim().min(3).max(200)}),{title:[]}],
  F2_trim_min_given_long_array:[z.object({title:z.string().trim().min(3).max(5)}),{title:[1,2,3,4,5,6,7]}],
  F2_min_given_empty_array:[z.object({p:z.string().min(8)}),{p:[]}],
  F2_string_into_min_array:[z.object({ids:z.array(z.string()).min(2)}),{ids:'x'}],
  F2_string_into_length_array:[z.object({ids:z.array(z.string()).length(3)}),{ids:'abcd'}],
  F2_int_keeps_check:[z.object({n:z.number().int().min(5)}),{n:1.5}],
  F3a_array_min_bad_elems:[z.object({ids:z.array(z.string().min(3)).min(2)}),{ids:['a']}],
  F3_nested:[z.object({m:z.array(z.array(z.string().min(2)).min(2)).min(2)}),{m:[['a']]}],
  F3_siblings:[z.object({a:z.string(),ids:z.array(z.number()).min(3),b:z.string()}),{a:1,ids:['x'],b:2}],
  F2xF3_union:[z.object({u:z.union([z.array(z.string().min(3)).min(2), z.string().min(5)])}),{u:['a']}],
  F2xF3_union_str:[z.object({u:z.union([z.array(z.string().min(3)).min(2), z.string().min(5)])}),{u:'ab'}],
  F3b_array_over_max_bad_elems:[z.object({ids:z.array(z.string().min(3)).max(2)}),{ids:['a','b','c']}],
  F4_number:[z.object({tier:NE(Tier)}),{tier:1}],
  F4_zero:[z.object({tier:NE(Tier)}),{tier:0}],
  F4_float:[z.object({tier:NE(Tier)}),{tier:1.5}],
  F4_string_bad:[z.object({tier:NE(Tier)}),{tier:'gold'}],
  F4_string_ok:[z.object({tier:NE(Tier)}),{tier:'premium'}],
  F4_key_not_value:[z.object({tier:NE(Tier)}),{tier:'PREMIUM'}],
  F4_bool:[z.object({tier:NE(Tier)}),{tier:true}],
  F4_null:[z.object({tier:NE(Tier)}),{tier:null}],
  F4_missing:[z.object({tier:NE(Tier)}),{}],
  F4_missing_optional:[z.object({tier:NE(Tier).optional()}),{}],
  F4_number_optional:[z.object({tier:NE(Tier).optional()}),{tier:7}],
  F4_array:[z.object({tier:NE(Tier)}),{tier:[]}],
  F4_numeric_enum_ok:[z.object({n:NE(Num)}),{n:1}],
  F4_numeric_enum_bad:[z.object({n:NE(Num)}),{n:5}],
  F4_numeric_enum_keystr:[z.object({n:NE(Num)}),{n:'A'}],
  F4_numeric_enum_numstr:[z.object({n:NE(Num)}),{n:'1'}],
  F4_mixed_bad:[z.object({n:NE(Mixed)}),{n:3}],
  T1_safe_int:[z.object({n:z.number().int()}),{n:2**53}],
};
const out={};
for (const [k,[schema,body]] of Object.entries(cases)) {
  for (const [label,mwfn] of [['mw.validateBody+errorHandler',mw.validateBody],['validation.validateBody',val.validateBody]]) {
    let status=0, json=null; const res={status(s){status=s;return this;},json(j){json=j;return this;},setHeader(){},getHeader(){},headersSent:false,locals:{}};
    const rq={body, headers:{}, method:'POST', path:'/x', originalUrl:'/x', url:'/x', ip:'127.0.0.1', get(){return undefined;}, header(){return undefined;}};
    let nextErr=null; mwfn(schema)(rq,res,(e)=>{nextErr=e||null;});
    if (nextErr) { try { shared.errorHandler(nextErr, rq, res, ()=>{}); } catch(e){ json={THROW:String(e)}; } }
    out[k+' | '+label]={status, body: json, nextOk: !nextErr && status===0};
  }
}
// raw safeParse for values JSON cannot carry (NaN, Infinity), F4
for (const [k,v] of [['NaN',NaN],['Infinity',Infinity],['-Infinity',-Infinity]]) { const r=z.object({tier:NE(Tier)}).safeParse({tier:v}); out['F4_raw_'+k]=r.success?'OK':(side==='head'?compat.zod3Issues(r.error.issues):r.error.issues); }
require("fs").writeFileSync(process.argv[4], JSON.stringify(out,null,1));
