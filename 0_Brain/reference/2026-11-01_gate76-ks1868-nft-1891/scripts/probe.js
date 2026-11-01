const {proxy,revoke}=Proxy.revocable({}, {}); revoke();
const g=Object.create(Error.prototype,{message:{get(){throw new Error('b')}}});
const np=Object.create(null);
function read(err){let r;try{r=err instanceof Error?err.message:String(err)}catch{r='unreadable thrown value'}return r}
function oldread(err){return err instanceof Error?err.message:String(err)}
for (const [n,v] of [['revoked',proxy],['getter',g],['nullproto',np],['string','s'],['undefined',undefined],['symbol',Symbol('x')]]) {
  let o; try{o=oldread(v)}catch(e){o='THROWS '+e.constructor.name}
  console.log(n,'| old:',typeof o==='symbol'?'sym':o,'| new:',read(v));
}
