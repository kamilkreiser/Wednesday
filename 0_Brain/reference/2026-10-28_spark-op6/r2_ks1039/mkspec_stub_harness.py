import sys
full,mode,out=sys.argv[1:4]
t=open(full).read()
i=t.index("  test('2.4.6:"); j=t.index("  test('2.4.7:")
blk=t[i:j]
hdr='''import { test, expect } from '@playwright/test';
import * as http from 'http';
const TEST_PASSWORD='x'; let base=''; let srv: http.Server;
function getBaseUrl(){ return base; }
function uniqueEmail(){ return 'a+'+Date.now()+'@agentmail.to'; }
test.beforeAll(async()=>{ srv=http.createServer((rq,rs)=>{ let b=''; rq.on('data',c=>b+=c); rq.on('end',()=>{ const d=JSON.parse(b); let n=d.name; if(%s) n=n.replace(/[;']/g,''); rs.writeHead(201,{'content-type':'application/json'}); rs.end(JSON.stringify({success:true,data:{accessToken:'t',user:{id:'u',email:d.email,displayName:n,role:'OWNER'}}})); }); }); await new Promise<void>(r=>srv.listen(0,'127.0.0.1',()=>r())); base='http://127.0.0.1:'+(srv.address() as any).port+'/'; });
test.afterAll(()=>{ srv.close(); });
test.describe('stub',()=>{
''' % ('true' if mode=='strip' else 'false')
open(out,'w').write(hdr+blk+"});\n")
